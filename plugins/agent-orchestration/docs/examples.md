# Usage Examples

Concrete, real-world examples of using the agent-orchestration skill for effective sub-agent delegation.

## Example 1: Linting Task Delegation

**Scenario**: User requests "Fix all linting issues in the Python project"

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
- No specific files or error types mentioned

DEFINITION OF SUCCESS:
- All configured linting rules pass
- Code quality checks (linting, formatting) performed and issues addressed per the holistic-linting skill
- Solutions follow existing project patterns
- No regression in functionality

CONTEXT:
- Location: Project root
- Scope: All Python files in the project
- Constraints: Maintain backward compatibility

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria for this task type
2. Use the /is-it-done checklists as your working guide throughout this task
3. Activate holistic-linting skill for linting workflows
4. Run linting tools (ruff, mypy, etc.) to gather comprehensive error data
5. Research root causes for each error category
6. Implement fixes following project conventions
7. Re-run linting to verify all issues resolved
8. Verify each /is-it-done checklist item as you complete it
9. Only report completion after all /is-it-done criteria satisfied with evidence

INVESTIGATION REQUIREMENTS:
- Categorize errors by type and frequency
- Identify systematic patterns vs one-off issues
- Document root causes for each category
- Verify fixes against official style guides

VERIFICATION REQUIREMENTS:
- /is-it-done is step 1 of YOUR TASK - run it before starting work
- Use /is-it-done checklists as working guide, not post-mortem report
- Provide evidence: clean linting output, test results
- Document number of issues fixed by category

AVAILABLE RESOURCES:
- This Python project uses `uv` - activate the `uv` skill and use:
  - `uv run python` instead of `python3`
  - `uv pip` instead of `pip`
  - `uv run ruff check .` for linting
- Linting configuration in pyproject.toml defines project rules
- Previous fixes may be documented in .claude/reports/ for reference
- Test suite available to verify no functionality broken
- Full project context including all source, tests, and documentation
"""
)
```

**Why This Works**:
- Agent gathers their own linting data (no pre-gathering waste)
- Clear success criteria without prescribing implementation steps
- World-building context about tooling ecosystem
- Agent has full autonomy to discover patterns and optimal solutions
- Emphasizes /is-it-done as working guide, not post-mortem

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Pre-gathering data

Orchestrator runs: uv run ruff check .
Orchestrator captures: 244 errors across 50 files
Orchestrator pastes: [All 244 error messages into delegation prompt]

Problem:
- Wasted orchestrator context window on data the agent will gather anyway
- Agent can't see full context, only isolated error snippets
- Agent can't re-run linting during debugging
- Causes context rot as errors are copied multiple times
```

---

## Example 2: Feature Implementation

**Scenario**: User requests "Add authentication middleware to the API"

**Correct Delegation**:

```text
Task(
  agent="python-cli-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

Implement authentication middleware for the API.

OBSERVATIONS:
- User requested authentication middleware
- Observed: existing API uses FastAPI framework
- Observed: current routes have no authentication layer
- No specific auth mechanism specified by user

DEFINITION OF SUCCESS:
- Authentication middleware integrated into existing FastAPI application
- All protected routes require valid authentication tokens
- Backward compatibility maintained for public/health-check routes
- Tests pass demonstrating auth works correctly
- Implementation follows FastAPI best practices

CONTEXT:
- Location: ./src/api/
- Scope: Middleware layer and route protection
- Constraints: Must integrate with existing FastAPI patterns

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria for this task type
2. Use the /is-it-done checklists as your working guide
3. Examine existing API structure and FastAPI patterns in codebase
4. Research FastAPI authentication best practices using available tools
5. Design middleware considering:
   - Token validation
   - Public vs protected routes
   - Error handling for auth failures
   - Existing middleware patterns in the project
6. Implement with comprehensive test coverage
7. Verify all /is-it-done criteria satisfied with evidence

INVESTIGATION REQUIREMENTS:
- Review existing middleware implementations for patterns
- Identify which routes need protection vs public access
- Determine appropriate auth mechanism (JWT, Bearer token, etc.)
- Consider error handling and status codes

VERIFICATION REQUIREMENTS:
- Tests demonstrate protected routes require auth
- Tests demonstrate public routes work without auth
- Tests demonstrate invalid tokens are rejected
- Integration tests pass showing end-to-end flow

AVAILABLE RESOURCES:
- Excellent MCP servers installed - check your <functions> list and prefer these specialists:
  - `Ref` for FastAPI documentation (high-fidelity verbatim source, much better than WebFetch which returns low-fidelity AI summaries)
  - `context7` for library API docs (current versions, precise signatures)
- FastAPI skill may be available in your <available_skills> list
- Existing middleware examples in ./src/api/middleware/ showing project patterns
- Test fixtures in ./tests/fixtures/ for sample requests
- Full project context including all routes, models, and test suites
"""
)
```

**Why This Works**:
- Provides observations about existing system (FastAPI, no current auth)
- Defines clear success criteria (what must work)
- Lets agent research and design the approach (trusted expertise)
- Points to high-fidelity resources (Ref > WebFetch)
- Emphasizes discovering existing patterns before implementing

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Prescribing implementation

OBSERVATIONS:
- Need authentication middleware

YOUR TASK:
1. Create file ./src/api/middleware/auth.py
2. Import jwt library
3. Add verify_token function at line 10
4. Add middleware decorator at line 30
5. Apply @auth_required to routes at lines 45, 67, 89

Problem:
- Prescribes exact implementation (file structure, libraries, line numbers)
- Prevents agent from researching FastAPI best practices
- Prevents agent from discovering existing project patterns
- Prevents agent from choosing optimal auth mechanism
- Reduces agent to code-editing tool without context
```

