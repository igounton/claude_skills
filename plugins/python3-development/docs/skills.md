# Skills Reference

This document provides detailed reference information for the skills included in the python3-development plugin.

## python3-development

**Location**: `skills/python3-development/SKILL.md`

**Description**: Orchestration guide for Python development using specialized agents and modern Python 3.11-3.14 patterns. Provides comprehensive workflows for TDD, feature addition, refactoring, debugging, and code review with extensive reference documentation for modern Python modules, tools, and patterns.

**User Invocable**: Yes

**Version**: 1.2.0

**Python Compatibility**: 3.11+

**Last Updated**: 2026-01-14

### When to Use

The skill automatically activates when:

1. Working within any Python project
2. Python CLI applications with Typer and Rich are mentioned by the user
3. Tasked with Python script writing or editing
4. Building CI scripts or tools
5. Creating portable Python scripts with stdlib only
6. Planning out a python package design
7. Running any python script or test
8. Writing tests (unit, integration, e2e, validation) for a python script, package, or application
9. Reviewing Python code against best practices or for code smells
10. The python command fails to run or errors, or the python3 command shows errors
11. Pre-commit or linting errors occur in python files
12. Writing or editing python code in a git repository

### Activation

**Automatic**: Claude decides when to use based on task context

**Manual**:

```text
@python3-development
```

**Skill tool invocation**:

```text
Skill(command: "python3-development")
```

### What This Skill Provides

1. **Workflow patterns** for test-driven development, feature addition, refactoring, debugging, and code review using modern Python 3.11+ patterns
2. **References to favored modules** - 50+ modern Python libraries with usage patterns
3. **Working pyproject.toml configurations** - Complete build, linting, and type checking setups
4. **Linting and formatting configuration** - ruff, mypy/basedpyright/pyright, pytest integration
5. **Resource files** that provide solutions to known errors and linting issues
6. **Project layouts** the user prefers - standard directory structure and naming conventions

### Core Concepts

#### Python Development Standards

- **Python Version**: Python 3.11+ required (3.12+ recommended for native generic syntax)
- **Docstring Standard**: Google style (Args/Returns/Raises sections)
- **Type Safety**: Comprehensive mypy typing with generics, protocols, TypedDict
- **Script Dependencies**: PEP 723 inline metadata for scripts with dependencies
- **Quality Gates**: Format-first workflow with ruff → type checking → pytest

#### Modern Python Patterns

The skill enforces Python 3.11+ patterns:

- Native generics: `list[str]` instead of `List[str]`
- Union types: `str | int` instead of `Union[str, int]`
- PEP 723: Inline script metadata for portable executables
- Type-safe async: Proper async/await patterns
- Modern syntax: StrEnum, Protocol, TypeVar, Self type

#### Script Dependency Trade-offs

**Scripts with dependencies (Typer + Rich via PEP 723)**:
- Benefits: Less complexity, better UX, well-tested libraries
- Trade-off: Requires network access on first run

**Stdlib-only scripts**:
- Benefits: Maximum portability, runs without network
- Trade-offs: More development complexity, basic UX

**Default recommendation**: Use Typer + Rich with PEP 723 unless specific portability requirements prevent network access.

### Agent Orchestration (Orchestrators Only)

#### Pre-Delegation Protocol

Before using the Task tool for ANY Python development delegation, orchestrators MUST complete:

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Read orchestration guide | `Read("~/.claude/skills/python3-development/references/python-development-orchestration.md")` |
| 2 | Identify workflow pattern | Which pattern? (TDD / Feature Addition / Refactoring / Debugging / Code Review) |
| 3 | Plan agent chain | List ALL agents needed in sequence |
| 4 | Define scope boundaries | What is IN scope? What is OUT of scope for each agent? |
| 5 | Set success criteria | What specific, measurable outcomes define completion? |

**BLOCKING RULE**: If you cannot answer steps 2-5 from memory, you have NOT read the orchestration guide.

#### Delegation Pattern

Orchestrators delegate rather than implement:

| Task Type | Delegation Target |
|-----------|-------------------|
| Python code | `@agent-python-cli-architect` |
| Test creation | `@agent-python-pytest-architect` |
| Code review | `@agent-python-code-reviewer` |
| Stdlib-only script | `@agent-python-portable-script` |
| Architecture | `@agent-spec-architect` |
| Task breakdown | `@agent-spec-planner` |
| Requirements | `@agent-spec-analyst` |

**DO NOT pre-gather data for agents**. Agents perform their own Chain of Verification (CoVe). Provide:
- Outcomes: What must be true when done
- Constraints: User requirements, compatibility needs
- Known issues: Error messages (pass-through, not pre-gathered)
- File paths: Where to start looking (not what you found there)

