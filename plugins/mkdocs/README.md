# MkDocs Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Comprehensive MkDocs documentation plugin for Claude Code, providing complete reference materials for creating and managing professional documentation sites with MkDocs and Material theme.

## Features

- **Complete CLI Reference** - All mkdocs commands with parameters, options, and usage examples
- **Configuration Guide** - Comprehensive mkdocs.yml settings documentation with valid values
- **Material Theme Reference** - Full Material for MkDocs theme configuration including colors, navigation, search, and advanced features
- **Plugin Ecosystem** - Detailed documentation for essential plugins (mkdocstrings, gen-files, literate-nav, mermaid2, and more)
- **Real-World Examples** - Active GitHub/GitLab repositories and proven CI/CD deployment patterns
- **Best Practices** - Production-tested patterns for documentation structure, SEO, and performance

## Installation

### Prerequisites

- Claude Code 2.1 or later
- Git repository initialized (for plugin installation)

### Install Plugin

```bash
# Using Claude Code plugin system
/plugin marketplace add Jamie-BitFlight/claude_skills
/plugin install mkdocs@claude_skills

# Or manually clone to plugins directory
git clone https://github.com/Jamie-BitFlight/claude_skills.git
cd claude_skills
python install.py
```

### Verify Installation

```bash
# Check if plugin is loaded
/plugin list

# The mkdocs skill should appear in your skills list
```

## Quick Start

### Create a New MkDocs Project

```markdown
I need to create a new MkDocs documentation site for my Python project with Material theme.
```

Claude will guide you through:
1. Running `mkdocs new` to scaffold the project
2. Configuring `mkdocs.yml` with Material theme
3. Setting up navigation structure
4. Adding markdown extensions
5. Configuring plugins for your needs

### Configure Material Theme

```markdown
Help me configure Material for MkDocs with dark mode toggle, search suggestions, and social cards.
```

Claude will provide the complete theme configuration with:
- Color palettes with light/dark mode
- Navigation features
- Search configuration
- Social cards setup
- Typography settings

### Set Up API Documentation

```markdown
I want to auto-generate API documentation from Python docstrings using mkdocstrings.
```

Claude will help you:
1. Install mkdocstrings plugin
2. Configure the plugin in mkdocs.yml
3. Create documentation structure with gen-files
4. Set up literate-nav for dynamic navigation
5. Customize docstring rendering

## Capabilities

| Reference File | Description | Use Cases |
|---------------|-------------|-----------|
| [CLI Reference](./skills/mkdocs/references/cli_reference.md) | Complete command documentation | Running builds, serving locally, GitHub Pages deployment |
| [Configuration Reference](./skills/mkdocs/references/configuration_reference.md) | All mkdocs.yml settings | Site configuration, theme setup, plugin integration |
| [Material Theme Reference](./skills/mkdocs/references/material_theme_reference.md) | Material for MkDocs configuration | Theme customization, navigation, search, social features |
| [Plugins Reference](./skills/mkdocs/references/plugins_reference.md) | Essential plugins documentation | API docs, diagrams, terminal animations, versioning |
| [Real-World Examples](./skills/mkdocs/references/real_world_examples.md) | Production implementations | CI/CD workflows, deployment patterns, active projects |

## Usage

### Skill Activation

The mkdocs skill activates automatically when:
- You mention "MkDocs" or "mkdocs.yml" in your requests
- You're working on documentation site configuration
- You need to set up Material theme
- You're configuring MkDocs plugins

Manual activation:
```markdown
@mkdocs
```

### Common Workflows

#### 1. Initial Project Setup

**Request:**
```markdown
Set up a new MkDocs project with Material theme, including:
- Modern navigation with tabs and sections
- Dark mode toggle
- Code highlighting with copy button
- Search with suggestions
- Social cards for sharing
```

**What Claude Does:**
- Creates project structure with `mkdocs new`
- Configures Material theme with requested features
- Sets up markdown extensions
- Adds recommended plugins
- Provides complete mkdocs.yml

#### 2. API Documentation Generation

**Request:**
```markdown
Configure mkdocstrings to auto-generate API docs from my Python package in src/mypackage/.
Use Google-style docstrings and show source code links.
```

