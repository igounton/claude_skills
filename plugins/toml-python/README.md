# TOML Python

Helps Claude work with TOML configuration files in Python projects without destroying your comments and formatting.

## Why Install This?

When you ask Claude to modify configuration files like pyproject.toml or config.toml, you want your carefully-written comments and formatting to survive. Without this plugin, Claude might:

- Strip all comments when updating a config value
- Reformat the entire file, creating noisy git diffs
- Use the wrong library for reading vs writing TOML
- Forget to handle file corruption during updates

This plugin ensures Claude treats your config files with care.

## What Changes

With this plugin installed, Claude will:

- Preserve all comments and formatting when modifying TOML files
- Use tomlkit (comment-preserving) instead of standard parsers
- Implement atomic file updates to prevent corruption if something fails
- Handle missing keys and parse errors gracefully
- Follow XDG Base Directory conventions for config file locations
- Choose the right library (tomlkit vs tomllib) based on whether you need read/write vs read-only

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install toml-python@jamie-bitflight-skills
```

## Usage

Just install it - it works automatically when you work with TOML files. You'll notice the difference when you ask Claude to:

- "Update the version in pyproject.toml to 2.0.0"
- "Add a new database section to config.toml"
- "Change the port number but keep all the comments"
- "Create a config file manager for my Python app"

## Example

**Without this plugin**: You have a config.toml with detailed comments explaining each setting. You ask Claude to "change the database port to 5433". Claude reads the file, parses it with the standard library, updates the port, and writes it back. Your comments are gone. The entire file is reformatted. Git shows 50 lines changed when only 1 value changed.

**With this plugin**: Same request. Claude uses tomlkit to read the file, updates just the port value, and writes it back. All your comments remain. The formatting is unchanged. Git shows exactly 1 line changed. If the write fails mid-way, your original file is safe because Claude used atomic updates.

## Requirements

- Claude Code v2.0+
- Python 3.8+ for projects using tomlkit

## What You Get

This plugin teaches Claude about:

- **tomlkit library**: Comment-preserving TOML parser for Python
- **Common patterns**: Load-or-create, atomic updates, validation
- **Error handling**: Parse errors, missing keys, file not found
- **Type mappings**: How TOML types map to Python types
- **Best practices**: When to use tomlkit vs tomllib (stdlib)
- **XDG compliance**: Standard config file locations

## Related Plugins

- **xdg-base-directory**: For proper config file locations
- **python3-development**: For Python development patterns
- **uv**: For managing the tomlkit dependency
