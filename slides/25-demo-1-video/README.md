# Slide 25 · Connect once, then just ask

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-25)

Added 2026-11-02 after slide 24 ("Formation MCP"). This is the recorded Demo 1, played on its own slide: Claude Code connects to MESA's Formation and iRODS (Data Store) MCP servers and answers plain-language requests, with the MESA portal open alongside. The slides after it moved up by one (Questions? is now 39).

## The video

- Source: the speaker's screen recording (QuickTime, 1280×700 H.264, 87.8 s, no audio), 2026-11-02. Not committed; its size and SHA-256 are in [`data/media/MANIFEST.yaml`](data/media/MANIFEST.yaml).
- For the deck: VP9 WebM at CRF 30, no audio, **1.5 MB** (from 11 MB). Terminal text stays as legible as the source (compared frame by frame). It is embedded as a data: URL, so the deck plays offline.
- On the slide it fills the space under the heading (1446×791 px). It starts from the beginning each time the slide opens, plays once and holds on its last frame, and pauses when the slide is left. **Click the video to pause or resume** it so you can talk over it. That behavior comes from the deck's shared video script in `slides/04-kubrick/src/04_place_trailer.py`.
- The poster image ([`figures/poster.webp`](figures/poster.webp), the frame at 35 s) shows before playback starts.

## What it shows (timestamps in the speaker notes)

| Time | On screen |
|---|---|
| 0:00 | `claude mcp add --transport http formation https://de.cyverse.org/formation/mcp`, the command the Formation page gives |
| 0:10 | OAuth sign-in through CyVerse in the browser: "Authentication successful. Connected to formation." |
| 0:20 | "use the formation MCP to list my running apps": one running analysis in the Discovery Environment |
| 0:35 | "give me details, and list the name": MESA KASM Ubuntu Desktop (GPU), a private interactive VICE app. The MESA portal shows the same analysis. |
| 1:10 | "use the irods mcp to list the folders in my neon-beetle-seg/ folder": the agent calls the Data Store server, and the portal's Data Browser shows that collection |

The recording ends while the iRODS request is still running, so the folder list on screen is the portal's view, not the agent's answer. The notes say so.

## Findings (checked 2026-11-02)

All five quotes from the [Formation page](https://de.cyverse.org/formation) match word for word ([`quote_check.csv`](data/processed/quote_check.csv)): the server over streamable HTTP, the one-line Claude Code command, and OAuth via CyVerse Keycloak.

## Reproduce

```
uv run python slides/25-demo-1-video/src/01_encode.py path/to/formation_irods_mcp_demo_720p.mov   # recording -> WebM + poster
uv run python slides/25-demo-1-video/src/02_place_slide.py           # insert/refresh the slide after "Formation MCP" (idempotent)
uv run python slides/25-demo-1-video/src/03_check_formation_docs.py  # live Formation page; quotes word for word
```
