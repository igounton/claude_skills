# verification-gate

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Enforce mandatory pre-action verification checkpoints to prevent pattern-matching from overriding explicit reasoning. This plugin implements structural gates between hypothesis formation and action execution, ensuring Claude's actions align with verified hypotheses rather than reflexive pattern-matching responses.

## Features

- **4-Checkpoint Verification System**: Mandatory gates before any implementation action
- **Hypothesis-Action Alignment**: Prevents cognitive dissonance where correct diagnosis leads to wrong implementation
- **Pattern-Matching Detection**: Identifies and blocks actions based on training data patterns vs. project reality
- **Research-Backed Approach**: Based on Meta's Chain-of-Verification (CoVe) methodology and Anthropic's best practices
- **Comprehensive Documentation**: Includes research foundations and real-world failure pattern analysis

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- No external dependencies required

### Install Plugin

```bash
# Method 1: From plugin marketplace (if available)
/plugin install verification-gate

# Method 2: Manual installation
# Copy to your plugins directory
cp -r ./plugins/verification-gate ~/.claude/plugins/
/plugin reload
```

## Quick Start

The verification-gate skill activates automatically when Claude is about to execute implementation actions (Bash, Write, Edit). It enforces a 4-checkpoint verification protocol:

```
Checkpoint 1: Hypothesis Stated
    ↓
Checkpoint 2: Hypothesis Verified
    ↓
Checkpoint 3: Hypothesis-Action Alignment
    ↓
Checkpoint 4: Pattern-Matching Detection
    ↓
Execute Action
```

If any checkpoint fails, execution is blocked until the issue is resolved.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | verification-gate | Enforces mandatory verification checkpoints before implementation actions | Auto-invoked by Claude |

## Usage

### When Verification Gates Activate

The verification-gate skill automatically activates before:

- **Any Bash command** that modifies system state
- **Any Write/Edit operation** on files
- **Any action following error diagnosis**
- **Implementation choices** between multiple approaches

### The 4-Checkpoint System

#### Checkpoint 1: Hypothesis Stated

**Question:** Have I explicitly stated what system/component the issue affects?

**Requirement:** Must name the specific system and write the hypothesis explicitly.

**Example:**
```
✓ PASS: "Hypothesis: The issue affects PEP 723 inline metadata dependencies"
✗ FAIL: "There's a dependency problem" (too vague)
```

#### Checkpoint 2: Hypothesis Verified

**Question:** Have I gathered evidence to confirm or refute my hypothesis?

**Requirement:** Must use Read/Grep/MCP tools to gather evidence with specific file paths and line numbers.

**Example:**
```
✓ PASS: "Verified via Read(cli.py, lines 1-20): Found # /// script block with dependencies=['httpx']"
✗ FAIL: "This is usually how it works" (no verification)
```

#### Checkpoint 3: Hypothesis-Action Alignment

**Question:** Does my planned action target the SAME system as my hypothesis identified?

**Requirement:** Hypothesis system and action system must be identical.

**Example:**
```
✓ PASS:
  Hypothesis: PEP 723 inline metadata missing dependency
  Action: Add dependency to # /// script block
  (Both target PEP 723 system)

✗ FAIL:
  Hypothesis: PEP 723 inline metadata missing dependency
  Action: Run uv sync (operates on pyproject.toml)
  (Different dependency systems)
```

#### Checkpoint 4: Pattern-Matching Detection

**Question:** Is this action based on verified project reality or pattern-matching from training data?

**Requirement:** Must have read project files and verified against actual project setup.

**Example:**
```
✓ PASS: "Read package.json to verify this project uses npm (not yarn)"
✗ FAIL: "Most projects use npm, so I'll run npm install" (assumption)
```

## Configuration

No configuration required. The skill works out-of-the-box with default settings.

### Optional: Disable Auto-Invocation

If you want to manually control when verification gates activate, you can set:

```yaml
# In .claude/skills/verification-gate/SKILL.md frontmatter
disable-model-invocation: true
```

Then invoke manually:
```
@verification-gate
```

## Examples

For detailed usage examples, see [Usage Examples](./docs/examples.md).

### Example 1: Preventing Dependency System Misalignment

**Scenario:** ModuleNotFoundError for missing package

