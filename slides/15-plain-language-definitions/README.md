# Slide 15 · Agents, tools, and the Model Context Protocol

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-15)

| Card | Verdict | Evidence |
|---|---|---|
| **The model:** answers from training; can't see your files or run your code | ✅ | True of a bare model. Products that read files or run code do it through tools in a harness, which is cards 2–3. |
| **The agent:** a loop of read goal → call tool → read result → decide | ✅ | The tool side of that loop runs in [slide 14's MCP demo](../14-agentic-ai/), with a scripted plan standing in for the model. |
| **The harness:** owns the loop, files and permissions | ✅ | In slide 14, permissions are enforced outside the model: the lake is read-only and the DELETE was refused. |
| **The protocol:** "MCP is the USB-C port for agents" | ✅ | The MCP docs: *"Think of MCP like a USB-C port for AI applications."* Credit the analogy. |

| **The protocol, part 2:** "describe a server once, and any agent that speaks MCP can use it" | ✅ | MCP docs: *"making it easy to build once and integrate everywhere."* Each client still needs its own registration line, which MESA's installer writes for you. |

**Speaker notes**
- **"Usable from Claude Code, Codex, Antigravity, OpenCode, Goose": ✅ for all five.** Each client's own documentation states MCP support (`src/01_mcp_support.py`, [`mcp_support.csv`](data/processed/mcp_support.csv)). Slide 14's server needs one [`mcp.json`](../14-agentic-ai/mcp.json) to register with any of them. Note: MESA's installer targets four of them; Goose is in the MESA CLI app but not an installer target.
- **"MESA's MCP servers are public today": ◐ partly supported** (public docs only; repos not read). The docs show a public one-line installer, say it clones the servers from the idss-mesa GitHub org, and link each repo ([`mesa_public.csv`](data/processed/mesa_public.csv), [`facts.csv`](data/raw/research/facts.csv)). Not checked: repo visibility and licence (no licence named in the docs). Two of the three registered servers are CyVerse's (Formation, irods-mcp-server); MESA's own is mesa-mcp.
  - Suggested wording: *"MESA's MCP stack is public today: one install command, and its servers' source is on GitHub (idss-mesa)."* Don't say "open source" until the licence is confirmed.

Re-run both scripts the day before the talk (documentation moves; Goose's moved to goose-docs.ai):

```bash
uv run python slides/15-plain-language-definitions/src/01_mcp_support.py
uv run python slides/15-plain-language-definitions/src/02_mesa_public.py
```
