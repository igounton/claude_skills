# Memory Bank MCP Technical Reference

**Document Type**: Technical Reference Guide **Based On**: Official documentation + verified file system implementation **Last Verified**: 2025-11-15

---

## Quick Reference: Tool Names and Usage

### Tools Available (Official Documentation)

These five tools form the complete Memory Bank MCP API:

| Tool Name            | Purpose                             | Parameter Requirements         |
| -------------------- | ----------------------------------- | ------------------------------ |
| `list_projects`      | List available projects             | MEMORY_BANK_ROOT only          |
| `list_project_files` | List files in a project             | projectName                    |
| `memory_bank_read`   | Read a file from memory bank        | projectName, fileName          |
| `memory_bank_write`  | Create new file in memory bank      | projectName, fileName, content |
| `memory_bank_update` | Update existing file in memory bank | projectName, fileName, content |

**Note**: Parameters listed in official documentation as "autoApprove" items. Detailed parameter formats are NOT provided in official README or custom-instructions.md.

---

## File System Structure Reference

### Expected Directory Layout

Based on actual verified structure and official documentation:

```
MEMORY_BANK_ROOT/
├── project-name-1/
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   ├── progress.md
│   ├── .clinerules
│   └── custom/
│       └── [custom-docs]/
└── project-name-2/
    └── [same structure as project-name-1]
```

### Core Files Purpose Matrix

| File              | Purpose                             | Read Order | Update Order                        |
| ----------------- | ----------------------------------- | ---------- | ----------------------------------- |
| projectbrief.md   | Foundation: core requirements/goals | 1st        | 5th                                 |
| productContext.md | Problem context and solutions       | 2nd        | 4th                                 |
| systemPatterns.md | Architecture and design patterns    | 3rd        | 3rd                                 |
| techContext.md    | Technology stack and setup          | 4th        | 2nd                                 |
| activeContext.md  | Current focus and decisions         | 5th        | 1st                                 |
| progress.md       | Status and roadmap                  | 6th        | 6th (updates reflect activeContext) |
| .clinerules       | Pattern repository                  | Throughout | Throughout                          |

**Access Pattern**: Read hierarchical order (1→6), Update reverse order (6→1)

---

## Configuration Reference

### Environment Variables

**MEMORY_BANK_ROOT**

- Type: Directory path (required)
- Purpose: Root directory for all project memory banks
- Format: Absolute file path
- Example: `/path/to/your/project/.memory-bank`
- Scope: Required for MCP server startup

### Configuration File Locations

By Client Type:

| Client | Config File Path | Configuration Type |
| --- | --- | --- |
| Cline (VS Code) | `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` | JSON MCP settings |
| Roo Code | `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json` | JSON MCP settings |
| Cursor | Custom via Cursor settings UI | Shell environment command |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | JSON MCP settings |
| Claude Code CLI | `~/.claude.json` | JSON MCP settings |

### MCP Settings Structure (JSON Format)

```json
{
    "allpepper-memory-bank": {
        "command": "npx",
        "args": ["-y", "@allpepper/memory-bank-mcp"],
        "env": {
            "MEMORY_BANK_ROOT": "/path/to/memory/bank"
        },
        "disabled": false,
        "autoApprove": [
            "memory_bank_read",
            "memory_bank_write",
            "memory_bank_update",
            "list_projects",
            "list_project_files"
        ]
    }
}
```

### Configuration Field Definitions

| Field                | Type    | Required | Default | Purpose                                                  |
| -------------------- | ------- | -------- | ------- | -------------------------------------------------------- |
| command              | string  | Yes      | -       | Command to execute (typically "npx")                     |
| args                 | array   | Yes      | -       | Arguments to command (includes package name and version) |
| env.MEMORY_BANK_ROOT | string  | Yes      | -       | Path to memory bank root directory                       |
| disabled             | boolean | No       | false   | Whether to disable this MCP server                       |
| autoApprove          | array   | No       | []      | Tools that don't require explicit user approval          |

---

## Installation Command Reference

### Latest Version (Recommended)

**Smithery automated installation**:

```bash
npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude
```

**Result**: Automatically configures MCP server in Claude Desktop/Client

### Project-Scoped Installation (For Teams)

**Claude Code CLI with project scope** (creates `.mcp.json` in project root):

```bash
claude mcp add --scope project \
  --env MEMORY_BANK_ROOT=$(pwd)/.memory-bank \
  memory-bank \
  npx -y @allpepper/memory-bank-mcp
```