**What Claude Does:**
- Installs mkdocstrings with Python handler
- Configures gen-files to scan source directory
- Sets up literate-nav for automatic navigation
- Customizes docstring rendering options
- Creates reference documentation structure

#### 3. CI/CD Deployment

**Request:**
```markdown
Create a GitHub Actions workflow to deploy my MkDocs site to GitHub Pages
when I push to main branch. Use strict mode and cache dependencies.
```

**What Claude Does:**
- Creates `.github/workflows/mkdocs.yml`
- Configures Python environment with caching
- Installs dependencies from requirements.txt
- Builds with strict mode enabled
- Deploys to GitHub Pages with proper permissions

#### 4. Theme Customization

**Request:**
```markdown
Customize Material theme colors to match my brand: primary #4051b5, accent #448aff.
Add my logo and configure social links for GitHub and Twitter.
```

**What Claude Does:**
- Updates palette configuration with custom colors
- Adds logo and favicon settings
- Configures social links in footer
- Provides custom CSS if needed
- Shows how to override theme templates

#### 5. Plugin Integration

**Request:**
```markdown
Add Mermaid diagram support, terminal animations with termynal, and git revision dates.
```

**What Claude Does:**
- Installs required plugins
- Configures each plugin in mkdocs.yml
- Sets up markdown extensions
- Provides usage examples
- Explains integration with Material theme

## Configuration Examples

### Minimal mkdocs.yml

```yaml
site_name: My Documentation
site_url: https://example.com/

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - content.code.copy

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - pymdownx.details

nav:
  - Home: index.md
  - User Guide: guide.md
  - API Reference: api.md
```

### Production-Ready Configuration

```yaml
site_name: My Project Documentation
site_url: https://example.com/
site_description: Comprehensive documentation for My Project
repo_url: https://github.com/username/project
repo_name: username/project

theme:
  name: material
  custom_dir: overrides
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - tables

plugins:
  - search:
      lang: en
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            docstring_style: google
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
  - social:
      cards: true

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/username
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/username
  analytics:
    provider: google
    property: G-XXXXXXXXXX

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
  - User Guide:
      - user-guide/index.md
      - Basics: user-guide/basics.md
      - Advanced: user-guide/advanced.md
  - API Reference:
      - api/index.md
      - Core API: api/core.md
  - About:
      - Release Notes: about/changelog.md
      - License: about/license.md
```

## Examples

### Example 1: Python Package Documentation

**Scenario:** You're developing a Python package and need professional documentation with API references.

**Request:**
```markdown
Set up MkDocs documentation for my Python package "mylib" with:
- Material theme
- Auto-generated API docs from docstrings
- User guide with tutorials
- GitHub Pages deployment
```

**Steps:**
1. Claude creates project structure
2. Configures mkdocstrings for API documentation
3. Sets up gen-files to scan source code
4. Creates navigation with literate-nav
5. Adds GitHub Actions workflow

**Result:** Complete documentation site with automatic API reference generation, deployed to GitHub Pages.

---

### Example 2: Software Project Documentation

**Scenario:** You need documentation for a multi-component software project.

**Request:**
```markdown
Create documentation site with:
- Architecture diagrams using Mermaid
- Installation guides with terminal examples
- Configuration reference with all options
- Versioned documentation using mike
```

**Steps:**
1. Claude configures Mermaid plugin for diagrams
2. Adds termynal for terminal animations
3. Sets up comprehensive navigation structure
4. Configures mike for version management
5. Provides diagram and terminal examples

**Result:** Professional documentation with visual diagrams, animated terminal examples, and version selector.

---

### Example 3: DevOps Runbook

**Scenario:** You're creating operational runbooks for your team.

**Request:**
```markdown
Build a runbook site with:
- Step-by-step procedures
- Code blocks with syntax highlighting
- Admonitions for warnings and tips
- Search functionality
- GitLab Pages deployment
```

**Steps:**
1. Claude creates structured navigation for procedures
2. Configures markdown extensions for rich content
3. Sets up admonitions for callouts
4. Adds syntax highlighting for code
5. Creates GitLab CI pipeline

**Result:** Searchable runbook site with well-formatted procedures, deployed automatically on GitLab Pages.

## Troubleshooting

### Plugin Not Loading

**Problem:** The mkdocs skill doesn't activate.

