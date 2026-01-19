# Memory Bank MCP Quick Start Guide

**For**: Developers using Memory Bank MCP with python_picotool project
**Based On**: Official Memory Bank MCP documentation + verified implementation
**Last Updated**: 2025-11-15

---

## What Is Memory Bank MCP?

Memory Bank MCP is a Model Context Protocol server that provides persistent memory storage for AI assistants. It stores project information in structured files that the assistant reads before every task.

**Key Benefit**: AI assistants can remember project context between sessions, enabling:

- Consistent decision-making
- Reduced context repetition
- Accumulated project knowledge
- Multi-session continuity

---

## Understanding Context Types

Before installing, understand the three architectural layers:

### Three Types of Context

| Type                  | Location                                         | Portable? | Committed? | Purpose                                                                   |
| --------------------- | ------------------------------------------------ | --------- | ---------- | ------------------------------------------------------------------------- |
| **Capability Config** | `.mcp.json` (project) or `~/.claude.json` (user) | Yes       | Yes        | Enable Memory Bank MCP for all developers                                 |
| **Session Memory**    | `.memory-bank/` directory                        | No        | No         | Orchestrator discoveries, ephemeral findings, session-specific analysis   |
| **Curated Context**   | `AGENTS.md` (project root)                       | Yes       | Yes        | Universal AI assistant guidance, architecture decisions, coding standards |

**Key Insight**: `.mcp.json` is like `package.json` or `pyproject.toml` (shared config), while `.memory-bank/` is like `.pytest_cache` or `node_modules` (generated, local).

---

## Installation (Choose One Method)

### Option 1: Automated Installation (Recommended)

If using Claude Desktop:

```bash
npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude
```

This automatically configures Memory Bank MCP in your Claude settings.

### Option 2: Project-Scoped Installation (Recommended for Teams)

Enable Memory Bank MCP for all developers in the project:

```bash
claude mcp add --scope project \
  --env MEMORY_BANK_ROOT=$(pwd)/.memory-bank \
  memory-bank \
  npx -y @allpepper/memory-bank-mcp
```

This creates `.mcp.json` in your project root (portable with your repository) instead of modifying `~/.claude.json` (user-specific).

**Benefits**:

- All developers get the same Memory Bank configuration
- Configuration is version-controlled with the project
- No need for manual setup on each machine
- `.mcp.json` in `.gitignore` is NOT recommended (commit it like `package.json`)

### Option 3: Manual Setup for Cline (Cursor)

1. Open Cursor settings
2. Find MCP Settings
3. Add this configuration:

```json
{
    "allpepper-memory-bank": {
        "command": "npx",
        "args": ["-y", "@allpepper/memory-bank-mcp"],
        "env": {
            "MEMORY_BANK_ROOT": "/path/to/memory-bank"
        },
        "disabled": false,
        "autoApprove": [
            "memory_bank_read",
            "memory_bank_write",
            "memory_bank_update",
            "list_projects",
            "list_project_files"
        ]
    }
}
```

Replace `/path/to/memory-bank` with your actual memory bank directory (e.g., `/home/user/repos/python_picotool/.memory-bank`).

### Option 4: Manual Setup for Claude Code CLI

1. Edit `~/.claude.json` (user scope) or `.mcp.json` (project scope)
2. Add to the `mcpServers` section:

```json
"allPepper-memory-bank": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@allpepper/memory-bank-mcp@latest"],
  "env": {
    "MEMORY_BANK_ROOT": "/path/to/memory-bank"
  }
}
```

---

## Repository Setup

### Add to .gitignore

Add this line to your repository's `.gitignore`:

```
.memory-bank/
```

**Reasoning**: The `.memory-bank/` directory contains session-specific discoveries and ephemeral AI findings, similar to:

- `node_modules/` - Generated dependencies
- `.pytest_cache/` - Generated test cache
- `__pycache__/` - Generated Python bytecode

