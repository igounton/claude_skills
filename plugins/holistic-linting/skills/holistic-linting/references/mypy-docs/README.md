# Mypy Error Code Documentation (Local Cache)

This directory contains locally-cached mypy error code documentation from the official mypy repository.

## Files

- `error_code_list.rst` - Primary mypy error codes documentation
- `error_code_list2.rst` - Additional mypy error codes documentation

## Source

These files are downloaded from the official mypy GitHub repository:

- Source: <https://github.com/python/mypy/tree/master/docs/source>
- File 1: <https://github.com/python/mypy/raw/refs/heads/master/docs/source/error_code_list.rst>
- File 2: <https://github.com/python/mypy/raw/refs/heads/master/docs/source/error_code_list2.rst>
- Last updated: 2025-12-03

## Purpose

These files are cached locally to provide fast lookup of mypy error codes during linting resolution workflows. This avoids network latency and ensures consistent documentation availability.

## Usage

When encountering a mypy error with error code `[error-code-name]`, search these files:

```bash
grep -n "error-code-name" /path/to/holistic-linting/references/mypy-docs/*.rst
```

Or read the files directly using the Read tool:

```claude
Read("/path/to/holistic-linting/references/mypy-docs/error_code_list.rst")
Read("/path/to/holistic-linting/references/mypy-docs/error_code_list2.rst")
```

## Updating

To update the cached documentation:

```bash
cd /path/to/holistic-linting/references/mypy-docs
curl -L -o error_code_list.rst "https://github.com/python/mypy/raw/refs/heads/master/docs/source/error_code_list.rst"
curl -L -o error_code_list2.rst "https://github.com/python/mypy/raw/refs/heads/master/docs/source/error_code_list2.rst"
```

## Error Code Format

Mypy error codes appear in square brackets in error messages:

```text
error: Incompatible return value type  [return-value]
error: Cannot determine type of 'x'  [has-type]
error: Name 'foo' is not defined  [name-defined]
```

The documentation files use ReStructuredText format with sections for each error code explaining:

- What the error detects
- When code triggers the error
- Examples of error-producing code
- Examples of corrected code
- Configuration options
