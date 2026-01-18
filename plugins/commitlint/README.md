# Commitlint Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A Claude Code plugin providing comprehensive guidance for setting up, configuring, and integrating commitlint for Conventional Commits validation.

## Features

- **Configuration Detection**: Understand commitlint's cosmiconfig file discovery and priority order
- **Rule Configuration**: Complete reference for all commitlint rules, severity levels, and applicability
- **Common Configurations**: Detailed documentation of `@commitlint/config-conventional` and custom configs
- **CLI Usage**: Command patterns for linting commits in various contexts
- **Programmatic Integration**: JavaScript/TypeScript examples for loading config and validating messages
- **LLM Integration Patterns**: Extract rules for AI prompt generation and implement validation loops
- **Troubleshooting**: Solutions for common configuration and validation issues

## Installation

### Prerequisites

- Claude Code 2.1 or higher
- Node.js and npm/yarn/pnpm (for running commitlint)
- Git repository (for commit message validation)

### Install Plugin

If this plugin is available in a marketplace:

```bash
/plugin install commitlint@marketplace-name
```

For manual installation:

```bash
# Clone to your local plugins directory
cp -r ./plugins/commitlint ~/.claude/plugins/

# Or install as project-scoped plugin
/plugin install ./plugins/commitlint --scope project
```

## Quick Start

The commitlint skill activates automatically when you're working with commit message validation. Trigger phrases include:

- "Set up commitlint for this repository"
- "Configure commit message validation"
- "Extract commitlint rules for LLM prompts"
- "Debug why my commit message is being rejected"

Example workflow:

```text
User: Set up commitlint with conventional commits config for this project

Claude: I'll help you set up commitlint with the conventional commits configuration...
[Skill activates and provides step-by-step guidance]
```

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | commitlint | Validate commit messages against Conventional Commits format using commitlint configuration and rules | Auto-activated or `@commitlint` |

## Usage

### Automatic Activation

The commitlint skill activates automatically when:

- Setting up commit message validation for a project
- Working with `commitlint.config.js` or `.commitlintrc` files
- Configuring CI/CD to enforce commit format
- Extracting commit rules for LLM prompt generation
- Debugging commit message rejection errors

### Manual Activation

You can explicitly activate the skill:

```text
@commitlint
```

Or in code:

```text
Skill(command: "commitlint")
```

### Key Use Cases

#### 1. Setting Up Commitlint

The skill provides guidance for installing and configuring commitlint:

```bash
# Install commitlint with conventional config
npm install -D @commitlint/cli @commitlint/config-conventional

# Create config file
echo "export default { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js

# Test it
echo "feat: add new feature" | npx commitlint
```

#### 2. Understanding Configuration Formats

The skill documents all configuration formats (JavaScript, TypeScript, JSON, YAML) and file discovery priority:

**Dedicated config files** (highest priority):
- `.commitlintrc`
- `.commitlintrc.json`
- `commitlint.config.js`
- `commitlint.config.ts`
- And more...

**Package files**:
- `package.json` with `commitlint` field
- `package.yaml` (PNPM) with `commitlint` field

#### 3. Rule Configuration

Complete reference for configuring rules with severity levels and applicability:

```javascript
rules: {
  // [level, applicability, value]
  'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style']],
  'header-max-length': [2, 'always', 100],
  'subject-case': [2, 'never', ['upper-case', 'pascal-case']],
}
```

**Severity Levels:**
- `0` = Disabled
- `1` = Warning
- `2` = Error

#### 4. LLM Integration

The skill provides patterns for integrating commitlint with LLM-based commit message generation:

**Extract Rules for Prompts:**
```python
def extract_rules_for_prompt(config: dict) -> str:
    """Convert commitlint rules to LLM-friendly constraints."""
    # Extract type-enum, scope-enum, max-length, case rules
    # Return formatted string for LLM context
```

**Validation Loop:**
1. LLM generates commit message based on diff and rules
2. Validate with commitlint
3. If invalid, feed errors back to LLM
4. Retry (max 3 times)
5. Return valid message or best effort

#### 5. CLI Commands

```bash
# Lint the last commit
npx commitlint --last

# Lint a range of commits
npx commitlint --from HEAD~5

# Lint message from stdin
echo "feat: add feature" | npx commitlint

# Print resolved config
npx commitlint --print-config

# Strict mode (warnings become errors)
npx commitlint --last --strict
```

#### 6. Programmatic Usage

```javascript
import load from '@commitlint/load';
import lint from '@commitlint/lint';

async function validateMessage(message) {
  const config = await load();
  const result = await lint(message, config.rules);

  return {
    valid: result.valid,
    errors: result.errors,
    warnings: result.warnings,
  };
}
```

## Examples

See [Usage Examples](./docs/examples.md) for detailed workflows including:

- Setting up commitlint for a new repository
- Extracting rules for AI commit message generation
- Implementing a validation loop with retry logic
- Configuring custom rules for team conventions
- Integrating with pre-commit hooks and CI/CD

## Troubleshooting

### Node v24 ESM Issues

Use `.mjs` extension for ES modules config, or add `"type": "module"` to package.json.

### "Please add rules" Error

Config without `extends` or `rules` fails. Include at least one:

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
};
```

### Subject Case Confusion

`@commitlint/config-conventional` uses `never` with specific cases, meaning those cases are **forbidden** (not required):

```javascript
// This FORBIDS sentence-case, start-case, pascal-case, upper-case
'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']]
```

### Empty Scope Enum

`scope-enum` with `[]` passes all scopes. Use specific array to restrict:

```javascript
rules: {
  'scope-enum': [2, 'always', ['api', 'ui', 'docs']],
}
```

## Related Skills

This plugin works well with:

- **pre-commit**: For pre-commit hook integration
- **conventional-commits**: For Conventional Commits format specification

Activate related skills:

```text
Skill(command: "pre-commit")
Skill(command: "conventional-commits")
```

## Configuration

This plugin uses Claude Code's standard skill activation mechanism. No additional configuration is required.

The skill automatically activates when you mention commitlint-related tasks or work with commitlint configuration files.

## Contributing

Improvements and corrections welcome. When contributing:

1. Verify all technical claims against official commitlint documentation
2. Include source citations with access dates
3. Test code examples in real projects
4. Follow markdown formatting standards (MD031 - blank lines around fences)

## License

This plugin is part of the Claude Skills repository. See repository LICENSE file.

## Credits

**Author**: Claude Skills Repository Contributors

**Sources**:
- [Commitlint Official Site](https://commitlint.js.org/)
- [Configuration Reference](https://commitlint.js.org/reference/configuration.html)
- [Rules Reference](https://commitlint.js.org/reference/rules.html)
- [CLI Reference](https://commitlint.js.org/reference/cli.html)
- [GitHub Repository](https://github.com/conventional-changelog/commitlint)

**Attribution**: Skill created from reference documentation at the commit-polish repository (2025-12-01)