**Why NOT exclude `.mcp.json`**:

- Unlike `.memory-bank/`, `.mcp.json` is configuration that enables the capability for all developers
- It should be committed (like `package.json` or `pyproject.toml`)
- All developers benefit from the same Memory Bank setup

### Commit .mcp.json

If using project-scoped installation, commit `.mcp.json`:

```bash
git add .mcp.json
git commit -m "config: add Memory Bank MCP configuration for team"
```

---

## Setting Up Memory Bank for Your Project

### Step 1: Create Memory Bank Directory

```bash
mkdir -p /path/to/project/.memory-bank/project-name
```

Example for python_picotool:

```bash
mkdir -p /home/user/repos/python_picotool/.memory-bank/python_picotool
```

### Step 2: Initialize Core Files

Create these files in `project-name/` directory:

**projectbrief.md**

```markdown
# Project Brief: python_picotool

## Overview

Brief description of the project.

## Key Goals

- Goal 1
- Goal 2

## Success Criteria

- Criterion 1
- Criterion 2
```

**productContext.md**

```markdown
# Product Context

## Problem Statement

What problem does this solve?

## Current Solution

How is it currently solved?

## Proposed Approach

What is the new approach?
```

**systemPatterns.md**

```markdown
# System Patterns

## Architecture

High-level system design.

## Key Patterns

- Pattern 1
- Pattern 2

## Design Decisions

Important architectural choices.
```

**techContext.md**

```markdown
# Technical Context

## Technology Stack

- Language: Python 3.11+
- Main frameworks: [List here]

## Setup Instructions

How to set up the development environment.

## Key Dependencies

- Dependency 1
- Dependency 2
```

**activeContext.md**

```markdown
# Active Context

## Current Focus

What are we currently working on?

## Active Issues

- Issue 1
- Issue 2

## Current Decisions

Important decisions made this session.
```

**progress.md**

```markdown
# Progress

## Completed

- Task 1
- Task 2

## In Progress

- Task 3

## Next Steps

- Task 4
- Task 5
```

**.clinerules**

```markdown
# Project Rules and Patterns

## Critical Implementation Paths

- Path 1
- Path 2

## Tool Usage Patterns

How to use specific tools in this project.

## Workflow Preferences

Preferred ways to accomplish common tasks.

## Project-Specific Decisions

Important decisions that affect development.
```

---

## Using Memory Bank in Your AI Assistant

### Command: "Follow Your Custom Instructions"

Type this to trigger the memory bank workflow:

```
Follow your custom instructions
```

This will:

1. Validate project structure
2. Load all memory bank files
3. Enter either Plan or Act mode
4. Read .clinerules for your project patterns
5. Apply learned patterns to current task

### Command: "Initialize Memory Bank"

Use this when setting up a new project:

```
Initialize memory bank
```

The system will:

1. Check if project directory exists
2. Create missing core files
3. Set up initial structure
4. Ready for first task

### Command: "Update Memory Bank"

Use this after significant changes:

```
Update memory bank
```

The system will:

1. Re-read all project files
2. Update based on current state
3. Capture new patterns
4. Synchronize context

---

## File Reading Order (Important)

The AI assistant should read files in this order:

1. **projectbrief.md** - Understand project goals
2. **productContext.md** - Understand problem domain
3. **systemPatterns.md** - Understand architecture
4. **techContext.md** - Understand tech stack
5. **activeContext.md** - Understand current work
6. **.clinerules** - Learn project patterns

---

## File Updating Order (Important)

Update files in reverse order:

1. **.clinerules** - Add new patterns
2. **activeContext.md** - Update current focus
3. **techContext.md** - Update if tech stack changes
4. **systemPatterns.md** - Update if architecture changes
5. **productContext.md** - Update if problem changes
6. **projectbrief.md** - Rarely changes
7. **progress.md** - Update to reflect work done

---

