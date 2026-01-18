# Reference Documentation Guide

The clang-format skill includes comprehensive reference documentation organized for efficient lookup and learning. This guide explains how to navigate and use the 14 reference files.

## Documentation Structure

```
references/
├── index.md                          # Documentation hub and overview
├── quick-reference.md                # Complete configurations with explanations
├── cli-usage.md                      # Command-line usage and integrations
├── 01-alignment.md                   # Vertical alignment options
├── 02-breaking.md                    # Line breaking and wrapping rules
├── 03-braces.md                      # Brace placement styles
├── 04-indentation.md                 # Indentation rules
├── 05-spacing.md                     # Whitespace control
├── 06-includes.md                    # Include/import organization
├── 07-languages.md                   # Language-specific options
├── 08-comments.md                    # Comment formatting
├── 09-advanced.md                    # Penalty system and advanced features
└── complete/
    ├── clang-format-cli.md           # Full CLI reference
    └── clang-format-style-options.md # All 194 style options
```

## Quick Navigation Strategy

### For Common Tasks

| Task | Start Here | Then Go To |
|------|------------|------------|
| Create new config from scratch | `quick-reference.md` | Relevant category guide (01-09) |
| Understand a specific option | Category guide (01-09) | `complete/clang-format-style-options.md` |
| Fix unexpected formatting | `cli-usage.md` | Relevant category guide |
| Set up editor integration | `cli-usage.md` | Editor-specific docs |
| Learn command-line usage | `cli-usage.md` | `complete/clang-format-cli.md` |
| Browse all options | `complete/clang-format-style-options.md` | Category guides for details |

### For Questions by Topic

| Question Topic | Reference File |
|----------------|----------------|
| "How do I align variable declarations?" | `01-alignment.md` |
| "How do I control line breaks?" | `02-breaking.md` |
| "How do I change brace style?" | `03-braces.md` |
| "How do I configure indentation?" | `04-indentation.md` |
| "How do I adjust spacing around operators?" | `05-spacing.md` |
| "How do I organize #include directives?" | `06-includes.md` |
| "How do I configure Java/JavaScript differently?" | `07-languages.md` |
| "How do I control comment formatting?" | `08-comments.md` |
| "What's the penalty system?" | `09-advanced.md` |
| "What command-line options exist?" | `complete/clang-format-cli.md` |

## Reference File Summaries

### index.md - Documentation Hub

**Purpose**: Overview of the clang-format documentation and navigation guide.

**Contents**:
- Documentation organization
- Quick links to all reference files
- Recommended learning path
- Common use case routing

**When to use**: Starting point when you're new to the documentation or looking for a specific topic.

---

### quick-reference.md - Complete Working Configurations

**Purpose**: Provides 5-7 complete, working `.clang-format` configurations with detailed explanations.

**Contents**:
- Complete configuration examples
- Line-by-line explanations of each option
- Use cases for each configuration
- Comparison of different approaches

**When to use**:
- Creating a new configuration from scratch
- Learning by example
- Understanding how options work together
- Finding a starting point similar to your needs

**Example usage**:
```
"Show me a complete configuration for Google C++ style"
→ Claude references quick-reference.md
```

---

### cli-usage.md - Command-Line and Integration Guide

**Purpose**: Comprehensive guide to clang-format command-line usage, editor integrations, and CI/CD setups.

**Contents**:
- All command-line flags and options
- Exit codes and error handling
- Editor integration instructions (VS Code, Vim, Emacs, CLion, etc.)
- CI/CD examples (GitHub Actions, GitLab CI, Jenkins, etc.)
- Batch processing examples
- Troubleshooting common CLI issues

**When to use**:
- Setting up clang-format for the first time
- Configuring editor integration
- Adding formatting checks to CI/CD
- Troubleshooting formatting command issues
- Scripting bulk formatting operations

**Example usage**:
```
"How do I run clang-format on all files in my project?"
→ Claude references cli-usage.md for batch processing examples
```

---

### 01-alignment.md - Vertical Alignment Options

**Purpose**: Options for aligning code vertically (declarations, assignments, comments, etc.).

**Contents**:
- **Declaration alignment**: `AlignConsecutiveDeclarations`, `AlignConsecutiveBitFields`
- **Assignment alignment**: `AlignConsecutiveAssignments`
- **Macro alignment**: `AlignConsecutiveMacros`
- **Trailing comment alignment**: `AlignTrailingComments`
- **Operand alignment**: `AlignOperands`, `AlignAfterOpenBracket`
- **Array alignment**: `AlignArrayOfStructures`
- **Escaped newline alignment**: `AlignEscapedNewlines`

