# GitLab Skill Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive Claude Code plugin for GitLab CI/CD pipeline configuration, GitLab Flavored Markdown documentation, local pipeline testing, and GitLab CLI operations.

## Features

- **CI/CD Pipeline Configuration** - Expert guidance for .gitlab-ci.yml creation, optimization, and debugging
- **GitLab Flavored Markdown (GLFM)** - Complete GLFM syntax support with validation tooling
- **Local Pipeline Testing** - gitlab-ci-local integration for testing pipelines before push
- **GitLab CLI (glab)** - Non-interactive CLI operations for automation and scripting
- **Automated CI Token Setup** - Slash command for creating project access tokens with proper scoping
- **Documentation Sync** - Automatic updates from official GitLab CI/CD documentation

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- GitLab account (for CI/CD features)
- `glab` CLI installed (for command features)
- `gitlab-ci-local` installed (for local testing features)
- Python 3.x with `requests` library (for GLFM validation)

### Install Plugin

```bash
# Add marketplace (if not already added)
cd /home/user/claude_skills
/plugin marketplace add local-plugins

# Install gitlab-skill plugin
/plugin install gitlab-skill@local-plugins
```

### Manual Installation

```bash
# Clone or copy to Claude plugins directory
cp -r /home/user/claude_skills/plugins/gitlab-skill ~/.claude/plugins/
cc plugin reload
```

## Quick Start

### CI/CD Pipeline Optimization

When working on `.gitlab-ci.yml` files, the skill automatically activates and provides:

- Caching strategy recommendations
- Job parallelization suggestions
- Docker-in-Docker optimization patterns
- GitLab CI Steps composition guidance

```yaml
# Example: Optimized pipeline with caching
stages:
  - build
  - test

build:
  stage: build
  script:
    - npm ci
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
```

### GLFM Documentation

Create GitLab-compatible markdown with validated syntax:

```markdown
> [!note]
> Alert blocks must use lowercase syntax

<details><summary>Collapsible Section</summary>

Content here
</details>
```

### Local Pipeline Testing

Test CI/CD changes before pushing:

```bash
# List all jobs
gitlab-ci-local --list

# Run specific job
gitlab-ci-local build

# Preview parsed configuration
gitlab-ci-local --preview
```

### Setup CI Publishing Token

Quickly configure project access tokens for CI/CD operations:

```bash
/setup-ci-publish-token
```

This command creates a project access token with appropriate permissions and adds it as a masked, protected CI variable.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | gitlab-skill | CI/CD pipeline configuration, GLFM syntax, local testing, and glab CLI integration | Auto-invoked by Claude |
| Command | /setup-ci-publish-token | Create GitLab project access token for CI/CD publishing | User types `/setup-ci-publish-token` |

## Documentation

- [Skills Reference](./docs/skills.md) - Detailed skill capabilities and domains
- [Commands Reference](./docs/commands.md) - Command usage and examples
- [Configuration Guide](./docs/configuration.md) - Setup and customization options
- [Examples](./docs/examples.md) - Real-world usage patterns

## Skill Domains

### 1. CI/CD Pipeline Configuration

**Triggers:**
- Tasks involving `.gitlab-ci.yml` files
- Pipeline performance optimization
- Caching strategy implementation
- Docker-in-Docker workflows
- GitLab CI Steps composition

**Key Features:**
- Validates .gitlab-ci.yml syntax before committing
- Implements caching for dependencies
- Optimizes job dependencies
- Tests pipelines locally with gitlab-ci-local

### 2. GitLab Flavored Markdown (GLFM)

**Triggers:**
- Writing README files for GitLab projects
- Creating GitLab Wiki pages
- API documentation with syntax highlighting
- Process flow diagrams with Mermaid

**Key Features:**
- Alert blocks: `[!note]`, `[!tip]`, `[!important]`, `[!caution]`, `[!warning]`
- Collapsible sections with `<details><summary>`
- Mermaid diagrams for visualizations
- GitLab references: #issue, !MR, @user

### 3. Local Pipeline Testing

**Triggers:**
- Testing .gitlab-ci.yml changes before push
- Debugging pipeline job failures locally
- Validating release workflows
- Testing specific jobs/stages in isolation

**Key Features:**
- gitlab-ci-local integration
- Authentication token configuration
- Artifact generation and verification
- Job-specific execution

### 4. GitLab CLI (glab)

**Triggers:**
- Monitoring pipeline status from terminal
- Linting CI configuration before push
- Non-interactive CI/CD operations

**Key Features:**
- Non-interactive pipeline monitoring
- CI configuration linting via GitLab API
- Pipeline status checking in automation
- Avoids interactive TUI commands

## Usage Examples

### Optimize Pipeline Caching

```bash
# Claude will apply gitlab-skill automatically when editing .gitlab-ci.yml
# Request: "Optimize this pipeline for faster builds"
```

The skill will analyze your pipeline and suggest:
- Dependency caching strategies
- Job parallelization opportunities
- Docker layer caching patterns
- Artifact management best practices

### Validate GLFM Syntax

```bash
# Use the validation script
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file README.md

# Or validate inline markdown
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --markdown "> [!note]\n> Test alert"
```

### Test Pipeline Locally

```bash
# Configure authentication in $HOME/.gitlab-ci-local/variables.yml
# Then test specific jobs
gitlab-ci-local build
gitlab-ci-local --stage test
gitlab-ci-local --needs release
```

### Lint CI Configuration

```bash
# Validate .gitlab-ci.yml syntax via GitLab API
glab ci lint

# Include job list in output
glab ci lint --include-jobs

# Simulate pipeline creation (dry run)
glab ci lint --dry-run --ref main
```

### Setup CI Token for Publishing

```bash
# Run the setup command
/setup-ci-publish-token

# Use the token in .gitlab-ci.yml
# CI_PUBLISH_TOKEN is now available as a protected, masked variable
```

## Validation Checklists

### CI/CD Pipeline Validation

Before committing .gitlab-ci.yml:

- [ ] Syntax validated against GitLab CI schema
- [ ] Jobs and stages use descriptive names
- [ ] Caching configured for dependencies
- [ ] Secrets masked, environment variables secured
- [ ] Conditional execution prevents unnecessary resource consumption
- [ ] Artifacts configured with appropriate expiration
- [ ] Timeout limits defined per job
- [ ] Pipeline tested locally with gitlab-ci-local
- [ ] Pipeline architecture documented

### GLFM Documentation Validation

Before committing GLFM files:

- [ ] Alert blocks use lowercase syntax
- [ ] Collapsible sections use single-line `<details><summary>` format
- [ ] No markdown syntax in `<summary>` tags
- [ ] Mermaid diagrams used for process flows
- [ ] Table of contents present for documents >100 lines
- [ ] GitLab references used: #issue, !MR, @user
- [ ] Code blocks have language specifiers
- [ ] Heading hierarchy consistent
- [ ] Rendered output validated with validate-glfm.py

## Utility Scripts

### validate-glfm.py

Validates GLFM rendering via GitLab Markdown API.

```bash
# Validate markdown file
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file README.md

# Save rendered HTML
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file test.md --output rendered.html

# Verbose debugging
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file test.md --verbose
```

### sync-gitlab-docs.py

Updates GitLab CI documentation from official repository.

```bash
# Update documentation (respects 3-day cooldown)
uv run scripts/sync-gitlab-docs.py --working-dir .

# Force update (bypass cooldown)
uv run scripts/sync-gitlab-docs.py --working-dir . --force
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITLAB_TOKEN` | For commands | Personal access token with `api` scope |
| `GL_TOKEN` | Alternative | Alternative to GITLAB_TOKEN |
| `CI_JOB_TOKEN` | In CI/CD | Automatic in GitLab CI/CD environment |
| `CI_PUBLISH_TOKEN` | For publishing | Created by setup-ci-publish-token command |

### gitlab-ci-local Configuration

Create `$HOME/.gitlab-ci-local/variables.yml`:

```yaml
GITLAB_TOKEN: your-personal-access-token
CI_SERVER_URL: https://gitlab.com
```

Create `.gitlab-ci-local-variables.yml` in project root for project-specific variables.

### glab Authentication

```bash
# Login with token
glab auth login --hostname gitlab.com --token YOUR_TOKEN

# Or use environment variable
export GITLAB_TOKEN=your-token
```

## Troubleshooting

### Pipeline Validation Fails

**Issue:** `glab ci lint` shows errors for included files

**Solution:** Commit and push included files first. The lint command resolves `include:` directives from the remote repository.

### Local Pipeline Fails with Authentication Error

**Issue:** gitlab-ci-local reports authentication errors

**Solution:**
1. Verify `$HOME/.gitlab-ci-local/variables.yml` exists and contains `GITLAB_TOKEN`
2. Ensure token has appropriate scopes (`api`, `read_repository`)
3. Check token hasn't expired: `glab token list`

### GLFM Alerts Not Rendering

**Issue:** Alert blocks show as plain text in GitLab

**Solution:**
- Ensure alert types are lowercase: `[!note]` not `[!Note]` or `[!NOTE]`
- Validate with `validate-glfm.py` script
- Check GitLab version supports GLFM alert syntax (GitLab 16.0+)

### Command Not Found: /setup-ci-publish-token

**Issue:** Slash command doesn't appear in autocomplete

**Solution:**
1. Verify plugin is installed: `/plugin list`
2. Reload plugins: `/plugin reload`
3. Check commands directory exists: `ls ~/.claude/plugins/gitlab-skill/commands/`

### CI_PUBLISH_TOKEN Not Available in Job

**Issue:** Pipeline job reports CI_PUBLISH_TOKEN is undefined

**Solution:**
- Protected variables only work on protected branches
- Verify branch/tag is protected in Settings > Repository > Protected branches
- Check token hasn't expired: `glab token list`

## Contributing

Contributions are welcome! When contributing:

1. Test CI/CD configurations locally with gitlab-ci-local before submitting
2. Validate GLFM syntax with validate-glfm.py
3. Update documentation index with sync-gitlab-docs.py
4. Follow existing patterns in reference documentation
5. Add examples for new features

## Reference Documentation

The plugin includes extensive reference documentation synchronized from official GitLab sources:

- **CI/CD Pipeline References** - Performance optimization, caching, common patterns
- **GLFM References** - Complete syntax guide with examples and anti-patterns
- **gitlab-ci-local References** - Setup, authentication, troubleshooting
- **GitLab CI Steps References** - Steps feature overview, syntax, examples, architecture

See [Documentation Index](./skills/gitlab-skill/SKILL.md#documentation-index) for complete documentation structure.

## License

This plugin follows the repository's license. See the main repository for license details.

## Credits

Created as part of the Claude Skills repository. Synchronized documentation is sourced from the official GitLab documentation repository.

## Version History

### 1.0.0 (Current)

- Initial release
- CI/CD pipeline configuration domain
- GLFM syntax domain with validation tooling
- Local pipeline testing with gitlab-ci-local
- GitLab CLI (glab) integration
- CI publishing token setup command
- Automated documentation sync from GitLab repository
- Comprehensive reference documentation (600+ files)
