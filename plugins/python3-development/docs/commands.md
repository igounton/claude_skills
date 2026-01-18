# Commands Reference

This document describes the **command reference library** included in the python3-development plugin.

**Important**: The `commands/` directory contains **reference material for creating slash commands**, NOT actual deployable slash commands. These files serve as templates, patterns, and procedural guides for command development.

## Purpose

The command reference library provides:

- **Command Templates** - Standardized structures for creating new slash commands
- **Command Patterns** - Configuration defining command categories, workflows, and integration
- **Meta-Commands** - Guides for generating other commands using established patterns
- **Specialized Workflows** - Domain-specific command procedures (testing, development)

## Directory Structure

```text
commands/
├── development/                  # Development workflow reference
│   ├── config/
│   │   └── command-patterns.yml # Command categories, workflows, risk levels
│   ├── templates/
│   │   └── command-template.md  # Base template for new commands
│   ├── use-command-template.md  # Meta-command: generate commands from template
│   └── create-feature-task.md   # Structured feature development workflow
│
└── testing/                      # Testing workflow reference
    ├── analyze-test-failures.md  # Investigate test failures
    ├── comprehensive-test-review.md # Thorough test reviews
    └── test-failure-mindset.md   # Test failure analysis approach
```

## Reference Files

### Development Workflow

#### create-feature-task

**Location**: `commands/development/create-feature-task.md`

**Type**: Development workflow reference

**Purpose**: Reference material for setting up comprehensive feature development tasks with proper tracking, phases, and documentation.

**Key Sections**:
- Parse feature requirements from user input
- Generate task structure with customized phases
- Create task documentation from template
- Set up tracking with checkpoints and progress markers

**Template Usage**: References `~/.claude/templates/feature-task-template.md`

**Integration**:
- Prerequisites: Clear feature requirements
- Follow-up: `/development:implement-feature [task-file]`
- Related: `create-test-plan`, `estimate-context-window`

**Example Application**:
```text
User: "I want to create a task for adding user authentication with OAuth"

Reference Material Usage:
1. Parse requirements: "user authentication with OAuth"
2. Identify complexity: Medium-High (external service integration)
3. Generate task structure with phases:
   - Requirements analysis
   - Architecture design
   - OAuth provider setup
   - Implementation
   - Testing
   - Security review
4. Create documentation at .claude/tasks/oauth-auth.md
5. Set up tracking with checkpoints
```

---

#### use-command-template

**Location**: `commands/development/use-command-template.md`

**Type**: Meta-command reference

**Purpose**: Reference material for creating new Claude Code commands following established patterns and templates.

**Execution Steps**:
1. Determine command type from purpose
2. Apply base template with customizations
3. Configure integration with workflow chains
4. Create command file in appropriate location

**Template Structure**: Standard structure includes:
- Purpose statement (single sentence)
- Task description with `$ARGUMENTS`
- Phased execution steps
- Context preservation rules
- Expected output format
- Integration guidance

**Best Practices**:
- Keep commands focused on single responsibility
- Use clear verb-noun naming (analyze-dependencies, create-component)
- Include at least 3 example usages
- Define what gets cached for reuse
- Specify prerequisite and follow-up commands

**Example Application**:
```bash
# Creating a new analysis command reference
Purpose: "analyze API endpoints for rate limiting needs"

Template Application:
1. Command type: Analysis
2. Name: analyze-rate-limits (verb-noun format)
3. Category: Quality/Analysis
4. Integration: Fits in pre-deployment workflow
5. Output: Rate limit recommendations and implementation plan
```

---

### Testing Workflow

#### analyze-test-failures

**Location**: `commands/testing/analyze-test-failures.md`

**Type**: Testing workflow reference

**Purpose**: Reference material for analyzing failing test cases with a balanced, investigative approach to determine whether failures indicate test issues or genuine bugs.

**Key Principles**:
1. **Tests as First-Class Citizens** - Tests encode important business logic
2. **Dual Hypothesis Approach** - Consider both possibilities (test wrong OR implementation wrong)
3. **Evidence-Based Decisions** - Never assume, always investigate
4. **Respect the Test Author** - They may have understood requirements you're missing

**Analysis Process**:
1. Read the failing test and understand its intent
2. Investigate the implementation being tested
3. Apply critical thinking to determine root cause
4. Classify as: Test Bug | Implementation Bug | Ambiguous
5. Document reasoning with evidence

