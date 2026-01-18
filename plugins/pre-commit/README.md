# Pre-commit

Helps Claude set up and configure automated code quality checks that run when you commit code.

## Why Install This?

When you ask Claude to "set up a formatter" or "add linting to my project," Claude sometimes:
- Suggests running formatters manually instead of automating them
- Confuses different types of git hooks
- Misconfigures commit message validation
- Doesn't know about the difference between checking vs rewriting commit messages

This plugin teaches Claude how to properly set up git hooks using the pre-commit framework.

## What Changes

With this plugin installed, Claude will:
- Correctly configure .pre-commit-config.yaml files
- Set up formatters like black or prettier to run automatically on commit
- Know when to use prepare-commit-msg vs commit-msg hooks
- Install hooks with the right settings
- Understand both pre-commit and prek (the faster Rust alternative)
- Run hooks on just your changed files, not the entire codebase

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install pre-commit@jamie-bitflight-skills
```

## Usage

Just install it - it works automatically. Claude will use this knowledge when you ask for tasks like:
- "Set up black formatting on commit"
- "Add a hook to check for trailing whitespace"
- "Configure commit message validation"
- "Set up linting to run before I push"
- "Add prettier to run automatically"

## Example

**Without this plugin**: You say "set up black formatter." Claude suggests running `black .` manually or creates a script you have to remember to run.

**With this plugin**: Same request, but Claude:
1. Creates .pre-commit-config.yaml with correct black configuration
2. Installs the pre-commit tool if needed
3. Runs `pre-commit install` to activate the hooks
4. Explains that black will now run automatically on changed files when you commit
5. Shows you how to run it manually if needed

## What It Covers

This plugin helps Claude with:
- Setting up code formatters (black, prettier, rustfmt)
- Configuring linters to run on commit
- Commit message validation and rewriting
- Different hook stages (pre-commit, pre-push, prepare-commit-msg)
- Testing hooks before using them
- Troubleshooting hook configuration issues

## Requirements

- Claude Code v2.0+
