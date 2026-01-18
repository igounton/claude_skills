# Agents Reference

This plugin provides two specialized agents that work together in a dual-phase workflow to ensure code quality through systematic linting resolution and architectural validation.

---

## linting-root-cause-resolver

**Location**: `agents/linting-root-cause-resolver.md`

**Description**: Resolves linting and type checking errors by investigating root causes rather than silencing symptoms.

**Model**: Inherits from session

**Color**: Orange

**User Invocable**: Yes (via Task delegation)

### When to Use

Trigger this agent when:
- Ruff reports code quality issues (F401, E501, B006, etc.)
- Mypy reports type checking errors (attr-defined, arg-type, return-value, etc.)
- Pyright/basedpyright reports type safety issues (reportGeneralTypeIssues, reportOptionalMemberAccess, etc.)
- After completing code implementation that modified Python files
- Before claiming a task is "production ready"

### Activation

Orchestrators should delegate immediately after code changes WITHOUT pre-gathering linting data:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Format, lint, and resolve any issues in src/auth.py"
)
```

For multiple files, launch concurrent agents:

```text
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/auth.py")
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/api.py")
Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in tests/test_auth.py")
```

### What the Agent Does

1. **Loads Required Skills**
   - Activates `holistic-linting` skill for complete resolution workflows
   - Activates `python3-development` skill for Python 3.11+ standards

2. **Follows Linter-Specific Workflows**
   - **Ruff issues**: Uses `ruff rule {CODE}` for documentation
   - **Mypy issues**: Reads locally-cached mypy error code documentation
   - **Pyright issues**: Uses MCP tools (Ref, exa) or WebFetch for basedpyright docs

3. **Investigates Root Causes**
   - Researches linting rules and error codes
   - Reads affected code and architectural context
   - Traces type flows for type checking errors
   - Checks library type stubs when needed

4. **Implements Elegant Fixes**
   - Addresses root causes, not symptoms
   - Follows python3-development modern patterns
   - Uses Python 3.11+ syntax (native generics, union `|` syntax)
   - Maintains or improves code readability

5. **Verifies Resolution**
   - Re-runs formatters and linters
   - Confirms all issues resolved
   - Documents verification results

6. **Produces Artifacts**
   - Investigation reports in `.claude/reports/linting-investigation-*.md`
   - Resolution summaries in `.claude/reports/linting-resolution-*.md`
   - Structured data in `.claude/artifacts/linting-artifacts-*.json`

### Directory Structure Created

The agent ensures these directories exist:

```
.claude/
├── reports/           # Investigation and resolution reports
├── artifacts/         # Structured data for review
└── knowledge/         # Agent-internal notes (gitignored)
```

And updates `.claude/.gitignore`:

```gitignore
reports/
artifacts/
knowledge/
```

### Core Philosophy

The agent treats linting errors as valuable feedback about code quality and design, not annoyances to silence. It:

- Never adds `# type: ignore` or `# noqa` without understanding root causes
- Always verifies assumptions through investigation
- Prioritizes clarity and correctness over quick fixes
- Documents the investigative process for review

### Example Workflow: Ruff Issue

```text
Issue: ruff reports "F401: 'os' imported but unused" in utils.py

Agent Process:
1. Load holistic-linting + python3-development skills
2. Research: ruff rule F401
   → Output: Unused imports clutter namespace
   → Fix: Remove unused import or use it
3. Read code: Read("utils.py")
   → Line 5: import os
   → Code never references 'os'
4. Check context: Grep "import os" in project
   → Other files use os.path, os.environ
   → This file genuinely doesn't need it
5. Implement: Remove unused import from line 5
6. Verify: ruff check utils.py → Clean
7. Create artifacts in .claude/reports/
```

### Example Workflow: Mypy Issue

```text
Issue: mypy reports "Incompatible return value type (got dict[str, Any], expected Response)" in api_client.py:45

Agent Process:
1. Load holistic-linting + python3-development skills
2. Research: Search mypy error_code_list.rst for "return-value"
   → Error code [return-value]
   → Principle: Function must return type matching annotation
3. Read documentation:
   → Occurs when returned expression type doesn't match declared type
4. Trace type flow:
   - Read api_client.py line 45
   - Signature: def fetch_data() -> Response:
   - Actual return: return response.json()
   - response.json() returns dict[str, Any], not Response
5. Check context:
   - fetch_data should return parsed JSON as dict
   - Function signature is wrong, not implementation
6. Implement: Change signature from Response to dict[str, Any]
7. Verify: mypy api_client.py → Clean
8. Create artifacts in .claude/reports/
```

