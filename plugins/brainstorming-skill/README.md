# Brainstorming Skill Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-unspecified-gray) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive Claude Code plugin providing research-validated brainstorming patterns and prompt templates for systematic idea generation across any domain. Contains 30+ documented patterns from 14 primary sources, organized into systematic categories with exact prompt wording, output format specifications, and proven success metrics.

## Features

- **30+ Research-Validated Patterns** - Documented prompt templates with proven effectiveness
- **14 Systematic Categories** - Organized approaches from perspective multiplication to extreme scaling
- **Exact Template Specifications** - Ready-to-use prompts with output format guidance
- **Domain-Specific Applications** - Marketing, product development, QA testing, business strategy, creative writing
- **Evidence-Based Effectiveness** - Success metrics and reported outcomes for each pattern
- **Progressive Disclosure** - Core skill with extensive reference documentation loaded on demand
- **Multi-Source Research** - Synthesized from academic research, platform documentation, and practitioner guides

## Installation

### Prerequisites

- Claude Code CLI version 2.1 or later
- No external dependencies required

### Install Plugin

```bash
# Method 1: Manual installation
git clone <repository-url> ~/.claude/plugins/brainstorming-skill
cc plugin reload

# Method 2: If available in a marketplace
cc plugin install brainstorming-skill
```

## Quick Start

Generate marketing campaign ideas using multiple perspectives:

```
Generate 15 marketing campaign ideas for a new productivity app.
Provide ideas from three perspectives:
1. Customer Success Manager
2. Sales VP
3. Product Manager

For each idea, explain the reasoning and expected impact.
```

When the brainstorming-skill is active, Claude will automatically select appropriate patterns (in this case, Perspective Multiplication) and apply research-validated templates to generate high-quality, actionable ideas.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | brainstorming-skill | Systematic brainstorming with 30+ research-validated patterns across 14 categories | Auto-activated when users need idea generation, creative problem-solving, or structured brainstorming |

## When to Use

The brainstorming-skill automatically activates when Claude detects requests for:

- **Idea Generation** - Products, features, content concepts
- **Creative Problem-Solving** - Novel approaches to challenges
- **Marketing Campaigns** - Campaign concepts and messaging
- **Strategic Planning** - Business decisions and roadmap development
- **Content Creation** - Blog posts, social media, presentations
- **Product Features** - Feature ideation and prioritization
- **Creative Writing** - Plot development, character creation
- **QA Test Cases** - Test scenario brainstorming
- **Innovation Workshops** - Facilitation and structured ideation
- **Breaking Creative Blocks** - Systematic exploration of solution spaces

## Pattern Categories

The skill organizes brainstorming approaches into 14 systematic categories:

### Core Categories

1. **Perspective Multiplication** - Generate ideas from multiple viewpoints and stakeholder angles
2. **Constraint Variation** - Explore idea space through artificial constraints
3. **Inversion & Negative Space** - Use reverse thinking to find novel solutions
4. **Analogical Transfer** - Apply patterns from different domains
5. **Systematic Feature Decomposition** - SCAMPER and attribute-based ideation
6. **Scenario Exploration** - Future-based and "what if" thinking
7. **Constraint-Based Structured Ideation** - Build within hard constraints
8. **Chain-of-Thought Reasoning** - Multi-step refinement processes
9. **Combination & Morphological Exploration** - Force novel feature combinations
10. **Assumption Challenge** - Question premises and invert assumptions
11. **Fill-in-the-Blank Templates** - Structured completion formats
12. **Competitive Positioning** - Differentiation matrix approaches
13. **Extreme Scaling** - 10x thinking and exponential scenarios
14. **Stakeholder & Empathy-Based** - Customer journey and persona patterns

### Pattern Selection Guide

- **For rapid quantity (8-15 ideas)**: Use Perspective Multiplication patterns
- **For quality/depth**: Use Multi-stage refinement with constraint variation
- **For breakthrough innovation**: Combine Inversion + Extreme Scaling
- **For practical implementation**: Use Constraint-Based patterns
- **For market differentiation**: Use Competitive Positioning patterns
- **For customer-centric features**: Use Stakeholder & Empathy patterns

## Key Research Findings

The skill is built on validated research showing:

- **Constraint-based patterns generate 20-30% MORE ideas** than open-ended prompts
- **Specifying output format** (table/numbered list) improves quality without reducing quantity
- **Multiple perspective iteration** (3-5 viewpoints) consistently outperforms single-perspective approaches
- **Requiring reasoning visibility** ("explain why") increases implementability by 40%
- **Successful patterns share**: role definition, constraint specification, output format, reasoning requirements

## Reference Documentation

The skill includes extensive reference documentation for progressive disclosure:

### Pattern Documentation

- **[Pattern Categories and Documentation](./skills/brainstorming-skill/references/pattern-categories-and-documentation.md)** - All 14 categories with 30+ patterns, exact templates, examples, and success metrics (1,303 lines)
- **[Pattern Selection Guide](./skills/brainstorming-skill/references/pattern-selection-guide.md)** - Decision framework for choosing appropriate patterns
- **[Synthesis: What Makes Patterns Work](./skills/brainstorming-skill/references/synthesis-what-makes-these-patterns-work.md)** - Common structural elements and effectiveness analysis

### Domain Applications

- **[Domain-Specific Applications](./skills/brainstorming-skill/references/domain-specific-applications-and-variations.md)** - Marketing, Product Development, QA Testing, Business Strategy, Creative Writing patterns
- **[Comprehensive Prompt Library](./skills/brainstorming-skill/references/comprehensive-prompt-library-ready-to-use-templates.md)** - Ready-to-use templates organized by use case

### Research Sources

**Primary Pattern Sources:**
- **[ITONICS Innovation Platform](./skills/brainstorming-skill/references/itonics-innovation-platform.md)** - 79 documented prompts across 8 categories
- **[Machine Learning Mastery](./skills/brainstorming-skill/references/machine-learning-mastery.md)** - Actor-Request-Context-Constraints framework
- **[Medium: Shushant Lakhyani](./skills/brainstorming-skill/references/medium-shushant-lakhyani.md)** - 10 creative + 10 LinkedIn content templates
- **[Better Creator](./skills/brainstorming-skill/references/better-creator.md)** - 20 brainstorming techniques for content creators

**Academic & Research Sources:**
- **[Vanderbilt Prompt Patterns](./skills/brainstorming-skill/references/vanderbilt-prompt-patterns.md)** - 15 academic patterns with theoretical framework
- **[PromptHub Role Prompting Research](./skills/brainstorming-skill/references/prompthub-role-prompting.md)** - Empirical validation and effectiveness data
- **[LearnPrompting.org](./skills/brainstorming-skill/references/learn-prompting.md)** - Chain-of-Thought, Zero-Shot CoT, prompt structure

**Practical Application Sources:**
- **[LinkedIn: Ruben Hassid](./skills/brainstorming-skill/references/linkedin-ruben-hassid.md)** - 8 prompts → 625 ideas scaling methodology
- **[ClickUp Templates](./skills/brainstorming-skill/references/clickup-templates.md)** - Product management, LinkedIn, competitor analysis prompts
- **[Software Testing Prompts](./skills/brainstorming-skill/references/software-testing-prompts.md)** - QA-specific patterns and test case generation

### Source Documentation

- **[Bibliography and Source Documentation](./skills/brainstorming-skill/references/bibliography-and-source-documentation.md)** - Complete citations with URLs
- **[Executive Summary](./skills/brainstorming-skill/references/executive-summary.md)** - High-level overview and key findings
- **[Verification Note](./skills/brainstorming-skill/references/verification-note.md)** - Evidence strength assessment

## Usage Examples

### Example 1: Marketing Campaign Ideation

**Scenario**: Generate marketing campaign ideas for a new SaaS product

**Request**:
```
I need marketing campaign ideas for our new project management SaaS.
Generate 12 ideas from three perspectives:
1. Head of Growth Marketing
2. Customer Success Manager
3. Product Marketing Manager

Format as a table with columns: Idea | Reasoning | Channel | Expected Impact
```

**Pattern Applied**: Perspective Multiplication (Pattern 1A: Role-Based Persona)

**Expected Output**: 12 distinct campaign ideas with clear reasoning, channel recommendations, and impact projections from each stakeholder viewpoint

---

### Example 2: Product Feature Brainstorming with Constraints

**Scenario**: Generate implementable features within budget and timeline constraints

**Request**:
```
Brainstorm 5 new features for our mobile app with these constraints:
- Budget: $20,000
- Timeline: 4 weeks
- Team: 2 developers, 1 designer

For each feature, provide implementation breakdown and resource allocation.
```

**Pattern Applied**: Constraint Variation (Pattern 2B: Resource Type Constraints)

