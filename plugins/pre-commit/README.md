# Pre-commit Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A Claude Code plugin providing comprehensive guidance for implementing git hooks automation using the pre-commit framework. Enables automated code quality checks, formatting, linting, and commit message processing across multi-language projects.

## Features

- **Git Hooks Automation**: Configure pre-commit, prepare-commit-msg, commit-msg, and other git hook stages
- **Commit Message Processing**: Implement hooks that rewrite or validate commit messages
- **Multi-Language Support**: Python, JavaScript, TypeScript, Rust, Go, and more
- **Alternative Implementation**: Support for both pre-commit (Python) and prek (Rust) tools
- **Hook Distribution**: Create and distribute custom hooks as pre-commit repositories
- **Common Patterns**: Ready-to-use configurations for formatters, linters, and validators
- **Troubleshooting**: Solutions for common hook installation and execution issues

## Installation

### Prerequisites

- Claude Code 2.1 or later
- Git 2.24+ (for advanced hook stages)

### Install Plugin

```bash
# Method 1: From Claude Code Marketplace (if available)
/plugin install pre-commit

# Method 2: Manual installation
git clone <repository-url> ~/.claude/plugins/pre-commit
/plugin reload
```

## Quick Start

The skill activates automatically when Claude detects you're working with git hooks or pre-commit configurations:

```
"Set up pre-commit hooks for Python formatting"
"Configure prepare-commit-msg hook to rewrite commit messages"
"Fix issue where pre-commit hooks aren't running"
```

You can also explicitly activate the skill:

```
@pre-commit
```

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | pre-commit | Git hooks automation using pre-commit framework. Covers hook stages, configuration, implementation patterns, and troubleshooting. | Auto-activated or `@pre-commit` |

## Usage

### Core Use Cases

**1. Setting Up Git Hooks**

Claude will guide you through:
- Installing pre-commit or prek tools
- Creating `.pre-commit-config.yaml` configuration
- Installing hooks for specific stages (pre-commit, prepare-commit-msg, etc.)
- Configuring default hook types

**2. Implementing Commit Message Hooks**

The skill provides complete guidance for:
- Creating `prepare-commit-msg` hooks that modify commit messages
- Understanding hook arguments and environment variables
- Configuring `pass_filenames` and `always_run` correctly
- Implementing Python entry points and hook definitions

**3. Configuring Code Quality Hooks**

Get configurations for:
- Language-specific formatters (Black, Prettier, rustfmt)
- Linters (Ruff, ESLint, Clippy)
- Standard checks (trailing whitespace, YAML validation)
- Multi-stage workflows

**4. Troubleshooting**

Claude can help debug:
- Hooks not running during commits
- Incorrect argument passing to hooks
- Hook execution order issues
- Cache and environment problems

### Key Concepts

**Hook Stages**

The skill covers all pre-commit stages:
- `pre-commit` - Before commit creation (formatting, linting)
- `prepare-commit-msg` - Before message editor (message rewriting)
- `commit-msg` - After message written (validation only)
- `pre-push` - Before push to remote (integration tests)
- Additional stages: pre-merge-commit, post-checkout, post-commit, post-merge, manual

**Critical Distinction**

The skill emphasizes the difference between:
- `prepare-commit-msg` - Can modify commit messages
- `commit-msg` - Can only validate (cannot modify)

### Related Skills

The pre-commit skill integrates with:

- **conventional-commits**: Commit message format standards
- **commitlint**: Commit message validation rules

These related skills are referenced within the pre-commit documentation for comprehensive commit workflow guidance.

## Configuration

The skill provides guidance on two configuration files:

**1. `.pre-commit-config.yaml`** (User Repository)

Defines which hooks to use in your project:

```yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
```

**2. `.pre-commit-hooks.yaml`** (Hook Definition)

Defines hooks for distribution to other users:

```yaml
- id: commit-polish
  name: Polish Commit Message
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false
  always_run: true
```

See [docs/configuration.md](./docs/configuration.md) for complete configuration reference.

## Examples

