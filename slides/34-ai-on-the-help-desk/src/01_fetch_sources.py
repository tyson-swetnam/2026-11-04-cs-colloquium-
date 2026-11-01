"""Slide 34: fetch NVIDIA's DGX Spark specifications (product page, hardware guide, launch release).

    uv run python slides/34-ai-on-the-help-desk/src/01_fetch_sources.py [--refresh]
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from tools.source_fetch import fetch_pages  # noqa: E402

PAGES = {
    "nvidia_dgx_spark.html": ("https://www.nvidia.com/en-us/products/workstations/dgx-spark/", "NVIDIA DGX Spark product page"),
    "nvidia_dgx_spark_hardware.html": ("https://docs.nvidia.com/dgx/dgx-spark/hardware.html", "NVIDIA DGX Spark User Guide: Hardware Overview"),
    "nvidia_dgx_spark_release.html": ("https://nvidianews.nvidia.com/news/nvidia-dgx-spark-arrives-for-worlds-ai-developers",
                                      "NVIDIA newsroom, 13 Oct 2025: DGX Spark arrives"),
}

if __name__ == "__main__":
    sys.exit(1 if fetch_pages(HERE, PAGES, refresh="--refresh" in sys.argv) else 0)
