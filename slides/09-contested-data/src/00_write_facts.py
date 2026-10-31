"""Write data/raw/research/facts.csv (quotes copied from documents fetched 2026-10-31 by 01_fetch.py).

Each row's `file` (in FILES below) names the saved document; 02_check.py confirms every quote appears in it.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "data/raw/research/facts.csv"
COLS = ["id", "claim_id", "value", "quote", "source_title", "publisher", "date", "url", "source_type", "notes"]

BZ231 = ("Bartz v. Anthropic PBC, No. C 24-05417 WHA, Order on Fair Use (Dkt. 231)", "U.S. District Court, N.D. Cal. (Judge William Alsup)", "2025-06-23",
         "https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf")
BZFA = ("Bartz v. Anthropic PBC, No. 3:24-cv-05417-AMO, Order Granting Final Approval of Class Action Settlement (Dkt. 680)",
        "U.S. District Court, N.D. Cal. (Judge Araceli Martínez-Olguín); copy hosted by the Association of American Publishers", "2026-07-20",
        "https://publishers.org/wp-content/uploads/2026/07/Order-Granting-Final-Approval-of-Settlement171.pdf")
SITE = ("Anthropic Copyright Settlement (official settlement website)", "JND Legal Administration, court-appointed administrator", "accessed 2026-10-31",
        "https://www.anthropiccopyrightsettlement.com/")
PC = ("Federal Court Approves $1.5 Billion Anthropic Copyright Settlement — Largest in History", "Pearl Cohen (Haim Ravia, Dotan Hammer)", "2026-07-30",
      "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history")
KAD = ("Kadrey v. Meta Platforms, No. 23-cv-03417-VC, Order on cross-motions for partial summary judgment (Dkt. 598)", "U.S. District Court, N.D. Cal. (Judge Vince Chhabria)", "2025-06-25",
       "https://storage.courtlistener.com/recap/gov.uscourts.cand.415175/gov.uscourts.cand.415175.598.0.pdf")
NYT = ("In re OpenAI, Inc. Copyright Infringement Litigation, 25-md-3143 (SHS) (OTW), Order (Stein, J.)", "U.S. District Court, S.D.N.Y.; copy hosted by Law360", "2026-01-05",
       "https://assets.law360news.com/2426000/2426657/https-ecf-nysd-uscourts-gov-doc1-127138822336.pdf")
CIETW = ("Summary judgment briefing starts in OpenAI MDL Litigation before Judge Stein", "Chat GPT Is Eating the World (Edward Lee)", "2026-09-04",
         "https://chatgptiseatingtheworld.com/2026/09/04/summary-judgment-briefing-starts-in-openai-mdl-litigation-before-judge-stein/")
GP = ("Disney, Warner Bros., Universal and Midjourney Discovery Dispute Kicked to Late May", "Graphic Policy (Brett)", "2026-05-11",
      "https://graphicpolicy.com/2026/05/11/disney-warner-bros-universal-and-midjourney-discovery-dispute/")
COMP = ("Concord Music Group, Inc. et al. v. Anthropic PBC et al., Case 3:26-cv-00880, Complaint (Dkt. 1)", "U.S. District Court, N.D. Cal.; copy hosted by Music Business Worldwide", "2026-01-28",
        "https://www.musicbusinessworldwide.com/files/2026/01/Anthropic-complaint-01.28.26-1.pdf")
MBW = ("UMG sues Anthropic for $3bn over ‘brazen’ copyright infringement of 20,000+ songs", "Music Business Worldwide (Murray Stassen)", "2026-01-28",
       "https://www.musicbusinessworldwide.com/umg-concord-and-abkco-sue-anthropic-for-3bn-in-what-could-be-single-largest-non-class-action-copyright-case-in-us-history/")
MBW2 = ("Anthropic seeks partial dismissal in music publishers’ $3B lyrics suit", "Music Business Worldwide (Mandy Dalugdug)", "2026-08-06",
        "https://www.musicbusinessworldwide.com/anthropic-seeks-partial-dismissal-in-music-publishers-3b-lyrics-suit-as-CEO-moves-to-drop-the-direct-infringement-claim-against-him/")
W3 = ("Usage statistics of content languages for websites", "W3Techs (Q-Success)", "accessed 2026-10-31", "https://w3techs.com/technologies/overview/content_language")
W3H = ("Historical yearly trends in the usage statistics of content languages for websites, October 2026", "W3Techs (Q-Success)", "2026-10-31",
       "https://w3techs.com/technologies/history_overview/content_language/ms/y")
DODGE = ("Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus (Dodge et al., EMNLP 2021)", "arXiv 2104.08758", "2021",
         "https://arxiv.org/pdf/2104.08758")
LL2 = ("Llama 2: Open Foundation and Fine-Tuned Chat Models (Touvron et al.)", "Meta AI, arXiv 2307.09288", "2023-07", "https://arxiv.org/pdf/2307.09288")
SPK = ("Legal, ethical, and social concerns (Intro to GPT course site)", "Tyson Swetnam (speaker's own page)", "accessed 2026-10-31", "https://tyson-swetnam.github.io/intro-gpt/legal/")
LTO = ("LG München I: GEMA siegt gegen OpenAI im Streit um Liedtexte", "Legal Tribune Online", "2025-11-11",
       "https://www.lto.de/recht/nachrichten/n/42o1413924-lg-muenchen-i-gema-openai-chatgpt-songtexte-ki")
GP25 = ("Court Suggests Disney v. Midjourney Go to Mediation", "Graphic Policy (Brett)", "2025-11-14",
        "https://graphicpolicy.com/2025/11/14/court-suggests-disney-v-midjourney-go-to-mediation/")
LFN = ("Bartz v. Anthropic, court-authorized Long Form Notice (updated deadline 2026-01-08)", "JND Legal Administration, court-appointed administrator", "2026-01-08",
       "https://assets-us-01.kc-usercontent.com:443/1eeb16db-4934-006e-40a6-38fa91285ebb/ce109a57-390c-4d76-ad65-5807d4830fe5/ANT%20-%20Long-Form%20Notice_Updated%20Deadline%201.8.2026.pdf")
SW = ("Sony Music Publishing (US) LLC et al. v. Anthropic PBC et al., Case 5:26-cv-09217, Complaint (Dkt. 1)", "U.S. District Court, N.D. Cal. (San Jose); copy hosted by Music Business Worldwide", "2026-08-28",
      "https://www.musicbusinessworldwide.com/files/2026/08/COMPLAINT-in-Sony_Music_Publishing_US_LLC_e.pdf")
MBW3 = ("Sony Music Publishing and Warner Chappell sue Anthropic in multi-billion dollar lawsuit", "Music Business Worldwide (Tim Ingham)", "2026-08-29",
        "https://www.musicbusinessworldwide.com/now-sony-music-publishing-and-warner-chappell-sue-anthropic-in-multi-billion-dollar-lawsuit-one-of")
FORT = ("Sony and Warner Music sue Anthropic over alleged theft of 'tens of thousands' of songs", "Fortune", "2026-09-01",
        "https://fortune.com/2026/09/01/anthropic-warner-sony-music-songs-lawsuit/")
BSAL = ("Getty Images v Stability AI – Getty granted permission to appeal", "Burges Salmon (Harry Jewson, Emily Roberts)", "2025-12-19",
        "https://www.burges-salmon.com/articles/102lydc/getty-images-v-stability-ai-getty-granted-permission-to-appeal")
IPKAT = ("Permission to appeal granted in Getty", "The IPKat", "2026-01",
         "https://ipkitten.blogspot.com/2026/01/permission-to-appeal-granted-in-getty.html")
GETTY = ("Getty Images (US) Inc & Ors v Stability AI Ltd [2025] EWHC 2863 (Ch)", "High Court of England and Wales (Joanna Smith J), The National Archives Find Case Law", "2025-11-04",
         "https://caselaw.nationalarchives.gov.uk/ewhc/ch/2025/2863")

ROWS = [
    # (id, claim, value, quote, source tuple, type, notes, file)
    ("F01", "c1", "1.5 USD billion", "The non-reversionary Settlement Fund of $1.5 billion", BZFA, "primary", "Final approval order.", "bartz_final_approval_order.pdf"),
    ("F02", "c1", "482,460 works", "for a total of 440,490 works of the 482,460 Works on the Works List", BZFA, "primary", "91.3% claimed as of 2026-04-16.", "bartz_final_approval_order.pdf"),
    ("F03", "c1", "~$3,000 per work (court's estimate, before costs and fees)", "The estimated per-work payment of approximately $3,000 is four times the minimum statutory damages amount", BZFA, "primary",
     "$1.5B / 482,460 = $3,109 gross (src/02_check.py). Net of fees, expenses and cost reserve: $2,855 per listed work, or about $3,127 per claimed work (440,490) if unclaimed money is redistributed, before administration costs and plus interest.", "bartz_final_approval_order.pdf"),
    ("F04b", "c1", "unclaimed funds redistributed", "If any funds remain in the Settlement Fund after all Valid Claims are paid, the Parties anticipate a redistribution of the remaining funds to Settlement Class Members unless it is economically infeasible to do so.", BZFA, "primary",
     "So per-claimed-work payments can exceed net fund / all listed works.", "bartz_final_approval_order.pdf"),
    ("F04", "c1", "fees $101,561,111", "amount of $101,561,111, nearly 6.8% percent of the non-reversionary Settlement Fund", BZFA, "primary", "Court cut the 12.5% ($187.5M) request.", "bartz_final_approval_order.pdf"),
    ("F05", "c1;c5", "2026-07-20", "On July 20, 2026, the Court granted final approval.", SITE, "primary", "Order itself: 'Document 680 Filed 07/20/26'.", "bartz_settlement_site.html"),
    ("F06", "c5", "largest copyright class action settlement in history (court)", "the Settlement is “the largest copyright class action settlement in history.”", BZFA, "primary",
     "Final approval order quoting the court's own preliminary-approval opinion (Bartz, 2025 WL 2961371, at *3). Wording is 'copyright class action settlement', narrower than 'US copyright settlement'.", "bartz_final_approval_order.pdf"),
    ("F27", "c1;c5", "largest copyright class action settlement; ~$3,000 per work plus interest less fees", "The resulting Settlement is the largest copyright class action settlement in history. It provides approximately $3,000 per work (not per Class Member), plus interest earned on the Settlement fund, less the Court-approved costs and fees taken out of the Settlement fund.", LFN, "primary",
     "Same sentence appears on the official settlement website (bartz_settlement_site.html).", "bartz_long_form_notice.pdf"),
    ("F06b", "c5", "largest in history (law-firm headline)", "Federal Court Approves $1.5 Billion Anthropic Copyright Settlement — Largest in History", PC, "secondary",
     "Secondary echo of the court's wording.", "pearlcohen_final_approval.html"),
    ("F07", "c2", "training = fair use (Bartz)", "the use of the books at issue to train Claude and its precursors was exceedingly transformative and was a fair use under Section 107 of the Copyright Act", BZ231, "primary", "", "bartz_dkt231_fair_use_order.pdf"),
    ("F08", "c2", "pirated library copies not fair use (Bartz)", "However, Anthropic had no entitlement to use pirated copies for its central library.", BZ231, "primary", "", "bartz_dkt231_fair_use_order.pdf"),
    ("F08b", "c2", "pirated library copies sent to trial (Bartz)", "We will have a trial on the pirated copies used to create Anthropic’s central library", BZ231, "primary",
     "Alsup denied Anthropic summary judgment on the pirated library copies; no final holding on them (the case then settled).", "bartz_dkt231_fair_use_order.pdf"),
    ("F10b", "c2", "Kadrey: plaintiffs made the wrong arguments", "It stands only for the proposition that these plaintiffs made the wrong arguments", KAD, "primary", "", "kadrey_dkt598_sj_order.pdf"),
    ("F09", "c2", "downloading from shadow libraries treated as part of fair use (Kadrey)", "Because Meta’s ultimate use of the plaintiffs’ books was transformative, so too was Meta’s downloading of those books.", KAD, "primary",
     "So Kadrey did NOT hold acquisition of pirated copies unlawful; the 'but not pirated copies' holding is Bartz only.", "kadrey_dkt598_sj_order.pdf"),
    ("F10", "c2", "ruling limited to this record", "this ruling does not stand for the proposition that Meta’s use of copyrighted materials to train its language models is lawful", KAD, "primary", "", "kadrey_dkt598_sj_order.pdf"),
    ("F11", "c2", "distribution (torrent seeding) claim left open", "so this will remain a live issue in the case", KAD, "primary", "Refers to the plaintiffs' distribution claim (leeching/seeding).", "kadrey_dkt598_sj_order.pdf"),
    ("F12", "c3;c6", "20M de-identified logs ordered, affirmed 2026-01-05", "her reasons for ordering production of the entirety of the 20 million de-identified log sample", NYT, "primary",
     "Order: 'OpenAI's objections are denied and Judge Wang's orders are affirmed.' Wang's orders dated Nov. 7 and Dec. 5, 2025.", "nysd_20m_logs_order.pdf"),
    ("F13", "c3", "NYT MDL at summary judgment (Sept. 2026)", "will file their respective motions for summary judgment", CIETW, "secondary", "No merits ruling found as of 2026-10-31.", "cietw_sj_briefing_2026-09-04.html"),
    ("F14", "c3", "Midjourney: mediation ordered, to finish by Aug. 19, 2026 (schedule set Nov. 2025)", "It asks for the mediation proceeding to be completed by August 19, 2026", GP25, "news",
     "Schedule set in Nov. 2025, not a 2026 status. Outcome of mediation not found. CourtListener docket pages returned 403, so the docket was not read.", "graphicpolicy_midjourney_2025-11-14.html"),
    ("F14b", "c3", "Midjourney: discovery dispute, May 2026 (latest case report found)", "Disney, Warner Bros., Universal and Midjourney Discovery Dispute Kicked to Late May", GP, "news",
     "Latest case report found; no settlement or merits ruling found as of 2026-10-31.", "graphicpolicy_midjourney_2026-05.html"),
    ("F15", "c3;c7", "torrented books with 'hundreds or thousands' of works, including 714 (Exhibit A)", "Defendants torrented countless pirated copies of these books containing hundreds or thousands of Publishers’ works, including the 714 works identified in Exhibit A", COMP, "primary", "Allegation. 714 is the identified minimum, listed separately from Exhibit B.", "publishers_v_anthropic_complaint_2026-01-28.pdf"),
    ("F16", "c3;c7", "20,517 training/output works (Exhibit B)", "20,517 works identified in Exhibit B", COMP, "primary", "Allegation; pleaded as training and output infringement, a separate exhibit from the 714 torrenting works (src/02_check.py adds them: 21,231).", "publishers_v_anthropic_complaint_2026-01-28.pdf"),
    ("F17", "c3", "> $3B potential statutory damages (publishers' statement)", "In total, we are suing for infringement of more than 20,000 songs, with potential statutory damages of more than $3 billion.", MBW, "news",
     "Publishers' statement quoted by MBW; 21,231 works x $150,000 statutory max = $3.18B (src/02_check.py).", "mbw_publishers_v_anthropic.html"),
    ("F18", "c3", "Anthropic moved for partial dismissal Aug. 3, 2026 (case pending)", "The two filings landed on Monday (August 3) in the US District Court for the Northern District of California", MBW2, "news", "", "mbw_anthropic_partial_dismissal.html"),
    ("F28", "c3;c7", "Sony/Warner Chappell v. Anthropic filed Aug. 28, 2026 (separate suit)", "It was filed on Friday (August 28) in the US District Court for the Northern District of California", MBW3, "news",
     "Defendants: Anthropic, Dario Amodei, Benjamin Mann. Case 5:26-cv-09217. Pending; no ruling found.", "mbw_sony_warner_v_anthropic.html"),
    ("F29", "c3;c7", "Sony/Warner allege torrented books with 'hundreds or more' works (Exhibit A)", "pirate websites were books containing the lyrics and sheet music to hundreds or more of Music Publishers’ copyrighted musical compositions, identified in Exhibit A", SW, "primary",
     "Allegation. No total damages figure in the complaint; statutory damages per work.", "sony_warner_v_anthropic_complaint_2026-08-28.pdf"),
    ("F30", "c3;c7", "Sony/Warner: up to $150,000 per work; no total stated", "Sony and Warner are seeking statutory damages of up to $150,000 per work willfully infringed", MBW3, "news", "", "mbw_sony_warner_v_anthropic.html"),
    ("F31", "c7", "Sony/Warner: 'thousands if not tens of thousands' of works", "With the complaint covering at least “thousands if not tens of thousands” of works, the potential damages could reach into the billions of dollars.", FORT, "news",
     "Fortune's characterisation; not a $3B figure.", "fortune_sony_warner_v_anthropic.html"),
    ("F19", "c4", "English 49.5% of websites", "English is used by 49.5% of all the websites whose content language we know.", W3, "primary", "Under 50%; W3Techs counts websites (top 10M), not pages or tokens.", "w3techs_content_language.html"),
    ("F20", "c4", "English <50% since Jan 2025", "English 55.6% 53.9% 52.3% 51.2% 54.0% 56.8% 60.4% 63.6% 57.7% 52.2% 49.3% 49.4% 49.5%", W3H, "primary",
     "Columns 2015-01-01 ... 2026-01-01, 2026-10-31.", "w3techs_content_language_history_y.html"),
    ("F21", "c4", "51.3% of C4 pages US-hosted", "51.3% pages are hosted in the United States.", DODGE, "primary", "C4 is the T5 training corpus (English-only filter).", "dodge2021_c4.pdf"),
    ("F22", "c4", "Llama 2 pretraining 89.70% English", "Most data is in English, meaning that Llama 2 will perform best for English-language use cases.", LL2, "primary", "Table 10: en 89.70%.", "touvron2023_llama2.pdf"),
    ("F23", "c4", "speaker's source wording", "Current AI models are overwhelmingly based on European and North American historical literature and language.", SPK, "secondary",
     "The slide's cited page gives no study for this; the 'Over half' link points to an external statistic.", "intro_gpt_legal.html"),
    ("F26", "c4", "Common Crawl CC-MAIN-2026-43: English 42.56% of pages", "CC-MAIN-2026-43,eng,", ("Common Crawl crawl statistics: languages.csv", "Common Crawl Foundation", "2026-10 crawl",
     "https://commoncrawl.github.io/cc-crawl-statistics/plots/languages.csv"), "primary", "Row prefix; full value in data/processed/cc_english.csv (src/02_check.py).", "cc_languages.csv"),
    ("F24", "c8", "GEMA v OpenAI, LG München I, 11 Nov 2025", "Die Nutzung von Liedtexten durch den US-Konzern verstößt in den Augen der 42. Zivilkammer gegen das Urheberrecht (Urt. 11.11.2025, Az. 42 O 14139/24).", LTO, "news", "First instance; nine song lyrics. LTO: 'Das Urteil ist noch nicht rechtskräftig' (not yet final). Court press release not retrieved.", "lto_gema_openai.html"),
    ("F24b", "c8", "not yet final", "Das Urteil ist noch nicht rechtskräftig.", LTO, "news", "LTO adds that further instances are considered likely; it does not report a filed appeal.", "lto_gema_openai.html"),
    ("F25", "c9", "Getty v Stability: weights not infringing copies", "the model weights are not themselves an infringing copy and they do not store an infringing copy", GETTY, "primary", "Judgment handed down 4 Nov. 2025.", "getty_v_stability_ewhc_2025_2863.xml"),
    ("F32", "c9", "Getty granted permission to appeal (secondary infringement)", "Getty Images has been granted permission to appeal the High Court's judgment on the question of secondary copyright infringement.", BSAL, "secondary",
     "Permission granted by Joanna Smith J in Dec. 2025 ([2025] EWHC 3343 (Ch), per IPKat). No Court of Appeal decision found as of 2026-10-31.", "burgessalmon_getty_appeal.html"),
    ("F33", "c9", "appeal concerns rejection of secondary infringement claim", "granted Getty permission to appeal the rejection of its secondary infringement claim", IPKAT, "secondary", "", "ipkat_getty_appeal.html"),
]
FILES = {r[0]: r[7] for r in ROWS}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for fid, cid, value, quote, (title, pub, date, url), stype, notes, _ in ROWS:
            w.writerow([fid, cid, value, quote, title, pub, date, url, stype, notes])
    print("wrote", OUT, len(ROWS), "rows")


if __name__ == "__main__":
    main()
