# Usage Examples

Concrete, real-world examples of using the LiteLLM plugin for various integration scenarios.

---

## Example 1: Local Llamafile Development Workflow

**Scenario**: You're developing an AI-powered CLI tool that needs to work with local llamafile models for fast iteration without API costs.

**Steps**:
1. Start llamafile server with your chosen model
2. Configure LiteLLM to connect to local endpoint
3. Implement async service wrapper for clean integration
4. Add connection verification for better error messages

**Code**:

```python
import litellm
from litellm import acompletion, APIConnectionError
import asyncio


class LocalLLMService:
    """Service wrapper for llamafile integration via LiteLLM."""

    def __init__(
        self,
        model: str = "llamafile/gemma-3-3b",
        api_base: str = "http://localhost:8080/v1",
        temperature: float = 0.3,
        max_tokens: int = 200,
    ):
        self.model = model
        self.api_base = api_base
        self.temperature = temperature
        self.max_tokens = max_tokens

    def verify_connection(self) -> bool:
        """Check if llamafile server is accessible."""
        try:
            litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                api_base=self.api_base,
                max_tokens=1,
            )
            return True
        except APIConnectionError as e:
            print(f"Connection failed: {e.message}")
            return False

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate completion with optional system prompt."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                api_base=self.api_base,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()
        except APIConnectionError as e:
            raise RuntimeError(
                f"Failed to connect to llamafile at {self.api_base}. "
                f"Is the server running? Error: {e.message}"
            )


# Usage
async def main():
    service = LocalLLMService()

    # Verify connection first
    if not service.verify_connection():
        print("Please start llamafile server: llamafile -m model.gguf --server")
        return

    # Generate commit message
    diff = """
    + def calculate_total(items):
    +     return sum(item.price for item in items)
    """

    message = await service.generate(
        prompt=f"Generate a conventional commit message for:\n{diff}",
        system_prompt="You write concise git commit messages following conventional commits.",
    )

    print(f"Generated: {message}")


asyncio.run(main())
```

**Result**: Clean service abstraction with proper error handling and connection verification, suitable for production CLI tools.

---

## Example 2: Multi-Provider Fallback Chain

**Scenario**: You need high availability for your AI application - if the primary llamafile server is down, fall back to a cloud provider.

**Steps**:
1. Define provider chain (llamafile → OpenAI)
2. Implement retry logic with provider switching
3. Track which provider successfully responded
4. Log provider usage for cost optimization

**Code**:

```python
import litellm
from litellm import APIConnectionError, RateLimitError
import openai


class MultiProviderLLM:
    """LLM service with automatic provider fallback."""

    def __init__(self):
        self.providers = [
            {
                "name": "llamafile",
                "model": "llamafile/gemma-3-3b",
                "api_base": "http://localhost:8080/v1",
                "cost": 0.0,  # Free
            },
            {
                "name": "openai",
                "model": "gpt-4o-mini",
                "cost": 0.00015,  # Per 1K tokens
            },
        ]
        self.last_used_provider = None

    def complete(self, messages: list[dict], temperature: float = 0.3, max_tokens: int = 200) -> str:
        """Try each provider until one succeeds."""
        errors = []

        for provider in self.providers:
            try:
                kwargs = {
                    "model": provider["model"],
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                # Add api_base for llamafile
                if "api_base" in provider:
                    kwargs["api_base"] = provider["api_base"]

                response = litellm.completion(**kwargs)
                self.last_used_provider = provider["name"]

                print(f"✓ Used provider: {provider['name']} (cost: ${provider['cost']}/1K tokens)")
                return response.choices[0].message.content.strip()

            except (APIConnectionError, openai.APITimeoutError) as e:
                errors.append(f"{provider['name']}: {e}")
                print(f"✗ Provider {provider['name']} failed, trying next...")
                continue

            except RateLimitError as e:
                errors.append(f"{provider['name']}: Rate limited")
                print(f"✗ Provider {provider['name']} rate limited, trying next...")
                continue

        # All providers failed
        raise RuntimeError(
            f"All providers failed:\n" + "\n".join(errors)
        )


# Usage
service = MultiProviderLLM()

try:
    result = service.complete(
        messages=[{"role": "user", "content": "Explain quantum computing in one sentence"}]
    )
    print(f"\nResponse: {result}")
    print(f"Provider used: {service.last_used_provider}")

except RuntimeError as e:
    print(f"Error: {e}")
```

**Result**: Automatic failover to cloud providers when local llamafile is unavailable, with cost tracking for optimization decisions.

---

## Example 3: Streaming Chat Application

