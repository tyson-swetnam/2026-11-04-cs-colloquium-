# Slide 01 · How I Learned to Stop Worrying and Love the AI

Section: Opening · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-01)

## Findings

| Claim | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| `c1` Wed. Nov. 4, 2026, 2 p.m., Larrañaga Engineering Auditorium (Centennial 1041) | supported | UNM CS colloquium page lists exactly this; Python confirms Nov. 4, 2026 is a Wednesday | none |
| `c2` Host bio: Assoc. Prof. of CS, CARC Director, 12 years, PI/co-PI on OAC and DBI projects | partially supported | Faculty profile and CARC pages confirm the titles. Profile says CyVerse work began 2013 (13 years). NSF API: 8 awards (4 PI, 4 co-PI); only one active OAC award (MESA, 2632685, at UNM); the only DBI-labelled award (CyVerse) ended July 2025 | "more than a decade"; "has been PI or co-PI on NSF awards from OAC and the Directorate for Biological Sciences; now leads MESA, an NSF NAIRR award at UNM" |
| `c3` Tyson L. Swetnam, PhD, CARC, UNM | supported | Faculty profile (PhD, Univ. of Arizona, 2013); CARC welcome post | none |
| `c4` CS Colloquium; title "...Love the AI" | supported | Colloquium listing title matches; "Super Intelligence" reveal is a slide gag | none |

## Evidence

- `data/raw/research/facts.csv`: exact quotes from the colloquium page, faculty profile, CARC pages and NSF Award Search API.
- `src/01_nsf_awards.py`: queries the NSF Award Search API for PI and co-PI awards and checks the talk date's weekday. Outputs go to `data/processed/nsf_awards.csv` and `data/processed/summary.txt`.
- Fetched pages are in `data/raw/sources/` (gitignored, logged in MANIFEST.yaml).

Caveats: CARC pages are on `carc-temp.unm.edu`. The NSF API does not show subawards or senior-personnel roles.
