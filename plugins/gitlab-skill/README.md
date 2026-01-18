# GitLab CI/CD and Documentation

Makes Claude better at GitLab work: writing pipelines, creating documentation, and testing locally.

## Why Install This?

When working with GitLab projects, Claude sometimes:
- Writes pipelines that fail validation or miss optimizations
- Creates README files with syntax that doesn't render correctly in GitLab
- Suggests pushing untested pipeline changes
- Doesn't use GitLab-specific features like alert blocks or CI Steps

This plugin fixes those problems.

## What Changes

Claude will:
- Write `.gitlab-ci.yml` files with proper caching, parallelization, and optimization
- Create GitLab documentation that renders correctly the first time
- Test pipelines locally with `gitlab-ci-local` before pushing
- Use GitLab features like alert blocks, collapsible sections, and Mermaid diagrams correctly
- Help set up CI/CD authentication tokens

## Installation

```bash
/plugin install gitlab-skill
```

## Usage

Just install it - works automatically when you work with GitLab projects.

Useful for:
- "Add a test stage to the pipeline"
- "Create a README for this GitLab project"
- "Test this pipeline locally before pushing"
- "Set up caching for Python dependencies"
- "Add a collapsible troubleshooting section"

## Example

**Without this plugin:**
You say "add a note about security to the README". Claude writes standard Markdown that doesn't render as an alert in GitLab.

**With this plugin:**
Claude writes proper GLFM alert syntax that renders with styling and icons:

```markdown
> [!important]
> This requires authentication
```

## More Examples

**CI/CD pipelines:** Claude writes pipelines with dependency-based cache keys, parallel jobs, proper artifact management, and GitLab-specific features like coverage reports.

**Local testing:** Instead of pushing to see failures, Claude suggests testing with `gitlab-ci-local` to catch errors in 30 seconds instead of 5 minutes.

**Documentation:** Claude uses correct GLFM syntax - lowercase alerts, single-line summary tags, proper Mermaid diagrams - so your docs render correctly the first time.

## What's Included

- CI/CD configuration patterns and optimization strategies
- GitLab Flavored Markdown complete syntax guide
- gitlab-ci-local testing setup and usage
- GitLab CLI (glab) commands for pipeline monitoring
- `/setup-ci-publish-token` command for CI authentication
- Official GitLab documentation reference (auto-updated)

## Requirements

- Claude Code v2.0+
