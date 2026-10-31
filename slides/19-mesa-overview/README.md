# Slide 19 · Thawing the frozen data lake of public research

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-19)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` MESA connects data through curated metadata, runs on national infrastructure today, open source | partially supported | MESA site (developer-reported) says exactly this. Live today: the portal mesa.cyverse.org on CyVerse. The MCP servers (mesa-mcp, mesa-ducklake, irods-mcp-server) install and run on the user's machine and connect to CyVerse-hosted Formation and Data Store. The NSF abstract says MESA *will* run on TACC, OSN, Jetstream-2 and CyVerse via ACCESS-CI. Funding began 1 Jun 2026 at Arizona (award 2608717) and continues at UNM as 2632685 from 15 Jul 2026. Code is public; licence types not confirmed. | "MESA connects scientific data through curated, indexed metadata. Its portal runs on CyVerse today, and its MCP tools install in one line and connect to CyVerse-hosted services; TACC, Jetstream2 and OSN are planned. Code is public at github.com/idss-mesa." |
| `c2` NSF Award #2632685 | supported | NSF Award API: "Research Infrastructure: Category II: MESA", UNM, PI Swetnam, OAC, 2026-07-15 to 2029-05-31, $4.62M. Program element "Artificial Intelligence (AI)" (296Y00); fund program NAIRR. Figure's proposal origin cannot be checked publicly. | none |
| `c3` MESA = Multidisciplinary Environment for Scientific Advancement | supported | Award title and abstract. | none |
| `c4` Disciplines placeholder in notes | partially supported | Placeholder; figure not checked. Abstract: MESA "will enable" astronomy, biology, environment, public health, computer science; partners ESIIL, NCEMS, AIIRA, EHT. | "Disciplines named in the award: astronomy, biology, environment, public health and computer science. Partners: ESIIL (environmental data science), NCEMS (molecular and cellular science), AIIRA (AI in agriculture) and the Event Horizon Telescope." |

Open points:
- Funding label: the MESA site footer says the award is under Integrated Data Systems & Services (IDSS). The NSF record names no IDSS program or program element. Its program is "Artificial Intelligence (AI)" (296Y00) and its fund program is NAIRR. The abstract only describes MESA as "an integrated data system and service". So the slide-20 line "funded through NSF's IDSS program" rests on the developer's site alone.
- Award history: 2608717 (University of Arizona, 2026-06-01 to 2026-08-31, same title, PI and $4,617,408, $0 obligated) appears to be the same project before it moved to UNM. NSF does not state a transfer.
- Licence types need a check of the repositories themselves.
- The disciplines in `c4` should be checked against the figure by the speaker.

## Evidence

- `src/02_predecessor_award.py` fetches award 2608717 (MESA at Arizona) and a CyVerse keyword search listing both MESA awards; outputs `data/processed/award_2608717.json` and `mesa_awards_search.json`.
- `src/01_nsf_award.py` fetches awards 2632685 (MESA) and 1743442 (CyVerse) from the NSF Award API; outputs in `data/processed/` (contact fields removed).
- `data/raw/research/facts.csv`: exact quotes, each checked against the saved source.
- Fetched pages are in `data/raw/sources/` (gitignored) with a `MANIFEST.yaml`.
