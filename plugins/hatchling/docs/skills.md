# Skills Reference

This plugin provides one comprehensive skill for working with Hatchling, the modern Python build backend.

## hatchling

**Location**: `skills/hatchling/SKILL.md`

**Description**: This skill provides comprehensive documentation for Hatchling, the modern Python build backend that implements PEP 517/518/621/660 standards. Use this skill when working with Hatchling configuration, build system setup, Python packaging, pyproject.toml configuration, project metadata, dependencies, entry points, build hooks, version management, wheel and sdist builds, package distribution, setuptools migration, and troubleshooting Hatchling build errors.

**User Invocable**: Yes (default)

**Allowed Tools**: Inherits from session (no restrictions)

**Model**: Inherits from session (no override)

### When to Use

Claude automatically uses this skill when you:

- **Configure build systems**: Setting up `pyproject.toml` with Hatchling
- **Define project metadata**: Package name, version, dependencies, entry points
- **Work with build targets**: Configuring wheel or sdist builds
- **Create build hooks**: Custom build-time code execution
- **Manage versions**: Setting up version sources (code, regex, env, Git tags)
- **Select files**: Configuring include/exclude patterns, VCS integration
- **Migrate projects**: Converting from setuptools/setup.py to Hatchling
- **Troubleshoot builds**: Debugging build errors, file selection issues, validation failures
- **Extend Hatchling**: Developing custom plugins (builders, hooks, metadata hooks)

### Activation

**Automatic activation** (Claude decides based on context):
```text
Help me set up Hatchling for my Python project
```

**Manual activation** (explicit):
```text
@hatchling
```

**Programmatic activation** (in prompts/commands):
```text
Skill(command: "hatchling")
```

### Documentation Structure

The skill organizes documentation into focused topics for progressive disclosure:

#### Project Configuration (6 topics)
1. **Project Metadata** - Package name, version, authors, dependencies, entry points, classifiers, URLs
2. **Build System Configuration** - Build backend declaration, PEP 517/518 compliance, reproducible builds
3. **Dynamic Fields** - Runtime metadata generation for version, description, dependencies, etc.
4. **Dependencies** - Runtime, optional, feature groups, version constraints, environment markers
5. **Entry Points** - Console scripts, GUI scripts, plugin entry points
6. **Project URLs** - Homepage, documentation, repository, issue tracker, changelog

#### Build Targets (8 topics)
1. **Wheel Target** - Pure Python/binary wheels, package discovery, namespace packages
2. **Source Distribution (Sdist)** - VCS integration, include/exclude patterns, legacy setup.py
3. **Build Target Types** - Default targets, custom builders, multi-version builds
4. **Target Configuration** - Per-target hooks, dependencies, versions
5. **Editable Installs** - Development mode, editable wheel backend
6. **Package Discovery** - Automatic package detection, layout conventions (src/flat)
7. **File Selection** - Include/exclude patterns, force-include, VCS integration
8. **Build Artifacts** - Output location, naming conventions, reproducibility

#### Customization & Extensions (10 topics)
1. **Build Hooks** - Hook interface, execution phases, custom implementations
2. **Version Build Hook** - Automatic version file generation during build
3. **Custom Build Hooks** - Writing plugins, hook registration, configuration
4. **Hook Execution Order** - Initialize → finalize → clean, per-artifact execution
5. **Hook Dependencies** - Build-time dependencies, environment setup
6. **Metadata Hooks** - Dynamic metadata generation, runtime configuration
7. **Plugin System** - Builder plugins, hook plugins, version plugins, metadata plugins
8. **Force-Include** - Include files outside VCS, override patterns, path rewriting
9. **Build Data Passing** - Sharing data between build phases
10. **Conditional Execution** - Environment-based hook execution

#### Version & Metadata Management (5 topics)
1. **Version Management** - Version sources: code, regex, env variables, Git tags (hatch-vcs)
2. **Version Schemes** - Standard, release-branch-semver, custom schemes
3. **Version Validation** - PEP 440 compliance, scheme enforcement
4. **Dynamic Metadata** - Runtime metadata generation patterns
5. **Context Formatting** - Environment variable interpolation, conditional configuration

#### File Selection Patterns (4 topics)
1. **Include/Exclude Patterns** - Git-style glob patterns, precedence rules
2. **VCS Integration** - Automatic file detection from Git, Mercurial
3. **Force-Include Patterns** - Override VCS detection, include specific files
4. **Path Rewriting** - Relocate files during build, flatten directory structures

#### Build Environment & Integration (6 topics)
1. **Build Environment** - Dependency isolation, UV vs pip, virtual environments
2. **Environment Variables** - Build-time configuration, HATCH_BUILD_* variables
3. **PEP Compliance** - Standards implementation (PEP 517, 518, 621, 660)
4. **Setuptools Migration** - Conversion guide, compatibility notes, common patterns
5. **Extension Modules** - C/C++ compilation, CMake integration, Cython support
6. **Reproducible Builds** - SOURCE_DATE_EPOCH, deterministic output

