# Changelog

All notable changes to the async-python-patterns plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-18

### Added

- Initial release of async-python-patterns plugin
- Comprehensive async Python patterns skill with 10 fundamental and advanced patterns
- Core concepts documentation: event loops, coroutines, tasks, futures, async context managers, async iterators
- Fundamental patterns:
  - Basic async/await syntax
  - Concurrent execution with `asyncio.gather()`
  - Task creation and management
  - Error handling in async code
  - Timeout handling
- Advanced patterns:
  - Async context managers
  - Async iterators and generators
  - Producer-consumer pattern
  - Semaphore for rate limiting
  - Async locks and synchronization
- Real-world application examples:
  - Web scraping with aiohttp
  - Async database operations
  - WebSocket server implementation
- Performance best practices:
  - Connection pooling
  - Batch processing
  - Executor pattern for blocking operations
- Common pitfalls documentation:
  - Forgetting await
  - Blocking the event loop
  - Improper cancellation handling
  - Mixing sync and async code
- Testing guidance with pytest-asyncio
- Complete plugin documentation:
  - README.md with installation, features, and quick start
  - docs/skills.md with detailed skill reference
  - docs/examples.md with 5 real-world examples
- MIT License
- Changelog

### Documentation

- README.md: Main entry point with badges, installation, features, usage examples
- docs/skills.md: Comprehensive skill documentation with activation patterns and content overview
- docs/examples.md: 5 production-ready examples:
  1. Concurrent web scraper with rate limiting
  2. Async database operations with connection pooling
  3. WebSocket chat server with room management
  4. Task queue with background workers and retry logic
  5. API client with rate limiting and caching

## [Unreleased]

### Planned

- Python 3.11+ TaskGroups pattern
- Structured concurrency patterns
- asyncio debugging techniques
- Performance profiling guidance
- Migration strategies from sync to async
- Additional real-world examples:
  - Async file processing
  - Event-driven architecture patterns
  - Distributed task coordination
- Integration examples with popular frameworks:
  - FastAPI advanced patterns
  - Django async views
  - Sanic optimization

[1.0.0]: https://github.com/username/claude_skills/releases/tag/v1.0.0