## Memory Bank Structure for python_picotool

Your memory bank directory will look like:

```
.memory-bank/
└── python_picotool/
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── activeContext.md
    ├── progress.md
    ├── .clinerules
    └── custom/                    (Optional)
        ├── api-design.md
        ├── deployment-guide.md
        └── testing-strategy.md
```

---

## Example: First Memory Bank Session

### Initial Setup

You say to your AI assistant:

```
Initialize memory bank for python_picotool project
```

The assistant:

1. Creates project directory if needed
2. Asks you for information
3. Fills in core files with your answers

### Using It

Next time, you say:

```
Follow your custom instructions
```

The assistant:

1. Reads all memory bank files
2. Understands project context
3. Applies learned patterns
4. Works more efficiently

---

## Adding Custom Files

You can add custom files for specific needs:

**Example: Feature Specifications**

```
.memory-bank/python_picotool/features/usb-communication.md
```

**Example: API Documentation**

```
.memory-bank/python_picotool/api/device-discovery.md
```

**Example: Deployment Guide**

```
.memory-bank/python_picotool/deployment/raspberry-pi-pico.md
```

**Important**: Reference custom files in `activeContext.md` when you add them.

---

## AGENTS.md vs Memory Bank: When to Use Which

### What is AGENTS.md?

`AGENTS.md` is a project-level file that provides universal AI assistant context. It works across multiple AI tools:

- Claude Code CLI
- Windsurf
- Cursor
- Cline
- Any AI assistant that accepts file references with `@` syntax

### When to Use AGENTS.md

Use AGENTS.md for information that is:

- **Shareable**: Works with all AI assistants in your project
- **Curated**: Human-reviewed and intentionally documented
- **Stable**: Architecture decisions, coding standards, conventions
- **Universal**: Not specific to one developer's session

**Examples**:

- Architecture patterns and design decisions
- Coding style and conventions
- Project setup and configuration
- Common workflows and best practices
- Security policies and requirements
- Technology choices and rationale

### When to Use Memory Bank

Use Memory Bank for information that is:

- **Ephemeral**: Session-to-session discoveries
- **Orchestrator-driven**: Findings from orchestrator-to-agent workflows
- **Generated**: AI findings, not human-curated
- **Local**: Specific to one developer's environment or session

**Examples**:

- Codebase analysis results from sessions
- Problem-solving discoveries and workarounds found
- Performance analysis or benchmarks from testing
- Bug investigations and solutions
- Experimental approaches that worked
- Progress tracking on long-running tasks

### Decision Tree

```
Does the information...

├─ Work across multiple AI assistants (Claude, Windsurf, Cursor)?
│  └─ YES → Use AGENTS.md
│  └─ NO  → Continue
│
├─ Describe architecture or design decisions?
│  └─ YES → Use AGENTS.md
│  └─ NO  → Continue
│
├─ Need to be human-reviewed before sharing?
│  └─ YES → Use AGENTS.md (or do review, then add)
│  └─ NO  → Continue
│
├─ Come from AI discovery/analysis (not human decision)?
│  └─ YES → Use Memory Bank
│  └─ NO  → Use AGENTS.md
│
└─ Continue to next session?
   └─ YES → Use Memory Bank (or AGENTS.md if it's stable knowledge)
   └─ NO  → Use Memory Bank (ephemeral findings)
```

### Example: AGENTS.md Reference in CLAUDE.md

If you have a project-specific `CLAUDE.md` file (for Claude Code CLI), reference AGENTS.md:

```markdown
# Project-Specific Claude Instructions

Follow the guidelines in @AGENTS.md for universal project context covering:

- Architecture patterns
- Coding conventions
- Project setup
- Common workflows

## Claude-Specific Rules

[Additional Claude-only execution rules here, such as tool usage preferences specific to Claude Code CLI]
```

**How it works**: Claude automatically includes `@AGENTS.md` in the context using file reference syntax.

