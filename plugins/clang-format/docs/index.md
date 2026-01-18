# clang-format Plugin Documentation

Complete documentation for the clang-format Configuration plugin for Claude Code.

## Documentation Structure

This documentation is organized into several sections for easy navigation:

### Core Documentation

- **[README.md](../README.md)** - Main plugin documentation with installation, features, quick start, and examples
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and release notes

### Detailed Guides

- **[Skill Reference](./skill-reference.md)** - Complete documentation of the clang-format Configuration skill
  - Workflow routing system
  - Trigger types and activation
  - Impact measurement system
  - Key workflows and concepts

- **[Templates Guide](./templates.md)** - Documentation of all 7 configuration templates
  - Template descriptions and use cases
  - Key settings and characteristics
  - Code examples for each template
  - Decision tree for choosing templates
  - Customization guidelines

- **[Integrations Guide](./integrations.md)** - Documentation of editor and git integration scripts
  - Git hook setup (pre-commit, prek, manual)
  - Vim integration with format-on-save
  - Emacs integration with clang-format-mode
  - Troubleshooting integration issues

- **[References Guide](./references-guide.md)** - Navigation guide for the 14 reference files
  - Reference file summaries
  - Quick navigation strategies
  - Recommended learning paths
  - Tips for effective use

## Quick Links by Task

### Getting Started

