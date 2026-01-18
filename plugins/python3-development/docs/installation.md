# Installation Guide

Complete installation and setup instructions for the python3-development plugin.

## Prerequisites

### Required

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | 2.1+ | Plugin host platform |
| Python | 3.11+ | Modern Python patterns (3.12+ recommended for native generics) |
| uv | Latest | Python package and project manager |

### Recommended

| Component | Purpose |
|-----------|---------|
| ruff | Fast Python linter and formatter |
| basedpyright or pyright | Type checker (basedpyright recommended for GitLab projects) |
| pytest | Testing framework |
| pre-commit or prek | Git hook framework (prek is faster, Rust-based) |

## Installing Prerequisites

### Install Python 3.11+

**macOS** (using Homebrew):
```bash
brew install python@3.11
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

**Verify installation**:
```bash
python3.11 --version
# Should output: Python 3.11.x or higher
```

### Install uv (Required)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Verify installation**:
```bash
uv --version
# Should output: uv x.y.z
```

**Documentation**: [uv installation guide](https://github.com/astral-sh/uv#installation)

### Install Development Tools (Recommended)

**Using uv** (recommended):
```bash
# Install tools globally
uv tool install ruff
uv tool install basedpyright
uv tool install pytest
uv tool install pre-commit  # or prek for faster Rust-based alternative
```

**Using pipx** (alternative):
```bash
pipx install ruff
pipx install basedpyright
pipx install pytest
pipx install pre-commit
```

**Verify installation**:
```bash
ruff --version
basedpyright --version
pytest --version
pre-commit --version  # or prek --version
```

## Plugin Installation

### Method 1: Marketplace Installation (Recommended)

If the plugin is available in a Claude Code marketplace:

```bash
# Add marketplace (if not already added)
cc plugin marketplace add <marketplace-owner>/<marketplace-repo>

# Install plugin
cc plugin install python3-development

# Reload to activate
cc plugin reload
```

### Method 2: Manual Installation

**Clone to user plugins directory**:
```bash
# Clone repository
git clone <repository-url> ~/.claude/plugins/python3-development

# Reload Claude Code
cc plugin reload
```

**Clone to project plugins directory** (project-specific):
```bash
# Clone to project
git clone <repository-url> .claude/plugins/python3-development

# Add to project settings
echo '{
  "enabledPlugins": {
    "python3-development": true
  }
}' > .claude/settings.json

# Reload Claude Code
cc plugin reload
```

### Verify Plugin Installation

```bash
# List installed plugins
cc plugin list

# Should show: python3-development (enabled)
```

**In Claude Code**:
```text
/plugin list
```

You should see `python3-development` with status `enabled`.

## External Dependencies Installation

The plugin requires external capabilities that must be installed separately.

### Required Agents

These agents perform specialized Python development tasks. Install to `~/.claude/agents/`:

| Agent | Purpose | Installation |
|-------|---------|--------------|
| python-cli-architect | Python CLI development with Typer and Rich | See agent repository |
| python-pytest-architect | Test suite creation and planning | See agent repository |
| python-code-reviewer | Post-implementation code review | See agent repository |
| python-portable-script | Standalone stdlib-only script creation | See agent repository |

**Installation pattern**:
```bash
# Example for python-cli-architect
git clone <agent-repository-url> ~/.claude/agents/python-cli-architect

# Verify
ls ~/.claude/agents/
# Should show: python-cli-architect/
```

**Note**: Contact the plugin maintainer for agent repository URLs.

### Required Slash Commands

These commands provide validation and pattern enforcement. Install to `~/.claude/commands/`:

| Command | Purpose | Installation |
|---------|---------|--------------|
| /modernpython | Python 3.11+ pattern enforcement | See command repository |
| /shebangpython | PEP 723 validation and shebang standards | See command repository |

**Installation pattern**:
```bash
# Example for modernpython
curl -o ~/.claude/commands/modernpython.md <command-url>

