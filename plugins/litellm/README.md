# LiteLLM

Helps Claude write correct Python code when your project calls LLM APIs.

## Why Install This?

When you're building Python applications that need to call LLMs, there are many ways to get it wrong:

- Forgetting the `llamafile/` prefix when connecting to local models
- Using the wrong API endpoint format
- Not handling exceptions properly
- Missing retry logic for unreliable connections
- Hard-coding a single provider when you want flexibility

Without this plugin, Claude might suggest code patterns that look reasonable but won't work with your setup.

## What Changes

With this plugin installed, Claude will:

- Use the correct model names and prefixes (like `llamafile/gemma-3-3b`)
- Connect to your local llamafile server on the right port with the right endpoint format
- Handle exceptions properly using LiteLLM's OpenAI-compatible error types
- Add retry logic when needed
- Set up streaming correctly for async responses
- Know when to use sync vs async patterns
- Configure environment variables correctly

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install litellm@jamie-bitflight-skills
```

## Usage

Just install it - it works automatically. Claude will use this knowledge when you're writing Python code that involves LLMs.

## Example

**Without this plugin**: You say "connect this Python script to my local llamafile server". Claude might write:

```python
response = litellm.completion(
    model="gemma-3-3b",  # Wrong - missing prefix
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:8000",  # Wrong port
)
```

This code fails because the model name needs the `llamafile/` prefix and llamafile runs on port 8080 by default.

**With this plugin**: Same request, Claude writes:

```python
response = litellm.completion(
    model="llamafile/gemma-3-3b",  # Correct prefix
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:8080/v1",  # Correct port and endpoint
    timeout=30.0,
    num_retries=3,
)
```

This works immediately and includes timeout and retry handling.

## When This Helps

This plugin is most useful when you're:

- Building CLI tools that need to call LLMs (like commit message generators)
- Writing Python apps that use local models via llamafile
- Creating services that might switch between OpenAI, Anthropic, and local models
- Adding LLM features to existing Python projects
- Setting up retry/fallback logic for production systems

## Requirements

- Claude Code v2.0+
- Python 3.11+ (for your project - this plugin is just documentation)
