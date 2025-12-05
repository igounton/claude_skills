# GitLab Skill Scripts

Utility scripts for maintaining the GitLab Claude skill.

## sync-gitlab-docs.py

Downloads and synchronizes GitLab documentation from the official GitLab repository.

### Usage

```bash
# Sync documentation in current directory
./scripts/sync-gitlab-docs.py

# Sync documentation in specific directory
./scripts/sync-gitlab-docs.py --working-dir /path/to/skill

# Force sync bypassing cooldown
./scripts/sync-gitlab-docs.py --force

# Keep temporary files for debugging
./scripts/sync-gitlab-docs.py --no-cleanup
```

### What it does

1. Downloads the latest GitLab CI documentation archive from the official repository
2. Extracts the archive to a temporary directory (`references/ci-new/`)
3. Validates the extraction by checking for expected directory structure and markdown files
4. Atomically replaces the old documentation (`references/ci/`) with the new content
5. Cleans up temporary files (archive and extraction directory)

### Requirements

- Python 3.11+
- Network access to gitlab.com
- Write permissions in the working directory

The script uses PEP 723 inline metadata and will automatically install required dependencies (typer, httpx) when run with uv.

### Output

The script provides progress feedback with Rich formatting:

- Download progress with transfer speed and time remaining
- Extraction progress spinner
- Validation results showing number of markdown files found
- Success/failure panels with clear status messages

### Error Handling

The script handles various error conditions:

- **Network failures**: HTTP errors, timeouts, connection issues
- **Extraction failures**: Corrupt archives, filesystem errors
- **Validation failures**: Missing directories, no markdown files
- **Cleanup failures**: Logged but don't prevent success

All errors are displayed with Rich-formatted panels showing the specific failure reason.

### Development

The script follows modern Python 3.11+ patterns:

- Async I/O for downloads using httpx
- Type hints with Annotated syntax
- Rich for progress and status display
- Atomic directory replacement for safety
- Proper exception hierarchy with context preservation
- Google-style docstrings

To verify the script passes linting:

```bash
uv run ruff check scripts/sync-gitlab-docs.py
uv run mypy scripts/sync-gitlab-docs.py
```
