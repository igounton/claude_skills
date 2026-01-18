# PyPI README Creator

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Generate professional, PyPI-compliant README files in Markdown or reStructuredText that render correctly on PyPI, GitHub, GitLab, and BitBucket.

## Features

- **Multi-Format Support** - Generate README files in Markdown (GFM/CommonMark) or reStructuredText
- **PyPI Compliance** - Ensures README renders correctly on PyPI without Sphinx extensions
- **Sphinx Integration** - Leverages sphinx-readme for projects with Sphinx documentation
- **Validation Workflow** - Built-in guidance for testing with twine and local rendering
- **Template Library** - Ready-to-use templates for both Markdown and RST formats
- **Cross-Platform Compatible** - Ensures rendering works on PyPI, GitHub, GitLab, and BitBucket
- **Best Practice Guidance** - Follows documentation-expert and gitlab-docs-expert principles

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- Python 3.11+ (for validation tools)

### Install Plugin

```bash
# Method 1: Manual installation (current method)
git clone <repository-url> ~/.claude/plugins/pypi-readme-creator
cc plugin reload

# Method 2: If available via marketplace
cc plugin install pypi-readme-creator
```

## Quick Start

Activate the skill when working with Python package documentation:

```
@pypi-readme-creator

Create a README.md for my Python package "example-package" that:
- Uses Markdown format
- Includes installation via pip and uv
- Shows a quick start example
- Is PyPI-compliant
```

Claude will generate a complete README following PyPI best practices, validate the format, and provide guidance for testing before publication.

## When to Use

Use this plugin when:

- Creating README files for Python packages intended for PyPI publication
- Converting between Markdown and reStructuredText formats
- Validating README markup before publishing to PyPI
- Setting up `pyproject.toml` metadata for README inclusion
- Generating README.rst files from Sphinx documentation
- Ensuring README compatibility across multiple platforms
- Troubleshooting README rendering issues on PyPI
- Creating documentation that balances technical accuracy with user accessibility

## Capabilities

### Supported README Formats

| Format | Content Type | Use Case |
|--------|--------------|----------|
| **Markdown** | `text/markdown` (GFM/CommonMark) | New projects, GitHub/GitLab-first workflows |
| **reStructuredText** | `text/x-rst` | Sphinx-based projects, advanced tables |
| **Plain Text** | `text/plain` | Minimal documentation needs |

### Core Features

**Format Selection Strategy**
- Analyzes project structure and documentation needs
- Recommends format based on existing infrastructure
- Provides migration paths between formats

**Content Guidelines**
- Essential sections: Project identity, installation, quick start, features, usage
- Writing style principles: Clarity, user focus, accuracy, consistency
- Quality standards checklist

**PyPI Integration**
- pyproject.toml configuration for all formats
- Build and publishing workflows using uv and twine
- Validation commands and common error solutions

**Sphinx README Extension**
- Configure sphinx-readme for automatic generation
- Convert Sphinx-specific roles to PyPI-compatible equivalents
- Maintain single source of truth in documentation

**Validation Tools**
- Pre-publish checklist with step-by-step commands
- Local rendering tests for both Markdown and RST
- Common issues and solutions reference

### Reference Templates

The plugin includes three production-ready templates:

| Template | Location | Description |
|----------|----------|-------------|
| Markdown | `references/markdown-template.md` | Modern GFM template with badges |
| reStructuredText | `references/rst-template.rst` | RST template with docutils directives |
| Sphinx Integration | `references/sphinx-readme-example.md` | Using sphinx-readme extension |

## Usage

### Basic README Generation

```
@pypi-readme-creator

Generate a README.md for my package "data-processor" with:
- Installation via pip
- Quick start with a code example
- Features list highlighting async support
- Links to documentation
```

### Format Conversion

```
@pypi-readme-creator

Convert my existing README.md to README.rst format that's PyPI-compliant.
The Markdown file is at ./README.md
```

### Validation Workflow

```
@pypi-readme-creator

Guide me through validating my README.rst before publishing to PyPI.
I want to test locally and on TestPyPI first.
```

### Sphinx Integration

```
@pypi-readme-creator

Help me set up sphinx-readme to generate README.rst from my Sphinx docs.
My docs are in docs/ with index.rst as the entry point.
```

