from evidence import citations as cit


def test_parse_plain_reference_with_fake_arxiv_id():
    c = cit.parse(
        "John Doe and Jane Smith. Webvoyager: Building an end-to-end web agent with large "
        "multimodal models. arXiv preprint arXiv:2401.00001, 2024."
    )
    assert c.surnames == ["doe", "smith"]
    assert c.title.startswith("Webvoyager: Building an end-to-end web agent")
    assert c.arxiv_id == "2401.00001"


def test_parse_keeps_initials_in_author_block():
    c = cit.parse("A. Yang, B. Yang, C. Yang, et al. Qwen 3.5-mathematical report for iterative model self-improvement. arXiv: 2909.12233")
    assert c.surnames == ["yang", "yang", "yang"]
    assert c.title.startswith("Qwen 3.5")


def test_parse_doi_and_incomplete_arxiv():
    c = cit.parse("John Smith and Jane Doe. Deep learning techniques for avatars. IEEE TNNLS, 32(12):5600-5612, 2021. doi: 10.1109/ TNNLS.2021.3071234.")
    assert c.doi == "10.1109/TNNLS.2021.3071234"
    assert cit.parse("Nuo Lou and et al. Dsp: Diffusion-based span prediction. arXiv preprint arXiv:2305.XXXX, 2023.").arxiv_id == "2305.XXXX"


def test_parse_bibitem():
    entry = r"""\bibitem[Bender et~al.(2021)Bender, Gebru, McMillan-Major, and
  Shmitchell]{bender2021dangers}
Emily~M Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret
  Shmitchell.
\newblock On the dangers of stochastic parrots: Can language models be too big?
\newblock In \emph{Proceedings of the 2021 ACM conference on fairness}, pages 610--623, 2021."""
    c = cit.parse_bibitem(entry)
    assert c.title == "On the dangers of stochastic parrots: Can language models be too big?"
    assert c.surnames[:2] == ["bender", "gebru"]


def test_similarity_ignores_case_and_punctuation():
    assert cit.similar("WebVoyager: Building an End-to-End Web Agent", "Webvoyager building an end to end web agent") > 0.95
