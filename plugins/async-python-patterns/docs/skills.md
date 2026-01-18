# Skills Reference

This document provides detailed information about the skills included in the async-python-patterns plugin.

## async-python-patterns

**Location**: `skills/async-python-patterns/SKILL.md`

**Description**: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.

**User Invocable**: Yes (default)

**Allowed Tools**: Inherits from session (all tools available)

**Model**: Inherits from session (uses current model)

**Context**: Inline (loaded into main conversation context)

### When to Use

Activate this skill when working on:

1. **Async Web APIs**
   - Building FastAPI applications
   - Creating aiohttp servers or clients
   - Implementing Sanic web services

2. **Concurrent I/O Operations**
   - Database queries with asyncpg or motor
   - File operations with aiofiles
   - Network requests with aiohttp

3. **Web Scraping**
   - Fetching multiple URLs concurrently
   - Rate-limited scraping with semaphores
   - Paginated data collection

4. **Real-Time Applications**
   - WebSocket servers and clients
   - Chat systems with persistent connections
   - Live data streaming services

5. **Background Processing**
   - Async task queues
   - Job scheduling systems
   - Worker pool implementations

6. **Microservices**
   - Services with async communication
   - Event-driven architectures
   - Service mesh implementations

7. **Performance Optimization**
   - Converting blocking I/O to async
   - Optimizing I/O-bound bottlenecks
   - Improving throughput with concurrency

### Activation

**Automatic Activation**:

Claude Code automatically loads this skill when you:
- Mention keywords: "asyncio", "async/await", "concurrent", "non-blocking", "coroutine"
- Work on Python files containing `async def` or `await` keywords
- Ask about event loops, tasks, or futures
- Request help with async libraries (aiohttp, asyncpg, motor)

**Manual Activation**:

```text
@async-python-patterns
```

Or via Skill tool:

```text
Skill(command: "async-python-patterns")
```

### Content Overview

The skill provides comprehensive guidance organized into:

#### 1. Core Concepts (Lines 21-61)

- **Event Loop**: Single-threaded cooperative multitasking, scheduling coroutines
- **Coroutines**: Functions defined with `async def`, pausable and resumable
- **Tasks**: Scheduled coroutines running concurrently on event loop
- **Futures**: Low-level objects representing eventual results
- **Async Context Managers**: Resources supporting `async with`
- **Async Iterators**: Objects supporting `async for`

#### 2. Fundamental Patterns (Lines 76-206)

- **Pattern 1**: Basic async/await syntax and execution
- **Pattern 2**: Concurrent execution with `asyncio.gather()`
- **Pattern 3**: Task creation and management with `asyncio.create_task()`
- **Pattern 4**: Error handling with try/except and `return_exceptions`
- **Pattern 5**: Timeout handling with `asyncio.wait_for()`

#### 3. Advanced Patterns (Lines 207-402)

- **Pattern 6**: Async context managers with `__aenter__` and `__aexit__`
- **Pattern 7**: Async iterators and generators with `yield`
- **Pattern 8**: Producer-consumer pattern with `asyncio.Queue`
- **Pattern 9**: Semaphore for rate limiting and concurrency control
- **Pattern 10**: Async locks and synchronization primitives

#### 4. Real-World Applications (Lines 403-547)

- **Web Scraping**: Complete example with aiohttp and error handling
- **Database Operations**: Concurrent queries with simulated async DB client
- **WebSocket Server**: Client management, broadcasting, message handling

#### 5. Performance Best Practices (Lines 549-609)

- **Connection Pooling**: Using `aiohttp.TCPConnector` for efficiency
- **Batch Processing**: Processing items in manageable chunks
- **Executor Pattern**: Running blocking operations in thread pools

#### 6. Common Pitfalls (Lines 611-661)

- Forgetting `await` keyword
- Blocking the event loop with synchronous operations
- Not handling task cancellation properly
- Mixing sync and async code incorrectly

#### 7. Testing (Lines 663-681)

- Using pytest-asyncio for async tests
- Testing with timeouts
- Mocking async operations

#### 8. Resources (Lines 683-690)

- Links to official documentation
- Recommended async libraries
- Community resources

### Key Features

**Comprehensive Examples**: Every pattern includes working code examples with:
- Type hints for clarity
- Error handling demonstrations
- Performance considerations
- Usage documentation

**Progressive Complexity**: Content organized from basic to advanced:
1. Simple async/await (beginner)
2. Concurrent execution (intermediate)
3. Synchronization primitives (advanced)
4. Production patterns (expert)

**Real-World Focus**: Examples based on actual use cases:
- HTTP clients with connection pooling
- Database query batching
- WebSocket server architecture
- Rate-limited API scraping

