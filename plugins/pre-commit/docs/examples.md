# Usage Examples

Real-world examples demonstrating common pre-commit patterns and use cases.

## Example 1: Python Project - Basic Setup

**Scenario**: Add code quality automation to a Python project using modern tools (Ruff, Black, mypy)

**Configuration**:

```yaml
# .pre-commit-config.yaml
repos:
  # Standard file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
        args: [--maxkb=1000]

  # Code formatting with Black
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  # Fast linting and fixing with Ruff
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  # Type checking with mypy
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-pyyaml]
```

**Setup**:

```bash
# Install pre-commit
uv tool install pre-commit

# Install hooks
pre-commit install

# Test on all files (first time)
pre-commit run --all-files
```

**Result**: Every commit automatically formats, lints, and type-checks Python code.

---

## Example 2: Commit Message Rewriting Hook

**Scenario**: Create a hook that transforms commit messages to conventional commits format using an LLM

### Hook Implementation

**Directory structure**:

```
commit-polish/
├── .pre-commit-hooks.yaml
├── pyproject.toml
├── README.md
└── src/
    └── commit_polish/
        ├── __init__.py
        └── hook.py
```

**Hook implementation** (`src/commit_polish/hook.py`):

```python
#!/usr/bin/env python3
"""Pre-commit hook for polishing commit messages."""
import os
import sys
from pathlib import Path


def main() -> int:
    """
    Entry point for prepare-commit-msg hook.

    Args received from pre-commit:
        sys.argv[1]: Path to commit message file

    Environment variables:
        PRE_COMMIT_COMMIT_MSG_SOURCE: Message source
        PRE_COMMIT_COMMIT_OBJECT_NAME: Commit SHA (amend only)

    Returns:
        0 on success, non-zero to abort commit
    """
    if len(sys.argv) < 2:
        print("Error: No commit message file provided", file=sys.stderr)
        return 1

    commit_msg_file = Path(sys.argv[1])
    source = os.environ.get('PRE_COMMIT_COMMIT_MSG_SOURCE', '')

    # Skip for merge commits or if source is commit (amend)
    if source in ('merge', 'commit'):
        return 0

    # Read current message
    try:
        original = commit_msg_file.read_text(encoding='utf-8')
    except OSError as e:
        print(f"Error reading commit message: {e}", file=sys.stderr)
        return 1

    # Skip empty messages
    if not original.strip():
        return 0

    # Transform message
    polished = polish_message(original)

    # Write transformed message
    try:
        commit_msg_file.write_text(polished, encoding='utf-8')
    except OSError as e:
        print(f"Error writing commit message: {e}", file=sys.stderr)
        return 1

    return 0


def polish_message(message: str) -> str:
    """
    Transform commit message to conventional commits format.

    Args:
        message: Original commit message

    Returns:
        Polished commit message
    """
    # In real implementation:
    # - Call LLM API to transform message
    # - Apply conventional commits format
    # - Ensure message follows standards

    # Simple example transformation
    lines = message.strip().split('\n')
    summary = lines[0]

    # Check if already conventional
    if any(summary.startswith(f"{type_}:") for type_ in [
        'feat', 'fix', 'docs', 'style', 'refactor',
        'perf', 'test', 'build', 'ci', 'chore'
    ]):
        return message

    # Infer type and reformat
    if 'test' in summary.lower():
        type_ = 'test'
    elif 'doc' in summary.lower():
        type_ = 'docs'
    elif 'fix' in summary.lower() or 'bug' in summary.lower():
        type_ = 'fix'
    else:
        type_ = 'feat'

    # Ensure summary is lowercase and imperative
    summary_clean = summary.strip().lower()
    if summary_clean.endswith('.'):
        summary_clean = summary_clean[:-1]

    polished = f"{type_}: {summary_clean}"

    # Preserve body if exists
    if len(lines) > 1:
        body = '\n'.join(lines[1:]).strip()
        if body:
            polished += f"\n\n{body}"

    return polished


if __name__ == "__main__":
    sys.exit(main())
```

