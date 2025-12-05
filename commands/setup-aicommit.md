---
description: Set up aicommit2 + conventional-pre-commit for non-interactive AI-powered Conventional Commits
allowed-tools: Bash(*), Read(*), Write(*), Edit(*)
model: sonnet
---

# Setup Instructions for Claude

Execute the following setup workflow to configure aicommit2 + conventional-pre-commit in the current repository.

## Team-Friendly Design Context

This setup is designed to work per-project without affecting team members who don't have an ANTHROPIC_API_KEY:

- Developers WITH API key: Get AI-generated commit messages automatically
- Developers WITHOUT API key: aicommit2 gracefully skips, they write messages manually
- Both groups: Conventional Commits validation still applies
- No blocking: Missing API key never prevents commits

The `|| true` pattern in the hook ensures aicommit2 failures don't block commits.

## Execution Steps

### Step 1: Initial Discovery (Execute in Parallel)

Make these 3 tool calls concurrently in a single message:

**Call 1 - Check prerequisites:**

```bash
echo "=== Prerequisites Check ===" && \
echo "Node.js & npm:" && node --version && npm --version && \
echo "Python & uv:" && python3 --version && uv --version && \
echo "pre-commit:" && uv run pre-commit --version && \
echo "=== All prerequisites available ==="
```

**Call 2 - Detect any AI provider API keys:**

```bash
echo "=== Checking for AI provider API keys ===" && \
env | grep -i 'api_key' && \
echo "=== Found API keys above ===" || echo "=== No API keys found in environment ==="
```

**Call 3 - Check for existing config:** Use Read tool to check if `.pre-commit-config.yaml` exists.

After these 3 calls complete, analyze results:

- If prerequisites check failed: STOP and report which tool is missing
- If any API keys found: Proceed with full setup (aicommit2 + validation) - aicommit2 will automatically use environment variables
- If no API keys found: Proceed with validation-only setup (skip aicommit2 installation)
- If config file exists: Note to merge configuration instead of overwriting

Note which API keys were found (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY) for troubleshooting if tests fail.

### Step 3: Install aicommit2 (Only if API Keys Found)

**Skip this step if no API keys detected.**

If any AI provider API keys were found in Step 1, install aicommit2:

```bash
npm install -g aicommit2 && aicommit2 --version
```

aicommit2 will automatically detect and use API keys from environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY, etc.). No manual configuration needed.

If installation succeeds, report the version. If it fails with permissions error, inform user they may need to run with sudo or use nvm.

### Step 4: Install Pre-Commit Hook Types

Install all required hook types and verify installation:

```bash
uv run pre-commit install --hook-type prepare-commit-msg && \
uv run pre-commit install --hook-type commit-msg && \
uv run pre-commit install && \
ls -la .git/hooks/ | grep -E "prepare-commit-msg|commit-msg|pre-commit"
```

Report which hooks are now present in `.git/hooks/`.

### Step 5: Create/Update .pre-commit-config.yaml

Based on Step 1 Call 3 results:

**If file exists**: Read the current content, preserve any existing hooks, merge new configuration using Edit.

**If file doesn't exist**: Write the complete configuration using Write.

Use this configuration structure:

```yaml
ci:
  autofix_commit_msg: "chore: auto-generated commit message"
  autoupdate_commit_msg: "chore(pre-commit): autoupdate hooks"

default_install_hook_types:
  - pre-commit
  - commit-msg
  - prepare-commit-msg

repos:
  # Stage 1: AI-Generated Message (prepare-commit-msg)
  - repo: local
    hooks:
      - id: aicommit2-generate
        name: Generate commit message with AI (Claude)
        entry: bash -c 'aicommit2 --confirm || true'
        language: system
        stages: [prepare-commit-msg]
        always_run: true
        pass_filenames: false

  # Stage 2: Conventional Commits Validation (commit-msg)
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.3.0
    hooks:
      - id: conventional-pre-commit
        name: Validate Conventional Commits format
        stages: [commit-msg]
        args:
          - --strict
          - --force-scope
          - feat
          - fix
          - chore
          - docs
          - test
          - refactor
          - perf
          - ci
          - style
          - build
```

Report what was done (created new file vs. updated existing file).

### Step 6: Test the Setup

Execute test sequence to verify configuration:

**Test 1 - AI Generation Test (Only if aicommit2 installed)**:

```bash
echo "# Test aicommit2 setup" >> AICOMMIT_TEST.md && \
git add AICOMMIT_TEST.md && \
git commit
```

Expected: aicommit2 generates message, conventional-pre-commit validates it, commit succeeds.

**If Test 1 fails with API authentication error**:

- Report which API key failed
- List all API keys found in Step 1 (from `env | grep -i 'api_key'`)
- Inform user they can manually configure a different provider using: `aicommit2 config set PROVIDER.key=value`
- Example providers: OPENAI, ANTHROPIC, OPENROUTER, GEMINI, MISTRAL

**Test 2 - Manual Message Test (Always run)**:

```bash
echo "More content" >> AICOMMIT_TEST.md && \
git add AICOMMIT_TEST.md && \
git commit -m "docs(test): update test documentation"
```

Expected: aicommit2 skipped (message provided), validation passes, commit succeeds.

**Test 3 - Validation Rejection Test (Always run)**:

```bash
echo "Final test" >> AICOMMIT_TEST.md && \
git add AICOMMIT_TEST.md && \
git commit -m "bad message without conventional format"
```

Expected: conventional-pre-commit rejects with format error. This rejection is the correct behavior.

**Test 4 - Cleanup (Always run)**:

```bash
git rm AICOMMIT_TEST.md && \
git commit -m "chore(test): remove aicommit2 test file"
```

Expected: Cleanup commit succeeds.

Report test results:

- Which tests passed
- Which tests failed (and why)
- Overall setup status

### Step 7: Verify Complete Setup

Run final verification checks (combine if aicommit2 is installed, otherwise skip aicommit2 check):

**If aicommit2 installed**:

```bash
cat .git/hooks/prepare-commit-msg | head -5 && \
cat .git/hooks/commit-msg | head -5 && \
aicommit2 config get && \
uv run pre-commit run
```

**If aicommit2 NOT installed**:

```bash
cat .git/hooks/prepare-commit-msg | head -5 && \
cat .git/hooks/commit-msg | head -5 && \
uv run pre-commit run
```

**Note on Verification Scope**: Using `pre-commit run` (without flags) validates only staged files. This prevents formatting unrelated files and avoids diff pollution in merge requests. Use `--all-files` ONLY if the user explicitly requests repository-wide validation.

Report all verification results.

### Step 8: Report Summary

Generate final summary report for the user including:

**Configuration Status**:

- API keys detected: List which ones were found (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY, OPENROUTER_API_KEY)
- aicommit2 installed: Yes/No (with version if yes)
- Pre-commit hooks installed: List which ones
- `.pre-commit-config.yaml`: Created new / Updated existing
- Two-stage pipeline configured: Yes
- API provider being used: Determined automatically by aicommit2 from environment variables

**Test Results**:

- AI generation test: Passed/Skipped/Failed
- Manual message test: Passed/Failed
- Validation rejection test: Passed/Failed
- Cleanup: Passed/Failed

**What Works Now**:

- List capabilities based on configuration
- Mention that aicommit2 uses environment variable API keys automatically
- Cost depends on which provider/model is being used (determined by which API key aicommit2 detected)

**For Team Setup**: If this repository will be shared with a team, remind user to document in README/CONTRIBUTING.md:

> **Commit Messages**: This project uses Conventional Commits format (feat, fix, chore, etc.).
>
> - The pre-commit hook validates commit message format automatically.
> - Optional: Install aicommit2 for AI-generated commit messages (requires ANTHROPIC_API_KEY).
> - If you don't have aicommit2, just write commit messages manually following the format.
> - Format: `type(scope): subject` - Example: `feat(auth): add JWT token refresh`

## Troubleshooting Reference

If setup encounters issues, inform user of these common solutions:

**"aicommit2: command not found"**:

- Check npm global bin path: `npm config get prefix`
- Add to PATH: `export PATH="$PATH:$(npm config get prefix)/bin"`

**"Authentication error" from Claude API**:

- Verify API key: `echo $ANTHROPIC_API_KEY`
- Re-configure: `aicommit2 config set ANTHROPIC.key="sk-ant-..."`

**"Hook did not pass" from conventional-pre-commit**:

- Check type setting: `aicommit2 config get type` (should be "conventional")
- Set if needed: `aicommit2 config set type=conventional`

**Hooks don't run**:

- Reinstall hook types: `uv run pre-commit install --hook-type prepare-commit-msg --hook-type commit-msg`