## Configuration

### pyproject.toml Setup

For Markdown README:

```toml
[project]
name = "your-package"
version = "1.0.0"
readme = "README.md"
```

For reStructuredText README:

```toml
[project]
readme = "README.rst"
```

Explicit content type (optional):

```toml
[project]
readme = {file = "README.md", content-type = "text/markdown; variant=GFM"}
```

### Validation Commands

```bash
# Build package
uv build

# Validate README rendering
uv run --with twine twine check dist/*

# Preview Markdown locally
uvx grip README.md

# Validate RST locally
uv run --with docutils rst2html.py README.rst /dev/null
```

## Examples

### Example 1: Creating a New Package README

**Scenario**: You've built a new Python package and need a professional README for PyPI publication.

```
@pypi-readme-creator

Create a README.md for my package "api-client" that:
- Installs via: pip install api-client
- Provides a quick start showing basic API connection
- Lists features: async support, type hints, retry logic
- Links to https://api-client.readthedocs.io for full docs
- License: MIT
```

**Result**: Complete README.md with:
- Project header with badges
- Installation instructions for pip and uv
- Quick start code example with expected output
- Features list with bullet points
- Documentation and repository links
- License information

### Example 2: Fixing PyPI Rendering Issues

**Scenario**: Your README renders fine on GitHub but shows errors on PyPI.

```
@pypi-readme-creator

My README.rst fails twine check with "Unknown interpreted text role py:func".
Help me fix Sphinx-specific roles to be PyPI-compliant.
```

**Result**:
- Identifies Sphinx roles (`:py:func:`, `:ref:`, etc.)
- Converts to PyPI-compatible alternatives
- Tests with `twine check` to verify fixes
- Provides validation commands

### Example 3: Setting Up Sphinx README Integration

**Scenario**: You maintain Sphinx documentation and want to generate README automatically.

```
@pypi-readme-creator

Set up sphinx-readme to generate README.rst from my docs/index.rst file.
I want to maintain single source of truth in Sphinx docs.
```

**Result**:
- Installs sphinx-readme extension
- Configures docs/conf.py with proper settings
- Sets up build workflow
- Provides commands to generate and validate README
- Documents limitations and review process

## Troubleshooting

### Common Issues

**Issue: README not showing on PyPI after upload**
- **Cause**: Incorrect content-type in pyproject.toml
- **Solution**: Verify `readme` field matches file extension (`.md` → `text/markdown`, `.rst` → `text/x-rst`)

**Issue: "Unknown interpreted text role" errors in RST**
- **Cause**: Sphinx-specific roles in README
- **Solution**: Remove `:py:func:`, `:ref:`, `:doc:` roles; use plain text or standard RST links

**Issue: Markdown renders differently on PyPI vs GitHub**
- **Cause**: PyPI uses different Markdown renderer
- **Solution**: Test on TestPyPI before production; avoid GitHub-specific extensions

**Issue: Code blocks not showing properly**
- **Cause**: Missing language specifier or incorrect indentation
- **Solution**: Add language after opening fence (```python) or fix RST code-block indentation

### Validation Steps

If README rendering fails:

1. Run `uv run --with twine twine check dist/*` to identify errors
2. For RST: `uv run --with docutils rst2html.py README.rst /dev/null`
3. For Markdown: `uvx grip README.md` to preview locally
4. Test on TestPyPI before production upload
5. Check pyproject.toml `readme` field matches actual file

## Contributing

This plugin is part of the Claude Skills repository. To contribute improvements:

1. Test changes with various Python packages
2. Verify templates render correctly on PyPI
3. Update reference files with new best practices
4. Submit issues or pull requests to the repository

## License

This plugin is provided as part of the Claude Skills project. See the repository LICENSE file for details.

## Credits

Created following official Python Packaging Guide recommendations and Anthropic prompt engineering best practices.

### References

- [Making a PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/) - Official Python Packaging Guide
- [PyPI README Renderer](https://github.com/pypa/readme_renderer) - PyPI's rendering engine
- [sphinx-readme Documentation](https://sphinx-readme.readthedocs.io/) - Sphinx to PyPI README converter
- [GitHub Flavored Markdown](https://github.github.com/gfm/) - GFM specification
