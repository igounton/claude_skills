# Usage Examples

Concrete examples demonstrating how to use the hatchling skill for common Python packaging scenarios.

## Example 1: New Package Setup

**Scenario**: Create a new Python library with Hatchling from scratch.

**Steps**:

1. Activate the skill and request basic setup:
```text
@hatchling Set up a new Python package called "datatools" with:
- Hatchling as the build backend
- Source layout (src/datatools/)
- MIT license
- Python 3.8+ requirement
```

2. Claude generates a complete `pyproject.toml`:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "datatools"
dynamic = ["version"]
description = "Data manipulation utilities"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[tool.hatchling.version]
path = "src/datatools/__init__.py"

[tool.hatchling.build.targets.wheel]
packages = ["src/datatools"]
```

3. Create the directory structure and build:
```bash
mkdir -p src/datatools
echo '__version__ = "0.1.0"' > src/datatools/__init__.py
python -m build
```

**Result**: A standards-compliant Python package ready for development and distribution.

---

## Example 2: Adding Entry Points

**Scenario**: Add a CLI command to an existing Hatchling-based package.

**Steps**:

1. Request entry point configuration:
```text
@hatchling Add a console script entry point "datatool" that calls datatools.cli:main
```

2. Claude shows the configuration to add:
```toml
[project.scripts]
datatool = "datatools.cli:main"
```

3. Create the CLI module:
```python
# src/datatools/cli.py
def main():
    print("DataTools CLI v0.1.0")
    # CLI logic here

if __name__ == "__main__":
    main()
```

4. Install and test:
```bash
pip install -e .
datatool
```

**Result**: The `datatool` command is available system-wide after installation.

---

## Example 3: Dynamic Version from Git Tags

**Scenario**: Use Git tags for automatic version management with hatch-vcs.

**Steps**:

1. Request hatch-vcs setup:
```text
@hatchling Configure automatic versioning from Git tags using hatch-vcs
```

2. Claude provides the configuration:
```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
dynamic = ["version"]

[tool.hatchling.version]
source = "vcs"

[tool.hatchling.build.hooks.vcs]
version-file = "src/datatools/_version.py"
```

3. Create a Git tag:
```bash
git tag v0.2.0
git push --tags
```

4. Build the package:
```bash
python -m build
```

**Result**: Package version automatically matches Git tag (0.2.0), and a `_version.py` file is generated during build.

---

## Example 4: Custom Build Hook for Asset Compilation

**Scenario**: Compile SCSS stylesheets to CSS during package build.

**Steps**:

1. Request build hook guidance:
```text
@hatchling Create a custom build hook that compiles SCSS files to CSS before building
```

2. Claude provides the hook implementation:
```python
# hatch_build_scss.py (in project root)
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess

class SCSSBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        """Compile SCSS to CSS before file collection."""
        scss_dir = self.root / "src" / "mypackage" / "styles"
        css_dir = scss_dir / "compiled"
        css_dir.mkdir(exist_ok=True)

        for scss_file in scss_dir.glob("*.scss"):
            css_file = css_dir / f"{scss_file.stem}.css"
            subprocess.run(
                ["sass", str(scss_file), str(css_file)],
                check=True
            )

        print(f"Compiled {len(list(scss_dir.glob('*.scss')))} SCSS files")
```

3. Register the hook in `pyproject.toml`:
```toml
[tool.hatchling.build.hooks.custom]
path = "hatch_build_scss.py"

[tool.hatchling.build.hooks.custom.dependencies]
runtime = ["sass"]
```

4. Build the package:
```bash
python -m build
```

**Result**: SCSS files are compiled to CSS automatically during each build, and CSS files are included in the distribution.

---

## Example 5: Optional Dependencies and Feature Groups

**Scenario**: Define optional dependency groups for testing, documentation, and development.

**Steps**:

1. Request optional dependencies configuration:
```text
@hatchling Add optional dependency groups:
- "test": pytest, pytest-cov, pytest-asyncio
- "docs": sphinx, sphinx-rtd-theme
- "dev": includes both test and docs, plus ruff and mypy
```

2. Claude provides the configuration:
```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21",
]
docs = [
    "sphinx>=6.0",
    "sphinx-rtd-theme>=1.2",
]
dev = [
    "datatools[test,docs]",
    "ruff>=0.1",
    "mypy>=1.5",
]
```

3. Install with optional dependencies:
```bash
# Install with test dependencies
pip install -e ".[test]"

# Install with all dev dependencies
pip install -e ".[dev]"

