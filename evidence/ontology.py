"""Validate ontology terms through EBI's Ontology Lookup Service (OLS4).

The control on slide 17 ("terms must resolve in an ontology") and the examples on slide 25
use this: an agent proposes a CURIE for a free-text value, and the write is refused unless
the term exists, is not obsolete, comes from the ontology the field allows, and its label,
synonyms or alternative labels match the text that was written.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from evidence.http import CachedGet

OLS = "https://www.ebi.ac.uk/ols4/api"
# Annotation properties that carry alternative names in OBO ontologies (e.g. OBI, CLO).
NAME_ANNOTATIONS = ("alternative label", "alternative term", "editor preferred term", "exact synonym", "related synonym")


def norm(text: str) -> str:
    """Lower-case alphanumerics; NFKD first so that "mm²" reads as "mm2"."""
    return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", text).lower()).strip()


@dataclass
class Term:
    curie: str
    label: str
    names: list[str] = field(default_factory=list)  # label + synonyms + alternative labels
    obsolete: bool = False
    iri: str = ""
    ontology: str = ""


class OLSClient:
    def __init__(self, cache_dir: Path, user_agent: str):
        self.get = CachedGet(cache_dir, user_agent)

    def term(self, curie: str) -> Term | None:
        prefix = curie.split(":", 1)[0].lower()
        status, body = self.get(f"{OLS}/ontologies/{prefix}/terms?obo_id={quote(curie)}")
        if status != 200:
            return None
        terms = json.loads(body).get("_embedded", {}).get("terms", [])
        defining = [t for t in terms if t.get("is_defining_ontology")] or terms
        if not defining:
            return None
        t = defining[0]
        names = [t["label"], *(t.get("synonyms") or [])]
        for key in NAME_ANNOTATIONS:
            names += (t.get("annotation") or {}).get(key, [])
        return Term(curie, t["label"], list(dict.fromkeys(names)), bool(t.get("is_obsolete")), t.get("iri", ""), t.get("ontology_name", ""))

    def ancestors(self, curie: str) -> list[tuple[str, str]]:
        t = self.term(curie)
        if t is None:
            return []
        iri = quote(quote(t.iri, safe=""), safe="")
        status, body = self.get(f"{OLS}/ontologies/{t.ontology}/terms/{iri}/hierarchicalAncestors?size=500")
        if status != 200:
            return []
        return [(a.get("obo_id"), a.get("label")) for a in json.loads(body).get("_embedded", {}).get("terms", [])]


HEAD_NOUNS = (" cell line", " cells", " cell", " assay")


def _forms(name: str) -> set[str]:
    """Spacing-, plural- and head-noun-insensitive forms of a name: 'RNA-seq assay' -> {'rnaseqassay', 'rnaseq'}."""
    n = norm(name)
    forms = {n}
    for head in HEAD_NOUNS:
        if n.endswith(head) and len(n) > len(head):
            forms.add(n[: -len(head)])
    forms |= {re.sub(r"s$", "", f) for f in forms}
    return {f.replace(" ", "") for f in forms}


def names_match(text: str, names: list[str]) -> bool:
    """The written text is one of the term's names (up to spacing, plurals, a head noun) or an abbreviated binomial."""
    written = _forms(text)
    for name in names:
        if written & _forms(name):
            return True
        parts = norm(name).split()
        if len(parts) == 2 and re.fullmatch(rf"{parts[0][0]} {parts[1]}", norm(text)):  # "M. musculus"
            return True
    return False


@dataclass
class Check:
    ok: bool
    reason: str
    label: str = ""


def validate(client: OLSClient, text: str, curie: str, allowed_prefixes: tuple[str, ...]) -> Check:
    prefix = curie.split(":", 1)[0]
    if prefix not in allowed_prefixes:
        return Check(False, f"{prefix} is not allowed for this field (expects {', '.join(allowed_prefixes)})")
    t = client.term(curie)
    if t is None:
        return Check(False, f"{curie} does not exist in OLS")
    if t.obsolete:
        return Check(False, f"{curie} is obsolete", t.label)
    if not names_match(text, t.names):
        return Check(False, f"'{text}' does not match {curie} ({t.label})", t.label)
    return Check(True, "resolves", t.label)
