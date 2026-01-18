# Claude Skills Collection

A collection of Claude Code plugins providing specialized skills for development workflows, code quality, documentation, and AI-assisted programming.

## Installation

Install plugins from this collection using Claude Code:

```bash
# Add the marketplace repository
/plugin marketplace add Jamie-BitFlight/claude_skills

# Install individual plugins
/plugin install plugin-name
```

Or clone and install locally:

```bash
git clone https://github.com/Jamie-BitFlight/claude_skills.git
cd claude_skills
./install.py
```

## Available Plugins

### Python Development

| Plugin | Description |
|--------|-------------|
| [python3-development](./plugins/python3-development) | Comprehensive Python 3.11+ development workflows including test-driven development, linting, and modern patterns |
| [uv](./plugins/uv) | Expert guidance for Astral's uv - fast Python package and project manager |
| [async-python-patterns](./plugins/async-python-patterns) | Python asyncio, concurrent programming, and async/await patterns |
| [hatchling](./plugins/hatchling) | Modern Python build backend implementing PEP 517/518/621/660 standards |
| [pypi-readme-creator](./plugins/pypi-readme-creator) | Create PyPI-compatible README files with proper formatting |
| [toml-python](./plugins/toml-python) | Read and write TOML config files in Python while preserving formatting |

### Code Quality & Linting

| Plugin | Description |
|--------|-------------|
| [holistic-linting](./plugins/holistic-linting) | Comprehensive linting workflows with format, lint, and resolve pipelines |
| [pre-commit](./plugins/pre-commit) | Set up automated code quality checks with pre-commit hooks |
| [clang-format](./plugins/clang-format) | C/C++ code formatting configuration and style analysis |

### Git & Version Control

| Plugin | Description |
|--------|-------------|
| [conventional-commits](./plugins/conventional-commits) | Write standardized commit messages following Conventional Commits spec |
| [commitlint](./plugins/commitlint) | Commit message validation and CI/CD enforcement |
| [gitlab-skill](./plugins/gitlab-skill) | GitLab CI/CD pipelines, GLFM syntax, and gitlab-ci-local testing |

### AI & LLM Development

| Plugin | Description |
|--------|-------------|
| [fastmcp-creator](./plugins/fastmcp-creator) | Build Model Context Protocol (MCP) servers with FastMCP framework |
| [litellm](./plugins/litellm) | Call LLM APIs from Python with provider abstraction |
| [llamafile](./plugins/llamafile) | Set up local LLM inference with llamafile and GGUF models |
| [prompt-optimization-claude-45](./plugins/prompt-optimization-claude-45) | Optimize CLAUDE.md files and skills following Anthropic best practices |

### Documentation

| Plugin | Description |
|--------|-------------|
| [mkdocs](./plugins/mkdocs) | Create MkDocs documentation projects with Material theme |

### Agent Workflows & Patterns

| Plugin | Description |
|--------|-------------|
| [agent-orchestration](./plugins/agent-orchestration) | Scientific delegation framework for multi-agent task coordination |
| [brainstorming-skill](./plugins/brainstorming-skill) | 30+ research-validated prompt patterns for structured ideation |
| [story-based-framing](./plugins/story-based-framing) | Narrative structure for pattern description and detection |
| [verification-gate](./plugins/verification-gate) | Pre-action verification checkpoints for hypothesis-action alignment |

### System Configuration

| Plugin | Description |
|--------|-------------|
| [xdg-base-directory](./plugins/xdg-base-directory) | XDG Base Directory specification for cross-platform file storage |

## Plugin Structure

Each plugin follows the Claude Code plugin structure:

```text
plugins/plugin-name/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest with metadata
├── skills/
│   └── skill-name/
│       ├── SKILL.md      # Skill definition with frontmatter
│       └── references/   # Supporting documentation
├── commands/             # Slash commands (optional)
├── agents/               # Sub-agent definitions (optional)
├── docs/                 # Generated documentation
└── README.md             # Plugin documentation
```

## Creating New Plugins

Use the skill-creator to create new plugins:

```bash
# Ask Claude to create a new skill
"Create a new skill for [topic]"
```

After creating skills, run the installation script:

```bash
./install.py
```

This creates symlinks in `~/.claude/skills/` making skills immediately available.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add or modify plugins following the structure above
4. Run `./install.py` to test locally
5. Submit a pull request

## License

MIT License - see individual plugins for specific licensing.

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Anthropic Skills Repository](https://github.com/anthropics/claude-skills)