**Best Practices**: Embedded throughout content:
- Always use `asyncio.run()` for entry point (Python 3.7+)
- Never block the event loop
- Use semaphores for rate limiting
- Handle cancellation properly
- Test async code with pytest-asyncio

### Usage Examples

#### Example 1: Get Help with Concurrent API Calls

**User Request**:
```text
I need to fetch data from 50 API endpoints as quickly as possible. How should I structure this with asyncio?
```

**Claude Response** (with skill loaded):
- Recommends `asyncio.gather()` for concurrent execution
- Provides example with aiohttp session
- Suggests semaphore for rate limiting
- Includes error handling with `return_exceptions=True`
- Shows connection pooling configuration

#### Example 2: Debug Blocking Event Loop

**User Request**:
```text
My async application seems to hang. I'm using time.sleep() in an async function. Is that okay?
```

**Claude Response** (with skill loaded):
- Identifies `time.sleep()` as blocking operation
- Explains event loop blocking concept
- Recommends replacing with `asyncio.sleep()`
- Suggests executor pattern for CPU-bound work
- References Common Pitfalls section

#### Example 3: Implement Producer-Consumer

**User Request**:
```text
Help me implement a task queue where multiple workers process items from a shared queue
```

**Claude Response** (with skill loaded):
- Provides Pattern 8 (Producer-Consumer) example
- Explains `asyncio.Queue` usage
- Shows graceful shutdown with None sentinel
- Demonstrates `queue.task_done()` for completion tracking
- Includes multiple producers and consumers

### Integration with Other Tools

The skill works seamlessly with:

**Read Tool**: References code examples and patterns from skill content

**Write Tool**: Generates async Python code using patterns from skill

**Edit Tool**: Refactors sync code to async using skill guidance

**Bash Tool**: Can run async Python scripts for testing patterns

### Performance Characteristics

**Context Efficiency**:
- Skill content: ~7000 tokens (loaded on-demand)
- Reference content only loaded when relevant
- Progressive disclosure prevents context pollution

**Activation Speed**:
- Automatic activation: < 100ms overhead
- Manual activation: Immediate

### Hooks

This skill does not configure any hooks. It operates purely as a knowledge resource for Claude Code.

### Reference Files

This skill does not include separate reference files. All content is in the main SKILL.md file for:
- Single-file simplicity
- Easier maintenance
- Complete context in one place
- No cross-file navigation needed

### Version History

**1.0.0** (2026-01-18)
- Initial release with 10 patterns
- Real-world application examples
- Performance optimization guidance
- Common pitfall prevention
- Testing strategies

### Maintenance Notes

**Content Organization**: The skill uses a flat structure with all patterns in SKILL.md because:
- Async patterns are interconnected (context managers use locks, queues use tasks, etc.)
- Learners benefit from seeing full picture
- Reference lookup is faster with single file
- Total content (~700 lines) is manageable in one file

**Future Enhancements**: Potential additions for future versions:
- Python 3.11+ TaskGroups pattern
- Structured concurrency patterns
- asyncio debugging techniques
- Performance profiling guidance
- Migration strategies from sync to async

### Related Skills

This skill complements:
- **python3-development**: General Python best practices
- **fastapi-development**: FastAPI-specific async patterns (if available)
- **web-scraping**: Advanced scraping techniques with async (if available)

### Common Questions

**Q: Should I use this skill for CPU-bound tasks?**
A: No. Asyncio is designed for I/O-bound tasks. For CPU-bound work, use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`. The skill covers using `run_in_executor()` for blocking operations.

**Q: Do I need to understand event loops to use asyncio?**
A: Not deeply. The skill provides practical patterns you can use immediately. Understanding event loops helps with debugging, but `asyncio.run()` handles event loop management automatically.

**Q: Can I mix async and sync code?**
A: Yes, but carefully. The skill shows how to:
- Call async from sync using `asyncio.run()`
- Call sync from async using `loop.run_in_executor()`
- Avoid common mixing pitfalls

**Q: What Python version do I need?**
A: Python 3.7+ is recommended for modern asyncio features (`asyncio.run()`, `async with`, `async for`). The skill uses 3.7+ syntax throughout.

**Q: How do I test async code?**
A: The skill includes pytest-asyncio patterns. Use `@pytest.mark.asyncio` decorator and `await` in test functions. See Testing section (lines 663-681).

### Additional Resources

For deeper understanding:
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html) - Official reference
- [PEP 492](https://www.python.org/dev/peps/pep-0492/) - Coroutines with async/await syntax
- [aiohttp documentation](https://docs.aiohttp.org/) - Async HTTP client/server
- [FastAPI documentation](https://fastapi.tiangolo.com/) - Modern async web framework
- [Real Python asyncio guide](https://realpython.com/async-io-python/) - Comprehensive tutorial
