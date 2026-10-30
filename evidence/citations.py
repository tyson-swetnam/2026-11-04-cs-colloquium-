"""Check a citation against real indexes: the DOI registry (doi.org) and arXiv.

A citation passes only if an index returns a record whose title matches the cited title
and whose authors share at least one surname with the cited authors. Everything else is
flagged, with the reason:

    bad_identifier       the DOI is not registered, or the arXiv ID is malformed or unused
    identifier_mismatch  the identifier exists but belongs to a different work
    author_mismatch      the title exists, but none of the cited authors wrote it
    not_found            no identifier, and title search found nothing (needs a human or a wider index)

Responses are cached on disk, so a rerun makes no network calls.
"""

from __future__ import annotations

import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import quote

from evidence.http import CachedGet

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_ID = re.compile(r"arXiv[:\s]*((?:\d{4}\.[\dX]{4,5})|(?:[a-z\-]+/\d{7}))(v\d+)?", re.I)
DOI = re.compile(r"\b(10\.\d{4,9}/[^\s,;}]+[^\s,;.}])", re.I)
STOPWORDS = {"with", "from", "that", "this", "into", "over", "your", "their", "what", "when", "which", "towards", "toward", "using", "via", "than"}
SKIP_SURNAME = {"al", "et", "others", "jr", "sr", "ii", "iii", "lastname", "and"}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def surname(name: str) -> str | None:
    tokens = [t for t in normalize(name).split() if t not in SKIP_SURNAME and len(t) > 1]
    return tokens[-1] if tokens else None


@dataclass
class Citation:
    raw: str
    title: str = ""
    surnames: list[str] = field(default_factory=list)
    doi: str | None = None
    arxiv_id: str | None = None


def _split_authors(block: str) -> list[str]:
    names = re.split(r",\s*|\s+and\s+", block)
    return [s for s in (surname(n) for n in names) if s]


def _identifiers(text: str) -> tuple[str | None, str | None]:
    # Re-join a DOI split after its slash ("10.1109/ TNNLS.2021..."), but keep other spaces as delimiters.
    joined = re.sub(r"(\b10\.\d{4,9}/)\s+", r"\1", text)
    doi = DOI.search(joined)
    ax = ARXIV_ID.search(text)
    # "arXiv preprint arXiv" with no number is not an identifier
    return (doi.group(1).rstrip(".") if doi else None), (ax.group(1) if ax else None)


def parse(raw: str) -> Citation:
    """A plain-text reference in the usual 'Authors. Title. Venue, year.' form."""
    text = re.sub(r"\s+", " ", raw).strip()
    cuts = []
    for m in re.finditer(r"[.?!]\s+", text):
        before = text[: m.start()].split()[-1] if text[: m.start()].split() else ""
        if re.fullmatch(r"[A-Z]|[A-Z]\.[A-Z]|[A-Z][a-z]?", before.rstrip(".")) and before not in ("al",):
            continue  # an initial, e.g. "A. Yang"
        cuts.append(m.end())
        if len(cuts) == 2:
            break
    authors = text[: cuts[0]] if cuts else ""
    title = text[cuts[0] : cuts[1]] if len(cuts) == 2 else text[cuts[0] :] if cuts else text
    doi, ax = _identifiers(text)
    return Citation(raw=text, title=title.strip(" ."), surnames=_split_authors(authors.rstrip(". ")), doi=doi, arxiv_id=ax)


def _delatex(s: str) -> str:
    s = re.sub(r"\\url\{[^}]*\}", "", s)
    s = re.sub(r"\\doi\{([^}]*)\}", r"doi: \1", s)
    s = re.sub(r"\\(emph|textit|textbf|textsc)\{", "{", s)
    s = re.sub(r"\\['`^\"~=.]\{?(\w)\}?", r"\1", s)
    s = s.replace("~", " ").replace("``", '"').replace("''", '"').replace("--", "-")
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def parse_bibitem(entry: str) -> Citation:
    """One \\bibitem from a natbib .bbl file: blocks separated by \\newblock (authors, title, venue)."""
    body = re.sub(r"^\\bibitem(\[.*?\])?\{[^}]*\}", "", entry.strip(), flags=re.S)
    blocks = [_delatex(b) for b in body.split("\\newblock")]
    authors = re.sub(r"\.?\s*\d{4}[a-z]?\.?$", "", blocks[0]).strip(" .")
    title = blocks[1].strip(" .") if len(blocks) > 1 else ""
    raw = " ".join(blocks)
    doi, ax = _identifiers(raw)
    return Citation(raw=raw, title=title, surnames=_split_authors(authors), doi=doi, arxiv_id=ax)


def bibitems(bbl: str) -> list[str]:
    return [("\\bibitem" + p) for p in bbl.split("\\bibitem")[1:]]


