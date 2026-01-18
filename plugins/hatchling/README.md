# Hatchling Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A comprehensive Claude Code plugin providing expert-level documentation for Hatchling, the modern Python build backend that implements PEP 517/518/621/660 standards.

## Features

- **Complete Hatchling Reference** - Comprehensive documentation covering all aspects of Hatchling configuration and usage
- **Standards-Compliant** - Detailed coverage of PEP 517, 518, 621, and 660 specifications
- **Build System Expertise** - In-depth guidance on wheel/sdist builds, build hooks, and version management
- **Migration Support** - Clear guidance for migrating from setuptools to Hatchling
- **Plugin Development** - Documentation for extending Hatchling through custom plugins and hooks
- **Progressive Disclosure** - Documentation organized into focused topics, loaded on-demand to preserve context efficiency

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- No external dependencies required

### Install Plugin

```bash
# Method 1: Manual installation
git clone <repository-url> ~/.claude/plugins/hatchling
cc plugin reload

# Method 2: From local path (if available)
cc plugin install ./plugins/hatchling
```

## Quick Start

The hatchling skill is automatically activated by Claude when working with Python packaging. You can also manually activate it:

```text
@hatchling
```

Or use the Skill tool:

```text
Skill(command: "hatchling")
```

**Example use case**: When configuring a Python project's `pyproject.toml` or troubleshooting build errors, the skill provides immediate access to Hatchling-specific documentation without polluting your context window with unnecessary details.

## Capabilities

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | hatchling | Comprehensive Hatchling build backend documentation for Python packaging | `@hatchling` or automatic |

## Usage

### When Claude Uses This Skill

Claude automatically activates the hatchling skill when you:

- Configure `pyproject.toml` with Hatchling as the build backend
- Work with Python package build configuration
- Troubleshoot Hatchling build errors
- Set up project metadata, dependencies, or entry points
- Configure build hooks or version management
- Migrate from setuptools to Hatchling
- Work with wheel or sdist builds
- Configure file selection patterns or VCS integration

### Manual Activation

You can explicitly request the skill:

```
Use the hatchling skill to help me configure my pyproject.toml for a new Python package
```

Or activate it directly:

```
@hatchling
```

### Documentation Organization

The skill provides documentation organized into focused topics:

#### Project Configuration
- **Project Metadata** - Package metadata, dependencies, entry points, dynamic fields
- **Build System Configuration** - Build backend setup, PEP 517/518, reproducible builds

#### Build Targets
- **Wheel Target** - Wheel configuration, package discovery, editable installs
- **Source Distribution (Sdist)** - Sdist configuration, VCS integration
- **Build Target Types** - Custom builders, multi-version builds
- **Target Configuration** - Target-specific hooks, dependencies, versions

#### Customization & Extensions
- **File Selection** - Git-style globs, include/exclude patterns, VCS integration
- **Build Hooks** - Hook interface, custom hooks, version hooks
- **Advanced Features** - Dynamic dependencies, force-include, path rewriting
- **Plugin System** - Builder, hook, metadata, version plugins

#### Version & Metadata
- **Version Management** - Version sources (code, regex, env), schemes, validation
- **Metadata Hooks** - Dynamic metadata generation
- **Context Formatting** - Environment-based configuration, interpolation

#### Integration & Operations
- **Build Environment** - Environment config, dependencies, UV vs pip
- **Integration** - Setup.py migration, setuptools compatibility
- **CLI Building** - Build commands, pip install, output customization
- **Error Handling** - Validation, troubleshooting common issues

## Configuration

This plugin has no hooks, MCP servers, or LSP servers. It provides documentation-only capabilities through the skill system.

## Examples

### Example 1: Basic Hatchling Setup

**Scenario**: Set up a new Python project with Hatchling as the build backend.

**Invocation**:
```text
@hatchling I need to create a pyproject.toml for a new Python package called "myapp"
```

**What Claude provides**: Configuration guidance following PEP 621 standards, including proper build-system table setup, project metadata structure, and dependency specification.

### Example 2: Troubleshooting Build Errors

**Scenario**: Your package build fails with file selection errors.

**Invocation**:
```text
@hatchling Why is Hatchling excluding my data files from the wheel?
```

**What Claude provides**: Explanation of Hatchling's file selection rules, VCS integration behavior, and how to use force-include patterns to include specific files.

### Example 3: Migration from Setuptools

**Scenario**: Convert an existing setup.py-based project to use Hatchling.

**Invocation**:
```text
@hatchling Help me migrate this setup.py to pyproject.toml with Hatchling
```

**What Claude provides**: Step-by-step migration guidance, mapping of setuptools configuration to Hatchling equivalents, and notes on compatibility differences.

### Example 4: Custom Build Hook

**Scenario**: Need to compile assets during the build process.

**Invocation**:
```text
@hatchling How do I create a custom build hook to compile TypeScript assets?
```

**What Claude provides**: Build hook interface documentation, hook registration patterns, execution order details, and examples of custom hook implementation.

### Example 5: Version Management Setup

**Scenario**: Configure automatic version management from Git tags.

**Invocation**:
```text
@hatchling Configure version management using Git tags with the hatch-vcs plugin
```

**What Claude provides**: hatch-vcs plugin configuration, version source setup, version schemes, and integration with build hooks.

## Troubleshooting

### Skill Not Activating

If Claude doesn't automatically use the skill:

1. **Verify installation**: Run `cc plugin list` to confirm the plugin is installed and enabled
2. **Manually activate**: Use `@hatchling` to explicitly activate the skill
3. **Check keywords**: Mention "Hatchling", "pyproject.toml", or "Python packaging" to trigger automatic activation

### Documentation Not Found

If referenced documentation appears unavailable:

1. **Check plugin integrity**: Ensure all files were copied during installation
2. **Verify references directory**: Confirm `/skills/hatchling/references/` exists and contains markdown files
3. **Reinstall plugin**: Use `cc plugin uninstall hatchling` followed by reinstallation

### Context Window Concerns

The skill uses progressive disclosure - Claude loads specific documentation topics on-demand rather than including everything upfront. This preserves your context window for actual work.

## Contributing

Contributions are welcome. When adding or updating documentation:

1. Follow the existing directory structure in `skills/hatchling/references/`
2. Use markdown with proper headings and code fences with language specifiers
3. Include concrete examples with expected input/output
4. Link related topics using relative paths: `[Topic](./path/to/file.md)`
5. Verify all internal links work correctly

## License

This plugin follows the repository's license. Hatchling itself is licensed under MIT.

## Credits

**Plugin Author**: Claude Code community

**Hatchling**: Developed by the [PyPA](https://www.pypa.io/) and [Hatch](https://hatch.pypa.io/) project maintainers

**Documentation Sources**:
- [Hatchling Official Documentation](https://hatch.pypa.io/latest/)
- [Python Packaging User Guide](https://packaging.python.org/)
- PEP specifications (517, 518, 621, 660)

## Related Resources

- [Hatchling Official Docs](https://hatch.pypa.io/latest/) - Upstream documentation
- [PyPA Packaging Guide](https://packaging.python.org/) - Python packaging standards and best practices
- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface specification
- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml
