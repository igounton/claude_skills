# Installation Guide

Complete installation instructions for using the pre-commit plugin and setting up pre-commit or prek in your projects.

## Installing the Plugin

### Option 1: Claude Code Marketplace

```bash
/plugin install pre-commit
```

### Option 2: Manual Installation

```bash
# Clone or copy plugin to Claude's plugin directory
git clone <repository-url> ~/.claude/plugins/pre-commit

# Reload plugins in Claude Code
/plugin reload

# Verify installation
/plugin list
```

## Installing Pre-commit Framework

You have two options for the pre-commit framework: the original Python-based tool or prek, a faster Rust-based alternative.

### Option A: pre-commit (Python-based)

**Using uv (Recommended)**

```bash
uv tool install pre-commit

# Verify installation
pre-commit --version
```

**Using pip**

```bash
pip install pre-commit

# Or install globally with pipx
pipx install pre-commit

# Verify installation
pre-commit --version
```

**Using package managers**

```bash
# macOS with Homebrew
brew install pre-commit

# Ubuntu/Debian
apt install pre-commit

# Arch Linux
pacman -S pre-commit
```

### Option B: prek (Rust-based)

**Using uv (Recommended)**

```bash
uv tool install prek

# Verify installation
prek --version
```

**Using pip**

```bash
pip install prek

# Verify installation
prek --version
```

**Using cargo**

```bash
cargo install prek

# Verify installation
prek --version
```

### Choosing Between pre-commit and prek

| Feature | pre-commit | prek |
|---------|-----------|------|
| **Speed** | Standard | Faster (Rust) |
| **Dependencies** | Requires Python | Standalone binary |
| **Compatibility** | Standard | Drop-in replacement |
| **Configuration** | `.pre-commit-config.yaml` | Same file |
| **CLI** | Standard | Identical |
| **Maturity** | Established | Newer |

**Recommendation**: Use prek if you want faster execution and don't want Python dependencies. Use pre-commit if you prefer the established, widely-adopted tool.

## Setting Up Hooks in Your Repository

### Quick Setup

```bash
# Navigate to your repository
cd /path/to/your/repo

# Create configuration (if not exists)
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
EOF

# Install hooks (using pre-commit)
pre-commit install

# Or using prek
prek install
```

### Installing Specific Hook Types

By default, only `pre-commit` stage hooks are installed. For other stages:

```bash
# Install prepare-commit-msg hooks (for message rewriting)
pre-commit install --hook-type prepare-commit-msg

# Install commit-msg hooks (for message validation)
pre-commit install --hook-type commit-msg

# Install pre-push hooks
pre-commit install --hook-type pre-push

# Install multiple types at once
pre-commit install --hook-type pre-commit --hook-type prepare-commit-msg
```

### Configuring Default Hook Types

To automatically install multiple hook types with `pre-commit install`:

```yaml
# .pre-commit-config.yaml
default_install_hook_types: [pre-commit, prepare-commit-msg]

repos:
  # ... your repos
```

Now `pre-commit install` (without arguments) installs both types.

### Install Options

```bash
# Install and download all hook environments immediately
pre-commit install --install-hooks

# Allow overwriting existing git hooks
pre-commit install --overwrite

# Install all configured hook types
pre-commit install --hook-type pre-commit \
                   --hook-type prepare-commit-msg \
                   --hook-type commit-msg \
                   --hook-type pre-push
```

## Verifying Installation

### Check Git Hooks

```bash
# List installed git hooks
ls -la .git/hooks/

# Check specific hook content
cat .git/hooks/pre-commit
cat .git/hooks/prepare-commit-msg
```

**Expected output in hook file**:
- For pre-commit: Contains "pre-commit.com"
- For prek: Contains "github.com/j178/prek"

### Test Hook Execution

```bash
# Run all hooks manually (on staged files only)
pre-commit run

# Run specific hook
pre-commit run trailing-whitespace

# Run on all files (use sparingly)
pre-commit run --all-files

# Run with verbose output
pre-commit run --verbose
```

