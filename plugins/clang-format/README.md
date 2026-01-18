# clang-format Configuration Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A Claude Code plugin that provides intelligent clang-format configuration assistance with ready-to-use templates, code style analysis, integration scripts, and comprehensive reference documentation.

## Features

- **7 Ready-to-Use Templates** - Production-ready `.clang-format` configurations for common coding styles (Google, Linux Kernel, Microsoft, Modern C++17/20, and more)
- **Intelligent Code Style Analysis** - Analyze existing codebases and generate minimal-impact configurations that match current formatting patterns
- **Impact Measurement System** - Quantify formatting changes with weighted scoring to minimize conflicts during adoption
- **Editor Integration** - Pre-configured setups for Vim and Emacs with format-on-save
- **Git Hook Integration** - Compatible with pre-commit/prek frameworks and manual git hooks
- **Comprehensive Reference Documentation** - 14 organized reference files covering all 194 clang-format style options
- **Troubleshooting Workflows** - Systematic approaches to diagnose and resolve formatting issues

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- clang-format installed on your system (version 10.0 or higher recommended)
  ```bash
  # Ubuntu/Debian
  sudo apt install clang-format

  # macOS
  brew install clang-format

  # Verify installation
  clang-format --version
  ```

### Install Plugin

#### Method 1: Using Claude Code Plugin System (Recommended)

```bash
# If available in a marketplace
cc plugin marketplace add <marketplace-url>
cc plugin install clang-format
```

#### Method 2: Manual Installation

```bash
# Clone or copy to plugins directory
cp -r /path/to/clang-format ~/.claude/plugins/clang-format

# Reload plugins
cc plugin reload
```

## Quick Start

### Use Case 1: Start a New Project with Google C++ Style

```bash
# Let Claude help you set up formatting
```

Then in Claude Code:
```
Set up clang-format for my project using Google C++ style with 4-space indentation
```

Claude will:
1. Copy the appropriate template to your project
2. Test it on your files
3. Set up editor integration if requested

### Use Case 2: Match Existing Code Style

```bash
# Analyze existing code and generate matching configuration
```

In Claude Code:
```
Analyze my codebase at ./src and create a clang-format config that matches the existing style with minimal changes
```

Claude will:
1. Examine your code for formatting patterns
2. Generate multiple configuration hypotheses
3. Test each configuration and measure impact (line changes, whitespace changes)
4. Present the best option with impact scores and example diffs
5. Create the configuration after your approval

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | clang-format Configuration | Configure clang-format with templates, analysis, and troubleshooting | Auto-invoked when discussing clang-format, code style, or formatting |

## Usage

### Skills

The plugin provides one comprehensive skill that handles all clang-format configuration tasks:

**clang-format Configuration** - Automatically activated when you:
- Mention "clang-format" or ".clang-format"
- Request code style or formatting analysis
- Ask about creating/modifying formatting configurations
- Troubleshoot formatting behavior
- Inquire about brace styles, indentation, spacing, alignment, or line breaking
- Want to preserve existing style with minimal changes

The skill provides intelligent routing to appropriate workflows based on your request.

### Configuration Templates

Seven production-ready templates included:

1. **google-cpp-modified.clang-format** - Google C++ style with 4-space indent, 120 column limit
2. **linux-kernel.clang-format** - Linux kernel coding standards (tabs, K&R braces)
3. **microsoft-visual-studio.clang-format** - Microsoft/Visual Studio conventions
4. **modern-cpp17-20.clang-format** - Modern C++17/20 style with contemporary idioms
5. **compact-dense.clang-format** - Compact style for space-constrained environments
6. **readable-spacious.clang-format** - Spacious style prioritizing readability
7. **multi-language.clang-format** - Multi-language configuration (C++, JavaScript, Java)

### Integration Scripts

Three integration scripts for seamless workflow integration:

1. **pre-commit** - Git hook for automatic formatting of staged files (compatible with pre-commit/prek frameworks)
2. **vimrc-clang-format.vim** - Vim configuration for format-on-save
3. **emacs-clang-format.el** - Emacs configuration for clang-format integration

### Reference Documentation

Comprehensive documentation organized by category:

- **Quick Reference** - Complete working configurations with explanations
- **CLI Usage** - Command-line usage, editor setup, CI/CD integration
- **Option Categories** - 9 detailed guides covering alignment, breaking, braces, indentation, spacing, includes, languages, comments, and advanced features
- **Complete Reference** - Exhaustive documentation of all 194 style options and full CLI reference

## Configuration

The skill operates without additional configuration. It automatically accesses:

- **Configuration Templates** - Located in `skills/clang-format/assets/configs/`
- **Integration Scripts** - Located in `skills/clang-format/assets/integrations/`
- **Reference Documentation** - Located in `skills/clang-format/references/`

All resources are bundled with the plugin and available on-demand.

## Examples

### Example 1: Set Up Formatting for a New C++ Project

**Scenario**: You're starting a new C++ project and want to use Google style with some customizations.

**Interaction**:
```
I'm starting a new C++ project. Set up clang-format with Google style,
4-space indentation, and 120 character line limit.
```

**Claude's Actions**:
1. Selects `google-cpp-modified.clang-format` template (already has these settings)
2. Copies to your project root as `.clang-format`
3. Tests on sample files if available
4. Offers to set up editor integration

**Result**: Your project has a working `.clang-format` configuration ready to use.

---

### Example 2: Match Existing Code Style

**Scenario**: You have an existing codebase with inconsistent formatting and want to introduce clang-format without massive diffs.

**Interaction**:
```
Analyze my codebase at ./src/core and create a clang-format config that
matches the existing style. I want minimal changes to reduce conflicts.
```

**Claude's Actions**:
1. Examines code files for formatting patterns (braces, indentation, spacing, alignment)
2. Identifies dominant patterns (e.g., Allman braces, 2-space indent, spaces around operators)
3. Generates 3-5 configuration hypotheses from closest templates
4. Tests each configuration on representative files
5. Measures impact using weighted scoring:
   - Line count changes (weight: 10) - major impact on diffs
   - Whitespace changes (weight: 1) - minor impact
6. Reports results:
   ```
   Configuration Hypothesis Results:

   Hypothesis 1 (readable-spacious base): Score 45
     - 3 line changes, 15 whitespace changes
     - Matches: Allman braces, 2-space indent
     - Mismatches: Adds spaces in empty blocks

   Hypothesis 2 (google-cpp modified): Score 120
     - 12 line changes, 0 whitespace changes
     - Mismatches: Wrong brace style, wrong indent

   Hypothesis 3 (readable-spacious + tweaks): Score 15 ⭐ RECOMMENDED
     - 0 line changes, 15 whitespace changes
     - Matches: All major patterns
     - Only normalizes spacing around operators

   Example diff for Hypothesis 3:
   [Shows specific before/after examples]

   Ready to test: clang-format --style=/tmp/myproject/hypothesis_3.clang-format src/file.cpp | diff - src/file.cpp
   ```
7. Waits for your approval before creating final `.clang-format`

**Result**: Minimal-impact configuration that respects existing style while enforcing consistency.

---

### Example 3: Troubleshoot Unexpected Formatting

**Scenario**: clang-format is formatting your code unexpectedly after applying a configuration.

**Interaction**:
```
clang-format is adding weird line breaks in my function parameters.
How do I fix this?
```

**Claude's Actions**:
1. Identifies issue category: line breaking (references/02-breaking.md)
2. Asks for example code or reads provided file
3. Runs `clang-format --dump-config` to verify active configuration
4. Identifies relevant options:
   - `AllowAllParametersOfDeclarationOnNextLine`
   - `BinPackParameters`
   - `AlignAfterOpenBracket`
5. Explains each option's effect with examples
6. Suggests configuration adjustments
7. Provides test command to verify fix

**Result**: You understand why the formatting occurred and how to configure it to your preference.

---

### Example 4: Set Up CI/CD Formatting Checks

**Scenario**: You want to enforce code formatting in your CI pipeline.

**Interaction**:
```
Add clang-format checks to my GitHub Actions CI pipeline
```

**Claude's Actions**:
1. References `references/cli-usage.md` for CI examples
2. Proposes GitHub Actions workflow:
   ```yaml
   - name: Check code formatting
     run: |
       clang-format --dry-run --Werror src/**/*.{cpp,h} include/**/*.h
   ```
3. Explains options:
   - `--dry-run`: Don't modify files
   - `--Werror`: Treat warnings as errors (fail build)
