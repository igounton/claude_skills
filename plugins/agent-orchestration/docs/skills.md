# Skills Reference

This plugin provides a single comprehensive skill for orchestrating sub-agent delegation using a scientific framework.

## agent-orchestration

**Location**: `skills/agent-orchestration/SKILL.md`

**Description**: This skill should be used when the model's ROLE_TYPE is orchestrator and needs to delegate tasks to specialist sub-agents. Provides scientific delegation framework ensuring world-building context (WHERE, WHAT, WHY) while preserving agent autonomy in implementation decisions (HOW). Use when planning task delegation, structuring sub-agent prompts, or coordinating multi-agent workflows.

**User Invocable**: Yes (default)

**Allowed Tools**: Inherits (all tools available)

**Model**: Inherits

### When to Use

The agent-orchestration skill activates when:

- Your ROLE_TYPE is orchestrator
- You need to delegate tasks to specialist sub-agents
- You're structuring Task tool prompts for sub-agents
- You're coordinating multi-agent workflows
- You need guidance on avoiding delegation anti-patterns

### Core Principle

**Provide world-building context (WHERE, WHAT, WHY). Define success criteria. Trust agent expertise for implementation (HOW).**

The orchestrator's role:
- Route context and observations between user and agents
- Define measurable success criteria
- Enable comprehensive discovery
- Trust agent expertise and their 200k context windows

**Reason**: Sub-agents are specialized experts with full tool access. Prescribing implementation limits their ability to discover better solutions and prevents them from applying domain expertise effectively.

### Scientific Method Alignment

Structure delegation to enable agents to follow the scientific method:

1. **Observation** → Provide factual observations, not interpretations
2. **Hypothesis** → Let agent form their own hypothesis
3. **Prediction** → Let agent make testable predictions
4. **Experimentation** → Let agent design and execute tests
5. **Verification** → Let agent verify against official sources
6. **Conclusion** → Let agent determine if hypothesis is rejected

### Pre-Delegation Verification Checklist

Before delegating any task to a sub-agent, verify the delegation includes:

#### ✅ Observations without assumptions

- Raw error messages already in context (verbatim, not paraphrased)
- Observed locations (file:line references where errors/issues were seen)
- Command outputs you already received
- State facts using phrases like "observed", "measured", "reported"
- Replace "I think", "probably", "likely", "seems" with verifiable observations

#### ⚠️ Critical: Pass-Through vs Pre-Gathering

- **Pass-through (correct)**: Include data already in your context
- **Pre-gathering (incorrect)**: DO NOT run commands to collect data for agents
- Example: DO NOT run `ruff check .` or `pytest` to collect errors before delegating

**Reason**: Pre-gathering wastes context, duplicates agent work, and causes context rot.

#### ✅ Definition of success

- Specific, measurable outcome
- Acceptance criteria
- Verification method
- Focus on WHAT must work, not HOW to implement it

#### ✅ World-building context

- Problem location (WHERE)
- Identification criteria (WHAT)
- Expected outcomes (WHY)
- Available resources and tools

#### ✅ Preserved agent autonomy

- List available tools and resources
- Trust agent's 200k context window
- Let agent choose implementation approach
- Enable agent to discover patterns and solutions

### Delegation Template

The skill provides a complete template structure for Task tool invocations:

```text
Your ROLE_TYPE is sub-agent.

[Task identification]

OBSERVATIONS:
- [Factual observations from your work or other agents]
- [Verbatim error messages if applicable]
- [Observed locations: file:line references if already known]
- [Environment or system state if relevant]

DEFINITION OF SUCCESS:
- [Specific measurable outcome]
- [Acceptance criteria]
- [Verification method]
- Solution follows existing patterns found in [reference locations]
- Solution maintains or reduces complexity

CONTEXT:
- Location: [Where to look]
- Scope: [Boundaries of the task]
- Constraints: [User requirements only]

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria for this task type
2. Use the /is-it-done checklists as your working guide throughout this task
3. Perform comprehensive context gathering using:
   - Available functions and MCP tools from the <functions> list
   - Relevant skills from the <available_skills> list
   - Project file exploration and structure analysis
   - External resources (CI/CD logs, API responses, configurations)
   - Official documentation and best practices
   - Known issues, forums, GitHub issues if relevant
4. Form hypothesis based on gathered evidence
5. Design and execute experiments to test hypothesis
6. Verify findings against authoritative sources
7. Implement solution following discovered best practices
8. Verify each /is-it-done checklist item as you complete it
9. Only report completion after all /is-it-done criteria satisfied with evidence

INVESTIGATION REQUIREMENTS:
- Trace the issue through the complete stack before proposing fixes
- Document discoveries at each layer
- Identify both symptom AND root cause
- Explain why addressing root instead of patching symptom

VERIFICATION REQUIREMENTS:
- /is-it-done is step 1 of YOUR TASK - run it before starting work
- Use /is-it-done checklists as working guide, not post-mortem report
- Provide evidence for each checklist item as you complete it

AVAILABLE RESOURCES:
[See "Writing Effective AVAILABLE RESOURCES" section for examples]
```

