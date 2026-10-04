---
name: uv
description: Guidelines for managing Python dependencies and running scripts using uv (Astral). Use when the user asks to install a Python package, run a Python script, or manage Python environments.
---

# uv (Python Package Manager)

`uv` is an extremely fast Python package manager and resolver written in Rust. It serves as a drop-in replacement for `pip`, `pip-tools`, `virtualenv`, and `pipx`.

## Key Commands

### 1. Running Scripts (`uv run`)
Run a script with its dependencies declared inline (PEP 723) or dynamically:
```bash
uv run script.py
uv run --with requests script.py
```

### 2. Managing Environments (`uv venv`)
Create and manage virtual environments:
```bash
uv venv
# On Windows (PowerShell/CMD)
.venv\Scripts\activate
# On Linux/macOS
source .venv/bin/activate
```

### 3. Package Operations (`uv pip`)
Install or resolve packages within the active virtual environment:
```bash
uv pip install requests
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

### 4. Tool Execution (`uvx` or `uv tool`)
Run a Python CLI tool in an isolated environment (like `pipx`):
```bash
uvx ruff check .
```

## Best Practices
- Always prefer `uv` over standard `pip` for Python operations on this machine, as it is significantly faster (often 10-100x).
- Use `uv run` for executing self-contained scripts to automatically manage temporary environments.
- Verify `uv --version` on startup if you require Python package execution.
