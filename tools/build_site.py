"""Build the GitHub Pages site: the full deck plus one evidence page per slide.

    python tools/build_site.py _site

Layout of the output (it mirrors the repository, so relative links in the READMEs keep working):
    index.html              landing page: the talk, the deck, every slide with its claim status
    deck/index.html         talk/deck.html, unchanged
    talk/index.html         talk/slides.md (slide text and speaker notes)
    claims/index.html       CLAIMS.md (the claims register)
    slides/NN-*/index.html  each slide's README.md, its claims table, figures inline
Links to other repository files (data, code, claims.yaml) point at GitHub.
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/tyson-swetnam/2026-11-04-cs-colloquium-"
BLOB = f"{REPO_URL}/blob/main"
TITLE = "How I Learned to Stop Worrying and Love the AI"
ICON = {
    "supported": "✅", "partially-supported": "🟧", "contradicted": "❌", "revise-slide": "✏️",
    "unverified": "⬜", "in-progress": "🟨", "not-applicable": "➖", "superseded": "🗄️",
}

CSS = """
:root{--bg:#fff;--fg:#1a1a1a;--muted:#5f5f5f;--line:#e3e3e3;--accent:#ba0c2f;--code:#f5f5f4;--link:#1c5cab}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--fg:#ececec;--muted:#a8a8a8;--line:#333;--accent:#ff5a74;--code:#222;--link:#86b6ef}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
header{border-top:8px solid var(--accent);padding:20px 16px 8px}main{max-width:1060px;margin:0 auto;padding:0 16px 48px}
header .inner{max-width:1060px;margin:0 auto}header a{color:var(--muted);text-decoration:none;margin-right:16px;font-size:14px}
h1{font-size:2rem;line-height:1.2;margin:.6em 0 .3em}h2{margin-top:1.8em;border-bottom:1px solid var(--line);padding-bottom:.2em}
a{color:var(--link)}img{max-width:100%;height:auto;border:1px solid var(--line);border-radius:4px;margin:8px 0}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto;font-size:14px;margin:12px 0}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--code)}
code,pre{background:var(--code);border-radius:4px;font-size:13px}code{padding:1px 4px}pre{padding:10px;overflow-x:auto}
blockquote{margin:12px 0;padding:4px 14px;border-left:4px solid var(--accent);color:var(--muted)}
.muted{color:var(--muted)}.cta{display:inline-block;background:var(--accent);color:#fff;padding:10px 16px;border-radius:6px;text-decoration:none;font-weight:600;margin:8px 0}
"""


def page(title: str, body: str, depth: int) -> str:
    up = "../" * depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><header><div class="inner"><a href="{up}">Home</a><a href="{up}deck/">Deck</a><a href="{up}talk/">Slide text</a><a href="{up}claims/">Claims register</a><a href="{REPO_URL}">GitHub</a></div></header>
<main>{body}</main></body></html>"""


def render_md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])


def rewrite_links(body: str, src: Path, depth: int) -> str:
    """Point links at the site where a page exists, otherwise at the file on GitHub.

    `src` is the markdown file (links resolve relative to it); `depth` is how deep its page sits in the site.
    """

    def fix(m: re.Match) -> str:
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#)", url):
            return m.group(0)
        path, _, frag = url.partition("#")
        target = (src.parent / path).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        frag = f"#{frag}" if frag else ""
        if rel == "talk/slides.md":
            new = "talk/"
        elif rel == "CLAIMS.md":
            new = "claims/"
        elif rel.startswith("slides/") and (target.is_dir() or rel.endswith("README.md")):
            new = rel.removesuffix("README.md").rstrip("/") + "/"
        elif rel.startswith("slides/") and "/figures/" in rel:
            new = rel  # copied into the site
        else:
            return f'{attr}="{BLOB}/{rel}{frag}"'
        return f'{attr}="{"../" * depth}{new}{frag}"'

    return re.sub(r'(href|src)="([^"]+)"', fix, body)


