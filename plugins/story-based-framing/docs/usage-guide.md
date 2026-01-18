# Story-Based Framing Usage Guide

Complete guide to using story-based framing for pattern detection across any domain.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Pattern Descriptions](#creating-pattern-descriptions)
3. [Using with LLM Agents](#using-with-llm-agents)
4. [Integration Patterns](#integration-patterns)
5. [Best Practices](#best-practices)
6. [Advanced Techniques](#advanced-techniques)

---

## Getting Started

### Understanding the Four Acts

Every pattern description follows a narrative structure with clear causation:

```
Act 1: What it promises/appears to be
   ↓ (declares to implement X)
Act 2: Where it actually breaks
   ↓ (violation causes)
Act 3: Observable symptoms
   ↓ (symptoms reveal)
Act 4: Root cause
```

### Why This Works

**Cognitive Alignment**: The structure mirrors how experts naturally investigate problems:

1. **First glance**: "This looks like X" → Act 1
2. **Deeper inspection**: "Wait, this violates Y" → Act 2
3. **Validation**: "And I can see symptoms Z" → Act 3
4. **Understanding**: "This happened because..." → Act 4

**Search Efficiency**: Acts 1-2 contain the most distinctive criteria, eliminating 90%+ of false positives immediately.

---

## Creating Pattern Descriptions

### Step 1: Identify the Pattern

Before writing, clearly identify:

- **Pattern name**: Memorable, evocative (e.g., "The Fake Generic", "The Phantom Approval")
- **Domain**: Code, business, security, UX, data, medical, operations, etc.
- **Core violation**: What promise is being broken?
- **Distinctive traits**: What uniquely identifies this pattern vs. similar ones?

### Step 2: Write Act 1 - The Promise

**Purpose**: Establish what appears correct at first glance.

**Good Act 1 Examples**:

```markdown
# Code domain
Act 1: A generic class `Container(Generic[T])` promises to preserve type T throughout its operations.

# Business domain
Act 1: The approval workflow documentation states: "All purchase requests over $5,000 require approval from department head, finance manager, and VP before processing."

# Security domain
Act 1: IAM policy documentation specifies: "Service accounts follow principle of least privilege."

# UX domain
Act 1: Cancel subscription button promises user control: "You can cancel anytime, no questions asked."
```

**Checklist**:
- [ ] States what is claimed/promised/documented
- [ ] Cites specific declarations (class signature, policy doc, UI text)
- [ ] Describes the "correct-looking" initial state
- [ ] Uses the most distinctive structural criterion

### Step 3: Write Act 2 - The Betrayal

**Purpose**: Reveal where the implementation violates the promise.

**Good Act 2 Examples**:

```markdown
# Code domain
Act 2: But the constructor accepts `raw_value: ConfigValue` (a union type) instead of `raw_value: T`, storing a union type rather than the promised generic parameter.

# Business domain
Act 2: But requests tagged as "urgent" or "vendor renewal" bypass all approval gates and go directly to processing.

# Security domain
Act 2: But the `data-pipeline-service` account has AdministratorAccess policy attached, granting full access to all AWS resources.

# UX domain
Act 2: But clicking "Cancel Subscription" shows modal with confirm-shaming buttons and requires 5 steps to complete.
```

**Checklist**:
- [ ] Specifies the exact violation point
- [ ] Uses "But" or similar contrast word
- [ ] Cites specific code/config/UI element
- [ ] Contains the second most distinctive criterion

### Step 4: Write Act 3 - The Consequences

**Purpose**: Describe observable symptoms that result from the violation.

**Good Act 3 Examples**:

```markdown
# Code domain
Act 3: Methods contain `isinstance()` checks and `# type: ignore` comments to work around the type mismatch.

# Business domain
Act 3: Audit logs show 40% of purchases over $5,000 lack pre-approval; approvers receive "FYI" emails after purchase completion.

# Security domain
Act 3: Security scanning tool flags 127 excessive permissions; penetration test successfully escalates privileges.

# UX domain
Act 3: 40% of users who initiate cancellation don't complete it; support tickets mention "deceptive cancellation process."
```

**Checklist**:
- [ ] Lists concrete, observable symptoms
- [ ] Provides verification criteria
- [ ] Includes metrics/counts where available
- [ ] Shows workarounds or compensating mechanisms

### Step 5: Write Act 4 - The Source

**Purpose**: Explain why the pattern exists (root cause).

**Good Act 4 Examples**:

```markdown
# Code domain
Act 4: Values originate from heterogeneous storage (`dict[str, TypeA | TypeB]`) where specific type information is lost at the storage boundary.

# Business domain
Act 4: The auto-approve feature was added during pandemic supply chain crisis (March 2020) and the "temporary" exception was never removed.

# Security domain
Act 4: Account was created during initial POC phase when team "just needed something working quickly" and production inherited POC configuration.

# UX domain
Act 4: Product team was incentivized on monthly recurring revenue (MRR) and retention rate, leading to design that reduces cancellation completion.
```

**Checklist**:
- [ ] Explains architectural root cause
- [ ] Traces origin (historical decision, constraint, incentive)
- [ ] Distinguishes isolated vs. systemic issue
- [ ] Informs fix strategy

### Step 6: Write The Fix

**Purpose**: Provide resolution approach.

**Good Fix Examples**:

```markdown
# Code domain
The Fix: Use TypeGuard to narrow the union BEFORE instantiation, and change constructor to accept the type parameter directly.

# Business domain
The Fix: Remove auto-approve bypass for amounts over threshold; create expedited approval workflow (4-hour SLA) for genuine emergencies.

# Security domain
The Fix: Audit CloudTrail logs to identify actually-used permissions; create new policy with only required permissions; rotate credentials.

# UX domain
The Fix: Single-click cancellation from account settings; neutral language; optional feedback form AFTER cancellation completes.
```

**Checklist**:
- [ ] Addresses the Act 2 violation directly
- [ ] Tackles Act 4 root cause when possible
- [ ] Provides specific action steps
- [ ] Brief (2-4 sentences)

---

## Using with LLM Agents

### For Automated Detection

**Prompt Template**:

```markdown
Search for instances of "{Pattern Name}" in {domain/codebase}:

**The Promise**: {Act 1}
**The Betrayal**: {Act 2}
**The Consequences**: {Act 3}
**The Source**: {Act 4}

Report each match with:
- Location (file, line, identifier)
- Evidence for Act 1 (promise declaration)
- Evidence for Act 2 (violation point)
- Evidence for Act 3 (symptoms observed)
- Evidence for Act 4 (root cause indicators)
```

**Example Invocation**:

```python
Task(
    agent="Explore",
    prompt="""
    Search for instances of "The Fake Generic" in this codebase:

    **The Promise**: Class declares Generic[T] to preserve type information
    **The Betrayal**: Constructor accepts union type instead of T
    **The Consequences**: Methods use isinstance() checks and type suppressions
    **The Source**: Values from heterogeneous storage lose type info

    Report all matches with file locations and code snippets.
    """
)
```

### For Code Review

**Review Comment Template**:

```markdown
⚠️ **Pattern Detected: "{Pattern Name}"**

**The Promise**: {What it claims to do}

**The Betrayal**: {Where it breaks}

**The Consequences**: {Observed symptoms with line numbers}

**The Source**: {Root cause}

**Suggested Fix**: {Resolution approach}
```

### For Documentation

Use the full narrative template from [../skills/story-based-framing/assets/narrative_template.md](../skills/story-based-framing/assets/narrative_template.md).

---

## Integration Patterns

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run story-based pattern detector
python scripts/detect_patterns.py --patterns ./patterns/*.md

exit_code=$?

if [ $exit_code -eq 1 ]; then
    echo "❌ Patterns detected. Review findings in pattern_report.md"
    exit 1
fi

exit 0
```

### CI/CD Pipeline

```yaml
# .github/workflows/pattern-detection.yml
name: Pattern Detection

on: [pull_request]

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run story-based pattern detector
        run: |
          python scripts/detect_patterns.py \
            --patterns ./patterns/*.md \
            --format github-comment

      - name: Post findings as PR comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('pattern_report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

### IDE Integration

```python
# VS Code extension or language server
class StoryBasedPatternLinter:
    def lint_file(self, file_path: str) -> list[Diagnostic]:
        """Detect patterns using story-based descriptions."""
        diagnostics = []

        for pattern in self.load_patterns():
            matches = self.detect_pattern(file_path, pattern)

            for match in matches:
                diagnostics.append(Diagnostic(
                    range=match.range,
                    severity=DiagnosticSeverity.Warning,
                    message=self.format_narrative(pattern, match),
                    source="story-based-framing"
                ))

        return diagnostics

    def format_narrative(self, pattern: Pattern, match: Match) -> str:
        return f"""
Pattern: {pattern.name}

The Promise: {pattern.act1}
The Betrayal: {pattern.act2}
The Consequences: {pattern.act3}
The Source: {pattern.act4}

Fix: {pattern.fix}
"""
```

---

## Best Practices

### 1. Frontload Distinctive Criteria

**Poor** (generic symptoms first):
```
Act 1: System has configuration
Act 2: Configuration changes sometimes
Act 3: Errors occur
```

**Good** (unique structure first):
```
Act 1: System promises immutable configuration
Act 2: But configuration is mutated by background thread
Act 3: Race conditions cause non-deterministic errors
```

### 2. Use Causal Language

**Weak transitions**:
- "Additionally..." (implies independent facts)
- "Also..." (suggests a list)
- "Furthermore..." (just adds more)

**Strong transitions**:
- "But..." (shows violation)
- "Because of this..." (shows causation)
- "This forces..." (shows consequence)
- "Which originates from..." (traces root cause)

### 3. Provide Concrete Examples

**Abstract** (hard to match):
```
Act 2: The function violates the contract
```

**Concrete** (easy to match):
```
Act 2: The function accepts `raw_value: Union[A, B]` instead of the promised `raw_value: T`
```

### 4. Vary Example Details

When providing multiple examples, vary names/scenarios to prevent literal matching:

```markdown
# Example 1
class TemplateExpander(Generic[T]):
    def __init__(self, raw_value: ConfigValue): ...

# Example 2
class DataContainer(Generic[K]):
    def __init__(self, contents: StorageType): ...

# Example 3
class ResultWrapper(Generic[R]):
    def __init__(self, data: ResponseUnion): ...
```

This ensures agents match on structure, not specific identifiers.

### 5. Measure Detection Efficiency

Track metrics to validate story-based approach:

```python
# Before story-based framing
baseline_metrics = {
    "average_steps": 10,
    "false_positives": 45,  # per 100 detections
    "fix_time_hours": 2.5
}

# After story-based framing
improved_metrics = {
    "average_steps": 3,
    "false_positives": 12,
    "fix_time_hours": 0.8
}

improvement = {
    "efficiency": (baseline_metrics["average_steps"] / improved_metrics["average_steps"] - 1) * 100,  # 70%
    "accuracy": (1 - improved_metrics["false_positives"] / baseline_metrics["false_positives"]) * 100,  # 73%
    "speed": (1 - improved_metrics["fix_time_hours"] / baseline_metrics["fix_time_hours"]) * 100  # 68%
}
```

---

## Advanced Techniques

### Multi-Pattern Stories

For related patterns, create a pattern family:

```markdown
# Pattern Family: "Type Safety Violations"

## Pattern 1: "The Fake Generic"
- Promise: Preserves type T
- Betrayal: Stores union type

## Pattern 2: "The Type Eraser"
- Promise: Returns typed result
- Betrayal: Uses cast() without validation

## Pattern 3: "The Any Spreader"
- Promise: Typed pipeline
- Betrayal: Introduces Any in middle
```

### Nested Narratives

For complex patterns with sub-patterns:

```markdown
# Main Pattern: "The Broken Promise"

## Sub-Pattern A: Configuration Error Variant
- Act 2a: Promise breaks due to missing config value

## Sub-Pattern B: Integration Failure Variant
- Act 2b: Promise breaks due to API incompatibility

## Sub-Pattern C: Resource Constraint Variant
- Act 2c: Promise breaks due to memory limitation
```

### Comparative Narratives

For patterns with subtle differences:

```markdown
# Comparison: "The False Promise" vs "The Partial Promise"

## The False Promise
- Act 2: Claims X but delivers Y (complete violation)

## The Partial Promise
- Act 2: Claims X and delivers some X but not all (partial delivery)

**Key Difference**: Complete vs. partial violation at Act 2 betrayal point.
```

### Pattern Evolution Tracking

Monitor how patterns spread over time:

```markdown
# Pattern: "The Overprivileged Service Account"

## Timeline
- Commit 1 (2023-01): 1 instance (Act 4: "POC testing")
- Commit 50 (2023-06): 5 instances (Act 4: "Copy-pasted from original")
- Commit 100 (2024-01): 15 instances (Act 4: "Became standard pattern")

## Decision
→ Time to address systemically (Act 4 indicates architectural issue)
```

### Cross-Domain Adaptation

Adapt language for target audience:

```markdown
# Technical Audience (Code)
Act 2: Constructor accepts `Union[A, B]` instead of TypeVar `T`

# Business Audience
Act 2: Implementation bypasses the approval requirement

# Executive Audience
Act 2: System allows unauthorized purchases over $5K

# All audiences, same pattern - just different framing
```

---

## Troubleshooting

### Issue: Too Many False Positives

**Cause**: Acts 1-2 not distinctive enough

**Solution**: Strengthen Acts 1-2 with more unique criteria:

```markdown
# Weak Act 1 (not distinctive)
Act 1: Function returns a value

# Strong Act 1 (distinctive)
Act 1: Function declares return type `AppConfig` with strict schema
```

### Issue: Pattern Not Found

**Cause**: Acts 1-2 too specific, missing valid instances

**Solution**: Generalize Acts 1-2 while keeping Acts 3-4 for verification:

```markdown
# Too specific
Act 1: Class named exactly "TemplateExpander"

# Properly general
Act 1: Class inherits from Generic[T]
```

### Issue: Agent Confused by Symptoms

**Cause**: Started with Act 3 (symptoms) instead of Act 1 (structure)

**Solution**: Verify search order: Act 1 first, Act 2 second, Acts 3-4 for validation:

```python
# Wrong order
if has_isinstance_checks(code):  # Act 3 first
    if is_generic_class(code):   # Act 1 last
        # Too many false positives

# Correct order
if is_generic_class(code):        # Act 1 first - most distinctive
    if has_union_constructor(code):  # Act 2 second - narrows matches
        if has_isinstance_checks(code):  # Act 3 - verifies
            # Accurate detection
```

---

## Additional Resources

- [Narrative Template](../skills/story-based-framing/assets/narrative_template.md) - Blank template
- [Code Analysis Examples](../skills/story-based-framing/resources/code-analysis/example_patterns.md) - Fully-worked examples
- [Cross-Domain Examples](../skills/story-based-framing/references/cross_domain_examples.md) - Business, security, UX, data, medical, operations
- [Experiment Results](../skills/story-based-framing/resources/code-analysis/experiment_results.md) - Validation data
- [Practical Guide](../skills/story-based-framing/resources/code-analysis/practical_guide.md) - Integration with linting, CI/CD

---

**Last Updated**: 2026-01-18
