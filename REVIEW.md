# Deck-wide review

Cross-slide findings from the completeness critic of the fact-check workflow run on 2026-10-31. Slide-level verdicts are in each `slides/NN-*/claims.yaml`; this file records what no single slide owns.

Note: the `revise-slide` statuses (slides 05, 12, 13, 14, 17) record wording the speaker agreed to; they were set by hand, not by the review agents.

## Inconsistencies between slides

- Agent write rights, slide 22 vs slides 24, 27 and 30: slide 22 says the AI agent has 'Its own account, read-only' and 'Agent writes: denied'. Slide 27 shows an agent (Claude Desktop via MESA MCP) writing AVUs onto the iRODS collection, and slide 30 says 'written back as iRODS attributes'. Only 24 c7 flags this (the Data Store MCP acts as the signed-in researcher). 27 c2 and 30 c2 do not mention the conflict.
- Beetle site linkage, slide 26 vs slide 27: slide 26 notes say 'only 20,698 of the segmented beetles link to a NEON site'. Slide 27's AVU row says 'specimens 65,830 segmented, 47 sites', and its notes say '65,830 beetles ... linked to trap records at 47 sites'. 47 is the site count for the whole NEON product (27 c3), not the sites linked to segmented beetles.
- Timing markers do not add up. Slide 06 is 'by 7:30', then slides 07 to 10 add about 6.5 min, yet slide 11 is 'by 10:30'. Slide 15 is 'by 18:00', then slide 16 (~1.5 min) and slide 17 is 'by 10:00', then slide 18 is 'by 18:30'. Slide 21 is 'by 22:00', but 18:30 plus 2 + 1.5 + 2 min is 24:00. Summing the per-slide durations (slide 04 has none) gives about 51.5 min against the 44:00 end target, which leaves about 2.5 min of the planned 10-min Q&A.
- Demo lengths: slide 24 says 'Target length ~1:30' but its notes say '[~2 min]' (flagged as 24 c8). Slide 29 says 'Target length ~2:00' but its notes say '[~2.5 min]'; this one is not flagged.
- Slide 17 notes call it 'The hinge of the worry section', but the slide sits in section 02 (Science), after the slide 11 divider.
- ESM naming differs three ways: slide 13 says 'EvolutionaryScaleModel (ESM)', its notes say 'Evolutionary Scale Models (ESM)', and 13 c2 says the project is 'Evolutionary Scale Modeling' and the model is ESMFold2.
- Agent lists: slide 15 notes name five (Claude Code, Codex, Antigravity, OpenCode, Goose). Slide 24 names four ('Claude', no Goose). Slide 27 uses 'Claude Desktop', which MESA's docs say does not get mesa-mcp (27 c2).
- PhD credential, 01 c3 vs 34 c6: 01 c3 is supported for 'PhD' from the faculty profile ('Ph.D., ... University of Arizona, 2013'). 34 c6 says 'no source for "PhD" was fetched, so that part is unverified'. 34 c6 should reuse the 01 evidence or cross-reference it.
- Bartz per-work figure: slide 09 and 09 c1 say '$3,100' (gross). 06 c11 says '~$3,000 per work' (court wording). Both are defensible, but the claim files differ.
- Ontology and provenance verdicts conflict across slides. 17 c2 ('Terms must resolve in an ontology') and 17 c4 ('Provenance in DuckLake; replay any run') are supported, and the slide 17 notes say these controls 'come back in section three' as MESA features. The MESA versions are not verified: 25 c4 ('one that will not resolve fails the write') and 27 c4 are unverified, and 30 c3 is only partially supported ('every write' holds only if a DuckLake catalog DSN is set).
- MESA funding program: slide 20 notes say MESA is 'funded through NSF's Integrated Data Systems and Services (IDSS) program, one of three NSF programs that feed NAIRR'. NSF records the fund line as NAIRR (19 c2, 20 c10), NSF says 'coordinate with' rather than 'feed' (20 c13), slide 34 still shows '[NAIRR]' as a placeholder, and slide 18 notes say 'under NAIRR'. These should be stated one way across slides 18, 20 and 34.
- Early adopters: slides 20 and 34 list six communities (NEON, ESIIL, NCEMS, NSCORE, AIIRA, EHT), but the award names only four (20 c9, 34 c5; NEON and NSCORE are absent). The verdicts agree with each other, but the slides state all six as fact.
- Slide 05 footer says 'Cumulative cost in 2025 dollars', but 05 c4 and c5 say Moorhouse's chart and the folder's own reconciliation are in 2024 dollars ('$844B (2024 $)'). The footer also credits Gartner, which Moorhouse does not cite.
- NEON DP1.10022.001 date range: slide 26 says '2013–2026', its notes say 'July 2013 to September 2026', and the NEON API (26 c13, 27 c3) shows data through 2026-10.
- Slide 32 says 'Spring 2026: CS 491/591' for a talk on Nov. 4, 2026. That term is past; 32 c5 proposes Spring 2027.
- Data Store size: 23 c1 finds 6 PB (CyVerse docs) and 5.2 PB (CARC and MESA hiring pages). The slide hedges with 'Petabytes', so it is fine.
- Deck tooling: in talk/slides.md the headings for slides 04, 07, 08, 09, 10 and 16 have no '[evidence](../slides/NN-*/)' link, though those folders exist.

