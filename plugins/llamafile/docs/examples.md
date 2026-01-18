# Llamafile Usage Examples

Comprehensive examples demonstrating llamafile setup, configuration, and integration patterns.

---

## Example 1: Complete Setup from Scratch

**Scenario**: Set up a local LLM server for development with no prior llamafile installation.

**Steps**:

1. Download llamafile binary (v0.9.3)
2. Download recommended model (Gemma 3 3B)
3. Start server with basic configuration
4. Verify server is responding
5. Test with Python client

**Code**:

```bash
#!/bin/bash
# setup-llamafile.sh - Complete llamafile setup script

set -euo pipefail

# Configuration
LLAMAFILE_VERSION="0.9.3"
INSTALL_DIR="$HOME/.local/bin"
MODEL_DIR="$HOME/.local/share/llamafile/models"
LLAMAFILE_PATH="$INSTALL_DIR/llamafile"
MODEL_PATH="$MODEL_DIR/gemma-3-3b.gguf"

# Create directories
mkdir -p "$INSTALL_DIR" "$MODEL_DIR"

# Download llamafile binary
echo "Downloading llamafile ${LLAMAFILE_VERSION}..."
curl -L -o "$LLAMAFILE_PATH" \
  "https://github.com/mozilla-ai/llamafile/releases/download/${LLAMAFILE_VERSION}/llamafile-${LLAMAFILE_VERSION}"

chmod 755 "$LLAMAFILE_PATH"

# Download model
echo "Downloading Gemma 3 3B model..."
curl -L -o "$MODEL_PATH" \
  "https://huggingface.co/Mozilla/gemma-3-3b-it-gguf/resolve/main/gemma-3-3b-it-Q4_K_M.gguf"

# Verify downloads
echo "Verifying installation..."
"$LLAMAFILE_PATH" --version
ls -lh "$MODEL_PATH"

echo "Setup complete!"
echo "Start server with: $LLAMAFILE_PATH --server -m $MODEL_PATH --nobrowser --port 8080"
```

**Result**: Llamafile binary and model downloaded to user's local directories, ready for use.

---

## Example 2: Systemd Service Configuration

**Scenario**: Run llamafile as a systemd service that starts automatically on boot.

**Steps**:

1. Create systemd service unit file
2. Configure service to run as user
3. Enable automatic restart on failure
4. Start and enable service

**Code**:

```ini
# /etc/systemd/system/llamafile.service
[Unit]
Description=Llamafile Local LLM Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/.local/share/llamafile
ExecStart=/home/your-username/.local/bin/llamafile \
    --server \
    -m /home/your-username/.local/share/llamafile/models/gemma-3-3b.gguf \
    --nobrowser \
    --port 8080 \
    --host 127.0.0.1 \
    --ctx-size 4096 \
    --n-gpu-layers 99 \
    --threads 8

Restart=on-failure
RestartSec=10

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Installation**:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start llamafile

# Check status
sudo systemctl status llamafile

# Enable automatic start on boot
sudo systemctl enable llamafile

# View logs
sudo journalctl -u llamafile -f
```

**Result**: Llamafile runs as a system service with automatic restart on failure and boot-time startup.

---

## Example 3: Application Configuration with TOML

**Scenario**: Build an application that uses llamafile for local inference with configurable settings.

**Steps**:

1. Create configuration file with llamafile settings
2. Implement configuration loader
3. Start llamafile server automatically
4. Make API requests using configuration

**Code**:

```toml
# config.toml
[ai]
model = "llamafile/gemma-3-3b"
temperature = 0.3
max_tokens = 500
timeout = 30

[llamafile]
binary_path = "~/.local/bin/llamafile"
model_path = "~/.local/share/llamafile/models/gemma-3-3b.gguf"
api_base = "http://127.0.0.1:8080/v1"
port = 8080
host = "127.0.0.1"
auto_start = true

[llamafile.server_args]
ctx_size = 4096
n_gpu_layers = 99
threads = 8
nobrowser = true
```