**Hook definition** (`.pre-commit-hooks.yaml`):

```yaml
- id: commit-polish
  name: Polish Commit Message
  description: Transforms commit messages to conventional commits format
  entry: commit-polish
  language: python
  stages: [prepare-commit-msg]
  pass_filenames: false
  always_run: true
  minimum_pre_commit_version: '3.2.0'
```

**Package configuration** (`pyproject.toml`):

```toml
[project]
name = "commit-polish"
version = "1.0.0"
description = "Pre-commit hook for polishing commit messages"
requires-python = ">=3.8"

[project.scripts]
commit-polish = "commit_polish.hook:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### User Installation

**User's configuration** (`.pre-commit-config.yaml`):

```yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]

repos:
  - repo: https://github.com/your-org/commit-polish
    rev: v1.0.0
    hooks:
      - id: commit-polish
        stages: [prepare-commit-msg]
```

**Installation**:

```bash
# Install hooks (including prepare-commit-msg)
pre-commit install

# Test the hook
echo "fix bug in parser" > /tmp/test-msg
pre-commit try-repo /path/to/commit-polish commit-polish \
    --commit-msg-filename /tmp/test-msg
cat /tmp/test-msg
# Output: "fix: fix bug in parser"
```

**Result**: Commit messages automatically transformed before editor opens.

---

## Example 3: Multi-Language Monorepo

**Scenario**: Polyglot project with Python, TypeScript, Rust, and YAML files

**Configuration**:

```yaml
# .pre-commit-config.yaml
fail_fast: false

repos:
  # Universal file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: check-case-conflict

  # Python formatting and linting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        files: 'backend/.*\\.py$'

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]
        files: 'backend/.*\\.py$'

  # TypeScript/JavaScript formatting
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        files: 'frontend/.*\\.(ts|tsx|js|jsx|json)$'
        additional_dependencies:
          - prettier@3.1.0
          - '@trivago/prettier-plugin-sort-imports@4.3.0'

  # TypeScript linting
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: 'frontend/.*\\.[jt]sx?$'
        types: [file]
        additional_dependencies:
          - eslint@8.56.0
          - '@typescript-eslint/eslint-plugin@6.0.0'
          - '@typescript-eslint/parser@6.0.0'

  # Rust formatting and linting
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
        args: [--manifest-path, rust-service/Cargo.toml, --]
      - id: clippy
        args:
          - --manifest-path=rust-service/Cargo.toml
          - --
          - -D
          - warnings

  # YAML linting
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint
        args: [-c=.yamllint.yml]
```

**Directory structure**:

```
monorepo/
├── .pre-commit-config.yaml
├── backend/           # Python
├── frontend/          # TypeScript
├── rust-service/      # Rust
└── config/            # YAML
```

**Result**: All languages formatted consistently with appropriate tools.

---

## Example 4: Security and Quality Checks

**Scenario**: Add security scanning and advanced quality checks before commits

**Configuration**:

```yaml
repos:
  # Detect secrets and credentials
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
        exclude: 'package-lock\\.json'

  # Check for security issues in Python
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ['bandit[toml]']

  # Detect common security issues
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
        args: [--maxkb=500]

  # Check dependencies for known vulnerabilities
  - repo: local
    hooks:
      - id: pip-audit
        name: Audit Python Dependencies
        entry: uv run pip-audit
        language: system
        files: 'requirements.*\\.txt$|pyproject\\.toml$'
        pass_filenames: false
```

**Initialize secrets baseline**:

```bash
# Create baseline of known false positives
detect-secrets scan > .secrets.baseline

# Review and audit baseline
detect-secrets audit .secrets.baseline
```

**Result**: Security issues detected before code is committed.

---

## Example 5: Testing Workflow

**Scenario**: Run different test suites at different stages

**Configuration**:

```yaml
default_install_hook_types: [pre-commit, pre-push]

