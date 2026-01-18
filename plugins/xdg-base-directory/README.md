# XDG Base Directory Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

Implement standardized directory paths for configuration, data, cache, and state files following the XDG Base Directory Specification.

## Features

- **XDG Specification Compliance** - Complete implementation of XDG Base Directory Specification v0.8
- **Environment Variable Handling** - Proper validation and fallback for all XDG environment variables
- **Python Implementation Patterns** - Both stdlib-only and cross-platform (platformdirs) approaches
- **Directory Selection Guidance** - Clear rules for choosing config vs data vs cache vs state directories
- **Anti-Pattern Prevention** - Comprehensive list of common mistakes and their solutions
- **Testing Strategies** - Manual and automated testing approaches for XDG compliance
- **Cross-Platform Support** - Guidance for Linux, macOS, and Windows applications

## Installation

### Prerequisites

- Claude Code version 2.1 or higher
- No external dependencies required

### Install Plugin

**From this repository** (manual installation):

```bash
# Clone or ensure this repository is available
cd /path/to/claude_skills

# Run the installation script to symlink plugins
python3 install.py
```

The plugin will be symlinked from the repository to `~/.claude/plugins/xdg-base-directory/`.

**Verify installation**:

```bash
# Check plugin is loaded
/plugin list
```

You should see `xdg-base-directory` in the enabled plugins list.

## Quick Start

### Automatic Activation

Claude automatically applies this skill when you:

- Discuss storing config, data, cache, or state files
- Mention hardcoded home directory paths like `~/.appname`
- Ask about where user-specific files should be stored
- Work with applications needing cross-platform file storage

### Manual Activation

You can explicitly activate the skill:

```text
@xdg-base-directory
```

Or via the Skill tool:

```text
Skill(command: "xdg-base-directory")
```

## Usage

### When to Use This Skill

Use this skill when:

- Creating CLI tools or applications that store user-specific files
- Implementing configuration file management for Linux/Unix applications
- Building cross-platform Python applications requiring standardized directory paths
- Migrating legacy applications from `~/.appname` to XDG-compliant paths
- Designing file storage architecture for Python packages
- Implementing proper environment variable handling for user directories
- Writing applications that respect user-configured directory preferences
- Testing applications with custom XDG directory overrides

### Core Concepts

The skill covers:

1. **XDG Environment Variables** - Understanding and implementing all XDG environment variables
2. **Directory Selection** - Choosing the appropriate directory for different data types
3. **Path Validation** - Ensuring absolute paths and proper fallback handling
4. **Python Implementation** - Both stdlib-only and platformdirs approaches
5. **Common Anti-Patterns** - Avoiding mistakes like hardcoded paths and relative path acceptance
6. **Testing XDG Compliance** - Verifying correct behavior with environment variable overrides

## Environment Variables Reference

### User-Specific Directories

| Variable | Purpose | Default | Example Use |
|----------|---------|---------|-------------|
| `XDG_CONFIG_HOME` | Configuration files | `~/.config` | Settings, preferences |
| `XDG_DATA_HOME` | User data files | `~/.local/share` | Databases, persistent data |
| `XDG_STATE_HOME` | State files | `~/.local/state` | Logs, history, undo buffers |
| `XDG_CACHE_HOME` | Cache files | `~/.cache` | Temporary data, downloads |
| `XDG_RUNTIME_DIR` | Runtime files | System-set (`/run/user/$UID`) | Sockets, pipes, IPC |

### System-Wide Directories

| Variable | Purpose | Default |
|----------|---------|---------|
| `XDG_DATA_DIRS` | System data search path | `/usr/local/share/:/usr/share/` |
| `XDG_CONFIG_DIRS` | System config search path | `/etc/xdg` |

## Examples

### Example 1: Stdlib-Only Implementation

Create XDG-compliant paths using only Python standard library:

```python
from pathlib import Path
import os

def get_config_home() -> Path:
    """Get XDG_CONFIG_HOME path."""
    xdg = os.environ.get('XDG_CONFIG_HOME')
    if xdg and Path(xdg).is_absolute():
        return Path(xdg)
    return Path.home() / '.config'

# Use in application
config_dir = get_config_home() / 'myapp'
config_file = config_dir / 'config.toml'

# Create directories before writing
config_file.parent.mkdir(parents=True, exist_ok=True)
config_file.write_text('[settings]\ndebug = true')
```