### Quality Gates

Every Python task must pass:

1. **Format-first**: `uv run ruff format <files>` (or via pre-commit/prek)
2. **Linting**: `uv run ruff check <files>` (clean, after formatting)
3. **Type checking**: Use detected type checker (basedpyright/pyright/mypy)
4. **Tests**: `uv run pytest` (>80% coverage)
5. **Modern patterns**: `/modernpython` (no legacy typing)
6. **Script compliance**: `/shebangpython` (for standalone scripts)

**For critical code** (payments, auth, security):
- Coverage >95%
- Mutation testing: `uv run mutmut run` (>90% score)
- Security scan: `uv run bandit -r packages/`

### Linting Discovery Protocol

The skill executes this discovery sequence before any linting:

1. **Check for git hook tool**:
   ```bash
   test -f .pre-commit-config.yaml && echo "git hook config detected"
   ```
   If found, detect tool (pre-commit or prek) and run:
   ```bash
   uv run <detected-tool> run --files <files>
   ```

2. **Else check CI pipeline**:
   - Read `.gitlab-ci.yml` or `.github/workflows/*.yml`
   - Identify required linting tools and commands
   - Execute exact CI commands locally

3. **Else fallback to tool detection**:
   - Check `pyproject.toml` for dev tools
   - Use discovered tools with standard configurations

### Type Checker Discovery

Detection priority:
1. Check `.pre-commit-config.yaml` for basedpyright/pyright/mypy hooks
2. Check `pyproject.toml` for `[tool.basedpyright]` / `[tool.pyright]` / `[tool.mypy]`
3. Check CI config for type checker invocations

Common patterns:
- **basedpyright**: GitLab projects (native GitLab reporting)
- **pyright**: General TypeScript-style projects
- **mypy**: Python-first type checking

### Standard Project Structure

```text
project-root/
├── pyproject.toml
├── packages/
│   └── package_name/      # Hyphens in project → underscores in package
│       ├── __init__.py
│       └── ...
├── tests/
├── scripts/
├── sessions/              # Optional: cc-sessions framework
└── README.md
```

**Package naming**: Project `my-cli-tool` → Package directory `packages/my_cli_tool/`

### Reference Documentation

Complete guides in `references/` subdirectory:

- **[User Project Conventions](../skills/python3-development/references/user-project-conventions.md)** - Production project conventions (MANDATORY for new projects)
- **[Modern Python Modules](../skills/python3-development/references/modern-modules.md)** - 50+ library guides with usage patterns
- **[Tool & Library Registry](../skills/python3-development/references/tool-library-registry.md)** - Development tools catalog
- **[Python Development Orchestration](../skills/python3-development/references/python-development-orchestration.md)** - Workflow patterns for TDD, feature addition, refactoring, code review
- **[PEP 723 Reference](../skills/python3-development/references/PEP723.md)** - Inline script metadata guide
- **[Exception Handling](../skills/python3-development/references/exception-handling.md)** - Typer exception chain prevention
- **[API Reference](../skills/python3-development/references/api_reference.md)** - API specifications and integration guides

#### Navigating Large References

Find specific modules:
```bash
grep -i "^### " references/modern-modules.md
```

Search tools by category:
```bash
grep -A 5 "^## " references/tool-library-registry.md
```

Locate workflow patterns:
```bash
grep -i "^## " references/python-development-orchestration.md
```

### Asset Templates

Copy standard configurations:

```bash
# Version management
cp ~/.claude/skills/python3-development/assets/version.py packages/{package}/version.py

# Pre-commit configuration
cp ~/.claude/skills/python3-development/assets/.pre-commit-config.yaml .

# Markdown linting
cp ~/.claude/skills/python3-development/assets/.markdownlint.json .

# Editor settings
cp ~/.claude/skills/python3-development/assets/.editorconfig .

# Build hooks (only if needed for binaries/assets)
mkdir -p scripts/
cp ~/.claude/skills/python3-development/assets/hatch_build.py scripts/hatch_build.py
```

### External Commands

These slash commands are external dependencies (install to `~/.claude/commands/`):

- **[/modernpython](~/.claude/commands/modernpython.md)** - Python 3.11+ pattern enforcement and legacy code detection
- **[/shebangpython](~/.claude/commands/shebangpython.md)** - PEP 723 validation and shebang standards

### Type Safety Patterns

#### When to Use Generics

Use for type-safe container classes and functions working with multiple types:

- Custom collection classes (stacks, queues, boxes)
- Functions accepting multiple type variants
- Decorators and factory methods
- Reusable protocols and type aliases

**MUST read**: [Mypy Generics Documentation](../skills/python3-development/references/mypy-docs/generics.rst)

