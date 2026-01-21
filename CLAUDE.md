# Claude Skills Repository - AI-Facing Project Instructions

This repository contains a Claude Code Marketplace Plugin providing Skills for Claude - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools.

---

## Skill Creator Activation Protocol

<skill_activation_triggers>

The model MUST activate the skill-creator skill from the <available_skills> list when ANY of these conditions are met:

**Positive Triggers** (MUST activate):

- User explicitly requests creating, modifying, or reviewing a skill
- Model is about to modify files matching patterns: `*/SKILL.md`, `*/references/*.md` within a skill directory
- User asks questions about skill structure, frontmatter format, or validation requirements
- Model needs to convert documentation into AI-optimized instruction format
- User requests optimization of existing skill documentation for LLM consumption

**Activation Syntax**:

```claude
Skill(command: "example-skills:skill-creator")
```

**Negative Conditions** (MUST NOT activate):

- Simply using an existing skill (read-only activation)
- Referencing a skill in conversation without modification intent
- General coding tasks unrelated to skill creation
- Reading skill documentation for context without editing

**Verification**: Before activating skill-creator, the model MUST verify:

1. The task involves skill creation/modification (not just usage)
2. No other specialized skill better matches the task domain
3. The model has read any existing skill files being modified

</skill_activation_triggers>

---

## Task Delegation Rule

**When invoking the Task tool, follow the Delegation Template in the agent-orchestration skill.**

### Path Conventions for Sub-Agent Delegation

<delegation_path_rules>

The model MUST use paths relative to the current working directory when delegating tasks to sub-agents.

**Correct Pattern:**

```text
CONTEXT:
- Location: ./gitlab-skill/scripts/
- File to modify: ./gitlab-skill/scripts/sync-gitlab-docs.py
```

**Incorrect Patterns:**

```text
# Absolute paths - unnecessary, verbose
- Location: /home/user/repos/project/gitlab-skill/scripts/

# Symlink paths - triggers security prompts, outside repo
- Location: ~/.claude/skills/gitlab-skill/scripts/
```

**Why This Matters:**

1. **Security**: Paths outside the current repository trigger manual approval prompts for every file operation
2. **Simplicity**: Relative paths are shorter and clearer
3. **Portability**: Relative paths work regardless of where the repo is cloned
4. **Symlinks**: Skills are symlinked from `~/.claude/skills/` to this repo - always use the repo path, not the symlink

**Rule**: If the file exists within the current working directory tree, use `./relative/path`. The sub-agent inherits the same working directory.

</delegation_path_rules>

---

## Plugin Post-Creation Requirements

The model MUST run `install.py` after creating a new plugin in the plugins/ directory:

- This script executes `ln -sf` for each skill directory nested in the plugins/ directory to symlink them to `~/.claude/skills/` this is to support instant testing of the skills by the local developer.
- Safe to run multiple times (idempotent operation)
- Modifications to existing plugins do NOT require re-running install.py (symlinks point to directory)

---

## Content Optimization for Skills

<content_optimization_purpose> When tasked with rewriting text for LLM consumption: Transform input into concise, technical instructions, reference material, and rules suitable for AI consumption. The audience is an AI model with expert-level comprehension of all technical concepts. Assume complete familiarity with domain internals. </content_optimization_purpose>

### Core Principles

The model MUST follow these principles when transforming text into RULES, CONDITIONS, and CONSTRAINTS:

- Write focused, imperative, actionable, scoped rules
- Keep rules concise (target: under 500 lines per file)
- Split significant concepts into multiple composable rules or contextually tagged data sets
- Preemptively provide URLs to further reading and links to referenced files
- Avoid vague guidance - write rules as clear internal documentation
- Use declarative phrasing ("The model MUST") for all instructions
- Produce deterministic, flat ASCII text - avoid stylistic markdown (bold, italic) - use only structural markdown (headings, lists, links, code fences with language specifiers)
- Include explicit sections for: identity, intent, task rules, issue handling, triggers, external references
- Preserve or expand structured examples found in source text

### Strategic XML Tag Usage

<xml_usage_guidelines>

**When to Use XML Tags** (Source: Anthropic docs.claude.com/prompt-engineering/use-xml-tags):

XML tags improve clarity, accuracy, flexibility, and parseability when prompts involve multiple components such as context, instructions, and examples.

**Application**:

- Use tags like `<instructions>`, `<example>`, `<formatting>` to separate prompt parts
- Prevents Claude from mixing up instructions with examples or context
- Be consistent with tag names throughout prompts
- Nest tags `<outer><inner></inner></outer>` for hierarchical content
- Combine with multishot prompting (`<examples>`) or chain of thought (`<thinking>`, `<answer>`)

**Key Insight**: There are no canonical "best" XML tags - use semantic names that make sense with the information they surround.

</xml_usage_guidelines>

### Text Transformation Rules

<transformation_rules>

When rewriting text for AI consumption, the model MUST:

1. Open with a directive on how to read and apply the rules
2. Maximize information density using technical jargon, dense terminology, equations, industry-specific terms
3. Rephrase for accuracy and specificity
4. Address an expert, scientific, or academic audience
5. Use only visible ASCII characters
6. Write as lookup references for AI consumption - optimize as decision triggers and pattern-matching rules for an AI that already knows technical details, NOT educational content
7. Omit greetings and unnecessary prose
8. Preserve original text's output structure specifications if observed
9. Use precise, deterministic ACTION→TRIGGER→OUTCOME format in frontmatter descriptions
10. Set clear priority levels between rules to resolve conflicts efficiently
11. Provide concise positive and negative examples of rule application
12. Optimize for AI context window efficiency - remove non-essential information
13. Use standard glob patterns without quotes (e.g., _.js, src/\*\*/_.{ts,js})
14. Keep frontmatter descriptions rich with TRIGGERS for when rules should be used
15. Limit examples to essential patterns only

</transformation_rules>

---

## File Reference Patterns in Skills

### Code Fence Language Specifiers

The model MUST add a language specifier to ALL opening code fences:

Markdown file containing nested code blocks

````markdown
# Section Title

```text
Plain text content or structured ASCII
```

```python
def example():
    return True
```
````

<rationale>4 backticks on outer fence, language specifiers on all inner fences, proper nesting</rationale>

### Markdown Links with Relative Paths

<correct_pattern>

When creating references between files within a skill, the model MUST use markdown links with relative paths starting with `./`:

**Syntax**: `[descriptive text](./path/to/file.md)`

**Examples from Anthropic's mcp-builder skill**:

```markdown
[📋 View Best Practices](./reference/mcp_best_practices.md) [🐍 Python Implementation Guide](./reference/python_mcp_server.md) [✅ Evaluation Guide](./reference/evaluation.md)
```

**Directory Context Rules**:

- From `SKILL.md` → reference files: `[text](./references/filename.md)`
- From `references/modern-modules.md` → same dir: `[text](./filename.md)`
- From `references/modern-modules.md` → subdir: `[text](./modern-modules/filename.md)`

**Why This Matters**:

1. Navigability: Markdown links allow Claude Code to click through to referenced files
2. Portability: Relative paths work regardless of installation location
3. Progressive Disclosure: Claude can load referenced files on demand, preserving context efficiency
4. User Experience: Users and Claude can follow references naturally

</correct_pattern>

<anti_patterns>

The model MUST NOT use these patterns:

**❌ Backticks Around Filenames** (not navigable):

```markdown
See `modern-modules/httpx.md` for details
```

**❌ Absolute Paths** (not portable):

```markdown
See [httpx](/home/user/repos/claude_skills/python3-development/references/modern-modules/httpx.md)
```

**❌ Skill Activation as File Path** (incorrect syntax):

```markdown
See `/uv/SKILL.md` for uv documentation
```

Correct: `Activate the uv skill with @uv or Skill(command: "uv")`

**❌ Relative Paths Without `./` Prefix** (ambiguous):

```markdown
[text](references/file.md)
```

Correct: `[text](./references/file.md)`

</anti_patterns>

### Skill Activation References

<skill_reference_pattern>

When referencing other skills, the model MUST use activation syntax in descriptive text:

**✅ Correct**:

```markdown
For comprehensive Astral uv documentation, activate the uv skill:

Skill(command: "uv")
```

**❌ Incorrect**:

```markdown
See `/uv/SKILL.md` for uv documentation
```

</skill_reference_pattern>

---

## Skill Documentation Verification Requirements

<critical_understanding>

**Skill documentation (SKILL.md, reference files) is AI-facing documentation, NOT user-facing documentation.**

**Primary Audience**:

1. The orchestrator (Claude) - reads skills to guide orchestration decisions, agent selection, workflow patterns
2. Sub-agents - load and follow the same skill guidance when delegated tasks
3. Future sessions - skills persist across conversations and inform all future AI instances

