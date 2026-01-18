# Skill Reference

Complete reference for the pypi-readme-creator skill included in this plugin.

## Skill: pypi-readme-creator

**Location**: `skills/pypi-readme-creator/SKILL.md`

**Description**: When creating a README for a Python package. When preparing a package for PyPI publication. When README renders incorrectly on PyPI. When choosing between README.md and README.rst. When running twine check and seeing rendering errors. When configuring readme field in pyproject.toml.

**User Invocable**: Yes (default)

**Allowed Tools**: All tools (inherits from context)

**Model**: Default (inherits from context)

**Context**: Inline (default)

### When to Use

The skill activates automatically when Claude detects README-related tasks for Python packages. You can also invoke it explicitly:

```
@pypi-readme-creator
```

Use this skill when you need to:

- Create new README files (Markdown or reStructuredText)
- Convert between README formats
- Fix PyPI rendering issues
- Validate README markup
- Configure pyproject.toml for README inclusion
- Set up Sphinx integration with sphinx-readme
- Troubleshoot common README problems
- Generate PyPI-compliant documentation

### Core Capabilities

**1. Format Support and Selection**

The skill understands three README formats:

| Format | PyPI Content Type | Best For |
|--------|------------------|----------|
| Plain Text | `text/plain` | Minimal documentation |
| Markdown | `text/markdown` | Modern projects, GitHub-first |
| reStructuredText | `text/x-rst` | Sphinx integration, advanced tables |

Provides decision framework for choosing between formats based on:
- Existing documentation infrastructure
- Team preferences and skills
- Platform compatibility requirements
- Technical complexity needs

**2. Content Guidelines**

Follows documentation best practices from multiple sources:
- Official Python Packaging Guide
- documentation-expert skill principles
- gitlab-docs-expert skill guidelines
- Anthropic prompt engineering patterns

Includes structured guidance for:
- Essential sections (project identity, installation, quick start, features, usage)
- Writing style principles (clarity, user focus, accuracy, consistency)
- Visual elements (badges, tables, code examples)
- Quality standards checklist

**3. Format-Specific Syntax**

Provides working examples for:

**Markdown (GFM)**:
- Code blocks with syntax highlighting
- Badges and shields
- Tables
- Alerts (GitHub/GitLab)
- Links

**reStructuredText**:
- code-block directives
- Image directives for badges
- Table syntax (grid and simple)
- Admonitions (note, warning, tip)
- Links and references
- Section header hierarchy

**4. Sphinx Integration**

Guides setup of sphinx-readme extension:
- Installation configuration
- conf.py settings
- Build workflow
- Conversion limitations
- Validation process

Explains how to:
- Convert Sphinx roles to PyPI-compatible equivalents
- Handle cross-references
- Maintain single source of truth
- Automate README generation

**5. PyPI Integration**

Complete guidance for:

**pyproject.toml Configuration**:
- Simple readme field: `readme = "README.md"`
- Explicit content type: `readme = {file = "README.md", content-type = "text/markdown"}`
- Markdown variants: GFM vs CommonMark
- Project metadata and URLs

**Build and Validation**:
- Building with uv: `uv build`
- Validating with twine: `uv run --with twine twine check dist/*`
- Common validation errors and solutions
- Publishing workflow

**6. Validation Tools and Workflow**

Pre-publication checklist:
1. Build package
2. Validate README rendering
3. Test installation locally
4. Upload to TestPyPI
5. Verify rendering on TestPyPI
6. Test installation from TestPyPI
7. Publish to production PyPI

Local testing tools:
- `grip` for Markdown preview
- `rst2html.py` for RST validation
- `twine check` for PyPI validation

**7. Troubleshooting**

Common issues and solutions:

**reStructuredText**:
- Sphinx roles not rendering → Convert to plain text or RST links
- Code block indentation → Fix blank lines and indentation
- Link definition spacing → Add blank lines

**Markdown**:
- Missing language specifiers → Add language after opening fence
- Heading hierarchy → Don't skip levels
- Cross-platform rendering → Test on TestPyPI

**General**:
- Line ending issues → Convert to Unix LF
- Content-type mismatch → Verify pyproject.toml matches file
- Platform differences → Test on all targets

### Reference Files

The skill includes three reference templates in `skills/pypi-readme-creator/references/`:

#### markdown-template.md

Modern Markdown README template featuring:
- Project header with badges (PyPI version, Python versions, license)
- Clear feature list with bullet points
- Installation instructions for pip and uv
- Quick start code example
- Usage examples with output
- Documentation links
- Contributing guidelines
- License information

**Use when**: Starting a new Python package with Markdown documentation

**Customize**: Replace placeholders for package name, description, author, repository URLs

#### rst-template.rst

