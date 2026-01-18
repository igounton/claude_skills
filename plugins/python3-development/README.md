# Python3 Development Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Comprehensive Python development orchestration plugin providing modern Python 3.11+ patterns, agent coordination workflows, quality gates, and extensive reference documentation for building robust Python applications and CLI tools.

## Features

- **Modern Python 3.11+ Patterns** - Native generics, union types (PEP 604), PEP 723 inline script metadata, type-safe async processing
- **Agent Orchestration** - Structured workflows for TDD, feature addition, refactoring, debugging, and code review
- **Comprehensive Type Safety** - Complete mypy patterns with generics, protocols, TypedDict, and type narrowing
- **Quality Gates** - Integration with ruff, mypy/basedpyright/pyright, pytest, and pre-commit/prek
- **50+ Modern Modules** - In-depth guides for Typer, Rich, httpx, attrs, pydantic, FastAPI, and more
- **PEP 723 Support** - Inline script metadata for portable single-file executables with dependencies
- **Command Reference Library** - Templates and patterns for creating Claude Code slash commands
- **Tool Registry** - Catalog of development tools for linting, testing, and build automation

## Installation

### Prerequisites

**Required**:
- Claude Code 2.1+
- Python 3.11 or higher
- `uv` - Python package and project manager ([install guide](https://github.com/astral-sh/uv))

**Recommended**:
- `ruff` - Fast Python linter and formatter
- `basedpyright` or `pyright` - Type checker
- `pytest` - Testing framework
- `pre-commit` or `prek` - Git hook framework

### Install Plugin

```bash
# Method 1: Using cc plugin install (if plugin is in a marketplace)
cc plugin install python3-development

# Method 2: Manual installation
git clone <repository-url> ~/.claude/plugins/python3-development
cc plugin reload
```

### External Dependencies

This plugin provides orchestration guidance and reference documentation. The following external capabilities must be installed separately:

**Agents** (install to `~/.claude/agents/`):
- `@agent-python-cli-architect` - Python CLI development with Typer and Rich
- `@agent-python-pytest-architect` - Test suite creation and planning
- `@agent-python-code-reviewer` - Post-implementation code review
- `@agent-python-portable-script` - Standalone stdlib-only script creation

**Slash Commands** (install to `~/.claude/commands/`):
- `/modernpython` - Python 3.11+ pattern enforcement and legacy code detection
- `/shebangpython` - PEP 723 inline script metadata validation

See [Installation Guide](./docs/installation.md) for detailed setup instructions.

## Quick Start

### Using the Skill

The `python3-development` skill activates automatically when working with Python projects. Claude decides when to use it based on your task.

**Manual activation**:

```text
@python3-development
```

**Triggers automatic activation**:
- Working within any Python project
- Python script writing or editing
- Running Python tests
- Linting or formatting Python code
- Building CLI applications with Typer and Rich
- Creating portable Python scripts
- Pre-commit or linting errors in Python files

### Creating a Python CLI Tool

```text
User: "Build a CLI tool to process CSV files with progress bars"

Claude (orchestrator):
1. Reads python-development-orchestration.md
2. Delegates to @agent-python-cli-architect for implementation
3. Delegates to @agent-python-pytest-architect for tests
4. Validates with /modernpython and /shebangpython
5. Delegates to @agent-python-code-reviewer for final review
```

### Validating Modern Python Patterns

```bash
# Check for Python 3.11+ patterns and legacy code
/modernpython src/mymodule.py

# Validate script shebang and PEP 723 metadata
/shebangpython scripts/deploy.py
```

## Capabilities

| Type | Name | Description | User Invocable |
|------|------|-------------|----------------|
| Skill | python3-development | Orchestration guide for Python development using modern 3.11+ patterns, agent coordination, and quality gates | Yes |

### Command Reference Library

The plugin includes command reference material in `commands/` (NOT actual slash commands):

| File | Purpose |
|------|---------|
| `development/create-feature-task.md` | Reference for structured feature development workflows |
| `development/use-command-template.md` | Reference for creating new slash commands |
| `testing/analyze-test-failures.md` | Reference for balanced test failure investigation |
| `testing/comprehensive-test-review.md` | Reference for thorough test reviews |
| `testing/test-failure-mindset.md` | Reference for test failure analysis approach |

See [docs/commands.md](./docs/commands.md) for complete command reference details.

## Usage

### Skills

The **python3-development** skill provides:

1. **Agent Orchestration** - Coordinate specialized agents for complex Python development tasks
2. **Modern Python Standards** - Python 3.11+ patterns with PEP citations
3. **Quality Gates** - Format-first workflow with ruff, type checking, and testing
4. **Reference Documentation** - 50+ module guides, tool registry, API specs
5. **Workflow Patterns** - TDD, feature addition, refactoring, debugging, code review

**Pre-Delegation Protocol** (orchestrators):

Before delegating any Python task, orchestrators MUST:
1. Read the orchestration guide
2. Identify the workflow pattern (TDD/Feature Addition/Refactoring/etc.)
3. Plan the agent chain (design → test → implement → review)
4. Define scope boundaries for each agent
5. Set success criteria

See [docs/skills.md](./docs/skills.md) for complete skill reference.

### Agent Coordination

The skill coordinates specialized agents for Python development:

```text
Feature Addition Workflow:
User Request
    ↓
@python3-development skill (orchestrator reads guide)
    ↓
@agent-python-cli-architect (implementation)
    ↓
@agent-python-pytest-architect (testing)
    ↓
@agent-python-code-reviewer (review)
    ↓
Quality Gates: /modernpython, /shebangpython, ruff, pytest
```

**Agent Responsibilities**:
- **python-cli-architect**: Implement Python code with Typer+Rich or stdlib
- **python-pytest-architect**: Create comprehensive test suites
- **python-code-reviewer**: Review against best practices and code smells
- **python-portable-script**: Create standalone stdlib-only scripts

### Quality Gates

Every Python task must pass:

1. **Format-first**: `uv run ruff format` (or via pre-commit/prek)
2. **Linting**: `uv run ruff check` (clean, after formatting)
3. **Type checking**: Use detected type checker (basedpyright/pyright/mypy)
4. **Tests**: `uv run pytest` (>80% coverage)
5. **Modern patterns**: `/modernpython` (no legacy typing)
6. **Script compliance**: `/shebangpython` (for standalone scripts)

**Preferred execution** (if `.pre-commit-config.yaml` exists):

```bash
# Detect which tool is installed (pre-commit or prek)
uv run <detected-tool> run --files <changed_files>
```

### Reference Documentation

Comprehensive guides included in `skills/python3-development/references/`:

- [User Project Conventions](./skills/python3-development/references/user-project-conventions.md) - Extracted conventions from production projects
- [Modern Python Modules](./skills/python3-development/references/modern-modules.md) - 50+ library guides
- [Tool & Library Registry](./skills/python3-development/references/tool-library-registry.md) - Development tools catalog
- [Python Development Orchestration](./skills/python3-development/references/python-development-orchestration.md) - Detailed workflow patterns
- [PEP 723 Reference](./skills/python3-development/references/PEP723.md) - Inline script metadata guide
- [Exception Handling](./skills/python3-development/references/exception-handling.md) - Typer exception patterns

## Examples

See [docs/examples.md](./docs/examples.md) for detailed usage examples including:

1. Creating a Python CLI tool with Typer and Rich
2. Implementing comprehensive type safety with mypy
3. Using the orchestration workflow for feature addition
4. Creating portable scripts with PEP 723 metadata
5. Setting up quality gates with pre-commit/prek

## Configuration

### Skill Frontmatter

```yaml
---
name: python3-development
description: Python development orchestration with modern 3.11+ patterns
version: "1.2.0"
python_compatibility: "3.11+"
---
```

### Customization

**Linting Discovery Protocol**: The skill automatically detects project-specific tools:

1. Check for `.pre-commit-config.yaml` (pre-commit or prek)
2. Check CI pipeline configuration (`.gitlab-ci.yml`, `.github/workflows/`)
3. Fallback to `pyproject.toml` tool detection

**Type Checker Detection**: Automatically detects basedpyright, pyright, or mypy from:
- `.pre-commit-config.yaml` hooks
- `pyproject.toml` configuration sections
- CI pipeline invocations

### Asset Templates

Copy standard configurations from `skills/python3-development/assets/`:

```bash
# Version management
cp ~/.claude/skills/python3-development/assets/version.py packages/{package}/version.py

# Pre-commit configuration
cp ~/.claude/skills/python3-development/assets/.pre-commit-config.yaml .

# Markdown linting
cp ~/.claude/skills/python3-development/assets/.markdownlint.json .

# Editor settings
cp ~/.claude/skills/python3-development/assets/.editorconfig .
```

## Troubleshooting

### "The model should read the orchestration guide first"

**Problem**: Orchestrator attempts to delegate without reading the guide, leading to context exhaustion or architectural mistakes.

**Solution**: The skill enforces a pre-delegation protocol. Orchestrators must read `references/python-development-orchestration.md` and state the workflow pattern before using the Task tool.

### "Command not found: /modernpython or /shebangpython"

**Problem**: External slash commands are not installed.

**Solution**: These commands must be installed separately to `~/.claude/commands/`. They are not bundled with this plugin. Contact the plugin maintainer for command installation instructions.

### "Pre-commit hook not running"

**Problem**: Git hooks not installed or wrong tool detected.

**Solution**:

```bash
# Detect which tool is installed
uv run python -c "print(open('.git/hooks/pre-commit').readlines()[1].split()[4].rstrip(':') if __import__('pathlib').Path('.git/hooks/pre-commit').exists() else 'prek')"

# Install hooks with detected tool
uv run <detected-tool> install
```

### "Type checking fails with wrong checker"

**Problem**: Project uses basedpyright but skill detected mypy.

**Solution**: The skill auto-detects type checkers from configuration. Ensure your `.pre-commit-config.yaml` or `pyproject.toml` clearly specifies the type checker:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/detachhead/basedpyright
  hooks:
    - id: basedpyright
```

### "Linting errors on vendored code"

**Problem**: Linter flags issues in third-party code copied into the repository.

**Solution**: Vendored code is an acceptable linting exception. Configure per-file ignores in `pyproject.toml`:

```toml
[tool.ruff.lint.per-file-ignores]
"vendor/**" = ["ALL"]
```

## Contributing

Contributions are welcome. When contributing:

1. Follow the skill's own standards (it's self-referential)
2. Run quality gates before submitting
3. Update reference documentation for new patterns
4. Add examples for new features

## License

[Specify license here]

## Credits

Developed for Claude Code to provide comprehensive Python development orchestration with modern 3.11+ patterns, agent coordination, and quality assurance workflows.

## Related Resources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Python 3.11+ Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
- [PEP 723 - Inline Script Metadata](https://peps.python.org/pep-0723/)
- [uv - Python Package Manager](https://github.com/astral-sh/uv)
- [Ruff - Fast Python Linter](https://github.com/astral-sh/ruff)
