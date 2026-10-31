"""Turn saved HTML/PDF sources into plain text for quote checking."""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path


def to_text(path: Path) -> str:
    path = Path(path)
    if path.suffix == ".pdf":
        t = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
    else:
        t = path.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", " ", t, flags=re.S | re.I)
        t = re.sub(r"<[^>]+>", " ", t)
        t = html.unescape(t)
    t = t.replace(" ", " ").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-").replace("­", "")
    return re.sub(r"\s+", " ", t)
