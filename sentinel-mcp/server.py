#!/usr/bin/env python3
"""
SENTINEL MCP Server
Exposes SENTINEL governance workflow tools over the MCP stdio protocol.
Compatible with: Claude, GPT-4o, Gemini, Llama 3.x (via Ollama), and any
MCP-compliant client (Claude Desktop, Cursor, Windsurf, Jan.ai, LM Studio,
Continue.dev, Open WebUI, Google ADK, OpenAI Agents SDK).
"""

import asyncio
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from dotenv import dotenv_values
import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# ---------------------------------------------------------------------------
# Project root: two levels up from this file (sentinel-mcp/server.py)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
LOBSTERTRAP_DIR = PROJECT_ROOT / "lobstertrap"
SUITE_SCRIPT = PROJECT_ROOT / "research" / "governance-suite" / "scripts" / "run-suite.sh"
GEMINI_SCRIPT = PROJECT_ROOT / "research" / "gemini-validation" / "scripts" / "run-gemini-validation.py"
BUILD_SCRIPT = PROJECT_ROOT / "sentinel-wrapper" / "scripts" / "build_dataset.py"
WRAPPER_DIR = PROJECT_ROOT / "sentinel-wrapper"
SCENARIOS_FILE = WRAPPER_DIR / "data" / "scenarios.json"
OBSERVED_LATEST = PROJECT_ROOT / "research" / "governance-suite" / "observed" / "latest"
GEMINI_LATEST = PROJECT_ROOT / "research" / "gemini-validation" / "outputs" / "latest"
SUBMISSION_SITE = PROJECT_ROOT / "submission" / "site"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _run(args: list[str], cwd: Path | None = None, env: dict | None = None) -> tuple[bool, str]:
    """Run a subprocess, return (success, combined output)."""
    try:
        result = subprocess.run(
            args,
            cwd=str(cwd or PROJECT_ROOT),
            capture_output=True,
            text=True,
            env={**os.environ, **(env or {})},
            timeout=300,
        )
        output = result.stdout + result.stderr
        return result.returncode == 0, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out after 300 seconds."
    except Exception as e:
        return False, str(e)


def _bash_runner() -> list[str] | None:
    """Return the bash executable for the current platform, or None."""
    if platform.system() != "Windows":
        return ["bash"]
    for candidate in [
        r"C:\Windows\System32\bash.exe",          # WSL
        r"C:\Program Files\Git\bin\bash.exe",      # Git Bash
        r"C:\Program Files (x86)\Git\bin\bash.exe",
    ]:
        if Path(candidate).exists():
            return [candidate]
    if _cmd_exists("bash"):
        return ["bash"]
    return None


def _read_env() -> dict[str, str]:
    if ENV_FILE.exists():
        return {k: v for k, v in dotenv_values(ENV_FILE).items() if v is not None}
    return {}


def _ok(output: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps({"success": True, "output": output, "error": None}))]


