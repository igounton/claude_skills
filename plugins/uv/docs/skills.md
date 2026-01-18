# Skills Reference

This document provides detailed reference information for all skills included in the uv plugin.

## Overview

The uv plugin provides a single comprehensive skill that delivers expert guidance for Astral's uv package and project manager. The skill covers all aspects of modern Python development including project initialization, dependency management, script creation, tool installation, and environment management.

---

## uv

**Location**: `skills/uv/SKILL.md`

**Description**: Expert guidance for Astral's uv - an extremely fast Python package and project manager. Use when working with Python projects, managing dependencies, creating scripts with PEP 723 metadata, installing tools, managing Python versions, or configuring package indexes. Covers project initialization, dependency management, virtual environments, tool installation, workspace configuration, CI/CD integration, and migration from pip/poetry.

**User Invocable**: Yes (default)

**Allowed Tools**: All (unrestricted)

**Model**: Default (inherits from session)

### When to Use

Claude automatically activates this skill when:

- Working with Python projects or `pyproject.toml` files
- Managing project dependencies or resolving version conflicts
- Creating or editing Python scripts with dependencies
- Setting up virtual environments
- Installing command-line tools (ruff, black, pytest, etc.)
- Managing Python interpreter versions
- Configuring package indexes or private registries
- Migrating from pip, pip-tools, poetry, pipenv, or conda
- Setting up CI/CD pipelines for Python projects
- Configuring Docker containers for Python applications
- Troubleshooting dependency resolution or build failures

You can also explicitly invoke the skill with:

```
@uv
```

or via the Skill tool:

```
Skill(command: "uv")
```

### Core Capabilities

The uv skill provides comprehensive guidance across 10 major capability areas:

#### 1. Project Initialization and Management

Initialize new Python projects with modern structure and automatic configuration:

- **Standard projects**: `uv init myproject`
- **Application projects**: `uv init myapp --app`
- **Library projects**: `uv init mylib --lib --build-backend hatchling`
- **Bare projects**: `uv init --bare` (pyproject.toml only)

Creates complete project structure with:
- `.venv/` - Virtual environment (auto-created)
- `.python-version` - Pinned Python version
- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Lockfile for reproducible installs

#### 2. Dependency Management

Add, remove, and manage project dependencies with version constraints:

- **Production dependencies**: `uv add requests flask pydantic`
- **Development dependencies**: `uv add --dev pytest ruff mypy`
- **Optional groups**: `uv add --group docs sphinx`
- **Lock environments**: `uv lock` (update lockfile)
- **Sync environments**: `uv sync` (install from lockfile)
- **Upgrade packages**: `uv lock --upgrade-package requests`

Supports dependencies from:
- PyPI packages with version constraints
- Git repositories
- Local paths (editable or non-editable)
- Private package indexes

#### 3. Running Code in Project Context

Execute Python scripts and modules within the project environment:

- **Run scripts**: `uv run python script.py`
- **Run modules**: `uv run -m pytest`
- **Specific Python version**: `uv run --python 3.11 script.py`
- **Frozen mode** (no sync): `uv run --frozen script.py`
- **Temporary dependencies**: `uv run --with httpx script.py`
- **Environment files**: `uv run --env-file .env script.py`

Automatically syncs dependencies before running unless `--frozen` is specified.

#### 4. PEP 723 Inline Script Metadata

Create portable single-file scripts with embedded dependency information:

- **Initialize script**: `uv init --script example.py --python 3.12`
- **Add dependencies**: `uv add --script example.py requests rich`
- **Lock script**: `uv lock --script example.py`
- **Run directly**: `./example.py` (with proper shebang)

Scripts include inline metadata block:

```python
#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "rich>=13.0",
# ]
# ///
```

Best practices:
- Always include `requires-python` constraint
- Use version constraints for critical dependencies
- Lock scripts before sharing for reproducibility
- Add `exclude-newer` for time-based pinning

#### 5. Tool Management

Install and run command-line tools in isolated environments:

**Ephemeral execution** (no installation):
- `uvx ruff check` - Run tool once
- `uvx --from httpie http GET example.com` - Specify package
- `uvx --with mkdocs-material mkdocs serve` - Add plugins

**Persistent installation**:
- `uv tool install ruff black mypy` - Install globally
- `uv tool upgrade ruff` - Upgrade tool
- `uv tool list` - Show installed tools
- `uv tool uninstall ruff` - Remove tool
- `uv tool update-shell` - Update PATH configuration

#### 6. Python Version Management

Download, install, and manage Python interpreter versions:

- **Install Python**: `uv python install 3.12`
- **List versions**: `uv python list --all-versions`
- **Pin version**: `uv python pin 3.12` (creates `.python-version`)
- **Find executable**: `uv python find 3.11`
- **Upgrade installations**: `uv python upgrade --all`

Supports multiple implementations:
- CPython (standard Python)
- PyPy (JIT-compiled Python)
- GraalPy (polyglot Python)

Python downloads are automatic and managed in `~/.local/share/uv/python/`

#### 7. Virtual Environment Management

Create and manage isolated Python environments:

- **Create environment**: `uv venv`
- **Specific Python**: `uv venv --python 3.11`
- **Custom path**: `uv venv myenv`
- **System packages**: `uv venv --system-site-packages`
- **Seed packages**: `uv venv --seed` (pip, setuptools, wheel)