- **Install the plugin** → [README.md - Installation](../README.md#installation)
- **Quick start guide** → [README.md - Quick Start](../README.md#quick-start)
- **First-time setup** → [Skill Reference - Common Workflows](./skill-reference.md#key-workflows)

### Configuration

- **Choose a template** → [Templates Guide](./templates.md)
- **Create new config** → [Skill Reference - Creating New Configuration](./skill-reference.md#creating-new-configuration-from-template)
- **Match existing style** → [Skill Reference - Analyzing Existing Code](./skill-reference.md#analyzing-existing-code-style)
- **Customize options** → [References Guide](./references-guide.md)

### Integration

- **Set up git hooks** → [Integrations Guide - Git Hook](./integrations.md#git-hook-pre-commit)
- **Configure Vim** → [Integrations Guide - Vim](./integrations.md#vim-integration-vimrc-clang-formatvim)
- **Configure Emacs** → [Integrations Guide - Emacs](./integrations.md#emacs-integration-emacs-clang-formatel)
- **Set up CI/CD** → [Integrations Guide - CI/CD](./integrations.md#cicd-integration)

### Learning

- **Understand the skill** → [Skill Reference](./skill-reference.md)
- **Learn from examples** → [README.md - Examples](../README.md#examples)
- **Navigate references** → [References Guide](./references-guide.md)
- **Learning paths** → [References Guide - Recommended Learning Paths](./references-guide.md#recommended-learning-paths)

### Troubleshooting

- **Common issues** → [README.md - Troubleshooting](../README.md#troubleshooting)
- **Integration problems** → [Integrations Guide - Troubleshooting sections](./integrations.md)
- **Formatting issues** → [Skill Reference - Troubleshooting Workflow](./skill-reference.md#trigger-4-formatting-behavior-investigation)

## What's Included

### Skill

**clang-format Configuration** - A comprehensive skill that provides:
- Intelligent workflow routing based on trigger types
- Code style analysis with impact measurement
- Configuration generation with hypothesis testing
- Troubleshooting assistance
- Access to all bundled resources

See [Skill Reference](./skill-reference.md) for complete documentation.

### Templates

7 production-ready `.clang-format` configuration templates:

1. **google-cpp-modified** - Google C++ style (4-space indent, 120 columns)
2. **linux-kernel** - Linux kernel standards (tabs, K&R braces)
3. **microsoft-visual-studio** - Microsoft/Visual Studio conventions
4. **modern-cpp17-20** - Modern C++17/20 style
5. **compact-dense** - Compact style for space-constrained environments
6. **readable-spacious** - Spacious style prioritizing readability
7. **multi-language** - Multi-language support (C++, JavaScript, Java)

See [Templates Guide](./templates.md) for complete documentation.

### Integration Scripts

3 integration scripts for development workflow:

1. **pre-commit** - Git hook for automatic formatting (pre-commit/prek compatible)
2. **vimrc-clang-format.vim** - Vim format-on-save configuration
3. **emacs-clang-format.el** - Emacs clang-format integration

See [Integrations Guide](./integrations.md) for complete documentation.

### Reference Documentation

14 reference files organized by category:

**Quick References**:
- index.md - Documentation hub
- quick-reference.md - Complete configurations with explanations
- cli-usage.md - Command-line usage and integrations

**Option Categories** (01-09):
- 01-alignment.md - Vertical alignment
- 02-breaking.md - Line breaking and wrapping
- 03-braces.md - Brace placement styles
- 04-indentation.md - Indentation rules
- 05-spacing.md - Whitespace control
- 06-includes.md - Include/import organization
- 07-languages.md - Language-specific options
- 08-comments.md - Comment formatting
- 09-advanced.md - Penalty system and advanced features

**Complete References**:
- complete/clang-format-cli.md - Full CLI reference
- complete/clang-format-style-options.md - All 194 style options

See [References Guide](./references-guide.md) for navigation assistance.

## Usage Patterns

### Pattern 1: New Project Setup

1. Read [Quick Start](../README.md#quick-start)
2. Ask Claude: "Set up clang-format for my C++ project using [style]"
3. Claude uses [Creating New Configuration workflow](./skill-reference.md#creating-new-configuration-from-template)
4. Optionally set up [integration](./integrations.md)

### Pattern 2: Existing Project Integration

1. Read [Example 2: Match Existing Code Style](../README.md#example-2-match-existing-code-style)
2. Ask Claude: "Analyze my code and create a minimal-impact clang-format config"
3. Claude uses [Analyzing Existing Code workflow](./skill-reference.md#analyzing-existing-code-style)
4. Review impact scores and approve configuration
5. Optionally set up [git hook](./integrations.md#git-hook-pre-commit)

### Pattern 3: Troubleshooting Formatting

1. Identify the formatting aspect (braces, spacing, etc.)
2. Ask Claude: "Why is clang-format [doing X]?"
3. Claude uses [Troubleshooting workflow](./skill-reference.md#trigger-4-formatting-behavior-investigation)
4. Consult [relevant category guide](./references-guide.md#for-questions-by-topic)
5. Test suggested options

### Pattern 4: Learning clang-format

1. Start with [Quick Start](../README.md#quick-start)
2. Explore [Templates](./templates.md) for examples
3. Follow [Learning Path](./references-guide.md#recommended-learning-paths)
4. Experiment with templates and customizations

### Pattern 5: Team Configuration

1. Discuss requirements with team
2. Use [Templates Guide](./templates.md) to choose base template
3. Ask Claude to customize for specific needs
4. Test on representative codebase samples
5. Document in project README
6. Set up [CI/CD checks](./integrations.md#cicd-integration)
7. Configure [git hooks](./integrations.md#git-hook-pre-commit) for enforcement

## Key Features

### Impact Measurement System

The skill uses a weighted scoring system when analyzing existing code:

**Formula**: `Impact Score = (line_changes × 10) + (whitespace_changes × 1)`

This prioritizes minimizing line changes (which affect git history, rebasing, and code review) over whitespace changes (which have minimal impact).

See [Skill Reference - Impact Measurement System](./skill-reference.md#impact-measurement-system) for details.

### Progressive Refinement

The skill follows a progressive refinement approach:
1. Start with closest template
2. Test on representative samples
3. Measure impact
4. Adjust high-impact options
5. Re-test and re-measure
6. Iterate until optimal

This minimizes trial-and-error and produces maintainable configurations.

### Intelligent Routing

The skill automatically routes to the appropriate workflow based on which trigger activated it:
- Explicit clang-format mentions → Reference consultation
- Code style analysis requests → Analysis workflow with impact measurement
- Configuration operations → Template-based creation or modification
- Troubleshooting → Systematic diagnosis with reference consultation
- Style option inquiries → Category-specific guidance
- Minimal-disruption requests → Analysis workflow with emphasis on minimal changes

See [Skill Reference - Workflow Routing](./skill-reference.md#workflow-routing) for details.

## Getting Help

### Ask Claude Directly

The clang-format Configuration skill is automatically activated when you discuss clang-format topics. Simply ask:

```
"Set up clang-format for my project"
"Analyze my code style and create a matching config"
"Why is clang-format adding spaces around my operators?"
"How do I change brace style to Allman?"
"Set up git hooks for formatting"
```

### Browse Documentation

- **Start here**: [README.md](../README.md)
- **Deep dive**: [Skill Reference](./skill-reference.md)
- **Examples**: [README.md - Examples](../README.md#examples)
- **Specific topics**: [References Guide](./references-guide.md)

### External Resources

- [clang-format Official Documentation](https://clang.llvm.org/docs/ClangFormat.html)
- [LLVM Project](https://llvm.org/)
- [ClangFormat Style Options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)
- [pre-commit Framework](https://pre-commit.com/)

## Version Information

**Current Version**: 1.0.0 (2026-01-18)

See [CHANGELOG.md](../CHANGELOG.md) for version history and release notes.

## Contributing

This plugin is part of the Claude Code Skills repository. Contributions welcome!

See [README.md - Contributing](../README.md#contributing) for guidelines.

## License

MIT License - See LICENSE file in plugin root directory.

---

**Navigation**: [↑ Back to Top](#clang-format-plugin-documentation) | [→ README](../README.md) | [→ Skill Reference](./skill-reference.md) | [→ Templates](./templates.md) | [→ Integrations](./integrations.md) | [→ References Guide](./references-guide.md)
