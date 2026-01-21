# Refactoring Design Map: python3-development

## Overview

This specification defines the architectural transformation of the python3-development plugin from a monolithic 1318-line skill into focused, maintainable skills following the 500-line target. The refactoring resolves 2 critical issues (oversized skill, broken reference), 5 warnings (orphaned documentation), and applies progressive disclosure patterns to improve context efficiency.

## Source Assessment

- **Plugin**: ./plugins/python3-development
- **Overall Score**: 68/100 (from Phase 1 assessment)
- **Total Refactoring Targets**: 4 skill splits + 2 orphan resolutions + 1 broken link fix + 1 frontmatter fix
- **Current Line Count**: 1318 lines (exceeds 500-line target by 164%)

## Frontmatter Fix (CRITICAL)

### Description Field Quotation Issue

**Source**: `./plugins/python3-development/skills/python3-development/SKILL.md` lines 1-7

**Issue**: The description field uses single quotes around the entire multi-line value, making it a literal string with embedded quotes rather than a properly parsed YAML string.

**Current (Problematic)**:

```yaml
description: 'The model must use this skill when : 1. working within any python project...'
```

**Target (Corrected)**:

```yaml
description: |
  The model must use this skill when:
  1. Working within any Python project
  2. Python CLI applications with Typer and Rich are mentioned
  3. Tasked with Python script writing or editing
  4. Building CI scripts or tools
  5. Creating portable Python scripts with stdlib only
  6. Planning out a Python package design
  7. Running any Python script or test
  8. Writing tests (unit, integration, e2e, validation)
  9. Reviewing Python code against best practices
  10. Pre-commit or linting errors occur in Python files
```

**Implementation**: Edit SKILL.md frontmatter to use YAML multiline syntax with `|` block scalar indicator.

## Skill Splits

### Split 1: python3-core (Foundational Standards)

**Source**: ./plugins/python3-development/skills/python3-development/SKILL.md
**Lines**: Approximately 1-98, 98-270, 941-1088
**Target Size**: ~350-400 lines

**Domain**: Core Python development standards, exception handling, linting, quality gates

**Content to Extract**:

| Section                      | Original Lines | Description                                   |
| ---------------------------- | -------------- | --------------------------------------------- |
| Role Identification          | 1-35           | Mandatory role identification protocol        |
| Skill Architecture           | 38-97          | Bundled resources, external dependencies      |
| Script Dependency Trade-offs | 127-156        | Typer+Rich vs stdlib-only decision            |
| Rich Panel/Table Handling    | 157-247        | Width handling, emoji usage                   |
| Python Exception Handling    | 249-269        | Fail-fast patterns                            |
| Linting Discovery Protocol   | 941-1046       | Format-first workflow, type checker discovery |
| Quality Gates                | 1047-1125      | Mandatory validation sequence                 |
| Linting Exceptions           | 1088-1125      | Acceptable and unacceptable exceptions        |

**Dependencies**:

- References: `./references/exception-handling.md`
- References: `./references/tool-library-registry.md`
- Assets: `./assets/typer_examples/index.md`

**Frontmatter Triggers**:

```yaml
description: |
  The model must use this skill when:
  - Writing or editing Python code in any context
  - Running Python scripts or tests
  - Pre-commit or linting errors occur in Python files
  - Building CI/CD pipelines for Python projects
  - Determining script dependency strategy (Typer+Rich vs stdlib-only)
  - Handling Rich console output formatting issues
```

---

### Split 2: python3-typing (Type Hints and Safety)

**Source**: ./plugins/python3-development/skills/python3-development/SKILL.md
**Lines**: 271-711
**Target Size**: ~440 lines

**Domain**: Mypy configuration, generics, protocols, TypedDict, type narrowing, attrs/dataclasses/pydantic selection

**Content to Extract**:

| Section                          | Original Lines | Description                                |
| -------------------------------- | -------------- | ------------------------------------------ |
| Type Safety with Mypy            | 273-278        | Requirements overview                      |
| When to Use Generics             | 279-363        | TypeVar, Generic, bounds, method chaining  |
| When to Use Protocols            | 364-436        | Structural subtyping, runtime checks       |
| TypedDict for Dictionary Typing  | 437-505        | Required/optional fields, mixed patterns   |
| Type Narrowing                   | 506-568        | isinstance, None checks, TypeGuard, TypeIs |
| attrs vs dataclasses vs pydantic | 569-640        | Decision matrix, patterns                  |
| Additional Mypy Features         | 641-677        | Generic dataclasses, Self type             |
| Mypy Configuration               | 678-711        | Strict mode, per-module overrides          |

