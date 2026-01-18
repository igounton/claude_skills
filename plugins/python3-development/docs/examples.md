# Usage Examples

This document provides concrete, real-world examples of using the python3-development plugin.

## Example 1: Creating a Python CLI Tool with Typer and Rich

**Scenario**: Build a CLI tool to process CSV files with progress bars and colored output.

**Steps**:

1. **Skill activates automatically** (working with Python + CLI mentioned):
   ```text
   User: "Build a CLI tool to process CSV files with progress bars"

   Claude: Activating python3-development skill...
   ```

2. **Orchestrator reads the orchestration guide**:
   ```text
   Claude (internal): Reading python-development-orchestration.md
   Pattern identified: Feature Addition workflow
   Agent chain: @agent-python-cli-architect → @agent-python-pytest-architect → @agent-python-code-reviewer
   ```

3. **Delegation to python-cli-architect**:
   ```text
   Task(
     agent="python-cli-architect",
     prompt="""Create CSV processing CLI tool with:
     - Typer for argument parsing
     - Rich for progress bars and colored output
     - PEP 723 metadata for dependencies
     - Type hints throughout

     Scope: packages/csv_tool/main.py only
     Success criteria: Functional CLI with --input, --output, --format flags
     """
   )
   ```

4. **Agent implements**:
   ```python
   #!/usr/bin/env -S uv --quiet run --active --script
   # /// script
   # dependencies = [
   #   "typer>=0.9.0",
   #   "rich>=13.0.0",
   #   "pandas>=2.0.0",
   # ]
   # ///

   from pathlib import Path
   from typing import Annotated

   import pandas as pd
   import typer
   from rich.console import Console
   from rich.progress import track

   app = typer.Typer()
   console = Console()

   @app.command()
   def process(
       input_file: Annotated[Path, typer.Argument(help="CSV file to process")],
       output_file: Annotated[Path, typer.Option("--output", "-o")] = Path("output.csv"),
       format: Annotated[str, typer.Option(help="Output format")] = "csv",
   ) -> None:
       """Process CSV file with progress tracking."""
       df = pd.read_csv(input_file)

       for _ in track(range(len(df)), description="Processing..."):
           # Processing logic here
           pass

       df.to_csv(output_file, index=False)
       console.print(f":white_check_mark: Processed {len(df)} rows", style="green")

   if __name__ == "__main__":
       app()
   ```

5. **Delegation to pytest-architect for tests**:
   ```text
   Task(
     agent="python-pytest-architect",
     prompt="""Create test suite for CSV processor.

     Scope: tests/test_csv_tool.py only
     Coverage required: >80%
     Test cases: valid input, missing file, invalid format, empty CSV
     """
   )
   ```

6. **Quality gates validation**:
   ```bash
   # Format first
   uv run ruff format packages/csv_tool/

   # Lint
   uv run ruff check packages/csv_tool/

   # Type check
   uv run basedpyright packages/csv_tool/

   # Test
   uv run pytest tests/test_csv_tool.py -v --cov=packages/csv_tool
   ```

7. **Validation with external commands**:
   ```text
   /modernpython packages/csv_tool/main.py
   /shebangpython packages/csv_tool/main.py
   ```

8. **Delegation to code-reviewer**:
   ```text
   Task(
     agent="python-code-reviewer",
     prompt="""Review CSV processor for:
     - Modern Python 3.11+ patterns
     - Typer and Rich best practices
     - Exception handling patterns
     - Code smells

     Scope: Review only, no implementation
     """
   )
   ```

**Result**: Fully functional, type-safe CSV processing CLI tool with comprehensive tests, passing all quality gates.

---

## Example 2: Implementing Comprehensive Type Safety with Mypy

**Scenario**: Add comprehensive type hints to an existing Python module with complex data structures.

**Steps**:

1. **User request**:
   ```text
   User: "Add full type hints to the data processing module"
   ```

2. **Skill activates** (Python + type hints mentioned):
   ```text
   Claude: Activating python3-development skill for type safety guidance
   ```

3. **Reference mypy documentation patterns**:
   ```text
   Claude (internal): Reading mypy patterns from skill references
   - Generics for container classes
   - Protocols for duck typing
   - TypedDict for JSON-like structures
   - Type narrowing for unions
   ```

4. **Before (untyped)**:
   ```python
   def process_data(data):
       results = []
       for item in data:
           if validate(item):
               results.append(transform(item))
       return results

   def validate(item):
       return item.get("status") == "active"
   ```

