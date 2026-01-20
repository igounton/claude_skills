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
| `PreCompact`        | Before context compaction       | Yes             | State backup           |
| `SessionStart`      | Session begins or resumes       | Yes             | Environment setup      |
| `SessionEnd`        | Session ends                    | No              | Cleanup, persistence   |

---

## Event-Specific Matchers

### SessionStart Matchers

| Matcher   | Trigger                                |
| --------- | -------------------------------------- |
| `startup` | New session started                    |
| `resume`  | `--resume`, `--continue`, or `/resume` |
| `clear`   | `/clear` command                       |
| `compact` | Auto or manual compact                 |

### PreCompact Matchers

| Matcher  | Trigger                     |
| -------- | --------------------------- |
| `manual` | `/compact` command          |
| `auto`   | Auto-compact (full context) |

### Notification Matchers

| Matcher              | Trigger                              |
| -------------------- | ------------------------------------ |
| `permission_prompt`  | Permission requests from Claude      |
| `idle_prompt`        | Claude waiting for input (60s+ idle) |
| `auth_success`       | Authentication success               |
| `elicitation_dialog` | MCP tool elicitation                 |

### Tool Matchers (PreToolUse, PermissionRequest, PostToolUse)

| Pattern            | Matches                          |
| ------------------ | -------------------------------- |
| `Write`            | Exact match (case-sensitive)     |
| `Edit\|Write`      | Either Edit or Write             |
| `Notebook.*`       | NotebookEdit, NotebookRead, etc. |
| `mcp__.*__write.*` | MCP write tools                  |
| `mcp__memory__.*`  | All memory server tools          |
| `*` or `""`        | All tools                        |

**MCP Tool Naming**: `mcp__<server>__<tool>` (e.g., `mcp__github__search_repositories`)

---

## Configuration Locations

### Precedence (highest to lowest)

1. **Managed** - `managed-settings.json` (enterprise)
2. **Local** - `.claude/settings.local.json` (gitignored)
3. **Project** - `.claude/settings.json` (shared via git)
4. **User** - `~/.claude/settings.json` (personal)
5. **Plugin** - `hooks/hooks.json` or frontmatter
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
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/setup.js\""
          }
        ]
      }
    ]
  }
}
```

### Frontmatter Format (Skills/Commands/Agents)

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

**Supported events in frontmatter**: `PreToolUse`, `PostToolUse`, `Stop`

**`once` option**: Only available in Skills/Commands frontmatter. Runs hook once per session.

---

## Hook Structure

```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "./scripts/validate.sh",
      "timeout": 60
    }
  ]
}
```

### Fields

| Field     | Type    | Required         | Description                                 |
| --------- | ------- | ---------------- | ------------------------------------------- |
| `matcher` | string  | For some events  | Regex pattern (case-sensitive)              |
| `type`    | string  | Yes              | `command` or `prompt`                       |
| `command` | string  | For command type | Shell command to execute                    |
| `prompt`  | string  | For prompt type  | LLM prompt for evaluation                   |
| `timeout` | number  | No               | Seconds (default: 60)                       |
| `once`    | boolean | No               | Run once per session (Skills/Commands only) |

---

## Hook Input (JSON via stdin)

### Common Fields (All Events)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

### PreToolUse Input

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies",
    "timeout": 120000
  },
  "tool_use_id": "toolu_01ABC123"
}
```

**Tool-specific `tool_input` fields:**

| Tool    | Fields                                                   |
| ------- | -------------------------------------------------------- |
| `Bash`  | `command`, `description`, `timeout`, `run_in_background` |
| `Write` | `file_path`, `content`                                   |
| `Edit`  | `file_path`, `old_string`, `new_string`, `replace_all`   |
| `Read`  | `file_path`, `offset`, `limit`                           |

### PostToolUse Input

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path/to/file.txt", "content": "..." },
  "tool_response": { "filePath": "/path/to/file.txt", "success": true },
  "tool_use_id": "toolu_01ABC123"
}
```

### Notification Input

```json
{
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "notification_type": "permission_prompt"
}
```

### UserPromptSubmit Input

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate factorial"
}
```

### Stop / SubagentStop Input

```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

**`stop_hook_active`**: True when Claude is already continuing due to a stop hook. Check this to prevent infinite loops.

### PreCompact Input

```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### SessionStart Input

```json
{
  "hook_event_name": "SessionStart",
  "source": "startup"
}
```

### SessionEnd Input

```json
{
  "hook_event_name": "SessionEnd",
  "reason": "exit"
}
```

**`reason` values**: `clear`, `logout`, `prompt_input_exit`, `other`

---

## Hook Output

### Exit Codes

| Code  | Behavior                                        |
| ----- | ----------------------------------------------- |
| 0     | Success - stdout processed (JSON or plain text) |
| 2     | Blocking error - stderr shown, action blocked   |
| Other | Non-blocking error - stderr in verbose mode     |

