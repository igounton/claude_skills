# Holistic Linting

Makes Claude automatically check and fix code quality issues before completing tasks.

## Why Install This?

When you ask Claude to write or modify code, Claude sometimes:
- Says "all done!" but leaves linting errors in the code
- Adds `# type: ignore` or `# noqa` comments to silence errors instead of fixing them
- Forgets to run formatters and linters before finishing
- Doesn't know which linters your project uses

This plugin makes Claude treat code quality checks as a required part of every task.

## What Changes

With this plugin installed, Claude will:
- Automatically format and lint modified files before saying a task is complete
- Investigate the root cause of linting errors instead of just suppressing them
- Read your project's linting configuration from `CLAUDE.md` to know which tools to use
- Fix type errors by understanding what the types should be, not just adding ignore comments
- Verify that fixes actually work by re-running linters

## Installation

```bash
/plugin install holistic-linting
```

## Usage

### Automatic Behavior

Just install it - Claude will automatically check code quality when finishing tasks involving code changes.

### Manual Commands

**Check specific files**:
```bash
/lint src/auth.py
/lint src/*.py
```

**Auto-detect your project's linters**:
```bash
/lint init
```

This scans your project (pyproject.toml, .pre-commit-config.yaml, package.json, etc.) and documents which linters you use in `CLAUDE.md`.

## Example

**Without this plugin**:
```
You: "Add authentication to the API"
Claude: [writes code]
Claude: "Done! I've added authentication middleware."
You: [runs ruff check]
You: "There are 5 linting errors..."
```

**With this plugin**:
```
You: "Add authentication to the API"
Claude: [writes code]
Claude: [automatically runs ruff format, ruff check, mypy]
Claude: [finds 5 errors, investigates root causes, fixes them properly]
Claude: [verifies fixes with linters]
Claude: "Done! I've added authentication middleware. All linting checks pass."
```

## What's Included

- **Automatic quality checks** - Claude formats and lints code before finishing
- **Root cause analysis** - Investigates why linting errors happen
- **Manual `/lint` command** - Check code quality on demand
- **Project linter detection** - `/lint init` auto-discovers your linters
- **Rules documentation** - Complete reference for ruff, mypy, and bandit rules

## Requirements

- Claude Code v2.0+
- Python projects: ruff, mypy, pyright, or similar linters
- Other languages: eslint, prettier, shellcheck, etc.

## Supported Linters

- **Python**: ruff, mypy, pyright, basedpyright, bandit
- **JavaScript/TypeScript**: eslint, prettier
- **Shell**: shellcheck, shfmt
- **Markdown**: markdownlint
- **Pre-commit hooks**: pre-commit, prek
