# Async Python Patterns

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Master Python asyncio, concurrent programming, and async/await patterns for building high-performance, non-blocking applications. This plugin provides comprehensive guidance for implementing asynchronous systems with Python's asyncio library.

## Features

- **Complete asyncio fundamentals** - Event loops, coroutines, tasks, futures, and async/await syntax
- **10 production-ready patterns** - From basic async operations to advanced synchronization primitives
- **Real-world applications** - Web scraping with aiohttp, async database operations, WebSocket servers
- **Performance optimization** - Connection pooling, batch processing, and executor patterns
- **Error handling strategies** - Timeout management, cancellation handling, and exception propagation
- **Testing guidance** - pytest-asyncio patterns and async test best practices
- **Common pitfall prevention** - Learn what to avoid when writing async code

## Installation

### Prerequisites

- Claude Code 2.1 or later
- Python 3.7+ (for asyncio.run() and modern async features)

### Install Plugin

#### Method 1: From Local Repository

```bash
# Navigate to your Claude Code plugins directory
cd ~/.claude/plugins

# Clone or copy the plugin
cp -r /path/to/async-python-patterns .

# Reload Claude Code plugins
cc plugin reload
```

#### Method 2: Via Claude Code CLI

If the plugin is available in a marketplace:

```bash
cc plugin install async-python-patterns
```

### Verify Installation

```bash
# List installed plugins
cc plugin list

# You should see async-python-patterns in the output
```

## Quick Start

Once installed, the plugin is automatically activated when you work on async Python code. Here's a simple example to get started:

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"url": url, "data": "result"}

async def main():
    # Sequential execution
    result1 = await fetch_data("https://api.example.com/1")
    result2 = await fetch_data("https://api.example.com/2")

    # Concurrent execution
    results = await asyncio.gather(
        fetch_data("https://api.example.com/3"),
        fetch_data("https://api.example.com/4"),
        fetch_data("https://api.example.com/5")
    )

    print(f"Fetched {len(results)} results concurrently")

asyncio.run(main())
```

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | async-python-patterns | Comprehensive asyncio guidance with patterns, real-world examples, and best practices | Auto-activated by Claude or `/async-python-patterns` |

## Usage

### Automatic Activation

Claude Code automatically loads the async-python-patterns skill when you:

- Mention "asyncio", "async/await", "concurrent", or "non-blocking" in your requests
- Work on files using `async def` or `await` keywords
- Ask about Python async patterns, event loops, or coroutines
- Build async web APIs, WebSocket servers, or I/O-bound applications

### Manual Activation

You can explicitly activate the skill using:

```text
@async-python-patterns
```

or via the Skill tool:

```text
Skill(command: "async-python-patterns")
```

### Skills

The plugin provides one comprehensive skill:

**async-python-patterns** - [View detailed documentation](./docs/skills.md)

This skill includes:
- Fundamental concepts (event loops, coroutines, tasks, futures)
- 10 production-ready patterns from basic to advanced
- Real-world application examples (web scraping, databases, WebSockets)
- Performance optimization techniques
- Common pitfall avoidance
- Testing strategies with pytest-asyncio

## Examples

### Example 1: Concurrent API Requests

Fetch multiple API endpoints concurrently to improve performance:

```python
import asyncio
import aiohttp
from typing import List, Dict

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict:
    """Fetch single URL with error handling."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            data = await response.json()
            return {"url": url, "status": response.status, "data": data}
    except Exception as e:
        return {"url": url, "error": str(e)}

async def fetch_all(urls: List[str]) -> List[Dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Usage
urls = [
    "https://api.github.com/users/octocat",
    "https://api.github.com/users/torvalds",
    "https://api.github.com/users/gvanrossum"
]

results = asyncio.run(fetch_all(urls))
print(f"Fetched {len(results)} profiles")
```

### Example 2: Producer-Consumer Pattern

Implement a work queue with multiple producers and consumers:

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, producer_id: int):
    """Produce work items."""
    for i in range(5):
        item = f"Task-{producer_id}-{i}"
        await queue.put(item)
        print(f"Producer {producer_id}: {item}")
        await asyncio.sleep(0.1)

async def consumer(queue: Queue, consumer_id: int):
    """Consume and process work items."""
    while True:
        item = await queue.get()
        if item is None:  # Shutdown signal
            queue.task_done()
            break

        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.3)  # Simulate work
        queue.task_done()

async def main():
    queue = Queue(maxsize=10)

    # Start producers and consumers
    producers = [asyncio.create_task(producer(queue, i)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    # Wait for all production
    await asyncio.gather(*producers)

    # Send shutdown signals
    for _ in consumers:
        await queue.put(None)

    # Wait for all consumption
    await asyncio.gather(*consumers)

asyncio.run(main())
```

### Example 3: Rate-Limited Scraping

Scrape multiple pages while respecting rate limits:

```python
import asyncio
import aiohttp
from typing import List

async def scrape_page(session: aiohttp.ClientSession, url: str,
                      semaphore: asyncio.Semaphore) -> dict:
    """Scrape single page with rate limiting."""
    async with semaphore:
        print(f"Scraping: {url}")
        async with session.get(url) as response:
            text = await response.text()
            return {"url": url, "length": len(text), "status": response.status}

async def scrape_with_limit(urls: List[str], max_concurrent: int = 5) -> List[dict]:
    """Scrape multiple URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

