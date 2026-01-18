# Commitlint Plugin Usage Examples

Concrete examples demonstrating how to use the commitlint plugin for various workflows.

---

## Example 1: Setting Up Commitlint for a New Repository

**Scenario**: You're starting a new project and want to enforce Conventional Commits format for all commit messages.

**Steps**:

1. Activate the commitlint skill to get setup guidance:

```text
User: Set up commitlint with conventional commits for this project

Claude: [Skill activates automatically]
I'll help you set up commitlint with the conventional commits configuration.
```

2. Follow the guidance to install dependencies:

```bash
# Install commitlint CLI and conventional config
npm install -D @commitlint/cli @commitlint/config-conventional
```

3. Create configuration file:

```bash
# Create commitlint.config.js
cat > commitlint.config.js << 'EOF'
export default {
  extends: ['@commitlint/config-conventional'],
};
EOF
```

4. Test the configuration:

```bash
# Test with a valid commit message
echo "feat: add user authentication" | npx commitlint
# Exit code: 0 (success)

# Test with an invalid commit message
echo "Added user authentication" | npx commitlint
# Exit code: 1 (error - missing type)
```

5. Set up pre-commit hook (optional):

```bash
# Install husky
npm install -D husky

# Initialize husky
npx husky init

# Add commit-msg hook
echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
chmod +x .husky/commit-msg
```

**Result**: All commits are now validated against Conventional Commits format automatically.

---

## Example 2: Extracting Rules for AI Commit Message Generation

**Scenario**: You're building an AI tool that generates commit messages and need to extract commitlint rules to use as constraints in your LLM prompt.

**Steps**:

1. Activate the commitlint skill:

```text
User: Extract commitlint rules from my project config to use in LLM prompts

Claude: [Skill provides rule extraction guidance]
```

2. Read the commitlint configuration:

```javascript
import load from '@commitlint/load';
import { resolve } from 'path';

async function getCommitlintConfig(projectDir) {
  const config = await load({}, { cwd: projectDir });
  return config;
}
```

3. Extract rules into LLM-friendly format:

```python
def extract_rules_for_prompt(config: dict) -> str:
    """Extract commitlint rules into LLM-friendly format."""
    rules = config.get('rules', {})
    prompt_parts = []

    # Extract allowed commit types
    if 'type-enum' in rules:
        level, applicability, types = rules['type-enum']
        if level > 0 and applicability == 'always':
            prompt_parts.append(f"COMMIT TYPES: Use one of: {', '.join(types)}")

    # Extract allowed scopes
    if 'scope-enum' in rules:
        level, applicability, scopes = rules['scope-enum']
        if level > 0 and applicability == 'always' and scopes:
            prompt_parts.append(f"SCOPES: Use one of: {', '.join(scopes)}")

    # Extract header max length
    if 'header-max-length' in rules:
        level, applicability, length = rules['header-max-length']
        if level > 0:
            prompt_parts.append(f"MAX LENGTH: Header must be {length} characters or less")

    # Extract subject case restrictions
    if 'subject-case' in rules:
        level, applicability, cases = rules['subject-case']
        if level > 0 and applicability == 'never':
            prompt_parts.append(f"CASE RESTRICTIONS: Subject must NOT use: {', '.join(cases)}")
        elif level > 0 and applicability == 'always':
            prompt_parts.append(f"CASE REQUIREMENT: Subject must use: {', '.join(cases)}")

    # Extract subject full-stop rule
    if 'subject-full-stop' in rules:
        level, applicability, value = rules['subject-full-stop']
        if level > 0 and applicability == 'never':
            prompt_parts.append(f"PUNCTUATION: Subject must NOT end with '{value}'")

    return '\n'.join(prompt_parts)
```

4. Generate LLM prompt with extracted rules:

```python
config = await get_commitlint_config('/path/to/project')
rules_text = extract_rules_for_prompt(config)

llm_prompt = f"""
Generate a commit message following these rules:

{rules_text}

Git diff:
{git_diff}

Format: type(scope): subject

Examples:
- feat(auth): add OAuth2 login flow
- fix(api): handle null response in user endpoint
- docs: update installation instructions
"""
```

**Result**: You now have commitlint rules formatted as clear constraints for LLM prompt generation.

---

## Example 3: Validation Loop with Retry Logic

**Scenario**: You're implementing an AI commit message generator that needs to validate generated messages with commitlint and retry if validation fails.

