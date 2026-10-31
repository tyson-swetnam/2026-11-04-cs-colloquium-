"""Log every document fetched for slide 23 in data/raw/sources/MANIFEST.yaml.

The documents were downloaded with curl (User-Agent "colloquium-evidence/0.1 (UNM CARC research)")
on 2026-10-31; this script records URL, retrieval date and SHA-256 for each.
"""
from pathlib import Path

from evidence.fetch import record

SRC = Path(__file__).resolve().parents[1] / "data/raw/sources"

FILES = {
    "docs.cyverse.org_architecture_system-overview_.html": ("https://docs.cyverse.org/architecture/system-overview/", "CyVerse docs: System overview"),
    "docs.cyverse.org_platform_data-store_.html": ("https://docs.cyverse.org/platform/data-store/", "CyVerse docs: Data Store (not quoted)"),
    "docs.cyverse.org_services_ds_.html": ("https://docs.cyverse.org/services/ds/", "CyVerse docs: 404 page (not used)"),
    "cyverse.org_data-store.html": ("https://cyverse.org/data-store", "CyVerse: Data Store product page"),
    "learning.cyverse.org_ds_.html": ("https://learning.cyverse.org/ds/", "CyVerse Learning Center: Data Store methods table"),
    "cyverse_unblockme.html": ("https://unblockme.cyverse.org/", "CyVerse IP unblock page (target of the dav-anon 307 redirect)"),
    "mesa_docs_llms-full.txt": ("https://idss-mesa.github.io/docs/llms-full.txt", "MESA docs full corpus"),
    "mesa_site_llms.txt": ("https://idss-mesa.github.io/llms.txt", "MESA site llms.txt"),
    "mesa_site_llms-full.txt": ("https://idss-mesa.github.io/llms-full.txt", "MESA site full corpus"),
    "mesa_sandbox_concept.md": ("https://idss-mesa.github.io/okf/concepts/mesa-sandbox.md", "MESA OKF concept: mesa-sandbox"),
    "mesa_anyjev_llms-full.txt": ("https://idss-mesa.github.io/mesa-anyjev/llms-full.txt", "mesa-anyjev docs full corpus"),
    "carc_docs_llms.txt": ("https://carc.unm.edu/docs/llms.txt", "UNM CARC docs llms.txt"),
    "carc_docs_llms-full.txt": ("https://carc.unm.edu/docs/llms-full.txt", "UNM CARC docs full corpus"),
    "carc_site_llms.txt": ("https://carc.unm.edu/llms.txt", "UNM CARC website llms.txt"),
    "carc_site_llms-full.txt": ("https://carc.unm.edu/llms-full.txt", "UNM CARC website full corpus (incl. AI research resources, jobs)"),
    "docs.jetstream-cloud.org_inference-service_overview_.html": ("https://docs.jetstream-cloud.org/inference-service/overview/", "Jetstream2 docs: Inference Service Overview"),
    "docs.jetstream-cloud.org_general_vmsizes_.html": ("https://docs.jetstream-cloud.org/general/vmsizes/", "Jetstream2 docs: Instance flavors"),
    "docs.jetstream-cloud.org_alloc_overview_.html": ("https://docs.jetstream-cloud.org/alloc/overview/", "Jetstream2 docs: Allocations overview"),
    "docs.jetstream-cloud.org_ui_cacao_overview_.html": ("https://docs.jetstream-cloud.org/ui/cacao/overview/", "Jetstream2 docs: CACAO overview"),
    "docs.jetstream-cloud.org_general_gpu_.html": ("https://docs.jetstream-cloud.org/general/gpu/", "Jetstream2 docs: 404 page (not used)"),
    "docs.jetstream-cloud.org_overview_overview-doc_.html": ("https://docs.jetstream-cloud.org/overview/overview-doc/", "Jetstream2 docs: System overview"),
    "nrp.ai_documentation_userdocs_ai_llm-managed_.html": ("https://nrp.ai/documentation/userdocs/ai/llm-managed/", "NRP docs: NRP-Managed LLMs"),
    "cider.access-ci.org_public_resources_RDR_003540.html": ("https://cider.access-ci.org/public/resources/RDR_003540", "ACCESS CiDeR: Prototype National Research Platform"),
    "docs.jetstream-cloud.org_general_running-llm_.html": ("https://docs.jetstream-cloud.org/general/running-llm/", "Jetstream2 docs: Orientation to Running LLMs (training vs inference)"),
    "nrp.ai_about_.html": ("https://nrp.ai/about/", "NRP: About (AI and machine learning workloads)"),
}

if __name__ == "__main__":
    for name, (url, source) in FILES.items():
        p = SRC / name
        if p.exists():
            record(p, url=url, source=source, note="fetched 2026-10-31 for slide 23")
            print("recorded", name)
        else:
            print("MISSING", name)
