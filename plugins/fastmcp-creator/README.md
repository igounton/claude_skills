# fastmcp-creator

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive Claude Code plugin for building Model Context Protocol (MCP) servers with specialized guidance for FastMCP (Python) and TypeScript/Node implementations. Includes agent-centric design principles, evaluation creation, validation patterns, and production deployment strategies.

## Features

- **Complete MCP Coverage** - Universal MCP protocol guidelines for any implementation
- **FastMCP Specialization** - Python decorator-based patterns with Pydantic validation
- **TypeScript/Node Support** - Complete SDK guide with Zod validation
- **Agent-Centric Design** - Build tools optimized for AI agents, not just API wrappers
- **Evaluation Framework** - Scripts and guidance for testing server effectiveness
- **Production Ready** - Security, performance, observability, and .mcpb packaging
- **Standalone Operation** - No external dependencies, all guidance self-contained

## Installation

### Prerequisites

- Claude Code 2.1 or higher
- Python 3.11+ (for Python MCP servers)
- Node.js 18+ (for TypeScript/Node MCP servers)

### Install Plugin

```bash
# From Claude Code CLI or within a session
/plugin install fastmcp-creator

# Or manually clone to your plugins directory
git clone <repository-url> ~/.claude/plugins/fastmcp-creator
/plugin reload
```

## Quick Start

When you need to build an MCP server, simply describe your goal. Claude will automatically activate the fastmcp-creator skill:

```
Create an MCP server for GitHub that provides tools to list repositories,
create issues, and search code.
```

Or activate explicitly:

```
@fastmcp-creator

I want to build an MCP server for Slack with message sending and
channel listing capabilities.
```

The skill guides you through a 4-phase workflow:
1. **Research & Planning** - Understand requirements and design agent-optimized tools
2. **Implementation** - Build using FastMCP (Python) or TypeScript SDK patterns
3. **Review & Refine** - Ensure code quality, consistency, and error handling
4. **Evaluation** - Create comprehensive tests for server effectiveness

## Capabilities

### Skill: fastmcp-creator

**Description**: Build Model Context Protocol (MCP) servers with comprehensive coverage of generic MCP protocol AND FastMCP framework specialization.

**Invocation**: Claude automatically activates when you mention MCP servers, FastMCP, or building integrations.

**Coverage**:
- Generic MCP protocol (all implementations)
- Agent-centric design principles
- FastMCP framework (Python, decorator-based, Pydantic validation)
- TypeScript/Node MCP SDK (Zod validation)
- Evaluation creation for testing server quality
- Production deployment and packaging
- Security, performance, and observability patterns

**Reference Files**: 7 comprehensive guides included
- `mcp-best-practices.md` - Universal MCP guidelines
- `development-guidelines.md` - FastMCP Python specialization
- `typescript-mcp-server.md` - TypeScript/Node implementation
- `community-practices.md` - Mid-2025+ patterns and .mcpb packaging
- `prompts-and-templates.md` - Prompt system configuration
- `example-projects.md` - Real-world implementations
- `evaluation-guide.md` - Testing server quality

**Scripts**: Evaluation harness included
- `evaluation.py` - Test server effectiveness
- `connections.py` - MCP connection utilities
- `requirements.txt` - Python dependencies
- `example_evaluation.xml` - Example evaluation

## Usage

### Building a Python MCP Server with FastMCP

The skill guides you to create well-structured, agent-optimized servers:

```python
from fastmcp import FastMCP
from pydantic import Field
from typing import Annotated

mcp = FastMCP("github-mcp")

@mcp.tool()
def list_repositories(
    org: Annotated[str, Field(description="Organization name")],
    limit: Annotated[int, Field(ge=1, le=100)] = 20
) -> dict:
    """List repositories for an organization."""
    repos = fetch_repositories(org, limit)
    return {
        "repositories": repos,
        "count": len(repos)
    }

if __name__ == "__main__":
    mcp.run()  # STDIO transport by default
```

### Building a TypeScript MCP Server

For TypeScript/Node implementations:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "github-mcp-server",
  version: "1.0.0",
});

const ListReposSchema = z.object({
  org: z.string().describe("Organization name"),
  limit: z.number().int().min(1).max(100).default(20),
}).strict();