def _err(error: str, output: str = "") -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps({"success": False, "output": output, "error": error}))]


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
server = Server("sentinel-mcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="sentinel_status",
            description=(
                "Check SENTINEL project status: prerequisites (Python, Git, Go, Ollama), "
                ".env configuration, Phase 1/2 artifacts, and dataset freshness. "
                "Always run this first to understand what needs to be done."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="sentinel_setup",
            description=(
                "Set up SENTINEL: clone the Lobster Trap repo, create a .env file from "
                "the template, and optionally store a Gemini API key. Safe to run multiple times."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "gemini_api_key": {
                        "type": "string",
                        "description": "Optional Gemini API key (stored in .env, never logged)",
                    },
                    "clone_lobstertrap": {
                        "type": "boolean",
                        "description": "Clone the Lobster Trap repo if missing (default true)",
                        "default": True,
                    },
                },
            },
        ),
        types.Tool(
            name="sentinel_configure",
            description=(
                "Read or update SENTINEL environment variables in .env. "
                "Supports GEMINI_API_KEY, GEMINI_MODEL, OLLAMA_ENDPOINT. "
                "API key values are never echoed back."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["read", "write"],
                        "description": "'read' returns current non-secret settings; 'write' updates values",
                        "default": "read",
                    },
                    "gemini_api_key": {"type": "string", "description": "New GEMINI_API_KEY value"},
                    "gemini_model": {"type": "string", "description": "New GEMINI_MODEL value"},
                    "ollama_endpoint": {"type": "string", "description": "Ollama API endpoint, e.g. http://localhost:11434"},
                },
            },
        ),
        types.Tool(
            name="sentinel_run_suite",
            description=(
                "Run Phase 1: the governance test suite using Lobster Trap. "
                "Executes run-suite.sh via bash (Mac/Linux) or WSL/Git Bash (Windows). "
                "Produces observed artifacts under research/governance-suite/observed/latest/."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="sentinel_run_gemini",
            description=(
                "Run Phase 2: Gemini validation. Reads Phase 1 artifacts and calls the "
                "Gemini API (or uses mock mode if no key is set) to produce structured "
                "governance recommendations under research/gemini-validation/outputs/latest/."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "mock_mode": {
                        "type": "boolean",
                        "description": "Force mock mode even if GEMINI_API_KEY is present (default false)",
                        "default": False,
                    }
                },
            },
        ),
        types.Tool(
            name="sentinel_build_dataset",
            description=(
                "Aggregate Phase 1 and Phase 2 artifacts into sentinel-wrapper/data/scenarios.json. "
                "Must be run after sentinel_run_suite and sentinel_run_gemini."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="sentinel_serve",
            description=(
                "Start the SENTINEL web interface at http://localhost:8787. "
                "Opens the governance review UI with all scenarios loaded. "
                "Runs in the background — press Ctrl+C in the terminal to stop."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="sentinel_inspect_scenarios",
            description=(
                "Read and return the current scenarios.json dataset as structured data. "
                "Shows all governance scenarios with Lobster Trap verdicts and "
                "SENTINEL/Gemini recommendations. Useful for any LLM to analyze the data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_name": {
                        "type": "string",
                        "description": "Optional: filter to a single scenario by name",
                    }
                },
            },
        ),
        types.Tool(
            name="sentinel_run_pipeline",
            description=(
                "Run the complete SENTINEL pipeline end-to-end: "
                "Phase 1 (governance suite) → Phase 2 (Gemini validation) → "
                "build dataset → start web server. "
                "Use this for a quick demo or first-time setup."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "skip_suite": {
                        "type": "boolean",
                        "description": "Skip Phase 1 (use existing artifacts)",
                        "default": False,
                    },
                    "mock_gemini": {
                        "type": "boolean",
                        "description": "Use mock Gemini responses instead of real API",
                        "default": False,
                    },
                    "serve": {
                        "type": "boolean",
                        "description": "Start the web server after building (default true)",
                        "default": True,
                    },
                },
            },
        ),
        types.Tool(
            name="sentinel_deploy",
            description=(
                "Build the GitHub Pages static payload for SENTINEL deployment. "
                "Copies public assets and scenarios.json into submission/site/. "
                "Automates section C of the deployment checklist."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "validate_locally": {
                        "type": "boolean",
                        "description": "After building, start a local server on port 8899 to validate",
                        "default": False,
                    }
                },
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "sentinel_status":
        return await _tool_status()
    elif name == "sentinel_setup":
        return await _tool_setup(arguments)
    elif name == "sentinel_configure":
        return await _tool_configure(arguments)
    elif name == "sentinel_run_suite":
        return await _tool_run_suite()
    elif name == "sentinel_run_gemini":
        return await _tool_run_gemini(arguments)
    elif name == "sentinel_build_dataset":
        return await _tool_build_dataset()
    elif name == "sentinel_serve":
        return await _tool_serve()
    elif name == "sentinel_inspect_scenarios":
        return await _tool_inspect(arguments)
    elif name == "sentinel_run_pipeline":
        return await _tool_pipeline(arguments)
    elif name == "sentinel_deploy":
        return await _tool_deploy(arguments)
    else:
        return _err(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------

async def _tool_status() -> list[types.TextContent]:
    lines = ["## SENTINEL Status\n"]

    def check(label: str, ok: bool, detail: str = "") -> str:
        icon = "✓" if ok else "✗"
        suffix = f"  ({detail})" if detail else ""
        return f"  {icon} {label}{suffix}"

    # Prerequisites
    lines.append("### Prerequisites")
    py_ver = sys.version.split()[0]
    lines.append(check("Python", True, py_ver))

    git_ok = _cmd_exists("git")
    lines.append(check("Git", git_ok, "install from git-scm.com" if not git_ok else ""))

    go_ok = _cmd_exists("go")
    lines.append(check("Go", go_ok, "needed to build Lobster Trap from source — install from golang.org" if not go_ok else ""))

    ollama_ok = _cmd_exists("ollama")
    lines.append(check("Ollama", ollama_ok, "optional — local LLM backend at :11434" if not ollama_ok else "running"))

    bash_runner = _bash_runner()
    lines.append(check("Bash / WSL", bash_runner is not None, "needed for Phase 1 on Windows" if not bash_runner else ""))

    # Config
    lines.append("\n### Configuration (.env)")
    env = _read_env()
    lines.append(check(".env file", ENV_FILE.exists(), "run sentinel_setup to create" if not ENV_FILE.exists() else ""))
    key_set = bool(env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY"))
    lines.append(check("GEMINI_API_KEY", key_set, "mock mode will be used" if not key_set else "set"))
    model = env.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
    lines.append(check("GEMINI_MODEL", True, model))

    # Artifacts
    lines.append("\n### Project Artifacts")
    lt_exists = LOBSTERTRAP_DIR.exists()
    lines.append(check("lobstertrap/ repo", lt_exists, "run sentinel_setup to clone" if not lt_exists else ""))

    suite_ok = OBSERVED_LATEST.exists() and any(OBSERVED_LATEST.iterdir()) if OBSERVED_LATEST.exists() else False
    lines.append(check("Phase 1 artifacts", suite_ok, "run sentinel_run_suite" if not suite_ok else ""))

    gemini_ok = GEMINI_LATEST.exists() and any(GEMINI_LATEST.iterdir()) if GEMINI_LATEST.exists() else False
    lines.append(check("Phase 2 artifacts", gemini_ok, "run sentinel_run_gemini" if not gemini_ok else ""))

    ds_ok = SCENARIOS_FILE.exists() and SCENARIOS_FILE.stat().st_size > 100
    lines.append(check("scenarios.json dataset", ds_ok, "run sentinel_build_dataset" if not ds_ok else f"{SCENARIOS_FILE.stat().st_size} bytes"))

    # Recommended next action
    lines.append("\n### Recommended next action")
    if not lt_exists:
        lines.append("→ Run `sentinel_setup` to clone Lobster Trap and create .env")
    elif not suite_ok:
        lines.append("→ Run `sentinel_run_suite` (Phase 1: governance test scenarios)")
    elif not gemini_ok:
        lines.append("→ Run `sentinel_run_gemini` (Phase 2: Gemini recommendations)")
    elif not ds_ok:
        lines.append("→ Run `sentinel_build_dataset` to generate scenarios.json")
    else:
        lines.append("→ All good! Run `sentinel_serve` to open the web UI at http://localhost:8787")

    return _ok("\n".join(lines))


async def _tool_setup(args: dict) -> list[types.TextContent]:
    steps = []
    gemini_key = args.get("gemini_api_key", "")
    clone = args.get("clone_lobstertrap", True)

    # Clone Lobster Trap
    if clone:
        if LOBSTERTRAP_DIR.exists():
            steps.append("✓ lobstertrap/ already exists — skipped clone")
        else:
            steps.append("Cloning Lobster Trap...")
            ok, out = _run(["git", "clone", "https://github.com/veeainc/lobstertrap.git", "lobstertrap"])
            if ok:
                steps.append("✓ Lobster Trap cloned successfully")
            else:
                steps.append(f"✗ Clone failed: {out[:300]}")

    # Create .env
    if ENV_FILE.exists():
        steps.append("✓ .env already exists — skipped copy")
    elif ENV_EXAMPLE.exists():
        import shutil
        shutil.copy(ENV_EXAMPLE, ENV_FILE)
        steps.append("✓ .env created from .env.example")
    else:
        ENV_FILE.write_text("GEMINI_API_KEY=\nGEMINI_MODEL=gemini-2.5-flash-lite\n")
        steps.append("✓ .env created with defaults")

    # Write API key if provided
    if gemini_key:
        _write_env_key("GEMINI_API_KEY", gemini_key)
        steps.append("✓ GEMINI_API_KEY stored in .env (value not logged)")

    # Detect Ollama
    if _cmd_exists("ollama"):
        steps.append("✓ Ollama detected — Lobster Trap can use it as backend at http://localhost:11434")
    else:
        steps.append("ℹ Ollama not found — install from ollama.ai to use local LLMs with Lobster Trap")

    steps.append("\nSetup complete. Run `sentinel_status` to verify your environment.")
    return _ok("\n".join(steps))


def _write_env_key(key: str, value: str) -> None:
    lines: list[str] = []
    found = False
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"{key}={value}")
    ENV_FILE.write_text("\n".join(lines) + "\n")


async def _tool_configure(args: dict) -> list[types.TextContent]:
    action = args.get("action", "read")

    if action == "read":
        env = _read_env()
        safe = {
            "GEMINI_API_KEY": "***set***" if env.get("GEMINI_API_KEY") else "(not set)",
            "GOOGLE_API_KEY": "***set***" if env.get("GOOGLE_API_KEY") else "(not set)",
            "GEMINI_MODEL": env.get("GEMINI_MODEL", "gemini-2.5-flash-lite"),
            "OLLAMA_ENDPOINT": env.get("OLLAMA_ENDPOINT", "(not set)"),
        }
        return _ok(json.dumps(safe, indent=2))

    # Write mode
    written = []
    if args.get("gemini_api_key"):
        _write_env_key("GEMINI_API_KEY", args["gemini_api_key"])
        written.append("GEMINI_API_KEY (value not logged)")
    if args.get("gemini_model"):
        _write_env_key("GEMINI_MODEL", args["gemini_model"])
        written.append(f"GEMINI_MODEL = {args['gemini_model']}")
    if args.get("ollama_endpoint"):
        _write_env_key("OLLAMA_ENDPOINT", args["ollama_endpoint"])
        written.append(f"OLLAMA_ENDPOINT = {args['ollama_endpoint']}")

    if not written:
        return _err("No values provided to write. Pass gemini_api_key, gemini_model, or ollama_endpoint.")
    return _ok(f"Updated .env:\n" + "\n".join(f"  ✓ {w}" for w in written))


async def _tool_run_suite() -> list[types.TextContent]:
    bash = _bash_runner()
    if bash is None:
        return _err(
            "Bash not found on this Windows system.\n"
            "Options:\n"
            "  1. Install WSL: wsl --install (then restart)\n"
            "  2. Install Git for Windows (includes Git Bash): https://git-scm.com\n"
            "  3. On Mac/Linux: bash is always available."
        )

    if not SUITE_SCRIPT.exists():
        return _err(f"Script not found: {SUITE_SCRIPT}")

    ok, out = _run([*bash, str(SUITE_SCRIPT)], cwd=PROJECT_ROOT)
    if ok:
        return _ok(f"Phase 1 governance suite completed.\n\n{out[-2000:]}")
    return _err("Phase 1 suite failed", out[-2000:])


async def _tool_run_gemini(args: dict) -> list[types.TextContent]:
    if not GEMINI_SCRIPT.exists():
        return _err(f"Script not found: {GEMINI_SCRIPT}")

    env_vars: dict[str, str] = {}
    if args.get("mock_mode"):
        env_vars["MOCK_MODE"] = "1"
    else:
        env = _read_env()
        key = env.get("GEMINI_API_KEY") or env.get("GOOGLE_API_KEY", "")
        if key:
            env_vars["GEMINI_API_KEY"] = key

    ok, out = _run([sys.executable, str(GEMINI_SCRIPT)], env=env_vars)
    mode = "mock" if args.get("mock_mode") or not env_vars.get("GEMINI_API_KEY") else "real API"
    if ok:
        return _ok(f"Phase 2 Gemini validation completed (mode: {mode}).\n\n{out[-2000:]}")
    return _err(f"Phase 2 failed (mode: {mode})", out[-2000:])


async def _tool_build_dataset() -> list[types.TextContent]:
    if not BUILD_SCRIPT.exists():
        return _err(f"Script not found: {BUILD_SCRIPT}")

    ok, out = _run([sys.executable, str(BUILD_SCRIPT)])
    if ok:
        size = SCENARIOS_FILE.stat().st_size if SCENARIOS_FILE.exists() else 0
        return _ok(f"Dataset built successfully.\nscenarios.json: {size} bytes\n\n{out[-1000:]}")
    return _err("Dataset build failed", out[-2000:])


async def _tool_serve() -> list[types.TextContent]:
    if not SCENARIOS_FILE.exists():
        return _err("scenarios.json not found. Run sentinel_build_dataset first.")

    cmd = [sys.executable, "-m", "http.server", "8787"]
    try:
        subprocess.Popen(cmd, cwd=str(WRAPPER_DIR), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return _ok(
            "SENTINEL web UI started in background.\n"
            "Open: http://localhost:8787/public/index.html\n\n"
            "To stop: kill the Python http.server process in your terminal."
        )
    except Exception as e:
        return _err(f"Could not start server: {e}")


async def _tool_inspect(args: dict) -> list[types.TextContent]:
    if not SCENARIOS_FILE.exists():
        return _err("scenarios.json not found. Run sentinel_build_dataset first.")

    data = json.loads(SCENARIOS_FILE.read_text())
    filter_name = args.get("scenario_name", "").strip()

    if filter_name:
        if isinstance(data, list):
            matches = [s for s in data if s.get("scenario_name") == filter_name]
        elif isinstance(data, dict):
            matches = [data.get(filter_name, {})]
        else:
            matches = []
        if not matches:
            return _err(f"Scenario '{filter_name}' not found.")
        return _ok(json.dumps(matches, indent=2))

    return _ok(json.dumps(data, indent=2))


async def _tool_pipeline(args: dict) -> list[types.TextContent]:
    results = ["## SENTINEL Pipeline\n"]
    skip_suite = args.get("skip_suite", False)
    mock_gemini = args.get("mock_gemini", False)
    serve = args.get("serve", True)

    # Phase 1
    if skip_suite:
        results.append("Phase 1: skipped (using existing artifacts)")
    else:
        results.append("Phase 1: running governance suite...")
        r = await _tool_run_suite()
        data = json.loads(r[0].text)
        results.append("  ✓ Done" if data["success"] else f"  ✗ Failed: {data['error']}")
        if not data["success"]:
            results.append("\nPipeline stopped at Phase 1.")
            return _ok("\n".join(results))

    # Phase 2
    results.append("\nPhase 2: running Gemini validation...")
    r = await _tool_run_gemini({"mock_mode": mock_gemini})
    data = json.loads(r[0].text)
    results.append("  ✓ Done" if data["success"] else f"  ✗ Failed: {data['error']}")
    if not data["success"]:
        results.append("\nPipeline stopped at Phase 2.")
        return _ok("\n".join(results))

    # Build dataset
    results.append("\nBuilding dataset...")
    r = await _tool_build_dataset()
    data = json.loads(r[0].text)
    results.append("  ✓ Done" if data["success"] else f"  ✗ Failed: {data['error']}")
    if not data["success"]:
        return _ok("\n".join(results))

    # Serve
    if serve:
        results.append("\nStarting web UI...")
        r = await _tool_serve()
        data = json.loads(r[0].text)
        results.append("  ✓ http://localhost:8787/public/index.html" if data["success"] else f"  ✗ {data['error']}")

    results.append("\n✓ Pipeline complete.")
    return _ok("\n".join(results))


async def _tool_deploy(args: dict) -> list[types.TextContent]:
    steps = ["## GitHub Pages Deploy\n"]

    if not SCENARIOS_FILE.exists():
        return _err("scenarios.json not found. Run sentinel_build_dataset first.")

    # Build site directory
    import shutil as _shutil
    site = SUBMISSION_SITE
    site.mkdir(parents=True, exist_ok=True)
    (site / "data").mkdir(exist_ok=True)

    # Copy public assets
    public_src = WRAPPER_DIR / "public"
    for f in public_src.iterdir():
        _shutil.copy(f, site / f.name)
    steps.append(f"✓ Copied public assets from {public_src.name}/")

    # Copy scenarios.json
    _shutil.copy(SCENARIOS_FILE, site / "data" / "scenarios.json")
    steps.append(f"✓ Copied scenarios.json ({SCENARIOS_FILE.stat().st_size} bytes)")

    steps.append(f"\nStatic site ready at: submission/site/")
    steps.append("Contents:")
    for f in sorted(site.rglob("*")):
        if f.is_file():
            steps.append(f"  {f.relative_to(site)}")

    # Validate locally
    if args.get("validate_locally"):
        steps.append("\nStarting local validation server at http://localhost:8899 ...")
        try:
            subprocess.Popen(
                [sys.executable, "-m", "http.server", "8899"],
                cwd=str(site),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            steps.append("✓ Open http://localhost:8899/index.html to validate")
        except Exception as e:
            steps.append(f"✗ Could not start validation server: {e}")

    steps.append(
        "\nNext steps:\n"
        "  git add submission/site/\n"
        "  git commit -m 'chore: build GitHub Pages payload'\n"
        "  git push origin gh-pages  (or configure Pages to use /docs or main/submission/site)"
    )
    return _ok("\n".join(steps))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
