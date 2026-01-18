# Troubleshooting Guide

Common issues and solutions when using LiteLLM with llamafile and other providers.

---

## Connection Issues

### Problem: `APIConnectionError` when connecting to llamafile

**Symptoms**:
```
litellm.APIConnectionError: Connection refused at http://localhost:8080/v1
```

**Solutions**:

1. **Verify llamafile server is running**:
   ```bash
   # Check if server is accessible
   curl http://localhost:8080/v1/models

   # Should return JSON with model list
   ```

2. **Check the port**:
   ```python
   # Default llamafile port is 8080, not 8000
   api_base = "http://localhost:8080/v1"  # Correct
   api_base = "http://localhost:8000/v1"  # Wrong
   ```

3. **Verify `/v1` suffix**:
   ```python
   api_base = "http://localhost:8080/v1"     # Correct
   api_base = "http://localhost:8080"        # Wrong - missing /v1
   api_base = "http://localhost:8080/v1/chat/completions"  # Wrong - too specific
   ```

4. **Start llamafile if not running**:
   ```bash
   # Start llamafile server
   llamafile -m your-model.gguf --server

   # Or with specific port
   llamafile -m your-model.gguf --server --port 8080
   ```

---

### Problem: Connection works with curl but not LiteLLM

**Symptoms**:
- `curl http://localhost:8080/v1/models` works
- LiteLLM raises `APIConnectionError`

**Solutions**:

1. **Check model name has correct prefix**:
   ```python
   # Correct - with llamafile/ prefix
   model = "llamafile/mistralai/mistral-7b-instruct-v0.2"

   # Wrong - missing prefix (LiteLLM won't route correctly)
   model = "mistralai/mistral-7b-instruct-v0.2"
   ```

2. **Enable debug logging**:
   ```python
   import os
   os.environ["LITELLM_LOG"] = "DEBUG"

   import litellm
   # Now all requests/responses are logged
   ```

3. **Test with minimal example**:
   ```python
   import litellm

   response = litellm.completion(
       model="llamafile/test",
       messages=[{"role": "user", "content": "hi"}],
       api_base="http://localhost:8080/v1",
       max_tokens=1,
   )
   print("Connection successful!")
   ```

---

## Model Issues

### Problem: Model not found error

**Symptoms**:
```
litellm.NotFoundError: 404 - Model not found
```

**Solutions**:

1. **Verify model is loaded in llamafile**:
   ```bash
   curl http://localhost:8080/v1/models
   ```

2. **Check model name format**:
   ```python
   # The model name after llamafile/ can be anything
   # It doesn't need to match the actual model file name
   model = "llamafile/my-model"        # Works
   model = "llamafile/any-name-here"   # Also works

   # Just ensure llamafile/ prefix is present
   ```

3. **Use generic model name**:
   ```python
   # For llamafile, the model name is primarily for routing
   # You can use a simple name if the exact model doesn't matter
   model = "llamafile/model"
   ```

---

### Problem: Wrong model responses or behavior

**Symptoms**:
- Responses don't match expected model capabilities
- Quality differs from direct llamafile access

**Solutions**:

1. **Verify you're hitting llamafile**:
   ```python
   from litellm import completion

   response = completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "What model are you?"}],
       api_base="http://localhost:8080/v1",
   )
   # Check if response indicates correct model
   ```

2. **Check llamafile server logs**:
   ```bash
   # Look for incoming requests in llamafile terminal
   # Should see POST /v1/chat/completions
   ```

3. **Test direct llamafile API**:
   ```bash
   curl http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [{"role": "user", "content": "test"}]
     }'
   ```

---

## Timeout Issues

### Problem: Requests timeout frequently

**Symptoms**:
```
openai.APITimeoutError: Request timed out
```

**Solutions**:

1. **Increase timeout**:
   ```python
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "Long prompt..."}],
       api_base="http://localhost:8080/v1",
       timeout=60.0,  # Increase from default 30s
   )
   ```

2. **Reduce max_tokens for faster responses**:
   ```python
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "Be brief"}],
       api_base="http://localhost:8080/v1",
       max_tokens=50,  # Limit response length
   )
   ```

3. **Check system resources**:
   ```bash
   # Llamafile might be slow if system is under load
   top
   # Check CPU/RAM usage
   ```

