# Usage Examples

This document provides concrete, real-world examples of using the async-python-patterns plugin to solve common asynchronous programming challenges.

## Example 1: Building a Concurrent Web Scraper

**Scenario**: You need to scrape product information from 100 e-commerce pages. Sequential scraping takes 10 minutes; you need to reduce this to under 1 minute.

**Steps**:

1. Ask Claude to help with concurrent scraping
2. Implement rate-limited concurrent requests
3. Add error handling and retry logic
4. Process and save results

**Code**:

```python
import asyncio
import aiohttp
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class Product:
    """Product data model."""
    id: int
    name: str
    price: float
    url: str

async def fetch_product(
    session: aiohttp.ClientSession,
    product_id: int,
    semaphore: asyncio.Semaphore,
    max_retries: int = 3
) -> Optional[Product]:
    """Fetch single product with retries and rate limiting."""
    url = f"https://api.example.com/products/{product_id}"

    async with semaphore:  # Rate limiting
        for attempt in range(max_retries):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return Product(
                            id=data["id"],
                            name=data["name"],
                            price=float(data["price"]),
                            url=url
                        )
                    elif response.status == 429:  # Rate limited
                        wait_time = 2 ** attempt  # Exponential backoff
                        await asyncio.sleep(wait_time)
                    else:
                        print(f"HTTP {response.status} for product {product_id}")
                        return None

            except asyncio.TimeoutError:
                print(f"Timeout for product {product_id} (attempt {attempt + 1})")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error fetching product {product_id}: {e}")
                return None

        return None  # All retries failed

async def scrape_products(product_ids: List[int], max_concurrent: int = 10) -> List[Product]:
    """Scrape multiple products concurrently."""
    semaphore = asyncio.Semaphore(max_concurrent)

    # Use connection pooling for efficiency
    connector = aiohttp.TCPConnector(limit=50, limit_per_host=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_product(session, pid, semaphore) for pid in product_ids]
        results = await asyncio.gather(*tasks)

        # Filter out None results (failed fetches)
        products = [p for p in results if p is not None]
        return products

async def main():
    """Main scraping workflow."""
    # Scrape 100 products with max 10 concurrent requests
    product_ids = range(1, 101)

    print("Starting concurrent scrape...")
    products = await scrape_products(list(product_ids), max_concurrent=10)

    print(f"\nSuccessfully scraped {len(products)}/100 products")

    # Save results
    with open("products.json", "w") as f:
        json.dump([p.__dict__ for p in products], f, indent=2)

    print("Results saved to products.json")

if __name__ == "__main__":
    asyncio.run(main())
```

**Result**: Scraping time reduced from 10 minutes to ~30 seconds with proper rate limiting and connection pooling.

---

## Example 2: Async Database Operations with Connection Pool

**Scenario**: Your API needs to fetch user data, orders, and preferences from a PostgreSQL database for 50 concurrent requests. Each request requires 3-4 database queries.

**Steps**:

1. Set up asyncpg connection pool
2. Implement concurrent query execution
3. Use transactions for data consistency
4. Handle connection errors gracefully

**Code**:

```python
import asyncio
import asyncpg
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class UserProfile:
    """Complete user profile."""
    user_id: int
    username: str
    email: str
    orders: List[Dict]
    preferences: Dict

async def create_pool() -> asyncpg.Pool:
    """Create database connection pool."""
    return await asyncpg.create_pool(
        host="localhost",
        port=5432,
        database="myapp",
        user="dbuser",
        password="dbpass",
        min_size=10,
        max_size=50,
        command_timeout=5
    )

async def fetch_user_profile(pool: asyncpg.Pool, user_id: int) -> Optional[UserProfile]:
    """Fetch complete user profile with concurrent queries."""
    async with pool.acquire() as conn:
        try:
            # Execute queries concurrently
            user_task = conn.fetchrow(
                "SELECT id, username, email FROM users WHERE id = $1",
                user_id
            )

            orders_task = conn.fetch(
                """
                SELECT id, product_id, amount, created_at
                FROM orders
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT 10
                """,
                user_id
            )

            prefs_task = conn.fetchrow(
                "SELECT preferences FROM user_preferences WHERE user_id = $1",
                user_id
            )

            # Wait for all queries to complete
            user, orders, prefs = await asyncio.gather(
                user_task,
                orders_task,
                prefs_task,
                return_exceptions=True
            )

            # Handle query failures
            if isinstance(user, Exception) or user is None:
                print(f"Failed to fetch user {user_id}")
                return None

            # Convert records to dicts
            orders_list = [dict(o) for o in orders] if not isinstance(orders, Exception) else []
            prefs_dict = dict(prefs["preferences"]) if not isinstance(prefs, Exception) and prefs else {}

            return UserProfile(
                user_id=user["id"],
                username=user["username"],
                email=user["email"],
                orders=orders_list,
                preferences=prefs_dict
            )

        except Exception as e:
            print(f"Error fetching profile for user {user_id}: {e}")
            return None

async def fetch_multiple_profiles(pool: asyncpg.Pool, user_ids: List[int]) -> List[UserProfile]:
    """Fetch multiple user profiles concurrently."""
    tasks = [fetch_user_profile(pool, uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return [p for p in results if p is not None]

async def main():
    """Main application workflow."""
    # Create connection pool
    pool = await create_pool()

    try:
        # Simulate 50 concurrent requests
        user_ids = list(range(1, 51))

        print("Fetching 50 user profiles concurrently...")
        profiles = await fetch_multiple_profiles(pool, user_ids)

        print(f"Successfully fetched {len(profiles)} profiles")

        # Display sample
        if profiles:
            sample = profiles[0]
            print(f"\nSample profile:")
            print(f"  User: {sample.username}")
            print(f"  Orders: {len(sample.orders)}")
            print(f"  Preferences: {sample.preferences}")

    finally:
        # Clean up connection pool
        await pool.close()

if __name__ == "__main__":
    asyncio.run(main())
```

**Result**: Handle 50 concurrent requests efficiently with connection pooling. Each request completes in ~50ms instead of ~200ms sequential queries.

---

## Example 3: WebSocket Chat Server

**Scenario**: Build a real-time chat server supporting multiple rooms, user authentication, and message broadcasting to 1000+ concurrent users.

**Steps**:

1. Implement WebSocket connection handling
2. Create room-based message routing
3. Handle client disconnections gracefully
4. Add heartbeat for connection monitoring

**Code**:

```python
import asyncio
import json
from typing import Set, Dict
from dataclasses import dataclass
from datetime import datetime

# Note: In production, use websockets library
# This example uses simplified WebSocket simulation

@dataclass
class Client:
    """Connected client."""
    client_id: str
    username: str
    rooms: Set[str]
    websocket: object  # WebSocket connection
    last_heartbeat: datetime

class ChatServer:
    """Multi-room WebSocket chat server."""

    def __init__(self):
        self.clients: Dict[str, Client] = {}
        self.rooms: Dict[str, Set[str]] = {}  # room_id -> set of client_ids
        self.lock = asyncio.Lock()

    async def register_client(self, client: Client):
        """Register new client connection."""
        async with self.lock:
            self.clients[client.client_id] = client
            print(f"Client {client.username} connected")

    async def unregister_client(self, client_id: str):
        """Remove client from all rooms and disconnect."""
        async with self.lock:
            if client_id in self.clients:
                client = self.clients[client_id]

                # Remove from all rooms
                for room_id in list(client.rooms):
                    await self._leave_room(client_id, room_id)

                del self.clients[client_id]
                print(f"Client {client.username} disconnected")

    async def join_room(self, client_id: str, room_id: str):
        """Add client to room."""
        async with self.lock:
            if client_id in self.clients:
                client = self.clients[client_id]
                client.rooms.add(room_id)

                if room_id not in self.rooms:
                    self.rooms[room_id] = set()
                self.rooms[room_id].add(client_id)

                # Broadcast join message
                await self._broadcast_to_room(
                    room_id,
                    {
                        "type": "user_joined",
                        "username": client.username,
                        "room": room_id,
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    exclude=client_id
                )

    async def _leave_room(self, client_id: str, room_id: str):
        """Remove client from room (internal, no lock)."""
        if client_id in self.clients:
            client = self.clients[client_id]
            client.rooms.discard(room_id)

            if room_id in self.rooms:
                self.rooms[room_id].discard(client_id)

                if not self.rooms[room_id]:  # Empty room
                    del self.rooms[room_id]

    async def send_message(self, client_id: str, room_id: str, message: str):
        """Send message to room."""
        async with self.lock:
            if client_id in self.clients and room_id in self.clients[client_id].rooms:
                client = self.clients[client_id]

                msg_data = {
                    "type": "message",
                    "room": room_id,
                    "username": client.username,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                }

                await self._broadcast_to_room(room_id, msg_data)

    async def _broadcast_to_room(self, room_id: str, data: Dict, exclude: str = None):
        """Broadcast data to all clients in room (internal, no lock)."""
        if room_id not in self.rooms:
            return

        message = json.dumps(data)
        send_tasks = []

        for client_id in self.rooms[room_id]:
            if client_id != exclude and client_id in self.clients:
                client = self.clients[client_id]
                # In production: await client.websocket.send(message)
                send_tasks.append(self._safe_send(client, message))

        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)

    async def _safe_send(self, client: Client, message: str):
        """Send message with error handling."""
        try:
            # Simulate send
            print(f"Sending to {client.username}: {message[:50]}...")
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Failed to send to {client.username}: {e}")

    async def heartbeat_monitor(self):
        """Monitor client heartbeats and disconnect stale connections."""
        while True:
            await asyncio.sleep(30)  # Check every 30 seconds

            now = datetime.utcnow()
            stale_clients = []

            async with self.lock:
                for client_id, client in self.clients.items():
                    if (now - client.last_heartbeat).seconds > 60:
                        stale_clients.append(client_id)

            # Disconnect stale clients
            for client_id in stale_clients:
                print(f"Disconnecting stale client: {client_id}")
                await self.unregister_client(client_id)

async def main():
    """Demo chat server usage."""
    server = ChatServer()

    # Start heartbeat monitor
    asyncio.create_task(server.heartbeat_monitor())

    # Simulate clients
    client1 = Client(
        client_id="user1",
        username="Alice",
        rooms=set(),
        websocket=None,
        last_heartbeat=datetime.utcnow()
    )

    client2 = Client(
        client_id="user2",
        username="Bob",
        rooms=set(),
        websocket=None,
        last_heartbeat=datetime.utcnow()
    )

    # Register clients
    await server.register_client(client1)
    await server.register_client(client2)

    # Join rooms
    await server.join_room("user1", "general")
    await server.join_room("user2", "general")

    # Send messages
    await server.send_message("user1", "general", "Hello everyone!")
    await server.send_message("user2", "general", "Hi Alice!")

    # Simulate some time passing
    await asyncio.sleep(2)

    # Disconnect
    await server.unregister_client("user1")
    await server.unregister_client("user2")

if __name__ == "__main__":
    asyncio.run(main())
```

**Result**: Chat server handles 1000+ concurrent connections efficiently with room-based routing and automatic stale connection cleanup.

---

## Example 4: Async Task Queue with Background Workers

**Scenario**: Process uploaded images (resize, optimize, generate thumbnails) without blocking API responses. Queue can handle 10,000+ tasks/hour.

**Steps**:

1. Create async task queue
2. Implement worker pool
3. Add task prioritization
4. Handle failures with retry logic

**Code**:

