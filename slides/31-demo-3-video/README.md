# Slide 31 · Which ground beetle is most common at Jornada?

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-31)

Added 2026-11-04. The recorded Demo 3 plays full-size, at the same layout and video size as slide 25 (1446×791 px under the heading). Slide 30 ("From question to result") introduces it. In the Claude app, a researcher asks which ground beetle is most common at NEON's Jornada Experimental Range (JORN). The agent queries the neon-beetle-seg DuckLake read-only over WebDAV, with the MESA portal alongside, and answers *Tetragonoderus pallidus*: 616 of 1,056 carabid individuals (58.3%).

- **The recording:** it stays with slide 30's evidence, in [`../30-demo-3-question-to-result/data/media/`](../30-demo-3-question-to-result/). `src/01_place_slide.py` finds that folder by name, so renumbering does not break it.
- **Playback:** it starts from the beginning each time the slide opens, holds on the answer, pauses when the slide is left, and **pauses or resumes on click**.
- **Speaker notes:** timestamps, read from the recording.
- **Still to check:** the answer, against NEON's own data. See slide 30's `src/02_jorn_carabids.py`, which needs a NEON API token.

```
uv run python slides/31-demo-3-video/src/01_place_slide.py   # insert/refresh after "From question to result" (idempotent)
```
