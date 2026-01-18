# Conventional Commits

Helps Claude write properly formatted commit messages that follow industry standards.

## Why Install This?

When you ask Claude to commit changes, you might get messages like:
- "Updated files" (too vague)
- "Fixed bug" (no context)
- Inconsistent formatting across commits
- Messages that don't work with automated changelog tools

This plugin teaches Claude the Conventional Commits standard, making commit messages more useful and consistent.

## What Changes

With this plugin installed, Claude will:
- Write commit messages that follow the Conventional Commits v1.0.0 specification
- Choose the correct commit type (feat, fix, docs, refactor, etc.)
- Use proper formatting with optional scope and body
- Indicate breaking changes correctly with `!` or `BREAKING CHANGE:`
- Follow best practices like imperative mood and lowercase descriptions

## Installation

```bash
/plugin install conventional-commits
```

## Usage

Just install it and use Claude normally. When you ask Claude to commit changes, the messages will automatically follow the standard.

## Example

**Without this plugin**:
```
Updated authentication code
```

**With this plugin**:
```
feat(auth)!: add JWT token validation

Replace basic auth with JWT tokens for improved security.
Sessions now expire after 24 hours instead of never.

BREAKING CHANGE: API clients must now include Authorization header
```

The structured format enables:
- Automated changelog generation
- Semantic versioning based on commit types
- Better searchability in git history
- Clear communication of breaking changes

## What You'll See

Commit messages will use this structure:
```
<type>(scope): <description>

[optional body]

[optional footer]
```

Common types Claude will use:
- `feat:` - New features (triggers minor version bump)
- `fix:` - Bug fixes (triggers patch version bump)
- `docs:` - Documentation changes
- `refactor:` - Code improvements with no behavior change
- `perf:` - Performance improvements
- `test:` - Test additions or fixes
- `build:` - Build system changes
- `ci:` - CI configuration changes

## Requirements

- Claude Code v2.0+

## Works Well With

This plugin works great alongside:
- Tools like semantic-release or git-cliff for automated versioning
- commitlint for commit message validation
- Projects that use automated changelog generation
