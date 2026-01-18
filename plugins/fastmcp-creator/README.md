# FastMCP Creator

Build high-quality integrations that connect Claude to external services and APIs.

## Why Install This?

When you want Claude to interact with external services (Slack, GitHub, databases, web APIs, etc.), you need to build an MCP server - a specialized integration that bridges Claude with those services.

Without this plugin, Claude might:
- Create basic API wrappers that don't work well with AI workflows
- Miss important design patterns that make integrations reliable
- Skip critical error handling and validation
- Forget to include tests that verify the integration actually works

This plugin makes Claude an expert at building production-ready integrations.

## What Changes

With this plugin installed, Claude will:
- Build integrations optimized specifically for AI use (not just generic API wrappers)
- Design tools around complete workflows instead of individual API calls
- Include comprehensive validation using Pydantic (Python) or Zod (TypeScript)
- Add proper error handling with clear, actionable error messages
- Create evaluation tests to verify the integration works correctly
- Follow security best practices (path validation, rate limiting, etc.)
- Structure responses to be concise and context-efficient

## Installation

```bash
/plugin install fastmcp-creator
```

## Usage

Just install it - Claude will automatically use this knowledge when you ask it to build MCP servers or integrations.

You'll get the best results when you:
- Specify which service you want to integrate (e.g., "build a Slack MCP server")
- Mention whether you prefer Python or TypeScript
- Describe what workflows you need (e.g., "send messages and search channels")

## What You Can Build

**Communication tools**: Slack, Discord, email services
**Development platforms**: GitHub, GitLab, Jira, Linear
**Data sources**: PostgreSQL, SQLite, spreadsheets, web scrapers
**AI services**: Hugging Face, OpenAI, custom ML models
**Cloud infrastructure**: AWS, Render, database management
**Web automation**: Browser control, form filling, page scraping
**File operations**: JSON manipulation, file system access

## Example

**Without this plugin**:
You ask Claude to "create a GitHub MCP server." Claude builds a basic wrapper that exposes individual API endpoints. When you try to use it, you get cryptic errors, responses are too verbose, and it's missing key validation.

**With this plugin**:
Same request, but Claude:
1. Studies GitHub's API thoroughly
2. Designs workflow-oriented tools (like `github_create_pr_with_review_request` instead of separate create/assign tools)
3. Adds Pydantic validation for all inputs
4. Creates 10 complex evaluation questions to test the integration
5. Includes proper error handling with clear messages
6. Optimizes responses to be concise yet complete
7. Adds security validations for destructive operations

The result is a production-ready integration you can actually use reliably.

## Supported Languages

- **Python** with FastMCP framework (recommended)
- **TypeScript/Node.js** with official MCP SDK

Both implementations include:
- Input validation (Pydantic for Python, Zod for TypeScript)
- Async/await patterns for I/O operations
- Proper error handling and logging
- Security best practices
- Transport options (STDIO, HTTP, SSE)

## What's Included

When Claude builds an MCP server using this plugin, you get:
- Well-structured project with proper configuration
- Input validation schemas
- Clear, actionable error messages
- Comprehensive documentation
- Evaluation tests (10 complex questions that verify it works)
- Security patterns (path validation, confirmation flags for destructive operations)
- Performance optimizations (caching, pagination, character limits)

## Requirements

- Claude Code v2.0+
- For Python servers: Python 3.11+
- For TypeScript servers: Node.js 18+

## Learn More

After installing, ask Claude questions like:
- "Build me a Slack MCP server with message sending and channel search"
- "Create an MCP server for my PostgreSQL database"
- "Build a GitHub integration that can create issues and PRs"
- "Make an MCP server that scrapes web pages"

Claude will handle the research, implementation, validation, and testing automatically.
