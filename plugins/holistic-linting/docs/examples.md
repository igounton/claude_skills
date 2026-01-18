# Usage Examples

This document provides concrete, real-world examples of using the holistic-linting plugin in different scenarios.

---

## Example 1: Orchestrator Implements New Feature with Automatic Linting

**Scenario**: User requests a new authentication middleware feature. The orchestrator implements it and then uses the plugin's automatic workflow to ensure code quality.

**Context**:
- File: `src/middleware/auth.py`
- Changes: New authentication middleware class with JWT validation
- Linters: ruff, mypy, pyright

### Steps

1. **User Request**:
   ```text
   User: "Add JWT authentication middleware to validate tokens on all API endpoints"
   ```

2. **Orchestrator Implementation**:
   ```text
   Orchestrator:
   - Reads existing middleware patterns
   - Creates src/middleware/auth.py
   - Implements JWTAuthMiddleware class
   - Integrates with FastAPI application
   ```

3. **Automatic Linting Workflow (holistic-linting skill active)**:
   ```text
   Orchestrator:
   [Implementation complete, applying holistic-linting skill]
   [Delegates immediately WITHOUT running formatters/linters]

   Task(
     agent="linting-root-cause-resolver",
     prompt="Format, lint, and resolve any issues in src/middleware/auth.py"
   )
   ```

4. **Agent Execution**:
   ```text
   linting-root-cause-resolver agent:
   1. Loads holistic-linting + python3-development skills
   2. Runs formatter: uv run ruff format src/middleware/auth.py
      → Formatted 1 file
   3. Runs linters:
      - uv run ruff check src/middleware/auth.py
        → 2 errors found: F401 (unused import), B008 (mutable default)
      - uv run mypy src/middleware/auth.py
        → 1 error: Incompatible return value type
      - uv run pyright src/middleware/auth.py
        → 1 error: reportOptionalMemberAccess
   4. Investigates each issue using linter-specific workflows:
      - F401: Research with ruff rule F401 → Remove unused 'datetime' import
      - B008: Research with ruff rule B008 → Use None default, initialize in __post_init__
      - mypy: Research return-value error → Fix signature from Response to dict[str, Any]
      - pyright: Research reportOptionalMemberAccess → Add type guard for None check
   5. Implements all fixes following python3-development patterns
   6. Verifies:
      - uv run ruff check src/middleware/auth.py ✓ Clean
      - uv run mypy src/middleware/auth.py ✓ Clean
      - uv run pyright src/middleware/auth.py ✓ Clean
   7. Creates artifacts:
      - .claude/reports/linting-investigation-auth-middleware-20260118.md
      - .claude/reports/linting-resolution-auth-middleware-20260118.md
      - .claude/artifacts/linting-artifacts-auth-middleware-20260118.json
   ```

5. **Architectural Review**:
   ```text
   Orchestrator:
   Task(
     agent="post-linting-architecture-reviewer",
     prompt="Review linting resolution for src/middleware/auth.py"
   )

   post-linting-architecture-reviewer agent:
   1. Loads artifacts from .claude/reports/
   2. Verifies resolution quality:
      ✓ All fixes address root causes
      ✓ Solutions align with FastAPI middleware patterns
      ✓ Type safety improved with proper annotations
   3. Analyzes architectural impact:
      - Middleware follows single responsibility principle
      - Token validation separated from business logic
      - Error handling consistent with project patterns
   4. Identifies systemic improvements:
      - Other middleware could benefit from similar type annotations
      - Consider extracting JWT validation to separate service
   5. Creates architectural review report:
      - .claude/reports/architectural-review-auth-middleware-20260118.md
   ```

6. **Orchestrator Reads Review**:
   ```bash
   Read(".claude/reports/architectural-review-auth-middleware-20260118.md")
   ```

7. **Result**:
   ```text
   Orchestrator: "✓ JWT authentication middleware implemented and validated. All linting issues resolved at root cause. Architectural review confirms quality standards met. Feature ready for testing."
   ```

### Code Changes Made