**Result**: Configuration stored in `~/.config/myapp/config.toml` or user-specified `XDG_CONFIG_HOME`.

### Example 2: Cross-Platform Application

Use platformdirs for applications targeting Linux, macOS, and Windows:

```python
from platformdirs import user_config_dir, user_data_dir, user_cache_dir
from pathlib import Path

APP_NAME = 'myapp'
APP_AUTHOR = 'myapp'

# Get platform-appropriate directories
config_dir = Path(user_config_dir(APP_NAME, APP_AUTHOR, ensure_exists=True))
data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR, ensure_exists=True))
cache_dir = Path(user_cache_dir(APP_NAME, APP_AUTHOR, ensure_exists=True))

# Store model in data directory
model_path = data_dir / 'models' / 'model.gguf'
model_path.parent.mkdir(parents=True, exist_ok=True)

# Store config in config directory
config_path = config_dir / 'config.toml'
config_path.write_text('[model]\npath = "models/model.gguf"')
```

**Result**:
- **Linux**: `~/.config/myapp/config.toml`, `~/.local/share/myapp/models/`
- **macOS**: `~/Library/Application Support/myapp/`
- **Windows**: `C:\Users\<user>\AppData\Local\myapp\`

### Example 3: Application-Specific Path Module

Create a dedicated paths module for your application:

```python
# myapp/paths.py
"""Path management for myapp following XDG specification."""
from pathlib import Path
import os

APP_NAME = 'myapp'

def get_config_dir() -> Path:
    """Get myapp config directory."""
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / APP_NAME

def get_config_file() -> Path:
    """Get myapp config file path."""
    return get_config_dir() / 'config.toml'

def get_data_dir() -> Path:
    """Get myapp data directory."""
    xdg = os.environ.get('XDG_DATA_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.local' / 'share'
    return base / APP_NAME

def get_cache_dir() -> Path:
    """Get myapp cache directory."""
    xdg = os.environ.get('XDG_CACHE_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.cache'
    return base / APP_NAME

def ensure_directories() -> None:
    """Create all required directories."""
    for directory in [get_config_dir(), get_data_dir(), get_cache_dir()]:
        directory.mkdir(parents=True, exist_ok=True)

# myapp/__main__.py
from myapp import paths

def main():
    paths.ensure_directories()
    config = paths.get_config_file()
    if not config.exists():
        config.write_text('[defaults]\nverbose = false')
```

**Result**: Clean, reusable path management throughout your application.

### Example 4: Testing XDG Compliance

Verify your application respects XDG environment variables:

```bash
# Test with custom XDG directories
export XDG_CONFIG_HOME=/tmp/test-config
export XDG_DATA_HOME=/tmp/test-data
export XDG_CACHE_HOME=/tmp/test-cache

# Run application
myapp init

# Verify files are in correct locations
ls -la /tmp/test-config/myapp/
ls -la /tmp/test-data/myapp/
ls -la /tmp/test-cache/myapp/

# Test with unset variables (should use defaults)
unset XDG_CONFIG_HOME XDG_DATA_HOME XDG_CACHE_HOME
myapp init
ls -la ~/.config/myapp/
ls -la ~/.local/share/myapp/
ls -la ~/.cache/myapp/
```

**Result**: Verified XDG compliance with both custom and default directory locations.

### Example 5: Common Anti-Pattern Fixes

Transform legacy hardcoded paths to XDG-compliant paths:

**Before (Anti-Pattern)**:

```python
# ❌ Hardcoded legacy path
config_file = Path.home() / '.myapp' / 'config.toml'

# ❌ Ignoring environment variables
config_dir = Path.home() / '.config' / 'myapp'

# ❌ Accepting relative paths
xdg = os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))
return Path(xdg)
```

**After (XDG-Compliant)**:

```python
# ✅ Use XDG_CONFIG_HOME
def get_config_dir() -> Path:
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / 'myapp'

