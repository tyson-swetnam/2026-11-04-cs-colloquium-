# Slide 24 · Demo 1: Formation MCP

> **Revised deck.** Demo 1 in the revised deck (2026-10-31) is Formation MCP: four agents reaching the same MESA servers. It was a rogue agent meeting the policy engine (c1, superseded).

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-24)

## Findings (checked 2026-10-31)

Checked against MESA's public docs (idss-mesa.github.io), CyVerse's core software docs (docs.cyverse.org) and the NSF Award API. No MESA or CyVerse code was read, and no recorded demo run is in this folder.

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| c2 · All four agents connect to the same servers without custom integration | partially supported | All four speak MCP (slide 15); the installer registers all three servers in every client. Formation sign-in is confirmed only for Claude: CyVerse does not yet accept the Codex/OpenCode callback, MESA has not tested Antigravity, and nothing says a fix is under way (f3-f6, f17, f22, f24). In the MESA apps OpenCode can sign in only on the KASM desktop (f23) | "All four agents speak MCP and register the same servers; Formation sign-in is confirmed for Claude, not yet for Codex, Antigravity or OpenCode." |
| c3 · Formation launches apps and jobs on CyVerse Kubernetes; Data Store MCP finds, reads and writes iRODS data | partially supported | Interactive apps run on Kubernetes (f9, f12). Batch jobs: Argo on Kubernetes in the pilot record (f10, f26, f27) vs HTCondor (f11, f13); `osg` jobs go to the Open Science Grid, off CyVerse Kubernetes (f25). Writes need a CyVerse sign-in (f14-f16) | "Formation launches CyVerse apps and analyses (interactive apps run on Kubernetes); the Data Store servers find and read data in iRODS, and write it once you sign in." |
| c4 · Label: Formation and Data Store are "MESA MCP servers" | partially supported | Formation is CyVerse's own hosted server; MESA only registers it (f1, f2) | "MCP servers MESA installs: CyVerse Formation + MESA Data Store" |
| c5 · Notes: both agents reach the same servers and the same data | partially supported | Same Data Store, but in the MESA apps each agent has a different irods instance (f18, f19) | "Show both agents call the same tools and get the same Data Store data." |
| c6 · Footer NSF Award #2632685 | supported | NSF API: MESA, University of New Mexico, OAC, started 07/15/2026; program field "Artificial Intelligence (AI)", funded through NAIRR (fundProgramName) (f21, f32) | — |
| c7 (new) · Notes: Data Store work happens "under the policies from the defense-in-depth slide" | partially supported | iRODS permissions apply, but slide 22's read-only agent account is not how Demo 1 is set up: Formation and the signed-in Data Store servers act as the user, with write and delete tools (f28-f30) | "The Data Store servers act as the signed-in researcher, with that person's iRODS permissions." |
| c8 (new) · Timing: slide "~1:30" vs notes "[~2 min]" | contradicted (internal) | talk/slides.md#slide-24 | Use one length in both places. |
| c9 (new) · Subtitle/body/notes: "the same (two) MESA servers" | partially supported | Formation is CyVerse's; MESA registers three servers, and Claude Code in the apps adds hosted CyVerse irods/irods-auth (f1, f2, f17, f31) | Subtitle "Any agent, the same MCP servers"; body "CyVerse's Formation server and the Data Store servers MESA installs". |

**Demo risk:** for "the same request from two agents", only Claude surfaces (claude.ai, Desktop, Claude Code) are documented to complete Formation's sign-in. Rehearse any Codex or Antigravity Formation call, use the KASM desktop if OpenCode is shown, or demo the second agent on Data Store requests. Remember that in the demo the agent acts as you, with delete rights (c7).

## Evidence

- `src/01_check.py` fetches the pages (cached in `data/cache/`, saved in `data/raw/sources/`, gitignored) and checks every quote → `data/processed/checks.csv`, `data/processed/nsf_award.csv`.
- `data/raw/research/facts.csv`: exact quotes with source URLs.
- MCP support in each client: [`../15-plain-language-definitions/data/processed/mcp_support.csv`](../15-plain-language-definitions/data/processed/mcp_support.csv).
