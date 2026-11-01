# Slide 33 · Paste our URL into any chat

Section: 04 · Stop worrying · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-33)

Added 2026-11-01 after slide 32. It shows the new CARC website and its documentation site, which is published for people and for AI agents. The screenshots were supplied by the speaker. `src/03_place_slide.py` builds the slide. The "Try it in any chat" prompt rises in on the first click.

## Findings (checked 2026-11-01)

All 13 quotes in [`facts.csv`](data/raw/research/facts.csv) match the live pages word for word ([`quote_check.csv`](data/processed/quote_check.csv)).

| Claim | Verdict | Key evidence |
|---|---|---|
| c2 Docs published "for people and for AI agents", an OKF v0.2 bundle | supported | [For AI agents](https://carc.unm.edu/docs/about/ai-agents/) page |
| c3 `/llms.txt` outlines ~80 pages; `<page>/index.md` gives the Markdown with OKF frontmatter | supported | llms.txt lists **80** pages with Markdown twins ([`llms_txt_pages.json`](data/processed/llms_txt_pages.json)) |
| c4 `/llms-full.txt`, ~180K tokens | supported | The site's own estimate: "about 696 KB, roughly 178,000 tokens" |
| c5 Example prompt (H100 access on Easley) | partially supported | The FAQ has the answer: group-gated partitions, ColdFront allocation requested by the PI. The prompt was not run against a chat assistant from here, so **run it once before the talk**. |
| c7 OKF v0.2; llms.txt | supported | OKF spec (GoogleCloudPlatform/knowledge-catalog); llmstxt.org |

Notes:
- An earlier draft asked how to set up project scratch on Hopper. The storage page says "There is no `/hopper/scratch`", so a live demo could have failed. The prompt now asks a question the docs answer directly.
- The For AI agents page's frontmatter says it was AI-generated (`generated.by: claude/fable-5-1`) and has no human `verified` entry. Worth a human review, since the slide puts it on screen.
- The `index.md` twins were served with no `Content-Type` header on 2026-11-01, although llms.txt says `text/markdown`. Agents still read them, but the header is worth fixing.
- The carc.unm.edu home page itself does not mention AI agents. That messaging is in the docs, `llms.txt` and `robots.txt`.

## Reproduce

```
uv run python slides/33-carc-docs-for-ai-agents/src/01_fetch_sources.py   # live pages -> data/raw/sources/ (+ MANIFEST.yaml)
uv run python slides/33-carc-docs-for-ai-agents/src/02_check_facts.py     # quotes word for word; count pages in llms.txt
uv run python slides/33-carc-docs-for-ai-agents/src/03_place_slide.py     # insert/refresh the slide (idempotent)
```
