# Skills Reference

This document provides detailed information about the skills included in the verification-gate plugin.

## verification-gate

**Location:** `skills/verification-gate/SKILL.md`

**Description:** Enforce mandatory pre-action verification checkpoints to prevent pattern-matching from overriding explicit reasoning. Use this skill when about to execute implementation actions (Bash, Write, Edit) to verify hypothesis-action alignment. Blocks execution when hypothesis unverified or action targets different system than hypothesis identified. Critical for preventing cognitive dissonance where correct diagnosis leads to wrong implementation.

**User Invocable:** Yes (default)

**Model:** Inherits from session (not specified in frontmatter)

**Allowed Tools:** All tools (not restricted)

**Context:** Inline (not forked)

### When to Use

The verification-gate skill automatically activates when:

- About to execute ANY implementation action (Bash, Write, Edit, NotebookEdit)
- After stating a hypothesis about what system/component has an issue
- Choosing between multiple implementation approaches
- Detecting potential pattern-matching from training data
- Error messages or observations could trigger multiple solution paths

### Core Principle

Verification is **not advisory**—it is a **mandatory gate**. Actions that don't align with verified hypotheses are BLOCKED.

### Activation

**Automatic:**
The skill auto-activates before implementation actions. No manual invocation needed.

**Manual:**
```
@verification-gate
```

or

```
Skill(command: "verification-gate")
```

### The 4-Checkpoint System

Before executing ANY implementation action, complete ALL checkpoints in sequence. If any checkpoint fails, HALT and report the failure.

#### Checkpoint 1: Hypothesis Stated

**Requirement:** Have I explicitly stated what system/component the issue affects?

**Test:**
- Can I name the specific system? (e.g., "PEP 723 inline metadata", "pyproject.toml dependencies", "Docker network configuration")
- Have I written this hypothesis explicitly in my response?

**Pass Criteria:**
```
✓ "Hypothesis: The issue affects [specific system/component]"
```

**Fail Criteria:**
```
✗ BLOCKED - Hypothesis not stated
REQUIRED: State hypothesis explicitly before proceeding
```

#### Checkpoint 2: Hypothesis Verified

**Requirement:** Have I gathered evidence to confirm or refute my hypothesis?

**Verification Methods:**
- Read relevant files to confirm system state
- Check official documentation for expected behavior (use MCP tools: Ref for docs, exa for code context)
- Test or execute commands to observe actual behavior
- Grep for configuration or implementation details

**Test:**
- Have I used Read/Grep/MCP tools (Ref/exa)/Bash (read-only) to gather evidence?
- Can I cite specific files, line numbers, or outputs supporting my hypothesis?

**Pass Criteria:**
```
✓ Verified via [tool calls with file paths and line numbers]
✓ Evidence: [specific observations from files/outputs]
```

**Fail Criteria:**
```
✗ BLOCKED - Hypothesis not verified
REQUIRED: Gather evidence before proceeding
NEXT STEPS:
1. Identify what evidence would confirm/refute hypothesis
2. Use appropriate tools to gather that evidence
3. Document findings with file paths and line numbers
4. Revise hypothesis if evidence contradicts it
```

#### Checkpoint 3: Hypothesis-Action Alignment

**Requirement:** Does my planned action target the SAME system as my hypothesis identified?

**Alignment Template:**
```
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: [What system does my hypothesis     │
│                     identify as the problem location?]  │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     [What system does my planned action  │
│                     operate on or modify?]              │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   [Same system = ✓ Proceed]           │
│                    [Different systems = ✗ BLOCKED]      │
└─────────────────────────────────────────────────────────┘
```

**Common Misalignments:**

| Hypothesis System | Wrong Action System | Why Blocked |
|-------------------|---------------------|-------------|
| PEP 723 inline metadata (`# /// script`) | `uv sync` (pyproject.toml) | Different dependency systems |
| Docker container config | Host network settings | Different network layers |
| Git repository state | File system permissions | Different system domains |
| Python virtual environment | Global pip install | Different installation scopes |
| Application code logic | Infrastructure configuration | Different operational layers |

**Pass Criteria:**
```
✓ ALIGNED - both target [system name]
```

**Fail Criteria:**
```
✗ BLOCKED - Hypothesis-action misalignment detected
HYPOTHESIS targets: [system A]
ACTION operates on: [system B]

REQUIRED: Either:
1. Revise action to target same system as hypothesis
2. Revise hypothesis after gathering new evidence
3. Report that systems are unrelated and task needs clarification
```

#### Checkpoint 4: Pattern-Matching Detection

**Requirement:** Is this action based on verified project reality or pattern-matching from training data?

**Detection Questions:**
1. Did I read any files in THIS project to verify this approach?
2. Did I check official documentation for THIS version/tool?
3. Is my action based on what THIS project actually uses?
4. Or is my action based on common patterns I've seen in training data?