@dataclass
class Result:
    verdict: str
    detail: str = ""
    index_title: str = ""

    @property
    def verified(self) -> bool:
        return self.verdict == "verified"


class Checker:
    def __init__(self, cache_dir: Path, user_agent: str):
        self._get = CachedGet(cache_dir, user_agent)

    # --- DOI registry ---------------------------------------------------------------
    def doi_record(self, doi: str) -> dict | None:
        status, body = self._get(f"https://doi.org/api/handles/{quote(doi)}")
        if status != 200 or '"responseCode":1' not in body.replace(" ", ""):
            return None
        status, body = self._get(f"https://doi.org/{quote(doi)}", accept="application/vnd.citationstyles.csl+json")
        record = {"title": "", "surnames": []}
        if status == 200 and body.lstrip().startswith("{"):
            import json

            meta = json.loads(body)
            title = meta.get("title", "")
            record["title"] = title[0] if isinstance(title, list) and title else title
            record["surnames"] = [normalize(a.get("family", "")) for a in meta.get("author", []) if a.get("family")]
        return record

    # --- arXiv ------------------------------------------------------------------------
    def _arxiv_entries(self, query: str) -> list[dict]:
        status, body = self._get(f"https://export.arxiv.org/api/query?{query}")
        if status != 200:
            return []
        out = []
        for e in ET.fromstring(body).findall(f"{ATOM}entry"):
            title = (e.findtext(f"{ATOM}title") or "").strip()
            if not title or title == "Error":
                continue
            out.append(
                {
                    "id": (e.findtext(f"{ATOM}id") or "").rsplit("/abs/", 1)[-1],
                    "title": re.sub(r"\s+", " ", title),
                    "surnames": [s for s in (surname(a.findtext(f"{ATOM}name") or "") for a in e.findall(f"{ATOM}author")) if s],
                }
            )
        return out

    def arxiv_record(self, arxiv_id: str) -> dict | None:
        hits = self._arxiv_entries(f"id_list={arxiv_id}&max_results=1")
        return hits[0] if hits else None

    def arxiv_search(self, title: str) -> list[dict]:
        """Title search on distinctive whole words; arXiv's index drops stop words and splits hyphens."""
        words = [normalize(w) for w in title.split() if "-" not in w and "/" not in w]
        words = [w for w in words if len(w) >= 4 and w not in STOPWORDS and " " not in w]
        for n in (6, 4):
            if len(words) < 2:
                return []
            q = "+AND+".join(f"ti:{quote(w)}" for w in words[:n])
            hits = self._arxiv_entries(f"search_query={q}&max_results=5")
            if hits:
                return hits
        return []

    # --- verdict ----------------------------------------------------------------------
    def _authors_ok(self, cited: list[str], found: list[str]) -> bool:
        return not cited or bool(set(cited) & set(found))

    def check(self, c: Citation) -> Result:
        if c.arxiv_id:
            if "X" in c.arxiv_id.upper().split(".")[-1]:
                return Result("bad_identifier", f"arXiv:{c.arxiv_id} is incomplete")
            rec = self.arxiv_record(c.arxiv_id)
            if rec is None:
                return Result("bad_identifier", f"arXiv:{c.arxiv_id} does not exist")
            if c.title and similar(c.title, rec["title"]) < 0.85:
                return Result("identifier_mismatch", f"arXiv:{c.arxiv_id} is a different paper", rec["title"])
            if not self._authors_ok(c.surnames, rec["surnames"]):
                return Result("author_mismatch", "no cited author on the arXiv record", rec["title"])
            return Result("verified", f"arXiv:{c.arxiv_id}", rec["title"])
        if c.doi:
            rec = self.doi_record(c.doi)
            if rec is None:
                return Result("bad_identifier", f"DOI {c.doi} is not registered")
            if c.title and rec["title"] and similar(c.title, rec["title"]) < 0.85:
                return Result("identifier_mismatch", f"DOI {c.doi} is a different work", rec["title"])
            if rec["surnames"] and not self._authors_ok(c.surnames, rec["surnames"]):
                return Result("author_mismatch", "no cited author on the DOI record", rec["title"])
            return Result("verified", f"doi:{c.doi}", rec["title"])
        if c.title:
            hits = [h for h in self.arxiv_search(c.title) if similar(c.title, h["title"]) >= 0.85]
            if hits:
                best = max(hits, key=lambda h: similar(c.title, h["title"]))
                if self._authors_ok(c.surnames, best["surnames"]):
                    return Result("verified", f"arXiv title match {best['id']}", best["title"])
                return Result("author_mismatch", f"title exists as arXiv:{best['id']} with other authors", best["title"])
        return Result("not_found", "no identifier; title not found on arXiv")
