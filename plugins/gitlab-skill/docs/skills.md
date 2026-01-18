# Skills Reference

The gitlab-skill plugin provides a single comprehensive skill that covers four distinct domains related to GitLab CI/CD and documentation workflows.

---

## gitlab-skill

**Location**: `skills/gitlab-skill/SKILL.md`

**Description**: The model must apply when tasks involve .gitlab-ci.yml configuration, GitLab Flavored Markdown (GLFM) syntax, gitlab-ci-local testing, CI/CD pipeline optimization, GitLab CI Steps composition, Docker-in-Docker workflows, or GitLab documentation creation. Triggers include modifying pipelines, writing GitLab README/Wiki content, debugging CI jobs locally, implementing caching strategies, or configuring release workflows.

**User Invocable**: Yes (default)

**Model**: Inherits from session

**Context**: Inline (runs in main conversation)

---

## Capability Domains

### Domain 1: CI/CD Pipeline Configuration

**When to Use**

Use this domain when working with:
- .gitlab-ci.yml file creation or modification
- Pipeline performance optimization
- Caching strategy implementation
- Conditional job execution configuration
- Secret and environment variable management
- Docker-in-Docker (dind) workflow setup
- Pipeline job failure troubleshooting
- GitLab CI Steps composition for reusable workflow units

**Activation**

Automatically activated when Claude detects tasks involving:
- Files named `.gitlab-ci.yml`
- Discussion of GitLab CI/CD pipelines
- Mentions of caching, stages, jobs, artifacts
- Docker-in-Docker workflows
- GitLab CI Steps

**Constraints**

When this domain is active, the model MUST:
- Validate .gitlab-ci.yml syntax before committing
- Implement caching for dependencies to minimize build time
- Use masked variables for sensitive data
- Define timeout limits for all jobs
- Test pipelines locally with gitlab-ci-local before pushing
- Use .gitlab-ci.yml include feature for modular configurations
- Optimize job dependencies to prevent unnecessary execution
- Implement comprehensive testing at each pipeline stage

**Key Capabilities**

- **Pipeline Optimization** - Analyzes pipelines for performance bottlenecks, suggests caching strategies, identifies parallelization opportunities
- **Job Configuration** - Helps structure jobs, stages, and dependencies according to best practices
- **Docker Integration** - Provides Docker-in-Docker patterns, image optimization, layer caching strategies
- **GitLab CI Steps** - Guides implementation of reusable CI Steps for workflow composition

**Reference Files**

- [pipeline-optimization.md](../skills/gitlab-skill/references/pipeline-optimization.md) - Caching strategies, job parallelization, Docker optimization patterns
- [common-patterns.md](../skills/gitlab-skill/references/common-patterns.md) - Reusable configuration examples
- [ci-steps/index.md](../skills/gitlab-skill/references/ci-steps/index.md) - Steps feature overview, syntax, implementation details

**Example Usage**

```text
User: "Optimize this .gitlab-ci.yml for faster builds"
Claude: [Activates gitlab-skill, analyzes pipeline, suggests caching strategies and parallelization]
```

---

### Domain 2: GitLab Flavored Markdown (GLFM)

**When to Use**

Use this domain when creating GitLab documentation:
- README files for GitLab projects
- GitLab Wiki pages
- API documentation with GitLab syntax highlighting
- User guides requiring collapsible sections
- Process flow diagrams with Mermaid
- Changelogs with GitLab issue/MR references

**Activation**

Automatically activated when Claude detects:
- Markdown file creation or editing in GitLab context
- Mention of GitLab-specific markdown features
- Discussion of alerts, collapsible sections, or Mermaid diagrams
- Documentation requirements for GitLab projects

**GLFM Syntax Features**

The skill provides guidance on:

- **Alert blocks**: `[!note]`, `[!tip]`, `[!important]`, `[!caution]`, `[!warning]`
- **Collapsible sections**: `<details><summary>` syntax
- **Mermaid diagrams**: For process visualizations
- **Task lists**: With completion tracking
- **GitLab references**: #issue, !MR, @user notation
- **Table of contents**: Auto-generation
- **Math expressions**: LaTeX-style math support
- **Color chips**: For design documentation

**Critical Syntax Rules**

The model MUST enforce these non-negotiable GLFM rendering requirements:

1. Alert types MUST be lowercase: `[!note]` not `[!Note]` or `[!NOTE]`
2. `<details><summary>` MUST be single line: `<details><summary>Text</summary>` not multi-line
3. No markdown syntax inside `<summary>` tags - use HTML equivalents (`<code>`, `<strong>`)
4. The model must validate rendering with validate-glfm.py script before finalizing

**Validation Tooling**

The domain includes a Python validation script:

```bash
# Validate markdown file
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file README.md

# Validate inline markdown
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --markdown "> [!note]\n> Test alert"

# Save rendered HTML
uv run --with requests ./skills/gitlab-skill/scripts/validate-glfm.py --file test.md --output rendered.html
```