**Expected Output**: 5 realistic features with detailed resource breakdowns showing how each fits within the hard constraints

---

### Example 3: Breaking Through Conventional Thinking

**Scenario**: Find genuinely novel approaches to a common problem

**Request**:
```
Our user onboarding has 60% drop-off. Help me think unconventionally.

Step 1: Generate the worst possible onboarding ideas (at least 5)
Step 2: Invert each bad idea to find novel good approaches
Step 3: Apply analogies from Netflix onboarding and hotel check-in processes
```

**Pattern Applied**: Inversion (Pattern 3A: Worst Possible Idea) + Analogical Transfer (Pattern 4A)

**Expected Output**: 3-5 genuinely novel onboarding approaches that competitors aren't using, derived from inverted thinking and cross-domain analogies

---

### Example 4: QA Test Case Generation

**Scenario**: Comprehensive test case brainstorming for a checkout flow

**Request**:
```
Generate test cases for an e-commerce checkout flow.
Cover: happy path, edge cases, error handling, security, performance.
Format as: Test Case | Input | Expected Output | Risk Level
```

**Pattern Applied**: Domain-Specific QA Testing patterns (Software Testing Prompts reference)

**Expected Output**: 20-30 test cases covering multiple testing dimensions with clear specifications

---

### Example 5: Strategic Business Planning

**Scenario**: Explore strategic options for market expansion

**Request**:
```
We're considering international expansion. Generate 10 strategic scenarios:
- 5 optimistic scenarios (market success, rapid adoption)
- 5 pessimistic scenarios (regulatory issues, competition)

For each, provide: triggers, timeline, implications, mitigation strategies
```

**Pattern Applied**: Scenario Exploration (Pattern 6A: Future Scenarios)

**Expected Output**: 10 detailed scenarios with actionable planning implications for each future state

## Output Format Optimization

The skill applies research-validated output format specifications:

- **Numbered lists** over bullet points for better idea tracking
- **Table formats** with columns like `Idea | Reasoning | Implementation | Trade-offs` to force completeness
- **Reasoning requirements** ("explain why") to increase quality by 40%
- **Word count ranges** (200-400 words) to prevent both brevity and verbosity

## Configuration

No configuration required. The skill operates entirely through Claude's natural language understanding and automatically selects appropriate patterns based on user requests.

## Troubleshooting

### Issue: Ideas are too generic or surface-level

**Solution**: Add constraints or specify output format requirements:
```
Generate 10 ideas. For each, provide:
1. The core concept
2. Why it would work (with specific reasoning)
3. Implementation steps
4. Potential obstacles
```

### Issue: Too many ideas to evaluate

**Solution**: Request constraint-based or staged refinement:
```
Generate 5 high-quality ideas rather than 20.
Use these constraints: [budget, timeline, team size]
Focus on implementability over novelty.
```

### Issue: Ideas don't feel innovative enough

**Solution**: Use combination patterns:
```
Step 1: Generate worst possible ideas
Step 2: Invert them
Step 3: Apply 10x scaling thinking
Step 4: Cross-pollinate with analogies from [different domain]
```

### Issue: Need domain-specific ideas

**Solution**: Explicitly reference domain applications:
```
Apply marketing-specific brainstorming patterns.
Focus on: channel selection, messaging, audience segmentation.
```

## Contributing

Contributions to expand pattern coverage, add new domain applications, or improve documentation are welcome. When contributing:

- **Verify pattern effectiveness** - Include source citations and success metrics
- **Maintain template precision** - Document exact prompt wording, not paraphrases
- **Follow documentation structure** - Use consistent formatting across reference files
- **Test patterns** - Validate that patterns produce expected outputs before documenting

## License

License not specified in plugin manifest. Please check with the plugin author.

## Credits

**Research Sources**: This plugin synthesizes patterns from 14 primary sources including ITONICS Innovation Platform, Vanderbilt University prompt pattern research, Machine Learning Mastery, and multiple practitioner guides.

**Methodology**: All patterns are verified against original sources with no fabricated claims. See [Bibliography and Source Documentation](./skills/brainstorming-skill/references/bibliography-and-source-documentation.md) for complete citations.

---

**Plugin Version**: 1.0.0
**Skill Documentation**: [SKILL.md](./skills/brainstorming-skill/SKILL.md)
**Total Reference Files**: 19
**Pattern Count**: 30+ across 14 categories