**Scope Options**:

- `--scope local` - Saves to current working directory `.mcp.json`
- `--scope project` - Saves to project root `.mcp.json` (for git-tracked projects)
- `--scope user` - Saves to `~/.claude.json` (user-specific, default)

**Result**: Creates `.mcp.json` file in specified scope (project root if project scope), which can be committed to git

### Direct npm Installation

**For testing/development**:

```bash
npm install @allpepper/memory-bank-mcp
```

**For global access**:

```bash
npm install -g @allpepper/memory-bank-mcp
```

### Docker Image Build

**Build locally**:

```bash
docker build -t memory-bank-mcp:local .
```

**Requires**: Cloned repository with Dockerfile

### Via Command Line (for active use)

**Cline/Roo Code configuration requires**:

```
env MEMORY_BANK_ROOT=/path/to/bank npx -y @allpepper/memory-bank-mcp@latest
```

---

## Memory Bank Lifecycle

### Phase Sequence (Official Documentation)

```
START
  ↓
a) Pre-Flight Validation
  ├─ Check project directory exists
  ├─ Check core files present
  └─ Check custom documentation inventory
  ↓
b) Determine Mode
  ├─ If only reading: Plan Mode
  └─ If executing tasks: Act Mode
  ↓
c) Plan Mode (if needed)
  ├─ List projects
  ├─ Select context
  └─ Develop strategy
  ↓
d) Act Mode (if needed)
  ├─ Read .clinerules
  ├─ Execute task
  └─ Update documentation
  ↓
e) Learning Process (continuous)
  ├─ Identify patterns
  ├─ Validate with user
  ├─ Update .clinerules
  └─ Apply patterns
  ↓
TASK COMPLETE
```

### Documentation Update Trigger Points

Update needed when ANY of these occur:

- Code impact changes ≥25%
- New pattern discovered
- User explicitly requests "update memory bank"
- Context ambiguity detected

**Update Process**: Full file re-read before update

---

## JSON Operation Format

### Standard JSON Structure

```json
{
    "projectName": "string-identifier",
    "fileName": "filename.md",
    "content": "File content with escaped\\nnewlines"
}
```

### Field Requirements

| Field       | Type   | Example              | Notes                                        |
| ----------- | ------ | -------------------- | -------------------------------------------- |
| projectName | string | "python_picotool"    | Project directory identifier                 |
| fileName    | string | "progress.md"        | Filename in project directory                |
| content     | string | "# Title\n\nContent" | Use \\n for newlines, not actual line breaks |

### Data Type Rules

- **Strings**: Double-quoted, escaped newlines as `\n`
- **Booleans**: Lowercase `true` or `false`
- **No XML**: JSON format only
- **Path format**: Forward slashes only in paths

---

## Verified Implementation Details

### Project Isolation Implementation

**Method**: Directory-based isolation

**How it works**:

```
MEMORY_BANK_ROOT/
├── project-a/
│   ├── file1.md
│   └── file2.md
└── project-b/
    ├── file1.md
    └── file3.md
```

**Result**: When accessing project-a, only files in project-a/ are listed **Security**: Path traversal prevention prevents access to parent directories

### Multi-Project Listing

**Operation**: list_projects **Returns**: List of all project directories under MEMORY_BANK_ROOT **Example directories**: python_picotool, testing, other-project

### Project File Listing

**Operation**: list_project_files(projectName) **Parameter**: projectName (must match subdirectory name) **Returns**: Files in `MEMORY_BANK_ROOT/projectName/`

### Read Operation

**Operation**: memory_bank_read(projectName, fileName) **Parameters**:

- projectName: subdirectory name
- fileName: filename to read **Returns**: File content as string

### Write Operation

**Operation**: memory_bank_write(projectName, fileName, content) **Parameters**:

- projectName: subdirectory name (auto-created if needed)
- fileName: new filename to create
- content: string content (newlines as `\n`) **Returns**: Success/error response

**Note**: Fails if file already exists (use update instead)

### Update Operation

**Operation**: memory_bank_update(projectName, fileName, content) **Parameters**:

- projectName: existing project subdirectory
- fileName: existing filename to update
- content: new string content **Returns**: Success/error response

**Note**: Fails if file doesn't exist (use write instead)

---

## Deployment Patterns

### Pattern 1: Single Workspace