config_file = get_config_dir() / 'config.toml'
```

**Result**: Application respects user directory preferences and follows XDG specification.

## Directory Selection Guide

**Use `XDG_CONFIG_HOME` for:**
- Application settings and preferences
- User-specific configuration files
- TOML/YAML/JSON configuration

**Use `XDG_DATA_HOME` for:**
- Persistent application data
- User-generated content
- Downloaded models or assets
- Database files

**Use `XDG_STATE_HOME` for:**
- Action history (command history, undo buffers)
- Application state that can be regenerated
- Log files specific to user actions

**Use `XDG_CACHE_HOME` for:**
- Temporary files safe to delete
- Downloaded data that can be re-fetched
- Build artifacts and compiled files

**Use `XDG_RUNTIME_DIR` for:**
- Unix domain sockets
- Named pipes (FIFOs)
- Lock files
- **Warning**: Often tmpfs-mounted with size limits; avoid large files

## Troubleshooting

### Problem: Application creates `~/.myapp` instead of `~/.config/myapp`

**Cause**: Hardcoded path not using XDG environment variables

**Solution**: Implement XDG-compliant path functions that check `XDG_CONFIG_HOME` first:

```python
def get_config_dir() -> Path:
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / 'myapp'
```

### Problem: Application fails when `XDG_RUNTIME_DIR` unset

**Cause**: `XDG_RUNTIME_DIR` has no default value per specification

**Solution**: Check for None before using:

```python
runtime_dir = os.environ.get('XDG_RUNTIME_DIR')
if runtime_dir and Path(runtime_dir).is_absolute():
    socket_path = Path(runtime_dir) / 'myapp.sock'
else:
    raise RuntimeError("XDG_RUNTIME_DIR not set by system")
```

### Problem: Application accepts relative paths in XDG variables

**Cause**: Not validating that paths are absolute per XDG specification

**Solution**: Validate paths are absolute, fall back to default otherwise:

```python
xdg = os.environ.get('XDG_CONFIG_HOME')
if xdg and Path(xdg).is_absolute():  # Validate absolute
    return Path(xdg)
return Path.home() / '.config'  # Default for unset or relative
```

### Problem: Directory creation fails when writing files

**Cause**: Parent directories don't exist

**Solution**: Create parent directories before writing:

```python
config_file = get_config_dir() / 'config.toml'
config_file.parent.mkdir(parents=True, exist_ok=True)
config_file.write_text(data)
```

## Related Skills

Activate these skills for related functionality:

- **toml-python** - TOML configuration file parsing and validation with tomllib
- **python3-development** - Modern Python development patterns and best practices
- **uv** - Python package and project management

## References

### Official Documentation

- [XDG Base Directory Specification v0.8](https://specifications.freedesktop.org/basedir-spec/latest/) - Authoritative specification (May 2021)
- [Freedesktop.org Specifications](https://specifications.freedesktop.org/) - All freedesktop specifications
- [XDG Git Repository](https://cgit.freedesktop.org/xdg/xdg-specs/tree/basedir) - Source repository

### Implementation Resources

- [ArchWiki: XDG Base Directory](https://wiki.archlinux.org/title/XDG_Base_Directory) - Comprehensive implementation guide
- [platformdirs Python Library](https://github.com/tox-dev/platformdirs) - Cross-platform Python implementation

## Key Principles

1. **Absolute Paths Only** - Validate all XDG paths are absolute; ignore relative paths
2. **Environment Variable Priority** - Always check XDG environment variables before defaults
3. **Specification Compliance** - Follow XDG Base Directory Specification v0.8 exactly
4. **Directory Creation** - Create parent directories before writing files
5. **Appropriate Storage** - Use correct directory for data type (config vs data vs cache vs state)
6. **Runtime Directory Limits** - Avoid large files in `XDG_RUNTIME_DIR` (tmpfs limits)
7. **Cross-Platform Awareness** - Use platformdirs for macOS/Windows support
8. **Search Path Handling** - Parse colon-separated search paths correctly
9. **No Default for Runtime** - `XDG_RUNTIME_DIR` has no default; check for None
10. **Testing** - Validate XDG compliance with environment variable overrides

## License

This plugin follows the licensing of the claude_skills repository.

## Contributing

Contributions are welcome! Please ensure any changes:
- Maintain XDG Base Directory Specification v0.8 compliance
- Include verification citations for implementation details
- Provide examples demonstrating the change
- Follow the markdown formatting standards in CLAUDE.md
