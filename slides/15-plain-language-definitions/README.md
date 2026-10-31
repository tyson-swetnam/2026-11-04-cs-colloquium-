# Slide 15 · Agents, tools, and the Model Context Protocol

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-15)

| Card | Verdict | Evidence |
|---|---|---|
| **The model:** answers from training; can't see your files or run your code | ✅ | True of a bare model. Products that read files or run code do it through tools in a harness, which is cards 2–3. |
| **The agent:** a loop of read goal → call tool → read result → decide | ✅ | The tool side of that loop runs in [slide 14's MCP demo](../14-agentic-ai/), with a scripted plan standing in for the model. |
| **The harness:** owns the loop, files and permissions | ✅ | In slide 14, permissions are enforced outside the model: the lake is read-only and the DELETE was refused. |
| **The protocol:** "MCP is the USB-C port for agents" | ✅ | The MCP docs: *"Think of MCP like a USB-C port for AI applications."* Credit the analogy. |

**Speaker notes**
- **"Usable from Claude Code, Codex, Antigravity, OpenCode, Goose": ✅ for all five.** Each client's own documentation states MCP support (`src/01_mcp_support.py`, [`mcp_support.csv`](data/processed/mcp_support.csv)). Slide 14's server needs one [`mcp.json`](../14-agentic-ai/mcp.json) to register with any of them.
- **"MESA's MCP servers are public today": ⬜ pending** until the github.com/idss-mesa repositories are attached.

Goose's documentation moved from block.github.io/goose to goose-docs.ai, so re-run the script the day before the talk:

```bash
uv run python slides/15-plain-language-definitions/src/01_mcp_support.py
```