### Example Workflow: Pyright Issue

```text
Issue: pyright reports "reportOptionalMemberAccess: 'upper' is not a known member of 'None'" in validator.py:23

Agent Process:
1. Load holistic-linting + python3-development skills
2. Research: Use MCP Ref tool for basedpyright reportOptionalMemberAccess docs
   → Rule detects accessing members on values that could be None
   → Prevents AttributeError at runtime
3. Read code: Read("validator.py")
   → Line 23: return data.upper()
   → Signature: def validate(data: str | None) -> str:
   → No None check before .upper()
4. Understand issue:
   → data could be None at runtime
   → .upper() would raise AttributeError
   → This is a genuine bug caught by type checker
5. Implement: Add type narrowing
   def validate(data: str | None) -> str:
       if data is None:
           raise ValueError("data cannot be None")
       return data.upper()
6. Verify: pyright validator.py → Clean
7. Create artifacts in .claude/reports/
```

### Output Artifacts

**Investigation Report** (`.claude/reports/linting-investigation-[topic]-[timestamp].md`):

```markdown
# Linting Investigation Report - 2026-01-18

## Issues Analyzed
- src/auth.py:45 - F401: 'os' imported but unused
- src/auth.py:67 - E501: Line too long (92 > 88 characters)
- src/auth.py:102 - mypy: Incompatible return value type

## Investigation Process
1. Loaded holistic-linting + python3-development skills
2. Followed Ruff Resolution Workflow for F401 and E501
3. Followed Mypy Resolution Workflow for return-value error
4. Read complete file context and architectural patterns

## Root Causes Identified
- F401: Leftover import from refactored code
- E501: Long error message string, should use textwrap
- mypy: Function signature incorrect after API change
```

**Resolution Summary** (`.claude/reports/linting-resolution-[topic]-[timestamp].md`):

```markdown
### Linting Resolution: auth.py - Import and Type Issues

**Investigation Summary:**
- Original assumption: os module needed for path operations
- Actual finding: Import was leftover from refactored file operations
- Pattern discovered: Project uses pathlib, not os.path

**Architectural Insights:**
- Codebase consistently uses pathlib.Path for file operations
- Error messages follow project standard: under 88 chars with textwrap
- API response types changed but signatures not updated

**Review Focus Areas:**
1. Check other modules for similar unused os imports
2. Validate all API client function signatures match new response types
3. Consider adding pre-commit hook to catch unused imports

**Follow-up Tasks:**
- [ ] Audit other files for unused os imports
- [ ] Review remaining API client methods for type accuracy
```

### Communication Style

The agent reports findings directly without hedging:
- ✅ "The import is unused and should be removed"
- ✅ "The function signature is incorrect"
- ❌ "It seems like the import might not be needed"
- ❌ "I think the function signature could be wrong"

It shares the investigative process transparently and states uncertainties explicitly when they exist.

### Final Handoff

After completing resolution, the agent recommends:

"I've completed linting resolution following the [Ruff/Mypy/Pyright] workflow from the holistic-linting skill. All artifacts are documented in `.claude/reports/`. I recommend using the `post-linting-architecture-reviewer` agent to perform comprehensive architectural review based on these findings."

---

## post-linting-architecture-reviewer

**Location**: `agents/post-linting-architecture-reviewer.md`

**Description**: Performs architectural review after linting-root-cause-resolver completes. Verifies resolution quality and identifies systemic improvements.

**Model**: Haiku (fast, cost-effective reviews)

**Color**: Yellow

**User Invocable**: Yes (via Task delegation)

### When to Use

Trigger this agent when:
- `linting-root-cause-resolver` has completed and created artifacts
- Resolution reports exist in `.claude/reports/`
- You need to validate that fixes align with codebase patterns
- You want to identify broader architectural improvements
- Before finalizing a task as complete

### Activation

Delegate after the resolver agent completes:

```text
Task(
  agent="post-linting-architecture-reviewer",
  prompt="Review linting resolution for src/auth.py"
)
```

For multiple file reviews:

```text
Task(agent="post-linting-architecture-reviewer", prompt="Review linting resolution for src/auth.py")
Task(agent="post-linting-architecture-reviewer", prompt="Review linting resolution for src/api.py")
```