### Writing Effective AVAILABLE RESOURCES

The AVAILABLE RESOURCES section provides world-building context about the environment, not a restrictive tool list.

**Anti-pattern (reductive, limiting)**:

```text
AVAILABLE RESOURCES:
- WebFetch tool
- Read tool
- Bash tool
```

**Problem**: Lists specific tools, implying these are the only options. Additionally, listing WebFetch without mentioning superior MCP alternatives (Ref, exa) causes agents to use low-fidelity tools.

**Correct pattern (world-building, empowering)**:

```text
AVAILABLE RESOURCES:
- The `gh` CLI is pre-authenticated for GitHub operations (issues, PRs, API queries)
- Excellent MCP servers installed for specialized tasks - check <functions> list and prefer MCP tools (like `Ref`, `context7`, `exa`) over built-in alternatives since they're specialists
- This Python project uses `uv` for all operations - activate the `uv` skill and use `uv run python` instead of `python3`
- Project uses `hatchling` as build backend - activate the `hatchling` skill for build/publish guidance
- This repository uses GitLab CI - use `gitlab-ci-local` to validate pipeline changes locally
- Recent linting fixes documented in `.claude/reports/` showing common issues and resolutions
- Package validation scripts in `./scripts/` - check README.md for available validators
- Full project context available including tests, configs, and documentation
```

**Why this works**:

1. Describes capabilities, not constraints
2. Provides context for tool selection
3. References skills to activate
4. Points to project-specific resources
5. Explains ecosystem conventions

### Resource Description Patterns

#### For authenticated CLI tools

```text
The `gh` CLI is pre-authenticated for GitHub operations
The `glab` CLI is configured for GitLab access
AWS CLI is configured with appropriate credentials
```

#### For MCP server preferences

```text
Excellent MCP servers installed - check <functions> list and prefer these specialists:
- `Ref` for documentation (high-fidelity verbatim source, unlike WebFetch which returns AI summaries)
- `context7` for library API docs (current versions, comprehensive)
- `exa` for web research (curated, high-quality sources)
- `mcp-docker` for container operations
```

#### For language/tooling ecosystems

```text
Python project using `uv` - activate `uv` skill, use `uv run`/`uv pip` exclusively
Node project using `pnpm` - use `pnpm` instead of `npm`
Rust project - use `cargo` commands, check Cargo.toml for features
```

#### For CI/CD validation

```text
GitHub Actions - use `act` to validate workflow changes locally
GitLab CI - use `gitlab-ci-local` to test pipeline before pushing
Code quality checks (linting, formatting) performed and issues addressed per the holistic-linting skill
```

#### For project-specific resources

```text
Validation scripts in `./scripts/` - check README.md for usage
Previous fix patterns in `.claude/reports/` for reference
Test fixtures in `./tests/fixtures/` for sample data
API mocks configured in `./tests/mocks/`
```

### Pattern Expansion: From Single Instance to Systemic Fix

**Core Principle**: When user identifies a code smell, bug, or anti-pattern at a specific location, treat it as a symptom of a broader pattern that likely exists elsewhere.

**What users say**:
- "Fix walrus operator in `_some_func()`"
- "Add error handling to this API call"
- "This validation is duplicated"

**What users mean**:
- "The developer consistently missed this pattern throughout the codebase"
- "Audit and fix ALL instances of this pattern, not just the one I pointed out"
- "This instance represents a systemic issue"

**Reason**: Users typically point out single instances as examples. Treating single instances as systemic saves user effort and improves codebase quality comprehensively.

### Common Anti-Patterns to Avoid

