---
name: claude-commands-reference-2026
description: Reference guide for Claude Code slash commands (January 2026). Use when creating custom commands, understanding command frontmatter, argument syntax, context fork, hooks, or plugin command namespacing.
---

# Claude Code Slash Commands - Complete Reference (January 2026)

Slash commands are user-invoked prompts executed via `/command-name`. Create custom commands in Markdown with YAML frontmatter.

---

## Command Frontmatter

```yaml
---
description: Brief description shown in /help
argument-hint: [arg1] [arg2]
allowed-tools: Read, Grep, Glob, Bash(git:*)
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
disable-model-invocation: false
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
---

# Command Title

Your instructions here...
```

### All Frontmatter Fields

| Field | Required | Type | Default | Description |
|-------|----------|------|---------|-------------|
| `description` | No | string | First line | Brief description for /help |
| `argument-hint` | No | string | None | Shows in autocomplete |
| `allowed-tools` | No | string/array | Inherits | Tool restrictions |
| `model` | No | string | Inherits | Model override |
| `context` | No | string | inline | `fork` for sub-agent context |
| `agent` | No | string | general-purpose | Agent type (with context: fork) |
| `disable-model-invocation` | No | boolean | false | Prevent Skill tool invocation |
| `hooks` | No | object | None | PreToolUse, PostToolUse, Stop |

---

## File Locations

### Project Commands (team-shared)

```
.claude/commands/
├── optimize.md          → /optimize
├── review-pr.md         → /review-pr
└── frontend/
    └── component.md     → /component (project:frontend)
```

### Personal Commands (user-only)

```
~/.claude/commands/
├── security-review.md   → /security-review (user)
└── my-workflow.md       → /my-workflow (user)
```

**Precedence**: Project commands override user commands with same name.

---

## Argument Syntax

### All Arguments: `$ARGUMENTS`

```markdown
Fix issue #$ARGUMENTS following our coding standards
```

Usage: `/fix-issue 123 high-priority`
Result: `$ARGUMENTS` → `"123 high-priority"`

### Positional Arguments: `$1`, `$2`, `$3`

```markdown
Review PR #$1 with priority $2 and assign to $3
```

Usage: `/review-pr 456 high alice`
Result: `$1` → `456`, `$2` → `high`, `$3` → `alice`

---

## Special Prefixes

### Bash Execution Prefix

**Prefix**: exclamation mark followed by backtick-wrapped command

Execute bash commands, output included in context.

```text
---
allowed-tools: Bash(git:*)
---

## Context

- Git status: !(git status)
- Git diff: !(git diff HEAD)
- Current branch: !(git branch --show-current)

## Task

Create a commit based on above changes.
```

**Note**: In actual usage, replace `()` with backticks around the command.

**Requirements**: Must include `allowed-tools` with `Bash` tool.

### File References: `@`

Include file contents in command context.

```markdown
Review the implementation in @src/utils/helpers.js
Compare @src/old-version.js with @src/new-version.js
```

- `@file-path`: Includes full file content
- `@dir-path`: Includes directory listing
- `@server:resource`: Fetches from MCP server

---

## Context Fork

Run command in isolated sub-agent context.

```yaml
---
context: fork
agent: general-purpose
---
```

| Agent | Model | Tools | Use Case |
|-------|-------|-------|----------|
| `general-purpose` | Inherits | All | Complex operations (default) |
| `Explore` | Haiku | Read-only | Fast codebase analysis |
| `Plan` | Inherits | Read-only | Research before planning |
| Custom | Custom | Custom | Project-specific work |

---

## Hooks in Commands

```yaml
---
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
---
```

**Supported Events**: PreToolUse, PostToolUse, Stop

**Hook Fields**:
- `matcher`: Tool pattern (regex, case-sensitive)
- `type`: `command` or `prompt`
- `command`: Bash command to execute
- `once`: Run only once per session (then remove)

---

## Discovery & Invocation

### Discovery
- All commands in `.claude/commands/` and `~/.claude/commands/` auto-discovered
- Listed in `/help` output
- Autocomplete with `/` anywhere in input

### Invocation

```
/command-name [arguments]
/review-pr 456 high
/optimize
```

### Skill Tool Access
- Custom commands available via `Skill` tool
- Claude can invoke programmatically
- Disable with `disable-model-invocation: true`
- Character budget: 15,000 chars (customizable via `SLASH_COMMAND_TOOL_CHAR_BUDGET`)

---

## Built-in vs Custom Commands

| Aspect | Built-in | Custom |
|--------|----------|--------|
| Location | Internal | `.claude/commands/` |
| Skill tool access | No | Yes |
| Overridable | No | Yes |
| Hooks | Not supported | Supported |

**Built-in Commands**: `/compact`, `/config`, `/cost`, `/help`, `/hooks`, `/init`, `/memory`, `/model`, `/plugin`, `/resume`, etc.

---

## Plugin Commands

### Location
`commands/` directory in plugin root

### Namespacing

```
/command-name                    (no conflicts)
/plugin-name:command-name        (disambiguation)
```

### Subdirectory Organization

```
commands/frontend/test.md → /test (plugin:frontend)
```

### Plugin Environment Variables

- `${CLAUDE_PLUGIN_ROOT}`: Absolute path to plugin
- `${CLAUDE_PROJECT_DIR}`: Project root

---

## MCP Commands

Dynamic commands from connected MCP servers.

```
/mcp__github__list_prs [arguments]
/mcp__server__prompt_name
```

Format: `/mcp__<server>__<prompt>` (lowercase, underscores)

---

## Examples

### Simple Command

```markdown
---
description: Generate conventional commit message
---

1. Run `git diff --staged`
2. Determine type (feat, fix, docs)
3. Write message under 50 chars
4. Use imperative mood
```

### With Arguments

```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number]
---

Fix issue #$1 following our coding standards.
```

### Forked Context

```markdown
---
description: Deep codebase research
context: fork
agent: Explore
---

Research the codebase thoroughly without polluting main context.
```

### With Hooks

```markdown
---
description: Deploy with validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy.sh"
          once: true
---

Deploy current branch to staging.
```

---

## Sources

- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows)
