# Slide 34 · Self-hosted AI helps answer our tickets

Section: 04 · Stop worrying · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-34)

Added 2026-11-01 after slide 33. It shows a real ticket in CARC's Zammad help desk with its AI Ticket Summary, produced by an open-weight model self-hosted on two NVIDIA DGX Spark systems (128 GB). The agent uses the knowledge in CARC's previous tickets, and tickets never leave CARC. `src/03_place_slide.py` builds the slide.

## The screenshot

[`figures/ticket_ai_summary_redacted.webp`](figures/ticket_ai_summary_redacted.webp) is the speaker's screenshot of ticket #208200 (Oct. 28, 2026). The speaker had already blurred the requester's name and email address. Because the deck is published on a public site, this copy also covers:

- the requester's initials (avatar),
- their group's scratch-directory name, which could identify the group,
- a staff email address.

The staff member's name stays, since the summary's point is what staff did. The unredacted original is not in the repository.

## Findings (checked 2026-11-01)

11/11 quotes match their sources word for word ([`quote_check.csv`](data/processed/quote_check.csv)).

| Claim | Verdict | Key evidence |
|---|---|---|
| c1 AI Summary on a real ticket in Zammad | supported | The screenshot. Zammad's docs: "Customer Intent and Conversation Summary are enabled by default"; Ollama can be the provider |
| c2 Open-weight model, self-hosted on 2× DGX Spark (128 GB model) | confirmed by CARC (2026-11-01) | Internal; no public source |
| c3 Each 128 GB unified memory, up to 1 petaFLOP (FP4) | supported | NVIDIA product page and hardware guide |
| c5 The agent *uses* the knowledge of every previous ticket | confirmed by CARC | Worded "uses", not "trained on" |
| c6 Tickets never leave CARC; they stay private | confirmed by CARC | Zammad's docs: with Ollama "your data is not transferred to a third party" |

Notes:
- The 1 petaFLOP figure is FP4 with sparsity, so it keeps "up to". The memory figure does not, because CARC's units are the 128 GB model (a 64 GB OEM version also exists).
- Two Sparks linked by a single QSFP cable can serve models up to ~400B parameters (product page; the hardware guide says 405B).
- If asked: how many past tickets the agent draws on, and which open-weight model it runs.

## Reproduce

```
uv run python slides/34-ai-on-the-help-desk/src/01_fetch_sources.py   # NVIDIA + Zammad docs -> data/raw/sources/ (+ MANIFEST.yaml)
uv run python slides/34-ai-on-the-help-desk/src/02_check_facts.py     # quotes word for word
uv run python slides/34-ai-on-the-help-desk/src/03_place_slide.py     # insert/refresh the slide (idempotent)
```