**Python 3.11 Pattern**:
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...
```

**Python 3.12+ Pattern**:
```python
class Stack[T]:
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...
```

#### When to Use Protocols

Use for structural subtyping (duck typing with type safety):

- Accept any object with specific capabilities without inheritance
- Define interfaces for duck-typed code
- Create flexible callback types

**MUST read**: [Mypy Protocols Documentation](../skills/python3-development/references/mypy-docs/protocols.rst)

**Example**:
```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def close_resource(resource: SupportsClose) -> None:
    resource.close()  # Works with ANY object having close()
```

#### TypedDict for Dictionary Typing

Use for dictionaries with fixed schemas:

- Dictionaries representing objects with predictable structure
- JSON-like data structures
- Configuration dictionaries
- API request/response payloads

**MUST read**: [Mypy TypedDict Documentation](../skills/python3-development/references/mypy-docs/typed_dict.rst)

### Workflow Patterns

The orchestration guide provides complete patterns for:

1. **TDD (Test-Driven Development)**: Design → Write Tests → Implement → Review → Validate
2. **Feature Addition**: Requirements → Architecture → Plan → Implement → Test → Review
3. **Code Review**: Self-Review → Standards Check → Agent Review → Fix → Re-validate
4. **Refactoring**: Tests First → Refactor → Validate → Review
5. **Debugging**: Reproduce → Trace → Fix → Test → Review

Each workflow uses agent chaining with specific quality gates.

### Rich Console Patterns

#### Panel and Table Width Handling

**Problem**: Rich containers wrap content at 80 characters in CI/non-TTY environments.

**Solution 1 - Plain Text**:
```python
console.print(long_url, crop=False, overflow="ignore")
```

**Solution 2 - Rich Containers**:
```python
def get_rendered_width(renderable: RenderableType) -> int:
    temp_console = Console(width=99999)
    measurement = Measurement.get(temp_console, temp_console.options, renderable)
    return int(measurement.maximum)

# Panel: Set Console width
panel = Panel(long_content)
console.width = get_rendered_width(panel)
console.print(panel, crop=False, overflow="ignore")

# Table: Set Table width
table = Table()
table.width = get_rendered_width(table)
console.print(table, crop=False, overflow="ignore")
```

**Executable examples**: See `assets/typer_examples/` for working scripts.

#### Rich Emoji Usage

Always use Rich emoji tokens instead of literal Unicode emojis:

```python
console.print(":white_check_mark: Task completed")
console.print(":cross_mark: Task failed")
console.print(":sparkles: New feature")
```

**Benefits**: Cross-platform compatibility, consistent rendering, markdown-safe alignment.

### Exception Handling

Catch exceptions only when you have a specific recovery action. Let all other errors propagate.

**Reason**: Fail-fast principle surfaces issues early.

**Pattern**:
```python
def get_user(id):
    return db.query(User, id)  # Errors surface naturally

def get_user_with_handling(id):
    try:
        return db.query(User, id)
    except ConnectionError:
        logger.warning("DB unavailable, using cache")
        return cache.get(f"user:{id}")  # Specific recovery
```

See [Exception Handling Guide](../skills/python3-development/references/exception-handling.md) for Typer exception chain prevention.

### Linting Exception Conditions

**Acceptable Exceptions**:
1. Vendored code - Third-party code copied without modification
2. Examples of what-not-to-do - Intentionally incorrect code
3. Code pinned to historic Python version - Python < 3.11 compatibility
4. Code for Python derivatives - CircuitPython, MicroPython

**Unacceptable**: If NONE of the above apply, MUST fix at root cause or document blocker.

**Never suppress without approval**:
- **BLE001** (blind-except) - Replace with specific exception types
- **D103** (missing-docstring) - Add docstrings to public functions
- **TRY300** (try-consider-else) - Restructure try/except/else properly

### Integration

**Complete working example** (external): `~/.claude/agents/python-cli-demo.py`

Demonstrates all patterns:
- PEP 723 metadata with correct shebang
- Typer + Rich integration
- Modern Python 3.11+ (StrEnum, Protocol, TypeVar, Generics)
- Annotated syntax for CLI params
- Async processing
- Comprehensive docstrings

### Summary

**For All Roles**:
- Modern Python 3.11+ standards
- Quality gates: ruff, type checking, pytest (>80% coverage)
- Reference documentation for 50+ modules
- Tool and library registry

**For Orchestrators**:
1. Read orchestration guide before delegating
2. Choose right agent based on task
3. Provide clear context with scope boundaries
4. Chain agents for complex workflows
5. Instruct agents to validate with quality gates
6. Enable uv skill for package management