repos:
  # Fast unit tests on pre-commit
  - repo: local
    hooks:
      - id: pytest-unit
        name: Run Unit Tests
        entry: uv run pytest tests/unit -v
        language: system
        types: [python]
        pass_filenames: false
        stages: [pre-commit]

      # Slower integration tests on pre-push
      - id: pytest-integration
        name: Run Integration Tests
        entry: uv run pytest tests/integration -v
        language: system
        pass_filenames: false
        stages: [pre-push]

      # Full test suite with coverage (manual only)
      - id: pytest-full
        name: Run Full Test Suite with Coverage
        entry: uv run pytest --cov=src --cov-report=html
        language: system
        pass_filenames: false
        stages: [manual]
```

**Installation**:

```bash
# Install both pre-commit and pre-push hooks
pre-commit install --hook-type pre-commit --hook-type pre-push
```

**Usage**:

```bash
# Unit tests run automatically on commit
git commit -m "feat: add feature"

# Integration tests run automatically on push
git push

# Full test suite run manually
pre-commit run pytest-full --hook-stage manual
```

**Result**: Fast feedback loop with appropriate testing at each stage.

---

## Example 6: Documentation and Changelog Automation

**Scenario**: Ensure documentation stays up-to-date and changelog is maintained

**Configuration**:

```yaml
repos:
  # Markdown formatting
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        files: '\\.md$'

  # Markdown linting
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args: [--fix]

  # Check documentation links
  - repo: https://github.com/tcort/markdown-link-check
    rev: v3.11.2
    hooks:
      - id: markdown-link-check
        args: [--config, .markdown-link-check.json]

  # Ensure CHANGELOG updated
  - repo: local
    hooks:
      - id: changelog-updated
        name: Check CHANGELOG Updated
        entry: bash -c 'git diff --cached --name-only | grep -q CHANGELOG.md || (echo "CHANGELOG.md not updated" && exit 1)'
        language: system
        pass_filenames: false
        always_run: true
```

**Markdown link check config** (`.markdown-link-check.json`):

```json
{
  "ignorePatterns": [
    {
      "pattern": "^https://localhost"
    }
  ],
  "timeout": "20s",
  "retryOn429": true
}
```

**Result**: Documentation quality enforced and changelog kept current.

---

## Example 7: Container and Infrastructure

**Scenario**: Lint Dockerfiles and validate infrastructure-as-code

**Configuration**:

```yaml
repos:
  # Dockerfile linting
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker

  # Terraform formatting
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.85.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint

  # Kubernetes manifest validation
  - repo: local
    hooks:
      - id: kubeval
        name: Validate Kubernetes Manifests
        entry: kubeval
        language: system
        files: 'k8s/.*\\.ya?ml$'
        pass_filenames: true

  # Docker Compose validation
  - repo: local
    hooks:
      - id: docker-compose-check
        name: Validate Docker Compose
        entry: docker compose -f docker-compose.yml config --quiet
        language: system
        files: 'docker-compose\\.ya?ml$'
        pass_filenames: false
```

**Result**: Infrastructure code validated before commits.

---

## Example 8: Conditional Execution

**Scenario**: Run expensive checks only in CI, skip locally

**Configuration**:

```yaml
repos:
  - repo: local
    hooks:
      # Always run locally and in CI
      - id: quick-lint
        name: Quick Linting
        entry: ruff check src/
        language: system
        pass_filenames: false

      # Only in CI
      - id: expensive-typecheck
        name: Full Type Checking
        entry: bash -c 'if [ "$CI" = "true" ]; then mypy --strict src/; else echo "Skipped locally"; fi'
        language: system
        pass_filenames: false
        verbose: true
```

**Skip locally**:

```bash
# Skip specific hook
SKIP=expensive-typecheck git commit -m "message"

# Skip all checks (emergency only)
git commit --no-verify -m "message"
```

**Result**: Fast local commits, thorough CI validation.

---

## Example 9: Working with Large Files

**Scenario**: Use Git LFS for large files and validate sizes

**Configuration**:

```yaml
repos:
  # Ensure large files tracked with LFS
  - repo: local
    hooks:
      - id: check-lfs
        name: Check Large Files Use LFS
        entry: bash -c 'git lfs ls-files | grep -q . || (echo "Large files not tracked with LFS" && exit 1)'
        language: system
        pass_filenames: false

  # Prevent accidentally committing large files
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: [--maxkb=100]
        exclude: '\\.lfs$'

  # Check LFS pointers valid
  - repo: local
    hooks:
      - id: lfs-verify
        name: Verify LFS Pointers
        entry: git lfs fsck
        language: system
        pass_filenames: false
        stages: [pre-push]
