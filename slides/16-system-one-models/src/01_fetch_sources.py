"""Slide 16: fetch the vendor pages and model cards behind the System One slide.

Saves raw HTML/Markdown/JSON plus a de-tagged .txt next to it under data/raw/sources/
(gitignored), logs each in MANIFEST.yaml, and uses CachedGet with data/cache.
Re-run before the talk; delete data/cache to refresh.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

SLIDE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SLIDE.parents[1]))
from evidence.fetch import record  # noqa: E402
from evidence.http import CachedGet  # noqa: E402

UA = "colloquium-evidence/0.1 (UNM CARC research)"
RAW = SLIDE / "data" / "raw" / "sources"

SOURCES = {
    # name: (url, publisher)
    "typesafe_launch": ("https://typesafe.ai/blog/introducing-system-one-models-and-jev", "TypeSafe AI"),
    "typesafe_concept": ("https://docs.typesafe.ai/concepts/system-one", "TypeSafe AI"),
    "typesafe_confidence": ("https://docs.typesafe.ai/confidence", "TypeSafe AI"),
    "typesafe_models": ("https://docs.typesafe.ai/models", "TypeSafe AI"),
    "typesafe_jagged": ("https://docs.typesafe.ai/model-jaggedness/jev-1.13", "TypeSafe AI"),
    "cloudflare_blog": ("https://blog.cloudflare.com/clef-decision-models", "Cloudflare"),
    "hf_clef_readme": ("https://huggingface.co/Cloudflare/clef/raw/main/README.md", "Cloudflare (Hugging Face)"),
    "hf_clef_flash_readme": ("https://huggingface.co/Cloudflare/clef-flash/raw/main/README.md", "Cloudflare (Hugging Face)"),
    "hf_clef_license": ("https://huggingface.co/Cloudflare/clef/raw/main/LICENSE", "Cloudflare (Hugging Face)"),
    "hf_clef_flash_license": ("https://huggingface.co/Cloudflare/clef-flash/raw/main/LICENSE", "Cloudflare (Hugging Face)"),
    "hf_api_clef": ("https://huggingface.co/api/models/Cloudflare/clef", "Hugging Face API"),
    "hf_api_clef_flash": ("https://huggingface.co/api/models/Cloudflare/clef-flash", "Hugging Face API"),
    "hf_api_clef_omni": ("https://huggingface.co/api/models/Cloudflare/clef-omni", "Hugging Face API"),
    "cloudflare_clairic": ("https://blog.cloudflare.com/clairic-extraction-model/", "Cloudflare"),
    "hf_clef_code": ("https://huggingface.co/Cloudflare/clef/raw/main/joint_schema_model.py", "Cloudflare (Hugging Face)"),
    "arxiv_xiong_2306_13063": ("https://export.arxiv.org/api/query?id_list=2306.13063", "arXiv"),
    "som_guide": ("https://systemonemodels.org/guides/what-is-a-system-one-model/", "systemonemodels.org"),
    "betterstack": ("https://betterstack.com/community/guides/ai/jev-vs-clef-decision-model/", "Better Stack"),
    "mindstudio": ("https://www.mindstudio.ai/blog/jev-system-one-model-launch", "MindStudio"),
}


def to_text(body: str) -> str:
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()


def main() -> None:
    get = CachedGet(SLIDE / "data" / "cache", UA)
    RAW.mkdir(parents=True, exist_ok=True)
    for name, (url, publisher) in SOURCES.items():
        status, body = get(url)
        ext = ".json" if "/api/models" in url else ".xml" if "export.arxiv" in url else ".py" if url.endswith(".py") else ".md" if url.endswith(".md") else ".html"
        raw = RAW / f"{name}{ext}"
        raw.write_text(body, encoding="utf-8")
        record(raw, url=url, source=publisher, note=f"HTTP {status}")
        txt = RAW / f"{name}.txt"
        txt.write_text(to_text(body) if ext == ".html" else body, encoding="utf-8")
        record(txt, url=url, source=publisher, note=f"text extracted from {raw.name}")
        print(f"{status} {len(body):>8} {name}")


if __name__ == "__main__":
    main()
