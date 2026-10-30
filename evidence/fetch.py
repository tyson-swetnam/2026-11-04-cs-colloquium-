"""Download source data once, then record where it came from.

Every file pulled from the network lands next to a MANIFEST.yaml that records
the URL, retrieval date and SHA-256, so a reviewer can tell whether the bytes
behind a figure have changed since it was made.
"""

from __future__ import annotations

import datetime as dt
import hashlib
from pathlib import Path

import requests
import yaml


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path, *, source: str = "", license: str = "", refresh: bool = False) -> Path:
    """Download `url` to `dest` unless it is already there, and log it in dest's MANIFEST.yaml."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if refresh or not dest.exists():
        resp = requests.get(url, timeout=120, headers={"User-Agent": "colloquium-evidence/0.1"})
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        record(dest, url=url, source=source, license=license)
    return dest


def record(path: Path, *, url: str = "", source: str = "", license: str = "", note: str = "") -> None:
    """Add or update the manifest entry for a file, including ones placed by hand."""
    path = Path(path)
    manifest_path = path.parent / "MANIFEST.yaml"
    manifest = yaml.safe_load(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest = manifest or {}
    manifest[path.name] = {
        k: v
        for k, v in {
            "url": url,
            "source": source,
            "license": license,
            "note": note,
            "retrieved": dt.date.today().isoformat(),
            "sha256": sha256(path),
        }.items()
        if v
    }
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True, allow_unicode=True))
