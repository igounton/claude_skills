# Holistic Linting Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive code quality plugin for Claude Code that ensures systematic linting and formatting verification. Prevents the common pattern where code is claimed "production ready" without actually running quality checks.

## Features

- **Automatic Linting Workflows** - Orchestrators delegate to specialized agents; sub-agents lint before task completion
- **Root Cause Resolution** - Never suppress errors without understanding them through systematic investigation
- **Multi-Linter Support** - Works with ruff, mypy, pyright/basedpyright, bandit, eslint, prettier, and more
- **Linter Discovery** - Automatically detect and document project linters via `/lint init`
- **Rules Knowledge Base** - Comprehensive documentation for ruff (933 rules), mypy error codes, and bandit security checks
- **Dual-Phase Workflow** - Resolution agent fixes issues, review agent validates architectural quality
- **Git Hook Integration** - Detects and uses prek or pre-commit for scoped formatting operations

## Installation

### Prerequisites

- Claude Code version 2.1+
- Python 3.11+ (for Python linting features)
- Git repository (for git hook detection)

### Install Plugin

```bash
# Method 1: From plugin directory
/plugin install holistic-linting --scope user

# Method 2: Manual installation (if developing locally)
cp -r ./plugins/holistic-linting ~/.claude/plugins/
/plugin reload
```

### Install Agents

The plugin includes two specialized agents that need to be installed separately:

```bash
# Install to user scope (~/.claude/agents/)
python ./plugins/holistic-linting/skills/holistic-linting/scripts/install-agents.py --scope user

# Install to project scope (<git-root>/.claude/agents/)
python ./plugins/holistic-linting/skills/holistic-linting/scripts/install-agents.py --scope project

# Force overwrite existing agents
python ./plugins/holistic-linting/skills/holistic-linting/scripts/install-agents.py --scope user --force
```

## Quick Start

### Discover Your Project's Linters

```bash
/lint init
```

This scans your project for linting tools and generates a `## LINTERS` section in your `CLAUDE.md` file.

### Lint Specific Files

```bash
/lint src/auth.py
/lint src/models.py tests/test_auth.py
```

### Automatic Linting (Orchestrators)

When you complete a task involving code changes, Claude will automatically:

1. Delegate to the `linting-root-cause-resolver` agent
2. Agent formats, lints, and resolves issues systematically
3. Delegate to `post-linting-architecture-reviewer` for quality validation
4. Read review reports to confirm completion

### Automatic Linting (Sub-Agents)

Sub-agents automatically format and lint their modified files before completing tasks.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| **Skill** | holistic-linting | Automatic linting workflows for orchestrators and sub-agents | Auto-activated |
| **Command** | `/lint` | Manual linting and linter discovery | `/lint [path\|init]` |
| **Agent** | linting-root-cause-resolver | Systematically resolves linting errors by investigating root causes | Delegated by orchestrator |
| **Agent** | post-linting-architecture-reviewer | Validates resolution quality and architectural implications | Delegated after resolution |

## Usage

### For Orchestrators

