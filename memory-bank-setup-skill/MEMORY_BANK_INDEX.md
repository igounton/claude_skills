# Memory Bank MCP Documentation Index

**Project**: python_picotool **Created**: 2025-11-15 **Documentation Version**: Complete Verified Documentation Set

---

## Quick Navigation

| Document | Purpose | Audience | Length |
| --- | --- | --- | --- |
| [MEMORY_BANK_QUICKSTART.md](#quick-start) | Get started quickly | New users | 10-15 min read |
| [MEMORY_BANK_MCP_DOCUMENTATION.md](#comprehensive) | Complete verified reference | Developers | 30-45 min read |
| [MEMORY_BANK_REFERENCE.md](#technical) | Technical implementation details | Technical users | 20-30 min read |

---

## Document Descriptions

### MEMORY_BANK_QUICKSTART.md {#quick-start}

**Start here if**: You're new to Memory Bank MCP or need to set up quickly.

**Contains**:

- What is Memory Bank MCP (in simple terms)
- Understanding context types (capability config vs session memory vs curated context)
- Installation instructions (4 methods including project-scoped)
- Repository setup (.gitignore and .mcp.json recommendations)
- Step-by-step setup guide
- AGENTS.md vs Memory Bank decision tree
- How to use memory bank with AI assistants
- Common tasks and examples
- Troubleshooting tips

**Best for**: Getting up and running in minutes, understanding architecture

---

### MEMORY_BANK_MCP_DOCUMENTATION.md {#comprehensive}

**Start here if**: You need complete, authoritative information with verified sources.

**Contains**:

- Section 1: Official documentation summary (with verbatim quotes)
- Section 2: Officially documented features
- Section 3: Available tools and operations
- Section 4: Installation methods (all 5 methods, detailed)
- Section 5: Official memory bank file structure
- Section 6: Verified file system state (actual .memory-bank/ directory)
- Section 7: Tested and verified capabilities
- Section 8: Official workflow and lifecycle phases
- Section 9: Custom files and extensibility
- Section 10: Environment variables
- Section 11: Installation status in python_picotool project
- Section 12: Features NOT verified in this environment
- Section 13: Comparison of official vs tested approach
- Section 14: Error handling documentation
- Section 15: Development and testing
- Section 16: Project metadata
- Section 17: Contributing guidelines
- Section 18: Acknowledgments
- Section 19: Architectural separation - context types (capability config vs session memory vs curated context)
- Summary: Verified vs unverified claims

**Key Features**:

- ONLY verified information
- All claims cited with sources
- Verbatim quotes from official documentation
- Observable evidence from file system
- Clear distinction between tested and untested features

**Best for**: Finding authoritative answers with citations

---

### MEMORY_BANK_REFERENCE.md {#technical}

**Start here if**: You need technical implementation details and quick reference materials.

**Contains**:

- Quick reference: Tool names and usage
- File system structure reference
- Configuration reference (variables, file locations, field definitions)
- Installation command reference
- Memory bank lifecycle diagram
- JSON operation format specifications
- Verified implementation details (project isolation, read/write/update operations)
- Deployment patterns (3 common patterns)
- Limitations and constraints
- Security model
- Official vs tested workflow comparison
- Development environment requirements
- Documentation references
- Troubleshooting reference

**Key Features**:

- Quick lookup tables
- Command reference
- Format specifications
- Practical examples

**Best for**: Technical implementation and troubleshooting

---

## How to Use These Documents

### Scenario 1: You're brand new to Memory Bank MCP

1. Read: **MEMORY_BANK_QUICKSTART.md** - "What Is Memory Bank MCP?" section
2. Follow: Installation section (choose appropriate method for your IDE)
3. Use: "Setting Up Memory Bank for Your Project" section
4. Try: "Example: First Memory Bank Session" section

**Time**: 15-20 minutes to have working setup

### Scenario 2: You need to verify a specific feature

1. Go to: **MEMORY_BANK_MCP_DOCUMENTATION.md**
2. Search: Find the feature in Section 1-9
3. Check: "Verified Through Official Documentation" or "Verified Through File System Evidence"
4. Cite: Use the provided source URL or file reference

**Time**: 5 minutes to find answer with citation

### Scenario 3: You're implementing something

1. Check: **MEMORY_BANK_REFERENCE.md** - Configuration or command reference
2. Use: Tables and examples for exact syntax
3. Verify: With **MEMORY_BANK_MCP_DOCUMENTATION.md** Section 4-7

**Time**: 5-10 minutes to get technical details

### Scenario 4: You hit a problem

1. Try: **MEMORY_BANK_QUICKSTART.md** - Troubleshooting section
2. Check: **MEMORY_BANK_REFERENCE.md** - Troubleshooting Reference section
3. Research: **MEMORY_BANK_MCP_DOCUMENTATION.md** - Section 12 (Features NOT Verified)

**Time**: 5-15 minutes to understand the issue

---

## Key Information Across Documents

### Installation

**Quick Start**: MEMORY_BANK_QUICKSTART.md > "Installation" section (5 methods) **Complete Details**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 4 **Commands Reference**: MEMORY_BANK_REFERENCE.md > "Installation Command Reference"

### File Structure

**Quick Start**: MEMORY_BANK_QUICKSTART.md > "Setting Up Memory Bank" section **Verified State**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 6 **Reference**: MEMORY_BANK_REFERENCE.md > "File System Structure Reference"

### Tools and Operations

**Tool Names**: MEMORY_BANK_REFERENCE.md > "Quick Reference: Tool Names and Usage" **Documentation**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 3 **Verification**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 7

### Configuration

**Setup Instructions**: MEMORY_BANK_QUICKSTART.md > "Installation" section **All Methods**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 4 **Reference**: MEMORY_BANK_REFERENCE.md > "Configuration Reference"

### Workflow

**How to Use**: MEMORY_BANK_QUICKSTART.md > "Using Memory Bank" section **Official Workflow**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 8 **Lifecycle**: MEMORY_BANK_REFERENCE.md > "Memory Bank Lifecycle"

---

## What's Verified and What's Not

### Verified (Observable Evidence)

✓ Multi-project support works (actual test in memory bank) ✓ File structure matches documentation (verified from .memory-bank/ directory) ✓ Project isolation is enforced (testing directory proves it) ✓ File reading capability works (agent-discovery.md was read) ✓ File writing capability works (agent-discovery.md was created) ✓ All tool names documented (listed in official sources) ✓ All installation methods documented (from official README) ✓ Configuration formats documented (from official sources)

**See**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 7 and Summary

### NOT Verified (Environment Limitation)

- Real MCP protocol tool calls (this is a CLI, not an IDE client)
- Type safety at runtime (would need TypeScript execution)
- Specific error messages (would need to trigger errors)
- Performance characteristics (would need benchmarking)
- Docker deployment in use (environment doesn't support Docker)

**See**: MEMORY_BANK_MCP_DOCUMENTATION.md > Section 12

---

## Citation Guide

### To Cite Official Features

Use **MEMORY_BANK_MCP_DOCUMENTATION.md**:

- Find the feature in Section 1-9
- Use the quoted text with "Source:" attribution
- Include the GitHub URL

Example:

> According to the official README.md: "The Memory Bank MCP Server transforms traditional file-based memory banks into a centralized service that provides remote access to memory bank files via MCP protocol" Source: <https://github.com/alioshr/memory-bank-mcp/blob/main/README.md>

### To Cite Verified Implementation

Use **MEMORY_BANK_MCP_DOCUMENTATION.md**:

- Find the feature in Section 7 "Tested and Verified Capabilities"
- Reference the actual evidence provided

Example:

> Memory bank read operations are verified to work correctly because agent-discovery.md contains the validation result: "Successfully retrieved orchestrator-created memory file (project-structure.md)" Source: /path/to/your/project/.memory-bank/python_picotool/agent-discovery.md

### To Cite Technical Details

Use **MEMORY_BANK_REFERENCE.md**:

- Find the information in the appropriate reference section
- The tables and examples are derived from official documentation

Example:

> The five available tools are listed in the Quick Reference section with parameter requirements. Source: MEMORY_BANK_REFERENCE.md > "Quick Reference: Tool Names and Usage"

---

## Document Statistics

### MEMORY_BANK_QUICKSTART.md

- Sections: 11 main sections
- Estimated read time: 10-15 minutes
- Use case: Getting started
- Audience: Everyone

### MEMORY_BANK_MCP_DOCUMENTATION.md

- Sections: 18 main sections + summary
- Estimated read time: 30-45 minutes
- Use case: Complete reference
- Audience: Developers, technical users
- Citations: All claims have sources
- Verification: Clear distinction between tested/untested

### MEMORY_BANK_REFERENCE.md

- Sections: 13 main sections
- Estimated read time: 20-30 minutes
- Use case: Technical implementation
- Audience: Technical users, implementers
- Format: Tables, quick reference, examples

---

## Quality Standards Applied

All documentation in this set follows these standards:

### Verified Data Only

- No estimates or guesses (marked if not verified)
- All claims cite sources (GitHub URLs, file paths, tool outputs)
- Observable evidence provided when available
- Clear distinction between "documented" and "tested"

### No Fabrication

- No made-up examples without marking them as examples
- No invented features
- No estimated measurements
- No "probably" or "likely" language without caveats

### Accurate Citations

- Verbatim quotes from official sources
- Direct URLs to original content
- Line-by-line references to file content
- Actual command outputs shown

### Completeness

- All 5 installation methods documented
- All 5 tools listed with parameters
- All core files described
- All phases documented
- All configuration options listed

---

## How to Update This Documentation

### When to Update

Update these documents when:

- Official Memory Bank MCP repository changes
- New version released with new features
- Configuration options change
- Installation methods change
- New verification test results available

### How to Update

1. **MEMORY_BANK_MCP_DOCUMENTATION.md**: Re-fetch official sources, verify against new content
2. **MEMORY_BANK_REFERENCE.md**: Update tables and quick reference based on new documentation
3. **MEMORY_BANK_QUICKSTART.md**: Update examples and setup instructions if methods change

### What NOT to Update

Do not add:

- Unverified claims
- Estimates or guesses
- "Probably" or "likely" language without caveats
- Features not in official documentation
- Custom examples not marked as examples

---

## Related Resources

### Official Sources

- **GitHub Repository**: <https://github.com/alioshr/memory-bank-mcp>
- **README.md**: <https://github.com/alioshr/memory-bank-mcp/blob/main/README.md>
- **Custom Instructions**: <https://github.com/alioshr/memory-bank-mcp/blob/main/custom-instructions.md>
- **License**: <https://github.com/alioshr/memory-bank-mcp/blob/main/LICENSE>

### Package Registry

- **npm Package**: <https://www.npmjs.com/package/@allpepper/memory-bank-mcp>
- **Smithery**: <https://smithery.ai/server/@alioshr/memory-bank-mcp>
- **Glama AI**: <https://glama.ai/mcp/servers/ir18x1tixp>

### Original Concept

- **Cline Memory Bank**: <https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md>

### Project Context

- **python_picotool Repository**: <https://sourcery.assaabloy.net/aehgfw/tools/python_picotool>
- **Memory Bank Location**: /path/to/your/project/.memory-bank/

---

## Document Maintenance Log

| Date       | Document | Change             | Reason                           |
| ---------- | -------- | ------------------ | -------------------------------- |
| 2025-11-15 | All      | Initial creation   | Comprehensive documentation task |
| 2025-11-15 | All      | Formatting applied | Automated markdown formatting    |
| -          | -        | -                  | -                                |

---

## How to Report Issues

If you find:

- Outdated information: Check against official sources in Section 16 of this document
- Inaccurate citations: Verify the source URL provided
- Missing information: Check if it's in Section 12 (Features NOT Verified)
- Unverified claims: They should be marked as such

Contact: Refer to official GitHub repository for official support
