# Configuration Reference

Complete reference for configuring pre-commit hooks using `.pre-commit-config.yaml` and defining hooks with `.pre-commit-hooks.yaml`.

## Overview

Two configuration files control pre-commit behavior:

| File | Location | Purpose | Audience |
|------|----------|---------|----------|
| `.pre-commit-config.yaml` | User repository root | Defines which hooks to use | Repository users |
| `.pre-commit-hooks.yaml` | Hook repository root | Defines available hooks | Hook authors |

## .pre-commit-config.yaml

Configuration file for users consuming hooks.

### Complete Schema

```yaml
# Top-level configuration
default_install_hook_types: [pre-commit, prepare-commit-msg]
default_stages: [pre-commit, prepare-commit-msg]
fail_fast: false
minimum_pre_commit_version: '3.2.0'

# Hook repositories
repos:
  - repo: https://github.com/org/tool
    rev: v1.0.0
    hooks:
      - id: hook-name
        name: Display Name Override
        alias: alternate-name
        language_version: python3.11
        files: '\\.py$'
        exclude: '^tests/'
        types: [python]
        types_or: [python, pyi]
        exclude_types: [markdown]
        args: [--option, value]
        stages: [pre-commit]
        additional_dependencies: ['package>=1.0']
        always_run: false
        pass_filenames: true
        require_serial: false
        verbose: false
```

### Top-Level Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `default_install_hook_types` | list | `[pre-commit]` | Hook types installed by `pre-commit install` |
| `default_stages` | list | all stages | Default stages for all hooks |
| `fail_fast` | bool | `false` | Stop execution on first failure |
| `minimum_pre_commit_version` | string | none | Minimum pre-commit version required |
| `repos` | list | **Required** | List of hook repositories |

### Repository Configuration

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `repo` | string | **Yes** | Repository URL or `local` |
| `rev` | string | **Yes** (except local) | Immutable ref (tag or SHA) |
| `hooks` | list | **Yes** | List of hooks to use |

**Repository URL Examples**:

```yaml
# GitHub
repo: https://github.com/org/repo

# GitLab
repo: https://gitlab.com/org/repo

# Bitbucket
repo: https://bitbucket.org/org/repo

# Local hooks
repo: local
```

**Immutable References**:

```yaml
# Good: Tags
rev: v1.0.0

# Good: Commit SHAs
rev: a1b2c3d4e5f6

# Bad: Branch names (don't auto-update)
rev: main  # Don't use
```

### Hook Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | string | **Required** | Hook identifier from `.pre-commit-hooks.yaml` |
| `name` | string | From definition | Override display name |
| `alias` | string | none | Alternative hook name |
| `language_version` | string | system | Python/Node/Ruby version |
| `files` | regex | `''` (all) | Files to run on (AND with types) |
| `exclude` | regex | `^$` (none) | Files to exclude |
| `types` | list | `[file]` | File types (AND logic) |
| `types_or` | list | none | File types (OR logic) |
| `exclude_types` | list | none | File types to exclude |
| `args` | list | none | Additional CLI arguments |
| `stages` | list | all | Hook stages to run for |
| `additional_dependencies` | list | none | Extra packages to install |
| `always_run` | bool | `false` | Run without matching files |
| `pass_filenames` | bool | `true` | Pass filenames to hook |
| `require_serial` | bool | `false` | Prevent parallel execution |
| `verbose` | bool | `false` | Show output on success |

### File Matching

**Match Python files**:

```yaml
hooks:
  - id: mypy
    files: '\\.py$'
    types: [python]
```

**Exclude test files**:

```yaml
hooks:
  - id: pylint
    exclude: '^tests/|^conftest\\.py$'
```

**Match multiple file types**:

```yaml
hooks:
  - id: prettier
    types_or: [javascript, jsx, ts, tsx, json, yaml]
```

**Exclude specific types**:

```yaml
hooks:
  - id: check-added-large-files
    exclude_types: [binary]
```

### Stages Configuration

**Available Stages**:

| Stage | Git Hook | Typical Use |
|-------|----------|-------------|
| `pre-commit` | pre-commit | Formatting, linting |
| `prepare-commit-msg` | prepare-commit-msg | Message rewriting |
| `commit-msg` | commit-msg | Message validation |
| `post-commit` | post-commit | Notifications |
| `pre-push` | pre-push | Integration tests |
| `pre-merge-commit` | pre-merge-commit | Merge validation |
| `pre-rebase` | pre-rebase | Rebase validation |
| `post-checkout` | post-checkout | Environment setup |
| `post-merge` | post-merge | Dependency updates |
| `manual` | none | Explicit `pre-commit run` only |

**Stage Examples**:

```yaml
# Run formatter on pre-commit only
- id: black
  stages: [pre-commit]

# Run tests on both pre-commit and pre-push
- id: pytest
  stages: [pre-commit, pre-push]

# Run manually only
- id: expensive-check
  stages: [manual]
```

### Language Versions

Specify interpreter version for language-based hooks:

```yaml
# Python
- id: black
  language_version: python3.11

# Node
- id: prettier
  language_version: node18.x

# Ruby
- id: rubocop
  language_version: ruby3.2
```

### Additional Dependencies

Install extra packages with the hook:

```yaml
# Python packages
- id: pylint
  additional_dependencies:
    - pylint-django>=2.5
    - pylint-celery>=0.3

# Node packages
- id: eslint
  additional_dependencies:
    - eslint-plugin-react@latest
    - '@typescript-eslint/eslint-plugin@5.0.0'
```

### Complete Examples

**Python Project**:

```yaml
default_install_hook_types: [pre-commit, pre-push]

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

**JavaScript/TypeScript Project**:

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, yaml]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: '\\.[jt]sx?$'
        types: [file]
        additional_dependencies:
          - eslint@8.56.0
          - '@typescript-eslint/eslint-plugin@6.0.0'
          - '@typescript-eslint/parser@6.0.0'
```

**Polyglot Project**:

```yaml
repos:
  # Python
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, tsx, json]

  # Rust
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
      - id: clippy

  # Go
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-lint

  # Universal
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

## .pre-commit-hooks.yaml

Configuration file for hook authors defining available hooks.

### Complete Schema

```yaml
- id: hook-identifier
  name: Display Name
  description: Hook description
  entry: command-to-execute
  language: python
  files: '\\.py$'
  exclude: '^tests/'
  types: [python]
  types_or: [python, pyi]
  exclude_types: [markdown]
  stages: [pre-commit]
  minimum_pre_commit_version: '3.2.0'
  always_run: false
  pass_filenames: true
  require_serial: false
  verbose: false
```

### Hook Definition Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | **Yes** | Unique hook identifier |
| `name` | string | **Yes** | Display name during execution |
| `entry` | string | **Yes** | Command to execute |
| `language` | string | **Yes** | Hook language |
| `description` | string | No | Hook description |
| `files` | regex | No | File pattern to match |
| `exclude` | regex | No | File pattern to exclude |
| `types` | list | No | File types (AND) |
| `types_or` | list | No | File types (OR) |
| `exclude_types` | list | No | File types to exclude |
| `stages` | list | No | Default stages |
| `minimum_pre_commit_version` | string | No | Minimum version |
| `always_run` | bool | No | Run without files |
| `pass_filenames` | bool | No | Pass filenames to command |
| `require_serial` | bool | No | Prevent parallel execution |
| `verbose` | bool | No | Show output on success |

### Supported Languages

| Language | Description | Entry Point |
|----------|-------------|-------------|
| `python` | Python package | Console script or module |
| `node` | Node.js package | npm script |
| `ruby` | Ruby gem | Gem executable |
| `rust` | Rust crate | Cargo binary |
| `golang` | Go module | Go binary |
| `docker` | Docker container | Container entry |
| `docker_image` | Pre-built image | Image command |
| `system` | System command | Direct command |
| `script` | Shell script | Script path |

### Entry Point Patterns

**Python**:

```yaml
# Console script (from pyproject.toml)
entry: tool-name

# Module execution
entry: python -m module.name

# Script file
entry: scripts/hook.py
```

**Node**:

```yaml
# npm package binary
entry: prettier

# Direct script
entry: node scripts/hook.js
```

**System**:

```yaml
# System command
entry: grep -E pattern

# Custom script
entry: ./scripts/custom-check.sh
```

### Examples for Hook Authors

**Python Formatter Hook**:

```yaml
- id: my-formatter
  name: My Python Formatter
  description: Formats Python code to house style
  entry: my-formatter
  language: python
  types: [python]
  require_serial: true
```

**Commit Message Hook**:

```yaml
- id: commit-polish
  name: Polish Commit Message
  description: Rewrites commit messages to conventional format
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false
  always_run: true
  minimum_pre_commit_version: '3.2.0'