#### CLI & Operations (4 topics)
1. **CLI Building** - `hatch build`, `python -m build`, `pip install`, output options
2. **Build Targets Selection** - Build specific targets, multiple targets, all targets
3. **Build Options** - Output directory, clean builds, hooks configuration
4. **Installation Testing** - Verify builds, editable installs, development workflow

#### Error Handling & Troubleshooting (5 topics)
1. **Path Validation Errors** - Invalid paths, directory structure issues
2. **File Selection Errors** - VCS detection failures, pattern matching issues
3. **Version Validation Errors** - PEP 440 violations, scheme mismatches
4. **License Validation Errors** - SPDX expression parsing, PEP 639 compliance
5. **Heuristic Failures** - Package discovery issues, layout detection problems

### Reference Files

The skill includes 22 subdirectories of focused documentation:

| Directory | Topic Count | Primary Focus |
|-----------|-------------|---------------|
| `project-metadata/` | ~15 files | Package metadata, dependencies, entry points |
| `build-system/` | ~8 files | Build backend configuration, PEP compliance |
| `wheel-target/` | ~12 files | Wheel builds, package discovery, editable installs |
| `sdist-target/` | ~8 files | Source distributions, VCS integration |
| `build-targets/` | ~6 files | Target types, custom builders |
| `target-config/` | ~8 files | Per-target configuration, precedence |
| `file-selection/` | ~10 files | Include/exclude patterns, VCS |
| `build-hooks/` | ~10 files | Hook interface, custom hooks, execution |
| `advanced-features/` | ~8 files | Force-include, path rewriting, build context |
| `version-management/` | ~12 files | Version sources, schemes, validation |
| `metadata-hooks/` | ~6 files | Dynamic metadata generation |
| `context-formatting/` | ~5 files | Environment variables, interpolation |
| `plugins/` | ~10 files | Plugin development, hatch-vcs |
| `build-environment/` | ~8 files | Dependency management, UV integration |
| `integration/` | ~10 files | Setuptools migration, C extensions |
| `special-config/` | ~8 files | Type hints, namespace packages, src-layout |
| `core-concepts/` | ~6 files | Architecture, philosophy, best practices |
| `standards/` | ~12 files | PEP references, metadata specs |
| `cli-building/` | ~6 files | Build commands, CLI options |
| `error-handling/` | ~8 files | Validation, troubleshooting |
| `release-notes/` | ~4 files | Version history, changelog |

### Hooks

This skill does not configure any hooks. It provides documentation-only capabilities.

### Performance Characteristics

**Progressive Disclosure**: The skill's main content (`SKILL.md`) is ~4KB. Detailed reference documentation (~200+ pages total) resides in the `references/` subdirectory and is loaded on-demand when Claude needs specific details. This design:

- Minimizes initial context usage
- Provides immediate high-level guidance
- Loads detailed documentation only when needed
- Preserves context window for your actual work

**Typical Context Usage**:
- Initial activation: ~4KB (SKILL.md only)
- With specific topic: ~4KB + 5-15KB (one reference file)
- Complex multi-topic query: ~4KB + 20-40KB (multiple references)

### Related Skills

This skill complements other Python development skills:

- **python3** - General Python development patterns and best practices
- **uv** - Modern Python package installer and environment manager (integrates with Hatchling builds)
- **ruff** - Fast Python linter/formatter (commonly used in build hooks)

### Common Workflows

#### Setting Up a New Project

```text
@hatchling Create a pyproject.toml for a new library called "mylib" with:
- Hatchling as build backend
- Dynamic version from __init__.py
- Entry point for CLI command "mylib"
- Optional dependencies for "dev" and "test" features
```

#### Configuring Build Hooks

```text
@hatchling I need to compile SCSS to CSS during the build. Show me how to:
1. Create a custom build hook
2. Register it in pyproject.toml
3. Ensure it runs before file collection
```

#### Migrating from Setuptools

```text
@hatchling Migrate this setup.py to Hatchling in pyproject.toml:
[paste setup.py content]
```

#### Troubleshooting Build Issues

```text
@hatchling My wheel build excludes data files in the src/mypackage/data/ directory.
The pyproject.toml has:
[tool.hatchling.build.targets.wheel]
packages = ["src/mypackage"]
```

### Best Practices

When working with Hatchling through this skill:

1. **Start with PEP 621 metadata** - Define standard project fields before Hatchling-specific configuration
2. **Use VCS file selection** - Let Hatchling discover files from Git rather than explicit patterns
3. **Prefer dynamic version sources** - Use `version = {path = "..."}` or hatch-vcs over hardcoded versions
4. **Test builds locally** - Use `python -m build` or `hatch build` before publishing
5. **Use editable installs** - Develop with `pip install -e .` for immediate feedback
6. **Leverage build hooks sparingly** - Only for essential build-time operations
7. **Document custom configuration** - Comment pyproject.toml extensively for team clarity
8. **Follow PEP 517/518** - Ensure build backend configuration is standards-compliant

### Limitations

- **Documentation-only**: This skill provides documentation but doesn't execute builds or modify files directly
- **Version coverage**: Documentation reflects Hatchling 1.x behavior (check release notes for breaking changes)
- **Plugin specifics**: Third-party plugin documentation may be limited (refer to plugin-specific docs)

---

[← Back to README](../README.md)
