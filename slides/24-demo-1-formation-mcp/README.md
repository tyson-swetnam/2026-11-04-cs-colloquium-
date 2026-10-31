# Slide 24 · Demo 1: Formation MCP

> **Revised deck.** Demo 1 in the revised deck (2026-10-31) is Formation MCP: four agents reaching the same MESA servers. It was a rogue agent meeting the policy engine (c1, superseded).

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-24)

## Findings (checked 2026-10-31)

Checked against MESA's public docs (idss-mesa.github.io), CyVerse's core software docs (docs.cyverse.org) and the NSF Award API. No MESA or CyVerse code was read, and no recorded demo run is in this folder.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c2 · All four agents connect to the same servers without custom integration | partially supported | All four speak MCP (slide 15); the installer registers all three servers in every client. But Formation sign-in is confirmed only for Claude; Codex/OpenCode callbacks are rejected and Antigravity is untested (facts f3-f6, f17) | "All four agents speak MCP and register the same servers; Formation sign-in is confirmed today for Claude, with Codex, Antigravity and OpenCode in progress." |
| c3 · Formation launches apps and jobs on CyVerse Kubernetes; Data Store MCP finds, reads and writes iRODS data | partially supported | Interactive apps run on Kubernetes (f9, f12). Batch jobs: Argo on Kubernetes (f10) vs HTCondor (f11, f13). The CyVerse pages disagree. Writes need a CyVerse sign-in; anonymous access is read-only (f14-f16) | "Formation launches CyVerse apps and analyses (interactive apps run on Kubernetes); the Data Store servers find and read data in iRODS, and write it once you sign in." |
| c4 (new) · Formation and Data Store are "MESA MCP servers" | partially supported | Formation is CyVerse's own hosted server; MESA only registers it (f1, f2) | "MCP servers MESA installs: CyVerse Formation + MESA Data Store" |
| c5 (new) · Notes: both agents reach the same servers and the same data | partially supported | Same Data Store, but in the MESA apps each agent has a different irods instance: hosted for Claude Code and OpenCode, local for Codex and Antigravity (f18, f19) | "Show both agents call the same tools and get the same Data Store data." |
| c6 (new) · Footer NSF Award #2632685 | supported | NSF API: MESA, University of New Mexico, NAIRR program, started 07/15/2026 (f21) | — |

**Demo risk:** for "the same request from two agents", only Claude surfaces (claude.ai, Desktop, Claude Code) are documented to complete Formation's sign-in. Rehearse any Codex or Antigravity Formation call, or demo the second agent on Data Store requests.

**Timing mismatch:** the slide says "Target length ~1:30" and the notes say "[~2 min]". Pick one.

## Evidence

- `src/01_check.py` fetches the pages (cached in `data/cache/`, saved in `data/raw/sources/`, gitignored) and checks every quote → `data/processed/checks.csv`, `data/processed/nsf_award.csv`.
- `data/raw/research/facts.csv`: exact quotes with source URLs.
- MCP support in each client: [`../15-plain-language-definitions/data/processed/mcp_support.csv`](../15-plain-language-definitions/data/processed/mcp_support.csv).
