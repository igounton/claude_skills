# Python Development

Teaches Claude modern Python 3.11+ patterns and your preferred workflows.

## Why Install This?

When you ask Claude to write Python code, Claude sometimes:
- Uses outdated syntax (old typing patterns, Python 3.8 style)
- Picks random libraries instead of ones that work well together
- Creates inconsistent project structures across different projects
- Immediately fixes tests to make them pass without investigating why they failed
- Doesn't follow conventions you use in your existing projects

## What Changes

With this plugin installed, Claude will:
- Write Python 3.11+ code with modern syntax (native generics, union types with `|`)
- Use proven library combinations (Typer+Rich for CLIs, specific tools you've used)
- Follow project structure patterns extracted from your actual codebases
- Investigate test failures carefully before making changes
- Apply consistent linting, formatting, and type checking workflows
- Reference 50+ modern Python libraries with usage guidance

## Installation

```bash
/plugin install python3-development
```

## Usage

Just install it - Claude uses it automatically when working with Python code. You'll notice:
- Cleaner, more modern Python code
- Consistent project structures
- Better library choices
- More thoughtful handling of test failures
- Comprehensive type hints and validation

## Example

**Without this plugin**: You say "build a CLI tool to process CSV files". Claude creates it with argparse, prints plain text, uses `List[str]` syntax, puts code in `src/`, and when a test fails, immediately changes the test to match the implementation.

**With this plugin**: Same request, but Claude uses Typer+Rich (progress bars, formatted tables), writes `list[str]` with native generics, puts code in `packages/csv_tool/`, includes comprehensive type hints, and when a test fails, investigates whether the test caught a real bug before deciding what to fix.

## Requirements

- Claude Code v2.0+