### Exit Code 2 Behavior Per Event

| Event               | Exit Code 2 Behavior                           |
| ------------------- | ---------------------------------------------- |
| `PreToolUse`        | Blocks tool call, shows stderr to Claude       |
| `PermissionRequest` | Denies permission, shows stderr to Claude      |
| `PostToolUse`       | Shows stderr to Claude (tool already ran)      |
| `Notification`      | Shows stderr to user only                      |
| `UserPromptSubmit`  | Blocks prompt, erases it, shows stderr to user |
| `Stop`              | Blocks stoppage, shows stderr to Claude        |
| `SubagentStop`      | Blocks stoppage, shows stderr to subagent      |
| `PreCompact`        | Shows stderr to user only                      |
| `SessionStart`      | Shows stderr to user only                      |
| `SessionEnd`        | Shows stderr to user only                      |

---

## JSON Output Control

**Important**: JSON output is only processed with exit code 0. Exit code 2 uses stderr only.

### Common JSON Fields (All Events)

```json
{
  "continue": true,
  "stopReason": "Message if continue is false",
  "suppressOutput": false,
  "systemMessage": "Optional warning to user"
}
```

| Field            | Type    | Effect                                  |
| ---------------- | ------- | --------------------------------------- |
| `continue`       | boolean | `false` stops Claude (takes precedence) |
| `stopReason`     | string  | Shown to user when `continue` is false  |
| `suppressOutput` | boolean | Hide stdout from transcript mode        |
| `systemMessage`  | string  | Warning message shown to user           |

### PreToolUse JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved documentation file",
    "updatedInput": { "file_path": "/modified/path" },
    "additionalContext": "Current environment: production"
  }
}
```

| Field                      | Values                 | Effect                                     |
| -------------------------- | ---------------------- | ------------------------------------------ |
| `permissionDecision`       | `allow`, `deny`, `ask` | Controls tool execution                    |
| `permissionDecisionReason` | string                 | Shown to user (allow/ask) or Claude (deny) |
| `updatedInput`             | object                 | Modifies tool input                        |
| `additionalContext`        | string                 | Added to Claude's context                  |

**Note**: `decision` and `reason` fields are deprecated. Use `hookSpecificOutput`.

### PermissionRequest JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": { "command": "npm run lint" }
    }
  }
}
```

For deny:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "Command not allowed",
      "interrupt": true
    }
  }
}
```

### PostToolUse JSON Output

```json
{
  "decision": "block",
  "reason": "Linting errors found",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Fix the 3 ESLint errors before proceeding"
  }
}
```

### UserPromptSubmit JSON Output

```json
{
  "decision": "block",
  "reason": "Prompt contains sensitive data",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Current time: 2026-01-20T10:30:00Z"
  }
}
```

**Note**: Plain text stdout (exit code 0) is also added to context. JSON not required for simple cases.

### Stop / SubagentStop JSON Output

```json
{
  "decision": "block",
  "reason": "Tests not yet run - please execute test suite"
}
```

### SessionStart JSON Output

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Project context: Node.js 20, TypeScript 5.3"
  }
}
```

**Note**: Multiple hooks' `additionalContext` values are concatenated.

---

## Prompt-Based Hooks

LLM-evaluated decisions using a fast model (Haiku).

### How Prompt-Based Hooks Work

Instead of executing a bash command, prompt-based hooks:

1. Send the hook input and your prompt to Haiku
2. The LLM responds with structured JSON containing a decision
3. Claude Code processes the decision automatically

### Configuration

```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

| Field     | Required | Description             |
| --------- | -------- | ----------------------- |
| `type`    | Yes      | Must be `"prompt"`      |
| `prompt`  | Yes      | Prompt text sent to LLM |
| `timeout` | No       | Seconds (default: 30)   |

### Response Schema

The LLM must respond with JSON:

```json
{
  "ok": true,
  "reason": "Explanation for the decision"
}
```

| Field    | Type    | Description                                    |
| -------- | ------- | ---------------------------------------------- |
| `ok`     | boolean | `true` allows the action, `false` prevents it  |
| `reason` | string  | Required when `ok` is `false`. Shown to Claude |

### $ARGUMENTS Placeholder

Use `$ARGUMENTS` in prompt to include hook input JSON. If omitted, input is appended to the prompt.

### Example: Intelligent Stop Hook

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Example: SubagentStop Validation

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this subagent should stop. Input: $ARGUMENTS\n\nCheck if:\n- The subagent completed its assigned task\n- Any errors occurred that need fixing\n- Additional context gathering is needed\n\nReturn: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"explanation\"} to continue."
          }
        ]
      }
    ]
  }
}
```

### Best Use Cases

