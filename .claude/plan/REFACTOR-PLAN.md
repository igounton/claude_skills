# Plugin Refactoring Plan Index

This index tracks all plugin refactoring projects across the repository. Each refactoring follows a three-phase workflow: Assessment → Design → Execution.

---

## Active Refactoring Projects

| Plugin              | Task File                                                                        | Status         | Score Before | Score After | Phase              |
| ------------------- | -------------------------------------------------------------------------------- | -------------- | ------------ | ----------- | ------------------ |
| python3-development | [tasks-refactor-python3-development.md](./tasks-refactor-python3-development.md) | ❌ NOT STARTED | 68/100       | TBD         | Phase 3: Execution |

---

## Completed Refactoring Projects

| Plugin       | Task File | Completion Date | Score Improvement | Notes |
| ------------ | --------- | --------------- | ----------------- | ----- |
| _(none yet)_ |           |                 |                   |       |

---

## Refactoring Workflow Phases

### Phase 1: Assessment

**Agent**: `plugin-assessor`
**Output**: Assessment report with score, issues, and recommendations
**Location**: `.claude/plan/assessment-{plugin-name}.md`

### Phase 2: Design

**Agent**: `claude-context-optimizer` or manual planning
**Output**: Detailed refactoring design specification
**Location**: `.claude/plan/refactor-design-{plugin-name}.md`

### Phase 3: Execution

**Input**: Task breakdown from Phase 2 design
**Output**: Refactored plugin with validation report
**Location**: `.claude/plan/tasks-refactor-{plugin-name}.md`

---

## Task Status Legend

- ❌ **NOT STARTED**: Task has not begun
- 🔄 **IN PROGRESS**: Task is currently being worked on
- ✅ **COMPLETE**: Task finished and verified

---

## Quick Links

- [Workflow Diagrams](../.claude/knowledge/workflow-diagrams/)
- [Plugin Assessment Agent](../../agents/plugin-assessor/)
- [Skill Refactorer Agent](../../agents/skill-refactorer/)
- [Plugin Documentation Writer](../../agents/plugin-docs-writer/)

---

## Notes

- **Score Target**: All refactored plugins should achieve >= 85/100 score
- **Size Target**: Individual skills should be under 500 lines
- **Parallelization**: Phase 3 tasks are designed for maximum parallelization where possible
- **Validation**: All refactoring must pass plugin-assessor validation before marking complete
