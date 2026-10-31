import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import build_site as site_builder  # noqa: E402


def test_site_builds_with_no_broken_internal_links(tmp_path):
    out = tmp_path / "_site"
    site_builder.main(out)
    assert (out / "deck" / "index.html").exists()
    broken = []
    for page in out.rglob("index.html"):
        if page.parent.name == "deck":
            continue
        for url in re.findall(r'(?:href|src)="([^"#]+)(?:#[^"]*)?"', page.read_text(encoding="utf-8")):
            if url.startswith(("http:", "https:", "mailto:")):
                continue
            target = page.parent / url
            target = target / "index.html" if url.endswith("/") else target
            if not target.resolve().exists():
                broken.append(f"{page.relative_to(out)} -> {url}")
    assert not broken, broken[:10]