---

## Example 3: Pattern Expansion - Code Quality

**Scenario**: User identifies "Fix walrus operator opportunity in `_some_func()` at line 45"

**Correct Delegation (Holistic)**:

```text
Task(
  agent="python-cli-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

User identified assign-then-check pattern that could use walrus operator.

OBSERVATIONS:
- User identified specific instance at _some_func():45 in ./src/utils/helpers.py
- Pattern: variable assigned, then immediately checked in conditional
- This indicates developer consistently missed walrus operator opportunities
- Code smell suggests systematic review needed across the file/module

DEFINITION OF SUCCESS:
- Identified instance at line 45 fixed using walrus operator
- All similar assign-then-check patterns in the file converted to walrus where appropriate
- Code follows Python 3.8+ best practices
- Tests pass confirming behavior preserved
- Code readability maintained or improved

CONTEXT:
- Location: ./src/utils/helpers.py
- Scope: Entire file - treat user's example as representative of broader pattern
- Constraints: Python 3.8+ syntax available, maintain existing function behavior

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria
2. Use /is-it-done checklists as working guide
3. Fix the specific instance user identified at line 45
4. Audit entire file for similar assign-then-check patterns
5. Apply walrus operator where it improves clarity and follows best practices
6. Document how many instances found and fixed
7. Run tests to verify behavior preserved
8. Verify all /is-it-done criteria satisfied with evidence

INVESTIGATION REQUIREMENTS:
- Identify all assign-then-check patterns in the file
- Evaluate each for walrus operator appropriateness
- Consider readability impact (walrus doesn't always improve code)
- Check for nested uses or complex expressions

VERIFICATION REQUIREMENTS:
- All tests pass (no behavior changes)
- Each walrus operator use improves or maintains readability
- Document pattern count: X instances found, Y converted, Z left unchanged with rationale

AVAILABLE RESOURCES:
- Python 3.8+ syntax fully supported
- Test suite in ./tests/ covers this module
- PEP 572 documentation available via MCP `Ref` tool if needed
- Full project context available
"""
)
```

**Why This Works**:
- Treats single instance as symptom of broader pattern
- Scopes to entire file (where developer likely repeated pattern)
- Lets agent audit comprehensively
- Lets agent evaluate appropriateness case-by-case
- Documents systematic fix rather than spot fix

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Micromanaged spot fix

OBSERVATIONS:
- Walrus operator opportunity at _some_func():45-47

YOUR TASK:
1. Open ./src/utils/helpers.py
2. Navigate to line 45
3. Change:
   result = calculate()
   if result:
   to:
   if result := calculate():
4. Save file

