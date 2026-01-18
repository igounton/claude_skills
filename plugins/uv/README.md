# uv Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Expert guidance for Astral's uv - an extremely fast Python package and project manager. Provides comprehensive knowledge for managing Python projects, dependencies, scripts, tools, and environments using modern standards.

## Features

- **Project Management**: Initialize projects with modern structure, lockfiles, and automatic virtual environments
- **Dependency Management**: Add/remove dependencies with version constraints, lock environments for reproducibility
- **PEP 723 Scripts**: Create portable single-file scripts with inline dependency metadata
- **Tool Management**: Install and run CLI tools (ruff, black, pytest, etc.) in isolated environments
- **Python Version Management**: Download, install, and switch between Python versions automatically
- **pip Compatibility**: Drop-in replacement for pip, pip-tools, and pip-compile commands
- **Workspace Support**: Manage monorepos with multiple packages and shared dependencies
- **CI/CD Integration**: Optimized workflows for GitHub Actions, GitLab CI, and Docker
- **Migration Assistance**: Convert from pip, poetry, pipenv, and conda-based projects

## Installation

### Prerequisites

- **Claude Code**: Version 2.1 or later
- **System**: Linux, macOS, or Windows
- **uv binary**: Installed on your system

Install uv if not already installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv

# With pipx
pipx install uv

# With Homebrew
brew install uv
```

### Install Plugin

```bash
# Method 1: From local repository
cd /home/user/claude_skills
./install.py

# Method 2: Manual installation
mkdir -p ~/.claude/plugins
cp -r ./plugins/uv ~/.claude/plugins/
```

The plugin will be automatically loaded by Claude Code on next session.

## Quick Start

Create a new Python project with modern tooling:

```bash
# Initialize project
uv init myproject
cd myproject

# Add dependencies
uv add fastapi uvicorn pydantic

# Add development dependencies
uv add --dev pytest ruff mypy

# Run your application
uv run python main.py

# Run tests
uv run pytest
```

Claude will automatically activate the uv skill when you work with Python projects, mention uv, or perform package management tasks.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | uv | Expert guidance for Astral's uv package manager covering project initialization, dependency management, PEP 723 scripts, tool installation, Python version management, virtual environments, workspaces, and CI/CD integration | Auto-invoked or `@uv` |

## Usage

### Skill: uv

The uv skill provides comprehensive guidance for using Astral's uv package manager. It covers all aspects of modern Python project management:

**Core Capabilities**:
- Project initialization with `uv init` (apps, libraries, scripts)
- Dependency management with `uv add`, `uv remove`, `uv lock`, `uv sync`
- Running code with `uv run` in project context
- PEP 723 inline script metadata for portable single-file scripts
- Tool management with `uv tool install` and `uvx` for ephemeral execution
- Python version management with automatic downloads
- Virtual environment creation and management
- pip-compatible commands for migration (`uv pip install`, `uv pip compile`)
- Workspace configuration for monorepos
- Package building and publishing to PyPI

**When Claude Uses This Skill**:
- Working with Python projects or pyproject.toml files
- Managing dependencies or resolving version conflicts
- Creating portable scripts with dependencies
- Setting up CI/CD pipelines for Python
- Migrating from pip, poetry, pipenv, or conda
- Troubleshooting build failures or environment issues

For detailed documentation, see [Skills Reference](./docs/skills.md).

## Examples

### Example 1: Create a FastAPI Application

```bash
# Initialize application project
uv init fastapi-app --app
cd fastapi-app

# Add production dependencies
uv add fastapi uvicorn[standard] pydantic sqlalchemy

# Add development dependencies
uv add --dev pytest pytest-asyncio httpx ruff mypy

# Create main application file
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI with uv"}
EOF

# Run the application
uv run uvicorn main:app --reload
```

### Example 2: Create a Portable Data Analysis Script

```bash
# Initialize script with metadata
uv init --script analyze.py --python 3.11

# Add dependencies
uv add --script analyze.py pandas matplotlib numpy

# The script now contains:
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "matplotlib", "numpy"]
# ///

# Lock for reproducibility
uv lock --script analyze.py

# Make executable and run
chmod +x analyze.py
./analyze.py
```

### Example 3: Migrate from requirements.txt

```bash
# In existing project with requirements.txt
uv init --bare

# Import dependencies
uv add -r requirements.txt

# Import dev dependencies
uv add --dev -r requirements-dev.txt

# Sync environment
uv sync

# Remove old files
rm requirements*.txt

# Continue with uv commands
uv run pytest
```

For more examples, see [Examples Documentation](./docs/examples.md).

## Configuration

The uv skill operates without additional configuration. It provides guidance based on:

- **Standard uv commands**: All official CLI commands and options
- **pyproject.toml conventions**: Modern Python packaging standards
- **PEP 723**: Inline script dependency metadata
- **Workspace patterns**: Monorepo management
- **CI/CD best practices**: GitHub Actions, GitLab CI, Docker

The skill references comprehensive documentation in `skills/uv/references/`:
- `cli_reference.md` - Complete command reference
- `configuration.md` - Environment variables and settings
- `troubleshooting.md` - Common issues and solutions

## Troubleshooting

### Skill Not Activating

If Claude doesn't automatically use the uv skill:

```bash
# Manually invoke with @-syntax
@uv help me set up a new Python project

# Or in conversation
Please use the uv skill to help me manage dependencies
```

### Plugin Not Loaded

Verify plugin installation:

```bash
# Check plugin is in settings
cat ~/.claude/settings.json | grep -A 2 "enabledPlugins"

# Reload Claude Code
# Restart your Claude Code session
```

### uv Binary Not Found

Ensure uv is installed and in PATH:

```bash
# Check installation
which uv
uv --version

# Add to PATH if needed (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

## Resources

- [Skills Documentation](./docs/skills.md) - Complete skill reference
- [Examples](./docs/examples.md) - Real-world usage examples
- [Official uv Documentation](https://docs.astral.sh/uv/) - Astral's official docs
- [uv GitHub Repository](https://github.com/astral-sh/uv) - Source code and issues
- [Migration Guides](https://docs.astral.sh/uv/guides/migration/) - From pip, poetry, etc.

## Contributing

This plugin is part of the claude_skills repository. Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes to `plugins/uv/`
4. Test with Claude Code
5. Submit a pull request

## License

MIT License - See LICENSE file for details.

## Credits

**Plugin Author**: claude_skills repository contributors

**uv Tool**: Created by [Astral](https://astral.sh) (makers of ruff)
- GitHub: https://github.com/astral-sh/uv
- Documentation: https://docs.astral.sh/uv/

**Version Information**:
- Plugin Version: 1.0.0
- uv Version Supported: 0.9.5+ (as of October 2025)
- Claude Code Compatibility: 2.1+