### Prerequisites Verification

The agent checks for required artifacts:

```bash
ls -la .claude/reports/linting-investigation-*.md
ls -la .claude/reports/linting-resolution-*.md
ls -la .claude/artifacts/linting-artifacts-*.json
```

If artifacts are missing, the agent stops and informs you to run `linting-root-cause-resolver` first.

### What the Agent Does

1. **Load Resolution Context**
   - Reads investigation reports
   - Reads resolution summaries
   - Loads structured artifacts
   - Identifies modified files

2. **Verify Resolution Quality**
   - Confirms fixes address root causes (not symptom suppression)
   - Validates solutions align with discovered codebase patterns
   - Checks type safety maintained or improved
   - Ensures no new technical debt introduced
   - Validates changes follow python3-development standards

3. **Analyze Architectural Impact**
   - **Design Principles**: SRP, separation of concerns, dependency injection
   - **Code Organization**: Service layer usage, file/class size, module boundaries
   - **Type Safety**: Enum usage, error handling patterns, API response handling
   - **Code Quality**: String centralization, documentation accuracy, CLAUDE.md conventions
   - **Testing**: Business logic testability, edge case coverage, mocking patterns
   - **Performance/Security**: Async patterns, resource management, sensitive data protection
   - **State Management**: Stateless design, state encapsulation, side effect isolation

4. **Output Structured Review**
   - Creates architectural review report
   - Identifies systemic improvements
   - Provides concrete code examples
   - Prioritizes findings by impact

5. **Capture Knowledge**
   - Documents patterns in `.claude/knowledge/linting-patterns.md`
   - Records resolution strategies for reuse
   - Captures architectural insights

### Review Checklist

The agent systematically checks:

**Resolution Quality**:
- [ ] Fix addresses root cause (not symptom suppression)
- [ ] Solution aligns with discovered codebase patterns
- [ ] Type safety maintained or improved
- [ ] No new technical debt introduced
- [ ] Changes follow python3-development standards

**Design Principles**:
- [ ] Single Responsibility Principle maintained
- [ ] Separation of concerns (UI/Business/Data)
- [ ] Dependency injection patterns followed
- [ ] Interface segregation appropriate

**Code Organization**:
- [ ] Service layer usage consistent
- [ ] File/class size reasonable
- [ ] Module boundaries respected
- [ ] Logic reuse opportunities identified

**Type Safety**:
- [ ] Enums used for type differentiation
- [ ] Error handling pattern consistent
- [ ] API response handling uniform
- [ ] Type annotations complete

**Testing & Quality**:
- [ ] Business logic unit testable
- [ ] Edge cases covered
- [ ] Documentation accurate
- [ ] No redundant comments

### Output Artifacts

**Architectural Review Report** (`.claude/reports/architectural-review-[timestamp].md`):

```markdown
# Post-Linting Architectural Review - 2026-01-18

## Resolution Context
- Files reviewed: src/auth.py
- Issues resolved: 3 (F401, E501, return-value)
- Patterns discovered: pathlib usage, textwrap for long strings
- Artifacts reviewed: linting-investigation-auth-20260118.md, linting-resolution-auth-20260118.md

## Verification Results

### Resolution Quality: PASS
- ✓ All fixes address root causes
- ✓ Solutions align with codebase pathlib pattern
- ✓ Type safety improved with correct return annotations
- ✓ No new technical debt
- ✓ Python 3.11+ patterns used

## Architectural Findings

### Import Management - Priority: Medium
**Original Issue**: F401: 'os' imported but unused (auth.py:45)
**Pattern Applied**: Use pathlib.Path instead of os.path
**Finding**: Codebase has migrated to pathlib but some modules still import os

**Proposed Solution**:
```python
# Audit script to find remaining os imports
import ast
from pathlib import Path

def find_os_imports(project_root):
    for py_file in Path(project_root).rglob("*.py"):
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "os":
                        print(f"{py_file}:{node.lineno} - Potential unused os import")
```

**Implementation**:
1. Run audit script on src/ directory
2. For each file, check if os module is actually used
3. Replace os.path patterns with pathlib.Path
4. Remove unused os imports

### Error Message Formatting - Priority: Low
**Original Issue**: E501: Line too long (auth.py:67)
**Pattern Applied**: Use textwrap.dedent for long messages
**Finding**: Error messages should use consistent formatting

**Proposed Solution**:
```python
from textwrap import dedent

