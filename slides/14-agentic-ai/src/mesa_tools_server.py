"""A minimal MCP server exposing the talk's evidence tools (run by 02_mcp_roundtrip.py, or by any MCP client).

Tools
    find_data       which lake tables match a plain-language question (keyword retrieval over descriptions)
    query_lake      read-only SQL against the DuckLake catalog; anything but SELECT is refused
    resolve_term    validate an ontology term for a metadata field (OLS4; see evidence/ontology.py)
    check_citation  check a reference against the DOI registry and arXiv (see evidence/citations.py)

Register it with an MCP client using mcp.json in this folder.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import duckdb

SLIDE = Path(__file__).resolve().parents[1]
ROOT = SLIDE.parents[1]
sys.path.insert(0, str(ROOT))

from mcp.server.mcpserver import MCPServer  # noqa: E402

from evidence.citations import Checker, parse  # noqa: E402
from evidence.ontology import OLSClient, validate  # noqa: E402

LAKE = SLIDE / "data" / "processed" / "lake"
UA = "colloquium-evidence/0.1 (UNM CARC research)"
FIELDS = {"organism": ("NCBITaxon",), "assay": ("OBI",), "cell_line": ("CLO",)}
CACHE = ROOT / "slides/17-hallucination-is-engineering/data/cache"  # reuse slide 17's API cache

server = MCPServer("mesa-evidence", instructions="Tools over the talk's evidence lake, ontologies and citation indexes.")


def _lake() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.sql("LOAD ducklake;")
    con.sql(f"ATTACH 'ducklake:{LAKE / 'catalog.ducklake'}' AS lake (DATA_PATH '{LAKE / 'data'}', READ_ONLY)")
    return con


@server.tool()
def find_data(question: str) -> list[dict]:
    """Return lake tables whose description or columns share words with the question, best first."""
    descriptions = json.loads((LAKE / "descriptions.json").read_text())
    words = {w for w in re.findall(r"[a-z]{4,}", question.lower())}
    con = _lake()
    hits = []
    for table, desc in descriptions.items():
        cols = [r[0] for r in con.execute(f"SELECT column_name FROM (DESCRIBE lake.{table})").fetchall()]
        text = (desc + " " + " ".join(cols)).lower()
        score = sum(w in text for w in words)
        if score:
            hits.append({"table": f"lake.{table}", "description": desc, "columns": cols, "score": score})
    return sorted(hits, key=lambda h: -h["score"])


@server.tool()
def query_lake(sql: str) -> dict:
    """Run a read-only SELECT against the lake. Writes, DDL and multiple statements are refused."""
    if not re.fullmatch(r"\s*(SELECT|WITH)\b[^;]*;?\s*", sql, flags=re.I | re.S):
        return {"refused": True, "reason": "only a single read-only SELECT is allowed"}
    con = _lake()
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    except duckdb.Error as e:
        return {"refused": True, "reason": str(e).splitlines()[0]}
    return {"columns": cols, "rows": [[str(v) for v in r] for r in rows[:50]], "row_count": len(rows)}


@server.tool()
def resolve_term(text: str, curie: str, field: str) -> dict:
    """Check that `curie` exists, is current, belongs to the field's ontology and is named by `text`."""
    check = validate(OLSClient(CACHE / "ols", UA), text, curie, FIELDS.get(field, ()))
    return {"ok": check.ok, "reason": check.reason, "label": check.label}


@server.tool()
def check_citation(citation: str) -> dict:
    """Check a reference string against the DOI registry and arXiv; 'verified' or the reason it failed."""
    r = Checker(CACHE / "citations", UA).check(parse(citation))
    return {"verdict": r.verdict, "detail": r.detail, "index_title": r.index_title}


if __name__ == "__main__":
    server.run("stdio")