4. **Use faster model**:
   ```python
   # Switch to smaller/faster model for development
   model = "llamafile/gemma-3-3b"  # Faster
   # Instead of:
   # model = "llamafile/mistralai/mistral-7b-instruct-v0.2"  # Slower
   ```

---

## Exception Handling Issues

### Problem: Exceptions not caught properly

**Symptoms**:
- `except litellm.APIConnectionError` doesn't catch errors
- Unexpected exception types

**Solutions**:

1. **Import from both litellm and openai**:
   ```python
   import litellm
   import openai

   try:
       response = litellm.completion(...)
   except openai.APITimeoutError:  # Inherits from OpenAI
       print("Timeout")
   except litellm.APIConnectionError:  # LiteLLM specific
       print("Connection failed")
   except openai.APIError:  # Generic fallback
       print("API error")
   ```

2. **Check exception inheritance**:
   ```python
   import litellm

   # LiteLLM exceptions inherit from OpenAI equivalents
   # Can catch either way:
   try:
       response = litellm.completion(...)
   except litellm.Timeout:  # LiteLLM alias
       pass
   # OR
   except openai.APITimeoutError:  # OpenAI base
       pass
   ```

3. **Use broad exception for debugging**:
   ```python
   try:
       response = litellm.completion(...)
   except Exception as e:
       print(f"Exception type: {type(e)}")
       print(f"Exception message: {e}")
       if hasattr(e, 'status_code'):
           print(f"Status code: {e.status_code}")
       if hasattr(e, 'llm_provider'):
           print(f"Provider: {e.llm_provider}")
   ```

---

## Streaming Issues

### Problem: Streaming returns empty chunks

**Symptoms**:
- Stream starts but no content appears
- Chunks exist but `delta.content` is None

**Solutions**:

1. **Check for None content**:
   ```python
   async for chunk in response:
       # Some chunks don't have content (metadata chunks)
       if chunk.choices[0].delta.content:  # Check before using
           print(chunk.choices[0].delta.content, end="", flush=True)
   ```

2. **Verify streaming is enabled**:
   ```python
   response = await acompletion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "test"}],
       api_base="http://localhost:8080/v1",
       stream=True,  # Must be True
   )
   ```

3. **Test without streaming first**:
   ```python
   # If non-streaming works, streaming should too
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "test"}],
       api_base="http://localhost:8080/v1",
       stream=False,  # Disable streaming for testing
   )
   print(response.choices[0].message.content)
   ```

---

## Environment Variable Issues

### Problem: Environment variables not working

**Symptoms**:
- `os.environ["LLAMAFILE_API_BASE"]` set but still need `api_base` parameter
- Credentials not recognized

**Solutions**:

1. **Set environment variables before importing**:
   ```python
   import os
   # Set BEFORE importing litellm
   os.environ["LLAMAFILE_API_BASE"] = "http://localhost:8080/v1"

   import litellm
   # Now can omit api_base parameter
   ```

2. **Verify variable names**:
   ```python
   # Correct environment variable names:
   os.environ["LLAMAFILE_API_BASE"] = "..."     # For llamafile
   os.environ["OPENAI_API_KEY"] = "..."         # For OpenAI
   os.environ["ANTHROPIC_API_KEY"] = "..."      # For Anthropic
   ```

3. **Explicit parameters override env vars**:
   ```python
   # Explicit api_base takes precedence over environment variable
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "test"}],
       api_base="http://localhost:9000/v1",  # Overrides LLAMAFILE_API_BASE
   )
   ```

---

## Performance Issues

### Problem: Slow response times

**Symptoms**:
- Requests take longer than expected
- High latency compared to direct llamafile access

**Solutions**:

1. **Profile the request**:
   ```python
   import time
   import litellm

   start = time.time()
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "test"}],
       api_base="http://localhost:8080/v1",
   )
   elapsed = time.time() - start
   print(f"Request took {elapsed:.2f}s")
   ```

2. **Use async for better throughput**:
   ```python
   from litellm import acompletion
   import asyncio

   async def concurrent_requests():
       tasks = [
           acompletion(
               model="llamafile/gemma-3-3b",
               messages=[{"role": "user", "content": f"Request {i}"}],
               api_base="http://localhost:8080/v1",
           )
           for i in range(5)
       ]
       return await asyncio.gather(*tasks)

   # Much faster than sequential
   results = asyncio.run(concurrent_requests())
   ```