**Steps**:

1. Create validation function:

```python
import subprocess
from pathlib import Path

async def validate_with_commitlint(
    message: str,
    cwd: Path | None = None,
) -> tuple[bool, list[str]]:
    """
    Validate commit message with commitlint.

    Args:
        message: The commit message to validate
        cwd: Working directory (defaults to current directory)

    Returns:
        Tuple of (is_valid, error_messages)
    """
    result = subprocess.run(
        ['npx', 'commitlint'],
        input=message,
        capture_output=True,
        text=True,
        cwd=cwd,
    )

    if result.returncode == 0:
        return True, []

    # Parse errors from stderr
    errors = []
    for line in result.stderr.split('\n'):
        line = line.strip()
        if line and not line.startswith('⚠') and not line.startswith('✖'):
            errors.append(line)

    return False, errors
```

2. Implement retry loop:

```python
async def generate_commit_message_with_validation(
    diff: str,
    project_dir: Path,
    max_retries: int = 3,
) -> tuple[str, bool]:
    """
    Generate commit message with commitlint validation and retry.

    Args:
        diff: Git diff output
        project_dir: Project directory with commitlint config
        max_retries: Maximum number of retry attempts

    Returns:
        Tuple of (commit_message, is_valid)
    """
    # Load commitlint config and extract rules
    config = await get_commitlint_config(project_dir)
    rules_text = extract_rules_for_prompt(config)

    # Initial prompt
    prompt = f"""
Generate a commit message following these rules:

{rules_text}

Git diff:
{diff}
"""

    for attempt in range(max_retries + 1):
        # Generate message with LLM
        message = await generate_with_llm(prompt)

        # Validate with commitlint
        is_valid, errors = await validate_with_commitlint(message, project_dir)

        if is_valid:
            return message, True

        # If not valid and retries remain, add error feedback to prompt
        if attempt < max_retries:
            error_text = '\n'.join(errors)
            prompt = f"""
The previous commit message was rejected by commitlint with these errors:

{error_text}

Please generate a new commit message that fixes these issues.

Rules:
{rules_text}

Git diff:
{diff}

Previous attempt (FAILED):
{message}
"""

    # Return best effort after max retries
    return message, False
```

3. Use in your workflow:

```python
# Example usage
diff = subprocess.check_output(['git', 'diff', '--staged'], text=True)
project_dir = Path.cwd()

message, is_valid = await generate_commit_message_with_validation(
    diff=diff,
    project_dir=project_dir,
    max_retries=3,
)

if is_valid:
    print(f"✓ Valid commit message generated:\n{message}")
else:
    print(f"⚠ Best effort after retries:\n{message}")
    print("Manual review recommended")
```

**Result**: Your AI tool generates commit messages that are validated against commitlint rules with automatic retry and error correction.

---

## Example 4: Custom Rules for Team Conventions

**Scenario**: Your team has specific commit message conventions beyond the standard Conventional Commits format.

**Steps**:

1. Activate the commitlint skill for custom rule guidance:

```text
User: Configure commitlint with custom rules for our team conventions

Claude: [Skill provides custom rule configuration guidance]
```

2. Create custom configuration:

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Restrict commit types to team-approved subset
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'refactor', 'test', 'chore'],
    ],

    // Require specific scopes for API changes
    'scope-enum': [
      2,
      'always',
      ['api', 'ui', 'db', 'auth', 'core', 'docs', 'ci'],
    ],

    // Enforce 72-character limit (stricter than default)
    'header-max-length': [2, 'always', 72],

    // Require scope for all commits except docs
    'scope-empty': [1, 'never'],

    // Allow sentence-case for subject (team preference)
    'subject-case': [2, 'always', 'sentence-case'],

    // Require imperative mood (custom message)
    'subject-full-stop': [2, 'never', '.'],

    // Require body for certain types
    'body-empty': [
      2,
      'never',
      // Only require body for feat and fix (custom logic would need plugin)
    ],

    // Enforce blank line before body
    'body-leading-blank': [2, 'always'],
  },
};
```

3. Document team conventions:

```markdown
# Commit Message Guidelines

## Format