# Verify
ls ~/.claude/commands/
# Should show: modernpython.md, shebangpython.md
```

**Note**: Contact the plugin maintainer for command installation instructions.

### Optional: Specialized Agents

| Agent | Purpose |
|-------|---------|
| spec-architect | Architecture design |
| spec-planner | Task breakdown and planning |
| spec-analyst | Requirements gathering |

Install to `~/.claude/agents/` following the same pattern as required agents.

## Project Setup

### Initialize a New Python Project

Using the plugin's standards:

```bash
# Create project directory
mkdir my-python-project
cd my-python-project

# Initialize with uv
uv init --python 3.11

# Create standard structure
mkdir -p packages/my_python_project tests scripts sessions

# Copy asset templates from plugin
cp ~/.claude/plugins/python3-development/skills/python3-development/assets/.pre-commit-config.yaml .
cp ~/.claude/plugins/python3-development/skills/python3-development/assets/.editorconfig .
cp ~/.claude/plugins/python3-development/skills/python3-development/assets/.markdownlint.json .

# Create pyproject.toml (see Configuration section)

# Initialize git
git init
git add .
git commit -m "Initial project structure"

# Install git hooks
uv run pre-commit install  # or: uv run prek install
```

### Configure pyproject.toml

Example configuration following plugin standards:

```toml
[project]
name = "my-python-project"
version = "0.1.0"
description = "Description of my project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.5.0",
    "basedpyright>=1.13.0",
    "pytest>=8.0.0",
    "pytest-cov>=5.0.0",
    "pre-commit>=3.7.0",
]

[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.targets.wheel]
packages = ["packages/my_python_project"]

[tool.ruff]
target-version = "py311"
line-length = 120

[tool.ruff.lint]
select = ["ALL"]
ignore = ["COM812", "ISC001"]  # Conflicts with formatter

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S", "D", "ANN", "PLR", "T"]
"scripts/**" = ["T201", "S"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.basedpyright]
pythonVersion = "3.11"
typeCheckingMode = "strict"
reportMissingTypeStubs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=packages",
    "--cov-report=term-missing",
    "--cov-report=html",
]
```

**Template variables**: See [Tool & Library Registry - Template Variables](../skills/python3-development/references/tool-library-registry.md) for complete variable reference and sourcing methods.

### Verify Setup

```bash
# Check Python version
python --version
# Should be 3.11+

# Check uv
uv --version

# Verify project structure
tree -L 2
# Should show:
# .
# ├── packages/
# │   └── my_python_project/
# ├── tests/
# ├── scripts/
# ├── pyproject.toml
# ├── .pre-commit-config.yaml
# └── README.md

# Install dependencies
uv sync

# Run quality checks
uv run pre-commit run --all-files
# Should pass (or auto-fix issues)
```

## Configuration

### Plugin Customization

The plugin automatically detects project-specific configurations. No plugin-level configuration required.

### Linting Tool Detection

The plugin's **Linting Discovery Protocol** automatically detects:

1. **Git hook tools** (pre-commit or prek):
   ```bash
   # Check if config exists
   test -f .pre-commit-config.yaml && echo "Git hooks detected"
   ```

2. **CI pipeline tools**:
   ```bash
   # GitLab CI
   test -f .gitlab-ci.yml && echo "GitLab CI detected"

   # GitHub Actions
   find .github/workflows -name "*.yml" 2>/dev/null
   ```

3. **Type checker detection**:
   ```bash
   # From pre-commit config
   grep -E "basedpyright|pyright|mypy" .pre-commit-config.yaml

   # From pyproject.toml
   grep -E "^\[tool\.(basedpyright|pyright|mypy)\]" pyproject.toml
   ```

### Environment Setup for Sessions

If using cc-sessions framework:

```bash
# Create sessions directory
mkdir -p sessions

# Optional: SessionStart hook for environment activation
# (Configured in .claude/settings.json)
```

See [Sessions Integration](../skills/python3-development/references/user-project-conventions.md) for details.

## Verification

### Test Plugin Activation

**In Claude Code**:
```text
User: "I want to create a Python CLI tool"

Claude should respond with:
"Activating python3-development skill..."
```

### Test Quality Gates

```bash
# Create test file
cat > packages/my_python_project/example.py << 'EOF'
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"
EOF

# Run quality gates
uv run ruff format packages/
uv run ruff check packages/
uv run basedpyright packages/

# All should pass without errors
```

### Test External Commands

**If installed**:
```text
/modernpython packages/my_python_project/example.py
# Should load Python 3.11+ reference guide

/shebangpython scripts/deploy.py
# Should validate shebang and PEP 723 metadata
```

## Troubleshooting

### "Plugin not found"

**Problem**: `cc plugin list` doesn't show python3-development

**Solution**:
```bash
# Check installation directory
ls -la ~/.claude/plugins/python3-development/

# If missing, reinstall
git clone <repository-url> ~/.claude/plugins/python3-development

# Reload
cc plugin reload
```

### "uv command not found"

**Problem**: `uv` not in PATH

**Solution**:
```bash
# Check installation
which uv

# If not found, reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.cargo/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

### "Skill not activating"

**Problem**: Skill doesn't activate when working with Python files

**Solution**:
1. Verify plugin is enabled:
   ```bash
   cc plugin list
   ```

2. Check plugin.json:
   ```bash
   cat ~/.claude/plugins/python3-development/.claude-plugin/plugin.json
   ```

3. Ensure `skills` field points to correct directory:
   ```json
   {
     "skills": ["./skills/python3-development"]
   }
   ```

4. Reload plugin:
   ```bash
   cc plugin reload
   ```

### "External agents not found"

**Problem**: Orchestrator can't find @agent-python-cli-architect

**Solution**:
```bash
# Check agents directory
ls ~/.claude/agents/

# If missing, install agents (contact maintainer for URLs)
git clone <agent-repo> ~/.claude/agents/python-cli-architect

# Verify AGENT.md or agent configuration exists
ls ~/.claude/agents/python-cli-architect/
```

### "Type checker not detected"

**Problem**: Skill runs wrong type checker

**Solution**:

1. Add explicit configuration to `.pre-commit-config.yaml`:
   ```yaml
   - repo: https://github.com/detachhead/basedpyright
     rev: v1.13.0
     hooks:
       - id: basedpyright
   ```

2. Or add to `pyproject.toml`:
   ```toml
   [tool.basedpyright]
   pythonVersion = "3.11"
   typeCheckingMode = "strict"
   ```

3. Reload and verify:
   ```bash
   grep -E "basedpyright|pyright|mypy" .pre-commit-config.yaml
   ```

### "Pre-commit hooks not running"

**Problem**: Git commit doesn't trigger hooks

**Solution**:
```bash
# Check if hooks are installed
ls -la .git/hooks/pre-commit

# If missing, install
uv run pre-commit install

# Or if using prek
uv run prek install

# Verify installation
cat .git/hooks/pre-commit
# Should show hook script referencing pre-commit or prek

# Test manually
uv run pre-commit run --all-files
```

## Next Steps

After installation:

1. **Read the orchestration guide** (orchestrators):
   - [Python Development Orchestration](../skills/python3-development/references/python-development-orchestration.md)

2. **Explore reference documentation**:
   - [Modern Python Modules](../skills/python3-development/references/modern-modules.md)
   - [Tool & Library Registry](../skills/python3-development/references/tool-library-registry.md)
   - [PEP 723 Reference](../skills/python3-development/references/PEP723.md)

3. **Review examples**:
   - [Usage Examples](./examples.md)

4. **Try the skill**:
   ```text
   User: "Create a simple Python CLI tool with Typer"
   ```

## Support

For issues, questions, or contributions:

- Review [Troubleshooting](#troubleshooting) section
- Check [examples](./examples.md) for usage patterns
- Consult [skill documentation](./skills.md) for detailed reference
- Contact plugin maintainer for external dependencies (agents, commands)

## Additional Resources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [PEP 723 - Inline Script Metadata](https://peps.python.org/pep-0723/)
- [Python 3.11+ Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
