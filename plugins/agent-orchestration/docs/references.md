# Reference Materials Guide

The agent-orchestration skill includes several supplementary reference documents that provide additional context and guidance for orchestrators and sub-agents.

## Reference Files in Skill Directory

Located in `skills/agent-orchestration/`:

### clear-framework.md

A condensed version of the delegation framework for quick reference.

**When to use**: When you need a quick reminder of the core delegation principles without reading the full SKILL.md.

**Contents**: Simplified overview of the scientific delegation framework.

### hallucination-triggers.md

Documentation of common patterns that trigger inaccurate or fabricated responses in AI agents.

**When to use**: When reviewing delegation prompts to avoid patterns that cause agents to hallucinate or make unfounded assumptions.

**Contents**:
- Common triggers for inaccurate responses
- Patterns that lead to fabrication
- Mitigation strategies

### how-confident.md

Guidance on calibrating confidence levels and distinguishing verified facts from assumptions.

**When to use**: When writing delegations or reviewing agent responses to ensure appropriate confidence calibration.

**Contents**:
- Confidence calibration guidelines
- Distinguishing facts from inferences
- Appropriate hedging language

### is-it-done_gemini.md

Completion criteria reference adapted for Gemini models.

**When to use**: When working with Gemini-based agents to ensure consistent completion standards.

**Contents**: Task completion criteria reference

**Note**: The delegation template in SKILL.md references `/is-it-done` slash command which should be available in your Claude Code environment for comprehensive completion checklists.

### post-completion-validation-protocol.md

Verification procedures for ensuring tasks are truly complete before marking them as done.

**When to use**: When reviewing agent work or establishing validation standards.

**Contents**:
- Validation protocols
- Verification procedures
- Evidence requirements for completion claims

## Reference Files in Subdirectory

Located in `skills/agent-orchestration/references/`:

### accessing_online_resources.md

**Full path**: `skills/agent-orchestration/references/accessing_online_resources.md`

Definitive guide for accessing web resources with high fidelity and accuracy.

**When to use**:
- When writing AVAILABLE RESOURCES sections in delegations
- When agents need to fetch documentation or web content
- When choosing between WebFetch and MCP tools like Ref

**Key concepts covered**:
- **Accuracy**: Conforming exactly to truth (Ref returns verbatim source, WebFetch returns AI interpretation)
- **Precision**: Exactly defined, not vague (Ref preserves every character, WebFetch omits specifics)
- **Fidelity**: Degree of faithful reproduction (Ref = high fidelity, WebFetch = low fidelity)

**Critical insight**: For technical documentation and skill creation, high-fidelity access to sources is essential. When orchestrators list `WebFetch` without mentioning `Ref`, agents use the low-fidelity tool and produce work based on summaries rather than source material.

**Referenced in SKILL.md**: Line 872 with markdown link syntax:
```markdown
> [Web resource access, definitive guide for getting accurate data for high quality results](./references/accessing_online_resources.md)
```

### synthesis-improvements-from-research.md

**Full path**: `skills/agent-orchestration/references/synthesis-improvements-from-research.md`

Patterns for synthesizing research findings and improving delegation based on evidence.

**When to use**:
- When agents need to synthesize multiple information sources
- When improving delegation patterns based on outcomes
- When documenting research findings

**Contents**:
- Research synthesis patterns
- Evidence-based improvement methodologies
- Best practices for information aggregation

## Using References in Delegations

### Progressive Disclosure Pattern

The skill uses markdown link syntax to reference additional materials without cluttering the main content:

```markdown
For detailed guidance, see [accessing online resources](./references/accessing_online_resources.md)
```

This allows:
- **Main skill remains focused** - Core principles in SKILL.md
- **Deep dives available** - Detailed guidance in reference files
- **Agent-driven discovery** - Agents can follow links as needed
- **Context efficiency** - Only load references when relevant

### Referencing from Delegations

When delegating tasks that might benefit from reference materials, you can:

**Option 1: Direct agent to activate skill** (skill loads references as needed):

```text
YOUR TASK:
1. Activate agent-orchestration skill for delegation best practices
2. [Continue with task steps]
```

