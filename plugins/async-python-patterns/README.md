# Async Python Patterns

Helps Claude write better asynchronous Python code using modern asyncio patterns.

## Why Install This?

When you ask Claude to write async Python code, you might get:
- Outdated patterns or incorrect async/await usage
- Missing error handling and timeouts
- Inefficient sequential code instead of concurrent operations
- Common pitfalls like blocking the event loop

This plugin teaches Claude modern asyncio best practices and proven patterns.

## What Changes

With this plugin installed, Claude will:
- Use proper async/await syntax and patterns
- Implement concurrent operations with `asyncio.gather()` and task management
- Add appropriate error handling, timeouts, and cancellation support
- Apply rate limiting with semaphores when making many API calls
- Use async context managers and iterators correctly
- Structure producer-consumer patterns properly
- Avoid common mistakes like forgetting `await` or blocking the event loop

## Installation

```bash
/plugin install async-python-patterns
```

## Usage

Just install it and Claude will automatically apply these patterns when you work with async Python code.

## Example

**Without this plugin**: You say "write code to fetch 100 URLs concurrently". Claude might write sequential code with blocking operations, no error handling, and no rate limiting.

**With this plugin**: Same request, but Claude writes code using `aiohttp` with connection pools, `asyncio.gather()` for concurrency, semaphores to limit concurrent requests, proper timeout handling, and graceful error recovery.

## When This Helps

- Building async web APIs with FastAPI or aiohttp
- Writing web scrapers with concurrent requests
- Creating real-time applications like WebSocket servers
- Working with async database operations
- Implementing background task queues
- Any I/O-bound workload requiring non-blocking operations

## Requirements

- Claude Code v2.0+
