# Slide 15 · Agents, tools, and the Model Context Protocol

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-15)

| Card / note | Verdict | Key evidence | Suggested wording |
|---|---|---|---|
| **The model:** answers from training; can't see your files or run your code | ✅ | MCP docs: apps reach *"local files, databases"* and tools by connecting to them (f26), i.e. through the harness. A simplification: a model also reads what's in its prompt. | Keep |
| **The agent:** a loop of read goal → call tool → read result → decide | ✅ | The tool side of that loop runs in [slide 14's MCP demo](../14-agentic-ai/), with a scripted plan standing in for the model. | Keep |
| **The harness:** owns the loop, files and permissions | ✅ | In slide 14, permissions are enforced outside the model: the lake is read-only and the DELETE was refused. | Keep |
| **The protocol:** "MCP is the USB-C port for agents" | ✅ | MCP docs: *"Think of MCP like a USB-C port for AI applications."* | Credit the analogy |
| **The protocol, part 2:** "describe a server once, and any agent that speaks MCP can use it" | ✅ | MCP docs: *"making it easy to build once and integrate everywhere."* Each client still needs its own registration entry, and sign-in can still block a client (MESA's Formation, below). | Keep |
| **Notes:** "usable from every agent your group already uses (Claude Code, Codex, Antigravity, OpenCode, Goose)" | ◐ | All five clients' own docs state MCP support (f14–f18). But MESA's docs say OpenCode and Goose *"cannot complete the sign-in"* to the hosted Formation server in the MESA apps, Antigravity is untested, and OpenCode's irods reads public data only (f23–f25). | *"Claude Code, Codex, Antigravity, OpenCode and Goose all speak MCP, so a server you stand up once can plug into each of them, though sign-in for hosted servers can still differ by client."* |
| **Notes:** "MESA's MCP servers are public today" | ◐ | Public one-line installer; MESA's own servers mesa-mcp and irods-mcp-server are linked as idss-mesa repos and run locally *"without signing in"* (f1–f5, f19, f22). Hosted mesa-mcp *"requires authentication"*; Formation is CyVerse's (source cyverse-de/formation) and needs a CyVerse login (f7, f20–f21). Repo visibility and licence not checked (public docs only). | *"MESA's own MCP servers are public today: one install command, source on GitHub (idss-mesa), and they run locally without signing in."* Don't say "open source" until the licence is confirmed. |

Other notes:
- MESA's installer targets four of the five clients; Goose is in the MESA CLI app but not an installer target (f9–f10).
- An earlier version of these notes called irods-mcp-server CyVerse's. MESA's docs link it as idss-mesa/irods-mcp-server; only its Docker image is under `cyverse/`.
- Slide 14's `mcp.json` is no longer cited: it points to `slides/10-agentic-ai/src/mesa_tools_server.py`, which does not exist (the server is under `slides/14-agentic-ai/src/`). Slide 14 should fix that path.

Evidence: [`facts.csv`](data/raw/research/facts.csv), [`mcp_support.csv`](data/processed/mcp_support.csv), [`mesa_public.csv`](data/processed/mesa_public.csv).

Re-run both scripts the day before the talk (documentation moves; Goose's moved to goose-docs.ai):

```bash
uv run python slides/15-plain-language-definitions/src/01_mcp_support.py
uv run python slides/15-plain-language-definitions/src/02_mesa_public.py
```
