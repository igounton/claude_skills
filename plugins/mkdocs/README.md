# MkDocs

Helps Claude work with MkDocs documentation sites accurately and efficiently.

## Why Install This?

When you ask Claude to create or modify MkDocs documentation, Claude sometimes:

- Guesses at command-line options or gets them wrong
- Uses outdated configuration syntax
- Suggests Material theme features that don't exist or configures them incorrectly
- Misremembers plugin settings or uses incompatible configurations

This plugin gives Claude complete, accurate reference material for MkDocs.

## What Changes

With this plugin installed, Claude will:

- Use exact command syntax with correct flags and options
- Write mkdocs.yml configurations that work the first time
- Configure Material theme features correctly (navigation, search, social cards, etc.)
- Set up popular plugins (mkdocstrings, gen-files, mermaid2) with valid settings
- Suggest deployment workflows that actually work

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install mkdocs@jamie-bitflight-skills
```

## Usage

Just install it - works automatically. You'll notice the difference when you ask Claude to:

- "Create a new MkDocs site with Material theme"
- "Add social cards to my documentation"
- "Set up mkdocstrings for Python API docs"
- "Configure navigation tabs and sections"
- "Deploy to GitHub Pages"

## Example

**Without this plugin**: You say "add a dark mode toggle to my MkDocs site". Claude suggests configuration that's missing required fields, uses wrong syntax, or doesn't match Material theme's actual options.

**With this plugin**: Same request. Claude writes:

```yaml
theme:
  palette:
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
```

Works immediately, no trial and error.

## What's Included

- Complete CLI command reference (build, serve, gh-deploy, etc.)
- Full mkdocs.yml configuration options with valid values
- Material theme features and settings
- Popular plugin configurations (mkdocstrings, mermaid2, gen-files, etc.)
- Real-world deployment patterns for GitHub Actions and GitLab CI

## Requirements

- Claude Code v2.0+