**NOT the Primary Audience**:

- Human users do not directly read SKILL.md line-by-line
- Skills are NOT user-facing product documentation
- Skills are AI→AI instruction sets

</critical_understanding>

### Why Verification Matters for Skill Documentation

<verification_importance>

When the model writes false, unverified, or assumed information in skill documentation:

1. **The model misleads itself** - will reference and believe fabricated content later
2. **Sub-agents are misled** - follow incorrect guidance in their implementations
3. **Future sessions are misled** - false information persists and compounds
4. **The human receives wrong results** - because all AI instances follow bad guidance
5. **Creates false feedback loops** - wrong information becomes "truth" in context

**Critical Principle**: The model must treat skill documentation with the same rigor as code - it must be verified, cited, and accurate.

</verification_importance>

### Mandatory Verification Protocol

<verification_protocol>

Before documenting ANY behavior, capability, or characteristic of:

- Commands (slash commands in `~/.claude/commands/`)
- Agents (in `~/.claude/agents/`)
- Tools (CLI tools, system commands)
- Libraries or packages
- System behavior or configuration

**The model MUST execute ALL of these steps**:

<verification_steps>

1. **Read the Actual Source**

   - Command files: Read entire file, note line numbers
   - Agent files: Read YAML frontmatter and complete prompt
   - Official documentation: Use WebSearch, WebFetch, or mcp\_\_Ref tools
   - Library code: Read source files directly

2. **Verify the Behavior**

   - Execute commands/scripts if possible to observe actual behavior
   - Cite evidence from source files with line number references
   - Test against documented claims before writing them

3. **Cite Observations**

   - Format: "According to lines X-Y of [file path]..."
   - Format: "Testing command X produces output: [exact output]"
   - Format: "Per official documentation at [URL]..."

4. **Never Fabricate**

   - If unknown, state "unverified" explicitly
   - Research using available tools (Read, Grep, WebSearch, mcp\_\_Ref)
   - If unable to verify, state "Unable to verify [claim] due to [reason]"

5. **Distinguish Assumption from Fact**
   - Mark assumptions explicitly: "Assuming [X] based on [pattern/inference]"
   - Separate verified facts from reasonable inferences
   - Never present assumptions as facts

</verification_steps>

**Minimum Requirements**:

- Cite minimum 3 independent authoritative sources for major claims
- Include line numbers when referencing code files
- Execute test if behavior can be observed directly
- Note publication dates for documentation sources

</verification_protocol>

### Verification Examples

<examples>

<example type="violation">
  <scenario>Documenting command behavior without reading source</scenario>
  <incorrect_output>
→ Validates shebang matches script type
→ Checks PEP 723 metadata if external dependencies detected
  </incorrect_output>
  <problem>Written without reading actual command file to verify what it does</problem>
  <consequence>If command doesn't actually validate shebangs, this creates false information in AI knowledge base</consequence>
</example>

<example type="violation">
  <scenario>Assuming tool capabilities without verification</scenario>
  <incorrect_output>
python-portable-script agent creates stdlib-only scripts
  </incorrect_output>
  <problem>Written without reading agent implementation or verifying PEP 723 requirement</problem>
  <consequence>Sub-agents will follow incorrect guidance when using this agent</consequence>
</example>

<example type="violation">
  <scenario>Inventing requirements from training data patterns</scenario>
  <incorrect_output>
Stdlib-only scripts need PEP 723 for self-contained execution
  </incorrect_output>
  <problem>Based on pattern-matching from training, not verification of PEP 723 specification</problem>
  <consequence>Creates false technical requirement that propagates across sessions</consequence>
</example>

<example type="correct">
  <scenario>Verified documentation with source citation</scenario>
  <correct_output>
→ Corrects shebang to match script type
→ Adds PEP 723 metadata if external dependencies detected
→ Removes PEP 723 if stdlib-only
→ Sets execute bit if needed

Source: Lines 162, 208 of ~/.claude/commands/shebangpython.md </correct_output> <rationale>Includes specific line number citations from actual source file</rationale> </example>

<example type="correct">
  <scenario>Explicit uncertainty when unable to verify</scenario>
  <correct_output>
The python-portable-script agent purpose is not yet verified. Before documenting its behavior, I will read the agent file to confirm its actual capabilities.
  </correct_output>
  <rationale>States uncertainty explicitly and commits to verification before documenting</rationale>