**When to use**:
- Want to vertically align declarations or assignments
- Aligning comments at the end of lines
- Aligning multi-line expressions or function arguments
- Aligning macro definitions

**Example usage**:
```
"How do I align variable declarations in columns?"
→ Claude consults 01-alignment.md for AlignConsecutiveDeclarations
```

---

### 02-breaking.md - Line Breaking and Wrapping Rules

**Purpose**: Options controlling when and how lines are broken and wrapped.

**Contents**:
- **Column limits**: `ColumnLimit`, `ColumnLimitExceptions`
- **Break positions**: `BreakBeforeBinaryOperators`, `BreakBeforeTernaryOperators`
- **String breaking**: `BreakStringLiterals`
- **Parameter breaking**: `BinPackParameters`, `BinPackArguments`, `AllowAllParametersOfDeclarationOnNextLine`
- **Template breaking**: `AlwaysBreakTemplateDeclarations`
- **Inheritance breaking**: `BreakInheritanceList`, `BreakConstructorInitializers`
- **Break penalties**: Various penalty options

**When to use**:
- Setting line length limits
- Controlling how long lines are wrapped
- Configuring function parameter wrapping
- Managing string literal breaking
- Adjusting template declaration formatting

**Example usage**:
```
"clang-format is breaking my function parameters weirdly"
→ Claude consults 02-breaking.md for parameter packing options
```

---

### 03-braces.md - Brace Placement Styles

**Purpose**: Options controlling brace placement (K&R, Allman, GNU, etc.).

**Contents**:
- **Brace styles**: `BreakBeforeBraces` (Attach, Linux, Mozilla, Stroustrup, Allman, Whitesmiths, GNU, WebKit, Custom)
- **Custom brace style**: `BraceWrapping` sub-options for fine control
- **Short blocks**: `AllowShortBlocksOnASingleLine`
- **Empty blocks**: Formatting for empty function bodies or blocks
- Examples for each brace style

**When to use**:
- Setting or changing brace placement style
- Understanding different brace conventions (K&R vs Allman, etc.)
- Fine-tuning brace placement for specific constructs
- Troubleshooting unexpected brace formatting

**Example usage**:
```
"I want opening braces on their own lines (Allman style)"
→ Claude consults 03-braces.md for BreakBeforeBraces: Allman
```

---

### 04-indentation.md - Indentation Rules

**Purpose**: Options controlling indentation for various code constructs.

**Contents**:
- **Basic indentation**: `IndentWidth`, `UseTab`, `TabWidth`
- **Special indentation**: `IndentCaseLabels`, `IndentGotoLabels`, `IndentPPDirectives`
- **Access specifier indentation**: `AccessModifierOffset`, `IndentAccessModifiers`
- **Function indentation**: `IndentWrappedFunctionNames`
- **Brace indentation**: `IndentBraces` (for Whitesmiths style)
- **Continuation indentation**: `ContinuationIndentWidth`
- **Namespace indentation**: `NamespaceIndentation`
- **Extern block indentation**: `IndentExternBlock`

**When to use**:
- Setting spaces vs tabs
- Adjusting indent width
- Controlling indentation of case labels, preprocessor directives
- Managing indentation in namespaces
- Configuring access modifier (public/private) indentation

**Example usage**:
```
"Use 4 spaces for indentation and don't indent case labels"
→ Claude consults 04-indentation.md for IndentWidth and IndentCaseLabels
```

---

### 05-spacing.md - Whitespace Control

**Purpose**: Options controlling spacing around operators, keywords, parentheses, brackets, etc.

**Contents**:
- **Pointer/reference alignment**: `PointerAlignment`, `ReferenceAlignment`, `DerivePointerAlignment`
- **Operator spacing**: `SpaceBeforeAssignmentOperators`, `BitFieldColonSpacing`
- **Parentheses spacing**: `SpaceBeforeParens`, `SpaceInEmptyParentheses`, `SpacesInParentheses`
- **Bracket spacing**: `SpaceBeforeSquareBrackets`, `SpacesInSquareBrackets`
- **Angle bracket spacing**: `SpaceAfterTemplateKeyword`, `SpacesInAngles`
- **Control flow spacing**: `SpaceBeforeRangeBasedForLoopColon`, `SpaceBeforeCtorInitializerColon`
- **Empty block spacing**: `SpaceInEmptyBlock`
- **Container literal spacing**: `SpacesInContainerLiterals`
- **C-style cast spacing**: `SpacesInCStyleCastParentheses`