5. **After (fully typed with Python 3.11+ patterns)**:
   ```python
   from typing import TypedDict, Protocol

   class DataItem(TypedDict):
       id: str
       status: str
       value: float
       metadata: dict[str, str]

   class Validator(Protocol):
       def __call__(self, item: DataItem) -> bool: ...

   class Transformer[T]:
       """Generic transformer for type-safe data processing."""

       def __init__(self, validator: Validator) -> None:
           self._validator = validator

       def process(self, data: list[DataItem]) -> list[DataItem]:
           """Process data items, keeping only valid ones."""
           results: list[DataItem] = []
           for item in data:
               if self._validator(item):
                   transformed = self._transform(item)
                   results.append(transformed)
           return results

       def _transform(self, item: DataItem) -> DataItem:
           """Transform a single item."""
           return item  # Actual transformation logic

   def validate_active(item: DataItem) -> bool:
       """Validate that item has active status."""
       return item.get("status") == "active"

   # Usage with type safety
   transformer = Transformer[DataItem](validate_active)
   processed: list[DataItem] = transformer.process(raw_data)
   ```

6. **Type checking validation**:
   ```bash
   # Detect type checker from project config
   uv run basedpyright packages/data_processing/

   # Result: ✓ No type errors found
   ```

7. **Mypy strict mode configuration**:
   ```toml
   [tool.mypy]
   python_version = "3.11"
   strict = true
   warn_return_any = true
   disallow_untyped_defs = true
   disallow_any_generics = true
   ```

**Result**: Fully type-safe module with generic transformers, protocols for duck typing, and TypedDict for structured data. All type checkers pass with strict mode enabled.

---

## Example 3: Using Orchestration Workflow for Feature Addition

**Scenario**: Add OAuth authentication to an existing Flask application.

**Steps**:

1. **User request**:
   ```text
   User: "Add OAuth authentication with Google sign-in to the Flask app"
   ```

2. **Pre-delegation protocol** (orchestrator):
   ```text
   Claude (orchestrator):

   Step 1: Read orchestration guide ✓
   Read("~/.claude/skills/python3-development/references/python-development-orchestration.md")

   Step 2: Identify workflow pattern ✓
   Pattern: Feature Addition (new capability, not refactoring existing)

   Step 3: Plan agent chain ✓
   Chain: @agent-spec-architect → @agent-python-cli-architect → @agent-python-pytest-architect → @agent-python-code-reviewer

   Step 4: Define scope boundaries ✓
   - spec-architect: Architecture design only (no implementation)
   - python-cli-architect: Implementation only (no architecture decisions)
   - pytest-architect: Test suite only (no implementation changes)
   - code-reviewer: Review only (no changes)

   Step 5: Set success criteria ✓
   - OAuth flow works with Google
   - User session management secure
   - Tests cover auth flow >90%
   - Security scan passes
   ```

3. **Architecture phase**:
   ```text
   Task(
     agent="spec-architect",
     prompt="""Design OAuth authentication architecture for Flask app.

     Requirements:
     - Google OAuth 2.0 integration
     - Secure session management
     - Token refresh handling

     Deliverables:
     - Component diagram
     - Data flow specification
     - Security considerations
     - Integration points with existing app
     """
   )
   ```

4. **Implementation phase**:
   ```text
   Task(
     agent="python-cli-architect",
     prompt="""Implement OAuth authentication following architecture spec.

     Scope: packages/auth/ directory only
     Files to create:
     - packages/auth/oauth.py (OAuth client)
     - packages/auth/session.py (Session management)
     - packages/auth/routes.py (Flask routes)

     Requirements:
     - Use authlib for OAuth
     - Type hints throughout
     - Modern Python 3.11+ patterns
     - Comprehensive docstrings
     """
   )
   ```

5. **Testing phase**:
   ```text
   Task(
     agent="python-pytest-architect",
     prompt="""Create test suite for OAuth authentication.

     Scope: tests/auth/ directory only
     Coverage required: >90%

     Test cases:
     - OAuth flow (mocked Google responses)
     - Session creation and validation
     - Token refresh
     - Error handling (invalid tokens, network failures)
     - Security edge cases (CSRF, token injection)
     """
   )
   ```

6. **Quality gates**:
   ```bash
   # Pre-commit hook runs all checks
   uv run prek run --files packages/auth/ tests/auth/

   # Additional security scan for auth code
   uv run bandit -r packages/auth/
   ```

7. **Review phase**:
   ```text
   Task(
     agent="python-code-reviewer",
     prompt="""Review OAuth authentication implementation.

     Focus areas:
     - Security best practices (OWASP guidelines)
     - Session management patterns
     - Error handling completeness
     - Token storage security
     - Modern Python patterns compliance

     Scope: Review only, document findings
     """
   )
   ```

