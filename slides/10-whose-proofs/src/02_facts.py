"""Build data/raw/research/facts.csv and check every quote appears verbatim in its saved source."""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "data" / "raw" / "sources"

W = "https://en.wikipedia.org/wiki/"
RW = ("OpenAI withdraws three preprints a day after releasing 722 manuscripts on unsolved math problems", "Retraction Watch", "2026-10-08", "https://retractionwatch.com/2026/10/08/openai-withdraws-preprints-722-manuscripts-unsolved-math-problems/", "news", "retractionwatch.txt")
README = ("openai/math README", "OpenAI (GitHub)", "2026-10-31", "https://github.com/openai/math/blob/main/README.md", "primary", "gh_readme.md")
HIST = ("openai/math history.md", "OpenAI (GitHub)", "2026-10-29", "https://github.com/openai/math/blob/main/history.md", "primary", "gh_history.md")
SA8 = ("The most exciting claims from OpenAI's heap of new proofs", "Scientific American", "2026-10-08", "https://www.scientificamerican.com/article/the-most-exciting-claims-from-openais-heap-of-new-proofs/", "news", "sciam_oct8.txt")
QU = ("Deluge of 377 OpenAI proofs bewilders the math world (Quanta updates)", "Quanta Magazine", "2026-10-06", "https://www.quantamagazine.org/updates/transformation/", "news", "quanta_updates.txt")
ZEN = ("A Severe Misalignment of AI in Mathematics (Zenodo record + PDF)", "Zenodo", "2026-09-11", "https://doi.org/10.5281/zenodo.22737750", "primary", "fl.txt")
MAI = ("A Severe Misalignment of AI in Mathematics (live signatory list)", "mathandai.org", "2026-10-31", "https://mathandai.org/", "primary", "mathandai.txt")
BS = ("Statement (Today, Levent Alpöge and I have made public three results)", "Tristan Buckmaster, NYU Courant", "2026-09-08", "https://cims.nyu.edu/~tristanb/statement.pdf", "primary", "bs.txt")
TC = ("OpenAI 'fought dirty' on career-making math problem, says NYU mathematician", "TechCrunch", "2026-09-08", "https://techcrunch.com/2026/09/08/openai-fought-dirty-on-career-making-math-problem-says-nyu-mathematician", "news", "techcrunch.txt")
VG = ("OpenAI just wants to win", "The Verge", "2026-09-12", "https://www.theverge.com/ai-artificial-intelligence/994255/openai-millennium-prize-problem-tristan-buckmaster-competition", "news", "verge_buckmaster.txt")
ABC = ("Racing to solve maths problems now 'pointless', says Australian at centre of OpenAI controversy", "ABC News (Australia)", "2026-09-11", "https://www.abc.net.au/news/2026-09-11/racing-to-solve-maths-problems-pointless-tristan-buckmaster-says/107141628", "news", "abc_sep11.txt")
SA13 = ("OpenAI's blockbuster math proof isn't what you think it is", "Scientific American", "2026-10-13", "https://www.scientificamerican.com/article/openais-blockbuster-navier-stokes-proof-isnt-what-we-thought-it-was/", "news", "sciam.txt")
FUT = ("Mathematicians furious at OpenAI (F. Landymore)", "Futurism", "2026-10-09", "https://futurism.com/artificial-intelligence/mathematicians-openai-furious", "news", "futurism.txt")
AHM = ("AHM Statement on OpenAI's October 6 Release of Mathematical Documents", "Association for Human Mathematics", "2026-10-07", "https://www.ahmath.org/statements", "primary", "ahm_statements.txt")
WNS = ("Navier–Stokes priority controversy", "Wikipedia", "2026-10-31", W + "Navier%E2%80%93Stokes_priority_controversy", "secondary", "wiki_ns_controversy.wikitext")
WBR = ("OpenAI bulk release of mathematical papers", "Wikipedia", "2026-10-31", W + "OpenAI_bulk_release_of_mathematical_papers", "secondary", "wiki_bulk_release.wikitext")