**When to use**:
- Adjusting pointer/reference style (`int* ptr` vs `int *ptr`)
- Controlling spacing around operators
- Managing spacing inside parentheses or brackets
- Configuring template formatting
- Setting spacing around colons

**Example usage**:
```
"I want 'int* ptr' style instead of 'int *ptr'"
→ Claude consults 05-spacing.md for PointerAlignment: Left
```

---

### 06-includes.md - Include/Import Organization

**Purpose**: Options for sorting and organizing `#include` directives and imports.

**Contents**:
- **Include sorting**: `SortIncludes`, `IncludeBlocks`
- **Include categories**: `IncludeCategories` with regex patterns
- **Main include**: `IncludeIsMainRegex`, `IncludeIsMainSourceRegex`
- **Priority control**: Setting priority for different include groups
- Examples of include organization patterns (Google, LLVM, etc.)

**When to use**:
- Setting up automatic include sorting
- Organizing includes into groups (system, local, third-party)
- Preserving existing include order
- Troubleshooting include sorting issues
- Setting priority for specific header groups

**Example usage**:
```
"Sort my #include directives with system headers first"
→ Claude consults 06-includes.md for SortIncludes and IncludeBlocks
```

---

### 07-languages.md - Language-Specific Options

**Purpose**: Options specific to different programming languages (C++, Java, JavaScript, C#, Objective-C, etc.).

**Contents**:
- **Language selection**: `Language` field
- **C++ specific**: `Standard`, C++ dialect options
- **Java specific**: Java formatting options
- **JavaScript specific**: JavaScript formatting options
- **C# specific**: C# formatting options
- **Objective-C specific**: Objective-C block formatting
- **Protocol Buffers**: proto file formatting
- **Multi-language configs**: Using multiple `Language` blocks

**When to use**:
- Configuring different languages in a single project
- Setting language-specific formatting rules
- Understanding language-specific options
- Creating multi-language configurations

**Example usage**:
```
"Use 2-space indent for JavaScript but 4-space for C++"
→ Claude consults 07-languages.md for multi-language configuration
```

---

### 08-comments.md - Comment Formatting

**Purpose**: Options controlling comment formatting and reflow.

**Contents**:
- **Comment reflow**: `ReflowComments`
- **Comment pragmas**: `CommentPragmas` (comments to ignore)
- **Trailing comment alignment**: (see also 01-alignment.md)
- **Comment breaking**: How comments are wrapped
- **Special comment handling**: Doxygen, JavaDoc, etc.

**When to use**:
- Controlling automatic comment wrapping
- Preserving special comment formats
- Aligning trailing comments
- Excluding certain comments from formatting

**Example usage**:
```
"Don't reflow my comments"
→ Claude consults 08-comments.md for ReflowComments: false
```

---

### 09-advanced.md - Penalty System and Advanced Features

**Purpose**: Advanced options including the penalty system, raw string formatting, and experimental features.

**Contents**:
- **Penalty system**: `PenaltyBreakAssignment`, `PenaltyBreakBeforeFirstCallParameter`, etc.
  - How penalties work
  - Which penalty affects what formatting decision
  - Adjusting penalties to influence formatting
- **Raw strings**: `RawStringFormats` for raw literal formatting
- **Macro handling**: `MacroBlockBegin`, `MacroBlockEnd`
- **Experimental features**: Features not yet stable
- **Sorting**: `SortUsingDeclarations`
- **Qualifiers**: `QualifierAlignment`, `QualifierOrder`

**When to use**:
- Fine-tuning formatting when multiple valid options exist
- Understanding why clang-format chooses specific formatting
- Configuring raw string formatting (C++11, Python, etc.)
- Using advanced or experimental features
- Adjusting const/volatile qualifier positions

**Example usage**:
```
"clang-format keeps choosing the longer line - how do I control this?"
→ Claude consults 09-advanced.md for penalty system explanation
```

---

### complete/clang-format-cli.md - Full CLI Reference

**Purpose**: Complete reference for all command-line flags and options.

**Contents**:
- All CLI flags with detailed descriptions
- Input/output options
- Style specification methods
- Range formatting options
- Dump options for debugging
- Exit codes
- Environment variables
- Usage examples

**When to use**:
- Looking up specific command-line flag
- Understanding all available CLI options
- Scripting clang-format operations
- Debugging clang-format behavior
- Learning advanced CLI usage

**Example usage**:
```
"What flags can I pass to clang-format?"
→ Claude consults complete/clang-format-cli.md for comprehensive list
```

---

### complete/clang-format-style-options.md - All 194 Style Options

**Purpose**: Exhaustive reference of every clang-format style option with examples.

**Contents**:
- All 194 style options in alphabetical order
- Type and valid values for each option
- Brief description
- Example before/after for each option
- Related options
- Version introduced

**When to use**:
- Looking up a specific option by name
- Understanding all options in a category
- Exploring all available options
- Detailed examples for complex options
- Version compatibility checking

**Example usage**:
```
"What does AlignConsecutiveAssignments actually do?"
→ Claude consults complete/clang-format-style-options.md for detailed explanation with examples
```

---

## Recommended Learning Paths

### Path 1: Quick Start (30 minutes)

For users who want to get started immediately:

1. **quick-reference.md** - Find configuration closest to your needs
2. **cli-usage.md** - Learn basic commands
3. **Templates** (assets/configs/) - Copy appropriate template
4. **One category guide** (based on first customization need)

### Path 2: Comprehensive Understanding (2-3 hours)

For users who want to deeply understand clang-format:

1. **index.md** - Overview
2. **quick-reference.md** - See examples of complete configs
3. **03-braces.md** - Understand brace styles (affects overall structure)
4. **04-indentation.md** - Understand indentation (fundamental concept)
5. **05-spacing.md** - Understand spacing (frequent customization)
6. **02-breaking.md** - Understand line breaking (complex but important)
7. **01-alignment.md** - Understand alignment (optional but useful)
8. **06-includes.md, 07-languages.md, 08-comments.md** - As needed
9. **09-advanced.md** - For fine-tuning
10. **cli-usage.md** - Integration and automation

### Path 3: Problem-Driven Learning (Variable time)

For users solving specific problems:

1. Identify the formatting aspect causing the issue
2. Go directly to relevant category guide (01-09)
3. Find the relevant option
4. Test in minimal configuration
5. Consult complete reference if needed for edge cases

### Path 4: Configuration Review (30 minutes)

For users reviewing or inheriting an existing configuration:

1. **complete/clang-format-style-options.md** - Look up unfamiliar options
2. **Category guides (01-09)** - Understand options in context
3. **quick-reference.md** - Compare with standard configurations
4. **cli-usage.md** - Understand how config is used

## Tips for Effective Use

### When Asking Claude Questions

Be specific about:
- **Context**: "In my C++ project..."
- **Current behavior**: "clang-format is doing X..."
- **Desired behavior**: "I want Y instead..."
- **Formatting aspect**: "...with my brace placement/spacing/alignment..."

This helps Claude route to the most relevant reference documentation.

### When Troubleshooting

1. **Isolate the issue** - Create minimal example
2. **Identify the category** - Braces? Spacing? Breaking?
3. **Consult category guide** - Find relevant options
4. **Test options individually** - Create minimal config with one option
5. **Combine and iterate** - Build up complete solution

### When Learning Options

1. **Start with examples** in quick-reference.md
2. **Read category overview** in relevant guide (01-09)
3. **Test each option** individually
4. **Check complete reference** for edge cases
5. **Combine options** progressively

## Reference File Access

All reference files are bundled with the skill. Claude automatically accesses them based on your questions. You can also:

**View directly** (if you've installed the plugin):
```bash
ls ~/.claude/plugins/clang-format/skills/clang-format/references/
cat ~/.claude/plugins/clang-format/skills/clang-format/references/03-braces.md
```

**Ask Claude to show you**:
```
"Show me the braces reference documentation"
"What's in the quick reference?"
"Explain the contents of 02-breaking.md"
```

## Keeping References Updated

These references are based on:
- clang-format 19.x (current as of January 2026)
- LLVM documentation: https://clang.llvm.org/docs/ClangFormat.html
- LLVM source code: https://github.com/llvm/llvm-project

For the absolute latest information, consult the official LLVM documentation. Claude will note when referencing may be outdated for your specific clang-format version.

## Summary

The reference documentation is organized for efficient lookup:

- **Quick tasks** → quick-reference.md, cli-usage.md
- **Specific questions** → Category guides (01-09)
- **Comprehensive learning** → Complete references
- **Problem solving** → Category guides + complete references

Claude automatically selects the most relevant documentation based on your questions, but understanding this organization helps you ask more targeted questions and learn more efficiently.
