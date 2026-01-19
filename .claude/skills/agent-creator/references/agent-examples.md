# Real-World Agent Examples

Examples from existing Claude Code agent implementations demonstrating best practices and patterns.

---

## Example 1: Plugin Assessor (Complex, Skill-Enhanced)

**Source**: `.claude/agents/plugin-assessor.md`

This agent demonstrates:
- Loading multiple skills for domain expertise
- Comprehensive phased workflow
- Detailed report format specification
- XML tags for structure

```yaml
---
name: plugin-assessor
description: >
  Analyze Claude Code plugins for structural correctness, frontmatter optimization,
  schema compliance, and enhancement opportunities. Use when reviewing plugins before
  marketplace submission, auditing existing plugins, validating plugin structure,
  or identifying improvements. Handles large plugins with many reference files.
  Detects orphaned documentation, duplicate content, and missing cross-references.
model: sonnet
skills: claude-skills-overview-2026, claude-plugins-reference-2026, claude-commands-reference-2026, claude-hooks-reference-2026
---
```

**Key Patterns:**
- Description includes multiple trigger phrases ("Use when reviewing", "auditing", "validating", "identifying")
- Loads 4 skills for comprehensive domain knowledge
- Uses sonnet for balanced capability

---

## Example 2: Code Review (Focused, Read-Implicit)

**Source**: `.claude/agents/code-review.md`

This agent demonstrates:
- Restricted invocation (user-only, not proactive)
- Clear input/output format
- Practical focus on "realness" of issues
- Categorized findings with severity levels

```yaml
---
name: code-review
description: Use ONLY when explicitly requested by user or when invoked by a protocol in sessions/protocols/. DO NOT use proactively. Reviews code for security vulnerabilities, bugs, performance issues, and adherence to project patterns during context compaction or pre-commit reviews. When using this agent, you must provide files and line ranges where code has been implemented along with the task file the code changes were made to satisfy. You may also give additional notes as necessary.
---
```

**Key Patterns:**
- Description explicitly states invocation conditions ("ONLY when explicitly requested")
- Specifies required inputs ("files and line ranges", "task file")
- Inherits default model and tools (appropriate for code review)

---

## Example 3: Context Optimizer (Specialized Domain)

**Source**: `.claude/agents/claude-context-optimizer.md`

This agent demonstrates:
- Description with embedded examples
- Skill activation as first action
- Clear optimization principles
- Structured output format

```yaml
---
name: claude-context-optimizer
description: Use this agent when the user wants to improve, rewrite, or optimize prompts, SKILL.md, CLAUDE.md files for better Claude comprehension and response quality. This includes refining system prompts, user instructions, agent configurations, or any text meant to guide AI behavior.
model: sonnet
color: yellow
---
```

**Key Patterns:**
- Uses `color` field for visual distinction
- Description includes specific file types it handles
- References skill to load for domain knowledge

---

## Example 4: Doc Drift Auditor (Git Forensics)

**Source**: `.claude/agents/doc-drift-auditor.md`

This agent demonstrates:
- Description with inline examples (unusual but effective)
- Comprehensive expertise areas
- Evidence-based reporting requirements
- Clear boundaries (what it must NOT do)

```yaml
---
name: doc-drift-auditor
description: Use when verifying documentation accuracy against actual implementation or investigating gaps between code and docs. Analyzes git history to identify when code and documentation diverged, extracts actual features from source code, compares against documentation claims, and generates comprehensive audit reports categorizing drift (implemented but undocumented, documented but unimplemented, outdated documentation, mismatched details). Uses git forensics, code analysis, and evidence-based reporting with specific file paths, line numbers, and commit SHAs.
model: sonnet
color: orange
---
```

**Key Patterns:**
- Very detailed description explaining methodology
- Lists specific outputs (file paths, line numbers, commit SHAs)
- Uses `color: orange` for audit visibility

---

## Example 5: Skill Refactorer (Modification Agent)

**Source**: `.claude/agents/skill-refactorer.md`

This agent demonstrates:
- `permissionMode: acceptEdits` for automated file changes
- Loading skill for domain knowledge
- Phased workflow with user confirmation points
- Validation and reporting phases

```yaml
---
name: skill-refactorer
description: >
  Refactor large or multi-domain skills into smaller, focused skills without losing fidelity.
  Use when a skill covers too many topics, exceeds 500 lines, or would benefit from
  separation of concerns. Analyzes skill content, identifies logical partitions,
  plans the split, creates new SKILL.md files, and validates complete coverage.
model: sonnet
permissionMode: acceptEdits
skills: claude-skills-overview-2026
---
```

**Key Patterns:**
- Uses `permissionMode: acceptEdits` since it creates/modifies files
- Loads relevant skill for understanding skill format
- Description specifies when to use ("exceeds 500 lines", "multiple topics")
- Mentions both analysis and creation capabilities

---

## Example 6: Context Gathering (Research Agent)

**Source**: `.claude/agents/context-gathering.md`

This agent demonstrates:
- Minimal frontmatter (inherits most settings)
- Clear restriction on output (ONLY edit task file)
- Comprehensive narrative output format
- Self-verification checklist

```yaml
---
name: context-gathering
description: Use when creating a new task OR when starting/switching to a task that lacks a context manifest. ALWAYS provide the task file path so the agent can read it and update it directly with the context manifest. Skip if task file already contains "Context Manifest" section.
---
```

**Key Patterns:**
- Very specific trigger conditions
- States what to skip (already has Context Manifest)
- Requires specific input (task file path)
- Inherits all defaults (appropriate for this use case)

---

## Pattern Summary

### Frontmatter Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| Minimal frontmatter | context-gathering | Agent needs flexibility, inherits well |
| Skill loading | plugin-assessor | Needs domain knowledge |
| Permission mode | skill-refactorer | Creates/modifies files |
| Color coding | doc-drift-auditor | Visual distinction helpful |
| Detailed description | doc-drift-auditor | Complex trigger conditions |

### Body Structure Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| Phased workflow | plugin-assessor | Multi-step process |
| Checklist | code-review | Quality validation |
| Boundaries section | doc-drift-auditor | Must clarify limits |
| Output format spec | code-review | Consistent output needed |
| Self-verification | context-gathering | Quality assurance |

### Description Patterns

| Pattern | Example | Effect |
|---------|---------|--------|
| Action verbs first | "Analyze", "Review", "Generate" | Clear purpose |
| "Use when" phrase | Most agents | Trigger clarity |
| "DO NOT" instruction | code-review | Prevent unwanted activation |
| Input requirements | context-gathering | Clear expectations |
| Output description | doc-drift-auditor | Sets expectations |

---

## Anti-Patterns Observed

### Avoid These

1. **Vague descriptions** - "Helps with code" doesn't guide delegation
2. **Missing invocation triggers** - When should Claude use this?
3. **Over-broad responsibilities** - One agent doing everything
4. **Missing tool restrictions** - Read-only agents inheriting write access
5. **Assuming skill inheritance** - Skills must be explicitly loaded

### Do These

1. **Specific action verbs** - "Review", "Generate", "Audit", "Debug"
2. **Clear trigger phrases** - "Use when", "Invoke for", "After completing"
3. **Focused responsibilities** - One agent, one domain
4. **Appropriate tool access** - Match tools to actual needs
5. **Explicit skill loading** - List all needed skills