</example>

</examples>

---

## Reference Documentation Citation Requirements

<citation_requirements>

**Principle**: Reference documentation is only as reliable as its sources. Without citations, guidance cannot be verified, updated, or trusted.

**The model MUST provide source attribution for ALL reference documentation using one of these methods:**

### Citation Method 1: Inline Citations

Cite sources directly within the contextual section where the information is used:

```markdown
### Tool Naming Standards

RULE: Use snake*case for tool names with pattern `{service}*{action}\_{resource}`

SOURCE: [MCP Best Practices - Tool Naming](https://modelcontextprotocol.io/docs/best-practices#tool-naming) (accessed 2025-01-15)

EXAMPLES:

- `slack_send_message` (not just `send_message`)
```

### Citation Method 2: References Footer

Add a "## References" section at the end of the document:

```markdown
## References

1. **MCP Protocol Specification** - https://modelcontextprotocol.io/llms-full.txt (accessed 2025-01-15)
2. **FastMCP Documentation** - https://github.com/jlowin/fastmcp (accessed 2025-01-15)
3. **Tool Design Patterns** - Community consensus from FastMCP examples repository
```

Reference in text using: `[1]`, `[2]`, etc.

### Citation Method 3: Separate references.md File

For skills with extensive citations, create `./references/references.md`:

```markdown
# References for fastmcp-creator Skill

## Official Documentation

- MCP Protocol: https://modelcontextprotocol.io/llms-full.txt
- FastMCP: https://github.com/jlowin/fastmcp

## Community Resources

- FastMCP Examples: https://github.com/jlowin/fastmcp/tree/main/examples
```

Reference in SKILL.md: `See [References](./references/references.md) for complete source list`

### Required Citation Details by Source Type

**Derived from Another Skill:**

```markdown
SOURCE: Based on [mcp-builder skill](https://github.com/anthropics/claude-code-examples/tree/main/mcp-builder) ADAPTATIONS: Modified tool naming conventions for Python-specific patterns
```

**Collated from Websites/Forums:**

The model MUST cite EVERY source when aggregating information:

```markdown
SOURCES:

- [MCP Best Practices](https://modelcontextprotocol.io/docs/best-practices) (accessed 2025-01-15)
- [FastMCP GitHub Issues #42](https://github.com/jlowin/fastmcp/issues/42) (accessed 2025-01-15)
- [Reddit: r/ClaudeAI - MCP Tool Design Discussion](https://reddit.com/r/ClaudeAI/comments/xyz) (accessed 2025-01-15)

RATIONALE: Allows verification and updates as new information becomes available
```

**Based on User Preferences/Discussions:**

The model MUST document the origin with date:

```markdown
SOURCE: User preference established in conversation (2025-01-15) CONTEXT: User prefers 5-part tool description structure based on improved AI tool selection in testing VALIDATION: Tested on 20 tools, improved selection accuracy from 65% to 89%
```

**Based on Experiments/Testing:**

The model MUST document the experimental basis:

```markdown
SOURCE: Experimental validation (2025-01-15) METHOD: Tested 15 tools with varying description formats across 50 prompts RESULTS: 5-part structure yielded 89% correct tool selection vs 65% for unstructured descriptions DATASET: Available at ./references/experiments/tool-description-testing.md
```

### Verification Requirements

When creating or updating reference documentation, the model MUST verify:

- [ ] Every factual claim has a cited source
- [ ] URLs include access dates (format: YYYY-MM-DD)
- [ ] Skill derivations link to source skill repository
- [ ] User preferences note the conversation date
- [ ] Experimental claims reference datasets or methodology
- [ ] Citations distinguish between official docs, community practices, and opinions

### Prohibited Patterns

**❌ Uncited Best Practices:**

```markdown
RULE: Tool descriptions must be concise and actionable
```

**✅ Properly Cited:**

```markdown
RULE: Tool descriptions must be concise and actionable SOURCE: [MCP Best Practices](https://modelcontextprotocol.io/docs/best-practices#descriptions) (accessed 2025-01-15)
```

**❌ Vague Attribution:**

```markdown
Based on community best practices
```

**✅ Specific Attribution:**

```markdown
SOURCE: Pattern observed across FastMCP example projects:

- https://github.com/jlowin/fastmcp/tree/main/examples/weather (accessed 2025-01-15)
- https://github.com/jlowin/fastmcp/tree/main/examples/github (accessed 2025-01-15)
```

