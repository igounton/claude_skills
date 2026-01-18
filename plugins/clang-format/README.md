# clang-format Configuration

Helps Claude configure clang-format to match your existing code style instead of forcing a style on you.

## Why Install This?

Setting up code formatting typically means:
- Massive whitespace-only commits that pollute git history
- Breaking every in-progress feature branch
- Days of bikeshedding about brace styles and indent width
- Copy-pasting config files from the internet and hoping they work

This plugin changes that. Claude will analyze your existing code, measure the impact of different configurations, and show you exactly what will change before applying anything.

## What Changes

With this plugin installed, Claude will:
- Analyze your existing code style before suggesting any formatting configuration
- Test multiple configuration options and score them by impact (line changes vs whitespace)
- Show you comparison tables and example diffs before changing anything
- Ask for your approval before finalizing a configuration
- Set up editor integration and git hooks automatically
- Know all 194 clang-format options without needing to search documentation

## Installation

```bash
/plugin install clang-format
```

## Usage

Just ask Claude naturally. The plugin works automatically.

### Generate Configuration from Existing Code

**You say**: "Set up clang-format for this C++ project, but don't change the existing style"

**Claude will**:
1. Examine multiple files in your codebase
2. Identify brace styles, indentation, spacing patterns
3. Generate several configuration hypotheses
4. Test each one and measure impact (line changes + whitespace changes)
5. Show you a comparison table with scores
6. Present example diffs showing what will change
7. Ask for approval before creating `.clang-format`

### Set Up Format-on-Save

**You say**: "Set up clang-format to run automatically in my editor"

**Claude will**: Pick the right integration for your editor (Vim, Emacs, VS Code) and set it up correctly.

### Add Git Hook

**You say**: "Make clang-format run before I commit"

**Claude will**: Set up a pre-commit hook that formats only staged files.

### Troubleshoot Formatting

**You say**: "Why is clang-format putting my braces in weird places?"

**Claude will**: Check your configuration, identify the relevant options, explain what's happening, and suggest fixes.

## Example

**Without this plugin**: You ask "add clang-format". Claude copies a random config file from the internet. You apply it. 2,847 lines change across 93 files. Your git history is now useless.

**With this plugin**: Same request, but Claude:
- Analyzes 5 files in your codebase
- Tests 3 configuration approaches
- Reports: "Config A: 34 line changes, Config B: 12 line changes, Config C: 8 line changes"
- Shows you diffs of what will change in each config
- Recommends Config C
- Waits for your approval

You approve. Claude creates `.clang-format`. You apply it. 8 lines change (real formatting fixes, not whitespace churn). Your git history stays clean.

## What's Included

This plugin bundles:
- 7 ready-to-use configuration templates (Google, Linux kernel, Microsoft, modern C++, etc.)
- 3 editor/git integration scripts
- Complete reference documentation for all clang-format options
- Systematic workflows for analyzing code style

## Requirements

- Claude Code v2.0+
- clang-format installed (`apt install clang-format` / `brew install clang-format`)