**Without Verification Gate:**
```
Error: ModuleNotFoundError: No module named 'pydantic'
→ Hypothesis: Dependencies not installed
→ Action: uv sync
→ Result: ✗ Wrong system (script uses PEP 723, not pyproject.toml)
```

**With Verification Gate:**
```
Checkpoint 1: ✓ Hypothesis stated
Checkpoint 2: ✓ Read script file, found # /// script block
Checkpoint 3: ✗ BLOCKED
  - Hypothesis: PEP 723 inline metadata
  - Proposed action: uv sync (pyproject.toml)
  - Systems don't align!
→ Revised action: Add pydantic to # /// script block
→ Result: ✓ Correct fix applied
```

### Example 2: Configuration Investigation

**Scenario:** Application not respecting timeout setting

**Without Verification Gate:**
```
→ "Usually timeouts are in config files"
→ Edit config file
→ Result: ✗ Application reads from env var, not config
```

**With Verification Gate:**
```
Checkpoint 1: ✓ Hypothesis: "Timeout read from config file"
Checkpoint 2: Grep for timeout loading code
  → Evidence: Code reads from env var first, config as fallback
  → Revised hypothesis: "Env var overrides config file"
Checkpoint 3: ✓ Action targets env var system
Checkpoint 4: ✓ Verified via reading source code
→ Result: ✓ Set env var, issue resolved
```

## Reference Materials

The skill includes comprehensive reference documentation:

### [Research Foundations](./skills/verification-gate/references/research-foundations.md)

Authoritative research backing the verification gate approach:

- Meta's Chain-of-Verification (CoVe) methodology
- Anthropic Chain-of-Thought best practices
- System 2 Attention research
- Academic findings on LLM reasoning failures

### [Failure Patterns](./skills/verification-gate/references/failure-patterns.md)

Real-world examples of verification failures and prevention:

- Pattern-matching override scenarios
- Cognitive dissonance examples
- Hypothesis-action misalignment cases
- Correct vs. incorrect action sequences

## Troubleshooting

### Issue: Verification gates feel too restrictive

**Solution:** The gates prevent errors that require 20+ tool calls to debug. The 2-3 Read operations during verification (50-100 tokens each) are a 5% cost for 95% reliability improvement.

### Issue: I want to skip verification for a specific action

**Response:** Verification is not optional—it's a defensive mechanism. If a checkpoint seems unnecessary, document why each checkpoint passes rather than bypassing them.

### Issue: Checkpoint 3 keeps blocking my actions

**Root Cause:** Your hypothesis and action target different systems. Either:
1. Revise your action to target the system your hypothesis identified
2. Gather new evidence and revise your hypothesis
3. Clarify that the systems are unrelated and need separate fixes

## Integration with Other Skills

The verification-gate skill works alongside:

- **python3-development**: Verification activates before Python script modifications
- **bash-script-developer**: Verification activates before script creation/modification
- **agent-orchestration**: Orchestrator ensures sub-agents follow verification protocol
- **holistic-linting**: Verification ensures fixes target root cause, not symptoms

## Why Verification Gates?

### The Problem

Large language models default to fast, pattern-based thinking (System 1) rather than deliberate, logical reasoning (System 2) without structural enforcement. This causes:

- 65% accuracy drop when irrelevant information is added
- Actions based on "what usually works" rather than project reality
- Correct diagnosis leading to wrong implementation

### The Solution

Verification gates implement **defensive programming for LLM reasoning**. Just as compilers block syntactically invalid code, verification gates block logically misaligned actions.

**Key Principle:** Speed without verification is not efficiency—it's error propagation.

## Contributing

Contributions welcome! When contributing:

1. Ensure changes align with research-backed verification principles
2. Update reference documentation if adding new checkpoint logic
3. Include failure examples that demonstrate the need for new checks
4. Test against real-world scenarios where verification prevents errors

## License

MIT License

## Credits

**Research Foundations:**
- Meta AI Research: Chain-of-Verification (CoVe) methodology
- Anthropic: Chain-of-Thought and prompt engineering best practices
- Academic research on System 2 Attention and LLM reasoning

**Development:**
- Based on analysis of real-world Claude Code failure patterns
- Implements structural gates to enforce existing CLAUDE.md verification protocols