```

**Setup LFS**:

```bash
# Install Git LFS
git lfs install

# Track large file types
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "*.zip"

# Commit .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS"
```

**Result**: Large files managed properly with LFS.

---

## Example 10: Custom Project-Specific Checks

**Scenario**: Enforce project-specific conventions

**Configuration**:

```yaml
repos:
  - repo: local
    hooks:
      # Ensure all Python files have copyright header
      - id: check-copyright
        name: Check Copyright Headers
        entry: python scripts/check_copyright.py
        language: system
        types: [python]

      # Validate API schema changes
      - id: validate-openapi
        name: Validate OpenAPI Schema
        entry: bash -c 'openapi-generator validate -i api/openapi.yaml'
        language: system
        files: 'api/openapi\\.yaml$'
        pass_filenames: false

      # Check migration files sequential
      - id: check-migrations
        name: Check Migration Numbers Sequential
        entry: python scripts/check_migrations.py
        language: system
        files: 'migrations/.*\\.py$'
        pass_filenames: false

      # Ensure no print statements in production code
      - id: no-print-statements
        name: No Print Statements in Production
        entry: bash -c 'grep -rn "print(" src/ && exit 1 || exit 0'
        language: system
        files: 'src/.*\\.py$'
```

**Custom script example** (`scripts/check_copyright.py`):

```python
#!/usr/bin/env python3
"""Check that Python files have copyright headers."""
import sys
from pathlib import Path

REQUIRED_HEADER = "# Copyright (c) 2024 Company Name"


def main() -> int:
    """Check files for copyright header."""
    missing = []

    for filepath in sys.argv[1:]:
        path = Path(filepath)
        content = path.read_text()

        if REQUIRED_HEADER not in content:
            missing.append(filepath)

    if missing:
        print("Missing copyright header in:")
        for file in missing:
            print(f"  {file}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Result**: Project conventions automatically enforced.

---

## Testing Hooks

### Test Locally Before Distribution

```bash
# Test hook from local repository
cd /path/to/hook-repo
pre-commit try-repo . hook-id --verbose

# Test with commit message file
echo "test message" > /tmp/test-msg
pre-commit try-repo . commit-polish \
    --commit-msg-filename /tmp/test-msg
cat /tmp/test-msg

# Test on specific files
pre-commit try-repo . hook-id \
    --files src/file1.py src/file2.py

# Test all hooks
pre-commit try-repo . --all-hooks
```

### Debug Hook Execution

```bash
# Run with verbose output
pre-commit run hook-id --verbose --files path/to/file.py

# Run with debug logging
PRE_COMMIT_COLOR=always pre-commit run --verbose --all-files

# Check hook environment
pre-commit run hook-id --verbose 2>&1 | grep -A 10 "hook environment"
```

## Best Practices from Examples

1. **Use specific file patterns**: `files: 'src/.*\\.py$'` not `files: '\\.py$'`
2. **Set `pass_filenames: false`** for message hooks and hooks that don't need file paths
3. **Use `always_run: true`** for hooks that must run even without matching files
4. **Set `require_serial: true`** for hooks that can't run in parallel
5. **Use `stages` appropriately**: Fast checks on `pre-commit`, slow on `pre-push`
6. **Test hooks with `try-repo`** before distributing
7. **Use `local` repos** for project-specific scripts
8. **Provide `verbose: true`** for hooks where output is always useful

## Additional Resources

- [Configuration Reference](./configuration.md) - Complete configuration schemas
- [Installation Guide](./installation.md) - Setup instructions
- [Pre-commit Official Examples](https://pre-commit.com/#usage)