**Scenario**: Build a real-time chat interface with streaming responses for better UX.

**Steps**:
1. Set up async streaming with LiteLLM
2. Process chunks as they arrive
3. Handle connection errors gracefully
4. Display streaming status to user

**Code**:

```python
from litellm import acompletion
from litellm import APIConnectionError
import asyncio
import sys


class StreamingChat:
    """Interactive streaming chat with llamafile."""

    def __init__(
        self,
        model: str = "llamafile/gemma-3-3b",
        api_base: str = "http://localhost:8080/v1",
    ):
        self.model = model
        self.api_base = api_base
        self.conversation = []

    async def send_message(self, user_message: str) -> str:
        """Send message and stream response."""
        self.conversation.append({"role": "user", "content": user_message})

        try:
            response = await acompletion(
                model=self.model,
                messages=self.conversation,
                api_base=self.api_base,
                stream=True,
                temperature=0.7,
            )

            assistant_message = ""
            print("\nAssistant: ", end="", flush=True)

            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    assistant_message += content
                    print(content, end="", flush=True)

            print()  # Newline after response
            self.conversation.append({"role": "assistant", "content": assistant_message})
            return assistant_message

        except APIConnectionError as e:
            error_msg = f"Connection error: {e.message}"
            print(f"\n✗ {error_msg}")
            return error_msg

    def clear_history(self):
        """Clear conversation history."""
        self.conversation = []


async def main():
    chat = StreamingChat()

    print("Streaming Chat (type 'exit' to quit, 'clear' to reset)")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "clear":
            chat.clear_history()
            print("✓ History cleared")
            continue
        elif not user_input:
            continue

        await chat.send_message(user_input)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
```

**Result**: Interactive streaming chat with conversation history and graceful error handling.

---

## Example 4: Batch Processing with Cost Tracking

**Scenario**: Process a large dataset through LLM with automatic cost calculation and rate limiting awareness.

**Steps**:
1. Set up batch processing pipeline
2. Track token usage and costs
3. Handle rate limits with backoff
4. Generate processing report

**Code**:

```python
import litellm
from litellm import completion, RateLimitError
import time
from typing import List, Dict


class BatchProcessor:
    """Process multiple items through LLM with cost tracking."""

    def __init__(
        self,
        model: str = "llamafile/gemma-3-3b",
        api_base: str = "http://localhost:8080/v1",
    ):
        self.model = model
        self.api_base = api_base
        self.total_tokens = 0
        self.total_cost = 0.0
        self.processed_count = 0
        self.failed_count = 0

    def process_item(
        self,
        item: str,
        system_prompt: str,
        max_retries: int = 3,
    ) -> Dict:
        """Process single item with retry logic."""
        for attempt in range(max_retries):
            try:
                response = completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": item},
                    ],
                    api_base=self.api_base,
                    temperature=0.3,
                    max_tokens=150,
                )

                # Track usage
                usage = response.usage
                self.total_tokens += usage.total_tokens
                # Note: llamafile is free, but this demonstrates cost tracking
                self.total_cost += litellm.completion_cost(completion_response=response)
                self.processed_count += 1

                return {
                    "success": True,
                    "result": response.choices[0].message.content,
                    "tokens": usage.total_tokens,
                }

            except RateLimitError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    self.failed_count += 1
                    return {"success": False, "error": "Rate limit exceeded"}

        self.failed_count += 1
        return {"success": False, "error": "Max retries exceeded"}

    def process_batch(
        self,
        items: List[str],
        system_prompt: str,
    ) -> List[Dict]:
        """Process batch of items."""
        results = []
        start_time = time.time()

        for i, item in enumerate(items, 1):
            print(f"Processing {i}/{len(items)}...", end=" ")
            result = self.process_item(item, system_prompt)

            if result["success"]:
                print(f"✓ ({result['tokens']} tokens)")
            else:
                print(f"✗ {result['error']}")

            results.append(result)

        elapsed = time.time() - start_time
        self._print_summary(elapsed)

        return results

    def _print_summary(self, elapsed: float):
        """Print processing summary."""
        print("\n" + "=" * 50)
        print("Batch Processing Summary")
        print("=" * 50)
        print(f"Processed: {self.processed_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Total tokens: {self.total_tokens:,}")
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Time elapsed: {elapsed:.2f}s")
        print(f"Avg time/item: {elapsed/self.processed_count:.2f}s")


# Usage
processor = BatchProcessor()

git_diffs = [
    "+ def calculate_total(items): return sum(i.price for i in items)",
    "+ class User: pass",
    "+ import logging; logger = logging.getLogger(__name__)",
]

results = processor.process_batch(
    items=git_diffs,
    system_prompt="Generate a conventional commit message (feat/fix/docs/etc). Be concise.",
)

for i, result in enumerate(results, 1):
    if result["success"]:
        print(f"\n{i}. {result['result']}")
```