**Before (with issues)**:
```python
from datetime import datetime  # F401: unused
from fastapi import Request, Response
from typing import Callable

class JWTAuthMiddleware:
    def __init__(self, secret_key: str, allowed_algorithms: list[str] = ["HS256"]):  # B008
        self.secret_key = secret_key
        self.allowed_algorithms = allowed_algorithms

    async def __call__(self, request: Request, call_next: Callable) -> Response:  # mypy: wrong return type
        token = request.headers.get("Authorization")
        decoded = self.decode_token(token)  # pyright: token could be None
        request.state.user = decoded
        return await call_next(request)
```

**After (resolved)**:
```python
from fastapi import Request
from typing import Callable, Any

class JWTAuthMiddleware:
    def __init__(self, secret_key: str, allowed_algorithms: list[str] | None = None):
        self.secret_key = secret_key
        self.allowed_algorithms = allowed_algorithms or ["HS256"]

    async def __call__(self, request: Request, call_next: Callable) -> dict[str, Any]:
        token = request.headers.get("Authorization")
        if token is None:
            raise ValueError("Authorization header missing")
        decoded = self.decode_token(token)
        request.state.user = decoded
        response = await call_next(request)
        return response
```

---

## Example 2: Sub-Agent Creates Module with Inline Linting

**Scenario**: An orchestrator delegates creation of a database connection pool module to a sub-agent. The sub-agent applies holistic-linting workflow before completing.

**Context**:
- File: `src/db/pool.py`
- Sub-agent task: Create connection pool with async support
- Linters: ruff, mypy

### Steps

1. **Orchestrator Delegation**:
   ```text
   Task(
     agent="general-purpose",
     prompt="Create database connection pool module at src/db/pool.py with async support for PostgreSQL"
   )
   ```

2. **Sub-Agent Implementation**:
   ```text
   Sub-agent:
   1. Reads project database patterns
   2. Creates src/db/pool.py
   3. Implements AsyncConnectionPool class
   4. Adds connection lifecycle methods
   ```

3. **Sub-Agent Applies Linting (before completion)**:
   ```text
   Sub-agent:
   [Implementation complete, applying holistic-linting skill before task completion]

   1. Read CLAUDE.md LINTERS section:
      → Formatters: ruff format [*.py]
      → Linters: ruff check [*.py], mypy [*.py]

   2. Run formatter:
      Bash("uv run ruff format src/db/pool.py")
      → Formatted 1 file

   3. Run linters:
      Bash("uv run ruff check src/db/pool.py")
      → 1 error: E501 (line too long)

      Bash("uv run mypy src/db/pool.py")
      → 1 error: Missing return type annotation on get_connection()

   4. Investigate and resolve E501:
      - Research: ruff rule E501
      - Finding: Connection string is 105 characters (limit 88)
      - Fix: Use textwrap for multi-line string

   5. Investigate and resolve mypy error:
      - Research: Check mypy error_code_list.rst
      - Finding: Function should return -> AsyncConnection
      - Fix: Add return type annotation

   6. Verify resolution:
      Bash("uv run ruff check src/db/pool.py")
      → ✓ Clean

      Bash("uv run mypy src/db/pool.py")
      → ✓ Clean

   7. Task complete - return to orchestrator ✓
   ```

### Code Changes Made

**Before (with issues)**:
```python
from asyncpg import create_pool, Pool

class AsyncConnectionPool:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string  # E501: too long in actual usage
        self.pool: Pool | None = None

    async def get_connection(self):  # mypy: missing return type
        if self.pool is None:
            await self.connect()
        return await self.pool.acquire()
```

**After (resolved)**:
```python
from textwrap import dedent
from asyncpg import create_pool, Pool, Connection as AsyncConnection

class AsyncConnectionPool:
    def __init__(self, connection_string: str):
        # Multi-line for readability
        self.connection_string = dedent("""
            postgresql://user:pass@localhost:5432/dbname
            ?sslmode=require&pool_size=20
        """).replace("\n", "")
        self.pool: Pool | None = None

    async def get_connection(self) -> AsyncConnection:
        if self.pool is None:
            await self.connect()
        return await self.pool.acquire()
```

---

## Example 3: Multiple Files with Concurrent Agent Resolution

**Scenario**: Orchestrator refactors authentication across multiple modules. Each file gets its own linting agent running concurrently.