### Rationale

**Why Citations Matter:**

1. **Verifiability** - Claims can be checked against original sources
2. **Updateability** - When upstream documentation changes, we know what to update
3. **Authority** - Distinguishes official specs from opinions
4. **Trust** - Future AI sessions can validate guidance before following it
5. **Debugging** - When guidance fails, citations reveal whether source changed or was misinterpreted

**Without Citations:**

- Cannot distinguish fact from assumption
- Cannot update when sources change
- Cannot verify correctness
- Creates false feedback loops in AI knowledge

</citation_requirements>

---

## File Reference Verification Checklist

<verification_checklist>

When creating or updating reference files, the model MUST verify:

- [ ] All file references use markdown link syntax: `[text](./path)`
- [ ] Relative paths start with `./`
- [ ] Paths are relative to the file containing the reference
- [ ] Referenced files actually exist at those paths (verify with Read tool)
- [ ] No backticks used for file references (unless showing code/commands)
- [ ] Language specifiers present on all code fences
- [ ] Nested code blocks use proper backtick counts (4 for outer, 3 for inner)

</verification_checklist>

---

## Skill Validation vs Packaging

<skill_validation>

**Validation: YES** - The model MUST validate skills to ensure quality standards:

- YAML frontmatter is properly formatted
- Required fields are present (name, description, tools, model)
- File references are correct and target files exist
- Directory structure is valid

**Packaging: NO** - The model MUST NOT package skills into .zip files for distribution:

- Skills in this repository are for local use
- Already in their final location
- Packaging creates unnecessary files
- Serves no purpose for local development

</skill_validation>

---

## Markdown Formatting Standards

<markdown_standards>

The model MUST follow these markdown formatting rules:

**MD031/blanks-around-fences**: Fenced code blocks MUST be surrounded by blank lines

**Example**:

````markdown
This is a paragraph.

```python
def example():
    return True
```
````

This is another paragraph.

````

</markdown_standards>

---

## Local Formatting and Linting Tools

<available_tools>

The model MUST use these tools for formatting and linting in this repository:

```bash
uv run pre-commit --files <file>
````

**When to use**:

- Before committing skill documentation
- After modifying SKILL.md or reference files
- To validate markdown formatting compliance

</available_tools>

---

## Linting Exception Conditions

<linting_exceptions>

The model MUST NOT ignore or bypass linting errors UNLESS the code falls into one of these categories:

**Acceptable Exceptions** (OK to ignore linting):

1. **Vendored code** - Third-party code copied into the repository without modification. The model did not author this code and should not modify it.

2. **Examples of what-not-to-do** - Intentionally incorrect code used for educational purposes or negative test cases. The linting errors are the point.

3. **Code pinned to historic Python version** - Code that must remain compatible with Python versions older than 3.11 where modern syntax is unavailable.

4. **Code for Python derivatives** - CircuitPython, MicroPython, or other Python implementations with different syntax requirements or missing standard library modules.

**Unacceptable Exceptions** (MUST fix or escalate):

If NONE of the above conditions apply, the model MUST:

1. Fix the linting error at root cause
2. If unable to fix, document the specific blocker
3. Never add `# type: ignore`, `# noqa`, or similar suppressions without explicit user approval

**Rule Codes That MUST Always Be Fixed** (never suppress):

These rule codes indicate real code quality issues that must be resolved at root cause:

- **BLE001** (blind-except): Replace generic `except Exception` with specific exception types
- **D103** (missing-docstring-in-public-function): Add docstrings to public functions
- **TRY300** (try-consider-else): Restructure try/except/else blocks properly

**Per-File Exceptions in pyproject.toml** (acceptable):

The following rules may be configured as per-file ignores in `pyproject.toml` `[tool.ruff.lint.per-file-ignores]`:

- `**/scripts/**`: T201 (print), S (security), DOC, ANN401, PLR0911, PLR0917, PLC0415
- `**/tests/**`: S, D, E501, ANN, DOC, PLC, SLF, PLR, EXE, N, T
- `**/assets/**`: PLC0415, DOC
- `typings/**`: N, ANN, A

These configurations allow relaxed checking in appropriate contexts without inline suppressions.

**Touched Files Must Be Clean**:

When files are modified, moved, or renamed, all linting issues in those files MUST be resolved before committing. Touching a file means taking responsibility for its quality.