**Result**: Efficient batch processing with automatic cost tracking, retry logic, and detailed reporting.

---

## Example 5: Embeddings Generation for RAG

**Scenario**: Generate embeddings for a document collection using local llamafile embedding models.

**Steps**:
1. Configure llamafile with embedding model
2. Use LiteLLM embedding API
3. Process documents in batches
4. Store embeddings for retrieval

**Code**:

```python
from litellm import embedding
import os
from typing import List
import numpy as np


class EmbeddingService:
    """Generate embeddings using llamafile via LiteLLM."""

    def __init__(
        self,
        model: str = "llamafile/sentence-transformers/all-MiniLM-L6-v2",
        api_base: str = "http://localhost:8080/v1",
    ):
        self.model = model
        os.environ["LLAMAFILE_API_BASE"] = api_base

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents."""
        response = embedding(
            model=self.model,
            input=documents,
        )

        # Extract embeddings from response
        return [item["embedding"] for item in response.data]

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query."""
        response = embedding(
            model=self.model,
            input=[query],
        )

        return response.data[0]["embedding"]

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# Usage
service = EmbeddingService()

# Document collection
documents = [
    "Python is a high-level programming language",
    "JavaScript is used for web development",
    "Machine learning uses statistical algorithms",
    "Docker containers isolate applications",
]

# Generate embeddings
print("Generating document embeddings...")
doc_embeddings = service.embed_documents(documents)
print(f"Generated {len(doc_embeddings)} embeddings of dimension {len(doc_embeddings[0])}")

# Query and find most similar
query = "What is Python?"
query_embedding = service.embed_query(query)

print(f"\nQuery: {query}")
print("Similarities:")

for i, doc in enumerate(documents):
    similarity = service.cosine_similarity(query_embedding, doc_embeddings[i])
    print(f"  {similarity:.4f} - {doc}")
```

**Result**: Local embedding generation for semantic search and RAG applications without external API dependencies.

---

## Example 6: Environment-Based Configuration

**Scenario**: Support multiple deployment environments (dev/staging/prod) with different LLM backends.

**Steps**:
1. Create environment-aware configuration
2. Load provider settings from environment
3. Implement configuration validation
4. Support both local and cloud deployments

**Code**:

```python
import litellm
from litellm import completion
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """LLM configuration for different environments."""

    model: str
    api_base: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 200
    environment: str = "dev"

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Load configuration from environment variables."""
        env = os.getenv("APP_ENV", "dev")

        configs = {
            "dev": cls(
                model="llamafile/gemma-3-3b",
                api_base="http://localhost:8080/v1",
                environment="dev",
            ),
            "staging": cls(
                model="llamafile/mistralai/mistral-7b-instruct-v0.2",
                api_base=os.getenv("STAGING_LLM_URL", "http://staging-llm:8080/v1"),
                environment="staging",
            ),
            "prod": cls(
                model=os.getenv("PROD_LLM_MODEL", "gpt-4o-mini"),
                # api_base not set - uses default cloud endpoint
                environment="prod",
                temperature=0.2,  # More conservative in prod
            ),
        }

        return configs.get(env, configs["dev"])

    def validate(self) -> bool:
        """Validate configuration is usable."""
        try:
            kwargs = {
                "model": self.model,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 1,
            }

            if self.api_base:
                kwargs["api_base"] = self.api_base

            completion(**kwargs)
            return True

        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False


class ConfiguredLLMService:
    """LLM service with environment-based configuration."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
        print(f"Loaded configuration for: {self.config.environment}")
        print(f"  Model: {self.config.model}")
        print(f"  API Base: {self.config.api_base or 'default'}")

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate completion using configured settings."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        if self.config.api_base:
            kwargs["api_base"] = self.config.api_base

        response = completion(**kwargs)
        return response.choices[0].message.content.strip()


# Usage
if __name__ == "__main__":
    # Load config from environment
    config = LLMConfig.from_env()

    # Validate before using
    if not config.validate():
        print("Error: Invalid configuration")
        exit(1)

    # Create service
    service = ConfiguredLLMService(config)

    # Use service
    result = service.generate("Write a haiku about coding")
    print(f"\nResponse:\n{result}")
```

**Result**: Clean environment-based configuration supporting local development and cloud production deployments with validation.

---

For more information, see the [main README](../README.md) or [troubleshooting guide](./troubleshooting.md).