**Pattern-Matching Indicators:**
- Solution appears immediately without investigation
- Executing command within 1-2 tool calls of error observation
- Not using Read/Grep/MCP tools to verify before acting
- Thinking "this is the standard way to do X" without checking if project uses standard approach
- Recognizing error pattern and jumping to common solution

**Pass Criteria:**
```
✓ VERIFIED against project reality
✓ Read files: [list]
✓ Confirmed approach matches project setup
```

**Fail Criteria:**
```
⚠ PATTERN-MATCHING WARNING
I am using training data patterns without project verification.

REQUIRED actions:
1. State: "I am pattern-matching from training data without verification"
2. Read relevant files to understand current project setup
3. Check project documentation or configuration
4. Verify approach against project reality
5. Return to Checkpoint 2 with gathered evidence
```

### Execution Decision

**After completing ALL four checkpoints:**

**✓ ALL CHECKPOINTS PASSED → EXECUTE ACTION**

Document verification trail:
```
VERIFICATION COMPLETE:
✓ Checkpoint 1: Hypothesis stated - [brief hypothesis]
✓ Checkpoint 2: Verified via [files/docs read]
✓ Checkpoint 3: Aligned - both target [system name]
✓ Checkpoint 4: Verified against project reality

EXECUTING: [action description]
```

**✗ ANY CHECKPOINT FAILED → HALT**

Report failure explicitly:
```
EXECUTION BLOCKED
Failed checkpoint: [number and name]
Reason: [specific failure reason]
Required before proceeding: [specific next steps]
```

### Reference Files

The skill includes reference documentation for deeper understanding:

#### [research-foundations.md](../skills/verification-gate/references/research-foundations.md)

Authoritative research backing the verification gate approach:

- Meta Chain-of-Verification (CoVe) methodology
- Anthropic Chain-of-Thought best practices
- System 2 Attention research
- Academic findings on LLM reasoning failures

**Load this reference when:**
- Understanding why verification gates are necessary
- Justifying verification overhead to users
- Researching advanced verification techniques
- Designing new checkpoint patterns

#### [failure-patterns.md](../skills/verification-gate/references/failure-patterns.md)

Common failure modes and how verification prevents them:

- Pattern-matching override scenarios
- Cognitive dissonance examples
- Hypothesis-action misalignment cases
- Real-world verification violations

**Load this reference when:**
- Diagnosing why verification failed
- Identifying subtle misalignments
- Learning from historical failures
- Teaching verification concepts

#### [accessing_online_resources.md](../skills/verification-gate/references/accessing_online_resources.md)

Guide for using MCP tools for high-fidelity research:

- `mcp__Ref__ref_search_documentation` for verbatim documentation
- `mcp__exa__get_code_context_exa` for code examples
- `mcp__exa__web_search_exa` for web research
- WebFetch usage as fallback

**Load this reference when:**
- Checkpoint 2 requires external documentation
- Verifying library behavior or API usage
- Researching best practices for unfamiliar tools

### Self-Monitoring

The model must actively monitor for verification violations:

**Warning Signs:**
- Stating hypothesis then immediately executing without Checkpoint 2
- Reading files AFTER taking action instead of BEFORE
- Modifying different files/systems than hypothesis identified
- Solution appearing reflexively upon seeing error message
- Not being able to cite specific evidence for hypothesis

**When Warning Signs Detected:**
```
⚠ VERIFICATION VIOLATION DETECTED
I attempted to bypass verification checkpoint.
HALTING and returning to Checkpoint [number].
```

### Integration with Other Skills

This skill works in conjunction with:

- **python3-development**: Verification gate activates before executing Python scripts or modifying code
- **bash-script-developer**: Verification gate activates before creating/modifying scripts
- **agent-orchestration**: Orchestrator ensures sub-agents follow verification protocol
- **holistic-linting**: Verification ensures fixes target root cause, not symptoms

### Integration with CLAUDE.md Rules

This skill enforces existing CLAUDE.md verification protocols by adding structural gates:

**CLAUDE.md states:** "The model must verify behavior with authoritative sources"
**This skill enforces:** "Cannot execute until verification completed and documented"

**CLAUDE.md states:** "Never cargo cult code without verification"
**This skill enforces:** "Checkpoint 4 detects and blocks pattern-matching behavior"

**CLAUDE.md states:** "Distinguish verified information from assumptions"
**This skill enforces:** "Checkpoint 2 requires evidence before proceeding"

### Performance Characteristics

**Overhead:** 2-3 Read operations (50-100 tokens each) for verification

**Benefit:** Prevents wrong implementations requiring 20+ tool calls to debug (4000+ tokens)

**ROI:** 5% cost for 95% reliability improvement

**Key Principle:** Speed without verification is not efficiency—it's error propagation.

---

## Additional Resources

For practical examples of the verification-gate skill in action, see [Usage Examples](./examples.md).

For installation and setup instructions, see the main [README](../README.md).
