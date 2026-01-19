# Verification Gate

Makes Claude investigate before acting instead of jumping to solutions.

## Why Install This?

Claude sometimes identifies the problem correctly but then applies the wrong fix. This happens when Claude recognizes an error pattern and immediately applies a "standard solution" from its training data without checking if that solution matches your specific project setup.

Examples of what goes wrong without this plugin:

- You get "module not found" error. Claude sees it's a PEP 723 script but runs `uv sync` (which updates pyproject.toml instead of the PEP 723 inline dependencies)
- Your config isn't working. Claude modifies the config file without checking that your app reads environment variables first
- Package won't import. Claude runs `pip install` globally when your script uses a virtualenv

## What Changes

With this plugin installed, Claude will:

- Read relevant files before trying to fix things
- Verify its diagnosis before taking action
- Check that its fix actually targets the system it identified as the problem
- Catch when it's about to apply a "common pattern" that doesn't match your project

This makes Claude slower to execute but much more accurate.

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install verification-gate@jamie-bitflight-skills
```

## Usage

Just install it - it works automatically. You'll notice the difference when Claude:

- Sees an error and reads files first instead of immediately running commands
- States what it thinks the problem is and then gathers evidence
- Explains what system it's targeting before making changes

## Example

**Without this plugin:**

```
You: This PEP 723 script can't find the pydantic module
Claude: I'll install the dependencies
Claude: [Runs uv sync immediately]
Result: Doesn't work - uv sync operates on pyproject.toml, not PEP 723
```

**With this plugin:**

```
You: This PEP 723 script can't find the pydantic module
Claude: Let me check the script first
Claude: [Reads the script file]
Claude: I can see the PEP 723 inline dependencies block. I'll add pydantic there.
Claude: [Edits the # /// script block in the file]
Result: Works correctly
```

## Trade-offs

- Claude will be slower (2-3 extra file reads before each action)
- Claude will explain its reasoning more (adds verbosity)
- Fixes will be more accurate (fewer debugging cycles)
- Overall time saved despite slower start

## Requirements

- Claude Code v2.0+