# Before
raise ValueError("Authentication failed: invalid credentials provided. Please check username and password.")

# After
raise ValueError(dedent("""
    Authentication failed: invalid credentials provided.
    Please check username and password.
""").strip())
```

## Systemic Improvements

1. **Codebase-wide pathlib migration** - Priority: Medium, Effort: Low
   - Audit all os.path usage
   - Migrate to pathlib.Path
   - Update linting rules to flag new os imports

2. **API response type consistency** - Priority: High, Effort: Medium
   - Review all API client methods
   - Ensure return types match actual responses
   - Add integration tests for type accuracy

## Knowledge Capture

Documented in `.claude/knowledge/linting-patterns.md`:
- Pattern: Codebase uses pathlib, not os.path
- Strategy: Use textwrap.dedent for multi-line error messages
- Insight: API client signatures need regular review after upstream changes
```

### Integration with Resolver Phase

This agent completes a two-phase workflow:
- **Phase 1** (linting-root-cause-resolver): Investigate root causes, create artifacts
- **Phase 2** (this agent): Verify resolution quality, validate architecture

The reviewer uses resolver artifacts as authoritative context. Its role is verification and systemic improvement identification, not re-investigation.

### Communication Style

The agent states findings directly:
- ✅ "The fix correctly addresses the root cause"
- ✅ "This reveals a broader pattern requiring attention"
- ❌ "The fix might be correct"
- ❌ "This could indicate a pattern"

It references artifact line numbers and provides concrete solutions with code examples.

### Example Review Process

```text
User: "Review the linting resolution for src/auth.py"

Agent Process:
1. Check for artifacts:
   - Found linting-investigation-auth-20260118.md
   - Found linting-resolution-auth-20260118.md
2. Load resolution context:
   - 3 issues resolved (F401, E501, mypy return-value)
   - Pattern discovered: pathlib usage
3. Verify resolution quality:
   ✓ All fixes address root causes
   ✓ Aligns with codebase patterns
4. Analyze architectural impact:
   - Import management: Medium priority
   - Error formatting: Low priority
   - API type consistency: High priority
5. Identify systemic improvements:
   - Audit all os imports (Medium effort)
   - Review API client types (High priority)
6. Create architectural review report
7. Document patterns in knowledge base
```

### When Review Identifies Issues

If the reviewer finds problems with the resolution, the orchestrator should delegate back to the resolver with specific guidance:

```text
Task(
  agent="linting-root-cause-resolver",
  prompt="Address issues found in architectural review: .claude/reports/architectural-review-20260118.md

Issues identified:
- Function signature fix incomplete: other methods also affected
- Pattern not applied consistently: similar code in utils.py

Review report contains detailed context and proposed solutions."
)
```

After re-resolution, delegate to the reviewer again to validate the updates.

---

## Dual-Phase Workflow

The two agents work together systematically:

```text
[Implementation complete]
  ↓
[Step 1: Delegate to linting-root-cause-resolver]
  - Agent formats, lints, resolves issues
  - Creates investigation and resolution reports
  - Produces structured artifacts
  ↓
[Step 2: Delegate to post-linting-architecture-reviewer]
  - Agent loads artifacts
  - Verifies resolution quality
  - Analyzes architectural impact
  - Identifies systemic improvements
  ↓
[Step 3: Orchestrator reads review report]
  - Determines if additional work needed
  ↓
[Step 4: If issues found, delegate back to resolver]
  - Provide review report path
  - Summarize specific issues
  ↓
[Step 5: Repeat review until clean]
  ↓
[Task complete ✓]
```

This dual-phase approach ensures:
1. **Separation of concerns** - Resolution and review are distinct responsibilities
2. **Systematic quality** - Every fix is validated architecturally
3. **Knowledge capture** - Patterns discovered are documented for reuse
4. **Continuous improvement** - Systemic issues are identified and addressed

---

## Installation

Install both agents using the provided script:

```bash
# User scope (~/.claude/agents/)
python ./skills/holistic-linting/scripts/install-agents.py --scope user

# Project scope (<git-root>/.claude/agents/)
python ./skills/holistic-linting/scripts/install-agents.py --scope project

# Force overwrite
python ./skills/holistic-linting/scripts/install-agents.py --scope user --force
```

---

## Related Skills

Both agents automatically load:
- **holistic-linting** - Complete resolution workflows and linter-specific methods
- **python3-development** - Modern Python 3.11+ patterns and best practices