**SOURCE**: User policy established in conversation (2025-01-15)

</linting_exceptions>

---

## Sessions Framework Integration

<sessions_integration>

**Context**: The file `@sessions/CLAUDE.sessions.md` provides essential instructions for Claude Code when working in the cc-sessions framework.

**Detection Trigger**: A project has cc-sessions enabled if EITHER condition is met:

- Directory `./sessions/` exists in project root
- File `./CLAUDE.sessions.md` exists in project root

**Integration Requirement**: When cc-sessions is detected, the model MUST read and follow instructions from the sessions documentation BEFORE beginning implementation tasks.

**Verification**:

```bash
# Check for sessions framework
ls -la ./sessions/ 2>/dev/null || ls -la ./CLAUDE.sessions.md 2>/dev/null
```

</sessions_integration>

---

## Agent Usage for Plugin Maintenance

<agent_usage_guidance>

This repository provides specialized agents for maintaining and improving Claude Code plugins.

### plugin-assessor

**Purpose**: Analyze plugins for structural correctness, frontmatter optimization, schema compliance, and enhancement opportunities.

**When to use**:

- Reviewing plugins before marketplace submission
- Auditing existing plugins for issues
- Validating plugin structure against schema
- Identifying orphaned documentation or missing cross-references
- Assessing frontmatter quality

**Delegation Pattern**:

```claude
Task(
  agent="plugin-assessor",
  prompt="Assess the plugin at ./plugins/my-plugin for marketplace readiness"
)
```

---

### plugin-docs-writer

**Purpose**: Generate comprehensive README.md and supplementary documentation for plugins.

**When to use**:

- Creating documentation for new plugins
- Updating documentation after plugin changes
- Generating docs/skills.md, docs/commands.md, docs/agents.md
- Creating usage examples and configuration guides

**Delegation Pattern**:

```claude
Task(
  agent="plugin-docs-writer",
  prompt="Generate complete documentation for the plugin at ./plugins/my-plugin"
)
```

---

### skill-refactorer

**Purpose**: Refactor large or multi-domain skills into smaller, focused skills without losing fidelity.

**When to use**:

- Skill exceeds 500 lines
- Skill covers multiple distinct domains
- Skill would benefit from separation of concerns
- Need to split by use case, tool requirements, or expertise level

**Delegation Pattern**:

```claude
Task(
  agent="skill-refactorer",
  prompt="Refactor ./plugins/python3-development/skills/python3/SKILL.md into focused skills for testing, async, and packaging"
)
```

---

### claude-context-optimizer

**Purpose**: Review and improve AI-facing documentation following Anthropic prompt engineering best practices.

**When to use**:

- Reviewing existing AI-facing documentation for clarity
- Optimizing instructions for LLM consumption
- Analyzing structure against best practices
- Converting unstructured documentation to structured format
- Creating new skills, agents, or commands

**Delegation Pattern**:

```claude
Task(
  agent="claude-context-optimizer",
  prompt="Review [skill|agent|command] at [path] and suggest improvements for AI comprehension"
)
```

---

### Agent Skills Configuration

All plugin maintenance agents load reference skills automatically:

| Agent              | Loaded Skills                                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| plugin-assessor    | claude-skills-overview-2026, claude-plugins-reference-2026, claude-commands-reference-2026, claude-hooks-reference-2026 |
| plugin-docs-writer | claude-skills-overview-2026, claude-plugins-reference-2026, claude-commands-reference-2026, claude-hooks-reference-2026 |
| skill-refactorer   | claude-skills-overview-2026                                                                                             |

This ensures agents have complete knowledge of Claude Code plugin architecture, frontmatter schemas, and best practices.

</agent_usage_guidance>

---

## Agentic Workflow Diagrams

<workflow_diagrams>

This repository includes comprehensive workflow diagrams that visualize how skills, agents, commands, and hooks work together across the 6-stage agentic process flow.

**Location**: `.claude/knowledge/workflow-diagrams/`

### Available Diagrams

