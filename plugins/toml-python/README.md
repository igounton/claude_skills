# toml-python Plugin

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Claude Code](https://img.shields.io/badge/claude--code-compatible-purple)

A Claude Code plugin for working with TOML configuration files in Python using the tomlkit library, which preserves comments and formatting during read-modify-write cycles.

## Features

- **Comment-Preserving Editing** - Modify TOML files while maintaining user comments and formatting
- **tomlkit API Reference** - Complete guide to reading, writing, and manipulating TOML documents
- **Config Management Patterns** - Best practices for atomic updates, validation, and default config creation
- **Error Handling** - Comprehensive exception handling patterns for robust config file operations
- **XDG Integration** - Patterns for XDG Base Directory specification compliance
- **Type Safety** - TOML-to-Python type mapping guidance and validation patterns

## Installation

### Prerequisites

- Claude Code 2.1 or later
- Python 3.8+ (for tomlkit)
- Python 3.11+ (for stdlib tomllib alternative)

### Install Plugin

```bash
# Method 1: If published to a marketplace
/plugin install toml-python@your-marketplace

# Method 2: Manual installation
git clone <repository-url> ~/.claude/plugins/toml-python
```

### Install Python Dependencies

The skill provides guidance for installing tomlkit:

```bash
# Using uv (recommended)
uv add tomlkit

# Using pip
pip install tomlkit
```

## Quick Start

The toml-python skill automatically activates when you work with TOML files. Here's a minimal example:

```python
import tomlkit

# Read existing config (preserves comments)
with open('config.toml', 'r') as f:
    doc = tomlkit.load(f)

# Modify a value
doc['database']['port'] = 5433

# Write back (comments preserved)
with open('config.toml', 'w') as f:
    tomlkit.dump(doc, f)
```

## Capabilities

This plugin provides one comprehensive skill for TOML file handling:

| Type | Name | Description | Invocation |
|------|------|-------------|------------|
| Skill | toml-python | TOML file reading, writing, and manipulation with tomlkit. Preserves comments and formatting. | Auto-activates or `@toml-python` |

## Usage

### Automatic Activation

The toml-python skill automatically activates when Claude detects you're:

- Reading or writing `.toml` files
- Working with `pyproject.toml` or config files
- Using tomlkit or tomllib in Python code
- Designing configuration file formats
- Implementing atomic config file updates

### Manual Activation

Explicitly activate the skill in your prompt:

```
@toml-python

Help me create a config file management system for my Python app
```

Or use the Skill tool:

```python
Skill(command: "toml-python")
```

### Core Use Cases

#### 1. Creating Configuration Files

```python
from tomlkit import document, table, comment, nl

doc = document()
doc.add(comment("Application configuration"))
doc.add(nl())

app = table()
app["name"] = "myapp"
app["version"] = "1.0.0"
app["debug"] = False
doc["app"] = app

with open('config.toml', 'w') as f:
    tomlkit.dump(doc, f)
```

#### 2. Updating Config While Preserving Comments

```python
import tomlkit

def update_config_value(path: str, section: str, key: str, value):
    """Update single value while preserving all comments."""
    with open(path, 'r') as f:
        doc = tomlkit.load(f)

    if section not in doc:
        doc[section] = tomlkit.table()

    doc[section][key] = value

    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

# All comments in config.toml remain intact
update_config_value('config.toml', 'database', 'port', 5433)
```

#### 3. Atomic Config Updates

```python
import tomlkit
from pathlib import Path
import tempfile
import shutil

def atomic_config_update(path: Path, updates: dict):
    """Update config atomically to prevent corruption."""
    with open(path, 'r') as f:
        doc = tomlkit.load(f)

    # Apply updates
    for section, values in updates.items():
        if section not in doc:
            doc[section] = tomlkit.table()
        for key, value in values.items():
            doc[section][key] = value

    # Write to temp file, then atomic move
    temp_fd, temp_path = tempfile.mkstemp(suffix='.toml')
    try:
        with open(temp_fd, 'w') as f:
            tomlkit.dump(doc, f)
        shutil.move(temp_path, path)
    except Exception:
        Path(temp_path).unlink(missing_ok=True)
        raise
```

#### 4. Config Validation

```python
import tomlkit
from tomlkit.exceptions import ParseError

def validate_config(path: str) -> tuple[bool, str]:
    """Validate config structure. Returns (is_valid, error_message)."""
    try:
        with open(path, 'r') as f:
            doc = tomlkit.load(f)
    except FileNotFoundError:
        return False, "Config file not found"
    except ParseError as e:
        return False, f"Invalid TOML at line {e.line}, col {e.col}"

    required_sections = ['app', 'database']
    missing = [s for s in required_sections if s not in doc]

    if missing:
        return False, f"Missing sections: {', '.join(missing)}"

    if 'name' not in doc.get('app', {}):
        return False, "Missing required key: app.name"

    return True, ""
```

## Library Selection: tomlkit vs tomllib

The skill provides guidance on choosing the right library:

### Use tomlkit when:
- Modifying existing config files (preserves comments and formatting)
- Building applications that write configuration
- Need single library for both reading and writing
- Python 3.8+ compatibility required

### Use tomllib (stdlib) when:
- Python 3.11+ only
- Read-only access sufficient (no writing capability)
- Minimal dependencies preferred

**Recommendation:** For config file management, tomlkit is the recommended choice due to comment preservation and write capabilities.

## Key Features

### Comment Preservation

tomlkit maintains all user comments when modifying TOML files:

```python
original = """
# Configuration file
[database]
# Database host
host = "localhost"
# Database port
port = 5432
"""

doc = tomlkit.parse(original)
doc['database']['port'] = 5433

result = tomlkit.dumps(doc)
# All comments are preserved in result
```

**Why this matters:** User-added comments in config files should survive application updates.

### Format Preservation

tomlkit maintains:
- Original indentation
- Whitespace patterns
- Key ordering
- Comment placement
- Quote style preferences

**Why this matters:** Minimal diffs in version control when config changes.

## Common Pitfalls

### Losing Comments with unwrap()

```python
# ❌ Wrong: Using unwrap() loses formatting
doc = tomlkit.load(f)
pure_dict = doc.unwrap()
# Modifications to pure_dict lose all comments

# ✓ Correct: Modify doc directly
doc = tomlkit.load(f)
doc["section"]["key"] = "value"
# Comments preserved
```

### Type Assumptions

```python
# ❌ Wrong: Assuming types
value = doc["port"]  # Might be string or int

# ✓ Correct: Validate types
port = doc["port"]
if not isinstance(port, int):
    raise ValueError(f"Expected int for port, got {type(port)}")
```

### Missing Key Access

```python
# ❌ Wrong: Direct access without checking
value = doc["section"]["key"]  # KeyError if missing

# ✓ Correct: Use .get() with defaults
value = doc.get("section", {}).get("key", "default")
```

## Integration with Other Skills

The toml-python skill references related capabilities:

- **xdg-base-directory** - For XDG-compliant config file locations
- **python3-development** - For Python development patterns
- **uv** - For dependency management

Activate related skills with:
```
@xdg-base-directory
```

## Troubleshooting

### Parse Errors

**Issue:** Invalid TOML syntax causes `ParseError`

**Solution:**
```python
from tomlkit.exceptions import ParseError

try:
    doc = tomlkit.parse(toml_string)
except ParseError as e:
    print(f"Parse error at line {e.line}, column {e.col}: {e}")
```

### File Not Found

**Issue:** Config file doesn't exist yet

**Solution:** Use load-or-create pattern:
```python
from pathlib import Path

def load_or_create_config(path: Path):
    if path.exists():
        with open(path, 'r') as f:
            return tomlkit.load(f)

    # Create default config
    doc = tomlkit.document()
    doc.add(tomlkit.comment("Default configuration"))
    # ... add default values ...

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

    return doc
```

### Key Already Exists

**Issue:** `KeyAlreadyPresent` exception when adding duplicate keys

**Solution:**
```python
# Check before adding
if "key" not in doc["section"]:
    doc["section"]["key"] = value
else:
    doc["section"]["key"] = value  # Update existing
```

## Examples

### Example 1: Application Config Management

**Scenario:** Build a config management system for a Python application with persistent storage, validation, and defaults.

**Implementation:**

```python
from dataclasses import dataclass
import tomlkit
from pathlib import Path

@dataclass
class AppConfig:
    name: str
    version: str
    debug: bool = False

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    pool_size: int = 10

@dataclass
class Config:
    app: AppConfig
    database: DatabaseConfig

def load_config(path: Path) -> Config:
    """Load TOML config into dataclasses."""
    with open(path, 'r') as f:
        data = tomlkit.load(f)

    return Config(
        app=AppConfig(**data.get('app', {})),
        database=DatabaseConfig(**data.get('database', {})),
    )

def save_config(config: Config, path: Path):
    """Save dataclasses to TOML, preserving existing comments."""
    if path.exists():
        with open(path, 'r') as f:
            doc = tomlkit.load(f)
    else:
        doc = tomlkit.document()

    # Update from dataclasses
    if 'app' not in doc:
        doc['app'] = tomlkit.table()
    doc['app']['name'] = config.app.name
    doc['app']['version'] = config.app.version
    doc['app']['debug'] = config.app.debug

    if 'database' not in doc:
        doc['database'] = tomlkit.table()
    doc['database']['host'] = config.database.host
    doc['database']['port'] = config.database.port
    doc['database']['name'] = config.database.name
    doc['database']['pool_size'] = config.database.pool_size

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)
```

**Result:** Type-safe config management with comment preservation.

### Example 2: CLI Tool Configuration

**Scenario:** Create a CLI tool that reads user config from `~/.config/mytool/config.toml`

**Implementation:**

```python
import tomlkit
from pathlib import Path

def get_config_path() -> Path:
    """Get XDG-compliant config path."""
    return Path.home() / '.config' / 'mytool' / 'config.toml'

def load_or_create_default():
    """Load existing config or create default."""
    path = get_config_path()

    if path.exists():
        with open(path, 'r') as f:
            return tomlkit.load(f)

    # Create default
    doc = tomlkit.document()
    doc.add(tomlkit.comment("mytool configuration"))
    doc.add(tomlkit.nl())

    doc["general"] = tomlkit.table()
    doc["general"]["editor"] = "vim"
    doc["general"]["color"] = True

    doc["api"] = tomlkit.table()
    doc["api"]["timeout"] = 30
    doc["api"]["retries"] = 3

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

    return doc

# Usage
config = load_or_create_default()
editor = config["general"]["editor"]
timeout = config["api"]["timeout"]
```

**Result:** CLI tool with persistent, user-editable configuration.

### Example 3: pyproject.toml Manipulation

**Scenario:** Programmatically update `pyproject.toml` to add a new dependency

**Implementation:**

```python
import tomlkit
from pathlib import Path

def add_dependency(package: str, version: str = "*"):
    """Add dependency to pyproject.toml."""
    path = Path("pyproject.toml")

    with open(path, 'r') as f:
        doc = tomlkit.load(f)

    # Ensure dependencies section exists
    if "tool" not in doc:
        doc["tool"] = tomlkit.table()
    if "poetry" not in doc["tool"]:
        doc["tool"]["poetry"] = tomlkit.table()
    if "dependencies" not in doc["tool"]["poetry"]:
        doc["tool"]["poetry"]["dependencies"] = tomlkit.table()

    # Add dependency
    deps = doc["tool"]["poetry"]["dependencies"]
    if package not in deps:
        deps[package] = version
        print(f"Added {package} = {version}")
    else:
        print(f"{package} already exists: {deps[package]}")

    # Write back
    with open(path, 'w') as f:
        tomlkit.dump(doc, f)

# Usage
add_dependency("requests", "^2.31.0")
add_dependency("rich", "^13.0.0")
```

**Result:** Automated dependency management with preserved formatting and comments.

## References

### tomlkit Documentation
- [tomlkit Documentation](https://tomlkit.readthedocs.io/) - Complete API reference
- [tomlkit PyPI](https://pypi.org/project/tomlkit/) - Package information
- [tomlkit GitHub](https://github.com/sdispater/tomlkit) - Source code

### TOML Specification
- [TOML v1.0.0 Specification](https://toml.io/en/) - Official TOML language specification

### Python Standard Library
- [tomllib Documentation](https://docs.python.org/3.11/library/tomllib.html) - Stdlib alternative (read-only, Python 3.11+)

### Related Tools
- `tomli_w` - Stdlib-compatible TOML writer

## Contributing

This plugin is part of the claude_skills repository. To contribute:

1. Fork the repository
2. Make your changes to the skill content
3. Test the skill with Claude Code
4. Submit a pull request with clear description of changes

## License

This plugin is provided as-is for use with Claude Code. Check the repository root for license information.

## Credits

Maintained as part of the Claude Code skills ecosystem.
