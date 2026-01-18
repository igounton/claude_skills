# Reference Files Guide

The prompt-optimization-claude-45 skill includes comprehensive reference documentation that Claude can access on-demand to provide accurate, up-to-date information about Claude 4.5 features and best practices.

## Available References

### 1. What's New in Claude 4.5

**Location**: `skills/prompt-optimization-claude-45/whats-new-claude-4.5.md`

**Purpose**: Complete guide to Claude 4.5 model improvements and new API features.

**Contents**:

#### Claude Opus 4.5 Highlights
- Maximum intelligence with practical performance
- Effort parameter for controlling response thoroughness
- Enhanced computer use with zoom capability
- Thinking block preservation across conversations
- More accessible pricing than previous Opus models

#### Claude Sonnet 4.5 Highlights
- Best coding model (SWE-bench Verified performance)
- Extended autonomous operation (hours of independent work)
- Context awareness with token usage tracking
- Enhanced parallel tool usage
- Concise, direct communication style
- Creative content generation excellence

#### Claude Haiku 4.5 Highlights
- Near-frontier intelligence at blazing speed
- First Haiku model with extended thinking
- Context awareness
- 2x faster than Sonnet 4 at 1/3 the cost
- Strong coding and tool use capabilities

#### New API Features (Beta)
- Programmatic tool calling - Reduce latency with code execution
- Tool search tool - Work with hundreds/thousands of tools
- Effort parameter - Control response thoroughness (Opus 4.5 only)
- Tool use examples - Provide concrete examples for complex tools
- Memory tool - Store information outside context window
- Context editing - Intelligent context management

**When to Use**: Reference this when optimizing prompts for specific Claude 4.5 models, understanding new capabilities, or applying model-specific best practices.

**Example Query**:

```
What are the key differences between Sonnet 4.5 and Opus 4.5?
How does the effort parameter work?
What is programmatic tool calling?
```

### 2. Context Windows

**Location**: `skills/prompt-optimization-claude-45/context-windows.md`

**Purpose**: Understanding context window management, token budgets, and extended thinking behavior.

**Contents**:

#### Core Concepts
- Context window definition and behavior
- Progressive token accumulation
- 200K token standard capacity
- Input-output flow patterns

#### Extended Thinking
- How thinking blocks affect token counts
- Automatic stripping of previous thinking blocks
- Token management during multi-turn conversations
- Technical implementation details

#### Extended Thinking with Tool Use
- Token calculation during tool use cycles
- Thinking block preservation requirements
- Cryptographic signature verification
- Interleaved thinking in Claude 4 models

#### 1M Token Context Window (Beta)
- Availability (Sonnet 4 and 4.5, usage tier 4+)
- Beta header configuration
- Premium pricing structure
- Rate limits and considerations

#### Context Awareness
- Token budget tracking in Sonnet 4.5 and Haiku 4.5
- Real-time capacity updates
- Benefits for long-running agents
- Multi-context-window workflows

**When to Use**: Reference this when optimizing for token efficiency, understanding context limitations, or designing long-running agent workflows.

**Example Query**:

```
How do thinking blocks affect context window?
What is context awareness in Sonnet 4.5?
How does the 1M token context window work?
```

## Progressive Disclosure Pattern

The skill uses progressive disclosure to keep the main SKILL.md focused while providing deep dives through reference files.

**Benefits**:

1. **Token Efficiency**: Main skill instructions stay under 500 lines
2. **On-Demand Loading**: Claude loads references only when needed
3. **Maintainability**: Updates to specific features isolated in reference files
4. **Clarity**: Core patterns in main skill, details in references

## How Claude Uses References

### Automatic Discovery

When you ask questions about:
- Claude 4.5 features → Loads `whats-new-claude-4.5.md`
- Context windows or token management → Loads `context-windows.md`
- Model-specific optimizations → Loads appropriate reference

### Manual Loading

You can explicitly request reference content:

```
@prompt-optimization-claude-45
Load the Claude 4.5 reference and explain the effort parameter
```

Or:

```
Read the context windows reference and explain how thinking blocks are managed
```

## Reference Update Cycle

References are based on official Anthropic documentation:

| Reference | Source | Last Updated |
|-----------|--------|--------------|
| whats-new-claude-4.5.md | [Anthropic Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5) | 2026-01-18 |
| context-windows.md | [Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows) | 2026-01-18 |

**Update Strategy**: References are updated when Anthropic releases:
- New model versions (4.6, 5.0, etc.)
- Breaking API changes
- Major feature additions
- Best practice revisions

## Using References in Optimization

### Example 1: Model-Specific Optimization

**User Query**:

```
Optimize this CLAUDE.md for Claude Sonnet 4.5
```

**Claude's Process**:
1. Activates prompt-optimization-claude-45 skill
2. Loads `whats-new-claude-4.5.md` for Sonnet 4.5 features
3. Applies model-specific patterns:
   - Direct action language
   - Parallel tool usage structure
   - Concise communication style
   - Context awareness guidance
4. Returns optimized CLAUDE.md with Sonnet 4.5 best practices

### Example 2: Token Budget Planning

**User Query**:

```
How should I structure my agent instructions to work within the 200K context window?
```

**Claude's Process**:
1. Activates prompt-optimization-claude-45 skill
2. Loads `context-windows.md` for token management patterns
3. Applies compression techniques:
   - Structural templates for protocols
   - Removal of verbose phrasing
   - Progressive disclosure recommendations
4. Suggests token-efficient architecture

### Example 3: Feature-Specific Guidance

**User Query**:

```
How do I use the new programmatic tool calling feature in my agent?
```

**Claude's Process**:
1. Activates prompt-optimization-claude-45 skill
2. Loads `whats-new-claude-4.5.md` for API features
3. Extracts programmatic tool calling details:
   - Beta header requirement
   - allowed_callers configuration
   - Benefits (latency, token efficiency)
4. Provides implementation guidance with examples

## Adding Custom References

You can extend the skill with project-specific references:

### Step 1: Create Reference File

```bash
# In your project
mkdir -p .claude/skills/prompt-optimization-custom/references/
touch .claude/skills/prompt-optimization-custom/references/project-patterns.md
```

### Step 2: Link from Skill

```markdown
# In SKILL.md
For project-specific patterns, see [Project Patterns](./references/project-patterns.md)
```

### Step 3: Reference in Prompts

```
Apply both standard Claude 4.5 optimizations and our project-specific patterns
```

## Best Practices

### When Optimizing Prompts

1. **Start with Core Principles**: Apply main skill guidance first
2. **Reference for Specifics**: Load references for model-specific or feature-specific details
3. **Verify Against Official Docs**: References cite sources for verification
4. **Update Periodically**: Check for reference updates quarterly

### When Writing Custom References

1. **Follow Progressive Disclosure**: Keep main skill focused, details in references
2. **Cite Sources**: Include URLs and access dates
3. **Use Markdown Links**: `[Text](./path)` for navigation
4. **Include Examples**: Show concrete usage patterns
5. **Maintain Consistency**: Match formatting of existing references

## FAQ

**Q: How do I know which reference to use?**

A: Ask Claude directly. The skill automatically determines the appropriate reference based on your query.

**Q: Can I use these references without the skill?**

A: Yes! Reference files are standard Markdown and can be read directly. However, the skill provides context on how to apply the information.

**Q: Do references work offline?**

A: Yes, reference files are local. However, they may reference online Anthropic documentation for latest updates.

**Q: How often should references be updated?**

A: Check quarterly or when Anthropic announces major releases. The skill includes source URLs for easy verification.

## Related Documentation

- [Main README](../README.md) - Installation and overview
- [Usage Examples](./examples.md) - Real-world optimization scenarios
- [Quick Reference](./quick-reference.md) - Fast lookup of patterns

## Sources

All reference files are derived from official Anthropic documentation:

- [Claude 4.5 Models](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5)
- [Context Windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [Prompt Engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering)
- [Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)

Last updated: 2026-01-18