**Context**:
- Files: `src/auth.py`, `src/api.py`, `tests/test_auth.py`
- Changes: Updated authentication logic across all three files
- Linters: ruff, mypy, pyright

### Steps

1. **Orchestrator Implementation**:
   ```text
   Orchestrator:
   - Refactors authentication to use new token format
   - Modifies src/auth.py (auth logic)
   - Modifies src/api.py (API integration)
   - Modifies tests/test_auth.py (test updates)
   ```

2. **Launch Concurrent Linting Agents**:
   ```text
   Orchestrator:
   [Implementation complete, launching concurrent linting agents]

   Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/auth.py")
   Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in src/api.py")
   Task(agent="linting-root-cause-resolver", prompt="Format, lint, and resolve any issues in tests/test_auth.py")
   ```

3. **Agents Execute in Parallel**:
   ```text
   Agent 1 (src/auth.py):
   - Formats with ruff format
   - Finds 2 ruff errors, 1 mypy error
   - Resolves all 3 issues
   - Creates artifacts
   - Completes

   Agent 2 (src/api.py):
   - Formats with ruff format
   - Finds 1 mypy error, 1 pyright error
   - Resolves both issues
   - Creates artifacts
   - Completes

   Agent 3 (tests/test_auth.py):
   - Formats with ruff format
   - Finds no errors (tests already clean)
   - Creates completion report
   - Completes
   ```

4. **Orchestrator Reads All Reports**:
   ```bash
   ls -la .claude/reports/linting-resolution-*.md
   ```

5. **Launch Concurrent Reviews**:
   ```text
   Task(agent="post-linting-architecture-reviewer", prompt="Review linting resolution for src/auth.py")
   Task(agent="post-linting-architecture-reviewer", prompt="Review linting resolution for src/api.py")
   ```

6. **Result**:
   ```text
   Orchestrator: "✓ Authentication refactoring complete across 3 files. All linting issues resolved. Architectural reviews confirm consistency. Ready for integration testing."
   ```

---

## Example 4: Discovering Project Linters

**Scenario**: New project without documented linting configuration. Use `/lint init` to discover and document linters.

**Context**:
- Project has `.pre-commit-config.yaml`, `pyproject.toml`, `package.json`
- No LINTERS section in CLAUDE.md yet

### Steps

1. **User Command**:
   ```text
   /lint init
   ```

2. **Discovery Process**:
   ```text
   Claude:
   1. Checking for existing ## LINTERS section in CLAUDE.md...
      → Not found, proceeding with discovery

   2. Scanning project configuration files:

      Bash("test -d .git && echo 'Git: yes'")
      → Git: yes

      Bash("test -f .pre-commit-config.yaml && echo 'pre-commit: found'")
      → pre-commit: found

      Read(".pre-commit-config.yaml")
      → Found 6 hooks: ruff (format + check), mypy, pyright, markdownlint-cli2, prettier

      Read("pyproject.toml")
      → Found [tool.ruff], [tool.mypy], [tool.pyright] sections
      → ruff: target-version = "py311", line-length = 88
      → mypy: strict = true, python_version = "3.11"
      → pyright: typeCheckingMode = "strict"

      Read("package.json")
      → Found devDependencies: prettier, markdownlint-cli2

      Bash("test -f .git/hooks/pre-commit")
      → Git hooks: enabled

      Read(".git/hooks/pre-commit")
      → Line 2: Using 'pre-commit' tool

   3. Generating LINTERS section...
   ```

3. **Generated Configuration**:
   ```markdown
   ## LINTERS

   git pre-commit hooks: enabled
   pre-commit tool: pre-commit

   ### Formatters

   - ruff format [*.py]
   - prettier [*.{ts,js,tsx,jsx,json,md}]
   - markdownlint-cli2 [*.{md,markdown}]

   ### Static Checking and Linting

   - ruff check [*.py]
   - mypy [*.py]
   - pyright [*.py]
   - markdownlint-cli2 [*.{md,markdown}]
   ```

4. **Update CLAUDE.md**:
   ```text
   Claude:
   4. Appending to CLAUDE.md...
      Edit(file_path="CLAUDE.md", old_string="<end_of_file>", new_string="\n\n## LINTERS\n...")
      ✓ LINTERS section written to CLAUDE.md

   Discovery complete! Your project linters are now documented.
   Use `/lint <file>` to run linters on specific files.
   ```

