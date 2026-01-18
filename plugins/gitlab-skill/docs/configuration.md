# Configuration Guide

This guide covers setup and customization options for the gitlab-skill plugin.

---

## Table of Contents

- [Environment Variables](#environment-variables)
- [GitLab Authentication](#gitlab-authentication)
- [gitlab-ci-local Configuration](#gitlab-ci-local-configuration)
- [glab CLI Configuration](#glab-cli-configuration)
- [Validation Tools](#validation-tools)
- [Documentation Sync](#documentation-sync)
- [Plugin Settings](#plugin-settings)

---

## Environment Variables

### Core Variables

| Variable | Required | Scope | Description |
|----------|----------|-------|-------------|
| `GITLAB_TOKEN` | For commands and validation | Personal | Personal access token with `api` scope |
| `GL_TOKEN` | Alternative | Personal | Alternative to GITLAB_TOKEN |
| `CI_JOB_TOKEN` | Automatic in CI | CI/CD | Provided automatically by GitLab CI/CD |
| `CI_PUBLISH_TOKEN` | For publishing | CI/CD | Created by /setup-ci-publish-token command |

### Setting Environment Variables

#### Temporary (Current Session)

```bash
export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
export GL_TOKEN=glpat-xxxxxxxxxxxx
```

#### Persistent (Shell Profile)

```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
echo 'export GITLAB_TOKEN=glpat-xxxxxxxxxxxx' >> ~/.bashrc
source ~/.bashrc
```

#### Project-Specific (.env file)

```bash
# Create .env in project root
cat > .env <<EOF
GITLAB_TOKEN=glpat-xxxxxxxxxxxx
GITLAB_HOST=gitlab.com
CI_PROJECT_PATH=username/repository
GITLAB_USER_ID=12345
EOF

# Add to .gitignore
echo ".env" >> .gitignore
```

The /setup-ci-publish-token command automatically creates and manages the `.env` file.

---

## GitLab Authentication

### Personal Access Tokens

#### Creating a Personal Access Token

1. Go to GitLab profile settings
2. Navigate to **Access Tokens**
3. Click **Add new token**
4. Configure:
   - **Name**: "Claude Code GitLab Skill"
   - **Expiration**: Set as needed (recommend 1 year)
   - **Scopes**:
     - `api` (required for full API access)
     - `read_repository` (for reading repository data)
     - `write_repository` (if modifying repositories)
5. Click **Create personal access token**
6. Copy the token immediately (shown only once)

#### Token Scopes Explained

| Scope | Purpose | Required For |
|-------|---------|--------------|
| `api` | Full API access | /setup-ci-publish-token, glab operations, GLFM validation |
| `read_repository` | Read repository contents | gitlab-ci-local, repository operations |
| `write_repository` | Write to repository | Creating releases, pushing changes |
| `read_api` | Read-only API access | Alternative to `api` for read-only operations |

#### Security Best Practices

1. **Use minimal scopes** - Only grant permissions you need
2. **Set expiration dates** - Rotate tokens regularly
3. **Store securely** - Never commit tokens to repositories
4. **Use CI variables** - For CI/CD operations, use project access tokens via CI variables
5. **Audit regularly** - Review active tokens in GitLab settings

### Project Access Tokens

Created by the /setup-ci-publish-token command. These tokens:
- Are scoped to specific projects
- Have configurable access levels (Guest to Owner)
- Can be managed programmatically
- Expire after set duration (plugin creates 1-year tokens)

See [/setup-ci-publish-token](./commands.md#setup-ci-publish-token) for details.

---

## gitlab-ci-local Configuration

### Installation

```bash
# Install globally via npm
npm install -g gitlab-ci-local

# Verify installation
gitlab-ci-local --version
```

### Global Configuration

Create `$HOME/.gitlab-ci-local/variables.yml`:

```yaml
# Authentication
GITLAB_TOKEN: glpat-xxxxxxxxxxxx

# GitLab instance
CI_SERVER_URL: https://gitlab.com

# Common variables
CI_SERVER_HOST: gitlab.com
CI_PROJECT_DIR: /builds/project
```

**Location**: `~/.gitlab-ci-local/variables.yml`

**Purpose**: Global variables available to all local pipeline runs

### Project Configuration

Create `.gitlab-ci-local-variables.yml` in project root:

```yaml
# Project-specific variables
PROJECT_NAME: my-project
DEPLOY_ENV: staging
CACHE_KEY: ${CI_COMMIT_REF_SLUG}

# Override global variables
CI_PROJECT_DIR: /custom/path
```

**Location**: `./.gitlab-ci-local-variables.yml`

**Purpose**: Project-specific variables that override global config

**Git**: Add to `.gitignore` if it contains secrets:

```bash
echo ".gitlab-ci-local-variables.yml" >> .gitignore
```

### Docker Configuration

gitlab-ci-local runs jobs in Docker containers. Ensure Docker is installed and running:

```bash
# Check Docker status
docker info

# Start Docker (if not running)
# macOS: Open Docker Desktop
# Linux: sudo systemctl start docker
```

### Authentication with Private Registries

For private Docker registries or GitLab Container Registry:

```yaml
# In ~/.gitlab-ci-local/variables.yml
CI_REGISTRY: registry.gitlab.com
CI_REGISTRY_USER: username
CI_REGISTRY_PASSWORD: glpat-xxxxxxxxxxxx
```

Then login before running gitlab-ci-local:

```bash
echo "$CI_REGISTRY_PASSWORD" | docker login $CI_REGISTRY -u $CI_REGISTRY_USER --password-stdin
```

### Common Configuration Issues

#### Issue: Jobs fail with "cannot pull image"

**Solution**: Login to Docker registry:

```bash
docker login registry.gitlab.com
# Or use CI_REGISTRY_PASSWORD from variables
```

#### Issue: Variables not accessible in jobs

**Solution**: Check variable precedence:
1. `.gitlab-ci-local-variables.yml` (project)
2. `~/.gitlab-ci-local/variables.yml` (global)
3. `.gitlab-ci.yml` `variables:` section

#### Issue: Artifacts not generated

**Solution**: Check artifacts are written to correct path and `.gitlab-ci-local/artifacts/` directory permissions.

---

## glab CLI Configuration

### Installation

```bash
# macOS
brew install glab

# Linux - Debian/Ubuntu
sudo apt install glab

# Linux - Fedora/RHEL
sudo dnf install glab

# From binary
# Download from: https://gitlab.com/gitlab-org/cli/-/releases
```

### Authentication

#### Interactive Login

```bash
glab auth login
```

Follow prompts to authenticate:
1. Choose GitLab instance (gitlab.com or self-hosted)
2. Choose authentication method:
   - Web browser (recommended)
   - Personal access token (paste token)
3. Choose default git protocol (HTTPS recommended)

#### Token-Based Login

```bash
# Using environment variable
export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
glab auth status

# Using command flag
glab auth login --hostname gitlab.com --token glpat-xxxxxxxxxxxx
```

### Configuration File

glab stores configuration in `~/.config/glab-cli/config.yml`:

```yaml
hosts:
  gitlab.com:
    token: glpat-xxxxxxxxxxxx
    git_protocol: https
    api_protocol: https
```

### Default Settings

```bash
# Set default GitLab instance
glab config set host gitlab.com

# Set default git protocol
glab config set git_protocol https

# Set default API protocol
glab config set api_protocol https

# View all settings
glab config get
```

### Multiple GitLab Instances

```bash
# Login to self-hosted instance
glab auth login --hostname gitlab.example.com

# Use specific host for commands
glab ci get --hostname gitlab.example.com

# Set default host
glab config set host gitlab.example.com
```

---

## Validation Tools

### validate-glfm.py

Python script that validates GitLab Flavored Markdown rendering via GitLab API.

#### Requirements

```bash
# Install dependencies
uv pip install requests

# Or use uv run (installs automatically)
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --help
```

#### Configuration

The script uses `GITLAB_TOKEN` environment variable:

```bash
export GITLAB_TOKEN=glpat-xxxxxxxxxxxx
```

Or create `.env` file:

```bash
echo "GITLAB_TOKEN=glpat-xxxxxxxxxxxx" > .env
```

#### Usage

```bash
# Validate file
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file README.md

# Validate inline markdown
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py \
  --markdown "> [!note]\n> Test alert"

# Save rendered HTML
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py \
  --file test.md --output rendered.html

# Verbose debugging
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py \
  --file test.md --verbose
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--file` | `-f` | Path to markdown file | - |
| `--markdown` | `-m` | Inline markdown string | - |
| `--output` | `-o` | Save HTML to file | stdout |
| `--verbose` | `-v` | Enable debug logging | False |

#### Exit Codes

- `0` - Success
- `1` - Validation error or API failure
- `2` - Missing GITLAB_TOKEN

---

## Documentation Sync

### sync-gitlab-docs.py

Synchronizes GitLab CI/CD documentation from official repository.

#### Usage

```bash
# Update documentation (respects 3-day cooldown)
uv run scripts/sync-gitlab-docs.py --working-dir .

# Force update (bypass cooldown)
uv run scripts/sync-gitlab-docs.py --working-dir . --force

# Dry run (show what would be updated)
uv run scripts/sync-gitlab-docs.py --working-dir . --dry-run
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--working-dir` | Skill directory path | Required |
| `--force` | Bypass cooldown check | False |
| `--dry-run` | Show changes without applying | False |

#### Cooldown System

The script maintains a lock file: `.sync-gitlab-docs.lock`

```json
{
  "last_successful_run": "2025-01-18T10:30:00Z",
  "last_run_status": "success",
  "cooldown_hours": 72
}
```

- **Cooldown period**: 72 hours (3 days) after successful run
- **Bypass**: Use `--force` flag or delete lock file
- **Failed runs**: Do not trigger cooldown

#### What Gets Synced

The script synchronizes:
1. GitLab CI/CD documentation markdown files
2. Directory structure and navigation
3. Documentation index in SKILL.md

**Source**: [GitLab Documentation Repository](https://gitlab.com/gitlab-org/gitlab/-/tree/master/doc/ci)

**Destination**: `./references/ci/`

#### Execution Protocol

The gitlab-skill automatically runs sync-gitlab-docs.py on first activation each session. The cooldown prevents excessive API calls.

---

## Plugin Settings

### Installation Scopes

The plugin can be installed at different scopes:

| Scope | Settings File | Use Case |
|-------|---------------|----------|
| `user` | `~/.claude/settings.json` | Personal, global (default) |
| `project` | `.claude/settings.json` | Team, shared via git |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |

### Enable/Disable Plugin

```bash
# Enable plugin
/plugin enable gitlab-skill

# Disable plugin
/plugin disable gitlab-skill

# Check status
/plugin list
```

### Plugin Directory Structure

```text
~/.claude/plugins/gitlab-skill/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   ├── setup-ci-publish-token.md
│   └── setup-ci-publish-token.sh
├── skills/
│   └── gitlab-skill/
│       ├── SKILL.md              # Main skill definition
│       ├── scripts/              # Utility scripts
│       └── references/           # Reference documentation
└── docs/                         # User documentation (this file)
```

### Customization

#### Override Skill Description

Create `.claude/settings.json` (project) or `~/.claude/settings.json` (user):

```json
{
  "skills": {
    "gitlab-skill": {
      "description": "Custom description for when to activate this skill"
    }
  }
}
```

#### Disable Automatic Activation

```json
{
  "skills": {
    "gitlab-skill": {
      "disable-model-invocation": true
    }
  }
}
```

The skill will only activate when explicitly invoked via `/gitlab-skill` or `@gitlab-skill`.

---

## Troubleshooting Configuration

### Plugin Not Loading

**Symptoms**: Skill doesn't activate, command not found

**Diagnosis**:

```bash
# Check plugin installation
/plugin list

# Check plugin directory
ls -la ~/.claude/plugins/gitlab-skill

# Check skill file
ls -la ~/.claude/plugins/gitlab-skill/skills/gitlab-skill/SKILL.md
```

**Solution**:
1. Ensure plugin is installed: `/plugin install gitlab-skill`
2. Reload plugins: `/plugin reload`
3. Check file permissions: `chmod -R 755 ~/.claude/plugins/gitlab-skill`

---

### Authentication Failures

**Symptoms**: API errors, 401 Unauthorized, permission denied

**Diagnosis**:

```bash
# Check token is set
echo $GITLAB_TOKEN

# Test token with glab
glab auth status

# Check token scopes
glab api personal_access_tokens/self | jq '.scopes'
```

**Solution**:
1. Verify `GITLAB_TOKEN` is set correctly
2. Ensure token has required scopes (api, read_repository)
3. Check token hasn't expired: GitLab Settings > Access Tokens
4. Regenerate token if needed

---

### gitlab-ci-local Not Finding Variables

**Symptoms**: Jobs fail with "variable not defined"

**Diagnosis**:

```bash
# Check variable files exist
ls -la ~/.gitlab-ci-local/variables.yml
ls -la .gitlab-ci-local-variables.yml

# Preview configuration
gitlab-ci-local --preview
```

**Solution**:
1. Create `~/.gitlab-ci-local/variables.yml` with global variables
2. Create `.gitlab-ci-local-variables.yml` with project variables
3. Verify YAML syntax: `yamllint ~/.gitlab-ci-local/variables.yml`
4. Check variable precedence (project overrides global)

---

### glab Commands Fail

**Symptoms**: "not logged in", "configuration error"

**Diagnosis**:

```bash
# Check authentication status
glab auth status

# Check configuration
cat ~/.config/glab-cli/config.yml

# Test API access
glab api user
```

**Solution**:
1. Authenticate: `glab auth login`
2. Verify host: `glab config get host`
3. Check token in config.yml is valid
4. Re-authenticate if needed

---

### GLFM Validation Fails

**Symptoms**: validate-glfm.py errors, "token not found"

**Diagnosis**:

```bash
# Check GITLAB_TOKEN
echo $GITLAB_TOKEN

# Test script manually
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py \
  --markdown "# Test" --verbose
```

**Solution**:
1. Set `GITLAB_TOKEN` environment variable
2. Ensure token has `api` scope
3. Check GitLab API is accessible: `curl https://gitlab.com/api/v4/user` -H "PRIVATE-TOKEN: $GITLAB_TOKEN"`
4. Verify network connectivity

---

## Next Steps

- [Skills Reference](./skills.md) - Learn about skill capabilities
- [Commands Reference](./commands.md) - Slash command usage
- [Examples](./examples.md) - Real-world usage patterns
- [README](../README.md) - Plugin overview

---

## Back to Documentation

- [README](../README.md) - Plugin overview and quick start
- [Skills Reference](./skills.md) - Skill capabilities and domains
- [Commands Reference](./commands.md) - Slash command usage
- [Examples](./examples.md) - Real-world usage patterns