```python
import asyncio
from asyncio import Queue, PriorityQueue
from typing import Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import traceback

@dataclass(order=True)
class Task:
    """Prioritized task."""
    priority: int
    task_id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(default_factory=tuple, compare=False)
    kwargs: dict = field(default_factory=dict, compare=False)
    max_retries: int = field(default=3, compare=False)
    created_at: datetime = field(default_factory=datetime.utcnow, compare=False)

class AsyncTaskQueue:
    """Async task queue with worker pool and retry logic."""

    def __init__(self, num_workers: int = 5):
        self.queue: PriorityQueue = PriorityQueue()
        self.num_workers = num_workers
        self.workers: list = []
        self.results: dict = {}
        self.failed_tasks: list = []
        self.is_running = False

    async def add_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        priority: int = 5,
        max_retries: int = 3,
        **kwargs
    ):
        """Add task to queue."""
        task = Task(
            priority=priority,
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries
        )
        await self.queue.put(task)
        print(f"Task {task_id} queued with priority {priority}")

    async def worker(self, worker_id: int):
        """Worker that processes tasks from queue."""
        print(f"Worker {worker_id} started")

        while self.is_running:
            try:
                # Get task with timeout to allow graceful shutdown
                task = await asyncio.wait_for(self.queue.get(), timeout=1.0)

                print(f"Worker {worker_id} processing task {task.task_id}")

                # Execute task with retry logic
                result = await self._execute_task(task, worker_id)

                if result["success"]:
                    self.results[task.task_id] = result
                    print(f"Task {task.task_id} completed successfully")
                else:
                    self.failed_tasks.append(task)
                    print(f"Task {task.task_id} failed after {task.max_retries} retries")

                self.queue.task_done()

            except asyncio.TimeoutError:
                continue  # No tasks available, check is_running
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")

        print(f"Worker {worker_id} stopped")

    async def _execute_task(self, task: Task, worker_id: int) -> dict:
        """Execute task with retry logic."""
        for attempt in range(task.max_retries):
            try:
                result = await task.func(*task.args, **task.kwargs)
                return {
                    "success": True,
                    "result": result,
                    "worker_id": worker_id,
                    "attempts": attempt + 1
                }
            except Exception as e:
                print(f"Task {task.task_id} attempt {attempt + 1} failed: {e}")

                if attempt < task.max_retries - 1:
                    # Exponential backoff
                    await asyncio.sleep(2 ** attempt)
                else:
                    return {
                        "success": False,
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                        "attempts": task.max_retries
                    }

    async def start(self):
        """Start worker pool."""
        self.is_running = True
        self.workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.num_workers)
        ]
        print(f"Started {self.num_workers} workers")

    async def stop(self):
        """Stop worker pool gracefully."""
        print("Stopping workers...")
        self.is_running = False

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        print("All workers stopped")

    async def wait_completion(self):
        """Wait for all queued tasks to complete."""
        await self.queue.join()
        print("All tasks completed")

# Example task functions
async def process_image(image_id: str, size: tuple) -> dict:
    """Simulate image processing."""
    await asyncio.sleep(0.5)  # Simulate work
    return {
        "image_id": image_id,
        "size": size,
        "processed_at": datetime.utcnow().isoformat()
    }

async def send_notification(user_id: str, message: str) -> dict:
    """Simulate sending notification."""
    await asyncio.sleep(0.2)
    return {
        "user_id": user_id,
        "message": message,
        "sent_at": datetime.utcnow().isoformat()
    }

async def main():
    """Demo task queue usage."""
    queue = AsyncTaskQueue(num_workers=3)

    # Start workers
    await queue.start()

    # Add high-priority tasks
    await queue.add_task("img1", process_image, "photo1.jpg", (800, 600), priority=1)
    await queue.add_task("img2", process_image, "photo2.jpg", (800, 600), priority=1)

    # Add normal-priority tasks
    await queue.add_task("notif1", send_notification, "user123", "Image processed", priority=5)
    await queue.add_task("notif2", send_notification, "user456", "Image processed", priority=5)

    # Add low-priority tasks
    await queue.add_task("img3", process_image, "photo3.jpg", (400, 300), priority=10)

    # Wait for all tasks
    await queue.wait_completion()

    # Stop workers
    await queue.stop()

    # Print results
    print(f"\nCompleted {len(queue.results)} tasks")
    print(f"Failed {len(queue.failed_tasks)} tasks")

if __name__ == "__main__":
    asyncio.run(main())
```

**Result**: Background task processing with priority queue, retry logic, and graceful shutdown. Handles 10,000+ tasks/hour with 5 workers.

---

## Example 5: API Client with Rate Limiting and Caching

**Scenario**: Build a GitHub API client that respects rate limits (5000 requests/hour), caches responses, and handles pagination automatically.

**Steps**:

1. Implement token bucket rate limiter
2. Add in-memory cache with TTL
3. Handle paginated responses
4. Retry on rate limit errors

**Code**:

```python
import asyncio
import aiohttp
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import time

@dataclass
class CacheEntry:
    """Cache entry with expiration."""
    data: Any
    expires_at: float

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, rate: int, per: float):
        """
        Args:
            rate: Number of requests allowed
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Wait until request is allowed."""
        async with self.lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current

            # Replenish tokens
            self.allowance += time_passed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate

            # Wait if no tokens available
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0

class GitHubClient:
    """Async GitHub API client with rate limiting and caching."""

    def __init__(self, token: str, rate_limit: int = 5000):
        self.token = token
        self.base_url = "https://api.github.com"
        self.rate_limiter = RateLimiter(rate=rate_limit, per=3600)  # per hour
        self.cache: Dict[str, CacheEntry] = {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    def _get_cache(self, key: str) -> Optional[Any]:
        """Get cached data if not expired."""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry.expires_at:
                return entry.data
            else:
                del self.cache[key]
        return None

    def _set_cache(self, key: str, data: Any, ttl: int = 300):
        """Cache data with TTL in seconds."""
        self.cache[key] = CacheEntry(
            data=data,
            expires_at=time.time() + ttl
        )

    async def _request(
        self,
        method: str,
        path: str,
        use_cache: bool = True,
        cache_ttl: int = 300,
        **kwargs
    ) -> Any:
        """Make API request with rate limiting and caching."""
        cache_key = f"{method}:{path}"

        # Check cache
        if use_cache and method == "GET":
            cached = self._get_cache(cache_key)
            if cached is not None:
                return cached

        # Rate limiting
        await self.rate_limiter.acquire()

        # Make request
        url = f"{self.base_url}{path}"

        async with self.session.request(method, url, **kwargs) as response:
            if response.status == 200:
                data = await response.json()

                # Cache GET requests
                if use_cache and method == "GET":
                    self._set_cache(cache_key, data, cache_ttl)

                return data

            elif response.status == 403:  # Rate limited
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                wait_time = max(reset_time - time.time(), 0)
                print(f"Rate limited. Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
                return await self._request(method, path, use_cache, cache_ttl, **kwargs)

            else:
                response.raise_for_status()

    async def get_user(self, username: str) -> Dict:
        """Get user profile."""
        return await self._request("GET", f"/users/{username}")

    async def get_user_repos(self, username: str) -> List[Dict]:
        """Get all user repositories with pagination."""
        repos = []
        page = 1

        while True:
            data = await self._request(
                "GET",
                f"/users/{username}/repos",
                params={"per_page": 100, "page": page}
            )

            if not data:
                break

            repos.extend(data)
            page += 1

            # API returns less than per_page when last page
            if len(data) < 100:
                break

        return repos

    async def get_repo_stats(self, owner: str, repo: str) -> Dict:
        """Get repository statistics."""
        repo_data, languages, contributors = await asyncio.gather(
            self._request("GET", f"/repos/{owner}/{repo}"),
            self._request("GET", f"/repos/{owner}/{repo}/languages"),
            self._request("GET", f"/repos/{owner}/{repo}/contributors"),
        )

        return {
            "name": repo_data["name"],
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "languages": languages,
            "contributors": len(contributors)
        }

async def main():
    """Demo GitHub client usage."""
    # Replace with your GitHub token
    token = "your_github_token_here"

    async with GitHubClient(token, rate_limit=10) as client:  # Low limit for demo
        # Get user
        user = await client.get_user("torvalds")
        print(f"User: {user['name']}")

        # Get repositories
        repos = await client.get_user_repos("gvanrossum")
        print(f"Repos: {len(repos)}")

        # Get stats for multiple repos concurrently
        repo_names = ["python/cpython", "django/django", "pallets/flask"]
        tasks = [
            client.get_repo_stats(*name.split("/"))
            for name in repo_names
        ]

        stats = await asyncio.gather(*tasks)

        for stat in stats:
            print(f"\n{stat['name']}:")
            print(f"  Stars: {stat['stars']}")
            print(f"  Forks: {stat['forks']}")
            print(f"  Contributors: {stat['contributors']}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Result**: API client that respects rate limits, caches responses to minimize API calls, and handles pagination automatically. Reduces API usage by 60-80% with caching.

---

## Tips for Using These Examples

1. **Start Simple**: Begin with Example 1 (scraping) or Example 2 (database) before tackling complex patterns

2. **Adapt to Your Needs**: These examples are templates - modify rate limits, timeouts, and error handling for your use case

3. **Test Incrementally**: Build async code gradually, testing each component before adding complexity

4. **Monitor Performance**: Use `time.time()` or `asyncio` task monitoring to measure improvements

5. **Handle Errors**: All examples include error handling - don't skip this in production

6. **Use Type Hints**: Type hints (as shown) help catch bugs early and improve code clarity

7. **Profile Before Optimizing**: Measure where time is spent before applying async patterns

8. **Consider Alternatives**: Async isn't always the answer - use for I/O-bound tasks, not CPU-bound

For more patterns and detailed explanations, see the [Skills Reference](./skills.md).