ROWS = [
    ("c1", "722 preprints; 372 problems; 2026-10-06", "On Oct. 6, OpenAI published 722 preprints in a GitHub repository about purported progress in solving 372 math problems", RW, ""),
    ("c1", "3 withdrawn on 2026-10-07", "But on Oct. 7, OpenAI announced the withdrawal of three manuscripts because of a sign error.", RW, ""),
    ("c1", "<24 h", "Less than 24 hours after OpenAI posted over 700 preprints describing major math results by an internal AI model, the company has withdrawn three of the manuscripts for errors.", RW, ""),
    ("c1", "3 withdrawn (OpenAI's own log)", "As a result, we have withdrawn the following three manuscripts:", HIST, "Entry dated October 7, 2026."),
    ("c1", "Oct 6 release date (OpenAI)", "We are releasing the model output directly, as we did in our October 6 release.", HIST, "October 26 entry."),
    ("c1", "now 721 manuscripts / 373 families", "The current catalogue contains 721 manuscripts organized into 373 families.", README, "722 - 3 withdrawn + 2 added Oct 26 = 721 (data/processed/checks.json). Slide figure 722/372 is the count at release."),
    ("c2", "~42% Lean (OpenAI log)", "This brings the total percentage of top-line results formalized to 300 / 719 = ~42%.", HIST, "October 7 entry; 300/719 = 41.7%."),
    ("c2", "~42% Lean (README)", "The repository has ~42% top-line results formalized.", README, ""),
    ("c2", "about half (OpenAI at release, via Quanta)", "According to OpenAI, about half of the results have been formally verified in the programming language Lean.", QU, "OpenAI's release-day figure; its own log later gives ~42%."),
    ("c2", "OpenAI had not read every paper", "No one, not even OpenAI researchers themselves, has been able to even read through everything yet.", SA8, "No first-hand OpenAI quote found; this is Scientific American's statement."),
    ("c2", "declaration title and benchmark warning", "However, the push by AI companies to solve mathematical problems as a benchmark is detrimental to the science of mathematics, and to the mathematical community.", ZEN, "Zenodo record publication_date 2026-09-11 lists 25 signatories."),
    ("c2", "28 signatories now", "Vladimir Drinfeld (Fields Medal 1990)", MAI, "Live page lists 28 Fields Medalists; Drinfeld, Margulis and Mumford were added after the 25-name Zenodo version (checks.json)."),
    ("c2", "24 then 28 (secondary)", "On 11 September 2026, 24 [[Fields Medal|Fields Medalists]] (later cosigned by four more) published an open letter", WNS, "Zenodo shows 25 at publication; press reported 25. Either way 28 now."),
    ("c3", "progress passed to OpenAI (tip)", "with Levent having received tips that infor- mation about our progress had been passed to OpenAI", BS, "Hyphenation as in the PDF text layer."),
    ("c3", "first OpenAI prompt after info reached OpenAI", "Eventually it was agreed that it had been sent in the past few days, after information about our work had reached OpenAI.", BS, ""),
    ("c3", "asked about Codex training", "I asked whether the model had been trained on, or had access to, our sessions in Codex, into which we had been putting all our drafts for the whole of this project.", BS, ""),
    ("c3", "not an accusation", "I do not know whether our data was used. I am not accusing anyone of anything.", BS, "Buckmaster frames his statement as an account, not an accusation."),
    ("c3", "Euler result obtained Aug 15", "on August 15th, we obtained the blow up results, with smooth forcing, for both Boussinesq and Euler.", BS, ""),
    ("c4", "first answer: cannot rule out", "While unlikely, we cannot rule out that de-identified data derived from their usage of our products helped improve our models", TC, "TechCrunch quoting OpenAI's 2026-09-08 post (openai.com returned HTTP 403 to our client)."),
    ("c4", "OpenAI says proofs differ", "However, our proofs differ significantly and even the precise results proved are different in the Euler case (forced vs unforced).", TC, "Same OpenAI post, as quoted by TechCrunch."),
    ("c4", "later: categorically impossible (2 months)", "We can say categorically that it is impossible for Dr Buckmaster's Codex prompts over the last two months to have influenced the system in any way, including training,", ABC, "Statement scoped to the last two months of prompts."),
    ("c4", "Buckmaster unconvinced", "Given their behavior up until this point, one should take such statements with great skepticism,", VG, ""),
    ("c4", "experts: methods differ", "But the resemblance between the two groups’ methods now seems merely skin-deep.", SA13, "Bears on the method question, not on the data question."),
    ("c5", "14 revised", "We have revised 14 other manuscripts with proof repairs, corrected statements, clearer hypotheses and dependencies, and one correction to an obsolete citation.", HIST, "October 7 entry."),
    ("c5", "unreleased internal model", "This repository contains mathematical manuscripts and supporting proof artifacts produced by an unnamed internal OpenAI model.", README, ""),
    ("c6", "AHM quote", "Mathematicians did not ask for this work to be done.", AHM, ""),
    ("c6", "Tao reshare (reported)", "A group called the Association for Human Mathematics released a statement blasting OpenAI’s release, which was then reshared, and effectively endorsed, by the Fields Medal-winning mathematician Terence Tau", FUT, "Futurism misspells Tao. No reshare in his public Mastodon timeline 2026-09-03 to 2026-10-08 (checks.json); platform not named."),
    ("c7", "Alpöge disputes 'different'", "but Alpöge refuted this argument, saying OpenAI's proof \"looks more along the lines of another Euler blowup proof we had\"", WNS, "Secondary; Alpöge's X post not fetched."),
    ("c8", "Futurism byline and date", "Frank Landymore", FUT, "Page datePublished 2026-10-09T10:14:55-04:00."),
]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


rows, bad = [], []
for i, (cid, val, q, src, note) in enumerate(ROWS, 1):
    title, pub, date, url, typ, fname = src
    text = (SRC / fname).read_text(encoding="utf-8", errors="ignore")
    if norm(q) not in norm(text):
        bad.append((i, fname, q[:80]))
    rows.append(dict(id=f"F{i:02d}", claim_id=cid, value=val, quote=q, source_title=title, publisher=pub, date=date, url=url, source_type=typ, notes=note))
out = HERE / "data" / "raw" / "research" / "facts.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows;", "missing quotes:", bad)
