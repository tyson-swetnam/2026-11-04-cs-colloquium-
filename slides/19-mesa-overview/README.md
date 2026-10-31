# Slide 19 · Thawing the frozen data lake of public research

Section: 03 · Build your AI · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-19)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` MESA connects data through curated metadata, runs on national infrastructure today, open source | partially supported | MESA site (developer-reported) says exactly this; portal mesa.cyverse.org is live on CyVerse. NSF abstract says MESA *will* run on TACC, OSN, Jetstream-2 and CyVerse (award began 15 Jul 2026). Code is public at github.com/idss-mesa, but licence types are not stated in public docs. | "MESA connects scientific data through curated, indexed metadata. Its portal and agent tools run on CyVerse today, with TACC, Jetstream2 and OSN to follow. Code is open at github.com/idss-mesa." |
| `c2` NSF Award #2632685 | supported | NSF Award API: "Research Infrastructure: Category II: MESA", UNM, PI Swetnam, OAC, 2026-07-15 to 2029-05-31, $4.62M, fund program NAIRR. Figure's proposal origin cannot be checked publicly. | none |
| `c3` MESA = Multidisciplinary Environment for Scientific Advancement | supported | Award title and abstract. | none |
| `c4` Disciplines placeholder in notes | supported (from award) | Abstract: astronomy, biology, environment, public health, computer science; partners ESIIL, NCEMS, AIIRA, EHT. | "Disciplines: astronomy (EHT), biology and multi-omics (NCEMS), environment (ESIIL), agriculture (AIIRA), public health and computer science." |

Open points: the MESA site footer says the award is under Integrated Data Systems & Services, while the NSF record's fund program is NAIRR (see slide 20). Licence types need a check of the repositories themselves.

## Evidence

- `src/01_nsf_award.py` fetches awards 2632685 (MESA) and 1743442 (CyVerse) from the NSF Award API; outputs in `data/processed/` (contact fields removed).
- `data/raw/research/facts.csv`: exact quotes, each checked against the saved source.
- Fetched pages are in `data/raw/sources/` (gitignored) with a `MANIFEST.yaml`.
