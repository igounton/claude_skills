# Usage Examples

This guide provides detailed, real-world examples of using the prompt-optimization-claude-45 skill to improve Claude Code documentation.

## Example 1: Optimizing a Project CLAUDE.md

**Scenario**: You have a project CLAUDE.md with numerous prohibition lists and vague quality instructions.

**Original CLAUDE.md**:

```markdown
# Project Instructions

## FORBIDDEN ACTIONS
❌ NEVER use cat, grep, or find commands
❌ NEVER commit without running tests
❌ NEVER use bare python commands
❌ DON'T use performative language

## Code Quality
Write clean code and handle errors properly.
Make sure everything is well documented.
```

**Prompt**:

```
@prompt-optimization-claude-45
Optimize this CLAUDE.md file following Claude 4.5 best practices
```

**Optimized Result**:

```markdown
# Project Instructions

## Tool Selection
| Operation | Tool | Reason |
|-----------|------|--------|
| Read files | `Read()` | Handles encoding, large files, binary detection |
| Search patterns | `Grep()` | Returns structured matches with context |
| Find files | `Glob()` | Respects gitignore, returns sorted results |
| Run Python | `Bash(uv run ...)` | Manages venv and dependencies automatically |

## Commit Protocol

TRIGGER: Ready to commit changes

PROCEDURE:
1. Run test suite: `uv run pytest`
2. Verify all tests pass
3. Stage changes: `git add .`
4. Commit with conventional format: `type(scope): description`

CONSTRAINT: Tests must pass before commit

## Code Standards

### Error Handling
Catch exceptions only when you have a specific recovery action.
Let all other errors propagate to surface issues early.

**Reason**: Explicit error handling reveals failure modes and recovery strategies.

<example>
# Good: specific recovery action
try:
    return api.fetch_user(id)
except NetworkError:
    logger.warning("API unavailable, using cache")
    return cache.get(f"user:{id}")

# Good: let errors propagate
def process_data(raw):
    return transform(raw)  # Errors surface naturally
</example>

### Documentation
Use docstrings for public functions with format:
- Brief description (one line)
- Args with types
- Returns with type
- Raises for expected exceptions

**Reason**: Enables IDE tooltips and auto-generated API documentation.

## Communication Style
- Lead with observations and findings
- State facts directly without hedging
- Skip summaries after tool operations unless requested
```

**Result**: Reduced from 100 lines to 68 lines, eliminated all prohibition markers, added concrete examples, and included motivations.

---

## Example 2: Improving a Skill Description

**Scenario**: Your skill has a weak description that doesn't trigger properly.

**Original Skill**:

```yaml
---
name: deploy-helper
description: Helps with deployments
allowed-tools: Bash(kubectl:*,aws:*)
---

# Deploy Helper

Use this skill to deploy applications.
```

**Prompt**:

```
Improve this skill description so Claude discovers it when needed
```

**Optimized Result**:

```yaml
---
name: kubernetes-deployer
description: Deploy containerized applications to Kubernetes clusters via kubectl. Validate manifests, apply configurations, check rollout status, and rollback if needed. Use when deploying to k8s, updating deployments, managing pods, or when user mentions kubectl, kubernetes, or deployment issues.
allowed-tools: Bash(kubectl:*,aws:*)
---

# Kubernetes Deployer

Deploy and manage applications in Kubernetes clusters with validation and safety checks.

## Deployment Workflow

TRIGGER: User requests deployment to Kubernetes

PROCEDURE:
1. Validate manifest: `kubectl apply --dry-run=client -f manifest.yaml`
2. Apply configuration: `kubectl apply -f manifest.yaml`
3. Monitor rollout: `kubectl rollout status deployment/app-name`
4. Verify pods: `kubectl get pods -l app=app-name`

ROLLBACK:
IF deployment fails THEN `kubectl rollout undo deployment/app-name`

## Safety Checks
- Validate manifests before applying
- Monitor rollout status until stable
- Check pod health after deployment
- Preserve previous deployment for rollback

**Reason**: Prevents downtime from invalid configurations.
```

**Result**: Skill description now includes trigger keywords (kubectl, kubernetes, deployment) and describes WHAT and WHEN. The skill body has concrete procedures with safety checks.

---

## Example 3: Compressing Verbose Agent Instructions

**Scenario**: Your agent instructions exceed 300 lines and need compression without losing compliance.