**Dependencies**:

- References: `./references/mypy-docs/generics.rst`
- References: `./references/mypy-docs/protocols.rst`
- References: `./references/mypy-docs/typed_dict.rst`
- References: `./references/mypy-docs/type_narrowing.rst`
- References: `./references/mypy-docs/additional_features.rst`
- References: `./references/tool-library-registry.md` (Mypy Configuration section)

**Frontmatter Triggers**:

```yaml
description: |
  The model must use this skill when:
  - Type hints are being added, reviewed, or debugged
  - Mypy or pyright errors need resolution
  - Choosing between attrs, dataclasses, or pydantic
  - Implementing generic types, protocols, or TypedDict
  - Type narrowing patterns are needed
  - Configuring mypy strict mode or per-module overrides
```

---

### Split 3: python3-orchestration (Agent Coordination)

**Source**: ./plugins/python3-development/skills/python3-development/SKILL.md
**Lines**: 712-846, 924-940, 1227-1318
**Target Size**: ~300 lines

**Domain**: Orchestrator-only patterns, agent delegation, workflow coordination

**Content to Extract**:

| Section                   | Original Lines | Description                                                |
| ------------------------- | -------------- | ---------------------------------------------------------- |
| Agent Orchestration       | 713-846        | Pre-delegation protocol, delegation patterns               |
| Core Workflows            | 924-940        | TDD, feature addition, code review, refactoring, debugging |
| Common Patterns to Follow | 1227-1246      | Orchestrator delegation table                              |
| Summary (Orchestrator)    | 1305-1318      | Coordination + Delegation + Validation                     |

**Dependencies**:

- References: `./references/python-development-orchestration.md` (CRITICAL - primary reference)

**Frontmatter Triggers**:

```yaml
description: |
  The model must use this skill when ROLE_TYPE is orchestrator and:
  - Delegating Python development tasks to specialized agents
  - Planning multi-agent workflows (design, implement, test, review)
  - Coordinating TDD, feature addition, or refactoring workflows
  - Validating agent outputs against quality gates
```

**Special Consideration**: This skill should have `ROLE_TYPE: orchestrator` in frontmatter to restrict loading to orchestrator context only.

---

### Split 4: python3-packaging (Project Structure and Distribution)

**Source**: ./plugins/python3-development/skills/python3-development/SKILL.md
**Lines**: 847-923, 1088-1226
**Target Size**: ~300 lines

**Domain**: Project layout, pyproject.toml, PEP 723, asset templates, commands

**Content to Extract**:

| Section                    | Original Lines | Description                            |
| -------------------------- | -------------- | -------------------------------------- |
| Command Usage              | 847-923        | /modernpython, /shebangpython commands |
| Standard Project Structure | 1130-1165      | packages/ layout, hatchling config     |
| Integration                | 1166-1190      | External reference example             |
| Using Asset Templates      | 1186-1226      | version.py, hatch_build.py, configs    |

**Dependencies**:

- References: `./references/PEP723.md`
- References: `./references/user-project-conventions.md`
- Assets: `./assets/version.py`, `./assets/hatch_build.py`, `./assets/.pre-commit-config.yaml`

**Frontmatter Triggers**:

```yaml
description: |
  The model must use this skill when:
  - Creating new Python projects or packages
  - Configuring pyproject.toml or project metadata
  - Using PEP 723 inline script metadata
  - Setting up project directory structure
  - Copying asset templates (version.py, pre-commit configs)
  - Using /modernpython or /shebangpython commands
```

---

## Shared References Strategy

### Files to Duplicate (Small, Context-Critical)

None - all references should use relative paths from skill directory.

### Files Requiring Path Updates

After split, each new skill directory needs correct relative paths:

- From `python3-core/SKILL.md` to `python3-core/references/exception-handling.md`
- From `python3-typing/SKILL.md` to `python3-typing/references/mypy-docs/generics.rst`

### Reference File Distribution

| Reference File                      | Used By Skills                        |
| ----------------------------------- | ------------------------------------- |
| exception-handling.md               | python3-core                          |
| tool-library-registry.md            | python3-core, python3-typing          |
| mypy-docs/\*.rst                    | python3-typing                        |
| python-development-orchestration.md | python3-orchestration                 |
| PEP723.md                           | python3-packaging                     |
| user-project-conventions.md         | python3-packaging                     |
| modern-modules.md                   | python3-core (as secondary reference) |
| modern-modules/\*.md                | python3-core (as secondary reference) |
| api_reference.md                    | python3-packaging                     |