reStructuredText README template featuring:
- RST-style section headers
- Image directives for badges
- code-block directives with Python syntax
- Admonitions (note, warning)
- External links with reference style
- Grid and simple table examples
- Field lists for metadata

**Use when**: Starting a new Python package with RST documentation or Sphinx integration

**Customize**: Update package metadata, links, code examples

#### sphinx-readme-example.md

Documentation for sphinx-readme extension integration:
- Extension installation steps
- Configuration examples for docs/conf.py
- Usage instructions
- Limitations and caveats
- Complete workflow from Sphinx to PyPI

**Use when**: Maintaining Sphinx documentation and need automated README generation

**Follow**: Step-by-step guide for initial setup and ongoing maintenance

### Related Skills

This skill references and complements:

- **uv** - For Python project and package management (`uv build`, `uv add`, `uv run`)
- **hatchling** - For build backend configuration in pyproject.toml
- **gitlab-skill** - For GitLab Flavored Markdown features (mentions, alerts)

### Skill Metadata

**Frontmatter**:

```yaml
---
name: pypi-readme-creator
description: When creating a README for a Python package. When preparing a package for PyPI publication. When README renders incorrectly on PyPI. When choosing between README.md and README.rst. When running twine check and seeing rendering errors. When configuring readme field in pyproject.toml.
---
```

**Hooks**: None configured

**Context**: Inline (runs in main conversation context)

**Progressive Disclosure**: References three template files that Claude loads on demand

### Quality Standards

The skill guides users to ensure:

- [ ] One-line description clearly states project purpose
- [ ] Installation instructions tested and accurate
- [ ] Code examples run successfully with current version
- [ ] All links valid and point to correct destinations
- [ ] Badges display correctly and are current
- [ ] Markup validated with `twine check`
- [ ] Tested rendering on target platforms (PyPI, GitHub/GitLab)
- [ ] Spelling and grammar checked
- [ ] Heading hierarchy is consistent (no skipped levels)
- [ ] License clearly stated
- [ ] Python version requirements specified
- [ ] Content type correctly set in pyproject.toml

### Key Principles

The skill follows these design principles:

1. **User-First Design** - Answer "What does this do for me?" early
2. **Show, Don't Tell** - Working code examples over abstract descriptions
3. **Platform Compatibility** - Test rendering on all target platforms
4. **Format Constraints** - Respect PyPI limitations (no Sphinx extensions in RST)
5. **Validation Before Publishing** - Always run `twine check` before uploading
6. **Single Source of Truth** - Use `sphinx-readme` for Sphinx-based projects
7. **Accessibility** - Write for diverse audiences (beginners to experts)
8. **Maintenance** - Update README with each release

### Sources and References

The skill is built on official documentation and best practices:

**Official Documentation**:
- [Making a PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/) - Python Packaging Guide
- [PyPI README Renderer](https://github.com/pypa/readme_renderer) - PyPI's rendering engine
- [sphinx-readme Documentation](https://sphinx-readme.readthedocs.io/) - Sphinx to PyPI converter
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) - Sphinx RST guide
- [GitHub Flavored Markdown](https://github.github.com/gfm/) - GFM specification
- [CommonMark](https://commonmark.org/) - CommonMark specification

**Tool Documentation**:
- [Twine Documentation](https://twine.readthedocs.io/) - Package upload tool
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package manager
- [Hatchling Documentation](https://hatchling.pypa.io/) - Modern build backend

**Related Resources**:
- [readme-renderer on PyPI](https://pypi.org/project/readme-renderer/) - Test README rendering
- [Grip](https://github.com/joeyespo/grip) - Preview Markdown as GitHub renders
- [Pandoc](https://pandoc.org/) - Universal document converter

### Usage Patterns

**Pattern 1: Generate from scratch**

```
@pypi-readme-creator

Create a README.md for package "example-pkg" with:
- Installation via pip
- Quick start code example
- Features list
- Link to documentation
```

**Pattern 2: Convert formats**

```
@pypi-readme-creator

Convert README.md to README.rst format for PyPI compliance.
Ensure no Sphinx-specific roles are used.
```

**Pattern 3: Fix validation errors**

```
@pypi-readme-creator

Fix twine check errors in README.rst:
- "Unknown interpreted text role py:func"
- "Unexpected indentation"
```

**Pattern 4: Setup automation**

```
@pypi-readme-creator

Configure sphinx-readme to auto-generate README.rst from docs/index.rst
```

**Pattern 5: Pre-publish validation**

```
@pypi-readme-creator

Walk me through validating README before PyPI upload,
including TestPyPI testing.
```

---

For complete usage examples, see [examples.md](./examples.md).

For installation and setup, see [README.md](../README.md).
