"""Download (once) the documents behind slide 09 and log each in data/raw/sources/MANIFEST.yaml.

Run from the repo root:  uv run python slides/09-contested-data/src/01_fetch.py
Wikipedia API returned 429 on 2026-10-31, so it is not used. Files that fail (403, bot challenge) are reported and skipped, never retried with another identity.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evidence.fetch import fetch  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "data/raw/sources"
UA = "colloquium-evidence/0.1 (UNM CARC research)"

DOCS = {
    # Bartz v. Anthropic
    "bartz_dkt231_fair_use_order.pdf": ("https://storage.courtlistener.com/recap/gov.uscourts.cand.434709/gov.uscourts.cand.434709.231.0.pdf",
                                        "Bartz v. Anthropic, N.D. Cal. 3:24-cv-05417, Order on Fair Use (Dkt. 231), 2025-06-23"),
    "bartz_settlement_site.html": ("https://www.anthropiccopyrightsettlement.com/",
                                   "Official court-authorized settlement website (JND)"),
    "bartz_long_form_notice.pdf": ("https://assets-us-01.kc-usercontent.com:443/1eeb16db-4934-006e-40a6-38fa91285ebb/ce109a57-390c-4d76-ad65-5807d4830fe5/ANT%20-%20Long-Form%20Notice_Updated%20Deadline%201.8.2026.pdf",
                                   "Court-authorized long-form notice (updated deadline 2026-01-08)"),
    "authorsguild_final_approval.html": ("https://authorsguild.org/news/court-grants-final-approval-anthropic-copyright-settlement/",
                                         "Authors Guild news, final approval (2026-07-21)"),
    "pearlcohen_final_approval.html": ("https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history",
                                       "Pearl Cohen client update on final approval (2026-07-30)"),
    "authorsalliance_fairness_hearing.html": ("https://www.authorsalliance.org/2026/05/14/bartz-v-anthropic-fairness-hearing-final-reminder-91-3-claims-rate-and-updates-from-the-docket/",
                                              "Authors Alliance, 2026-05-14"),
    # Kadrey v. Meta
    "kadrey_dkt598_sj_order.pdf": ("https://storage.courtlistener.com/recap/gov.uscourts.cand.415175/gov.uscourts.cand.415175.598.0.pdf",
                                   "Kadrey v. Meta, N.D. Cal. 3:23-cv-03417, SJ order (Dkt. 598), 2025-06-25"),
    # NYT v. OpenAI / Microsoft
    "joneswalker_20m_logs.html": ("https://www.joneswalker.com/en/insights/blogs/ai-law-blog/openai-loses-privacy-gambit-20-million-chatgpt-logs-likely-headed-to-copyright-p.html",
                                  "Jones Walker AI Law Blog on Stein order affirming 20M-log production"),
    "abajournal_20m_logs.html": ("https://www.abajournal.com/news/article/chatgpt-creator-must-turn-over-20m-chat-logs-in-copyright-litigation-federal-judge-says",
                                 "ABA Journal"),
    # Disney/Universal v. Midjourney
    "graphicpolicy_midjourney_2026-05.html": ("https://graphicpolicy.com/2026/05/11/disney-warner-bros-universal-and-midjourney-discovery-dispute/",
                                              "Graphic Policy, 2026-05-11"),
    # Music publishers v. Anthropic (second suit)
    "ipwatchdog_publishers_v_anthropic.html": ("https://ipwatchdog.com/2026/01/29/music-publishers-file-new-piracy-suit-against-anthropic-alleging-mass-torrenting-copyrighted-works/",
                                               "IPWatchdog, 2026-01-29"),
    "mbw_publishers_v_anthropic.html": ("https://www.musicbusinessworldwide.com/umg-concord-and-abkco-sue-anthropic-for-3bn-in-what-could-be-single-largest-non-class-action-copyright-case-in-us-history/",
                                        "Music Business Worldwide, 2026-01-28"),
    "techcrunch_publishers_v_anthropic.html": ("https://techcrunch.com/2026/01/29/music-publishers-sue-anthropic-for-3b-over-flagrant-piracy-of-20000-works/",
                                               "TechCrunch, 2026-01-29"),
    # Language of web content and training data
    "w3techs_content_language.html": ("https://w3techs.com/technologies/overview/content_language",
                                      "W3Techs, Usage statistics of content languages for websites"),
    "w3techs_content_language_history_y.html": ("https://w3techs.com/technologies/history_overview/content_language/ms/y",
                                                "W3Techs, historical yearly trends in content languages"),
    "dodge2021_c4_abs.html": ("https://arxiv.org/abs/2104.08758",
                              "Dodge et al. 2021, Documenting Large Webtext Corpora (C4), arXiv abstract"),
    # Cited source on the slide
    "intro_gpt_legal.html": ("https://tyson-swetnam.github.io/intro-gpt/legal/",
                             "Speaker's own compiled legal page cited on slide"),
}
EXTRA = {
    # Primary documents found as links in the secondary pages above
    "bartz_final_approval_order.pdf": ("https://publishers.org/wp-content/uploads/2026/07/Order-Granting-Final-Approval-of-Settlement171.pdf",
                                       "Bartz v. Anthropic, Order Granting Final Approval of Settlement (copy hosted by AAP)"),
    "publishers_v_anthropic_complaint_2026-01-28.pdf": ("https://www.musicbusinessworldwide.com/files/2026/01/Anthropic-complaint-01.28.26-1.pdf",
                                                        "Concord Music Group et al. v. Anthropic (N.D. Cal., filed 2026-01-28), complaint (copy hosted by MBW)"),
    "nysd_20m_logs_order.pdf": ("https://assets.law360news.com/2426000/2426657/https-ecf-nysd-uscourts-gov-doc1-127138822336.pdf",
                                "In re OpenAI Copyright Infringement Litig., S.D.N.Y. 25-md-3143, order on 20M logs (copy hosted by Law360)"),
    # Training-data composition
    "dodge2021_c4.pdf": ("https://arxiv.org/pdf/2104.08758", "Dodge et al. 2021, Documenting Large Webtext Corpora (EMNLP 2021)"),
    "touvron2023_llama2.pdf": ("https://arxiv.org/pdf/2307.09288", "Touvron et al. 2023, Llama 2 (Meta), Table 10 language distribution"),
    "cc_languages.csv": ("https://commoncrawl.github.io/cc-crawl-statistics/plots/languages.csv",
                         "Common Crawl crawl statistics: primary-language distribution per crawl"),
    # Case status pages
    "cietw_sj_briefing_2026-09-04.html": ("https://chatgptiseatingtheworld.com/2026/09/04/summary-judgment-briefing-starts-in-openai-mdl-litigation-before-judge-stein/",
                                          "ChatGPT Is Eating the World (Edward Lee), 2026-09-04"),
    "nysd_640396_dkt1586.pdf": ("https://storage.courtlistener.com/recap/gov.uscourts.nysd.640396/gov.uscourts.nysd.640396.1586.0.pdf",
                                "In re OpenAI Copyright Infringement Litig., S.D.N.Y. 25-md-3143, Dkt. 1586 (RECAP)"),
    "graphicpolicy_midjourney_tag.html": ("https://graphicpolicy.com/tag/midjourney/", "Graphic Policy, Midjourney tag page (latest case posts)"),
    "lto_gema_openai.html": ("https://www.lto.de/recht/nachrichten/n/42o1413924-lg-muenchen-i-gema-openai-chatgpt-songtexte-ki",
                             "Legal Tribune Online, LG München I GEMA v OpenAI (2025-11-11)"),
    "getty_v_stability_ewhc_2025_2863.xml": ("https://caselaw.nationalarchives.gov.uk/ewhc/ch/2025/2863/data.xml",
                                             "Getty Images v Stability AI [2025] EWHC 2863 (Ch), The National Archives Find Case Law"),
    "mbw_anthropic_partial_dismissal.html": ("https://www.musicbusinessworldwide.com/anthropic-seeks-partial-dismissal-in-music-publishers-3b-lyrics-suit-as-CEO-moves-to-drop-the-direct-infringement-claim-against-him/",
                                             "Music Business Worldwide, Aug. 2026"),
    # Added after review (2026-10-31)
    "graphicpolicy_midjourney_2025-11-14.html": ("https://graphicpolicy.com/2025/11/14/court-suggests-disney-v-midjourney-go-to-mediation/",
                                                 "Graphic Policy, 2025-11-14 (mediation schedule)"),
    "mbw_sony_warner_v_anthropic.html": ("https://www.musicbusinessworldwide.com/now-sony-music-publishing-and-warner-chappell-sue-anthropic-in-multi-billion-dollar-lawsuit-one-of",
                                         "Music Business Worldwide, Sony Music Publishing and Warner Chappell v. Anthropic (Aug. 2026)"),
    "sony_warner_v_anthropic_complaint_2026-08-28.pdf": ("https://www.musicbusinessworldwide.com/files/2026/08/COMPLAINT-in-Sony_Music_Publishing_US_LLC_e.pdf",
                                                         "Sony Music Publishing et al. v. Anthropic et al. (N.D. Cal., filed 2026-08-28), complaint (copy hosted by MBW)"),
    "fortune_sony_warner_v_anthropic.html": ("https://fortune.com/2026/09/01/anthropic-warner-sony-music-songs-lawsuit/",
                                             "Fortune, 2026-09-01"),
    "aljazeera_sony_warner_v_anthropic.html": ("https://www.aljazeera.com/economy/2026/8/31/sony-warner-music-sue-anthropic-saying-it-pirated-songs-to-train-its-ai",
                                               "Al Jazeera (Reuters), 2026-08-31"),
    "burgessalmon_getty_appeal.html": ("https://www.burges-salmon.com/articles/102lydc/getty-images-v-stability-ai-getty-granted-permission-to-appeal",
                                       "Burges Salmon, Getty granted permission to appeal (Jan. 2026)"),
    "ipkat_getty_appeal.html": ("https://ipkitten.blogspot.com/2026/01/permission-to-appeal-granted-in-getty.html",
                                "IPKat, Permission to appeal granted in Getty (Jan. 2026)"),
}


def main() -> None:
    for name, (url, source) in {**DOCS, **EXTRA}.items():
        try:
            fetch(url, SRC / name, source=source, user_agent=UA)
            print("ok  ", name)
        except Exception as e:  # noqa: BLE001
            print("FAIL", name, e)


if __name__ == "__main__":
    main()