**Option 2: Use @filepath syntax** (if delegation needs specific reference content):

```text
CONTEXT:
- For high-fidelity documentation access, follow guidelines in @~/.claude/skills/agent-orchestration/references/accessing_online_resources.md
```

**Option 3: Describe concept** (skill reference will activate automatically):

```text
AVAILABLE RESOURCES:
- Prefer `Ref` MCP tool over `WebFetch` for documentation (high-fidelity verbatim source vs low-fidelity AI summary)
```

## Context Rot Prevention

Referenced in SKILL.md line 962:

> **Reason**: Pre-gathering causes context rot (source: <https://research.trychroma.com/context-rot>). Orchestrator context should coordinate work, not duplicate specialist tasks.

**Key insight**: Context rot occurs when:
- The same information is duplicated across multiple context windows
- Information becomes stale as context grows
- Signal-to-noise ratio decreases
- Model effectiveness degrades

**Prevention strategies** (from the skill):
- Pass-through existing context, don't pre-gather
- Let agents gather their own data
- Use references for deep details, not in-line documentation
- Keep delegations focused on observations and success criteria

## Additional Resources

### External References Cited in Skill

The SKILL.md references external resources that provide foundational context:

- **Context rot research**: <https://research.trychroma.com/context-rot>
  - Understanding how duplicated context degrades model performance
  - Why pre-gathering data for delegation is harmful

### Related Skills and Commands

The delegation framework references several other capabilities that should be available:

**Skills**:
- `holistic-linting` - Linting workflow guidance
- `uv` - Python UV tool usage
- `hatchling` - Python packaging with hatchling

**Commands**:
- `/is-it-done` - Task completion criteria checklists (referenced in delegation template)

**Agents** (referenced for specialized delegation):
- `context-gathering` - Gather context without polluting orchestrator window
- `python-cli-architect` - Python code implementation
- `python-pytest-architect` - Python test planning and implementation
- `python-code-reviewer` - Python code review
- `bash-script-developer` - Bash script implementation
- `bash-script-auditor` - Bash script review
- `documentation-expert` - User-facing documentation
- `system-architect` - System architecture documentation
- `linting-root-cause-resolver` - Linting issue resolution

## Reference File Reading Tips

### For Orchestrators

When you're structuring a delegation and unsure about best practices:

1. **Check SKILL.md sections**:
   - "Pre-Delegation Verification Checklist" (lines 38-77)
   - "Writing Effective AVAILABLE RESOURCES" (lines 154-263)
   - "Common Delegation Issues to Avoid" (lines 780-874)

2. **Review anti-patterns**:
   - "The Pre-Gathering Anti-Pattern" (lines 876-963)
   - "Verification Questions for Orchestrators" (lines 522-549)

3. **Use the delegation template**:
   - Located at lines 84-152
   - Copy structure for consistency

### For Sub-Agents

When you receive a delegation prompt:

1. **Verify delegation quality**:
   - Are observations factual or assumed?
   - Is success criteria measurable?
   - Do you have full discovery access?

2. **Request clarification if needed**:
   - Missing success criteria
   - Contradictory constraints
   - Prescribed implementation without justification

3. **Follow the scientific method**:
   - Gather comprehensive data
   - Form hypothesis
   - Design tests
   - Verify against authoritative sources
   - Implement with evidence

## Documentation Maintenance

### When to Update References

Reference materials should be updated when:

- New anti-patterns are discovered through practice
- Research findings provide new insights
- Tool ecosystems evolve (new MCP servers, updated tools)
- User feedback reveals common misunderstandings

### Contribution Guidelines

When contributing updates to reference materials:

1. **Cite sources** - Include URLs and access dates for external references
2. **Provide examples** - Concrete examples over abstract principles
3. **Explain rationale** - Why patterns work or don't work
4. **Use consistent formatting** - Follow existing markdown patterns
5. **Link appropriately** - Use relative markdown links (`./file.md`) not backticks

---

[← Back to README](../README.md) | [Skills Reference](./skills.md) | [Examples](./examples.md)