---

## Example 5: Force Re-Discovery After Configuration Change

**Scenario**: Project added new linters (bandit for security). Re-discover with `--force` to update configuration.

**Context**:
- Added bandit to `.pre-commit-config.yaml`
- Existing LINTERS section in CLAUDE.md needs updating

### Steps

1. **User Command**:
   ```text
   /lint init --force
   ```

2. **Re-Discovery Process**:
   ```text
   Claude:
   1. Checking for existing ## LINTERS section in CLAUDE.md...
      → Found existing section
      → --force flag provided, will overwrite

   2. Removing existing section...
      Edit(file_path="CLAUDE.md", old_string="## LINTERS\n...\n", new_string="")

   3. Re-scanning project configuration...
      [Same discovery as Example 4, but now includes bandit]

      Read(".pre-commit-config.yaml")
      → Found 7 hooks: ruff, mypy, pyright, bandit, markdownlint-cli2, prettier

   4. Generating updated LINTERS section...
   ```

3. **Updated Configuration**:
   ```markdown
   ## LINTERS

   git pre-commit hooks: enabled
   pre-commit tool: pre-commit

   ### Formatters

   - ruff format [*.py]
   - prettier [*.{ts,js,tsx,jsx,json,md}]
   - markdownlint-cli2 [*.{md,markdown}]

   ### Static Checking and Linting

   - ruff check [*.py]
   - mypy [*.py]
   - pyright [*.py]
   - bandit [*.py]
   - markdownlint-cli2 [*.{md,markdown}]
   ```

4. **Result**:
   ```text
   ✓ LINTERS section updated in CLAUDE.md with bandit security checks
   ```

---

## Example 6: Manual Linting with `/lint` Command

**Scenario**: Developer wants to manually lint specific files before committing.

**Context**:
- Files: `src/utils/helpers.py`, `src/utils/validators.py`
- LINTERS section exists in CLAUDE.md

### Steps

1. **User Command**:
   ```text
   /lint src/utils/helpers.py src/utils/validators.py
   ```

2. **Linting Process**:
   ```text
   Claude:
   1. Reading ## LINTERS section from CLAUDE.md...
      → Found formatters: ruff format [*.py]
      → Found linters: ruff check [*.py], mypy [*.py], pyright [*.py]

   2. Running formatters on 2 files...
      Bash("uv run ruff format src/utils/helpers.py src/utils/validators.py")
      → Formatted 2 files

   3. Running linters on 2 files...
      Bash("uv run ruff check src/utils/helpers.py src/utils/validators.py")
      → helpers.py: 1 error (F841: unused variable)
      → validators.py: Clean

      Bash("uv run mypy src/utils/helpers.py src/utils/validators.py")
      → helpers.py: 1 error (arg-type mismatch)
      → validators.py: Clean

      Bash("uv run pyright src/utils/helpers.py src/utils/validators.py")
      → helpers.py: Clean
      → validators.py: Clean

   4. Launching linting-root-cause-resolver for files with errors...
      Task(
        agent="linting-root-cause-resolver",
        prompt="Format, lint, and resolve any issues in src/utils/helpers.py"
      )

   5. Agent resolves both errors in helpers.py

   6. Re-running linters to verify...
      Bash("uv run ruff check src/utils/helpers.py")
      → ✓ Clean

      Bash("uv run mypy src/utils/helpers.py")
      → ✓ Clean

   7. All linting errors resolved ✓
   ```

---

## Example 7: Type Error Investigation with Mypy

**Scenario**: Mypy reports a complex type error involving generic types and protocol conformance.

**Context**:
- File: `src/services/api_client.py`
- Error: `error: Argument 1 has incompatible type "dict[str, Any]"; expected "Serializable"`

### Steps

