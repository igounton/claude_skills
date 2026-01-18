# Llamafile Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-unspecified-lightgrey) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Claude Code plugin for configuring and managing Mozilla Llamafile - a cross-platform executable format for running local LLMs with an OpenAI-compatible API.

## Features

- Complete llamafile installation and setup guidance
- Server configuration for various performance profiles (GPU, CPU, network)
- OpenAI-compatible API integration patterns
- LiteLLM integration with proper configuration
- Process management and health checking utilities
- Comprehensive troubleshooting guides
- Model selection and download recommendations
- GGUF model format support

## Installation

### Prerequisites

- Claude Code version 2.1 or later
- System requirements:
  - macOS, Windows, Linux, FreeBSD, OpenBSD, or NetBSD
  - AMD64 or ARM64 architecture
  - Sufficient RAM for model (2GB+ recommended for Gemma 3 3B)
  - Optional: GPU with CUDA/Metal/Vulkan support

### Install Plugin

```bash
# Method 1: Using cc plugin install (if in marketplace)
cc plugin install llamafile

# Method 2: Manual installation
git clone <repository-url> ~/.claude/plugins/llamafile
cc plugin reload
```

## Quick Start

Download and start a local LLM server in three commands:

```bash
# Download llamafile binary
curl -L -o llamafile https://github.com/mozilla-ai/llamafile/releases/download/0.9.3/llamafile-0.9.3
chmod 755 llamafile

# Download model (Gemma 3 3B recommended)
curl -L -o gemma-3-3b.gguf \
  https://huggingface.co/Mozilla/gemma-3-3b-it-gguf/resolve/main/gemma-3-3b-it-Q4_K_M.gguf

# Start server
./llamafile --server -m gemma-3-3b.gguf --nobrowser --port 8080 --host 127.0.0.1
```

Test the server:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "temperature": 0.3,
    "max_tokens": 200
  }'
```

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | llamafile | Configure llamafile servers, integrate with APIs, troubleshoot local LLM setups | Auto-activated when working with local LLMs |

## Usage

### Skill

The llamafile skill provides specialized knowledge for:

- Installing llamafile binaries and GGUF model files
- Starting servers with optimal configurations
- Integrating with LiteLLM or OpenAI SDK
- Managing llamafile as a background process
- Troubleshooting server startup and API connection issues

**When activated**: The skill is automatically activated when you mention local LLMs, llamafile, GGUF models, or OpenAI-compatible APIs in your requests.

**Manual activation**:

```
@llamafile
```

or use the Skill tool:

```
Skill(command: "llamafile")
```

**Key capabilities**:

1. **Installation Guidance**: Download binaries and models from verified sources
2. **Server Configuration**: Optimal flags for GPU, CPU, network access scenarios
3. **API Integration**: LiteLLM and OpenAI SDK patterns with proper URL formatting
4. **Process Management**: Health checking and background service patterns
5. **Troubleshooting**: Common errors (port conflicts, missing /v1, connection refused)

## Configuration

### Basic Server

Start llamafile for local API access:

```bash
./llamafile --server \
    -m /path/to/model.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1
```

### GPU-Accelerated Server

For maximum performance with GPU:

```bash
./llamafile --server \
    -m /path/to/model.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1 \
    --ctx-size 4096 \
    --n-gpu-layers 99 \
    --threads 8 \
    --cont-batching \
    --parallel 4
```

### Configuration Options

| Flag | Purpose | Default | When to Use |
|------|---------|---------|-------------|
| `--server` | Enable HTTP API | Off | Required for API endpoints |
| `-m` | Model file path | None | Required, path to GGUF file |
| `--port` | Server port | 8080 | Change if port conflict |
| `--host` | Bind address | 127.0.0.1 | Use 0.0.0.0 for network access |
| `--ctx-size` | Context window | 512 | Increase for longer conversations |
| `--n-gpu-layers` | GPU offload layers | 0 | Set to 99 for full GPU |
| `--threads` | CPU threads | Auto | Control CPU usage |
| `--cont-batching` | Continuous batching | Off | Enable for concurrent requests |
| `--embedding` | Enable embeddings API | Off | Required for /v1/embeddings |

## Examples

### 1. Basic Local LLM Server

Start a llamafile server with default settings:

```bash
# Download binary
curl -L -o llamafile https://github.com/mozilla-ai/llamafile/releases/download/0.9.3/llamafile-0.9.3
chmod 755 llamafile

