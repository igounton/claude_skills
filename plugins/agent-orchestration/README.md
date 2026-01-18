# Agent Orchestration Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A Claude Code plugin providing a scientific delegation framework for orchestrator AIs coordinating specialist sub-agents. Ensures world-building context (WHERE, WHAT, WHY) while preserving agent autonomy in implementation decisions (HOW).

## Features

- **Scientific delegation framework** - Structure task delegation following observation → hypothesis → experimentation → verification patterns
- **Clear role separation** - Orchestrators route context and define success; agents implement solutions
- **Anti-pattern prevention** - Explicit guidance on avoiding pre-gathering, assumption cascades, and micromanagement
- **Comprehensive templates** - Ready-to-use delegation templates with all required sections
- **Pattern expansion guidance** - Transform single user-identified issues into systemic fixes
- **Resource description patterns** - World-building context that empowers rather than limits agents

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- Basic understanding of Claude Code's Task tool and sub-agent delegation

### Install Plugin

```bash
# Method 1: If available in a marketplace
/plugin install agent-orchestration

# Method 2: Manual installation
cp -r ./plugins/agent-orchestration ~/.claude/plugins/
/plugin reload
```

## Quick Start

When your ROLE_TYPE is orchestrator and you need to delegate a task to a sub-agent:

```text
Task(
  agent="appropriate-specialist",
  prompt="""
Your ROLE_TYPE is sub-agent.

Fix linting errors in the Python project.

OBSERVATIONS:
- User requested linting fixes
- Project uses ruff and mypy
- Configuration exists in pyproject.toml

DEFINITION OF SUCCESS:
- All linting rules pass
- Solutions follow existing project patterns
- Code maintains or improves quality

CONTEXT:
- Location: Python project root
- Scope: All Python files in src/
- Constraints: None specified by user

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria
2. Activate holistic-linting skill for workflow guidance
3. Run linting tools to gather comprehensive error data
4. Research root causes for each error category
5. Implement fixes following discovered patterns
6. Verify all /is-it-done criteria satisfied with evidence

AVAILABLE RESOURCES:
- This Python project uses `uv` - activate the `uv` skill
- Excellent MCP servers installed - check <functions> list and prefer specialists like `Ref` over `WebFetch`
- Full project context including tests and documentation
- Pre-commit hooks configured for validation
"""
)
```

## Capabilities

| Type  | Name                 | Description                              | Invocation          |
|-------|----------------------|------------------------------------------|---------------------|
| Skill | agent-orchestration  | Scientific delegation framework          | Auto-activated      |

## Usage

### For Orchestrators

This plugin activates automatically when Claude's ROLE_TYPE is orchestrator and needs to delegate tasks. The skill provides:

1. **Pre-Delegation Verification Checklist** - Ensure delegations include observations, success criteria, and preserve agent autonomy
2. **Delegation Template** - Structured format for Task prompts with all required sections
3. **Anti-Pattern Guidance** - Avoid common pitfalls like pre-gathering data, assumption cascades, and micromanagement

See [Skills Documentation](./docs/skills.md) for complete field descriptions and examples.

### Core Principle

**Provide world-building context (WHERE, WHAT, WHY). Define success criteria. Trust agent expertise for implementation (HOW).**

The orchestrator's role is to:
- Route context and observations between user and agents
- Define measurable success criteria
- Enable comprehensive discovery
- Trust agent expertise and their 200k context windows

**Never prescribe implementation steps** - agents are specialized experts who discover better solutions when given observations and success criteria rather than step-by-step instructions.

### Key Concepts

#### Observations Without Assumptions

Replace assumptions with factual observations:

- ❌ "I think the problem is..."
- ✅ "Observed symptoms: [list]"

- ❌ "This probably happens because..."
- ✅ "Command X produces output Y"

#### Pass-Through vs Pre-Gathering

- **Pass-through (correct)**: Include data already in context (user messages, prior agent reports, errors you encountered)
- **Pre-gathering (incorrect)**: DO NOT run commands to collect data for agents - they gather their own comprehensive data

#### Pattern Expansion

When users identify a code smell or bug at a specific location, treat it as a symptom of a broader pattern:

- User: "Fix walrus operator in `_some_func()`"
- Means: "Audit and fix ALL instances of this pattern throughout the file/module"

## Configuration

This plugin contains no hooks, MCP servers, or LSP servers. The skill activates automatically based on orchestration context.

## Examples

### Example 1: Linting Task Delegation

**Scenario**: User requests "Fix all linting issues"