**Solution:**
1. Verify plugin installation: `/plugin list`
2. Check skill is enabled: `/skill list`
3. Try manual activation: `@mkdocs`
4. Reload plugins: `/plugin reload`

### Build Errors

**Problem:** `mkdocs build` fails with errors.

**Solution:**
1. Use strict mode to see detailed errors: `mkdocs build --strict --verbose`
2. Check validation settings in mkdocs.yml
3. Verify all navigation links point to existing files
4. Ensure plugin dependencies are installed

### Theme Issues

**Problem:** Material theme features not working.

**Solution:**
1. Verify Material for MkDocs is installed: `pip install mkdocs-material`
2. Check feature names in theme configuration (see Material Theme Reference)
3. Ensure markdown extensions are configured for features like tabs and admonitions
4. Clear browser cache

### GitHub Pages Deployment

**Problem:** Site doesn't deploy to GitHub Pages.

**Solution:**
1. Check GitHub Actions workflow status
2. Verify Pages is enabled in repository settings
3. Ensure proper permissions in workflow (contents: read, pages: write)
4. Check site_url in mkdocs.yml matches GitHub Pages URL

## Best Practices

### Documentation Structure

- Use consistent navigation hierarchy (3 levels max)
- Create index.md for each section when using navigation.indexes
- Keep page titles concise and descriptive
- Use meaningful file and directory names

### Performance

- Enable `navigation.prune` for large sites (reduces size by 33%+)
- Use `navigation.instant` for SPA-like experience
- Optimize images before adding to docs
- Enable minify plugin for production

### SEO

- Always set `site_url` with trailing slash
- Add `site_description` and page descriptions
- Configure social cards for link previews
- Use proper heading hierarchy (H1 → H2 → H3)

### Content

- Write in active voice
- Use code blocks with language specifiers
- Add admonitions for important information
- Include examples for all features
- Keep content up-to-date with version management

### CI/CD

- Use strict mode in CI/CD pipelines
- Cache Python dependencies
- Only rebuild when docs/ changes
- Pin plugin versions for reproducibility

## Reference Documentation

For detailed configuration options and examples, see the reference files:

- **[CLI Reference](./skills/mkdocs/references/cli_reference.md)** - Complete command-line interface documentation with all commands, options, and examples
- **[Configuration Reference](./skills/mkdocs/references/configuration_reference.md)** - All mkdocs.yml settings with descriptions, valid values, and complete examples
- **[Material Theme Reference](./skills/mkdocs/references/material_theme_reference.md)** - Comprehensive Material for MkDocs theme configuration covering colors, navigation, features, and customization
- **[Plugins Reference](./skills/mkdocs/references/plugins_reference.md)** - Essential plugins with installation, configuration, and usage examples (mkdocstrings, gen-files, literate-nav, mermaid2, termynal, and more)
- **[Real-World Examples](./skills/mkdocs/references/real_world_examples.md)** - Active repositories using MkDocs, proven CI/CD workflows for GitHub Actions and GitLab CI, and production deployment patterns

## Contributing

This plugin is part of the claude_skills repository. To contribute:

1. Fork the repository
2. Make your changes in a feature branch
3. Test the plugin locally
4. Submit a pull request

See the main repository for contribution guidelines.

## License

This plugin is distributed as part of the claude_skills repository. See the repository's LICENSE file for details.

## Resources

### Official Documentation
- [MkDocs](https://www.mkdocs.org/) - Official MkDocs documentation
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - Material theme documentation
- [MkDocs Plugins Catalog](https://github.com/mkdocs/catalog) - Community plugins directory

### Community
- [MkDocs GitHub Discussions](https://github.com/mkdocs/mkdocs/discussions)
- [Material for MkDocs Discussions](https://github.com/squidfunk/mkdocs-material/discussions)

### Examples
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Built with MkDocs Material
- [Pydantic Documentation](https://docs.pydantic.dev/) - Advanced mkdocstrings usage
- [90 Days of DevOps](https://90daysofdevops.com/) - Educational content with MkDocs

## Changelog

### Version 1.0.0

- Initial release
- Complete CLI reference documentation
- Comprehensive mkdocs.yml configuration guide
- Material for MkDocs theme reference
- Essential plugins documentation
- Real-world examples and CI/CD patterns