### Backward Compatibility

The original skill name `python3-development` is referenced by other plugins and potentially external configurations. Options:

**Option A (Recommended)**: Keep `python3-development` as a "meta-skill" that loads all four sub-skills

- Maintains backward compatibility
- Users can still activate `python3-development` to get full coverage
- Individual skills loadable for focused contexts

**Option B**: Rename and update all references

- Breaking change requires coordination
- Cleaner long-term structure

**Recommendation**: Implement Option A initially, deprecate in future version.

---

## Documentation Improvements

### Broken Link Fix

**File**: `./plugins/python3-development/skills/python3-development/SKILL.md`
**Line**: 57
**Current**: `[Commands README](./commands/README.md)`
**Issue**: File does not exist

**Resolution Options**:

1. Create `./commands/README.md` documenting command templates
2. Remove the broken reference
3. Link to the actual commands directory: `./commands/`

**Recommendation**: Option 2 - Remove the reference since the sentence describes command templates which are documented inline.

**Target Change**:

```markdown
# Before (line 57)
- See [Commands README](./commands/README.md) for details

# After
- Templates provide patterns for creating slash commands
```

---

## Orphan Resolution

### Orphan 1: planning/reference-document-architecture.md

**Classification**: Historical (never implemented proposal)
**Path**: `./skills/python3-development/planning/reference-document-architecture.md`
**Evidence**: Lines 6-10 contain explicit metadata:

```yaml
status: "historical-proposal"
implementation_status: "not-implemented"
archived_date: "2025-11-02"
note: "This document represents an architectural proposal that was never implemented..."
```

**Resolution**: DELETE

- Document explicitly marked as not-implemented
- Actual skill uses different structure (references/ and commands/) than proposed (docs/scenarios/ and docs/standards/)
- Keeping creates confusion about actual architecture
- No reverse references point to this file

**Implementation**:

```bash
rm ./plugins/python3-development/skills/python3-development/planning/reference-document-architecture.md
rmdir ./plugins/python3-development/skills/python3-development/planning/  # if empty
```

---

### Orphan 2: references/modern-modules/datasette.md

**Classification**: New Content (exists but not linked)
**Path**: `./skills/python3-development/references/modern-modules/datasette.md`

**Evidence**: File exists in `modern-modules/` directory but is NOT referenced from `modern-modules.md` (grep found no "See Also" link for datasette).

**Resolution**: INTEGRATE

- Add entry in `modern-modules.md` under "Data Processing & Analysis" or "Database & ORM"
- Add "See Also" link pattern consistent with other modules

**Target Addition** (in modern-modules.md, after DuckDB section around line 443):

```markdown
---

### Datasette

**PyPI:** `datasette` | **Status:** Active | **Python:** 3.11+

Instant JSON API and web interface for SQLite databases. Enables data exploration and publishing.

**Key Features:**

- Automatic API generation from SQLite
- Web interface for data exploration
- Plugin ecosystem
- Faceted browse and search
- JSON, CSV export

**When to Use:**

- Publishing data as API
- Quick data exploration
- Building read-only data applications
- Sharing SQLite databases

**See Also:** [Datasette Documentation](./modern-modules/datasette.md)
```

---

## Dependency Map

```text
                    +------------------+
                    |  plugin.json     |
                    |  (frontmatter    |
                    |   fix required)  |
                    +--------+---------+
                             |
            +----------------+----------------+
            |                |                |
            v                v                v
    +--------------+  +--------------+  +--------------+
    |python3-core  |  |python3-typing|  |python3-      |
    |              |  |              |  |orchestration |
    +--------------+  +--------------+  +--------------+
            |                |                |
            |                |                |
            v                v                v
    +--------------+  +--------------+  +--------------+
    |exception-    |  |mypy-docs/    |  |python-dev-   |
    |handling.md   |  |*.rst (5)     |  |orchestration |
    |tool-library- |  |tool-library- |  |.md           |
    |registry.md   |  |registry.md   |  +--------------+
    |modern-       |  +--------------+
    |modules.md    |                          |
    +--------------+                          v
            |                         +--------------+
            |                         |python3-      |
            v                         |packaging     |
    +--------------+                  +--------------+
    |typer_examples|                         |
    |/index.md     |                         v
    +--------------+                  +--------------+
                                      |PEP723.md     |
                                      |user-project- |
                                      |conventions.md|
                                      |assets/       |
                                      +--------------+
```

### Task Dependencies