| Diagram                                                                                         | Purpose                                     | When to Consult                            |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| [Master Workflow](./.claude/knowledge/workflow-diagrams/master-workflow.md)                     | Complete 6-stage overview with all assets   | Understanding the full system architecture |
| [Asset Decision Tree](./.claude/knowledge/workflow-diagrams/asset-decision-tree.md)             | Skill vs Command vs Agent vs Hook selection | Creating new extensions                    |
| [Multi-Agent Orchestration](./.claude/knowledge/workflow-diagrams/multi-agent-orchestration.md) | Delegation and DONE/BLOCKED signaling       | Coordinating sub-agents                    |
| [Simple Task Workflow](./.claude/knowledge/workflow-diagrams/simple-task-workflow.md)           | Minimal path for straightforward tasks      | Quick implementations                      |
| [Investigation Workflow](./.claude/knowledge/workflow-diagrams/investigation-workflow.md)       | Hypothesis-driven scientific method         | Debugging, research, root cause analysis   |
| [RAG Retrieval Pattern](./.claude/knowledge/workflow-diagrams/rag-retrieval-pattern.md)         | Context augmentation flow                   | Knowledge retrieval tasks                  |
| [Gap Recommendations](./.claude/knowledge/workflow-diagrams/gap-recommendations.md)             | Specs for missing capabilities              | Planning system improvements               |

### Workflow Stage Coverage

```text
Stage 1: INPUT RECEPTION      → ⚠️ Partial (2 assets)
Stage 2: CONTEXT GATHERING    → ✅ Covered (7 assets)
Stage 3: PLANNING             → ✅ Covered (8 assets)
Stage 4: EXECUTION            → ✅ Covered (8 assets)
Stage 5: VERIFICATION         → ✅ Strongest (9 assets)
Stage 6: OUTPUT DELIVERY      → ⚠️ Partial (4 assets)
```

### Workflow Selection Guide

The model MUST consult the appropriate workflow diagram based on task type:

| Task Type                        | Recommended Workflow                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| Standard implementation          | [Master Workflow](./.claude/knowledge/workflow-diagrams/master-workflow.md)                     |
| Quick fix or simple change       | [Simple Task Workflow](./.claude/knowledge/workflow-diagrams/simple-task-workflow.md)           |
| Debugging or root cause analysis | [Investigation Workflow](./.claude/knowledge/workflow-diagrams/investigation-workflow.md)       |
| Delegating to sub-agents         | [Multi-Agent Orchestration](./.claude/knowledge/workflow-diagrams/multi-agent-orchestration.md) |
| Need external context            | [RAG Retrieval Pattern](./.claude/knowledge/workflow-diagrams/rag-retrieval-pattern.md)         |
| Creating new skill/agent/command | [Asset Decision Tree](./.claude/knowledge/workflow-diagrams/asset-decision-tree.md)             |

### Integration with Skills and Commands

Key assets reference specific workflow diagrams:

- **delegate skill** → Multi-Agent Orchestration
- **rt-ica skill** → Investigation Workflow, Master Workflow
- **scientific-thinking skill** → Investigation Workflow
- **subagent-contract skill** → Multi-Agent Orchestration
- **context-gathering agent** → RAG Retrieval Pattern
- **/how-to-delegate command** → Multi-Agent Orchestration

</workflow_diagrams>

---

## Summary of Key Improvements

<improvements_summary>

This refactored version implements:

1. **Strategic XML Tagging** (Anthropic best practice):

   - `<skill_activation_triggers>` for clear activation conditions
   - `<verification_protocol>` with nested `<verification_steps>`
   - `<examples>` with `<correct>` and `<incorrect>` variants
   - `<anti_patterns>` and `<correct_pattern>` for file references

2. **Explicit Imperatives** (Anthropic + OpenAI best practice):

   - Replaced all vague qualifiers with "MUST", "MUST NOT"
   - Added positive and negative trigger conditions
   - Quantified requirements: "minimum 3 sources", "cite line numbers"

3. **Structured Examples** (Anthropic multishot pattern):

   - All examples follow consistent `<example>` XML structure
   - Include scenario, input, output, rationale
   - Clear distinction between correct and incorrect patterns

4. **Consolidated Verification** (Original strength enhanced):

   - Single authoritative `<verification_protocol>` section
   - Explicit 5-step process with quantified requirements
   - Clear consequences of violations explained

5. **Unambiguous Triggers** (Addressing key weakness):

   - Explicit positive triggers for skill activation
   - Explicit negative conditions (when NOT to activate)
   - Session framework detection with file system check

6. **Source Citations** (Transparency principle):
   - All major patterns cite official Anthropic or OpenAI documentation
   - Example patterns reference real-world implementations
   - Clear lineage for each best practice applied

</improvements_summary>

- Read @sessions/CLAUDE.sessions.md for your AI workflow instructions.