# Install multiple groups
pip install -e ".[test,docs]"
```

**Result**: Users can install only the dependencies they need, and developers get a comprehensive development environment.

---

## Example 6: Including Data Files

**Scenario**: Include non-Python data files (JSON config, templates) in the wheel.

**Steps**:

1. Request data file inclusion guidance:
```text
@hatchling My package has these data files that need to be included:
- src/datatools/config/defaults.json
- src/datatools/templates/*.html
But they're being excluded from the wheel build.
```

2. Claude explains VCS integration and provides solution:
```toml
[tool.hatchling.build.targets.wheel]
packages = ["src/datatools"]

# Ensure data files are tracked in Git
# Or use force-include for files outside VCS:
[tool.hatchling.build.targets.wheel.force-include]
"config/defaults.json" = "datatools/config/defaults.json"
"templates" = "datatools/templates"
```

3. Verify Git tracking:
```bash
git add src/datatools/config/defaults.json
git add src/datatools/templates/*.html
git commit -m "Add data files"
```

4. Rebuild and verify:
```bash
python -m build
unzip -l dist/datatools-*.whl | grep config
```

**Result**: Data files are included in the wheel and accessible via `importlib.resources` or package path.

---

## Example 7: Migrating from setup.py

**Scenario**: Convert an existing setuptools-based project to Hatchling.

**Steps**:

1. Request migration assistance with existing setup.py:
```text
@hatchling Migrate this setup.py to Hatchling in pyproject.toml:

from setuptools import setup, find_packages

setup(
    name="oldproject",
    version="1.2.3",
    packages=find_packages(),
    install_requires=["requests>=2.28", "pydantic>=2.0"],
    extras_require={
        "dev": ["pytest", "black"],
    },
    entry_points={
        "console_scripts": [
            "oldcli=oldproject.cli:main",
        ],
    },
    python_requires=">=3.7",
)
```

2. Claude generates equivalent pyproject.toml:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "oldproject"
version = "1.2.3"
requires-python = ">=3.7"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "black",
]

[project.scripts]
oldcli = "oldproject.cli:main"

[tool.hatchling.build.targets.wheel]
packages = ["oldproject"]
```

3. Test the migration:
```bash
# Remove old setup.py
mv setup.py setup.py.bak

# Test build
python -m build

# Test editable install
pip install -e .

# Verify entry point
oldcli --help
```

**Result**: Project successfully migrated to Hatchling with equivalent functionality.

---

## Example 8: Namespace Packages

**Scenario**: Create a plugin for a namespace package ecosystem.

**Steps**:

1. Request namespace package configuration:
```text
@hatchling Create a namespace package plugin "mynamespace.plugins.myplugin"
using PEP 420 implicit namespaces
```

2. Claude provides directory structure and configuration:

**Directory structure**:
```
src/
└── mynamespace/
    └── plugins/
        └── myplugin/
            └── __init__.py
```

**pyproject.toml**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mynamespace-plugins-myplugin"
version = "0.1.0"

[tool.hatchling.build.targets.wheel]
packages = ["src/mynamespace"]
```

3. Create namespace directories WITHOUT `__init__.py`:
```bash
mkdir -p src/mynamespace/plugins/myplugin
# Note: mynamespace/ and plugins/ have NO __init__.py
echo "# Plugin code" > src/mynamespace/plugins/myplugin/__init__.py
```

4. Build and verify:
```bash
python -m build
python -m zipfile -l dist/*.whl | grep mynamespace
```

**Result**: Plugin installs into the shared namespace without conflicting with other plugins.

---

## Example 9: Environment-Specific Configuration

**Scenario**: Use different build configurations for development vs. production builds.

**Steps**:

1. Request environment-based configuration:
```text
@hatchling Configure the build to:
- Include test fixtures in dev builds
- Exclude them from production builds
- Set different version schemes based on environment
```

2. Claude provides context formatting solution:
```toml
[tool.hatchling.build.targets.wheel]
# Use environment variable for conditional inclusion
include = [
    "src/mypackage/**/*.py",
    "{env:INCLUDE_FIXTURES:}",  # Empty in production, path in dev
]

[tool.hatchling.version]
# Development builds get local version identifier
source = "vcs"
raw-options = { local_scheme = "{env:VERSION_SCHEME:node-and-date}" }
```

3. Build for different environments:
```bash
# Production build (fixtures excluded)
python -m build

# Development build (fixtures included)
INCLUDE_FIXTURES="src/mypackage/test_fixtures/**" python -m build

# Custom version scheme
VERSION_SCHEME="no-local-version" python -m build
```

**Result**: Single configuration adapts to different build contexts via environment variables.

---

## Example 10: Reproducible Builds

**Scenario**: Ensure builds are reproducible for security and verification.

**Steps**:

1. Request reproducible build configuration:
```text
@hatchling Configure reproducible builds with fixed timestamps
```

2. Claude provides the configuration and build command:

**pyproject.toml**:
```toml
[tool.hatchling.build]
reproducible = true

[tool.hatchling.build.targets.wheel]
# Ensure consistent file ordering
strict-naming = false
```

**Build command**:
```bash
# Set SOURCE_DATE_EPOCH for timestamp consistency
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) python -m build

# Verify reproducibility
sha256sum dist/*.whl
rm -rf dist/
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) python -m build
sha256sum dist/*.whl  # Should match previous hash
```

3. Document in CI:
```yaml
# .github/workflows/build.yml
- name: Build package
  env:
    SOURCE_DATE_EPOCH: ${{ github.event.head_commit.timestamp }}
  run: python -m build
```

**Result**: Identical source states produce byte-for-byte identical wheel files, enabling build verification.

---

## Common Patterns Summary

| Pattern | Use Case | Key Configuration |
|---------|----------|-------------------|
| Source layout | Library packages | `packages = ["src/mypackage"]` |
| Dynamic version | Avoid version duplication | `dynamic = ["version"]` + version source |
| Entry points | CLI tools | `[project.scripts]` |
| Optional deps | Feature groups | `[project.optional-dependencies]` |
| Build hooks | Asset compilation | Custom hook + `[tool.hatchling.build.hooks]` |
| Force-include | Non-VCS files | `[tool.hatchling.build.targets.wheel.force-include]` |
| VCS versioning | Git-based versions | `source = "vcs"` + hatch-vcs |
| Namespace packages | Plugin systems | PEP 420 + shared namespace |

---

[← Back to README](../README.md) | [Skills Reference](./skills.md)