8. **Final validation**:
   ```text
   /modernpython packages/auth/
   Security scan: ✓ No issues found
   Tests: ✓ 94% coverage
   Type checking: ✓ No errors
   Linting: ✓ Clean
   ```

**Result**: OAuth authentication implemented with comprehensive security review, >90% test coverage, and all quality gates passing. Architecture-first approach prevented costly refactoring.

---

## Example 4: Creating Portable Scripts with PEP 723 Metadata

**Scenario**: Create a standalone deployment script with external dependencies that can be executed anywhere.

**Steps**:

1. **User request**:
   ```text
   User: "Create a deployment script that checks server health and deploys the application"
   ```

2. **Skill recommends PEP 723** (script with dependencies mentioned):
   ```text
   Claude: This requires external dependencies (httpx for health checks, rich for output).
   Recommendation: Use PEP 723 inline metadata for portable single-file executable.
   ```

3. **Script creation**:
   ```python
   #!/usr/bin/env -S uv --quiet run --active --script
   # /// script
   # requires-python = ">=3.11"
   # dependencies = [
   #   "httpx>=0.27.0",
   #   "rich>=13.0.0",
   #   "typer>=0.9.0",
   # ]
   # ///
   """Deployment script with health check and application deployment.

   Portable single-file executable using PEP 723 metadata.
   No virtualenv or pip install required - just run it!
   """

   from typing import Annotated
   from pathlib import Path

   import httpx
   import typer
   from rich.console import Console
   from rich.progress import Progress, SpinnerColumn, TextColumn

   app = typer.Typer()
   console = Console()

   @app.command()
   def deploy(
       server: Annotated[str, typer.Argument(help="Server URL")],
       app_path: Annotated[Path, typer.Argument(help="Application directory")],
       health_endpoint: Annotated[str, typer.Option("--health")] = "/health",
       timeout: Annotated[int, typer.Option(help="Health check timeout")] = 30,
   ) -> None:
       """Deploy application after health check."""
       health_url = f"{server}{health_endpoint}"

       with Progress(
           SpinnerColumn(),
           TextColumn("[progress.description]{task.description}"),
           console=console,
       ) as progress:
           # Health check
           task = progress.add_task("Checking server health...", total=None)

           try:
               response = httpx.get(health_url, timeout=timeout)
               response.raise_for_status()
               progress.update(task, completed=True)
               console.print(":white_check_mark: Server healthy", style="green")
           except httpx.HTTPError as e:
               console.print(f":cross_mark: Health check failed: {e}", style="red")
               raise typer.Exit(1) from e

           # Deploy
           task = progress.add_task("Deploying application...", total=None)
           # Deployment logic here
           progress.update(task, completed=True)

       console.print(":sparkles: Deployment complete!", style="green bold")

   if __name__ == "__main__":
       app()
   ```

4. **Validation with /shebangpython**:
   ```text
   /shebangpython scripts/deploy.py

   Result:
   ✓ Shebang correct for script with dependencies
   ✓ PEP 723 metadata present
   ✓ Dependencies declared: httpx, rich, typer
   ✓ Python version requirement: >=3.11
   ✓ Execute bit set
   ```

5. **Usage** (no installation required):
   ```bash
   # On any machine with uv and Python 3.11+
   ./scripts/deploy.py https://api.example.com ./app

   # First run: uv automatically fetches dependencies
   # Subsequent runs: cached dependencies, instant execution
   ```

**Result**: Portable single-file deployment script that runs anywhere with Python 3.11+ and uv. No virtualenv setup, no requirements.txt, no pip install. Dependencies declared inline and handled automatically.

---

## Example 5: Setting Up Quality Gates with Pre-commit/Prek

**Scenario**: Configure automated quality checks for a Python project using the linting discovery protocol.

**Steps**:

1. **User request**:
   ```text
   User: "Set up automated linting and type checking for the project"
   ```

2. **Linting discovery protocol** (skill executes automatically):
   ```bash
   # Step 1: Check for git hook tool
   test -f .pre-commit-config.yaml
   # Result: Not found

   # Step 2: Check CI pipeline
   test -f .gitlab-ci.yml
   # Result: Found

   # Read CI config to identify tools
   grep -E "ruff|basedpyright|pytest" .gitlab-ci.yml
   # Result: Using ruff, basedpyright, pytest
   ```

3. **Copy asset template**:
   ```bash
   # Copy standard pre-commit config from skill assets
   cp ~/.claude/skills/python3-development/assets/.pre-commit-config.yaml .
   ```

