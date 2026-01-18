# Quick Reference Guide

Fast lookup for common optimization patterns and transformations.

## Transformation Patterns

### Prohibitions → Positive Instructions

```markdown
# BEFORE
❌ NEVER use cat
❌ DON'T use grep
❌ FORBIDDEN to use find

# AFTER
| Operation | Tool | Reason |
|-----------|------|--------|
| Read files | Read() | Handles encoding |
| Search | Grep() | Structured results |
| Find files | Glob() | Respects gitignore |
```

### Vague → Specific

```markdown
# BEFORE
Format code properly

# AFTER
Use 2-space indentation for all code
**Reason**: Consistent formatting improves readability
```

### Sequential → Parallel

```markdown
# BEFORE
First search, then read, then analyze

# AFTER
Execute simultaneously:
- Search: Grep(pattern)
- Read: Read(file)
- Check: Glob(tests)
```

### Abstract → Concrete

```markdown
# BEFORE
Write good tests

# AFTER
For each feature:
1. Happy path test
2. Edge cases (empty, max, boundary)
3. Error conditions (invalid input)

<example>
def test_validate():
    assert validate("valid") is True
    assert validate("") is False
    with pytest.raises(TypeError):
        validate(None)
</example>
```

## Compression Techniques

| Verbose | Compressed |
|---------|------------|
| "You might want to" | Direct imperative |
| "Consider doing X when Y" | "IF Y THEN X" |
| "It's important to remember" | "CONSTRAINT:" |
| "For example, when X happens" | "IF X THEN [action]" |
| "Please make sure to" | Direct imperative |

## Structural Templates

### Simple Protocol (<50 lines)

```text
## [Protocol Name]

TRIGGER: [When this applies]

PROCEDURE:
1. [Action]
2. [Action]
3. [Action]

CONSTRAINTS:
- [Required behavior]
- [Required behavior]

OUTPUT: [Expected deliverable]
```

### Tool Selection Table

```markdown
| Operation | Tool | Reason |
|-----------|------|--------|
| [What user wants] | [Tool call syntax] | [Why this tool] |
```

### Conditional Logic

```text
IF [condition] THEN [action]
ELSE IF [condition] THEN [action]
ELSE [default action]
```

## Claude 4.5-Specific Patterns

### Direct Action Language

| Indirect | Direct |
|----------|--------|
| "Can you suggest changes?" | "Make these changes" |
| "It might be good to..." | "Implement this feature" |
| "Consider adding..." | "Add X to Y" |

### Parallel Execution

```markdown
Execute simultaneously:
- Operation 1
- Operation 2
- Operation 3

Wait for all to complete, then proceed
```

### Concise Communication

```markdown
## Response Style
- Lead with findings, not process
- State facts directly
- Skip summaries after tool operations
- Provide code changes, not descriptions
```

## Skill Description Formula

```yaml
description: [ACTION 1], [ACTION 2], [ACTION 3]. Use when [SITUATION 1], [SITUATION 2], or when user mentions [KEYWORDS].
```

**Example**:

```yaml
description: Review code for best practices, security issues, and potential bugs. Use when reviewing PRs, analyzing code quality, checking implementations before merge, or when user mentions code review.
```

## Verification Checklist

Quick checklist for optimized documentation:

- [ ] Prohibition markers minimal or absent
- [ ] Each instruction states what TO do
- [ ] Motivations provided for non-obvious rules
- [ ] Complex behaviors have 2-3 examples
- [ ] Instructions grouped under headings
- [ ] Critical behaviors appear early
- [ ] Specific over vague
- [ ] Direct action language
- [ ] Technical terms verified

## Length Targets

| Document Type | Target |
|---------------|--------|
| Single protocol | <50 lines |
| Agent instructions | <100 lines |
| Complex workflow | <200 lines |
| Full CLAUDE.md | <500 lines |

## Common Anti-Patterns

### Anti-Pattern 1: Prohibition List

```markdown
# BAD
❌ NEVER X
❌ DON'T Y
❌ FORBIDDEN Z

# GOOD
Use A for X (reason)
Use B for Y (reason)
Use C for Z (reason)
```

### Anti-Pattern 2: Vague Quality

```markdown
# BAD
Write clean code

# GOOD
<example>
def process_user(data):
    """Process user data with validation.

    Args:
        data: Dict with 'name' and 'age'
    Returns:
        User object
    Raises:
        ValueError: If data invalid
    """
    if not data.get("name"):
        raise ValueError("Name required")
    return User(**data)
</example>
```

### Anti-Pattern 3: Missing Motivation

```markdown
# BAD
Always use conventional commits

# GOOD
Use conventional commits format: type(scope): description
**Reason**: Enables automated changelog and semantic versioning
```

### Anti-Pattern 4: Buried Priorities

```markdown
# BAD
[20 lines of background]
[Key instruction buried at line 50]

# GOOD
## CRITICAL: Key Behavior
[Important instruction first]

## Background
[Context later]
```

## Quick Wins

Five fastest improvements:

1. **Replace prohibition lists with tool tables** (5 minutes)
2. **Add "Reason:" to each major instruction** (10 minutes)
3. **Front-load critical behaviors** (reorder, 5 minutes)
4. **Add 2-3 concrete examples** (15 minutes)
5. **Use compression templates** (10 minutes)

Total: 45 minutes for significant improvement

## Resources

- [Main README](../README.md) - Complete documentation
- [Usage Examples](./examples.md) - Detailed real-world examples
- [Anthropic Prompt Engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering) - Official docs

## Activation

```
@prompt-optimization-claude-45
[Your request]
```

Or simply mention "optimize prompt" or "improve CLAUDE.md" - Claude will auto-activate the skill.
