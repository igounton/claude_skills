# Prompt Optimization for Claude 4.5

Makes your instructions to Claude more effective by transforming them into patterns that Claude understands better.

## Why Install This?

When you write instructions for Claude (in CLAUDE.md files or custom skills), you might write things like:

- "NEVER use cat or grep commands"
- "Don't state timelines or estimates"
- "Format code properly"
- "Handle errors correctly"

These instructions seem clear to humans, but they have problems:

1. **Negative framing confuses Claude**: "NEVER use X" still activates the concept of X in Claude's processing
2. **Vague guidance gives inconsistent results**: "Format properly" means different things each time
3. **Missing motivation reduces effectiveness**: Claude doesn't understand why rules matter

Without this plugin, your instructions might be ignored or misinterpreted, leading to frustrating results.

## What Changes

With this plugin installed, when you ask Claude to review or improve your CLAUDE.md or skill files, Claude will:

- Rewrite negative prohibitions into positive instructions
- Replace vague guidance with specific, concrete rules
- Add brief explanations for why each rule exists
- Provide 2-3 concrete examples for complex behaviors
- Organize instructions under clear headings
- Optimize specifically for Claude 4.5's communication style

## Installation

```bash
/plugin install prompt-optimization-claude-45
```

## Usage

The plugin activates automatically when you:

- Ask Claude to review your CLAUDE.md file
- Request improvements to custom skills
- Create new instructions for Claude Code projects
- Optimize existing project documentation

Just ask: "Review my CLAUDE.md and suggest improvements" or "Help me write better instructions for this skill."

## Example

**Before this plugin**: You write in CLAUDE.md:

```markdown
NEVER use cat, head, tail commands
Don't state timelines
Format code properly
```

**After this plugin**: Claude transforms it to:

```markdown
## Tool Selection
| Operation | Tool | Reason |
|-----------|------|--------|
| Read files | Read() | Handles encoding and large files correctly |
| Search files | Grep() | Returns structured matches with context |

## Communication Style
- Lead with observations and findings
- Acknowledge dependencies when uncertain about duration

## Code Standards
- Use 2-space indentation for all code
- Place opening braces on same line as declaration
```

See the difference? The new version tells Claude exactly what to DO, includes specific rules instead of vague guidance, and explains WHY each rule matters.

## Requirements

- Claude Code v2.0+
- Works best with Claude Sonnet 4.5 or later models

## What Gets Optimized

This plugin helps optimize:

- CLAUDE.md project instruction files
- Custom skill documentation (SKILL.md files)
- Command descriptions and prompts
- Any instructions you write for Claude Code

The result: Claude follows your instructions more consistently and produces better results.