def claims_table(doc: dict) -> str:
    rows = []
    for c in doc.get("claims") or []:
        new = f"<br><span class='muted'>Suggested: {html.escape(str(c['proposed_text']))}</span>" if c.get("proposed_text") and c["status"] != "superseded" else ""
        rows.append(
            f"<tr><td><code>{c['id']}</code></td><td>{html.escape(str(c['text']))}{new}</td>"
            f"<td>{ICON.get(c['status'], '')} {c['status']}</td><td>{c['kind']}</td></tr>"
        )
    if not rows:
        return ""
    return "<h2>Claims</h2><table><tr><th></th><th>Claim</th><th>Status</th><th>Kind</th></tr>" + "".join(rows) + "</table>"


def main(out: Path) -> None:
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    (out / ".nojekyll").touch()

    # the full deck, unchanged
    (out / "deck").mkdir()
    shutil.copy(ROOT / "talk" / "deck.html", out / "deck" / "index.html")

    # slide text and the claims register
    for src, dest, title in ((ROOT / "talk" / "slides.md", "talk", "Slide text and speaker notes"), (ROOT / "CLAIMS.md", "claims", "Claims register")):
        (out / dest).mkdir()
        body = rewrite_links(render_md(src.read_text(encoding="utf-8")), src, 1)
        (out / dest / "index.html").write_text(page(f"{title} · {TITLE}", body, 1), encoding="utf-8")

    # one page per slide
    listing = []
    for folder in sorted((ROOT / "slides").iterdir()):
        if not (folder / "claims.yaml").exists():
            continue
        doc = yaml.safe_load((folder / "claims.yaml").read_text(encoding="utf-8")) or {}
        dest = out / "slides" / folder.name
        dest.mkdir(parents=True)
        if (folder / "figures").is_dir():
            shutil.copytree(folder / "figures", dest / "figures", ignore=shutil.ignore_patterns("*.svg"))
        readme = folder / "README.md"
        body = rewrite_links(render_md(readme.read_text(encoding="utf-8")), readme, 2) if readme.exists() else f"<h1>Slide {doc.get('slide')}</h1>"
        body += claims_table(doc)
        body += f"<p class='muted'>Source: <a href='{REPO_URL}/tree/main/slides/{folder.name}'>slides/{folder.name}</a> · <a href='../../deck/'>open the deck</a></p>"
        (dest / "index.html").write_text(page(f"Slide {doc.get('slide', '')} · {TITLE}", body, 2), encoding="utf-8")
        counts = Counter(c["status"] for c in doc.get("claims") or [] if c["status"] != "superseded")
        listing.append((folder.name, doc, counts))

    # landing page
    rows = "".join(
        f"<tr><td>{d.get('slide', ''):>02}</td><td><a href='slides/{name}/'>{html.escape(str(d.get('title', name)))}</a></td>"
        f"<td>{html.escape(str(d.get('section', '')))}</td><td>{' '.join(f'{ICON.get(s, s)}&nbsp;{n}' for s, n in sorted(counts.items()))}</td></tr>"
        for name, d, counts in listing
    )
    total = Counter()
    for _, _, c in listing:
        total.update(c)
    summary = " · ".join(f"{ICON.get(s, s)} {s}: {n}" for s, n in total.most_common())
    body = f"""<h1>{TITLE}</h1>
<p>UNM Computer Science Colloquium · Tyson L. Swetnam · Wednesday, Nov. 4, 2026, 2 p.m. · Larrañaga Engineering Auditorium (Centennial 1041)</p>
<a class="cta" href="deck/">Open the full deck</a>
<p>Every number, attribution and technical statement in the talk has an entry below, backed by code you can rerun and data traced to its source, or marked as not yet checked. The code and data are on <a href="{REPO_URL}">GitHub</a>.</p>
<p class="muted">{summary} (superseded claims not counted)</p>
<h2>Slides</h2><table><tr><th>#</th><th>Slide</th><th>Section</th><th>Claims</th></tr>{rows}</table>"""
    (out / "index.html").write_text(page(TITLE, body, 0), encoding="utf-8")
    print(f"built {out} ({len(listing)} slide pages)")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve())