### Verify Configuration

```bash
# Validate .pre-commit-config.yaml syntax
pre-commit validate-config

# Validate .pre-commit-hooks.yaml (for hook authors)
pre-commit validate-manifest
```

## Team Setup

### For Repository Maintainers

1. Create `.pre-commit-config.yaml` in repository root
2. Configure desired hooks and stages
3. Commit configuration to version control
4. Document setup in project README

```bash
# Add to README.md
echo "## Development Setup" >> README.md
echo "" >> README.md
echo "Install pre-commit hooks:" >> README.md
echo "\`\`\`bash" >> README.md
echo "pre-commit install" >> README.md
echo "\`\`\`" >> README.md
```

### For Team Members

```bash
# Clone repository
git clone <repo-url>
cd <repo>

# Install pre-commit tool (if not already installed)
uv tool install pre-commit

# Install hooks from repository config
pre-commit install

# Optionally: Download all hook environments immediately
pre-commit run --all-files
```

## CI/CD Setup

### GitHub Actions

```yaml
# .github/workflows/pre-commit.yml
name: pre-commit

on:
  pull_request:
  push:
    branches: [main]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - uses: pre-commit/action@v3.0.0
```

### GitLab CI

```yaml
# .gitlab-ci.yml
pre-commit:
  image: python:3.11
  before_script:
    - pip install pre-commit
  script:
    - pre-commit run --all-files
```

### Using pre-commit.ci

Add repository to [https://pre-commit.ci](https://pre-commit.ci) for automatic:
- Hook execution on pull requests
- Auto-fixing and committing simple issues
- Updating hook versions

## Uninstalling

### Remove Git Hooks

```bash
# Uninstall all pre-commit hooks
pre-commit uninstall

# Uninstall specific hook type
pre-commit uninstall --hook-type prepare-commit-msg
```

### Remove Tool

```bash
# If installed with uv
uv tool uninstall pre-commit

# If installed with pip
pip uninstall pre-commit

# If installed with pipx
pipx uninstall pre-commit

# If installed with package manager
brew uninstall pre-commit  # macOS
apt remove pre-commit      # Ubuntu/Debian
```

### Clean Cache

```bash
# Remove cached hook environments
pre-commit clean
pre-commit gc

# Or manually delete cache
rm -rf ~/.cache/pre-commit
```

## Troubleshooting Installation

### Pre-commit Command Not Found

**Cause**: Tool not in PATH

**Solutions**:

```bash
# Check if installed
which pre-commit

# If using uv, ensure tools are in PATH
uv tool update-shell

# Reload shell
exec $SHELL

# Or use absolute path
~/.local/bin/pre-commit --version
```

### Permission Denied

**Cause**: Git hooks not executable

**Solution**:

```bash
# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/prepare-commit-msg

# Or reinstall with --overwrite
pre-commit install --overwrite
```

### Hooks Already Exist

**Cause**: Existing git hooks in `.git/hooks/`

**Solution**:

```bash
# Option 1: Overwrite existing hooks
pre-commit install --overwrite

# Option 2: Backup and remove existing hooks
mv .git/hooks/pre-commit .git/hooks/pre-commit.backup
pre-commit install
```

### Python Version Mismatch

**Cause**: Hooks require specific Python version

**Solution**:

```yaml
# In .pre-commit-config.yaml, specify Python version
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
```

## Next Steps

After installation:

1. [Configure your hooks](./configuration.md) - Set up `.pre-commit-config.yaml`
2. [Review examples](./examples.md) - See common patterns and use cases
3. [Read the skill](../skills/pre-commit/SKILL.md) - Comprehensive framework documentation

## Additional Resources

- [Pre-commit Official Site](https://pre-commit.com/)
- [prek GitHub Repository](https://github.com/j178/prek)
- [Pre-commit Hook Collections](../skills/pre-commit/references/pre-commit-official-docs.md)
