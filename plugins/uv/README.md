# uv

Modern Python project management with uv - the extremely fast Python package manager.

## Why Install This?

When working on Python projects, you might encounter:
- Slow dependency installation (pip taking minutes)
- Unclear project setup (where do requirements go?)
- Scripts that break when dependencies change
- Confusion between pip, pipx, poetry, virtualenv
- Different Python versions across team members
- CI builds that don't match local development

This plugin helps Claude guide you toward modern Python project practices using uv.

## What Changes

With this plugin installed, Claude will:
- Recommend uv for new Python projects instead of traditional pip workflows
- Set up projects with proper structure (pyproject.toml, lockfiles, virtual environments)
- Create portable single-file scripts with built-in dependency management
- Configure CI/CD pipelines that are fast and reproducible
- Help migrate existing projects from pip, requirements.txt, or poetry
- Troubleshoot Python dependency and version issues more effectively

## Installation

```bash
/plugin install uv
```

## What You'll Experience

### Better Project Setup

**Before**: You ask Claude to set up a Python project

```
Creates requirements.txt
Tells you to run pip install -r requirements.txt
No version pinning, no lockfile
```

**After**: Same request with this plugin

```
Creates pyproject.toml with dependencies
Creates uv.lock for reproducibility
Sets up virtual environment automatically
Includes proper Python version management
```

### Portable Scripts

**Before**: Creating a script that needs packages

```
Script has no dependency information
You manually pip install packages
Breaks when someone else tries to run it
```

**After**: Same task with this plugin

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "rich"]
# ///

import requests
from rich import print
# Script includes its own dependencies - just run it
```

### Faster Workflows

**Before**: Installing dependencies for a project

```
pip install takes 2-3 minutes
No caching between projects
Manual virtual environment management
```

**After**: With uv-based workflow

```
uv sync completes in 5-10 seconds
Intelligent caching across projects
Automatic environment handling
```

## When This Helps

This plugin is especially useful when you:
- Start new Python projects
- Set up dependency management
- Create standalone Python scripts
- Configure CI/CD for Python projects
- Migrate from pip, poetry, or conda
- Need to manage multiple Python versions
- Want faster and more reliable builds

## What is uv?

uv is Astral's Rust-based Python package manager that replaces pip, pipx, poetry, pyenv, and virtualenv with a single tool that's 10-100x faster. Think of it as a modern alternative to pip that handles project management, virtual environments, and Python versions all in one place.

## Requirements

- Claude Code v2.0+
- uv installed (Claude will guide you through installation if needed)