# Scrape 20 pages with max 5 concurrent requests
urls = [f"https://example.com/page/{i}" for i in range(1, 21)]
results = asyncio.run(scrape_with_limit(urls, max_concurrent=5))
print(f"Scraped {len(results)} pages")
```

[View more examples](./docs/examples.md)

## When to Use This Plugin

Use the async-python-patterns plugin when working on:

- **Async Web APIs** - FastAPI, aiohttp, Sanic applications
- **Concurrent I/O Operations** - Database queries, file operations, network requests
- **Web Scrapers** - Fetching multiple URLs concurrently
- **Real-Time Applications** - WebSocket servers, chat systems, live data streams
- **Microservices** - Services with async communication patterns
- **I/O-Bound Workloads** - Any application bottlenecked by I/O rather than CPU
- **Background Task Processing** - Async job queues and task schedulers

## Configuration

This plugin has no additional configuration requirements. The skill is automatically available once the plugin is installed and enabled.

### Environment Variables

No environment variables are required for this plugin.

### Customization

The skill content is loaded on-demand, meaning it doesn't consume context tokens until Claude determines it's needed. This ensures efficient use of your context window.

## Troubleshooting

### Plugin Not Loading

If the plugin doesn't appear to be working:

1. Verify installation: `cc plugin list`
2. Check plugin is enabled: `cc plugin enable async-python-patterns`
3. Reload plugins: `cc plugin reload`
4. Restart Claude Code session

### Skill Not Activating

If the skill isn't being used when expected:

1. Try explicit activation: `@async-python-patterns`
2. Use clear async-related keywords: "asyncio", "async/await", "concurrent"
3. Check Claude Code version: Requires 2.1+

### Getting Help

If you encounter issues:

1. Check the [skill documentation](./docs/skills.md) for detailed usage
2. Review the [examples](./docs/examples.md) for working patterns
3. Ensure you're using Python 3.7+ for modern asyncio features

## Best Practices

When using this plugin:

1. **Be specific** - Mention "asyncio" or "async/await" explicitly in your requests
2. **Provide context** - Describe your use case (API, database, WebSocket, etc.)
3. **Ask for patterns** - Request specific patterns like "producer-consumer" or "rate limiting"
4. **Review examples** - Start with the provided examples and adapt to your needs
5. **Test incrementally** - Build async code gradually, testing each pattern

## Contributing

This plugin is part of the claude_skills repository. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes to the skill content
4. Test with Claude Code
5. Submit a pull request

### Guidelines

- Keep examples concise and practical
- Include error handling in all examples
- Add type hints for clarity
- Document performance considerations
- Test examples before submitting

## License

MIT License - See LICENSE file for details

## Credits

**Author**: Claude Skills Repository Contributors

**Resources**:
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp documentation](https://docs.aiohttp.org/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Real Python asyncio guide](https://realpython.com/async-io-python/)

## Version History

### 1.0.0 (2026-01-18)

- Initial release
- 10 fundamental and advanced async patterns
- Real-world application examples (web scraping, databases, WebSockets)
- Performance optimization guidance
- Common pitfall prevention
- Testing strategies with pytest-asyncio