```
type(scope): Subject line (max 72 chars)

Body paragraph explaining the change in detail.
Can span multiple lines.

Footer with issue references.
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding or updating tests
- **chore**: Changes to build process or auxiliary tools

## Scopes

- **api**: Backend API changes
- **ui**: Frontend UI changes
- **db**: Database schema or queries
- **auth**: Authentication/authorization
- **core**: Core business logic
- **docs**: Documentation
- **ci**: CI/CD configuration

## Examples

```
feat(auth): Add OAuth2 login flow

Implement OAuth2 authentication with Google and GitHub providers.
Includes redirect handling and token storage.

Closes #123
```
```

4. Test custom rules:

```bash
# Valid message
echo "feat(api): Add user profile endpoint" | npx commitlint
# ✓ Success

# Invalid - missing scope
echo "feat: add feature" | npx commitlint
# ✖ Error: scope-empty

# Invalid - wrong scope
echo "feat(frontend): add feature" | npx commitlint
# ✖ Error: scope-enum (frontend not in allowed list)

# Invalid - exceeds 72 chars
echo "feat(api): This is a very long subject line that exceeds the maximum allowed length" | npx commitlint
# ✖ Error: header-max-length
```

**Result**: Your team has enforceable custom commit message conventions that match your workflow.

---

## Example 5: Integrating with CI/CD

**Scenario**: You want to validate all commit messages in a pull request as part of your CI/CD pipeline.

**Steps**:

1. Create CI validation script:

```bash
#!/bin/bash
# scripts/validate-commits.sh

set -e

# Get the base branch (usually main or master)
BASE_BRANCH="${1:-origin/main}"

# Get the range of commits to validate
COMMIT_RANGE="${BASE_BRANCH}..HEAD"

echo "Validating commits in range: ${COMMIT_RANGE}"

# Run commitlint on the commit range
npx commitlint --from "${BASE_BRANCH}" --to HEAD --verbose

echo "✓ All commits are valid"
```

2. Add to GitHub Actions:

```yaml
# .github/workflows/validate-commits.yml
name: Validate Commits

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history for all branches

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Validate commit messages
        run: npx commitlint --from ${{ github.event.pull_request.base.sha }} --to HEAD --verbose
```

3. Add to GitLab CI:

```yaml
# .gitlab-ci.yml
commitlint:
  stage: test
  image: node:20
  script:
    - npm ci
    - npx commitlint --from ${CI_MERGE_REQUEST_DIFF_BASE_SHA:-origin/main} --to HEAD --verbose
  only:
    - merge_requests
```

4. Test locally before pushing:

```bash
# Validate commits in current branch
./scripts/validate-commits.sh origin/main

# Or use commitlint directly
npx commitlint --from origin/main
```

**Result**: All pull requests are automatically validated for commit message format, preventing non-compliant commits from being merged.

---

## Example 6: Debugging Commit Message Rejections

**Scenario**: Your commit message is being rejected by commitlint and you need to understand why.

**Steps**:

1. Activate the commitlint skill:

```text
User: My commit message "Fixed bug in API" is being rejected by commitlint

Claude: [Skill activates and provides debugging guidance]
```

2. Run commitlint with verbose output:

```bash
echo "Fixed bug in API" | npx commitlint --verbose
```

Output:

```
⚠   input: Fixed bug in API
✖   type may not be empty [type-empty]
✖   subject may not be empty [subject-empty]
✖   found 2 problems, 0 warnings
```

3. Understand the errors:

- `type-empty`: The message doesn't start with a type (feat, fix, etc.)
- `subject-empty`: After parsing, no subject was found

4. Check the configuration:

```bash
npx commitlint --print-config
```

This shows which rules are active and their values.

5. Fix the message:

```bash
# Correct format
echo "fix(api): resolve null pointer exception" | npx commitlint
# ✓ Success
```

6. Common fixes:

```text
❌ "Fixed bug in API"
✓ "fix(api): resolve null pointer exception"

❌ "feat:add feature"
✓ "feat: add feature" (space after colon)

❌ "FEAT: Add Feature"
✓ "feat: add feature" (lowercase type)

❌ "feat: This Is A Very Long Subject Line That Exceeds The Maximum Length"
✓ "feat: add concise subject line" (under limit)

❌ "feat: add feature."
✓ "feat: add feature" (no period)
```

**Result**: You understand why your commit message was rejected and how to fix it according to your project's commitlint configuration.

---

## Related Documentation

- [README.md](../README.md) - Plugin overview and installation
- [Commitlint Official Docs](https://commitlint.js.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