**Setup**:

- One MEMORY_BANK_ROOT directory
- Multiple projects in subdirectories
- One MCP server instance

**Use case**: Individual developer, single machine

### Pattern 2: Shared Memory Bank (Docker)

**Setup**:

- Memory bank mounted as Docker volume
- MCP server runs in container
- Multiple clients connect to same server

**Command**:

```bash
docker run -i --rm \
  -e MEMORY_BANK_ROOT="/mnt/memory_bank" \
  -v /path/to/memory-bank:/mnt/memory_bank \
  memory-bank-mcp:local
```

**Use case**: Team collaboration, centralized memory

### Pattern 3: Development with IDE Integration

**Setup**:

- Memory bank in project root (e.g., `.memory-bank/`)
- MCP configured in IDE settings
- Automatic tool calls from assistant

**Configuration**: Client-specific (Cline/Cursor/Claude)

---

## Repository Configuration Reference

### .gitignore Configuration

Add to your project's `.gitignore`:

```
.memory-bank/
```

**Rationale**: The `.memory-bank/` directory is similar to generated build artifacts and should not be committed:

| Item            | Reason for .gitignore    | Committed? |
| --------------- | ------------------------ | ---------- |
| `.memory-bank/` | Generated session memory | NO         |
| `.mcp.json`     | Capability configuration | YES        |
| `.pytest_cache/ | Generated test cache     | NO         |
| `node_modules/` | Generated dependencies   | NO         |
| `.env`          | Secrets                  | NO         |

**Why .mcp.json IS committed**:

- It enables the capability for all developers
- Equivalent to committing `package.json` or `pyproject.toml`
- No sensitive data (configuration only)
- Same setup for all team members

### .mcp.json Scope Reference

**Location options** from `claude mcp add --scope`:

| Scope     | Location         | Use Case                        | Commits to Git |
| --------- | ---------------- | ------------------------------- | -------------- |
| `user`    | `~/.claude.json` | Personal machine setup only     | NO             |
| `local`   | `./.mcp.json`    | Local directory only            | NO             |
| `project` | `./mcp.json`     | Project-wide for all developers | YES            |

**Recommendation for Teams**: Use `--scope project` so all developers get the same Memory Bank configuration.

---

## Limitations and Constraints

### Constraint 1: No Automatic Project Creation

**Finding**: Projects must have existing directory or be created explicitly **Evidence**: Official docs mention "Create new project if needed" as pre-flight step

### Constraint 2: Strict File Isolation

**Finding**: Cannot access files across project boundaries **Implication**: Each project is completely isolated namespace

### Constraint 3: Path Traversal Prevention

**Finding**: Cannot use relative paths like `../` to escape project directory **Implication**: Prevents accidental/malicious access to parent directories

### Constraint 4: File Format Requirements

**Finding**: JSON format with escaped newlines required for writes **Implication**: Must properly escape content before sending via MCP

### Constraint 5: Tool Availability Depends on Client

**Finding**: Tools only available through MCP protocol client **Implication**: Cannot use memory bank tools in non-MCP environments

---

## Security Model

### Path Traversal Prevention

**Mechanism**: MCP server validates paths before file access **Protection**: Prevents `../../etc/passwd` style attacks

### Project Isolation

**Mechanism**: Each project = separate directory **Protection**: Write to project-a cannot affect project-b

### Type Safety

**Mechanism**: TypeScript implementation with strict types **Protection**: Runtime type validation of parameters

### Operation Scope

**Mechanism**: Limited to 5 specific operations **Protection**: Cannot execute arbitrary code or access filesystem outside memory bank root

---

## Comparison: Official vs Tested Workflow

### Official Workflow Example

**Trigger**: User says "follow your custom instructions"

**System Flow**:

```
1. Pre-Flight Validation runs automatically
2. Checks if project exists
3. Checks if all core files present
4. Loads .clinerules
5. Enters Plan or Act mode
6. Executes appropriate memory bank operations
```

**Tool Usage**: Abstract MCP tool calls **Input Format**: Natural language **Output**: Direct tool invocations

### Tested Workflow (This Environment)

**Trigger**: Manual Read/Write operations

**System Flow**:

```
1. Use Read() tool to inspect .memory-bank/ directory
2. Use Glob() to list project files
3. Manually verify file presence
4. Use Read() to load content
5. Perform analysis
6. Use Write() to create/update files
```

**Tool Usage**: CLI tools (Read, Write, Edit) **Input Format**: Direct file paths **Output**: File system modifications visible immediately

### Key Differences

| Aspect                | Official                      | Tested                           |
| --------------------- | ----------------------------- | -------------------------------- |
| Tool Invocation       | MCP protocol (abstract)       | File system operations (direct)  |
| Pre-Flight Validation | Automatic                     | Manual verification              |
| Error Handling        | MCP server reports            | Bash exit codes / file not found |
| Type Safety           | Runtime TypeScript validation | File content validation          |
| IDE Integration       | Built-in to client            | Not available                    |

---

## Development Environment Requirements

### For Running MCP Server

**Required**:

- Node.js v14+ (or as specified in package.json)
- npm or yarn
- @allpepper/memory-bank-mcp package

**Optional**:

- Docker (for containerized deployment)
- IDE with MCP client support (Cline, Cursor, Claude)

### For Contributing to Repository

**Required** (from README.md):

- Node.js with npm
- TypeScript knowledge
- Git

**Build tools**:

```bash
npm install          # Install dependencies
npm run build        # Compile TypeScript
npm run test         # Run test suite
npm run dev          # Run with ts-node
```

---

## Documentation References

### Official Sources

All configuration and feature documentation sourced from:

**Primary**: <https://github.com/alioshr/memory-bank-mcp/blob/main/README.md> **Custom Instructions**: <https://github.com/alioshr/memory-bank-mcp/blob/main/custom-instructions.md> **License**: <https://github.com/alioshr/memory-bank-mcp/blob/main/LICENSE>

### Related Projects

**Original Concept**:

- Cline Memory Bank: <https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md>

**Discovery**:

- Smithery: <https://smithery.ai/server/@alioshr/memory-bank-mcp>
- Glama AI: <https://glama.ai/mcp/servers/ir18x1tixp>
- npm: <https://www.npmjs.com/package/@allpepper/memory-bank-mcp>

---

## Troubleshooting Reference

### Issue: MEMORY_BANK_ROOT not found

**Cause**: Environment variable not set **Solution**: Set `MEMORY_BANK_ROOT=/path/to/bank` before running server

### Issue: Path traversal prevented

**Cause**: Attempting to use `../` in filenames **Solution**: Use only filenames and projectName parameters, avoid path separators

### Issue: File already exists

**Cause**: Using `memory_bank_write` on existing file **Solution**: Use `memory_bank_update` instead for existing files

### Issue: Tools not available in CLI

**Cause**: MCP server not running or not configured in client **Solution**: Ensure MCP configuration in IDE/client settings matches repository

### Issue: Project not found

**Cause**: projectName doesn't match existing subdirectory **Solution**: First run `list_projects` to see available projects

---

## Performance Considerations

### Not Documented in Official Sources

The following information is NOT provided in official Memory Bank MCP documentation:

- Expected latency of operations
- File size limits
- Maximum number of projects
- Maximum number of files per project
- Database backend or storage optimization details
- Caching behavior
- Connection pooling strategy

**Recommendation**: For performance-critical deployments, test with your expected workload before production deployment.

---

## Version Information

### Package Versions

**Latest from npm**:

- Command: `npm info @allpepper/memory-bank-mcp`
- Current version in python_picotool: mentioned as 0.2.1 in task description

**Version Specification in Configuration**:

- Pinned: `@allpepper/memory-bank-mcp@0.2.1`
- Latest: `@allpepper/memory-bank-mcp@latest`
- Major version: `@allpepper/memory-bank-mcp@^0`

### Checking Installed Version

```bash
npm list @allpepper/memory-bank-mcp    # Local project
npm list -g @allpepper/memory-bank-mcp # Global installation
npm info @allpepper/memory-bank-mcp    # Available versions from registry
```

---

## Summary: This Document

This technical reference provides:

- Command and tool name quick reference
- Configuration syntax and field descriptions
- File structure requirements
- Installation instructions
- Lifecycle and workflow patterns
- Implementation details for verified features
- Deployment patterns
- Security model overview

This document does NOT provide:

- API endpoint documentation (not applicable - uses MCP)
- Line-by-line code examples
- Debugging of application code
- Performance metrics
- Detailed type signatures

For complete details, refer to:

1. Official README.md (features, installation, configuration)
2. custom-instructions.md (workflow, phases, access patterns)
3. SOURCE CODE (implementation details, type signatures, error handling)