#### The Pre-Gathering Anti-Pattern

Running commands to collect data before delegating wastes context and duplicates agent work.

❌ **Incorrect**:

```text
Orchestrator runs: ruff check .
Orchestrator captures: 244 errors
Orchestrator pastes: All 244 errors into delegation prompt
```

✅ **Correct**:

```text
"Run linting against the project. Resolve all issues at root cause.

SUCCESS CRITERIA:
- All configured linting rules satisfied
- Solutions follow project patterns

CONTEXT:
- Python project using ruff and mypy
- Configuration in pyproject.toml

YOUR TASK:
1. Run /is-it-done to understand completion criteria
2. Run linting tools to gather comprehensive data
3. Research root causes
4. Implement fixes
5. Verify criteria satisfied"
```

#### The Assumption Cascade

Stating "I think the issue is X, which probably means Y, so likely Z needs fixing" creates chain of unverified assumptions.

Replace with: "[Observed symptoms]. Success: [desired behavior]. Investigate comprehensively before implementing."

#### The Prescription Trap

Instructing "Fix this by doing A, then B, then C" prevents agent from discovering better approaches.

Replace with: "Fix [observation]. Success: [outcome]. Available resources: [list]."

#### The Discovery Limiter

Directing "Just read these two files and fix the issue" prevents comprehensive investigation.

Replace with: "Fix [observation]. Success: [outcome]. Full project context available."

#### The Tool Dictation

Commanding "Use the MCP GitHub tool to fetch logs" when agent might find better information source.

Replace with: "Investigate [observation]. Available: MCP GitHub tool, local logs, API access."

#### The Reductive Tool List

Listing "AVAILABLE RESOURCES: WebFetch, Read, Bash" when agent has 50+ tools including specialized MCP servers.

Replace with world-building context that describes the ecosystem and guides tool selection (see examples above).

### Specialized Agent Assignments

The skill documents appropriate specialized agents for different task types:

- **Context Gathering**: `context-gathering` sub-agent
- **Python Development**: `python-cli-architect`, `python-pytest-architect`, `python-code-reviewer`
- **Bash Development**: `bash-script-developer`, `bash-script-auditor`
- **Documentation**: `documentation-expert` (user-facing only)
- **Architecture**: `system-architect`, `python-cli-architect`
- **Linting Issues**: `linting-root-cause-resolver`

**Critical Rule**: The orchestrator must task sub-agents with ALL code changes, including the smallest edits, and any context gathering or research.

### Verification Questions for Orchestrators

Before sending delegation, verify:

1. **Am I enabling full discovery?**
   - Listed available tools → ENABLING ✅
   - Specified which tool to use → LIMITING ❌

2. **Am I stating facts or making assumptions?**
   - "Fails with error X" → FACT ✅
   - "Probably fails because..." → ASSUMPTION ❌

3. **Am I defining WHAT or prescribing HOW?**
   - "Must successfully build the package" → WHAT ✅
   - "Run 'npm build' to build" → HOW ❌

4. **Am I sharing observations or solutions?**
   - "Line 42 contains 'import X'" → OBSERVATION ✅
   - "Change line 42 to 'import Y'" → SOLUTION ❌

5. **Am I trusting agent expertise?**
   - "Investigate using available resources" → TRUST ✅
   - "Check this specific documentation" → DISTRUST ❌

### Additional Reference Files

The skill includes several supplementary documents in the skill directory:

- `clear-framework.md` - Simplified framework overview
- `hallucination-triggers.md` - Common triggers for inaccurate responses
- `how-confident.md` - Confidence calibration guidelines
- `is-it-done_gemini.md` - Completion criteria reference
- `post-completion-validation-protocol.md` - Verification procedures

And in the `references/` subdirectory:

- `accessing_online_resources.md` - Guide to high-fidelity web resource access
- `synthesis-improvements-from-research.md` - Research synthesis patterns

### Delegation Formula

**Scientific delegation = Observations + Success Criteria + Available Resources - Assumptions - Prescriptions**

This formula maximizes agent effectiveness by:
- Providing complete factual context (enables accurate hypothesis formation)
- Defining clear success metrics (prevents scope ambiguity)
- Enabling full toolkit access (allows optimal tool selection)
- Removing limiting assumptions (prevents cascade errors)
- Trusting agent expertise (leverages specialized domain knowledge)

---

[← Back to README](../README.md)