**Never run formatters or linters yourself.** Delegate immediately to agents:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Format, lint, and resolve any issues in src/auth.py"
)
```

The agent will:
- Run formatters (ruff format, prettier, etc.)
- Run linters (ruff check, mypy, pyright, etc.)
- Investigate issues using linter-specific workflows
- Implement elegant fixes following python3-development patterns
- Verify resolution by re-running linters
- Create resolution reports in `.claude/reports/`

After resolution completes, delegate architectural review:

```text
Task(
  agent="post-linting-architecture-reviewer",
  prompt="Review linting resolution for src/auth.py"
)
```

Read the review report to determine if additional work is needed:

```bash
ls -la .claude/reports/architectural-review-*.md
```

### For Sub-Agents

Before completing any task involving Edit/Write:

1. Format touched files
2. Lint touched files
3. Resolve issues directly using linter-specific workflows from the skill
4. Don't complete until all issues are resolved

### Manual Linting with `/lint`

#### Lint Files

```bash
/lint path/to/file.py
/lint src/*.py
/lint src/
```

#### Discover Project Linters

```bash
/lint init               # Create LINTERS section in CLAUDE.md
/lint init --force       # Overwrite existing configuration
```

This scans for:
- `.pre-commit-config.yaml` hooks
- `pyproject.toml` linter configurations
- `package.json` dev dependencies
- Config files (`.eslintrc*`, `.prettierrc*`, `.markdownlint*`)

## Linter-Specific Resolution Workflows

The skill provides systematic resolution workflows for each major linting tool:

### Ruff Resolution Workflow

1. Research rule: `ruff rule {RULE_CODE}`
2. Read affected code and architectural context
3. Load python3-development skill
4. Implement elegant fix addressing root cause
5. Verify with `ruff check`

### Mypy Resolution Workflow

1. Research error code in local mypy documentation
2. Trace type flow through code
3. Check library type stubs if needed
4. Load python3-development skill
5. Fix annotation, implementation, or add type narrowing
6. Verify with `mypy`

### Pyright/Basedpyright Resolution Workflow

1. Research diagnostic rule using MCP tools (Ref, exa) or WebFetch
2. Read affected code and understand type inference
3. Check architectural context
4. Load python3-development skill
5. Add type guards, annotations, or use TypeGuard/cast
6. Verify with `pyright` or `basedpyright`

See [Usage Examples](./docs/examples.md) for detailed workflow demonstrations.

## Agents

### linting-root-cause-resolver

**Purpose**: Systematically investigates and resolves linting errors by understanding root causes rather than suppressing symptoms.

**Model**: Inherits from session

**Key Features**:
- Automatic skill loading (holistic-linting + python3-development)
- Linter-specific resolution workflows for ruff, mypy, pyright
- Produces structured artifacts for architectural review
- Verifies all fixes by re-running linters

**When to Use**:
- Orchestrators should delegate immediately after code changes
- When ruff, mypy, pyright, or basedpyright report issues

**Delegation Example**:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Format, lint, and resolve any issues in src/api.py"
)
```

### post-linting-architecture-reviewer

**Purpose**: Validates linting resolution quality and identifies systemic architectural improvements.

**Model**: Haiku (fast reviews)

**Key Features**:
- Verifies fixes address root causes, not symptoms
- Checks alignment with codebase patterns
- Validates architectural implications
- Identifies opportunities for systemic improvements

**When to Use**:
- After linting-root-cause-resolver completes
- When resolution artifacts exist in `.claude/reports/`

**Delegation Example**:

```text
Task(
  agent="post-linting-architecture-reviewer",
  prompt="Review linting resolution for src/api.py"
)
```

See [Agent Reference](./docs/agents.md) for complete documentation.

## Scripts

The plugin includes utility scripts in `skills/holistic-linting/scripts/`:

| Script | Purpose |
|--------|---------|
| `install-agents.py` | Install agents to user or project scope |
| `detect-hook-tool.py` | Detect and run git hook tool (prek or pre-commit) |
| `discover-linters.py` | Scan project and generate LINTERS configuration |
| `lint-orchestrator.py` | Run project linters based on CLAUDE.md configuration |

### Using detect-hook-tool.py

```bash
# Detect which tool is configured (outputs 'prek' or 'pre-commit')
uv run ./scripts/detect-hook-tool.py

# Run detected tool with arguments
uv run ./scripts/detect-hook-tool.py run --files path/to/file.py

# Check different repository
uv run ./scripts/detect-hook-tool.py --directory /path/to/repo run --files file.py
```

**Important**: Always use `--files` for scoped operations to avoid formatting unrelated code.

## Configuration

### Project Configuration (CLAUDE.md)

The plugin reads linter configuration from a `## LINTERS` section in your project's `CLAUDE.md`:

```markdown
## LINTERS

git pre-commit hooks: enabled
pre-commit tool: pre-commit

### Formatters

- ruff format [*.py]
- prettier [*.{ts,tsx,json,md}]
- markdownlint-cli2 [*.md]

### Static Checking and Linting

- ruff check [*.py]
- mypy [*.py]
- pyright [*.py]
- eslint [*.{ts,tsx}]
```

Generate this automatically with `/lint init`.

### Supported Linters

**Python**:
- ruff (formatting + linting)
- mypy (type checking)
- pyright/basedpyright (type checking)
- bandit (security)

**JavaScript/TypeScript**:
- prettier (formatting)
- eslint (linting)

**Shell**:
- shfmt (formatting)
- shellcheck (linting)

**Markdown**:
- markdownlint-cli2 (formatting + linting)

**Git Hooks**:
- pre-commit (Python-based)
- prek (Rust-based pre-commit replacement)

## Examples

### Example 1: Orchestrator Completes Python Feature

```text
User: "Add authentication middleware to the API"

Orchestrator:
1. [Implements authentication in src/auth.py]
2. [Applies holistic-linting skill workflow]
3. Task(agent="linting-root-cause-resolver",
        prompt="Format, lint, and resolve issues in src/auth.py")
4. [Agent formats, lints, resolves 5 issues]
5. [Agent creates resolution report]
6. Task(agent="post-linting-architecture-reviewer",
        prompt="Review linting resolution for src/auth.py")
7. [Orchestrator reads review report confirming quality]
8. Task complete ✓
```

### Example 2: Sub-Agent Writes Python Module

```text
Orchestrator delegates: "Create database connection pool module"

Sub-agent:
1. [Writes db_pool.py]
2. [Formats with: uv run ruff format db_pool.py]
3. [Lints with: uv run ruff check && uv run mypy]
4. [Finds 1 mypy error: Missing return type]
5. [Fixes: Adds -> ConnectionPool annotation]
6. [Verifies: uv run mypy db_pool.py - clean]
7. Returns to orchestrator ✓
```

### Example 3: Discover Project Linters

```text
/lint init

[Scanning project configuration...]
✓ Found .pre-commit-config.yaml with 6 hooks
✓ Found pyproject.toml with ruff, mypy, pyright
✓ Found package.json with eslint, prettier
✓ Git hooks: enabled (pre-commit)

[Generated LINTERS section and appended to CLAUDE.md]
```

See [More Examples](./docs/examples.md) for detailed workflow demonstrations.

## Rules Knowledge Base

The skill includes comprehensive linting rule documentation:

### Ruff Rules (933 rules)

Location: `skills/holistic-linting/references/rules/ruff/index.md`

Covers all rule families:
- E/W (pycodestyle)
- F (Pyflakes)
- B (flake8-bugbear)
- S (Bandit security)
- I (isort)
- UP (pyupgrade)
- And 13 more families

Each rule documents the design principle, violation patterns, resolution examples, and configuration options.

### MyPy Error Codes

Location: `skills/holistic-linting/references/rules/mypy/index.md`

Comprehensive type checking documentation:
- Attribute access errors
- Function call type checking
- Assignment compatibility
- Collection type checking
- Import resolution
- Abstract class enforcement

Each error code explains the type safety principle, valid vs. invalid patterns, and corrected examples.

### Bandit Security Checks (65+ checks)

Location: `skills/holistic-linting/references/rules/bandit/index.md`

Security vulnerability documentation:
- Credentials and secrets
- Cryptography weaknesses
- SSL/TLS vulnerabilities
- Injection attacks
- Deserialization risks
- Unsafe functions

Each check documents the security risk, vulnerable patterns, secure alternatives, and severity level.

## Integration with Claude Code Hooks

This plugin complements hook-based linting (like `claude-linting-hook`) but serves different purposes:

**PostToolUse Hook** (immediate feedback):
- Triggers after Edit/Write
- Provides instant feedback
- Blocks on issues

**holistic-linting Skill** (workflow guidance):
- Guides task completion workflow
- Ensures systematic resolution
- Provides rules knowledge base
- Includes architectural review

Use both together for comprehensive coverage:
1. Hook catches issues during editing
2. Skill ensures resolution before task completion
3. Knowledge base supports root-cause analysis
4. Architectural review validates quality

## Troubleshooting

### "I don't know which linters this project uses"

**Solution**: Run `/lint init` to scan and document project linters.

### "Linting errors but I don't understand the rule"

**Solution**: Reference the rules knowledge base at `skills/holistic-linting/references/rules/{ruff,mypy,bandit}/index.md`.

### "Multiple files with linting errors"

**Solution**:
- **Orchestrators**: Launch concurrent agents (one per file)
- **Sub-agents**: Resolve each file sequentially

### "Linter not found (command not available)"

**Solution**: Check linters are installed. Use `uv run <tool>` for Python tools to ensure virtual environment activation.

### "False positive linting error"

**Solution**: Investigate using rule documentation. If truly false positive, configure the rule in `pyproject.toml` rather than using ignore comments.

### "Agent reports persist after resolution"

**Solution**: Reports in `.claude/reports/` are intentionally preserved for documentation. Add `.claude/reports/` to `.gitignore` if needed:

```bash
echo "reports/" >> .claude/.gitignore
```

## Best Practices

1. **Orchestrators delegate immediately** - Don't run formatters/linters yourself
2. **Always read CLAUDE.md LINTERS section first** - Don't assume which linters are available
3. **Format before linting** - Formatters auto-fix trivial issues
4. **Run linters concurrently** - Use parallel execution for multiple files
5. **Use the rules knowledge base** - Reference official documentation when investigating
6. **Never suppress without understanding** - Don't add `# type: ignore` or `# noqa` without analysis
7. **Verify after fixes** - Always re-run linters to confirm resolution
8. **Trust agent verification** - Orchestrators read reports instead of re-running linters
9. **Use scoped operations** - Always use `--files` with git hooks to avoid unrelated changes

## Related Skills

- **python3-development** - Modern Python patterns and best practices (automatically loaded by resolver agent)
- **uv** - Python package management with uv

## Contributing

When contributing to this plugin:

1. Follow the linting standards documented in the plugin itself
2. Run `/lint init` to discover configuration
3. Use `/lint` on all modified files before committing
4. Ensure agents can be installed without errors
5. Update documentation for new linters or workflows

## License

See repository LICENSE file for details.