**Warning**: Running `uv venv` on existing environment wipes it without confirmation.

Activation uses standard Python methods:
- Unix: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

#### 8. pip-Compatible Interface

Drop-in replacement for pip and pip-tools commands:

- **Install packages**: `uv pip install flask requests`
- **Requirements files**: `uv pip install -r requirements.txt`
- **Editable installs**: `uv pip install -e .`
- **Compile requirements**: `uv pip compile pyproject.toml -o requirements.txt`
- **Sync environment**: `uv pip sync requirements.txt`
- **Dependency tree**: `uv pip tree`
- **Package info**: `uv pip show requests`

Performance comparison (76 packages):
- `uv pip freeze`: ~8ms
- `uv pip list`: ~10ms
- `uv pip show`: ~40ms (resolves relationships)

#### 9. Workspace Management (Monorepos)

Configure multi-package repositories with shared dependencies:

**Root pyproject.toml**:
```toml
[tool.uv.workspace]
members = ["packages/*", "apps/*"]
exclude = ["packages/deprecated"]
```

**Workspace commands**:
- `uv build --package my-package` - Build specific package
- `uv run --package my-package python script.py` - Run in package context
- `uv lock` - Single lockfile for all workspace members

**Workspace dependencies**:
```toml
[tool.uv.sources]
shared-lib = { workspace = true }
```

#### 10. Package Building and Publishing

Build distribution packages and publish to PyPI:

- **Build distributions**: `uv build` (wheel + sdist)
- **Build wheel only**: `uv build --wheel`
- **Workspace packages**: `uv build --package my-package`
- **Publish to PyPI**: `uv publish`
- **Test PyPI**: `uv publish --publish-url https://test.pypi.org/legacy/`
- **With token**: `uv publish --token $PYPI_TOKEN`

Smoke test before publishing:
```bash
uv run --isolated --no-project --with dist/*.whl python -c "import my_package"
```

### Configuration

The skill provides guidance for all uv configuration options:

**pyproject.toml settings**:
- `[tool.uv]` - Core uv settings
- `[tool.uv.sources]` - Custom package sources
- `[[tool.uv.index]]` - Additional package indexes
- `[dependency-groups]` - PEP 735 dependency groups

**Environment variables**:
- `UV_CACHE_DIR` - Custom cache location
- `UV_PYTHON_PREFERENCE` - Python discovery strategy
- `UV_CONCURRENT_DOWNLOADS` - Parallel download limit
- `UV_INDEX_*` - Package index authentication

See [./references/configuration.md](../skills/uv/references/configuration.md) for complete configuration reference.

### Common Workflows

The skill covers these standard workflows:

1. **Starting new projects**: Initialize, add dependencies, run code
2. **Creating portable scripts**: PEP 723 metadata, locking, execution
3. **Migrating from pip**: Import requirements.txt, convert to pyproject.toml
4. **Migrating from Poetry**: Automated conversion with migrate-to-uv
5. **CI/CD integration**: GitHub Actions, GitLab CI with caching and lockfiles
6. **Docker integration**: Multi-stage builds, optimized layers
7. **Git hooks**: pre-commit/prek integration with uv run

### Troubleshooting

The skill provides solutions for common issues:

- **"Externally Managed" errors**: Use virtual environments instead of --system
- **Build failures**: Missing system dependencies, Python version incompatibility
- **Lockfile out of sync**: When to use --locked vs --frozen
- **Cache issues**: Cleaning and pruning cache
- **Common pitfalls**: Forgetting sync, incorrect workspace globs, missing build-system

See [./references/troubleshooting.md](../skills/uv/references/troubleshooting.md) for comprehensive troubleshooting guide.

### Reference Files

The skill includes comprehensive reference documentation:

**CLI Reference** - [./references/cli_reference.md](../skills/uv/references/cli_reference.md)
- Complete command syntax and options
- All subcommands with examples
- Argument descriptions and constraints

**Configuration Reference** - [./references/configuration.md](../skills/uv/references/configuration.md)
- All environment variables
- pyproject.toml structure
- Index and source configuration
- Build settings and preferences

**Troubleshooting Guide** - [./references/troubleshooting.md](../skills/uv/references/troubleshooting.md)
- Common error messages and solutions
- Build failure diagnostics
- Dependency resolution issues
- Environment and cache problems

**Assets Directory** - `skills/uv/assets/`
- `pyproject_templates/` - Example configurations (basic, advanced, gitlab)
- `script_examples/` - PEP 723 script templates
- `docker_examples/` - Dockerfile configurations
- `github_actions/` - CI/CD workflow examples

### Hooks

This skill does not define custom hooks.

### Version Information

**Skill Version**: 1.0.0

**uv Version Coverage**: 0.9.5+ (October 2025)

Key features covered:
- Python 3.14 support with free-threaded builds
- Enhanced authentication system
- Advanced build configuration
- Workspace improvements
- Docker image optimizations

### External Resources

- **Official Documentation**: https://docs.astral.sh/uv/
- **GitHub Repository**: https://github.com/astral-sh/uv
- **Concepts Guide**: https://docs.astral.sh/uv/concepts/
- **Migration Guides**: https://docs.astral.sh/uv/guides/migration/
- **Astral (Creators)**: https://astral.sh

---

[← Back to README](../README.md)
