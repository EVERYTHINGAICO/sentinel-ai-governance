# SENTINEL MCP Server

A standards-compliant [Model Context Protocol](https://modelcontextprotocol.io) server that exposes the full SENTINEL governance workflow as callable tools.

**Works with any MCP-compatible AI** — Claude, GPT-4o, Gemini, Llama, Mistral, and any model with tool-calling support.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r sentinel-mcp/requirements.txt

# 2. Verify the server starts
python sentinel-mcp/server.py
# Should output MCP initialization JSON, then wait for input

# 3. Register with your AI client (see sections below)
```

---

## Available Tools

| Tool | What it does |
|------|-------------|
| `sentinel_status` | Check prerequisites, config, and artifact state |
| `sentinel_setup` | Clone Lobster Trap, create .env |
| `sentinel_configure` | Read/write .env values securely |
| `sentinel_run_suite` | Phase 1: governance test suite |
| `sentinel_run_gemini` | Phase 2: Gemini/mock recommendations |
| `sentinel_build_dataset` | Merge artifacts → scenarios.json |
| `sentinel_serve` | Start web UI at localhost:8787 |
| `sentinel_inspect_scenarios` | Read scenario data for analysis |
| `sentinel_run_pipeline` | Run everything end-to-end |
| `sentinel_deploy` | Build GitHub Pages static site |

---

## Client Registration

### Claude Code (this project — auto-configured)

A `.claude/settings.json` file in this project already registers the server.
Just open the project in Claude Code and the tools are available automatically.

---

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or  
`%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "sentinel": {
      "command": "python",
      "args": ["/absolute/path/to/SENTINEL/sentinel-mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. The SENTINEL tools appear in the tools panel.

---

### Cursor

Create or edit `.cursor/mcp.json` in this project:

```json
{
  "mcpServers": {
    "sentinel": {
      "command": "python",
      "args": ["sentinel-mcp/server.py"]
    }
  }
}
```

Reload Cursor window (`Ctrl+Shift+P` → "Reload Window").

---

### Windsurf

Create or edit `.windsurf/mcp.json`:

```json
{
  "mcpServers": {
    "sentinel": {
      "command": "python",
      "args": ["sentinel-mcp/server.py"]
    }
  }
}
```

---

### VS Code + GitHub Copilot

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "sentinel": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/sentinel-mcp/server.py"]
    }
  }
}
```

Enable MCP in VS Code settings: `"github.copilot.chat.experimental.mcp.enabled": true`.

---

### OpenAI Agents SDK (GPT-4o / o3)

```python
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    async with MCPServerStdio(
        command="python",
        args=["sentinel-mcp/server.py"],
    ) as sentinel_server:
        agent = Agent(
            name="SENTINEL Operator",
            instructions="Help the user install, configure, and run SENTINEL.",
            mcp_servers=[sentinel_server],
        )
        result = await Runner.run(agent, "Check SENTINEL status and tell me what to do next.")
        print(result.final_output)

asyncio.run(main())
```

---

### Google ADK (Gemini 2.x)

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

sentinel_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=["sentinel-mcp/server.py"],
    )
)

agent = LlmAgent(
    model="gemini-2.5-flash",
    name="sentinel_operator",
    instruction="Help the user install and run the SENTINEL governance platform.",
    tools=[sentinel_tools],
)
```

---

### ChatGPT Desktop

1. Open ChatGPT Desktop settings → Developer → MCP Servers
2. Add new server:
   - **Command**: `python`
   - **Args**: `/absolute/path/to/SENTINEL/sentinel-mcp/server.py`
   - **Name**: `sentinel`

---

### Jan.ai (Llama 3.x local)

1. Open Jan → Settings → Extensions → MCP Servers
2. Add server configuration:

```json
{
  "name": "sentinel",
  "command": "python",
  "args": ["/absolute/path/to/SENTINEL/sentinel-mcp/server.py"],
  "enabled": true
}
```

Use any Llama 3.1+ model (tool calling required — Llama 3.1 8B or larger recommended).

---

### LM Studio (Llama local)

1. Open LM Studio → Developer → MCP
2. Add MCP server:
   - **Transport**: stdio
   - **Command**: `python sentinel-mcp/server.py`
   - **Working directory**: project root

Load any GGUF model with tool-calling support (Llama-3.1-8B-Instruct or larger).

---

### Continue.dev (VS Code / JetBrains + Ollama)

Edit `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Llama 3.1 (Ollama)",
      "provider": "ollama",
      "model": "llama3.1:8b"
    }
  ],
  "mcpServers": [
    {
      "name": "sentinel",
      "command": "python",
      "args": ["/absolute/path/to/SENTINEL/sentinel-mcp/server.py"]
    }
  ]
}
```

Make sure Ollama is running: `ollama serve` and model is pulled: `ollama pull llama3.1:8b`.

---

### Open WebUI (Ollama)

1. Open WebUI → Admin Panel → Settings → Tools → Add Tool Server
2. Configuration:
   - **Type**: MCP (stdio)
   - **Command**: `python /absolute/path/to/SENTINEL/sentinel-mcp/server.py`

---

## Lobster Trap + Ollama (Local LLM Backend)

SENTINEL's underlying enforcement engine (Lobster Trap) is already designed for Ollama:

```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull llama3.1:8b

# Start Lobster Trap with Ollama as the AI backend
./lobstertrap/lobstertrap serve --listen :8080 --backend http://localhost:11434
```

This means SENTINEL can run 100% locally — no cloud APIs required:
- **Enforcement layer**: Lobster Trap + Ollama/Llama
- **Governance recommendations**: Gemini mock mode (or real API optionally)
- **Operator AI**: any Llama model via Ollama + MCP client

---

## Windows Notes

Phase 1 (`sentinel_run_suite`) requires bash. Options:
1. **WSL** (recommended): `wsl --install` in PowerShell, then restart
2. **Git Bash**: install [Git for Windows](https://git-scm.com)

Phase 2, build, serve, and deploy work natively on Windows without bash.

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google AI Studio key for real Gemini mode | (none — uses mock) |
| `GOOGLE_API_KEY` | Alias for GEMINI_API_KEY | (none) |
| `GEMINI_MODEL` | Gemini model ID | `gemini-2.5-flash-lite` |
| `OLLAMA_ENDPOINT` | Ollama API URL | `http://localhost:11434` |

Configure via `sentinel_configure` tool or edit `.env` directly.
