# Slide 34 · Self-hosted AI helps answer our tickets

Section: 04 · Stop worrying · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-34)

Added 2026-11-01 after slide 33. It shows a real CARC help-desk ticket with an AI Summary panel, produced by an open-weight model self-hosted on two NVIDIA DGX Spark systems. That model has been trained to use the knowledge in CARC's previous tickets. `src/03_place_slide.py` builds the slide.

## The screenshot

[`figures/ticket_ai_summary_redacted.webp`](figures/ticket_ai_summary_redacted.webp) is the speaker's screenshot of ticket #208200 (Oct. 28, 2026). The speaker had already blurred the requester's name and email address. Because the deck is published on a public site, this copy also covers:

- the requester's initials (avatar),
- their group's scratch-directory name, which could identify the group,
- a staff email address.

The staff member's name stays, since the summary's point is what staff did. The unredacted original is not in the repository.

## Findings (checked 2026-11-01)

| Claim | Verdict | Key evidence |
|---|---|---|
| c1 AI Summary on a real ticket | supported | The screenshot |
| c2 Open-weight model, self-hosted on 2× DGX Spark | **unverified** (CARC's own account) | No public source |
| c3 Each up to 128 GB unified memory and 1 petaFLOP (FP4) | supported | NVIDIA product page and hardware guide; 8/8 quotes match ([`quote_check.csv`](data/processed/quote_check.csv)) |
| c5 Trained to use the knowledge of every previous ticket | **unverified** (CARC's own account) | Be ready to say whether this is fine-tuning or retrieval (RAG), and how requester data is protected |
| c6 Ticket text is not sent to an outside AI service | **unverified** | Holds if the help desk's AI provider points only at the local server, with no cloud fallback |

Notes:
- "Up to" is deliberate. NVIDIA's 1 petaFLOP is FP4 with sparsity, and DGX Spark also comes in a 64 GB OEM configuration. If CARC's units are the 128 GB model, the memory figure can drop "up to".
- Two Sparks linked by a single QSFP cable can serve models up to ~400B parameters (product page; the hardware guide says 405B).
- The panel headings ("Customer Intent", "Conversation Summary") match [Zammad's AI Ticket Summary](https://admin-docs.zammad.org/en/latest/ai/summary.html), which can use a self-hosted Ollama server. That CARC's help desk is Zammad is an inference and is not on the slide.

## Reproduce

```
uv run python slides/34-ai-on-the-help-desk/src/01_fetch_sources.py   # NVIDIA pages -> data/raw/sources/ (+ MANIFEST.yaml)
uv run python slides/34-ai-on-the-help-desk/src/02_check_facts.py     # quotes word for word
uv run python slides/34-ai-on-the-help-desk/src/03_place_slide.py     # insert/refresh the slide (idempotent)
```
