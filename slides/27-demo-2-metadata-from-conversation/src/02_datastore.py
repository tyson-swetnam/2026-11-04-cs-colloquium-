"""Slide 27: look at the neon-beetle-seg collection on the CyVerse Data Store through
CyVerse's public, read-only Data Store MCP server (https://mcp-public.cyverse.ai/mcp,
documented on idss-mesa.github.io/docs/claude-ai/). Anonymous access only.

The plain HTTPS route (data.cyverse.org/dav-anon/...) redirected this session to a
CyVerse "Unblock Me" check, which we did not try to get past.

Usage: uv run python src/02_datastore.py [tools|call NAME JSON_ARGS OUTFILE]
Raw responses are saved under data/raw/sources/ and logged in its MANIFEST.yaml.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

SLIDE = Path(__file__).resolve().parents[1]
ROOT = SLIDE.parents[1]
sys.path.insert(0, str(ROOT))

from evidence.fetch import record  # noqa: E402

URL = "https://mcp-public.cyverse.ai/mcp"
UA = "colloquium-evidence/0.1 (UNM CARC research)"
SOURCES = SLIDE / "data" / "raw" / "sources"
HEAD = {"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}


def _parse(r: requests.Response) -> dict:
    if r.headers.get("content-type", "").startswith("text/event-stream"):
        for line in r.text.splitlines():
            if line.startswith("data:"):
                return json.loads(line[5:])
    return r.json()


class Session:
    def __init__(self) -> None:
        r = requests.post(URL, headers=HEAD, timeout=60, json={
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "colloquium-evidence", "version": "0.1"}}})
        r.raise_for_status()
        self.head = dict(HEAD, **{"Mcp-Session-Id": r.headers["mcp-session-id"], "MCP-Protocol-Version": "2025-06-18"})
        requests.post(URL, headers=self.head, timeout=60, json={"jsonrpc": "2.0", "method": "notifications/initialized"})
        self.n = 1

    def rpc(self, method: str, params: dict) -> dict:
        self.n += 1
        r = requests.post(URL, headers=self.head, timeout=120, json={"jsonrpc": "2.0", "id": self.n, "method": method, "params": params})
        r.raise_for_status()
        return _parse(r)


def save(name: str, obj: dict, note: str) -> Path:
    p = SOURCES / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    record(p, url=URL, source="CyVerse public Data Store MCP server (anonymous, read-only)", note=note)
    return p


def main() -> None:
    s = Session()
    if len(sys.argv) < 2 or sys.argv[1] == "tools":
        out = s.rpc("tools/list", {})
        save("datastore_mcp_tools.json", out, "tools/list")
        for t in out["result"]["tools"]:
            print(t["name"], "-", t.get("description", "")[:100], json.dumps(t.get("inputSchema", {}).get("properties", {}))[:200])
    else:
        _, name, args, outfile = sys.argv[1:5]
        out = s.rpc("tools/call", {"name": name, "arguments": json.loads(args)})
        save(outfile, out, f"tools/call {name} {args}")
        print(json.dumps(out, indent=1)[:6000])


if __name__ == "__main__":
    main()