# Download model
curl -L -o gemma-3-3b.gguf \
  https://huggingface.co/Mozilla/gemma-3-3b-it-gguf/resolve/main/gemma-3-3b-it-Q4_K_M.gguf

# Start server
./llamafile --server -m gemma-3-3b.gguf --nobrowser --port 8080
```

### 2. LiteLLM Integration

Use llamafile with LiteLLM for unified API:

```python
import litellm

response = litellm.completion(
    model="llamafile/gemma-3-3b",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    api_base="http://localhost:8080/v1",
    temperature=0.3,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 3. OpenAI SDK Direct Integration

Use OpenAI SDK with llamafile:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a Python function to calculate factorial"}
    ],
    temperature=0.3,
    max_tokens=300
)

print(response.choices[0].message.content)
```

### 4. Background Process Management

Start llamafile as managed background process:

```python
import subprocess
import time
import httpx

def start_llamafile(llamafile_path: str, model_path: str, port: int = 8080):
    """Start llamafile server with health checking."""
    cmd = [
        llamafile_path,
        "--server",
        "-m", model_path,
        "--nobrowser",
        "--port", str(port),
        "--host", "127.0.0.1",
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to be ready
    url = f"http://127.0.0.1:{port}/health"
    for _ in range(30):
        try:
            response = httpx.get(url, timeout=2)
            if response.status_code == 200:
                print(f"Llamafile server ready at port {port}")
                return process
        except httpx.RequestError:
            pass
        time.sleep(0.5)

    raise TimeoutError("Server did not start within 30 seconds")

# Usage
process = start_llamafile("./llamafile", "./gemma-3-3b.gguf")
```

### 5. GPU-Accelerated Configuration

Optimize for GPU inference:

```bash
./llamafile --server \
    -m gemma-3-3b.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1 \
    --n-gpu-layers 99 \
    --ctx-size 4096 \
    --threads 8 \
    --cont-batching \
    --parallel 4
```

## Troubleshooting

### Server Won't Start

**Port already in use:**

```bash
# Find and kill process on port 8080
kill $(lsof -t -i :8080)
```

**Permission denied:**

```bash
# Ensure llamafile is executable
chmod 755 llamafile
```

**Model file not found:**

```bash
# Verify model file exists and is readable
ls -lh /path/to/model.gguf
```

### Connection Refused

**Check server is running:**

```bash
# Test health endpoint
curl http://localhost:8080/health

# Check port listening
lsof -i :8080
```

**Common causes:**
- Forgot `--server` flag
- Wrong port (8080 vs 8000)
- Missing `/v1` in API URL path
- Server bound to 127.0.0.1 but accessing from remote machine

### API Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Missing `/v1` in URL | Add `/v1` before endpoint path |
| Connection refused | Server not running | Start with `--server` flag |
| Timeout | Model loading slowly | Wait longer or use smaller model |
| Invalid model | Wrong model path | Verify `-m` path to GGUF file |

### Performance Issues

**Optimize inference speed:**
1. Use quantized models (Q4_K_M recommended)
2. Enable GPU: `--n-gpu-layers 99`
3. Increase threads: `--threads 8`
4. Enable batching: `--cont-batching`
5. Reduce context: `--ctx-size 2048`

**Check GPU availability:**

```bash
# NVIDIA
nvidia-smi

# AMD
rocm-smi

# Apple Metal (Activity Monitor)
```

## Common Pitfalls

1. **Port 8000 vs 8080**: Llamafile defaults to port **8080**, not 8000
2. **Missing /v1**: Always include `/v1` suffix for OpenAI-compatible endpoints
3. **LiteLLM prefix**: Must use `llamafile/` prefix in model name
4. **API key**: No real key needed, but clients may require placeholder
5. **Binary permissions**: Must be executable (`chmod 755`)
6. **GPU layers on CPU**: Setting `--n-gpu-layers` on CPU-only systems causes errors

## Contributing

Contributions are welcome. Please ensure:

- Documentation follows Claude Code best practices
- Examples are tested and verified
- References cite official sources with access dates

## License

License not specified in plugin.json. Check repository for license details.

## Credits

Plugin maintained as part of Claude Code skills repository.

**Related Skills:**
- `litellm` - Unified LLM provider interface

**External Resources:**
- [Mozilla llamafile GitHub](https://github.com/mozilla-ai/llamafile)
- [llamafile Documentation](https://mozilla-ai.github.io/llamafile/)
- [LiteLLM llamafile Provider](https://docs.litellm.ai/docs/providers/llamafile)