1. **Agent Investigates**:
   ```text
   linting-root-cause-resolver:
   1. Load holistic-linting + python3-development skills

   2. Research mypy error code:
      Grep(pattern="arg-type", path="./references/rules/mypy/error_code_list.rst")
      → Found [arg-type] error code documentation
      → Principle: Arguments must match parameter type annotations

   3. Read affected code:
      Read("src/services/api_client.py")
      → Line 45: serialize_response(response_data)
      → response_data: dict[str, Any]
      → serialize_response parameter: data: Serializable

   4. Trace type flow:
      - What is Serializable?
      Grep(pattern="class Serializable", output_mode="content")
      → Found: Protocol with __serialize__ method

      - Does dict implement this protocol?
      → No, dict doesn't have __serialize__ method

      - What should we pass?
      Read code context → serialize_response expects objects with __serialize__

   5. Check architectural context:
      Grep(pattern="serialize_response", output_mode="content")
      → Used in 5 other files, all pass model instances
      → response_data should be converted to model first

   6. Implement fix:
      - Don't pass raw dict
      - Convert to ResponseModel first
      - ResponseModel implements Serializable protocol
   ```

2. **Fix Applied**:
   ```python
   # Before
   response_data: dict[str, Any] = await fetch_api_data()
   serialized = serialize_response(response_data)  # mypy error

   # After
   response_data: dict[str, Any] = await fetch_api_data()
   response_model = ResponseModel.from_dict(response_data)
   serialized = serialize_response(response_model)  # mypy: OK
   ```

3. **Verification**:
   ```bash
   uv run mypy src/services/api_client.py
   # Success: no issues found
   ```

---

## Example 8: Security Issue Detection with Bandit

**Scenario**: Agent detects security vulnerability during linting.

**Context**:
- File: `src/utils/crypto.py`
- Bandit reports: B303 (insecure hash function)

### Steps

1. **Agent Investigates**:
   ```text
   linting-root-cause-resolver:
   1. Research Bandit rule B303:
      Read("./references/rules/bandit/index.md")
      → B303: Use of insecure MD5 or SHA1 hash function
      → Risk: Collision attacks, not suitable for cryptographic purposes
      → Severity: HIGH

   2. Read affected code:
      Read("src/utils/crypto.py")
      → Line 23: hashlib.md5(data.encode()).hexdigest()
      → Used for: Password hashing

   3. Check context:
      → Password hashing requires cryptographic security
      → MD5 is broken for this purpose
      → Need secure alternative

   4. Research secure alternative:
      → Use bcrypt or argon2 for password hashing
      → These have built-in salt and iteration count

   5. Implement secure fix:
      - Replace hashlib.md5 with bcrypt
      - Add salt generation
      - Use proper work factor
   ```

2. **Fix Applied**:
   ```python
   # Before (INSECURE)
   import hashlib

   def hash_password(password: str) -> str:
       return hashlib.md5(password.encode()).hexdigest()  # B303: insecure

   # After (SECURE)
   import bcrypt

   def hash_password(password: str) -> str:
       salt = bcrypt.gensalt(rounds=12)
       return bcrypt.hashpw(password.encode(), salt).decode()
   ```

3. **Verification**:
   ```bash
   uv run bandit src/utils/crypto.py
   # No issues found
   ```

4. **Architectural Review Identifies Broader Issue**:
   ```text
   post-linting-architecture-reviewer:

   Finding: Password hashing was using insecure MD5

   Systemic Improvement:
   - Audit entire codebase for hashlib.md5 usage
   - Check if other security-sensitive operations use weak crypto
   - Document secure hashing standards in CLAUDE.md

   Proposed audit:
   ```bash
   rg "hashlib\.(md5|sha1)" --type py
   ```

   Review all matches for security implications.
   ```

---

## Key Takeaways from Examples

1. **Orchestrators delegate immediately** - Don't run linters yourself, let agents gather their own context
2. **Sub-agents lint before completion** - Always verify quality before returning to orchestrator
3. **Use concurrent agents for multiple files** - Parallel execution saves time
4. **Discovery saves repeated configuration** - `/lint init` creates reusable LINTERS section
5. **Root cause investigation prevents recurring issues** - Understanding principles improves future code
6. **Architectural review catches systemic problems** - Issues often reveal broader patterns
7. **Security issues require immediate attention** - Bandit findings should trigger comprehensive audits
8. **Type errors reveal design mismatches** - Mypy/Pyright errors often indicate architectural issues
