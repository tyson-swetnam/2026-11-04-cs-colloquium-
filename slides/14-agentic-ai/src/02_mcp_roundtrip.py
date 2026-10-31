"""The slide's flow, over the real protocol: request -> MCP tools -> data lake -> result.

Starts mesa_tools_server.py as a subprocess, connects with the official MCP client over stdio,
discovers the tools and their JSON schemas, then makes the calls a model would plan for a
plain-language question. A scripted plan stands in for the model (no model API here); every
call, including three the server refuses, goes through MCP exactly as a model's would.

Output: data/processed/mcp_transcript.json, mcp_calls.csv
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import anyio
import pandas as pd
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SLIDE = Path(__file__).resolve().parents[1]
OUT = SLIDE / "data" / "processed"
QUESTION = "Which infrastructure build-out took the biggest share of GDP in one year, and how many claims in this talk are verified?"
PLAN = [
    ("find_data", {"question": QUESTION}),
    ("query_lake", {"sql": "SELECT name, peak_annual_pct_gdp FROM lake.buildout_ranking WHERE program <> 'postwar' ORDER BY peak_annual_pct_gdp DESC LIMIT 3"}),
    ("query_lake", {"sql": "SELECT status, count(*) AS n FROM lake.talk_claims GROUP BY status ORDER BY n DESC"}),
    # What the guardrails are for:
    ("query_lake", {"sql": "DELETE FROM lake.talk_claims WHERE status = 'contradicted'"}),
    ("resolve_term", {"text": "mouse", "curie": "NCBITaxon:10116", "field": "organism"}),
    ("check_citation", {"citation": "John Doe and Jane Smith. Webvoyager: Building an end-to-end web agent with large multimodal models. arXiv preprint arXiv:2401.00001, 2024."}),
]


def payload(result) -> object:
    if getattr(result, "structured_content", None):
        return result.structured_content
    texts = [c.text for c in result.content if getattr(c, "text", None)]
    try:
        return json.loads(texts[0]) if len(texts) == 1 else texts
    except json.JSONDecodeError:
        return texts


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(SLIDE / "src" / "mesa_tools_server.py")])
    transcript = {"question": QUESTION, "tools": [], "calls": []}
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        init = await session.initialize()
        transcript["server"] = {"name": init.server_info.name, "protocol": init.protocol_version}
        tools = await session.list_tools()
        transcript["tools"] = [{"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in tools.tools]
        for name, args in PLAN:
            result = await session.call_tool(name, args)
            transcript["calls"].append({"tool": name, "arguments": args, "is_error": bool(result.is_error), "result": payload(result)})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mcp_transcript.json").write_text(json.dumps(transcript, indent=2, default=str))
    rows = []
    for c in transcript["calls"]:
        r = c["result"]
        refused = isinstance(r, dict) and (r.get("refused") or r.get("ok") is False or r.get("verdict", "verified") != "verified")
        rows.append({"tool": c["tool"], "arguments": json.dumps(c["arguments"])[:90], "refused_or_flagged": bool(refused), "result": json.dumps(r, default=str)[:160]})
    pd.DataFrame(rows).to_csv(OUT / "mcp_calls.csv", index=False)
    print(f"server: {transcript['server']}")
    print("tools:", [t["name"] for t in transcript["tools"]])
    print(pd.DataFrame(rows)[["tool", "refused_or_flagged", "result"]].to_string(index=False, max_colwidth=110))


if __name__ == "__main__":
    anyio.run(main)