4. Suggests adding badge to README
5. Documents formatting requirements for contributors

**Result**: CI pipeline enforces formatting standards automatically.

---

### Example 5: Set Up Format-on-Save in Vim

**Scenario**: You want Vim to automatically format your C++ files on save.

**Interaction**:
```
Set up clang-format to run automatically when I save files in Vim
```

**Claude's Actions**:
1. Copies content from `assets/integrations/vimrc-clang-format.vim`
2. Explains the configuration:
   ```vim
   " Auto-format on save for C/C++/Java
   autocmd BufWritePre *.cpp,*.h,*.c,*.java silent! execute '!clang-format -i %'
   ```
3. Guides you to add to `.vimrc`
4. Suggests testing with a sample file
5. Offers to set up similar integration for other editors

**Result**: Vim automatically formats code on save using your `.clang-format` configuration.

## Troubleshooting

### Configuration Not Detected

**Problem**: clang-format isn't using your `.clang-format` file.

**Solution**:
```bash
# Verify configuration detection
clang-format --dump-config src/file.cpp

# Check search path (looks up from file to root)
# Ensure .clang-format is in or above your source directory
```

### Unexpected Formatting Results

**Problem**: Formatting doesn't match expectations.

**Solution**:
1. Identify the formatting aspect (braces, spacing, alignment, etc.)
2. Ask Claude: "Why is clang-format formatting my [braces/spacing/etc.] this way?"
3. Claude will consult relevant reference documentation and explain the active options
4. Test isolated options with minimal configuration

### Merge Conflicts After Introducing clang-format

**Problem**: Massive diffs when introducing clang-format to existing codebase.

**Solution**:
```
Analyze my existing code and generate a clang-format config with minimal impact
```

Claude will use the impact measurement system to create a configuration that matches existing style, reducing conflicts.

### Format-on-Save Not Working

**Problem**: Editor integration isn't formatting files.

**Solution**:
1. Verify clang-format is in PATH: `which clang-format`
2. Test manual formatting: `clang-format -i test.cpp`
3. Check editor configuration matches integration script
4. Ask Claude: "My Vim/Emacs format-on-save isn't working" for specific troubleshooting

### Different Results Across Team Members

**Problem**: Different clang-format versions produce different results.

**Solution**:
1. Standardize clang-format version across team
2. Specify version in CI/CD pipeline
3. Document required version in project README
4. Consider using clang-format from pre-commit hooks (automatically manages versions)

## Advanced Features

### Impact Measurement System

When analyzing existing code, the skill uses a weighted scoring system:

- **Line count changes** (weight: 10) - Additions/removals that affect line numbers
- **In-line whitespace changes** (weight: 1) - Spacing within existing lines

**Impact Score = (line_changes × 10) + (whitespace_changes × 1)**

Lower scores indicate less disruption to git history, easier rebasing, and cleaner merge request reviews.

### Multi-Language Configuration

Use a single `.clang-format` file for multiple languages:

```yaml
---
# C++ settings
Language: Cpp
IndentWidth: 4
---
# JavaScript settings
Language: JavaScript
IndentWidth: 2
---
# Java settings
Language: Java
IndentWidth: 4
```

See `assets/configs/multi-language.clang-format` for complete example.

### Progressive Refinement Workflow

The skill follows a progressive refinement approach:
1. Start with closest template
2. Test on representative samples
3. Measure impact
4. Adjust high-impact options
5. Re-test and re-measure
6. Iterate until optimal

This minimizes trial-and-error and produces maintainable configurations.

## Contributing

This plugin is part of the Claude Code Skills repository. To contribute:

1. Fork the repository
2. Make changes to `plugins/clang-format/`
3. Test with `cc plugin validate ./plugins/clang-format`
4. Submit pull request with description of changes

## Support

For issues or questions:
- Review reference documentation in `skills/clang-format/references/`
- Ask Claude directly about clang-format configuration
- Check [clang-format documentation](https://clang.llvm.org/docs/ClangFormat.html)
- Submit issues to the Claude Skills repository

## License

MIT License - See LICENSE file for details

## Acknowledgments

- clang-format tool by LLVM Project
- Configuration templates based on industry-standard style guides
- Integration scripts adapted from community best practices
