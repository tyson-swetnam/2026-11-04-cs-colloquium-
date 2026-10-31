from evidence.ontology import names_match


def test_names_match_variants():
    names = ["Mus musculus", "house mouse", "mouse"]
    assert names_match("Mouse", names)
    assert names_match("M. musculus", names)
    assert names_match("HeLa cells", ["HeLa cell", "HeLa"])
    assert names_match("RNA-seq", ["transcription profiling by RNA sequencing assay", "RNA-seq assay"])
    assert names_match("RNAseq", ["transcription profiling by RNA sequencing assay", "RNA-seq assay"])
    assert not names_match("mouse", ["Rattus norvegicus", "rat", "Norway rat"])
    assert names_match("mm²", ["square millimeter", "mm2"])
    assert not names_match("RNA", ["transcription profiling by RNA sequencing assay", "RNA-seq assay"])
    assert not names_match("transcriptome", ["transcription profiling by RNA sequencing assay", "RNA-seq assay"])
