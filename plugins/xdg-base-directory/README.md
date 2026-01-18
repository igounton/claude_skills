# XDG Base Directory

Makes Claude organize application files properly on Linux and Unix systems.

## Why Install This?

When you ask Claude to build CLI tools or Python applications, it might:
- Clutter your home directory with files like `~/.myapp-config`
- Hardcode paths instead of respecting your environment settings
- Mix configuration files with cache data
- Break when you try to customize file locations

This plugin teaches Claude the standard Linux file organization conventions.

## What Changes

With this plugin installed, Claude will:
- Store config files in `~/.config/appname/` instead of `~/.appname`
- Put data files in `~/.local/share/appname/`
- Put cache in `~/.cache/appname/`
- Put log files in `~/.local/state/appname/`
- Respect your XDG environment variables if you've customized them
- Validate paths correctly (absolute paths only, per specification)
- Handle cross-platform storage when using the platformdirs library

## Installation

```bash
/plugin install xdg-base-directory
```

## Usage

Just install it and it works automatically. You'll notice the difference when you ask Claude to:
- "Create a CLI tool that saves configuration"
- "Build a Python app that downloads and caches data"
- "Write a script that logs user history"
- "Make this app respect XDG environment variables"

## Example

**Without this plugin**:
```python
# Claude might write this
config_file = Path.home() / '.myapp' / 'config.toml'
```
Result: Your home directory fills up with dotfiles.

**With this plugin**:
```python
# Claude writes this instead
def get_config_dir() -> Path:
    xdg = os.environ.get('XDG_CONFIG_HOME')
    base = Path(xdg) if xdg and Path(xdg).is_absolute() else Path.home() / '.config'
    return base / 'myapp'

config_file = get_config_dir() / 'config.toml'
```
Result: Clean home directory, proper organization, respects your customizations.

## What You Get

- Proper file organization following Linux standards
- Clean home directory (no more scattered dotfiles)
- Environment variable support for custom locations
- Correct handling of config vs data vs cache vs state
- Cross-platform awareness with platformdirs
- Test code that validates XDG compliance

## Requirements

- Claude Code v2.0+
- Works best for Linux/Unix development
- Also covers cross-platform apps (macOS, Windows) when using platformdirs