```

**Multi-File Validation**:

```yaml
- id: check-migrations
  name: Check Database Migrations
  description: Validates Django migrations
  entry: python -m migrations.check
  language: python
  files: 'migrations/.*\\.py$'
  pass_filenames: true
  require_serial: true
```

**System Command Hook**:

```yaml
- id: shellcheck
  name: ShellCheck
  description: Shell script analysis tool
  entry: shellcheck
  language: system
  types: [shell]
```

**Docker-Based Hook**:

```yaml
- id: hadolint
  name: Dockerfile Linter
  description: Lint Dockerfiles
  entry: hadolint/hadolint hadolint
  language: docker
  files: 'Dockerfile.*'
```

## Environment Variables

### During Hook Execution

| Variable | Description | Available In |
|----------|-------------|--------------|
| `PRE_COMMIT_COMMIT_MSG_SOURCE` | Message source (`message`, `template`, `merge`, `squash`, `commit`) | prepare-commit-msg |
| `PRE_COMMIT_COMMIT_OBJECT_NAME` | Commit SHA (for amend) | prepare-commit-msg |
| `PRE_COMMIT_FROM_REF` | Source ref | pre-push |
| `PRE_COMMIT_TO_REF` | Target ref | pre-push |
| `PRE_COMMIT_ORIGIN` | Remote name | post-checkout |
| `PRE_COMMIT_CHECKOUT_TYPE` | Checkout type | post-checkout |

### User Configuration

| Variable | Purpose |
|----------|---------|
| `SKIP` | Skip specific hooks: `SKIP=hook1,hook2 git commit` |
| `PRE_COMMIT_HOME` | Override cache location (default: `~/.cache/pre-commit`) |
| `PRE_COMMIT_COLOR` | Force color output: `always`, `never`, `auto` |

## Cache Management

Pre-commit caches hook environments for performance:

**Default location**: `~/.cache/pre-commit`

**Override location**:

```bash
export PRE_COMMIT_HOME=/custom/path
```

**Clean cache**:

```bash
# Remove unused environments
pre-commit gc

# Remove all environments
pre-commit clean
```

**Cache structure**:

```
~/.cache/pre-commit/
├── repo<hash>/
│   ├── <hook-env>/
│   └── ...
└── ...
```

## Advanced Patterns

### Local Hooks

Define hooks directly in repository without external dependency:

```yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run Tests
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true

      - id: mypy-strict
        name: Type Check (Strict)
        entry: uv run mypy --strict
        language: system
        types: [python]
        require_serial: true
```

### Meta Hooks

Pre-commit provides meta hooks for repository maintenance:

```yaml
repos:
  - repo: meta
    hooks:
      # Check hooks can be built
      - id: check-hooks-apply

      # Check useless excludes
      - id: check-useless-excludes
```

### Conditional Hooks

Use environment variables to conditionally skip hooks:

```yaml
hooks:
  - id: expensive-check
    name: Expensive Validation
    entry: bash -c 'if [ "$CI" != "true" ]; then expensive-check; fi'
    language: system
```

**Skip in CI**:

```bash
# In CI environment
export SKIP=expensive-check
```

## Validation

### Validate Configuration

```bash
# Validate .pre-commit-config.yaml
pre-commit validate-config

# Validate .pre-commit-config.yaml in another directory
pre-commit validate-config /path/to/.pre-commit-config.yaml

# Validate .pre-commit-hooks.yaml
pre-commit validate-manifest

# Validate specific manifest
pre-commit validate-manifest /path/to/.pre-commit-hooks.yaml
```

## Updating Hooks

### Auto-Update

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Update specific repository
pre-commit autoupdate --repo https://github.com/psf/black

# Freeze versions (add revs to config)
pre-commit autoupdate --freeze
```

### Manual Update

Edit `.pre-commit-config.yaml` and change `rev` values:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1  # Update this to latest tag
```

## Related Documentation

- [Installation Guide](./installation.md) - Setting up pre-commit
- [Usage Examples](./examples.md) - Real-world configurations
- [Official Schema](https://pre-commit.com/#pre-commit-configyaml---top-level) - Complete schema reference

## Additional Resources

- [Pre-commit Configuration](https://pre-commit.com/)
- [Creating Hooks](https://pre-commit.com/#creating-new-hooks)
- [Supported Languages](https://pre-commit.com/#supported-languages)
