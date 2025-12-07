# Custom Claude Skills

This repository contains custom Agent Skills for Claude - modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools.

## Skills in This Repository

- **opinionated-python-development** - Opinionated Python development workflow and best practices
- **clang-format** - C/C++ code formatting with clang-format
- **uv** - Expert guidance for Astral's uv Python package and project manager

## Using These Skills in Claude Code

Install this skill collection:

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
/plugin install development-skills@jamie-bitflight-skills
```

## Creating New Skills

Use the skill-creator skill (from the official Anthropic skills) to create new skills in this repository:

```bash
# The skill-creator skill is already available in Claude Code
# Just ask Claude to create a new skill and it will use the skill-creator
```

## Installing Skills Locally

After creating or modifying skills in this repository, run the installation script to make them available to Claude Code:

```bash
./install.py
```

This script discovers all skills (directories containing SKILL.md) and creates symlinks in `~/.claude/skills/`, making them immediately available for use.

## About Agent Skills

Skills are self-contained directories, each containing:

- `SKILL.md` (required): YAML frontmatter + markdown instructions
- `scripts/` (optional): Executable Python/Bash code
- `references/` (optional): Documentation loaded into context as needed
- `assets/` (optional): Files used in output (templates, images, fonts)

For more information, see the [official Agent Skills repository](https://github.com/anthropics/claude-skills).

## References

- [comfy-claude-prompt-lbrary](https://github.com/Comfy-Org/comfy-claude-prompt-library/tree/master)

# Test line 1764964946

# Another test 1764971205
