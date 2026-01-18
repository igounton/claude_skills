# Conventional Commits Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive Claude Code plugin that helps you write commit messages following the Conventional Commits v1.0.0 specification for structured commit history, automated changelog generation, and semantic versioning.

## Features

- **Complete Conventional Commits v1.0.0 specification** - Official rules and guidelines
- **Commit type reference** - `feat`, `fix`, and all Angular convention types
- **Semantic versioning correlation** - Understand how commits map to version bumps
- **Validation patterns** - Regex and code examples for validation
- **Breaking change guidance** - Multiple methods to indicate breaking changes
- **Tool integration** - commitlint, pre-commit, semantic-release, git-cliff
- **Best practices** - Description formatting, body structure, footer conventions
- **Rich examples** - 15+ complete commit message examples

## Installation

### Prerequisites

- Claude Code 2.1 or later
- Git repository

### Install Plugin

**Method 1: From Marketplace (if available)**

```bash
cc plugin marketplace add owner/claude-code-plugins
cc plugin install conventional-commits@owner
```

**Method 2: Manual Installation**

```bash
# Clone or copy to your plugins directory
git clone https://github.com/owner/conventional-commits ~/.claude/plugins/conventional-commits
cc plugin reload
```

**Method 3: Project-Specific Installation**

```bash
# Install to project directory
mkdir -p .claude/plugins
git clone https://github.com/owner/conventional-commits .claude/plugins/conventional-commits
```

## Quick Start

The plugin automatically activates when Claude detects you need to write commit messages or work with commit history.

**Typical workflow:**

```bash
# Make changes to your codebase
git add .

# Ask Claude to help
"Create a commit message for these changes"
```

Claude will:
1. Analyze your staged changes with `git diff --staged`
2. Determine the appropriate commit type (`feat`, `fix`, etc.)
3. Write a properly formatted conventional commit message
4. Follow best practices for description and body

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | conventional-commits | Complete Conventional Commits v1.0.0 specification and guidance | Auto-activated by Claude |

## Usage

### Automatic Activation

The skill automatically activates when:

- Writing git commit messages
- Task completion requires committing changes
- Project uses semantic-release, commitizen, or git-cliff
- Choosing between commit types (feat/fix/chore/docs)
- Indicating breaking changes
- Generating changelogs from commit history

### Manual Activation

You can explicitly activate the skill:

```text
@conventional-commits
```

Or programmatically:

```text
Skill(command: "conventional-commits")
```

## Commit Message Structure

### Basic Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Required Types (SemVer Impact)

| Type | Description | Version Bump | Example |
|------|-------------|--------------|---------|
| `feat` | New feature for users | MINOR (0.X.0) | `feat: add user authentication` |
| `fix` | Bug fix for users | PATCH (0.0.X) | `fix: prevent crash on empty input` |
| `BREAKING CHANGE` or `!` | Breaking change | MAJOR (X.0.0) | `feat!: remove support for Node 6` |

### Recommended Types (Angular Convention)

| Type | Description | Example |
|------|-------------|---------|
| `build` | Build system changes | `build: update webpack to v5` |
| `ci` | CI configuration changes | `ci: add Node 18 to test matrix` |
| `docs` | Documentation only | `docs: update API reference` |
| `perf` | Performance improvement | `perf: reduce bundle size by 20%` |
| `refactor` | Code change without fix/feature | `refactor: extract validation logic` |
| `style` | Code style changes | `style: fix indentation` |
| `test` | Adding or correcting tests | `test: add unit tests for parser` |
| `chore` | Changes not modifying src/test | `chore: update .gitignore` |
| `revert` | Reverts a previous commit | `revert: feat: add user auth` |

## Examples

### Simple Feature

```text
feat: add user authentication
```

### Bug Fix with Scope

```text
fix(auth): handle token expiration correctly
```

### Breaking Change

```text
feat!: send email notification when product ships
```

Or with footer:

```text
feat: allow config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

### With Full Body and Footers

```text
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

For more examples, see [docs/examples.md](./docs/examples.md).

## Tool Integration

### commitlint

Validate commit messages with commitlint:

```bash
# Install
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Configure
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js

# Test
echo 'feat(api): add new endpoint' | npx commitlint
```

### Pre-commit Hooks

Add validation to git hooks:

```bash
# Install husky
npm install --save-dev husky

# Enable Git hooks
npx husky install

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
```

### Semantic Release

Automate versioning and changelog generation:

```javascript
// release.config.js
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/npm',
    '@semantic-release/github',
  ],
};
```

### git-cliff

Generate changelogs from conventional commits:

```toml
# cliff.toml
[git]
conventional_commits = true
filter_unconventional = false

[changelog]
header = """
# Changelog\n
All notable changes to this project will be documented in this file.\n
"""
```

## Best Practices

### Description Guidelines

- **Use imperative, present tense**: "change" not "changed" nor "changes"
- **Don't capitalize first letter**: `feat: add feature` not `feat: Add feature`
- **No period at end**: `fix: resolve bug` not `fix: resolve bug.`
- **Keep header under 72 characters**: Type + scope + description combined

### Good vs Bad Examples

**Good:**

```text
feat: add validation for email input
fix: handle null pointer in user service
docs: update installation instructions
```

**Bad:**

```text
feat: Added validation for email input     # Past tense
fix: Handles null pointer in user service  # Third person
docs: Update installation instructions.    # Period at end, capitalized
```

### Body Guidelines

- Use imperative, present tense (same as summary)
- Explain **why** the change was made, not just what changed
- Include comparison of previous vs new behavior when helpful
- Separate body from description with one blank line

### Breaking Changes

Always clearly document breaking changes:

1. Use `!` suffix: `feat!: remove support for Node 6`
2. Or use footer: `BREAKING CHANGE: description of what broke`
3. Explain migration path in body if applicable

## Troubleshooting

### Commit message rejected by validation

**Problem**: commitlint rejects your commit message

**Solution**: Check:
- Type is lowercase and one of the allowed types
- Colon and space after type/scope: `feat: ` not `feat:`
- Description uses imperative mood
- No period at end of description

### Changelog not generating correctly

**Problem**: semantic-release or git-cliff doesn't include commits

**Solution**: Verify:
- Commits follow exact specification format
- Using `feat` and `fix` types for features and fixes
- Breaking changes use `BREAKING CHANGE` footer or `!` suffix
- Commits are on the correct branch

### Wrong version bump calculated

**Problem**: Expected MINOR but got PATCH

**Solution**: Ensure:
- Feature commits use `feat` type, not `chore` or other
- Breaking changes include `BREAKING CHANGE` or `!`
- Semantic release configuration is correct

### Team members not following format

**Problem**: Inconsistent commit messages from team

**Solution**:
- Install commitlint with pre-commit hooks
- Configure branch protection to require passing status checks
- Use squash merging with maintainer cleanup
- Add commit message template to repository

## Related Skills

This plugin works well with:

- **git-commit-helper** - Generate commit messages from git diffs
- **commitlint** - Configure and use commitlint for validation
- **pre-commit** - Set up pre-commit hooks for automated validation
- **semantic-release** - Automate versioning and changelog generation

## Contributing

Contributions are welcome! Please:

1. Follow the Conventional Commits specification for commit messages
2. Update documentation for any changes
3. Add examples for new features
4. Test with real git repositories

## License

MIT

## References

- [Conventional Commits Specification v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning](https://semver.org/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md)
- [commitlint](https://commitlint.js.org/)
- [semantic-release](https://semantic-release.gitbook.io/)
- [git-cliff](https://git-cliff.org/)

## Credits

This plugin is based on the official Conventional Commits v1.0.0 specification and incorporates guidance from Angular commit message guidelines and the commitlint project.