3. **Reduce token limits**:
   ```python
   response = litellm.completion(
       model="llamafile/gemma-3-3b",
       messages=[{"role": "user", "content": "Be concise"}],
       api_base="http://localhost:8080/v1",
       max_tokens=100,  # Limit response length
       temperature=0.2,  # Lower temperature can be faster
   )
   ```

---

## Import Issues

### Problem: Cannot import LiteLLM or exceptions

**Symptoms**:
```python
ImportError: No module named 'litellm'
```

**Solutions**:

1. **Install LiteLLM**:
   ```bash
   # Using pip
   pip install litellm

   # Using uv
   uv add litellm

   # Verify installation
   python -c "import litellm; print(litellm.__version__)"
   ```

2. **Check Python environment**:
   ```bash
   # Ensure you're in correct virtual environment
   which python
   python -m pip list | grep litellm
   ```

3. **Update to latest version**:
   ```bash
   pip install --upgrade litellm
   ```

---

## Debugging Techniques

### Enable verbose logging

```python
import os
import logging

# Enable LiteLLM debug logging
os.environ["LITELLM_LOG"] = "DEBUG"

# Enable Python logging
logging.basicConfig(level=logging.DEBUG)

import litellm
# Now all requests/responses are logged
```

### Test connection manually

```python
import litellm
from litellm import APIConnectionError

def test_connection(api_base: str = "http://localhost:8080/v1") -> bool:
    """Test if LiteLLM can connect to llamafile."""
    try:
        response = litellm.completion(
            model="llamafile/test",
            messages=[{"role": "user", "content": "test"}],
            api_base=api_base,
            max_tokens=1,
        )
        print(f"✓ Connection successful to {api_base}")
        return True
    except APIConnectionError as e:
        print(f"✗ Connection failed: {e.message}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

# Run test
test_connection()
```

### Inspect response object

```python
response = litellm.completion(
    model="llamafile/gemma-3-3b",
    messages=[{"role": "user", "content": "test"}],
    api_base="http://localhost:8080/v1",
)

print(f"Model: {response.model}")
print(f"Tokens: {response.usage.total_tokens}")
print(f"Content: {response.choices[0].message.content}")
print(f"Full response: {response}")
```

---

## Getting Help

### Check LiteLLM documentation

- [Official Docs](https://docs.litellm.ai/)
- [Llamafile Provider](https://docs.litellm.ai/docs/providers/llamafile)
- [Exception Mapping](https://docs.litellm.ai/docs/exception_mapping)

### Verify llamafile setup

- [Llamafile Documentation](https://github.com/Mozilla-Ocho/llamafile)
- [API Endpoints](https://github.com/Mozilla-Ocho/llamafile/blob/main/llama.cpp/server/README.md#api-endpoints)

### Community support

- [LiteLLM GitHub Issues](https://github.com/BerriAI/litellm/issues)
- [LiteLLM Discord](https://discord.gg/wuPM9dRgDw)

---

## Common Configuration Patterns

### Development setup

```python
import os

# Local llamafile for development
os.environ["LLAMAFILE_API_BASE"] = "http://localhost:8080/v1"

config = {
    "model": "llamafile/gemma-3-3b",
    "temperature": 0.7,  # Higher for creative tasks
    "max_tokens": 200,
}
```

### Production setup

```python
import os

# Cloud provider for production
config = {
    "model": "gpt-4o-mini",  # No api_base needed
    "temperature": 0.2,  # Lower for consistency
    "max_tokens": 150,
    "num_retries": 3,
    "timeout": 30.0,
}
```

### Multi-environment setup

```python
import os

env = os.getenv("APP_ENV", "dev")

configs = {
    "dev": {
        "model": "llamafile/gemma-3-3b",
        "api_base": "http://localhost:8080/v1",
    },
    "prod": {
        "model": "gpt-4o-mini",
        # Uses default OpenAI endpoint
    },
}

config = configs[env]
```

---

For more examples, see [examples.md](./examples.md). Return to [main README](../README.md) for overview.