### Example 1: Set Up Python Project Hooks

**Scenario**: Add automated formatting and linting to a Python project

**Steps**:
1. Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
```

2. Install hooks:

```bash
uv tool install pre-commit
pre-commit install
```

3. Test:

```bash
# Run on staged files
pre-commit run

# Run on specific files
pre-commit run --files src/module.py
```

**Result**: Code automatically formatted and linted before each commit.

---

### Example 2: Implement Commit Message Rewriting Hook

**Scenario**: Create a hook that transforms commit messages to conventional commits format

**Steps**:
1. Create hook implementation (`src/tool/hook.py`):

```python
#!/usr/bin/env python3
import sys

def main() -> int:
    if len(sys.argv) < 2:
        return 1

    commit_msg_file = sys.argv[1]

    with open(commit_msg_file, encoding='utf-8') as f:
        message = f.read()

    if not message.strip():
        return 0

    # Transform message
    new_message = transform_to_conventional(message)

    with open(commit_msg_file, 'w', encoding='utf-8') as f:
        f.write(new_message)

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

2. Define hook (`.pre-commit-hooks.yaml`):

```yaml
- id: commit-polish
  name: Polish Commit Message
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false
  always_run: true
```

3. Configure entry point (`pyproject.toml`):

```toml
[project.scripts]
commit-polish = "tool.hook:main"
```

4. Users install from your repository:

```yaml
# User's .pre-commit-config.yaml
repos:
  - repo: https://github.com/your-org/commit-polish
    rev: v1.0.0
    hooks:
      - id: commit-polish
        stages: [prepare-commit-msg]
```

**Result**: Commit messages automatically transformed before editor opens.

---

### Example 3: Multi-Language Formatting

**Scenario**: Set up formatting for Python, JavaScript, and YAML in a polyglot project

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
        types_or: [javascript, jsx, ts, tsx]

  # YAML
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
```

**Result**: All languages formatted consistently with their respective tools.

See [docs/examples.md](./docs/examples.md) for more detailed examples.

## Troubleshooting

### Hook Not Running

**Symptoms**: Hook configured but doesn't execute during commits

**Solutions**:
1. Verify hook type is installed: `ls -la .git/hooks/prepare-commit-msg`
2. Install specific hook type: `pre-commit install --hook-type prepare-commit-msg`
3. Add to `default_install_hook_types` in config

### Hook Receives Wrong Arguments

**Symptoms**: Message hook receives staged filenames instead of message file path

**Solution**: Set `pass_filenames: false` for message-related hooks:

```yaml
hooks:
  - id: commit-polish
    stages: [prepare-commit-msg]
    pass_filenames: false
```

### Hook Skipped

**Symptoms**: Hook doesn't run when no files match patterns

**Solution**: Set `always_run: true`:

```yaml
hooks:
  - id: commit-polish
    always_run: true
```

## Documentation

- [Installation Guide](./docs/installation.md) - Detailed installation instructions
- [Configuration Reference](./docs/configuration.md) - Complete configuration schemas
- [Usage Examples](./docs/examples.md) - Real-world implementation patterns
- [Official Docs](./skills/pre-commit/references/pre-commit-official-docs.md) - Links to pre-commit documentation

## Version Requirements

| Component | Minimum Version | Notes |
|-----------|----------------|-------|
| Claude Code | 2.1 | Skills framework support |
| pre-commit | 3.2.0 | Stage names match hook names |
| Python | 3.8+ | For pre-commit framework |
| Git | 2.24+ | For pre-merge-commit stage |

## Alternative: prek

The skill also covers **prek**, a Rust-based reimplementation of pre-commit:

- Faster execution (Rust vs Python)
- No Python dependency required
- Drop-in replacement (same `.pre-commit-config.yaml`)
- Identical CLI interface

Install with: `uv tool install prek` or `cargo install prek`

## Credits

This plugin provides guidance based on:
- [Pre-commit Official Documentation](https://pre-commit.com/)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [prek Project](https://github.com/j178/prek)

## License

[License information would go here]
