# LiteLLM Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Unified Python interface for calling 100+ LLM APIs with consistent OpenAI format, specialized for llamafile integration and local LLM server connectivity.

## Features

- **Unified API**: Single `completion()` interface for all providers (OpenAI, Anthropic, Google, Azure, llamafile, Ollama)
- **Llamafile Integration**: Specialized guidance for connecting to local llamafile servers
- **Exception Handling**: Standardized exception mapping across all providers
- **Retry Logic**: Built-in retry and fallback mechanisms
- **Streaming Support**: Synchronous and asynchronous streaming for all providers
- **Cost Tracking**: Automatic usage and cost calculation
- **Proxy Mode**: Deploy centralized LLM gateway with unified configuration

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- Python 3.11 or higher
- (Optional) Running llamafile server for local LLM integration

### Install Plugin

```bash
# Method 1: Using cc plugin install (if published to marketplace)
cc plugin install litellm

# Method 2: Manual installation
git clone <repository-url> ~/.claude/plugins/litellm
cc plugin reload
```

### Install LiteLLM Library

```bash
# Using pip
pip install litellm

# Using uv
uv add litellm
```

## Quick Start

### Basic Llamafile Connection

```python
import litellm

# Connect to local llamafile server
response = litellm.completion(
    model="llamafile/mistralai/mistral-7b-instruct-v0.2",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    api_base="http://localhost:8080/v1",
    temperature=0.2,
    max_tokens=80,
)

print(response.choices[0].message.content)
```

### Multi-Provider Support

```python
import litellm

# Same API works across providers
response = litellm.completion(
    model="gpt-4",  # OpenAI
    messages=[{"role": "user", "content": "Summarize this"}]
)

response = litellm.completion(
    model="claude-3-5-sonnet-20241022",  # Anthropic
    messages=[{"role": "user", "content": "Summarize this"}]
)

response = litellm.completion(
    model="llamafile/gemma-3-3b",  # Local llamafile
    messages=[{"role": "user", "content": "Summarize this"}],
    api_base="http://localhost:8080/v1"
)
```

## Capabilities

| Type | Name | Description |
|------|------|-------------|
| Skill | litellm | Unified LLM API interface with llamafile integration, exception handling, and retry logic |

## Usage

### When This Skill Activates

Claude automatically loads this skill when:

- Working with Python code that imports `litellm`
- Connecting to llamafile or local LLM servers
- Switching between OpenAI/Anthropic/local providers
- Implementing retry/fallback logic for LLM calls
- Using `completion()` patterns in code

### Manual Activation

```bash
# Activate skill explicitly
@litellm

# Or via Skill tool
Skill(command: "litellm")
```

### Core Use Cases

#### 1. Llamafile Integration

```python
import litellm

# MUST use llamafile/ prefix
model = "llamafile/mistralai/mistral-7b-instruct-v0.2"

# MUST include /v1 suffix
api_base = "http://localhost:8080/v1"

response = litellm.completion(
    model=model,
    messages=[{"role": "user", "content": "Hello"}],
    api_base=api_base,
)
```

**Critical Requirements**:
- Always use `llamafile/` prefix for model names
- API base must end with `/v1`
- Default port is 8080
- Do NOT add endpoint paths like `/chat/completions`

#### 2. Exception Handling

```python
import litellm
from litellm import APIConnectionError, RateLimitError
import openai

try:
    response = litellm.completion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Hello"}],
        api_base="http://localhost:8080/v1",
        timeout=30.0,
    )
except openai.APITimeoutError as e:
    # LiteLLM exceptions inherit from OpenAI types
    print(f"Timeout: {e}")
except APIConnectionError as e:
    print(f"Connection failed: {e.message}")
    print(f"Provider: {e.llm_provider}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
```

#### 3. Async Streaming

```python
from litellm import acompletion
import asyncio

async def stream_response():
    response = await acompletion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Write a story"}],
        api_base="http://localhost:8080/v1",
        stream=True,
    )

    async for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()

asyncio.run(stream_response())
```

#### 4. Retry and Fallback

```python
from litellm import completion

response = completion(
    model="llamafile/gemma-3-3b",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:8080/v1",
    num_retries=3,      # Retry 3 times on failure
    timeout=30.0,       # 30 second timeout
)
```

## Configuration

### Environment Variables

```bash
# Set default llamafile API base
export LLAMAFILE_API_BASE="http://localhost:8080/v1"

# Enable debug logging
export LITELLM_LOG="INFO"
```

### Configuration File Example

```toml
# ~/.config/your-app/config.toml
[ai]
model = "llamafile/gemma-3-3b"  # MUST have llamafile/ prefix
api_base = "http://localhost:8080/v1"
temperature = 0.3
max_tokens = 200
```

### Proxy Server Configuration

```yaml
# config.yaml
model_list:
  - model_name: my-local-model
    litellm_params:
      model: llamafile/gemma-3-3b          # add llamafile/ prefix
      api_base: http://localhost:8080/v1   # add /v1 suffix
```

## Examples

See [detailed examples](./docs/examples.md) for:
- Connection verification patterns
- Async service wrappers
- Multi-provider fallback chains
- Embedding generation
- Cost tracking implementation

## Troubleshooting

### Common Issues

**Problem**: `APIConnectionError` when connecting to llamafile

**Solution**: Verify:
1. Llamafile server is running: `curl http://localhost:8080/v1/models`
2. API base includes `/v1` suffix
3. Model name has `llamafile/` prefix
4. Port is correct (default: 8080)

**Problem**: Model not found error

**Solution**:
- Ensure model name starts with `llamafile/` prefix
- Check model is loaded in llamafile server

**Problem**: Timeout errors

**Solution**:
```python
response = litellm.completion(
    model="llamafile/gemma-3-3b",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:8080/v1",
    timeout=60.0,  # Increase timeout
)
```

**Problem**: Exception not caught properly

**Solution**: Import from both `litellm` and `openai`:
```python
import litellm
import openai

try:
    response = litellm.completion(...)
except openai.APITimeoutError:  # Inherits from OpenAI
    pass
except litellm.APIConnectionError:  # LiteLLM specific
    pass
```

See [troubleshooting guide](./docs/troubleshooting.md) for more solutions.

## Related Skills

- **llamafile**: For llamafile server setup, model management, and deployment patterns
  - Activate with: `Skill(command: "llamafile")`
- **uv**: For Python project management and dependency handling
  - Activate with: `Skill(command: "uv")`

## Contributing

Contributions welcome! Please ensure:
- Code examples are tested against latest LiteLLM version
- Documentation includes llamafile-specific configuration
- Exception handling patterns follow OpenAI inheritance model

## License

MIT License

## Credits

**Plugin Author**: Claude Code Skills Repository

**Based On**:
- [LiteLLM](https://github.com/BerriAI/litellm) by BerriAI
- [Llamafile](https://github.com/Mozilla-Ocho/llamafile) by Mozilla Ocho

**References**:
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Llamafile Provider Docs](https://docs.litellm.ai/docs/providers/llamafile)
- [Exception Mapping](https://docs.litellm.ai/docs/exception_mapping)

Documentation verified against LiteLLM main branch (accessed 2025-01-15)
