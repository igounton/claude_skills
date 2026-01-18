# Skill Reference

Complete reference for the clang-format Configuration skill.

## Overview

The clang-format Configuration skill provides intelligent assistance for configuring the clang-format code formatting tool. It combines ready-to-use templates, code analysis capabilities, and comprehensive reference documentation to streamline formatting configuration.

## Skill Details

**Location**: `skills/clang-format/SKILL.md`

**Name**: clang-format Configuration

**Description**: The skill is automatically invoked when any of these triggers occur:
1. User mentions "clang-format" or ".clang-format"
2. User requests analyzing code style/formatting patterns/conventions
3. User requests creating/modifying/generating formatting configuration
4. User troubleshoots formatting behavior or unexpected results
5. User asks about brace styles/indentation/spacing/alignment/line breaking/pointer alignment
6. User wants to preserve existing style/minimize whitespace changes/reduce formatting diffs/codify dominant conventions

**User Invocable**: Yes (auto-invoked based on triggers)

**Allowed Tools**: All tools (Read, Write, Edit, Bash, Grep, Glob, etc.)

**Model**: Inherits from session default

## When to Use

Use this skill whenever you need to:

- **Create new configurations** - Start a project with a specific coding style
- **Analyze existing code** - Generate configurations that match current formatting patterns
- **Minimize disruption** - Introduce clang-format with minimal whitespace changes
- **Troubleshoot formatting** - Understand why clang-format produces specific results
- **Set up integrations** - Configure editors or git hooks for automatic formatting
- **Learn clang-format options** - Understand the 194 available style options
- **Configure CI/CD** - Add formatting checks to continuous integration pipelines

## Activation

The skill activates automatically based on natural language triggers. You don't need to explicitly invoke it.

**Example activations**:
```
"Set up clang-format for my C++ project"
→ Trigger 1: Explicit mention + Trigger 3: Configuration operation

"Analyze my code style and create a matching config"
→ Trigger 2: Code style analysis

"Why is clang-format adding extra spaces around my operators?"
→ Trigger 4: Troubleshooting + Trigger 5: Spacing inquiry

"I want to format my code but keep changes minimal"
→ Trigger 6: Minimal-disruption request
```

## Workflow Routing

The skill uses intelligent routing based on which trigger activated it:

### Trigger 1: Explicit clang-format mention
- Routes to relevant reference documentation
- For specific options: Consults category guides (references/01-09.md)
- For complete reference: Uses references/complete/clang-format-style-options.md
- For CLI usage: References references/cli-usage.md

### Trigger 2: Code style analysis request
Follows systematic analysis workflow:
1. Examine code samples (braces → indentation → spacing → breaking → alignment)
2. Map patterns to closest template in assets/configs/
3. Generate configuration hypotheses as temporary files
4. Verify impact using `clang-format` with diff analysis
5. Measure impact with weighted scoring:
   - Line count changes (weight: 10)
   - In-line whitespace changes (weight: 1)
   - Lower score = better (less disruptive)
6. Iterate to minimize impact score
7. Report results with comparison table and example diffs
8. Await user approval before finalizing

### Trigger 3: Configuration file operations
- Creating new: Uses templates from assets/configs/
- Modifying existing: Reads current config, identifies needed changes
- Generating from code: Uses Trigger 2 workflow (analysis)

### Trigger 4: Formatting behavior investigation
Follows troubleshooting workflow:
1. Verify configuration detection with `--dump-config`
2. Identify affected category
3. Consult relevant references/0X.md guide
4. Test isolated options with minimal config

### Trigger 5: Style option inquiries
- Maps question to category:
  - Braces → 03-braces.md
  - Indentation → 04-indentation.md
  - Spacing → 05-spacing.md
  - Alignment → 01-alignment.md
  - Breaking → 02-breaking.md
- Provides examples from quick-reference.md

### Trigger 6: Minimal-disruption requests
- Uses Trigger 2 workflow (analysis) with emphasis on impact minimization
- Starts from closest template
- Tests on representative samples
- Documents which patterns were preserved vs normalized

## Bundled Resources

The skill includes three categories of resources:

### 1. Configuration Templates (assets/configs/)

Seven production-ready `.clang-format` files optimized for common scenarios. See [Templates Guide](./templates.md) for detailed documentation.

### 2. Integration Scripts (assets/integrations/)

Three scripts for editor and git integration:
- `pre-commit` - Git hook for automatic formatting
- `vimrc-clang-format.vim` - Vim format-on-save
- `emacs-clang-format.el` - Emacs integration

See [Integrations Guide](./integrations.md) for detailed documentation.

### 3. Reference Documentation (references/)

14 reference files organized by category:
- Quick reference and CLI usage
- 9 category guides (alignment, breaking, braces, indentation, spacing, includes, languages, comments, advanced)
- 2 complete references (all options, full CLI)

See [References Guide](./references-guide.md) for navigation.

## Key Workflows

### Creating New Configuration from Template

