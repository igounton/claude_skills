---
name: claude-skills-overview-2026
description: Reference guide for Claude Code skills system (January 2026). Use when creating, modifying, or understanding skills, SKILL.md format, frontmatter fields, hooks, context fork, or skill best practices.
---

# Claude Code Skills System - Complete Reference (January 2026)

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They are **model-invoked**: Claude automatically decides which skills to use based on your request.

---

## SKILL.md Complete Format

```yaml
---
name: skill-identifier
description: What this Skill does and when to use it
allowed-tools: Read, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
user-invocable: true
disable-model-invocation: false
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

# Skill Title

Your instructions here...
```

---

## All Frontmatter Fields

| Field | Required | Type | Max Length | Description |
|-------|----------|------|------------|-------------|
| `name` | **Yes** | string | 64 chars | Unique identifier: lowercase letters, numbers, hyphens only |
| `description` | **Yes** | string | 1024 chars | Claude uses this to decide when to apply the Skill |
| `allowed-tools` | No | string/array | — | Tools Claude can use: `Read, Grep, Glob, Bash(npm run:*)` |
| `model` | No | string | — | Override model: `claude-opus-4-5-20251101`, `claude-sonnet-4-20250514` |
| `context` | No | string | — | Set to `fork` for isolated sub-agent context |
| `agent` | No | string | — | With `context: fork`: `Explore`, `Plan`, `general-purpose`, or custom agent |
| `user-invocable` | No | boolean | — | Show in slash command menu (default: `true`) |
| `disable-model-invocation` | No | boolean | — | Block `Skill` tool from calling this programmatically |
| `hooks` | No | object | — | Scoped hooks: `PreToolUse`, `PostToolUse`, `Stop` |

---

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed to the Skill |
| `${CLAUDE_SESSION_ID}` | Current session ID for logging |

---

## Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional: docs loaded on demand
├── scripts/              # Optional: executed, not loaded into context
└── templates/            # Optional: reusable content
```

### Location Priority (Highest to Lowest)

1. **Managed/Enterprise** - System-level
2. **Personal** - `~/.claude/skills/`
3. **Project** - `.claude/skills/`
4. **Plugin** - Bundled with plugins

---

## Hooks in Skills

### Hook Events

- `PreToolUse`: Before tool executes
- `PostToolUse`: After successful execution
- `Stop`: When Skill finishes

### Hook Structure

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"           # Regex pattern
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true            # Run only once per session
```

### Hook I/O

- Receives JSON via stdin (session info, tool name, parameters)
- Exit 0: Success
- Exit 2: Blocking error (prevents tool, shows stderr)
- Other: Non-blocking error

---

## context: fork Options

```yaml
context: fork
agent: Explore
```

| Agent | Model | Tools | Use Case |
|-------|-------|-------|----------|
| `Explore` | Haiku | Read-only | Fast codebase analysis |
| `Plan` | Inherits | Read-only | Research before planning |
| `general-purpose` | Inherits | All tools | Complex operations (default) |
| Custom | Custom | Custom | Project-specific work |

---

## Description Best Practices

**Good**:
```yaml
description: Extract text and tables from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, extraction.
```

**Bad**:
```yaml
description: Helps with documents
```

**Template**:
```
[Action 1], [Action 2], [Action 3]. Use when [situation 1], [situation 2],
or when the user mentions [keywords].
```

---

## Examples

### Simple Skill

```yaml
---
name: commit-messages
description: Generate conventional commit messages from git diffs. Use when writing commits.
---

# Commit Messages

1. Run `git diff --staged`
2. Determine type (feat, fix, docs)
3. Write message under 50 chars
4. Use imperative mood
```

### Tool-Restricted

```yaml
---
name: safe-reader
description: Read files without changes. Use for code review.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Safe Reader

ONLY read files. Never modify.
```

### Forked Context

```yaml
---
name: deep-research
description: Thorough codebase research. Use for complex investigations.
context: fork
agent: Explore
---

# Deep Research

Runs in isolated context to avoid polluting main conversation.
```

### With Hooks

```yaml
---
name: secure-ops
description: Audit-logged file operations.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---

# Secure Operations

All modifications logged and validated.
```

### Hidden from Users

```yaml
---
name: internal-standards
description: Auto-apply code review standards.
user-invocable: false
---

Claude invokes this, users don't see it in menu.
```

### User-Only (No Auto-Invoke)

```yaml
---
name: deploy-production
description: Deploy to production.
disable-model-invocation: true
---

Only runs when user types `/deploy-production`.
```

---

## Skills vs Other Features

| Feature | Invocation | Use Case |
|---------|------------|----------|
| **Skills** | Claude decides | Specialized knowledge/workflows |
| **Slash Commands** | User types `/command` | Simple reusable prompts |
| **CLAUDE.md** | Always loaded | Project-wide instructions |
| **Subagents** | Claude delegates | Isolated complex operations |
| **MCP Servers** | Claude calls | External tools/data |
| **Hooks** | Tool events | Automate actions |

---

## Installation

**Marketplace**:
```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**Manual**: Copy to `~/.claude/skills/` or `.claude/skills/`

**Hot Reload**: Changes apply immediately without restart.

---

## Recent Updates (2.1+)

- `once: true` for hooks - run only once per session
- `${CLAUDE_SESSION_ID}` - session-scoped operations
- 15,000 character budget for skill metadata
- `context: fork` with agent selection
- Hot reload - immediate updates
- Unified commands/skills

---

## Sources

- [Agent Skills Docs](https://code.claude.com/docs/en/skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