server.registerTool(
  "list_repositories",
  {
    title: "List Repositories",
    description: "List repositories for an organization",
    inputSchema: ListReposSchema,
    annotations: { readOnlyHint: true },
  },
  async (params) => {
    const repos = await fetchRepositories(params.org, params.limit);
    return {
      content: [{
        type: "text",
        text: JSON.stringify({ repositories: repos, count: repos.length }, null, 2)
      }]
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Creating Evaluations

Test your server's effectiveness with the evaluation harness:

```bash
# Install evaluation dependencies
pip install -r skills/fastmcp-creator/scripts/requirements.txt

# Set API key
export ANTHROPIC_API_KEY=your_api_key

# Run evaluation
python skills/fastmcp-creator/scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_mcp_server.py \
  evaluation.xml
```

## Agent-Centric Design Principles

The skill emphasizes building tools for AI agents, not just API wrappers:

### Build for Workflows, Not Endpoints
- Consolidate related operations into single, powerful tools
- Example: `schedule_event` that checks availability AND creates the event
- Focus on enabling complete tasks, not individual API calls

### Optimize for Limited Context
- Return high-signal information, not data dumps
- Provide "concise" vs "detailed" response options
- Use human-readable identifiers (names over IDs)
- Treat agent context window as a scarce resource

### Design Actionable Error Messages
- Guide agents toward correct usage
- Suggest specific next steps in errors
- Make errors educational, not just diagnostic

### Follow Natural Task Subdivisions
- Name tools how humans think about tasks
- Group related tools with consistent prefixes
- Design around workflows, not API structure

### Use Evaluation-Driven Development
- Create realistic evaluation scenarios early
- Let agent feedback drive improvements
- Prototype and iterate based on performance

## Examples

### Example 1: Building a Slack MCP Server

**Scenario**: Create an MCP server that allows AI agents to send messages, list channels, and search conversations in Slack.

**Steps**:
1. Describe your goal to Claude with the fastmcp-creator skill active
2. Claude researches Slack API documentation using MCP Ref tools
3. Designs agent-optimized tools (not just API wrappers)
4. Implements using FastMCP with Pydantic validation
5. Creates evaluation with 10 complex test questions
6. Tests server effectiveness with evaluation harness

**Result**: Production-ready MCP server with comprehensive tool descriptions, error handling, pagination, and verified agent effectiveness.

### Example 2: Extending an Existing MCP Server

**Scenario**: Add new tools to an existing GitHub MCP server for managing pull requests.

**Steps**:
1. Ask Claude to add PR tools while the fastmcp-creator skill is active
2. Claude reads existing server structure for consistency
3. Designs new tools following established patterns
4. Implements with same validation and error handling approach
5. Updates evaluations to test new capabilities

**Result**: Consistent, well-integrated new tools that match existing server patterns and maintain code quality.

### Example 3: Converting TypeScript to Python

**Scenario**: Port an existing TypeScript MCP server to Python using FastMCP.

**Steps**:
1. Share TypeScript server code with fastmcp-creator active
2. Claude analyzes tool structure and behavior
3. Maps Zod schemas to Pydantic models
4. Converts registerTool patterns to @mcp.tool() decorators
5. Preserves tool names, descriptions, and behavior
6. Creates equivalent evaluations for both versions

**Result**: Functionally equivalent Python server with FastMCP patterns, maintaining all capabilities of original TypeScript implementation.

## Best Practices

The skill enforces comprehensive best practices:

### Tool Design
- Use workflow-oriented tools, not API endpoint wrappers
- Name with service prefix: `{service}_{action}_{resource}`
- Optimize for AI context window efficiency
- Provide actionable, educational error messages

### Input/Output
- Support both JSON and Markdown response formats
- Implement pagination for list operations
- Enforce character limits (typically 25,000) with truncation
- Use human-readable identifiers where appropriate

### Validation
- Python: Pydantic Field() with constraints
- TypeScript: Zod schemas with .strict()
- Validate all inputs against schema
- Sanitize file paths and external identifiers

### Error Handling
- Don't expose internal errors to clients
- Provide clear, actionable error messages
- Handle timeouts and rate limits gracefully
- Use ToolError (Python) for business logic errors

### Security
- Validate file paths against allowed directories
- Use confirmation flags for destructive operations
- Set destructiveHint annotation for state-changing tools
- Store secrets in environment variables
- Rate limit expensive operations

### Performance
- Use async for I/O-bound operations
- Cache repeated queries with lru_cache
- Stream large responses in HTTP mode
- Extract common functionality into reusable functions

### Deployment
- Package as .mcpb for Claude Desktop distribution
- Provide manifest.json with user_config fields
- Support environment variable configuration
- Test with evaluation harness before release

## Documentation

### Quick Start Guides

- **[Evaluation Framework Guide](./docs/evaluation.md)** - Complete guide for using the evaluation scripts, creating effective test questions, and interpreting results

### Reference Documentation

All reference files are located in `skills/fastmcp-creator/references/`:

- **[mcp-best-practices.md](./skills/fastmcp-creator/references/mcp-best-practices.md)** - Universal MCP guidelines including naming conventions, response formats, pagination, security, and compliance requirements

- **[development-guidelines.md](./skills/fastmcp-creator/references/development-guidelines.md)** - Complete FastMCP development guide covering decorators, Pydantic validation, async patterns, error handling, Context parameters, annotations, transport options, and production deployment

- **[typescript-mcp-server.md](./skills/fastmcp-creator/references/typescript-mcp-server.md)** - Complete TypeScript/Node implementation guide covering project structure, registerTool patterns, Zod validation, error handling, and production build process

- **[community-practices.md](./skills/fastmcp-creator/references/community-practices.md)** - Mid-2025+ best practices including .mcpb packaging, security by design patterns, observability and testing approaches, performance tuning, caching, ecosystem compatibility, and agent orchestration patterns

- **[prompts-and-templates.md](./skills/fastmcp-creator/references/prompts-and-templates.md)** - FastMCP prompt and template system covering @mcp.prompt decorator, system instructions for tool use, configuration for AI-native tools, and prompt engineering for MCP servers

- **[example-projects.md](./skills/fastmcp-creator/references/example-projects.md)** - Real-world FastMCP implementations demonstrating best practices and patterns from Ultimate MCP Server, Hugging Face MCP server, browser automation servers, data/DevOps integrations, coding assistants, and templates/aggregators

- **[evaluation-guide.md](./skills/fastmcp-creator/references/evaluation-guide.md)** - Complete guide for creating comprehensive evaluations to test whether LLMs can effectively use your MCP server to answer realistic, complex questions

## Troubleshooting

### Server Hangs When Testing

**Problem**: Running MCP server directly causes process to hang indefinitely.

**Solution**: MCP servers are long-running processes. Use one of these approaches:
```bash
# Use timeout for quick validation
timeout 5s python server.py

# Run in tmux for interactive testing
tmux new-session -d -s mcp "python server.py"

# Use evaluation harness (recommended)
python scripts/evaluation.py -t stdio -c python -a server.py evaluation.xml
```

### Import Errors in Python

**Problem**: Cannot import FastMCP or Pydantic.

**Solution**: Install dependencies with uv (recommended) or pip:
```bash
# With uv (recommended by python3-development skill)
uv pip install fastmcp pydantic

# With pip
pip install fastmcp pydantic
```

### Zod Validation Errors in TypeScript

**Problem**: Schema validation fails unexpectedly.

**Solution**: Ensure you're using `.strict()` on Zod schemas and all fields are explicitly defined:
```typescript
const Schema = z.object({
  field: z.string().describe("Description")
}).strict();  // Rejects extra fields
```

### Evaluation Fails to Connect

**Problem**: Evaluation script cannot connect to MCP server.

**Solution**: Verify connection parameters match server configuration:
```bash
# For STDIO transport with Python
python evaluation.py -t stdio -c python -a server.py evaluation.xml

# For HTTP transport
python evaluation.py -t http -u http://localhost:8000 evaluation.xml
```

### Tools Not Appearing in Claude

**Problem**: MCP server tools don't appear in Claude Desktop.

**Solution**:
1. Verify server is running without errors
2. Check Claude Desktop MCP settings for correct server path
3. Restart Claude Desktop after config changes
4. Check server logs for startup errors

## Contributing

This plugin is part of the Claude Skills repository. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes following the documentation standards
4. Test with real MCP server creation scenarios
5. Submit a pull request

Please ensure:
- All reference files maintain citation standards
- Examples are concrete and tested
- Markdown follows formatting rules (code fences with language specifiers, relative links with `./`)

## License

See repository LICENSE file for details.

## Credits

Created as part of the Claude Code plugin ecosystem. Based on official MCP documentation, FastMCP framework patterns, and community best practices collected mid-2025.

**Official Resources**:
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

## Version History

### 1.0.0 (2026-01-18)
- Initial release
- Complete MCP protocol coverage
- FastMCP Python specialization
- TypeScript/Node SDK guide
- Evaluation framework
- 7 comprehensive reference files
- Production deployment patterns