## Assertions with no claim

- Slide 18: claims.yaml is empty, but the slide says 'For the US national science community, on national research infrastructure.' and the notes say 'what CARC and partners are building under NAIRR'. The NAIRR fund line is checked on slide 20 (c10), but nothing is claimed here.
- Slide 16: the table footer 'an ontology and a schema fix the answer space before anything is written' and the notes' link to MESA ('ontology terms that must resolve, a JSON schema validated in the agent') have no claim. The same MESA behaviour is unverified on slide 25 (c4) and slide 27 (c4).
- Slide 16: the LLM column rows 'Writes text one token at a time' and 'Invents plausible text: citations, names' have no claim. c5 covers only the Confidence row.
- Slide 08: 'Cheaper AI does the same' and the notes' 'each token gets cheaper, total demand soars' have no claim. c5 checks Jevons (1865) and calls the AI link the speaker's analogy, but no source was fetched for the fall in per-token price or for demand rising because of it.
- Slide 13: the model name 'EvolutionaryScaleModel (ESM)' on the slide and 'Biohub's Evolutionary Scale Models (ESM) protein world model' in the notes have no claim. It is only mentioned in the c2 notes (the correct expansion is 'Evolutionary Scale Modeling', and the model Biohub used is ESMFold2).
- Slide 17: the middle column ('No retrieval step at all', 'Open vocabulary, nothing to check', 'Sampling with no output contract', 'No record of inputs or steps') and the notes' central claim 'every one of them is a missing engineering control, not a property of the model' have no claim. Sampling variance is arguably a property of the model. The old c5 and c6 are superseded.
- Slide 06: the current taglines ('how models are trained, how they are misused', 'Researchers' work stolen? openai/math') are covered only by c17 (not-applicable). Misuse is not claimed on any current slide. c12 and c13 (AI-run espionage, ICML 795 reviews) verify text that is no longer on the slide.
- Slide 06: c5 to c16 are marked supported but check text that was removed from the slide (c1 to c4 are superseded). They are orphaned: they should be superseded or tied to current text.
- Slide 26 notes: 'No archive was asked to change.' has no claim.
- Slide 09 source line: 'court records and case status as of August 2026' has no claim and is stale. c3 cites September 2026 developments (NYT summary-judgment motions filed Sept. 4, 2026).
- Slide 34 notes: the early-adopter award list leaves out EHT (NSF 2535855), which is on the slide. The '[NAIRR]' placeholder on the slide is still unresolved (c1 only proposes wording).
- Slide 04 notes: the interpretive themes (fascism and authoritarianism, war as a 'mathematical equation') have no claim. They are acceptable as interpretation, but they are unattributed readings of the film.

## Still unverified, and why

- 23 c7 (Co-scientists that write hypotheses and tests and report continuously): no public MESA, CARC or CyVerse page describes a running loop. It is only a goal (MESA Goal 3; 'agentic orchestration' in the NSF abstract).
- 25 c4 (a term that will not resolve fails the write): the behaviour lives in MESA code, which was out of scope. Public docs describe OLS candidate search plus curator approval, not refusal at write time.
- 25 c11 (neon-beetle-seg actually uses these four CURIEs, per docs/schema.md): the source is a GitHub repo other than the talk repo, which was out of scope.
- 25 c13 (a Coleoptera query returns the NEON carabid data untagged): the ontology half holds (c9). Query expansion to subclasses needs MESA code or a live run.
- 26 c10 (65,830 beetles; r = 0.98) and 26 c11 (outputs on the CyVerse Data Store: DuckLake, Parquet, public report): the report and folder URLs redirected (HTTP 307) to unblockme.cyverse.org, which was not bypassed. These are developer-reported.
- 26 c14 (145,906 pinned individuals of 826 taxa): not computed because it needs the full NEON per-site, per-month download. This one is computable from the NEON data API (data.neonscience.org/api/v0) and could still be done.
- 26 c15 (most specimens never photographed; 20,698 linked to a site; elytra about 8% long): project figures; the report was unreachable and the repo out of scope.
- 27 c4 (the MCP server refuses unresolved terms): same reason as 25 c4.
- 27 c6 (the neon-beetle-seg figures repeated in the slide 27 notes): report bot-gated, repo out of scope.
- 27 c7 (the collection lives at /iplant/home/tswetnam/neon-beetle-seg/): WebDAV redirected to unblockme, and CyVerse's public Data Store MCP answered 'Path is not publicly accessible'.
- 29 c1 (Demo 3): the slide is still a placeholder ('Recorded clip goes here'). There is no transcript, snapshot or figure, and no evidence the run used NAIRR compute.
- 30 c1 and c8 (the NCEMS pilot ran this summer; 'Already running on real collections'): there is no public pilot page, collection path or config, so this is speaker-reported. The title's ongoing, multi-collection framing conflicts with the notes' single summer run.
- 32 c5 (Spring 2026 CS 491/591 'AI Automation and Agents'): no public schedule page names that section in any term.
- Unverified parts inside partial verdicts: 01 c2 ('12 years'); 26 c9 (the single 16 GB GPU and the DuckLake recording, which need the repo or logs); 30 c3 (the OKF session-bundle half); 34 c2 (github.com/idss-mesa itself not fetched); 08 c8 (the ALA ozone 'F' grade loads by script, so it is attributed to SELC only); 08 c9 (the Shelby County permit for 15 turbines not fetched); 10 c7 (Alpöge's rebuttal sourced via Wikipedia only); 04 c1 (AFI and LoC records not reached).

## Verdicts to strengthen or soften

- 05 c1 is contradicted ('largest single investment in human history'), but the verdict depends on the metric. It rests on share of GDP from the folder's own ranking.csv, while 05 c5 finds that in constant dollars data centers ($844B, 2024 dollars) already exceed the Interstates ($700B) and railroads ($291B). The evidence is also US-only while the claim says 'human history'. 'Contradicted as share of GDP; unproven globally' would be more accurate than a flat contradicted.
- 15 c2 (definition of an agent loop) and 15 c3 (what the harness owns) are supported only by files in another slide's folder ('../14-agentic-ai/data/processed/mcp_transcript.json', 'mcp_calls.csv'). Those files come from a scripted run with no model (14 c2: 'a scripted plan stands in; no model API'), so the evidence is self-generated, and neither claim has notes or an external source.
- 14 c1 is set to revise-slide with evidence 'README.md' only, and no notes or sources. That is circular evidence for a verdict status.
- 17 c2 (supported) rests only on 'data/processed/ontology_writes.csv' from this repo's own validator demo, not MESA. 17 c4 (supported, 'replay any run') rests on a local DuckLake demo, and its own notes concede replay 'cannot re-draw the model's samples'. Both read as MESA controls ('come back in section three'), so partially-supported fits better, given 25 c4, 27 c4 and 30 c3.
- 21 c8 ('MESA's data lakehouse is built on DuckLake') is supported, but its notes say it is 'Project-reported ... MESA code was not checked'. It should be partially-supported or explicitly labelled developer-reported.
- 10 c5 is supported for 'from an unreleased internal model', but its notes say the sources say 'unnamed' and 'internal', not 'unreleased', and it offers proposed_text. The verdict should be partially-supported.
- 04 c5 (poster by Tomi Ungerer) is supported, but data/raw/research/facts.csv has no row tagged c5: the Ungerer fact F15 is tagged c2. The support is secondary only (eriac.org, Wikipedia). 04 c6 is also supported only by secondary framing.
- 08 c9 is supported, but only as the account of SELC, which is the NAACP's counsel; the permit was not fetched. The text should say it is an attribution to SELC, or the status should be partially-supported. 09 c8 (GEMA v. OpenAI) likewise rests on one legal-news report, with no court release fetched.
- 06 c5 to c16 are supported, but their facts.csv files (data/raw/environment, training_misuse and closed_systems) use a legacy schema (id, topic, value, unit, refers_to, ...) with no claim_id column, so no quote row can be tied to these claim ids. The same is true for slide 13's data/raw/research/facts.csv (c1, c2, c3, c6). These claims also verify text no longer on slide 06.
- Status revise-slide appears on 05 c4, 12 c1, 13 c2, c3, c4 and c6, 14 c1 and 17 c3. The convention says only the speaker sets revise-slide; if an agent set these, the underlying verdict is lost. In particular, 13 c2's notes find 'tested at the bench in days' not supported, which is a contradicted component that is now hidden under revise-slide.
- 24 c8 is contradicted, with evidence '../../talk/slides.md' outside the slide folder. It is acceptable as an internal-consistency check, but it is not a factual verdict.
- 34 c6 is partially-supported because the PhD is 'unverified', although 01 c3 already holds supporting evidence for it. This is under-claimed rather than over-claimed and should be supported, citing the 01 evidence.