1. Identify requirements (style guide, team preferences, language)
2. Select closest template from assets/configs/
3. Copy template to project root as `.clang-format`
4. Test formatting: `clang-format --dry-run file.cpp`
5. Customize specific options using references/01-09.md
6. Verify changes: `clang-format file.cpp | diff - file.cpp`

**Example interaction**:
```
"Set up clang-format for my project using Google C++ style with 4-space indentation"
```

### Analyzing Existing Code Style

1. Examine code samples for formatting patterns
2. Identify key characteristics (braces, indentation, spacing, breaking, alignment)
3. Map patterns to closest base style
4. Start with matching template
5. Override specific options to match observed patterns
6. Test on representative samples with impact measurement
7. Iterate until formatting matches existing style

**Example interaction**:
```
"Analyze my codebase and create a clang-format config that matches the existing style with minimal changes"
```

### Setting Up Editor Integration

For Vim, Emacs, or other editors:
1. Copy relevant integration script
2. Add to editor configuration
3. Restart or reload editor
4. Test on sample file

**Example interaction**:
```
"Set up clang-format to run automatically when I save files in Vim"
```

### Setting Up Git Hook

For pre-commit framework or manual hooks:
1. Configure in `.pre-commit-config.yaml` or
2. Copy manual hook script to `.git/hooks/pre-commit`
3. Make executable and test

**Example interaction**:
```
"Add a git hook to format code before commits"
```

### Troubleshooting Formatting Issues

When formatting produces unexpected results:
1. Verify configuration detection: `clang-format --dump-config file.cpp`
2. Identify affected formatting category
3. Consult relevant category guide
4. Test isolated options with minimal config

**Example interaction**:
```
"clang-format is adding weird line breaks in my function parameters. How do I fix this?"
```

## Impact Measurement System

The skill's code analysis workflow uses a weighted scoring system to quantify formatting changes:

**Formula**: `Impact Score = (line_changes × 10) + (whitespace_changes × 1)`

**Rationale**:
- **Line changes** (weight: 10) - Adding/removing lines affects:
  - Git blame history
  - Merge conflict likelihood
  - Rebase complexity
  - Code review clarity
- **Whitespace changes** (weight: 1) - Spacing within lines has minimal impact:
  - Doesn't affect line numbers
  - Easier to review
  - Fewer merge conflicts

**Goal**: Minimize score to reduce disruption when introducing clang-format to existing codebases.

**Example**:
```
Configuration A: 3 line changes, 15 whitespace changes
Score = (3 × 10) + (15 × 1) = 45

Configuration B: 0 line changes, 25 whitespace changes
Score = (0 × 10) + (25 × 1) = 25 ⭐ BETTER

Configuration B is preferred despite more total changes because line
changes have greater impact on git history and collaboration.
```

## Testing Configurations

Common commands for testing configurations:

```bash
# Preview changes without modifying file
clang-format --dry-run file.cpp

# Show diff of proposed changes
clang-format file.cpp | diff - file.cpp

# Test with specific config file
clang-format --style=file:/path/to/.clang-format file.cpp

# Apply formatting to file
clang-format -i file.cpp

# Format entire project
find src include -name '*.cpp' -o -name '*.h' | xargs clang-format -i

# Check formatting in CI (fail on violations)
clang-format --dry-run --Werror src/**/*.{cpp,h}
```

## Key Concepts

### Base Styles

Predefined configurations that provide starting points:
- LLVM (default)
- Google
- Chromium
- Mozilla
- WebKit
- Microsoft
- GNU

Use with `BasedOnStyle: Google` in your configuration, then override specific options.

### Multi-Language Support

Single `.clang-format` file can configure different languages separately using `Language:` key. Supports:
- C/C++
- Java
- JavaScript
- C#
- Objective-C
- Protocol Buffers
- TableGen

### Penalty System

clang-format uses penalties to choose between formatting alternatives. Higher penalty values discourage specific choices. Useful for fine-tuning when multiple valid formats exist.

### Progressive Refinement

Recommended approach:
1. Start with template closest to requirements
2. Customize incrementally
3. Test frequently on representative code samples
4. Measure impact of changes
5. Iterate until optimal

## Navigation Strategy

For most tasks, follow this progression:

1. **Start with templates** - Browse assets/configs/ for ready-to-use configurations
2. **Quick reference** - Check references/quick-reference.md for complete configurations with explanations
3. **Category guides** - Consult references/01-09.md for specific option categories
4. **CLI usage** - Reference references/cli-usage.md for command-line and integration details
5. **Complete reference** - Use references/complete/ for exhaustive option documentation

When analyzing code or troubleshooting, identify the formatting aspect (braces, spacing, alignment, etc.) and jump directly to the relevant category guide.

## Hooks

The skill does not configure any hooks. All operations are executed when Claude responds to formatting-related requests.

## Reference Files

The skill includes a comprehensive reference library. See [References Guide](./references-guide.md) for complete documentation of available references and how to use them effectively.