4. **Customize configuration**:
   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.5.0
       hooks:
         - id: ruff-format  # Format first
         - id: ruff         # Then lint

     - repo: https://github.com/RobertCraigie/pyright-python
       rev: v1.1.370
       hooks:
         - id: basedpyright  # Type check (detected from CI)

     - repo: https://github.com/pre-commit/mirrors-mypy
       rev: v1.10.0
       hooks:
         - id: mypy
           args: [--strict]
           additional_dependencies: [types-all]
   ```

5. **Detect and install git hook tool**:
   ```bash
   # Detection script from skill
   uv run holistic-linting/scripts/detect-hook-tool.py detect
   # Result: prek (Rust-based, faster than pre-commit)

   # Install hooks
   uv run prek install
   ```

6. **Test quality gates**:
   ```bash
   # Format-first workflow (automatic via hook)
   git add packages/mymodule.py
   git commit -m "Add new module"

   # Hook runs automatically:
   # 1. ruff-format (fixes formatting)
   # 2. ruff (checks linting)
   # 3. basedpyright (type checking)
   # 4. mypy (additional type checking)

   # Result: ✓ All checks passed
   ```

7. **Manual quality gate execution**:
   ```bash
   # Run on specific files
   uv run prek run --files packages/mymodule.py tests/test_mymodule.py

   # Run all hooks
   uv run prek run --all-files
   ```

8. **CI pipeline validation**:
   ```yaml
   # .gitlab-ci.yml
   test:
     script:
       - uv run prek run --all-files  # Same checks as local
       - uv run pytest --cov=packages/ --cov-report=xml
       - uv run bandit -r packages/
   ```

**Result**: Automated quality gates that run locally before commit and in CI pipeline. Format-first workflow prevents false positive linting errors. Same tool configuration locally and in CI ensures consistency.

---

## Example 6: Debugging Test Failures with Balanced Investigation

**Scenario**: Test suite failing after refactoring, need to determine if tests or implementation are wrong.

**Steps**:

1. **Test failure observed**:
   ```bash
   uv run pytest tests/test_parser.py -v

   FAILED tests/test_parser.py::test_parse_date - AssertionError: Expected '2024-01-15', got '2024-1-15'
   FAILED tests/test_parser.py::test_parse_time - AssertionError: Expected '14:30:00', got '14:30:0'
   ```

2. **Apply test-failure-mindset** (from command reference):
   ```text
   Claude (internal): Activating balanced investigative approach

   Hypothesis A: Tests expect zero-padded output, implementation changed
   Hypothesis B: Tests are wrong to expect zero-padding

   Need to investigate both before making changes.
   ```

3. **Investigate implementation**:
   ```python
   # Before refactoring
   def format_date(year: int, month: int, day: int) -> str:
       return f"{year:04d}-{month:02d}-{day:02d}"  # Zero-padded

   # After refactoring
   def format_date(year: int, month: int, day: int) -> str:
       return f"{year}-{month}-{day}"  # No padding
   ```

4. **Check requirements and usage**:
   ```python
   # API documentation says:
   # "Returns ISO 8601 formatted date string"

   # ISO 8601 requires zero-padding: YYYY-MM-DD
   ```

5. **Determination**:
   ```text
   Classification: Implementation Bug

   Evidence:
   - Tests expect ISO 8601 format (YYYY-MM-DD)
   - ISO 8601 requires zero-padding
   - Refactoring removed zero-padding
   - API documentation specifies ISO 8601

   Conclusion: Tests are correct. Implementation broke during refactoring.
   ```

6. **Fix implementation** (not tests):
   ```python
   def format_date(year: int, month: int, day: int) -> str:
       """Format date as ISO 8601 string.

       Args:
           year: Four-digit year
           month: Month (1-12)
           day: Day of month (1-31)

       Returns:
           ISO 8601 formatted date string (YYYY-MM-DD)
       """
       return f"{year:04d}-{month:02d}-{day:02d}"
   ```

7. **Re-run tests**:
   ```bash
   uv run pytest tests/test_parser.py -v
   # Result: ✓ All tests passed
   ```

**Result**: Bug caught by tests, not blamed on tests. Balanced investigation revealed refactoring broke ISO 8601 compliance. Tests saved the project from shipping incorrect date formatting.

---

## Summary

These examples demonstrate:

1. **Agent orchestration** - Reading guide first, planning agent chains, focused scope
2. **Modern Python patterns** - Type hints, generics, protocols, PEP 723
3. **Quality gates** - Format-first workflow, type checking, comprehensive testing
4. **Portable scripts** - PEP 723 inline metadata for single-file executables
5. **Automated tooling** - Pre-commit/prek setup with linting discovery protocol
6. **Balanced test analysis** - Investigating both hypotheses before fixing

Each example follows the skill's orchestration patterns and quality standards for professional Python development.
