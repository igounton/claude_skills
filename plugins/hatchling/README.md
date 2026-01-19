# Hatchling

Expert guidance for Python packaging with Hatchling, the modern build backend.

## Why Install This?

When you're working on Python projects that use Hatchling, Claude often:

- Gives generic packaging advice that doesn't match Hatchling's approach
- Suggests outdated setuptools patterns instead of modern pyproject.toml configuration
- Can't help troubleshoot specific Hatchling build errors
- Misses important configuration options or best practices

This plugin gives Claude comprehensive knowledge of Hatchling's features, configuration, and troubleshooting.

## What Changes

With this plugin installed, Claude can:

- Write correct pyproject.toml configuration for Hatchling projects
- Explain and configure build hooks, version management, and file selection patterns
- Troubleshoot build errors with specific solutions from Hatchling documentation
- Guide you through setuptools-to-Hatchling migrations
- Help with advanced features like editable installs, dynamic metadata, and custom plugins
- Reference specific PEP standards (517, 518, 621, 660) correctly

## Installation

First, add the marketplace (one-time setup):

```bash
/plugin marketplace add Jamie-BitFlight/claude_skills
```

Then install the plugin:

```bash
/plugin install hatchling@jamie-bitflight-skills
```

## Usage

Just install it - Claude will reference this knowledge automatically when you work with Hatchling projects. You'll notice the difference when you:

- Ask "how do I configure dependencies in pyproject.toml?"
- Request "help me fix this Hatchling build error"
- Say "migrate this project from setuptools to Hatchling"
- Need help with build hooks, version sources, or entry points

## Example

**Without this plugin**: You ask "how do I add a build hook in Hatchling?" Claude gives generic Python build system advice or setuptools patterns.

**With this plugin**: Same question, and Claude explains Hatchling's build hook system with specific configuration examples, shows you how to create custom hooks in `hatch_build.py`, and references the BuildHookInterface with proper initialization and finalization phases.

## What's Included

- Complete pyproject.toml configuration reference (project metadata, build system, dependencies)
- Build target configuration (wheel, sdist, custom builders)
- Build hooks and metadata hooks systems
- Version management (code, regex, environment sources)
- File selection patterns and VCS integration
- Error handling and troubleshooting guides
- Plugin system and extensibility
- PEP compliance details (517, 518, 621, 639, 660)

## Requirements

- Claude Code v2.0+