Problem:
- Treats single instance as isolated issue
- Prescribes exact code change
- Prevents agent from discovering other instances
- Prevents agent from evaluating appropriateness
- Wastes agent expertise on mechanical edit
```

---

## Example 4: Testing Task Delegation

**Scenario**: User reports "Tests failing in test_authentication.py after refactor"

**Correct Delegation**:

```text
Task(
  agent="python-pytest-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

Fix failing tests in test_authentication.py after recent authentication refactor.

OBSERVATIONS:
- User reports tests failing in test_authentication.py
- Authentication module was recently refactored (from prior context)
- No specific test names or error messages provided yet

DEFINITION OF SUCCESS:
- All tests in test_authentication.py pass
- No new test failures introduced in other test files
- Test coverage maintained or improved
- Tests accurately reflect refactored authentication behavior

CONTEXT:
- Location: ./tests/test_authentication.py
- Scope: Fix failing tests, may need to update test logic to match refactored implementation
- Constraints: Tests must validate actual security requirements, not just pass

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria
2. Use /is-it-done checklists as working guide
3. Run pytest on test_authentication.py to identify specific failures
4. Examine refactored authentication code to understand changes
5. Investigate root cause of each failure:
   - Is the test logic outdated?
   - Is the implementation incorrect?
   - Are fixtures or mocks outdated?
6. Fix failures by updating tests OR fixing implementation as appropriate
7. Verify all tests pass and coverage maintained
8. Verify /is-it-done criteria satisfied with evidence

INVESTIGATION REQUIREMENTS:
- Understand what the refactor changed in authentication logic
- Determine if test expectations are still valid
- Check if test fixtures need updating
- Identify if any security requirements changed

VERIFICATION REQUIREMENTS:
- All tests in test_authentication.py pass
- Full test suite passes (no regressions)
- Coverage report shows maintained or improved coverage
- Each fix has clear rationale (updated test vs fixed implementation)

AVAILABLE RESOURCES:
- This Python project uses `uv` - use `uv run pytest` for testing
- Pytest configuration in pyproject.toml
- Test fixtures in ./tests/fixtures/
- Authentication module source in ./src/api/auth.py (or similar)
- Full project context including all source and tests
"""
)
```

**Why This Works**:
- Agent runs tests themselves to see actual failures
- Delegates investigation of root cause (test vs implementation issue)
- Trusts agent to determine appropriate fix
- Emphasizes understanding refactor before fixing tests

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Pre-gathering and prescribing

Orchestrator runs: uv run pytest tests/test_authentication.py
Orchestrator captures: 5 test failures with full tracebacks
Orchestrator analyzes failures and determines:
  - test_valid_token needs mock updated
  - test_expired_token needs assertion changed
  - test_invalid_token needs new fixture

Orchestrator delegates:
"Update test_authentication.py:
1. Line 23: Change mock.return_value to new format
2. Line 45: Update assertion to check new error type
3. Line 67: Create fixture for new token format"

Problem:
- Orchestrator already did the investigation (wasted specialist agent)
- Prescribes exact changes at specific lines
- Agent doesn't understand WHY refactor caused failures
- Agent can't verify if fixes are correct
- Agent reduced to mechanical code editor
```

---

## Example 5: Investigation Task Delegation

**Scenario**: User reports "Production API returning 500 errors intermittently"

**Correct Delegation**:

```text
Task(
  agent="system-architect",
  prompt="""
Your ROLE_TYPE is sub-agent.

Investigate intermittent 500 errors in production API.

OBSERVATIONS:
- User reports 500 errors occurring intermittently in production
- No specific endpoints or patterns identified yet
- Issue is intermittent, not consistent

DEFINITION OF SUCCESS:
- Root cause identified with evidence
- Documented understanding of:
  - Which endpoints/operations affected
  - Frequency and timing patterns
  - Underlying system/code issue
  - Recommended fix approach
- Complete investigation report with reproduction steps if possible

CONTEXT:
- Location: Production API environment
- Scope: Full API stack (application, middleware, infrastructure)
- Constraints: Production system - observe and analyze, don't make changes yet

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria
2. Use /is-it-done checklists as working guide
3. Gather comprehensive data:
   - Production logs via available tools
   - Error patterns and frequency
   - Affected endpoints/operations
   - Timing/load patterns
   - System metrics (CPU, memory, connections)
4. Trace issue through complete stack:
   - Application layer
   - Middleware/framework layer
   - Infrastructure/system layer
5. Form hypothesis based on gathered evidence
6. Design experiments to test hypothesis (if safe in production)
7. Document findings with evidence
8. Recommend fix approach with rationale
9. Verify /is-it-done criteria satisfied

INVESTIGATION REQUIREMENTS:
- Trace through complete stack before concluding
- Document discoveries at each layer
- Identify both symptom AND root cause
- Explain why addressing root cause instead of symptom
- If multiple contributing factors, document all

VERIFICATION REQUIREMENTS:
- Root cause identified with supporting evidence
- Reproduction steps documented (if reproducible)
- Recommended fix addresses root cause, not symptom
- Investigation report includes all layers examined

AVAILABLE RESOURCES:
- MCP servers available - check <functions> for log analysis and monitoring tools
- The `gh` CLI is pre-authenticated for GitHub operations (if relevant to review recent changes)
- Production logs accessible via configured logging tools
- System monitoring dashboards available
- Full application source code and configuration
- Recent deployment history available
"""
)
```

**Why This Works**:
- Defines investigation goal (root cause) without assuming cause
- Trusts agent to gather comprehensive data
- Emphasizes tracing through full stack
- Focuses on understanding before recommending fixes
- Lists available observability tools without prescribing investigation path

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Assumption cascade

OBSERVATIONS:
- 500 errors in production
- I think it's probably a database connection issue
- Likely caused by connection pool exhaustion
- This usually happens under high load

YOUR TASK:
1. Check database connection pool settings
2. Look for connection leaks in the code
3. Increase pool size in configuration
4. Deploy and monitor

Problem:
- Chains unverified assumptions (think, probably, likely, usually)
- Prescribes solution before investigation
- Prevents agent from examining actual logs/evidence
- Prevents agent from discovering actual root cause
- May implement wrong fix based on false assumptions
```

---

## Example 6: Documentation Task Delegation

**Scenario**: User requests "Document the new authentication system"

**Correct Delegation**:

```text
Task(
  agent="documentation-expert",
  prompt="""
Your ROLE_TYPE is sub-agent.

Create comprehensive user-facing documentation for the authentication system.

OBSERVATIONS:
- New authentication middleware was recently implemented
- System uses JWT tokens with Bearer authentication
- Public routes and protected routes are distinguished
- No existing authentication documentation found

DEFINITION OF SUCCESS:
- Complete user-facing documentation for authentication system
- Covers:
  - How to authenticate (obtain tokens)
  - How to use tokens in requests
  - Public vs protected endpoints
  - Error handling and status codes
  - Example requests and responses
- Documentation is clear, accurate, and includes code examples
- Follows existing project documentation style and format

CONTEXT:
- Location: ./docs/ directory (or wherever project docs live)
- Scope: User-facing authentication documentation
- Constraints: Must be accurate to actual implementation

YOUR TASK:
1. Run SlashCommand /is-it-done to understand completion criteria
2. Use /is-it-done checklists as working guide
3. Examine authentication implementation in ./src/api/auth.py (or middleware location)
4. Test authentication flow to understand user experience
5. Review existing documentation for style and format patterns
6. Write comprehensive documentation covering all aspects
7. Include concrete code examples for common use cases
8. Verify documentation accuracy by testing examples
9. Verify /is-it-done criteria satisfied

INVESTIGATION REQUIREMENTS:
- Understand complete authentication flow
- Identify all public vs protected endpoints
- Document all possible error responses
- Test examples to ensure accuracy

VERIFICATION REQUIREMENTS:
- All code examples are tested and work correctly
- Documentation covers all user-facing aspects
- Follows project documentation style
- Technical accuracy verified against implementation

AVAILABLE RESOURCES:
- Authentication implementation in ./src/api/ (examine for accurate details)
- Existing documentation in ./docs/ showing project style
- API testing tools available to verify examples
- Full project context for understanding integration
"""
)
```

**Why This Works**:
- Agent examines actual implementation for accuracy
- Agent tests examples to ensure they work
- Agent discovers project documentation patterns
- Emphasizes accuracy over speed

**Anti-Pattern to Avoid**:

```text
❌ INCORRECT - Prescribing content

YOUR TASK:
Write documentation with these sections:
1. Introduction - explain JWT
2. Getting Started - show curl example
3. Protected Routes - list all protected endpoints
4. Error Codes - table of status codes

Use this template:
[Provides complete template with placeholder text]

Problem:
- Prescribes structure without letting agent examine implementation
- Provides template that may not match actual system
- Prevents agent from discovering what actually needs documenting
- May produce inaccurate documentation based on assumptions
```

---

## Common Patterns Summary

### Effective Delegation Checklist

✅ Use observations, not assumptions
✅ Define success criteria, not implementation steps
✅ List available resources, don't prescribe specific tools
✅ Enable comprehensive discovery
✅ Trust agent expertise
✅ Include /is-it-done in YOUR TASK section
✅ Pass through errors already in context
✅ Use world-building AVAILABLE RESOURCES

### Anti-Patterns to Avoid

❌ Pre-gathering data (run commands to collect errors/info before delegating)
❌ Assumption cascades ("I think", "probably", "likely")
❌ Prescribing implementation (exact steps, line numbers, specific tools)
❌ Discovery limiting ("just read these files")
❌ Tool dictation ("use tool X")
❌ Micromanagement (exact code changes)
❌ Reductive tool lists (listing 3 tools when agent has 50+)
❌ Confidence masking (stating assumptions as facts)

---

[← Back to README](../README.md) | [Skills Reference](./skills.md)
