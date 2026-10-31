# Slide 14 · Agentic AI

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-14)

> **That power, for researchers outside computer science**
> [One line: a researcher asks in plain language; the agent finds the data, runs the analysis, and returns a result.]
> *Notes:* Walk the flow left to right: user request, MCP context and RAG retrieval feed the orchestrator, which reaches the data mesh and data lake, then the result loops back to the user.

## Candidate lines

1. **Chosen (2026-10-31):** *"Ask in plain language; the agent finds the data, runs the analysis, and returns a result you can audit."*
2. *"A researcher asks a question in plain language; the agent finds the data, runs the analysis, and shows its work."*
3. *"You ask the question. The agent finds the data, runs the analysis, and returns the result with every step recorded."*

Option 1 ties the slide back to slide 17's controls; option 3 sets up provenance.

## The figure's flow, running over the real protocol

`src/mesa_tools_server.py` is an MCP server built with the official Python SDK. It exposes four tools over a DuckLake catalog built from this talk's own evidence (`src/01_build_lake.py`):

| Tool | Job | Box in the figure |
|---|---|---|
| `find_data` | Which tables answer a plain-language question | RAG retrieval (keyword, not vector) |
| `query_lake` | Read-only SQL; anything but a single SELECT is refused | Data lake (DuckLake) |
| `resolve_term` | Ontology validation (slide 17, control 2) | Guardrail |
| `check_citation` | DOI registry and arXiv (slide 17, control 1) | Guardrail |

`src/02_mcp_roundtrip.py` starts the server, connects with the official MCP client (protocol 2025-11-25) and discovers the tools and their JSON schemas. It then makes the calls a model would plan for *"Which infrastructure build-out took the biggest share of GDP in one year, and how many claims in this talk are verified?"*

| Call | Result |
|---|---|
| `find_data(question)` | `lake.buildout_ranking`, `lake.talk_claims` |
| `query_lake(SELECT … peak_annual_pct_gdp …)` | US railroads 5.42%, Marshall Plan 2.17%, … |
| `query_lake(SELECT status, count(*) …)` | the talk's own claim register by status |
| `query_lake(DELETE …)` | **refused**: only a single read-only SELECT is allowed |
| `resolve_term("mouse", NCBITaxon:10116)` | **refused**: names *Rattus norvegicus* |
| `check_citation(GPTZero's fake WebVoyager reference)` | **flagged**: arXiv:2401.00001 is a different paper |

The full transcript is in [`mcp_transcript.json`](data/processed/mcp_transcript.json).

**What this demo shows**
- **The tool layer and lake work.** MCP tools, retrieval and the DuckLake lake all run, and the result comes back to the requester.
- **The policies hold whoever plans the calls.** The refusals don't depend on what is doing the planning.
- **The same server works from any MCP client.** Register [`mcp.json`](mcp.json) in Claude Code, Codex, Goose or another client.

**What it doesn't show**
- **A model as orchestrator.** A scripted plan stands in, because there's no model API in this environment; slide 29's demo is the model-in-the-loop evidence.
- **The iRODS mesh.** That's slides 22–23.

**For a CS audience:** the figure draws MCP as "context." It is mainly the channel the orchestrator uses to *call tools*, which here means the lake and the guardrails.

## Pending

Mapping each box to MESA's own code (`c3`) needs the github.com/idss-mesa repositories attached to this session. The repository listing was unavailable on 2026-10-31.

## Reproduce

```bash
uv run python slides/14-agentic-ai/src/01_build_lake.py
```

```bash
uv run python slides/14-agentic-ai/src/02_mcp_roundtrip.py
```
