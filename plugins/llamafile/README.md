# Llamafile

Helps Claude set up and manage local AI models on your computer using Mozilla's llamafile.

## Why Install This?

Running AI models locally means:

- No API costs or usage limits
- Works offline or in air-gapped environments
- Your data never leaves your machine
- Full control over which models you use

But setting up local LLMs is complicated. You need to:

- Find and download the right binaries and models
- Configure server settings correctly
- Integrate with different frameworks (LiteLLM, OpenAI SDK)
- Debug connection issues and performance problems

This plugin makes Claude an expert at all of that.

## What Changes

With this plugin installed, Claude will:

- Guide you through downloading llamafile and GGUF models
- Generate correct server startup commands with optimal flags
- Help you integrate llamafile with Python code (LiteLLM, OpenAI SDK)
- Write health-check scripts and process management code
- Debug connection errors and performance issues
- Explain configuration options clearly

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install llamafile@jamie-bitflight-skills
```

## Usage

Just install it and ask Claude about llamafile. Examples:

- "Help me install llamafile and set up a local AI model"
- "I'm getting connection refused errors with my llamafile server"
- "Write Python code to use llamafile with LiteLLM"
- "How do I optimize llamafile for GPU acceleration?"
- "Create a script to start llamafile as a background process"

## Example

**Without this plugin**: You ask "How do I run a local AI model?" Claude gives generic advice about various tools but lacks specific knowledge about llamafile configuration, troubleshooting, or integration patterns.

**With this plugin**: Same question, but Claude:

1. Recommends llamafile and explains why
2. Provides exact download commands for binary and model
3. Generates correct server startup command with optimal flags
4. Shows you how to test the API with curl
5. Writes Python integration code with LiteLLM
6. Explains common pitfalls (port 8080 vs 8000, missing /v1 prefix)

## What Claude Will Know

After installing this plugin, Claude will know:

- How to download and install llamafile binaries and GGUF models
- Which models to recommend for different use cases
- All server configuration flags and when to use them
- How to integrate with LiteLLM and OpenAI SDK (including required URL formats)
- Common troubleshooting steps for connection and performance issues
- Process management patterns for running llamafile as a service
- Security considerations (localhost vs network binding)

## Requirements

- Claude Code v2.0+