```python
# config_loader.py
import tomli
import subprocess
import time
import httpx
from pathlib import Path
from typing import Optional


class LlamafileConfig:
    """Load and manage llamafile configuration."""

    def __init__(self, config_path: str = "config.toml"):
        with open(config_path, "rb") as f:
            self.config = tomli.load(f)

        self.ai = self.config["ai"]
        self.llamafile = self.config["llamafile"]
        self.server_args = self.llamafile.get("server_args", {})
        self._process: Optional[subprocess.Popen] = None

    def start_server(self) -> subprocess.Popen:
        """Start llamafile server if auto_start enabled."""
        if not self.llamafile.get("auto_start", False):
            return None

        # Check if server already running
        if self._check_server_running():
            print(f"Server already running on port {self.llamafile['port']}")
            return None

        # Build command
        cmd = [
            Path(self.llamafile["binary_path"]).expanduser(),
            "--server",
            "-m", Path(self.llamafile["model_path"]).expanduser(),
            "--port", str(self.llamafile["port"]),
            "--host", self.llamafile["host"],
        ]

        # Add optional arguments
        if self.server_args.get("nobrowser"):
            cmd.append("--nobrowser")
        if ctx_size := self.server_args.get("ctx_size"):
            cmd.extend(["--ctx-size", str(ctx_size)])
        if n_gpu := self.server_args.get("n_gpu_layers"):
            cmd.extend(["--n-gpu-layers", str(n_gpu)])
        if threads := self.server_args.get("threads"):
            cmd.extend(["--threads", str(threads)])

        # Start process
        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to be ready
        self._wait_for_server()
        print(f"Llamafile server started on port {self.llamafile['port']}")
        return self._process

    def _check_server_running(self) -> bool:
        """Check if server is already running."""
        url = f"http://{self.llamafile['host']}:{self.llamafile['port']}/health"
        try:
            response = httpx.get(url, timeout=2)
            return response.status_code == 200
        except httpx.RequestError:
            return False

    def _wait_for_server(self, timeout: int = 30) -> None:
        """Wait for server to respond to health checks."""
        url = f"http://{self.llamafile['host']}:{self.llamafile['port']}/health"
        start = time.time()
        while time.time() - start < timeout:
            try:
                response = httpx.get(url, timeout=2)
                if response.status_code == 200:
                    return
            except httpx.RequestError:
                pass
            time.sleep(0.5)
        raise TimeoutError(f"Server did not start within {timeout} seconds")

    def stop_server(self) -> None:
        """Stop the llamafile server if running."""
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=10)
            self._process = None
```

```python
# main.py
import litellm
from config_loader import LlamafileConfig


def main():
    # Load configuration and start server
    config = LlamafileConfig("config.toml")
    config.start_server()

    try:
        # Make API request using configuration
        response = litellm.completion(
            model=config.ai["model"],
            messages=[
                {"role": "user", "content": "Explain machine learning in one paragraph"}
            ],
            api_base=config.llamafile["api_base"],
            temperature=config.ai["temperature"],
            max_tokens=config.ai["max_tokens"],
        )

        print(response.choices[0].message.content)

    finally:
        # Clean up
        config.stop_server()


if __name__ == "__main__":
    main()
```

**Result**: Application with centralized configuration that automatically manages llamafile server lifecycle.

---

## Example 4: Multi-Model Switching

**Scenario**: Application that switches between different models based on task requirements.

**Steps**:

1. Define model configurations for different use cases
2. Implement model switching with server restart
3. Route requests to appropriate model based on task type

**Code**:

```python
# multi_model_manager.py
import subprocess
import time
import httpx
from typing import Literal, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    name: str
    path: str
    context_size: int
    use_case: str


class MultiModelManager:
    """Manage multiple llamafile models with automatic switching."""

    MODELS = {
        "fast": ModelConfig(
            name="Qwen3-0.6B",
            path="~/.local/share/llamafile/models/qwen3-0.6b.gguf",
            context_size=2048,
            use_case="Quick responses, simple tasks"
        ),
        "balanced": ModelConfig(
            name="Gemma-3-3B",
            path="~/.local/share/llamafile/models/gemma-3-3b.gguf",
            context_size=4096,
            use_case="General purpose, balanced quality/speed"
        ),
        "quality": ModelConfig(
            name="Llama-3.1-8B",
            path="~/.local/share/llamafile/models/llama-3.1-8b.gguf",
            context_size=8192,
            use_case="High quality responses, complex tasks"
        ),
    }

    def __init__(self, llamafile_path: str, port: int = 8080):
        self.llamafile_path = llamafile_path
        self.port = port
        self.host = "127.0.0.1"
        self.current_model: Optional[str] = None
        self._process: Optional[subprocess.Popen] = None

    def switch_model(self, model_key: Literal["fast", "balanced", "quality"]) -> None:
        """Switch to a different model."""
        if model_key == self.current_model:
            print(f"Already using {model_key} model")
            return

        model = self.MODELS[model_key]
        print(f"Switching to {model.name} ({model.use_case})")

        # Stop current server
        self.stop_server()

        # Start new server with selected model
        self._start_server(model)
        self.current_model = model_key

    def _start_server(self, model: ModelConfig) -> None:
        """Start llamafile server with specific model."""
        cmd = [
            self.llamafile_path,
            "--server",
            "-m", model.path,
            "--nobrowser",
            "--port", str(self.port),
            "--host", self.host,
            "--ctx-size", str(model.context_size),
            "--n-gpu-layers", "99",
        ]

        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._wait_for_server()
        print(f"{model.name} server ready")

    def stop_server(self) -> None:
        """Stop the current llamafile server."""
        if self._process:
            self._process.terminate()
            self._process.wait(timeout=10)
            self._process = None

    def _wait_for_server(self, timeout: int = 30) -> None:
        """Wait for server to be ready."""
        url = f"http://{self.host}:{self.port}/health"
        start = time.time()
        while time.time() - start < timeout:
            try:
                response = httpx.get(url, timeout=2)
                if response.status_code == 200:
                    return
            except httpx.RequestError:
                pass
            time.sleep(0.5)
        raise TimeoutError("Server did not start in time")


# Usage example
def main():
    import litellm

    manager = MultiModelManager("~/.local/bin/llamafile")

    # Start with fast model for simple task
    manager.switch_model("fast")
    response = litellm.completion(
        model="llamafile/model",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        api_base="http://127.0.0.1:8080/v1",
    )
    print("Fast model:", response.choices[0].message.content)

    # Switch to quality model for complex task
    manager.switch_model("quality")
    response = litellm.completion(
        model="llamafile/model",
        messages=[{"role": "user", "content": "Explain quantum entanglement"}],
        api_base="http://127.0.0.1:8080/v1",
    )
    print("Quality model:", response.choices[0].message.content)

    manager.stop_server()


if __name__ == "__main__":
    main()
```

**Result**: Application can dynamically switch between models optimized for different task types.

---

## Example 5: Embeddings Generation

**Scenario**: Generate embeddings from text for semantic search or similarity comparisons.

**Steps**:

1. Start llamafile with `--embedding` flag enabled
2. Use embeddings API endpoint
3. Calculate similarity between texts

**Code**:

```bash
# Start server with embeddings enabled
./llamafile --server \
    -m gemma-3-3b.gguf \
    --nobrowser \
    --port 8080 \
    --embedding
```

```python
# embeddings_example.py
import httpx
import numpy as np
from typing import List


def get_embeddings(texts: List[str], api_base: str = "http://localhost:8080/v1") -> np.ndarray:
    """Get embeddings for a list of texts."""
    response = httpx.post(
        f"{api_base}/embeddings",
        json={
            "model": "local",
            "input": texts,
        },
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    embeddings = [item["embedding"] for item in data["data"]]
    return np.array(embeddings)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    # Example texts
    texts = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with multiple layers",
        "Python is a popular programming language",
    ]

    # Get embeddings
    embeddings = get_embeddings(texts)

    # Calculate similarities
    sim_0_1 = cosine_similarity(embeddings[0], embeddings[1])
    sim_0_2 = cosine_similarity(embeddings[0], embeddings[2])

    print(f"Similarity between text 0 and 1: {sim_0_1:.4f}")
    print(f"Similarity between text 0 and 2: {sim_0_2:.4f}")

    # Expected: sim_0_1 > sim_0_2 (ML/DL more related than ML/Python)


if __name__ == "__main__":
    main()
```

**Result**: Generate embeddings for semantic similarity tasks using local LLM.

---

## Example 6: Docker Containerization

**Scenario**: Run llamafile in a Docker container for consistent deployment across environments.

**Steps**:

1. Create Dockerfile with llamafile installation
2. Build container with model included
3. Run container with port mapping

**Code**:

```dockerfile
# Dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up directories
RUN mkdir -p /app/models

# Download llamafile
RUN curl -L -o /app/llamafile \
    https://github.com/mozilla-ai/llamafile/releases/download/0.9.3/llamafile-0.9.3 \
    && chmod 755 /app/llamafile

# Download model
RUN curl -L -o /app/models/gemma-3-3b.gguf \
    https://huggingface.co/Mozilla/gemma-3-3b-it-gguf/resolve/main/gemma-3-3b-it-Q4_K_M.gguf

WORKDIR /app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start server
CMD ["/app/llamafile", "--server", "-m", "/app/models/gemma-3-3b.gguf", \
     "--nobrowser", "--port", "8080", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  llamafile:
    build: .
    ports:
      - "8080:8080"
    environment:
      - CUDA_VISIBLE_DEVICES=0  # Optional: GPU support
    volumes:
      - ./models:/app/models  # Optional: use host models
    restart: unless-stopped
```

```bash
# Build and run
docker build -t llamafile-server .
docker run -d -p 8080:8080 --name llamafile llamafile-server

# Or use docker-compose
docker-compose up -d

# Test
curl http://localhost:8080/health
```

**Result**: Llamafile running in containerized environment with consistent configuration.

---

## Example 7: Testing and Validation Script

**Scenario**: Automated testing script to verify llamafile server is working correctly.

**Steps**:

1. Check server health endpoint
2. Test chat completions endpoint
3. Validate response format
4. Check performance metrics

**Code**:

```python
#!/usr/bin/env python3
# test_llamafile.py - Validate llamafile server functionality

import httpx
import time
import sys
from typing import Dict, Any


class LlamafileValidator:
    """Test and validate llamafile server functionality."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.api_base = f"{base_url}/v1"
        self.tests_passed = 0
        self.tests_failed = 0

    def test_health(self) -> bool:
        """Test health endpoint."""
        print("Testing health endpoint...")
        try:
            response = httpx.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Health check passed")
                self.tests_passed += 1
                return True
            else:
                print(f"✗ Health check failed: status {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            self.tests_failed += 1
            return False

    def test_chat_completions(self) -> bool:
        """Test chat completions endpoint."""
        print("Testing chat completions...")
        try:
            start = time.time()
            response = httpx.post(
                f"{self.api_base}/chat/completions",
                json={
                    "model": "test",
                    "messages": [{"role": "user", "content": "Say 'Hello, World!'"}],
                    "max_tokens": 50,
                    "temperature": 0.3,
                },
                timeout=30,
            )
            elapsed = time.time() - start

            if response.status_code != 200:
                print(f"✗ Chat completions failed: status {response.status_code}")
                self.tests_failed += 1
                return False

            data = response.json()

            # Validate response structure
            if "choices" not in data or not data["choices"]:
                print("✗ Invalid response structure: missing choices")
                self.tests_failed += 1
                return False

            content = data["choices"][0].get("message", {}).get("content", "")
            print(f"✓ Chat completions passed (response: {content[:50]}...)")
            print(f"  Response time: {elapsed:.2f}s")
            self.tests_passed += 1
            return True

        except Exception as e:
            print(f"✗ Chat completions failed: {e}")
            self.tests_failed += 1
            return False

    def test_completions(self) -> bool:
        """Test text completions endpoint."""
        print("Testing text completions...")
        try:
            response = httpx.post(
                f"{self.api_base}/completions",
                json={
                    "model": "test",
                    "prompt": "The capital of France is",
                    "max_tokens": 20,
                },
                timeout=30,
            )

            if response.status_code != 200:
                print(f"✗ Text completions failed: status {response.status_code}")
                self.tests_failed += 1
                return False

            data = response.json()
            if "choices" not in data or not data["choices"]:
                print("✗ Invalid response structure")
                self.tests_failed += 1
                return False

            text = data["choices"][0].get("text", "")
            print(f"✓ Text completions passed (response: {text[:50]}...)")
            self.tests_passed += 1
            return True

        except Exception as e:
            print(f"✗ Text completions failed: {e}")
            self.tests_failed += 1
            return False

    def run_all_tests(self) -> bool:
        """Run all validation tests."""
        print(f"Validating llamafile server at {self.base_url}\n")

        self.test_health()
        self.test_chat_completions()
        self.test_completions()

        print(f"\nResults: {self.tests_passed} passed, {self.tests_failed} failed")

        return self.tests_failed == 0


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate llamafile server")
    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="Base URL of llamafile server",
    )
    args = parser.parse_args()

    validator = LlamafileValidator(args.url)
    success = validator.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

```bash
# Run validation
chmod +x test_llamafile.py
./test_llamafile.py

# Test remote server
./test_llamafile.py --url http://192.168.1.100:8080
```

**Result**: Automated validation ensures llamafile server is functioning correctly with all endpoints accessible.

---

## Additional Resources

For more examples and detailed guidance, refer to:

- [Main README](../README.md) - Plugin overview and quick start
- [Llamafile Skill](../skills/llamafile/SKILL.md) - Complete technical reference
- [Mozilla llamafile Documentation](https://mozilla-ai.github.io/llamafile/) - Official docs
- [LiteLLM llamafile Provider](https://docs.litellm.ai/docs/providers/llamafile) - Integration guide