---

## Common Tasks

### "I want the AI to remember this pattern"

1. Document the pattern in **.clinerules**
2. Include specific examples
3. Explain when to apply it
4. Ask AI to "update memory bank"

Example in .clinerules:

````markdown
## Pattern: Device Discovery

Always follow these steps:

1. Import device module
2. Call discover_devices()
3. Filter by device type
4. Return sorted list

Example:

```python
from python_picotool.core.device import discover_devices
devices = discover_devices(DeviceType.PICO)
```
````

````

### "I want to track progress"

Edit **progress.md**:

```markdown
## Completed This Session
- Implemented USB detection
- Added error handling

## In Progress
- Testing with real devices

## Next Steps
- Add CLI support
- Write documentation
````

### "I want to change the approach"

Edit **activeContext.md**:

```markdown
## Current Decision

Changed approach from serial-first to USB-first detection.

## Reasoning

USB detection is more reliable for BOOTSEL mode.

## Impact

Affects device.py initialization order.
```

---

## Important Notes

### Automatic Pre-Flight Validation

Before every task, the system automatically checks:

- Project directory exists
- Core files are present
- .clinerules file is loaded
- Custom documentation is accessible

### Project Isolation

Memory Bank keeps projects completely separate:

- `python_picotool` project can't see `other_project` files
- This prevents accidental context mixing
- Each project has independent memory

### JSON Format for Operations

When the assistant writes to memory bank, it uses:

- JSON format (no XML)
- Escaped newlines as `\n` (not actual line breaks)
- Lowercase booleans (true/false)
- UTF-8 encoding

---

## Troubleshooting

### Problem: "Memory bank files not found"

**Solution**: Check that MEMORY_BANK_ROOT is set correctly in your MCP configuration.

```bash
# Verify directory exists
ls -la /your/memory/bank/directory
```

### Problem: "AI doesn't remember previous context"

**Solution**: Ensure you say "follow your custom instructions" before asking about the project.

### Problem: "Too much information in memory"

**Solution**: Archive old entries in progress.md to keep activeContext.md focused.

### Problem: "Adding custom files didn't work"

**Solution**: Make sure to:

1. Create the file in the correct directory
2. Reference it in activeContext.md
3. Use forward slashes in paths
4. Use valid markdown filename

---

## Next Steps

1. **Set up your memory bank**: Follow "Setting Up Memory Bank for Your Project" section
2. **Initialize with AI**: Use "initialize memory bank" command
3. **Start using**: Begin each session with "follow your custom instructions"
4. **Build patterns**: Add to .clinerules as you discover patterns
5. **Keep updated**: Use "update memory bank" after significant changes

---

## Helpful Resources

**Official Repository**: <https://github.com/alioshr/memory-bank-mcp>

**Comprehensive Documentation**:

- See `MEMORY_BANK_MCP_DOCUMENTATION.md` for complete feature list
- See `MEMORY_BANK_REFERENCE.md` for technical reference

**Original Concept**:

- Cline Memory Bank: <https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md>

---

## Tips for Success

### Keep Files Focused

- Each file should have one primary purpose
- Don't mix project planning with technical decisions
- Separate concerns in custom files

### Update Regularly

- Update after completing significant work
- Add patterns to .clinerules as you discover them
- Keep progress.md current

### Use Consistent Formatting

- Use markdown headers consistently
- Use bullet points for lists
- Keep examples in code blocks

### Reference Context

- In activeContext.md, reference the files you're using
- In progress.md, link to relevant custom files
- In .clinerules, include concrete examples

---

## Summary

Memory Bank MCP enables persistent AI memory by:

- **Reading**: Loading your project context before each task
- **Learning**: Capturing patterns you want to repeat
- **Remembering**: Storing decisions for future reference
- **Improving**: Getting better results as it learns more

Start with the core files, then expand with custom documentation as your needs grow.
