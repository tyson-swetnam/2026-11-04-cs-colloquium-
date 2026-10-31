# Slide 11 · Agents, tools, and the Model Context Protocol

Section: 02 · Science · Slide text and notes: [`talk/slides.md`](../../talk/slides.md#slide-11)

## What needs checking

- **`c1`** (technical, low): A language model answers from what it read in training. It cannot see your files or run your code.
- **`c2`** (technical, low): An agent is a loop around the model: read the goal, call a tool, read the result, decide the next call.
- **`c3`** (technical, low): The harness owns the loop, the files it may touch and the permissions.
- **`c4`** (attribution, low): MCP is the USB-C port for agents
- **`c5`** (factual, medium): Notes: an MCP server is usable from Claude Code, Codex, Antigravity, OpenCode, Goose; MESA's MCP servers are public today

Status and the plan for each claim are in [`claims.yaml`](claims.yaml).

## Evidence

_Nothing yet. Code goes in `src/`, data in `data/`, outputs in `figures/`; see the top-level README._
