# PyPI README Creator

Helps Claude write professional README files for Python packages that render correctly on PyPI.

## Why Install This?

When you publish a Python package to PyPI, you've probably encountered:
- Your README looks perfect on GitHub but broken on PyPI
- Code examples don't render with syntax highlighting
- Sphinx-specific markup causes validation errors
- Unsure whether to use README.md or README.rst
- `twine check` reports rendering errors you don't understand

This plugin teaches Claude PyPI's specific README requirements and constraints.

## What Changes

With this plugin installed, Claude will:
- Choose the right format (Markdown vs reStructuredText) based on your project
- Write READMEs that render correctly on PyPI, GitHub, GitLab, and BitBucket
- Avoid PyPI's restrictions (like Sphinx extensions in RST files)
- Include proper `pyproject.toml` configuration for README metadata
- Add validation steps with `twine check` before you publish
- Provide complete templates with all the expected sections
- Set up `sphinx-readme` integration if your project uses Sphinx

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install pypi-readme-creator@jamie-bitflight-skills
```

## Usage

Just install it. Claude will apply this knowledge when you ask for help with Python package documentation.

**Examples of requests:**
- "Create a README.md for this Python package"
- "Why is my README broken on PyPI?"
- "Should I use Markdown or reStructuredText for my README?"
- "Set up sphinx-readme to generate my PyPI README"
- "Add the proper pyproject.toml configuration for my README"

## Example

**Without this plugin**: You ask Claude to create a README. It looks fine locally, but after publishing to PyPI, your code examples don't have syntax highlighting, Sphinx roles like `:py:func:` show as errors, and the formatting is broken.

**With this plugin**: Same request, but Claude creates a PyPI-compliant README with proper code block syntax, includes `twine check` validation in the workflow, configures `pyproject.toml` correctly, and if you're using Sphinx, sets up `sphinx-readme` to auto-generate a compatible README from your docs.

## What's Included

- **Format selection guidance**: When to use Markdown vs reStructuredText
- **Professional templates**: Both Markdown and RST with all recommended sections
- **PyPI constraints**: What markup works on PyPI vs what breaks
- **Validation workflow**: How to test README rendering before publishing
- **Sphinx integration**: Using `sphinx-readme` to generate PyPI-compatible READMEs
- **Configuration**: Proper `pyproject.toml` setup for different formats

## Requirements

- Claude Code v2.0+