| Event               | Use Case                              |
| ------------------- | ------------------------------------- |
| `Stop`              | Intelligent task completion detection |
| `SubagentStop`      | Verify subagent completed task        |
| `UserPromptSubmit`  | Context-aware prompt validation       |
| `PreToolUse`        | Complex permission decisions          |
| `PermissionRequest` | Intelligent allow/deny dialogs        |

### Comparison with Command Hooks

| Aspect            | Command Hooks       | Prompt Hooks            |
| ----------------- | ------------------- | ----------------------- |
| Execution         | Runs shell script   | Queries LLM (Haiku)     |
| Decision logic    | You implement       | LLM evaluates context   |
| Setup             | Requires script     | Configure prompt only   |
| Context awareness | Limited             | Full understanding      |
| Performance       | Fast (local)        | Slower (API call)       |
| Use case          | Deterministic rules | Context-aware decisions |

### Best Practices for Prompt Hooks

1. **Be specific in prompts** - Clearly state what you want the LLM to evaluate
2. **Include decision criteria** - List the factors the LLM should consider
3. **Test your prompts** - Verify the LLM makes correct decisions for your use cases
4. **Set appropriate timeouts** - Default is 30 seconds, adjust if needed
5. **Use for complex decisions** - Bash hooks are better for simple, deterministic rules

---

## Environment Variables

| Variable             | Description                        | Available In      |
| -------------------- | ---------------------------------- | ----------------- |
| `CLAUDE_PROJECT_DIR` | Project root (absolute path)       | All hooks         |
| `CLAUDE_CODE_REMOTE` | `"true"` if remote, empty if local | All hooks         |
| `CLAUDE_ENV_FILE`    | Path for persisting env vars       | SessionStart only |
| `CLAUDE_PLUGIN_ROOT` | Plugin directory (absolute)        | Plugin hooks      |

### SessionStart Environment Persistence

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

Variables in `$CLAUDE_ENV_FILE` are sourced before each Bash command.

---

## Execution Details

| Aspect              | Behavior                                |
| ------------------- | --------------------------------------- |
| **Parallelization** | All matching hooks run in parallel      |
| **Deduplication**   | Identical commands deduplicated         |
| **Timeout**         | 60 seconds default, configurable        |
| **Environment**     | Runs in cwd with Claude Code's env      |
| **Hook order**      | Hooks from all sources execute together |

### Output Handling by Event

| Event                          | stdout Handling                  |
| ------------------------------ | -------------------------------- |
| UserPromptSubmit, SessionStart | Added to Claude's context        |
| PreToolUse, PostToolUse, Stop  | Shown in verbose mode (Ctrl+O)   |
| Notification, SessionEnd       | Logged to debug only (`--debug`) |

---

## Security Considerations

**USE AT YOUR OWN RISK**: Hooks execute arbitrary shell commands. You are responsible for:

- Commands you configure
- File access (hooks can access anything your user can)
- Preventing data loss from malicious or poorly written hooks

### Best Practices

1. **Validate and sanitize inputs** - Never trust input blindly
2. **Always quote shell variables** - Use `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..` in file paths
4. **Use absolute paths** - Use `$CLAUDE_PROJECT_DIR` for project paths
5. **Skip sensitive files** - Avoid `.env`, `.git/`, keys

### Configuration Safety

- Hooks snapshot captured at startup
- External modifications warn user
- Changes require `/hooks` menu review

---

## Debugging

### Enable Debug Mode

```bash
claude --debug
claude --debug "hooks"  # Filter to hooks only
```

### Debug Output

```text
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Hook command completed with status 0: <output>
```

### Common Issues

| Problem            | Cause                 | Fix                           |
| ------------------ | --------------------- | ----------------------------- |
| Hook not running   | Wrong matcher pattern | Check case-sensitivity, regex |
| Command not found  | Relative path         | Use `$CLAUDE_PROJECT_DIR`     |
| JSON not processed | Non-zero exit code    | Exit 0 for JSON processing    |
| Hook times out     | Slow script           | Optimize or increase timeout  |
| Quotes breaking    | Unescaped in JSON     | Use `\"` inside JSON strings  |

### Test Commands Manually

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | ./your-hook.sh
```

---

## Examples

### Auto-Approve Documentation Reads

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/auto-approve-docs.js\""
          }
        ]
      }
    ]
  }
}
```

### SessionStart Context Injection

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/inject-context.js\""
          }
        ]
      }
    ]
  }
}
```

### Intelligent Stop Hook

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze if all tasks are complete. Context: $ARGUMENTS\n\nReturn {\"ok\": true} to stop, {\"ok\": false, \"reason\": \"...\"} to continue."
          }
        ]
      }
    ]
  }
}
```

### MCP Tool Validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-mcp-write.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Sources

- [Hooks Reference](https://code.claude.com/docs/en/hooks) (January 2026)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Settings Reference](https://code.claude.com/docs/en/settings)