**Example Classifications**:

**Test Bug Example**:
```text
Test expects divide(10, 0) to return 0, but it throws DivisionByZeroError

Analysis: Division by zero is mathematically undefined. Throwing error is correct.
Determination: Test Bug
Recommendation: Update test to expect error, not 0
```

**Implementation Bug Example**:
```text
Test expects validateEmail("user@example.com") to return true, but returns false

Analysis: Email is valid per RFC standards. Implementation regex missing dot support.
Determination: Implementation Bug
Recommendation: Fix regex to handle dots in domain
```

**Ambiguous Example**:
```text
Test expects calculateDiscount(100, 0.2) to return 20, but returns 80

Analysis: Name ambiguous - could mean discount amount or discounted price.
Determination: Ambiguous
Recommendation: Check documentation or clarify intended behavior
```

**Output Format**:
```text
Test: [test name]
Failure: [what failed]

Investigation:
- Test expects: [expected behavior]
- Implementation does: [actual behavior]
- Root cause: [why they differ]

Determination: [Test Bug | Implementation Bug | Ambiguous]

Recommendation: [specific fix]
```

---

#### comprehensive-test-review

**Location**: `commands/testing/comprehensive-test-review.md`

**Type**: Testing workflow reference

**Purpose**: Reference material for performing thorough test reviews following standard checklists.

**Review Areas**:
- Test isolation and independence
- Mock usage appropriateness
- Test execution time
- Flaky test patterns
- Test naming clarity
- Coverage completeness
- Edge case handling
- Error condition testing

**Template Reference**: Uses `templates/test-checklist.md` for standard review process

**Integration**:
- Used after test implementation
- Before final code review
- Part of quality gate validation

---

#### test-failure-mindset

**Location**: `commands/testing/test-failure-mindset.md`

**Type**: Testing workflow reference

**Purpose**: Reference material for establishing a balanced investigative approach to test failures for the entire session.

**Core Mindset**:
```text
"This test is failing. This could mean:
1. The test discovered a bug (valuable!)
2. The test's expectations don't match intended behavior
3. There's ambiguity about correct behavior

Let me investigate all three before making changes."
```

**Red Flags** (dangerous patterns):
- 🚫 Immediately changing tests to match implementation
- 🚫 Assuming implementation is always correct
- 🚫 Bulk-updating tests without individual analysis
- 🚫 Removing "inconvenient" test cases
- 🚫 Adding mock workarounds instead of fixing root causes

**Good Practices**:
- ✅ Treat each failure as potential bug discovery
- ✅ Document analysis in comments when fixing tests
- ✅ Write clear test names explaining intent
- ✅ Explain why original test was wrong when changing
- ✅ Add more tests when finding ambiguity

**Approach for Every Failure**:
1. Pause and read - understand test intent
2. Trace implementation - follow code path
3. Consider context - documented requirements, user impact
4. Make reasoned decision - fix bug OR fix test with documentation
5. Learn from failure - patterns, additional tests needed

---

## Configuration Files

### command-patterns.yml

**Location**: `commands/development/config/command-patterns.yml`

**Purpose**: Defines organizational structure for commands

**Contents**:
- **Command Categories**: Analysis, Development, Quality, Documentation, Operations
- **Workflow Chains**: Multi-step processes (Feature Development, Bug Fix, Code Review)
- **Context Sharing**: Information flow between commands
- **Cache Patterns**: TTL and invalidation rules
- **Risk Assessment**: Classification and safeguards

---

## Usage Patterns

### Creating a New Command

When creating a new slash command:

1. **Consult the patterns**:
   - Review `command-patterns.yml` to understand categories, workflows, and risk levels

2. **Use the template**:
   - Start with `command-template.md`
   - Replace placeholders with command-specific content
   - Customize execution steps
   - Define integration points

3. **Follow naming conventions**:
   - Analysis: `analyze-*`, `scan-*`, `validate-*`
   - Development: `create-*`, `implement-*`, `fix-*`
   - Operations: `deploy`, `migrate`, `cleanup-*`

4. **Deploy to proper location**:
   - User commands: `~/.claude/commands/`
   - Project commands: `.claude/commands/` (in project root)
   - **NOT** in this `commands/` reference directory

### Integrating Commands into Workflows

Commands chain together in workflows:

```yaml
Feature_Development:
  steps:
    - create-feature-task       # Initialize structured task
    - study-current-repo        # Understand codebase
    - implement-feature         # Write code
    - create-test-plan          # Design tests
    - comprehensive-test-review # Validate quality
    - gh-create-pr              # Submit for review
```

Each command produces context for subsequent commands.

---

## Relationship to Skill Structure

This directory is part of the python3-development skill's reference material:

```text
python3-development/
├── SKILL.md                    # Skill entry point
├── references/
│   ├── commands/               # THIS DIRECTORY (reference material)
│   ├── modern-modules/         # Python library guides
│   └── ...
└── scripts/                    # Executable tools
```

**Important Distinctions**:

- **This directory** (`commands/`): Templates and patterns for creating commands
- **Deployed commands** (`~/.claude/commands/`): Actual slash commands Claude Code executes
- **Skill scripts** (`scripts/`): Python tools that may be called by commands

---

## Best Practices

### When Creating Commands

1. **Single Responsibility** - Each command focuses on one clear task
2. **Clear Naming** - Descriptive verb-noun pairs (`analyze-dependencies`, `create-component`)
3. **Example Usage** - Include at least 3 concrete examples
4. **Context Definition** - Specify what gets cached for reuse
5. **Integration Points** - Define prerequisites and follow-up commands

### When Organizing Commands

1. **Category Alignment** - Place in appropriate category subdirectories
2. **Workflow Awareness** - Consider how commands chain together
3. **Risk Classification** - Mark high-risk commands with safeguards
4. **Documentation** - Keep command patterns file updated

---

## Integration with Python Development Skill

Commands support orchestration patterns from:

- [Python Development Orchestration](../skills/python3-development/references/python-development-orchestration.md)

They complement agent-based workflows:

```text
User Request
    ↓
Orchestrator (uses skill + commands)
    ↓
├─→ @agent-python-cli-architect (implementation)
├─→ @agent-python-pytest-architect (testing)
└─→ @agent-python-code-reviewer (review)
    ↓
Apply standards: /modernpython, /shebangpython
```

---

## Common Workflows

### Feature Development

```bash
# 1. Create structured task (using reference material)
Reference: create-feature-task.md
Purpose: Add user authentication with OAuth

# 2. Implement with appropriate agent
(Orchestrator delegates to @agent-python-cli-architect)

# 3. Validate with standards
/modernpython src/auth/oauth.py
/shebangpython scripts/migrate-users.py
```

### Test Failure Investigation

```bash
# Analyze failures (using reference material)
Reference: analyze-test-failures.md
Test: test_authentication.py::test_oauth_flow
Approach: Balanced investigation (test bug vs implementation bug)
```

### Command Creation

```bash
# Generate new command (using reference material)
Reference: use-command-template.md
Purpose: validate API endpoints for rate limiting
Output: New command file in appropriate location
```

---

## External Slash Commands

The following **actual slash commands** are referenced by this skill but must be installed separately:

### /modernpython

**Purpose**: Comprehensive reference guide for Python 3.11+ patterns with official PEP citations

**Usage**:
```text
/modernpython              # Load reference guide
/modernpython src/mymodule.py  # Load guide for specific file work
```

**Provides**:
- Python 3.11+ pattern examples
- PEP citations with research tool guidance
- Legacy patterns to avoid
- Modern alternatives
- Framework-specific guides (Typer, Rich, pytest)

### /shebangpython

**Purpose**: Validate correct shebang for ALL Python scripts based on dependencies

**Usage**:
```text
/shebangpython scripts/deploy.py
```

**Actions**:
- Analyzes imports to determine dependency type
- **Corrects shebang** to match script type (edits file)
- **Adds PEP 723 metadata** if external dependencies detected
- **Removes PEP 723** if stdlib-only
- Sets execute bit if needed
- Provides verification report

**Validates**:
- Stdlib-only scripts: `#!/usr/bin/env python3`
- Scripts with dependencies: `#!/usr/bin/env -S uv --quiet run --active --script` + PEP 723
- Package executables: `#!/usr/bin/env python3`
- Library modules: No shebang

---

## Summary

The command reference library provides templates, patterns, and procedural guides for:

1. **Creating new slash commands** with standard structure and best practices
2. **Analyzing test failures** with balanced investigative approach
3. **Reviewing tests comprehensively** against quality checklist
4. **Setting up feature tasks** with proper tracking and documentation

These reference materials support the python3-development skill's orchestration patterns and integrate with agent-based workflows for Python development.
