---
name: claude-hooks-reference-2026
description: Reference guide for Claude Code hooks system (January 2026). Use when creating hooks, understanding hook events, matchers, exit codes, JSON output control, environment variables, or hook best practices.
---

# Claude Code Hooks System - Complete Reference (January 2026)

Hooks execute custom commands or prompts in response to Claude Code events. Use for automation, validation, formatting, and security.

---

## All Hook Events

| Event               | When Fired                      | Matcher Applies | Common Uses            |
| ------------------- | ------------------------------- | --------------- | ---------------------- |
| `PreToolUse`        | Before tool execution           | Yes             | Validation, blocking   |
| `PermissionRequest` | When Claude requests permission | Yes             | Auto-approval policies |
| `PostToolUse`       | After successful tool execution | Yes             | Formatting, linting    |
| `Notification`      | When Claude wants attention     | Yes             | Custom notifications   |
| `UserPromptSubmit`  | User submits prompt             | No              | Input validation       |
| `Stop`              | Claude finishes response        | No              | Cleanup, final checks  |
| `SubagentStop`      | Subagent completes              | No              | Result validation      |
| `PreCompact`        | Before context compaction       | No              | State backup           |
| `SessionStart`      | Session begins                  | No              | Environment setup      |
| `SessionEnd`        | Session ends                    | No              | Cleanup, persistence   |

---

## Configuration Locations

### Precedence (highest to lowest)

1. **Managed** - `managed-settings.json` (enterprise)
2. **Local** - `.claude/settings.local.json` (gitignored)
3. **Project** - `.claude/settings.json` (shared via git)
4. **User** - `~/.claude/settings.json` (personal)
5. **Plugin** - `hooks.json` or frontmatter
6. **Capability** - Skill/Command/Agent frontmatter

### Settings.json Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/cleanup.sh"
          }
        ]
      }
    ]
  }
}
```

### Frontmatter Format

```yaml
---
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---
```

---

## Hook Structure

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "./scripts/validate.sh",
      "timeout": 60,
      "once": true
    }
  ]
}
```

### Fields

| Field     | Type    | Required         | Description                                 |
| --------- | ------- | ---------------- | ------------------------------------------- |
| `matcher` | string  | For tool events  | Regex pattern (case-sensitive)              |
| `type`    | string  | Yes              | `command` or `prompt`                       |
| `command` | string  | For command type | Bash command                                |
| `prompt`  | string  | For prompt type  | LLM prompt                                  |
| `timeout` | number  | No               | Seconds (default: 60)                       |
| `once`    | boolean | No               | Run once per session (Skills/Commands only) |

---

## Matcher Syntax

| Pattern            | Matches                          |
| ------------------ | -------------------------------- |
| `Write`            | Exact match (case-sensitive)     |
| `Edit\|Write`      | Either Edit or Write             |
| `Notebook.*`       | NotebookEdit, NotebookRead, etc. |
| `mcp__.*__write.*` | MCP write tools                  |
| `*` or `""`        | All tools                        |

**Not applicable to**: UserPromptSubmit, Stop, SubagentStop, PreCompact, SessionStart, SessionEnd

---

## Hook I/O

### Input (JSON via stdin)

```json
{
  "session_id": "abc123",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "content": "..."
  },
  "tool_use_id": "toolu_123",
  "permission_mode": "default"
}
```

### Exit Codes

| Code  | Behavior                                       |
| ----- | ---------------------------------------------- |
| 0     | Success - execution continues                  |
| 2     | Blocking error - prevents action, shows stderr |
| Other | Non-blocking error - stderr in verbose mode    |

---

## JSON Output Control

For advanced control, output JSON to stdout:

### PreToolUse Response

```json
{
  "decision": "allow",
  "reason": "Validation passed",
  "updatedInput": { "modified": "input" }
}
```

| Field          | Values                  | Effect                   |
| -------------- | ----------------------- | ------------------------ |
| `decision`     | `allow`, `block`, `ask` | Controls tool execution  |
| `reason`       | string                  | Shown to user if blocked |
| `updatedInput` | object                  | Modifies tool input      |

### Stop/SubagentStop Response

```json
{
  "decision": "continue",
  "reason": "Task incomplete",
  "additionalContext": "More details..."
}
```

| Field               | Values             | Effect                 |
| ------------------- | ------------------ | ---------------------- |
| `decision`          | `continue`, `stop` | Continue or stop agent |
| `reason`            | string             | Shown if continuing    |
| `additionalContext` | string             | Added to context       |

### Override Field

```json
{
  "continue": false
}
```

`continue: false` forces stop regardless of other fields.

---

## Prompt-Based Hooks

LLM-evaluated decisions (Stop/SubagentStop only).

```json
{
  "type": "prompt",
  "prompt": "Verify the task was completed correctly. Check for edge cases. Return {\"ok\": true} if satisfied, {\"ok\": false, \"reason\": \"...\"} otherwise."
}
```

**Use for**: Context-aware validation, complex decision logic

---

## Environment Variables

| Variable             | Description                        | Available In      |
| -------------------- | ---------------------------------- | ----------------- |
| `CLAUDE_PROJECT_DIR` | Project root (absolute path)       | All hooks         |
| `CLAUDE_CODE_REMOTE` | `"true"` if remote, empty if local | All hooks         |
| `CLAUDE_ENV_FILE`    | Path for persisting env vars       | SessionStart only |
| `CLAUDE_PLUGIN_ROOT` | Plugin directory (absolute)        | Plugin hooks      |

### Using in Commands

```bash
#!/bin/bash
"$CLAUDE_PROJECT_DIR/scripts/validate.sh"
```

---

## Execution Details

| Aspect              | Behavior                                |
| ------------------- | --------------------------------------- |
| **Parallelization** | All matching hooks run in parallel      |
| **Deduplication**   | Identical commands deduplicated         |
| **Timeout**         | 60 seconds default per command          |
| **Hook order**      | Hooks from all sources execute together |

---

## SessionStart for Environment

Persist environment variables across Bash commands:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

The file at `$CLAUDE_ENV_FILE` is sourced before each Bash command.

---

## Best Practices

1. **Use `$CLAUDE_PROJECT_DIR`** for project-relative paths
2. **Quote shell variables** to handle spaces
3. **Validate/sanitize JSON input** in scripts
4. **Use JSON output** for complex control logic
5. **Implement logging** for debugging
6. **Test in safe environments** before production
7. **Use prompt-based hooks** for context-aware decisions
8. **Use bash hooks** for deterministic rules
9. **Keep hooks fast** - timeout is 60 seconds
10. **Use `once: true`** for one-time setup in Skills/Commands

---

## Examples

### Code Formatting

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_PROJECT_DIR\"/**/*.{js,ts,json}"
          }
        ]
      }
    ]
  }
}
```

### File Protection

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/check-protected-files.sh"
          }
        ]
      }
    ]
  }
}
```

### Custom Notifications

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs attention\"'"
          }
        ]
      }
    ]
  }
}
```

### Task Verification

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion. Check edge cases. Return {\"ok\": true} or {\"ok\": false, \"reason\": \"...\"}."
          }
        ]
      }
    ]
  }
}
```

### Plugin Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Sources

- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Settings Reference](https://code.claude.com/docs/en/settings)