**Reference Files**

- [glfm-syntax.md](../skills/gitlab-skill/references/glfm-syntax.md) - Complete syntax guide, examples, common mistakes

**Example Usage**

```text
User: "Create a README for this GitLab project with collapsible troubleshooting section"
Claude: [Activates gitlab-skill, applies GLFM syntax rules, validates rendering]
```

---

### Domain 3: Local Pipeline Testing

**When to Use**

Use this domain when:
- Testing .gitlab-ci.yml changes before push
- Debugging pipeline job failures locally
- Validating release workflows without actual release creation
- Testing specific jobs/stages in isolation
- Verifying conditional job execution logic
- Checking artifact generation and dependencies

**Activation**

Automatically activated when Claude detects:
- Mention of `gitlab-ci-local`
- Discussion of local pipeline testing
- Request to test CI/CD changes before pushing
- Debugging pipeline issues locally

**Setup Procedure**

The domain guides through gitlab-ci-local installation and configuration:

```bash
# 1. Install gitlab-ci-local globally
npm install -g gitlab-ci-local

# 2. Configure authentication tokens
# Edit $HOME/.gitlab-ci-local/variables.yml

# 3. Set project-specific variables
# Create .gitlab-ci-local-variables.yml in project root

# 4. Execute job locally
gitlab-ci-local <job-name>
```

**Common Operations**

```bash
gitlab-ci-local --list                    # List all jobs
gitlab-ci-local --preview                 # Preview parsed configuration
gitlab-ci-local --stage test              # Run specific stage
gitlab-ci-local --needs release           # Run with dependencies
gitlab-ci-local --timestamps job-name     # Debug with timestamps
```

**Key Capabilities**

- **Configuration Validation** - Verifies .gitlab-ci.yml syntax locally
- **Job Execution** - Runs jobs in local Docker containers
- **Artifact Management** - Validates artifact generation and dependencies
- **Debug Support** - Provides detailed execution logs with timestamps
- **Conditional Logic Testing** - Tests rules and conditions before push

**Reference Files**

- [gitlab-ci-local-guide.md](../skills/gitlab-skill/references/gitlab-ci-local-guide.md) - Setup, authentication, troubleshooting, examples

**Example Usage**

```text
User: "Test this pipeline locally before I push"
Claude: [Activates gitlab-skill, guides through gitlab-ci-local setup, executes test]
```

---

### Domain 4: GitLab CLI (glab)

**When to Use**

Use this domain when:
- Monitoring pipeline status from terminal
- Linting CI configuration before push
- Listing or inspecting pipelines and jobs
- Non-interactive CI/CD operations in scripts or automation

**Activation**

Automatically activated when Claude detects:
- Mention of `glab` CLI
- Request for pipeline monitoring
- CI configuration validation needs
- Terminal-based GitLab operations

**Critical: Avoid Interactive Commands**

The `glab ci view` command launches an interactive TUI. Use non-interactive alternatives:

```bash
# INTERACTIVE (avoid in automation):
glab ci view                    # Opens interactive TUI

# NON-INTERACTIVE alternatives:
glab ci status --compact        # Quick pass/fail status
glab ci get                     # Pipeline details as text
glab ci list --per-page 5       # Recent pipelines table
```

**Linting CI Configuration**

```bash
# Validate .gitlab-ci.yml syntax via GitLab API
glab ci lint

# Include job list in output
glab ci lint --include-jobs

# Simulate pipeline creation (dry run)
glab ci lint --dry-run --ref main
```

The lint command sends the local `.gitlab-ci.yml` to GitLab API for validation. This resolves `include:` directives from the remote repository, so included files must be committed and pushed for accurate validation.

**Pipeline Monitoring**

```bash
# List recent pipelines with status
glab ci list --per-page 5

# Get current branch pipeline details
glab ci get

# Quick status check (exits non-zero on failure)
glab ci status --compact
```

**Common Workflow**

```bash
# 1. Validate before commit
glab ci lint

# 2. Commit and push
git add . && git commit -m "message" && git push

# 3. Monitor pipeline
glab ci list --per-page 3
glab ci status --compact

# 4. On failure, get details
glab ci get
```

**Key Capabilities**

- **Non-Interactive Validation** - Validates CI configuration without opening TUI
- **Pipeline Status** - Monitors pipeline status in automation-friendly format
- **Job Inspection** - Lists and inspects jobs without interactive navigation
- **API Integration** - Leverages GitLab API for accurate validation

**Example Usage**

```text
User: "Check if the pipeline passed for this branch"
Claude: [Activates gitlab-skill, executes glab ci status --compact, reports result]
```

---

## Execution Protocol

When gitlab-skill activates, the model follows this sequence:

1. **Update documentation reference** (first step on skill activation):

   ```bash
   uv run scripts/sync-gitlab-docs.py --working-dir .
   ```

   - Updates GitLab CI documentation from official repository
   - Respects 3-day cooldown (successful runs only)
   - Use `--force` flag to bypass cooldown if needed
   - Creates/updates Documentation Index in SKILL.md file
   - Lock file: `.sync-gitlab-docs.lock` (gitignored)

2. Identify domain: CI/CD configuration, GLFM documentation, local testing, or glab CLI
3. Load domain-specific reference files for technical specifications
4. Apply domain constraints and validation rules
5. Execute domain-specific validation checklist
6. Validate output using appropriate tooling (gitlab-ci-local, validate-glfm.py, or glab)

---

## Quick Start Paths

### IF task involves CI/CD pipeline:

1. Load [pipeline-optimization.md](../skills/gitlab-skill/references/pipeline-optimization.md)
2. Review [common-patterns.md](../skills/gitlab-skill/references/common-patterns.md) for reusable configurations
3. Test locally with gitlab-ci-local before pushing

### IF task involves GLFM documentation:

1. Load [glfm-syntax.md](../skills/gitlab-skill/references/glfm-syntax.md)
2. Apply CRITICAL_SYNTAX_RULES during writing
3. Validate rendering with validate-glfm.py script

### IF task involves local pipeline testing:

1. Load [gitlab-ci-local-guide.md](../skills/gitlab-skill/references/gitlab-ci-local-guide.md)
2. Verify authentication configuration in $HOME/.gitlab-ci-local/
3. Execute pipeline locally, verify artifacts in .gitlab-ci-local/artifacts/

### IF task involves glab CLI:

1. Use non-interactive commands only (avoid `glab ci view`)
2. Lint configuration with `glab ci lint` before push
3. Monitor pipelines with `glab ci get` or `glab ci status --compact`

---

## Validation Checklists

### CI/CD Pipeline Validation

The model must verify before committing .gitlab-ci.yml:

- [ ] Syntax validated against GitLab CI schema
- [ ] Jobs and stages use descriptive names, logical organization
- [ ] Caching configured for dependencies
- [ ] Secrets masked, environment variables secured
- [ ] Conditional execution prevents unnecessary resource consumption
- [ ] Artifacts configured with appropriate expiration
- [ ] Timeout limits defined per job
- [ ] Pipeline tested locally with gitlab-ci-local
- [ ] Pipeline architecture documented

### GLFM Documentation Validation

The model must verify before committing GLFM files:

- [ ] Alert blocks use lowercase syntax: `[!note]`, `[!tip]`, `[!important]`, `[!caution]`, `[!warning]`
- [ ] Collapsible sections use single-line `<details><summary>` format
- [ ] No markdown syntax in `<summary>` tags
- [ ] Mermaid diagrams used for process flows
- [ ] Table of contents present for documents >100 lines
- [ ] GitLab references used: #issue, !MR, @user
- [ ] Code blocks have language specifiers
- [ ] Heading hierarchy consistent (no skipped levels)
- [ ] Rendered output validated with validate-glfm.py

### Local Testing Validation

The model must verify local test environment:

- [ ] gitlab-ci-local installed and accessible
- [ ] Authentication tokens configured in $HOME/.gitlab-ci-local/variables.yml
- [ ] Project variables defined in .gitlab-ci-local-variables.yml
- [ ] Jobs execute locally without errors
- [ ] Artifacts present in .gitlab-ci-local/artifacts/
- [ ] Configuration validated with `--preview` flag

---

## Reference Documentation Structure

The skill includes 600+ reference files synchronized from official GitLab documentation:

- **CI/CD Core** - Pipeline configuration, jobs, variables, YAML syntax
- **Testing** - Code quality, unit tests, code coverage, performance testing
- **Environments** - Deployments, review apps, Kubernetes integration
- **Docker** - Docker-in-Docker, BuildKit, Buildah, image building
- **Cloud Services** - AWS, Azure, GCP integration with OIDC
- **Runners** - Configuration, hosted runners, fleet management
- **Secrets** - External secrets, Vault, AWS/Azure/GCP secret managers
- **Examples** - Language-specific examples, deployment patterns
- **Migration** - Migrate from Jenkins, GitHub Actions, CircleCI

See the [Documentation Index](../skills/gitlab-skill/SKILL.md#documentation-index) in SKILL.md for complete structure.

---

## Related Commands

The gitlab-skill works seamlessly with the plugin's commands:

- [/setup-ci-publish-token](./commands.md#setup-ci-publish-token) - Creates project access tokens for CI/CD publishing

---

## Back to Documentation

- [README](../README.md) - Plugin overview and quick start
- [Commands Reference](./commands.md) - Slash command usage
- [Configuration Guide](./configuration.md) - Setup and customization
- [Examples](./examples.md) - Real-world usage patterns