**Correct Delegation**:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="""
Your ROLE_TYPE is sub-agent.

Run linting against the project. Resolve all issues at root cause.

OBSERVATIONS:
- User requested comprehensive linting fixes
- Project type: Python
- No specific files mentioned - full project scope

DEFINITION OF SUCCESS:
- All configured linting rules pass
- Code quality checks (linting, formatting) performed per holistic-linting skill
- Solutions follow existing project patterns

CONTEXT:
- Location: Project root
- Scope: All Python files
- Constraints: Maintain backward compatibility

YOUR TASK:
1. Run /is-it-done to understand completion criteria
2. Activate holistic-linting skill for linting workflows
3. Run linting tools to gather comprehensive error data
4. Research root causes for each error category
5. Implement fixes following project conventions
6. Verify all /is-it-done criteria satisfied

AVAILABLE RESOURCES:
- This Python project uses `uv` - activate the `uv` skill, use `uv run` for all operations
- Linting configuration in pyproject.toml
- Previous fixes documented in .claude/reports/ if available
- Full project context including tests and configs
"""
)
```

**Why This Works**:
- Agent gathers their own linting data (no pre-gathering)
- Clear success criteria without prescribing HOW
- World-building context about the ecosystem
- Agent has autonomy to discover patterns and implement solutions

---

### Example 2: Feature Implementation

**Scenario**: User requests "Add authentication middleware"

**Correct Delegation**:

```text
Task(
  agent="python-cli-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

Implement authentication middleware for the API.

OBSERVATIONS:
- User requested authentication middleware
- Existing API structure uses FastAPI
- Current routes have no authentication

DEFINITION OF SUCCESS:
- Authentication middleware integrated into existing API
- All protected routes require valid tokens
- Backward compatibility maintained for public routes
- Tests pass demonstrating auth works correctly

CONTEXT:
- Location: ./src/api/
- Scope: Middleware layer and route protection
- Constraints: Must use existing FastAPI patterns

YOUR TASK:
1. Run /is-it-done to understand completion criteria
2. Examine existing API structure and patterns
3. Research FastAPI authentication best practices using available tools
4. Design middleware following discovered patterns
5. Implement with comprehensive test coverage
6. Verify all /is-it-done criteria satisfied

AVAILABLE RESOURCES:
- Excellent MCP servers installed - check <functions> and prefer `Ref` for FastAPI docs (high-fidelity verbatim source)
- FastAPI skill may be available in <available_skills>
- Existing middleware examples in ./src/api/middleware/
- Test fixtures in ./tests/fixtures/
- Full project context available
"""
)
```

---

### Example 3: Pattern Expansion

**Scenario**: User identifies "Fix walrus operator in `_some_func()` line 45"

**Correct Delegation**:

```text
Task(
  agent="python-cli-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

User identified assign-then-check pattern that could use walrus operator.

OBSERVATIONS:
- User identified specific instance at _some_func():45
- This indicates developer consistently missed walrus operator opportunities
- Code smell suggests systematic review needed

DEFINITION OF SUCCESS:
- Identified instance at line 45 fixed
- All similar assign-then-check patterns in the file converted to walrus where appropriate
- Code follows Python 3.8+ best practices
- Tests pass confirming behavior preserved

CONTEXT:
- Location: ./src/utils/helpers.py (or wherever _some_func is located)
- Scope: Entire file - treat user's example as representative of broader pattern
- Constraints: Maintain existing function behavior

YOUR TASK:
1. Run /is-it-done to understand completion criteria
2. Fix the specific instance user identified at line 45
3. Audit entire file for similar assign-then-check patterns
4. Apply walrus operator where appropriate and improves readability
5. Document how many instances found and fixed
6. Verify tests pass and /is-it-done criteria satisfied

AVAILABLE RESOURCES:
- Python 3.8+ syntax fully supported
- Test suite in ./tests/ covers this module
- Full project context available
"""
)
```

**Why Pattern Expansion Matters**: Users rarely audit entire codebases before reporting issues. Default to systemic fixes for better outcomes.

---

See [docs/examples.md](./docs/examples.md) for more comprehensive examples and anti-patterns to avoid.

## Troubleshooting

### Agent seems limited in tool usage

**Problem**: Delegation lists specific tools (e.g., "AVAILABLE RESOURCES: Read, Grep, Bash")

**Solution**: Use world-building context instead:

```text
AVAILABLE RESOURCES:
- Excellent MCP servers installed - check <functions> list and prefer specialists
- This Python project uses `uv` - activate the `uv` skill
- Full project context available including tests and docs
```

### Agent implements prescribed solution without investigation

**Problem**: Delegation prescribes HOW instead of defining WHAT

**Solution**: Provide observations and success criteria, let agent design approach:

```text
OBSERVATIONS:
- [factual observations]

DEFINITION OF SUCCESS:
- [measurable outcome]

YOUR TASK:
1. Run /is-it-done for completion criteria
2. Investigate comprehensively
3. Design solution following discovered patterns
4. Implement with verification
```

### Agent asks for information you haven't gathered

**Problem**: Pre-gathering data before delegation wastes context

**Solution**: Delegate with task + success criteria, let agent gather data:

```text
Run linting against the project. Resolve all issues at root cause.

[Success criteria and context]

YOUR TASK:
1. Run /is-it-done
2. Run linting tools to gather data
3. Research and fix issues
```

### Delegation feels verbose

**Problem**: Including every detail in every delegation

**Solution**: Use `@filepath` references for detailed documents:

```text
Fix issues documented in @.claude/smells/report.md

DEFINITION OF SUCCESS:
- All issues from report resolved
- Tests pass

[Rest of delegation template]
```

## Contributing

This plugin is part of the claude_skills repository. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make changes following existing patterns
4. Submit a pull request

## License

See repository LICENSE file for details.

## Credits

Developed as part of the Claude Code skills ecosystem to improve multi-agent orchestration patterns and outcomes.
