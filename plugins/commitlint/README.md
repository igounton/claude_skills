# Commitlint

Helps Claude work with your commitlint configuration and generate valid commit messages.

## Why Install This?

If your project uses commitlint to enforce commit message standards, Claude needs this plugin to:

- Understand your specific commitlint rules and configuration
- Generate commit messages that pass your validation checks on the first try
- Help you set up or modify commitlint configuration correctly
- Explain commitlint validation errors when they occur

Without this plugin, Claude might generate commit messages that fail your commitlint checks, requiring multiple attempts to get it right.

## What Changes

With this plugin installed, Claude will:

- Read and understand your commitlint configuration files (commitlint.config.js, .commitlintrc, etc.)
- Know which commit types are allowed in your project (feat, fix, docs, etc.)
- Follow your header length limits, scope rules, and formatting requirements
- Generate commit messages that match your exact conventions
- Help you configure commitlint with the correct syntax and rule format
- Explain what went wrong when commitlint rejects a commit message

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install commitlint@jamie-bitflight-skills
```

## Usage

Just install it - it works automatically. Claude will detect commitlint configuration in your project and apply those rules.

You'll notice the difference when you:

- Ask Claude to create a commit
- Request help setting up commitlint
- Ask Claude to explain a commitlint error
- Need to configure custom commit message rules

## Example

**Without this plugin**: You say "create a commit for these changes". Claude writes `"Updated the authentication system"` which fails because your project requires conventional commit format with type prefix.

**With this plugin**: Same request. Claude reads your commitlint.config.js, sees you require conventional commits with types [feat, fix, docs, refactor], and generates: `"feat: add OAuth2 authentication support"` which passes validation immediately.

## Requirements

- Claude Code v2.0+
- Project using commitlint (optional, but this plugin is most useful when commitlint is configured)