| Task ID | Task                                          | Depends On     | Blocks         |
| ------- | --------------------------------------------- | -------------- | -------------- |
| T1      | Fix SKILL.md frontmatter quotes               | None           | T2, T3, T4, T5 |
| T2      | Create python3-core skill                     | T1             | T6             |
| T3      | Create python3-typing skill                   | T1             | T6             |
| T4      | Create python3-orchestration skill            | T1             | T6             |
| T5      | Create python3-packaging skill                | T1             | T6             |
| T6      | Update python3-development as meta-skill      | T2, T3, T4, T5 | T7             |
| T7      | Fix broken ./commands/README.md link          | T6             | T8             |
| T8      | Delete planning/ directory                    | T7             | T9             |
| T9      | Integrate datasette.md into modern-modules.md | T8             | T10            |
| T10     | Validate all cross-references                 | T9             | None           |

---

## Parallelization Opportunities

### Group A: Skill Creation (Can Run Simultaneously After T1)

No shared file conflicts - each skill writes to separate directory:

- **T2**: Create `skills/python3-core/SKILL.md`
- **T3**: Create `skills/python3-typing/SKILL.md`
- **T4**: Create `skills/python3-orchestration/SKILL.md`
- **T5**: Create `skills/python3-packaging/SKILL.md`

**Parallelization Strategy**: Assign to 4 parallel sub-agents after frontmatter fix completes.

### Group B: Documentation Fixes (Sequential)

Must run sequentially - modifies same file or has ordering dependencies:

- **T7**: Fix broken link in SKILL.md
- **T8**: Delete planning/ directory
- **T9**: Add datasette to modern-modules.md

### Group C: Validation (Final)

- **T10**: Must run last to verify all changes

---

## Implementation Notes

### Skill Directory Structure Post-Refactor

```text
plugins/python3-development/
├── plugin.json                    # Updated with sub-skills list
├── skills/
│   ├── python3-development/       # Meta-skill (backward compat)
│   │   ├── SKILL.md              # Loads all sub-skills
│   │   └── references/           # Shared references (unchanged)
│   ├── python3-core/
│   │   ├── SKILL.md              # ~350 lines
│   │   └── references -> ../python3-development/references
│   ├── python3-typing/
│   │   ├── SKILL.md              # ~440 lines
│   │   └── references -> ../python3-development/references
│   ├── python3-orchestration/
│   │   ├── SKILL.md              # ~300 lines
│   │   └── references -> ../python3-development/references
│   └── python3-packaging/
│       ├── SKILL.md              # ~300 lines
│       └── references -> ../python3-development/references
└── commands/                      # Unchanged
```

### Meta-Skill Pattern (python3-development/SKILL.md)

```yaml
---
name: python3-development
description: |
  Meta-skill that loads comprehensive Python development guidance.
  Automatically activates: python3-core, python3-typing, python3-orchestration, python3-packaging.
version: "2.0.0"
includes:
  - python3-core
  - python3-typing
  - python3-orchestration
  - python3-packaging
---

# Python Development Meta-Skill

This skill provides comprehensive Python development guidance by loading focused sub-skills.

## Sub-Skills

- **python3-core**: Foundational standards, linting, quality gates
- **python3-typing**: Type hints, mypy, protocols, generics
- **python3-orchestration**: Agent coordination, workflow patterns
- **python3-packaging**: Project structure, PEP 723, templates

## Activation

Individual skills can be activated for focused contexts:
- `@python3-core` - Core development standards only
- `@python3-typing` - Type safety guidance only
- `@python3-orchestration` - Agent coordination only
- `@python3-packaging` - Project setup and templates only

Or activate `@python3-development` for full coverage.
```

---

## Estimated Impact

| Metric              | Before | After      | Change |
| ------------------- | ------ | ---------- | ------ |
| Main SKILL.md lines | 1318   | ~50 (meta) | -96%   |
| Largest skill       | 1318   | ~440       | -67%   |
| Orphaned files      | 20     | 0          | -100%  |
| Broken links        | 1      | 0          | -100%  |
| Estimated score     | 68/100 | 90+/100    | +32%   |

---

## Verification Checklist

Post-refactoring validation:

- [ ] All new SKILL.md files under 500 lines
- [ ] All frontmatter YAML parses correctly
- [ ] All relative reference paths resolve
- [ ] Meta-skill loads all sub-skills
- [ ] Individual skills load independently
- [ ] No orphaned files in references/
- [ ] No broken markdown links
- [ ] Planning directory removed
- [ ] Datasette integrated into modern-modules.md
- [ ] Pre-commit linting passes on all files