**Original Instructions** (excerpt):

```markdown
When you're working on a task, you might want to consider reading the
relevant documentation files first. It's important to remember that you
should check the test files to understand expected behavior. One approach
is to use the Grep tool to search for patterns. For example, when you
encounter an error, you could search for similar error messages in the
codebase.

After you've completed your investigation, it would be great if you could
write a summary of your findings. Please make sure to include all the
relevant details and context.
```

**Prompt**:

```
Compress these agent instructions using the compression techniques while preserving clarity
```

**Optimized Result**:

```markdown
## Investigation Protocol

TRIGGER: Assigned diagnostic task

PROCEDURE:
1. Read relevant docs (`Read()`)
2. Examine test files for expected behavior
3. Search patterns (`Grep()` for error messages, function calls)
4. Trace error propagation through codebase

OUTPUT: Findings summary with:
- Root cause identification
- Affected components
- Evidence (file:line references)

CONSTRAINT: Include code citations for all claims
```

**Result**: Reduced from 87 words to 47 words. Replaced conversational phrasing with imperative structure. Preserved all requirements (read docs, check tests, search patterns, write summary).

---

## Example 4: Adding Concrete Examples to Abstract Rules

**Scenario**: Your CLAUDE.md has abstract testing requirements that Claude interprets inconsistently.

**Original**:

```markdown
## Testing
Always write comprehensive tests for new features.
Make sure to test edge cases and error conditions.
```

**Prompt**:

```
Add concrete examples showing what "comprehensive tests" means in practice
```

**Optimized Result**:

```markdown
## Testing Requirements

For each new feature, write tests covering:
1. Happy path (expected input → expected output)
2. Edge cases (boundary values, empty inputs, max limits)
3. Error conditions (invalid input, missing dependencies)
4. Integration points (API contracts, database schemas)

**Reason**: Prevents regression and documents expected behavior.

<examples>
<example type="function-unit-test">
# Feature: User validation function
def test_validate_user():
    # Happy path
    assert validate_user({"name": "Alice", "age": 30}) is True

    # Edge cases
    assert validate_user({"name": "", "age": 30}) is False
    assert validate_user({"name": "A", "age": 0}) is False
    assert validate_user({"name": "A" * 256, "age": 999}) is False

    # Error conditions
    with pytest.raises(KeyError):
        validate_user({"name": "Alice"})  # missing age
    with pytest.raises(TypeError):
        validate_user(None)
</example>

<example type="api-integration-test">
# Feature: Payment processing endpoint
def test_process_payment():
    # Happy path
    response = client.post("/payment", json=valid_payment)
    assert response.status_code == 200
    assert "transaction_id" in response.json()

    # Edge cases
    response = client.post("/payment", json={"amount": 0.01})
    assert response.status_code == 200  # minimum amount

    # Error conditions
    response = client.post("/payment", json={"amount": -10})
    assert response.status_code == 400
    assert "invalid amount" in response.json()["error"]
</example>
</examples>

## Test Coverage Targets
- Unit tests: >80% line coverage
- Integration tests: All API endpoints
- E2E tests: Critical user workflows
```

**Result**: Replaced abstract "comprehensive tests" with specific categories, concrete examples, and measurable coverage targets.

---

## Example 5: Converting Tool Prohibitions to Tool Tables

**Scenario**: Your CLAUDE.md has a long list of prohibited bash commands that confuses Claude.

**Original**:

```markdown
## Tool Usage Rules
❌ NEVER use cat - use Read() instead
❌ NEVER use grep - use Grep() instead
❌ NEVER use find - use Glob() instead
❌ NEVER use head - use Read() with limits
❌ NEVER use tail - use Read() with offset
❌ NEVER use sed - use Edit() instead
❌ NEVER use awk - use Edit() instead
❌ NEVER use echo > file - use Write() instead
```

**Prompt**:

```
Convert these prohibitions into a positive tool selection table
```

**Optimized Result**:

```markdown
## Tool Selection Guide

| Operation | Correct Tool | Reason |
|-----------|--------------|--------|
| Read file contents | `Read(file_path)` | Handles encoding, detects binary, supports line ranges |
| Search file contents | `Grep(pattern, path)` | Returns structured matches, respects gitignore |
| Find files by name | `Glob(pattern, path)` | Faster than bash find, returns sorted results |
| Write file contents | `Write(file_path, content)` | Atomic writes, preserves permissions |
| Modify file contents | `Edit(file_path, old, new)` | Surgical edits, validates uniqueness |
| Run Python scripts | `Bash(uv run script.py)` | Manages dependencies and virtual environments |

### Tool Selection Logic

IF operation needs file I/O THEN use specialized tools (Read/Write/Edit)
ELSE IF operation is project-specific THEN use Bash with allowed patterns
ELSE ask for clarification

**Why specialized tools**: Safer (validation), faster (optimized), more reliable (error handling).
```

**Result**: Replaced 8 prohibition lines with a comprehensive 6-row table showing WHAT to do and WHY. Added decision logic for unclear cases.

---

## Example 6: Optimizing for Parallel Tool Usage (Claude 4.5)

**Scenario**: Your instructions force sequential operations when parallel execution is possible.

**Original**:

```markdown
## Codebase Research
First, search for the error message.
Then, read the files that match.
After that, check the test files.
Finally, look at the configuration.
```

**Prompt**:

```
Restructure this to enable Claude 4.5's parallel tool usage
```

**Optimized Result**:

```markdown
## Codebase Research Protocol

TRIGGER: Investigating error or feature behavior

### Phase 1: Discovery (parallel execution)
Execute simultaneously:
- Search error patterns: `Grep(error_message, "**/*.py")`
- Find test files: `Glob("**/test_*.py")`
- Locate config files: `Glob("**/{config,settings}.*")`
- Check recent changes: `Bash(git log --oneline -10)`

### Phase 2: Analysis (after Phase 1 completes)
Read discovered files:
- Source files from grep matches
- Relevant test files
- Configuration files

### Phase 3: Synthesis
Correlate findings:
- Map error → source location
- Identify test coverage
- Note configuration dependencies
```

**Result**: Restructured from sequential steps to phases with explicit parallel operations. Claude 4.5 will fire all Phase 1 tool calls simultaneously.

---

## Example 7: Adding Verification Requirements for Technical Terms

**Scenario**: Your skill documentation references tools and commands without verification, potentially misleading Claude.

**Original**:

```markdown
## Available Tools
Use the WebFetch tool to get web content.
Use the Exa tool for semantic search.
Use the Context7 tool for codebase context.
```

**Prompt**:

```
Add verification requirements to ensure technical terms are accurate
```

**Optimized Result**:

```markdown
## Tool Verification Protocol

CONSTRAINT: Before documenting any tool, verify its existence and capabilities.

### Verification Steps
1. Check tool availability: List tools in current session
2. Read tool documentation: Search official docs or use `mcp__Ref` if available
3. Test tool syntax: Execute simple test call
4. Document verified behavior: Cite source of truth

### Verified Tools (as of 2026-01-18)

| Tool | Purpose | Verification Source |
|------|---------|-------------------|
| `Read(file_path)` | Read file contents | Claude Code built-in tool |
| `Grep(pattern, path)` | Search file contents | Claude Code built-in tool |
| `Glob(pattern, path)` | Find files by pattern | Claude Code built-in tool |
| `WebFetch(url, prompt)` | Fetch and analyze web content | Claude Code built-in tool (verified via /help) |

### Unverified References
IF referencing a tool not in the verified table THEN:
- Mark as "unverified" explicitly
- Research using available tools
- Update table once verified

**Reason**: Prevents false information from propagating across sessions.
```

**Result**: Added verification protocol, created verified tools table with sources, established process for handling unverified terms.

---

## Summary of Transformation Patterns

| Pattern | Original | Optimized | Benefit |
|---------|----------|-----------|---------|
| Prohibition → Positive | "NEVER use X" | "Use Y because Z" | Reduces cognitive load |
| Vague → Specific | "Handle errors properly" | Examples with exception types | Consistent behavior |
| Sequential → Parallel | "First X, then Y" | "Execute simultaneously: X, Y" | Leverages Claude 4.5 |
| Abstract → Concrete | "Write good tests" | Test categories + examples | Measurable standards |
| Verbose → Compressed | 87 words conversational | 47 words imperative | Token efficiency |
| Tool list → Tool table | 8 prohibition bullets | 6-row decision table | Clarity + motivation |

## Next Steps

Apply these patterns to your own:
- CLAUDE.md files
- Skill definitions
- Agent instructions
- Command prompts

Use the verification checklist from the main README to ensure quality.
