# Usage Examples

This document provides concrete, real-world examples of using the uv plugin with Claude Code. Each example demonstrates a complete workflow from start to finish.

---

## Example 1: Building a REST API with FastAPI

**Scenario**: You need to create a REST API service with FastAPI, SQLAlchemy for database access, and proper testing infrastructure.

**Steps**:

1. Initialize the application project
2. Add production dependencies
3. Add development dependencies
4. Create application structure
5. Run and test the API

**Code**:

```bash
# 1. Initialize FastAPI application project
uv init fastapi-api --app
cd fastapi-api

# 2. Add production dependencies
uv add "fastapi>=0.115.0" "uvicorn[standard]>=0.32.0" \
     "sqlalchemy>=2.0" "pydantic>=2.5" "pydantic-settings>=2.0"

# 3. Add development dependencies
uv add --dev pytest pytest-asyncio httpx pytest-cov ruff mypy

# 4. Create application structure
cat > main.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="User API", version="1.0.0")

class User(BaseModel):
    id: int
    name: str
    email: str

users_db = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

@app.get("/")
def read_root():
    return {"message": "Welcome to User API"}

@app.get("/users", response_model=list[User])
def list_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}
EOF

# 5. Create test file
cat > test_main.py << 'EOF'
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User API"}

def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
EOF

# 6. Run the application
uv run uvicorn main:app --reload --port 8000

# 7. In another terminal, run tests
uv run pytest -v

# 8. Run linter
uv run ruff check .
```

**Result**:
- Fully configured FastAPI project with type-safe dependencies
- Reproducible environment via `uv.lock`
- Complete test infrastructure
- Development tools (ruff, mypy) isolated in dev dependencies
- Fast dependency installation and execution

---

## Example 2: Creating a Portable Data Analysis Script

**Scenario**: You need to create a self-contained data analysis script that others can run without manual dependency installation.

**Steps**:

1. Initialize script with metadata
2. Add analysis dependencies
3. Write analysis logic
4. Lock dependencies for reproducibility
5. Share the script

**Code**:

```bash
# 1. Initialize script with PEP 723 metadata
uv init --script analyze_sales.py --python 3.11

# 2. Add dependencies
uv add --script analyze_sales.py pandas matplotlib seaborn numpy

# 3. Edit the script (analyze_sales.py now contains dependencies)
cat > analyze_sales.py << 'EOF'
#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.0",
#   "matplotlib>=3.7",
#   "seaborn>=0.12",
#   "numpy>=1.24",
# ]
# ///

"""
Sales Analysis Script
Analyzes sales data and generates visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def main():
    # Sample data
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [15000, 18000, 22000, 19000, 24000, 27000],
        'Expenses': [12000, 13000, 15000, 14000, 16000, 17000]
    }

    df = pd.DataFrame(data)

    # Calculate profit
    df['Profit'] = df['Sales'] - df['Expenses']

    # Print summary
    print("Sales Analysis Summary")
    print("=" * 50)
    print(df.to_string(index=False))
    print(f"\nTotal Sales: ${df['Sales'].sum():,}")
    print(f"Total Expenses: ${df['Expenses'].sum():,}")
    print(f"Total Profit: ${df['Profit'].sum():,}")
    print(f"Average Monthly Profit: ${df['Profit'].mean():,.0f}")

    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Sales vs Expenses
    df.plot(x='Month', y=['Sales', 'Expenses'], ax=ax1, marker='o')
    ax1.set_title('Sales vs Expenses Over Time')
    ax1.set_ylabel('Amount ($)')

    # Profit trend
    df.plot(x='Month', y='Profit', ax=ax2, color='green', marker='o')
    ax2.set_title('Monthly Profit Trend')
    ax2.set_ylabel('Profit ($)')

    plt.tight_layout()
    plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved to: sales_analysis.png")

if __name__ == "__main__":
    main()
EOF

# 4. Lock dependencies for reproducibility
uv lock --script analyze_sales.py

# 5. Make executable
chmod +x analyze_sales.py

# 6. Run the script
./analyze_sales.py

# The script automatically:
# - Creates isolated environment
# - Installs dependencies
# - Runs analysis
# - Generates visualization
```

**Result**:
- Single portable file with embedded dependencies
- No manual environment setup required
- Locked dependencies ensure reproducible results
- Can be shared via email, git, or any file transfer
- Recipients just run `./analyze_sales.py`

---

## Example 3: Migrating from pip/requirements.txt to uv

**Scenario**: You have an existing Python project using `requirements.txt` and `requirements-dev.txt` and want to migrate to modern uv-based management.

**Steps**:

1. Backup existing requirements
2. Initialize uv project
3. Import dependencies
4. Verify migration
5. Clean up old files

**Code**:

```bash
# Starting state: existing project with requirements files
# requirements.txt:
#   flask==2.3.0
#   requests>=2.31.0
#   sqlalchemy==2.0.0
#
# requirements-dev.txt:
#   pytest==7.4.0
#   black==23.7.0
#   mypy==1.5.0

# 1. Backup existing requirements
cp requirements.txt requirements.txt.bak
cp requirements-dev.txt requirements-dev.txt.bak

# 2. Initialize uv in bare mode (no new files except pyproject.toml)
uv init --bare

# 3. Import production dependencies
uv add -r requirements.txt

# 4. Import development dependencies
uv add --dev -r requirements-dev.txt

# 5. Verify the migration
echo "Checking pyproject.toml..."
cat pyproject.toml

# Should now contain:
# [project]
# dependencies = [
#   "flask==2.3.0",
#   "requests>=2.31.0",
#   "sqlalchemy==2.0.0",
# ]
#
# [dependency-groups]
# dev = [
#   "pytest==7.4.0",
#   "black==23.7.0",
#   "mypy==1.5.0",
# ]

# 6. Sync environment to test
uv sync

# 7. Run existing tests to verify compatibility
uv run pytest

# 8. If tests pass, remove old files
rm requirements.txt requirements-dev.txt
rm requirements.txt.bak requirements-dev.txt.bak

# 9. Update CI/CD (if using GitHub Actions)
cat > .github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
      - run: uv python install 3.11
      - run: uv sync --frozen
      - run: uv run pytest
EOF

# 10. Commit changes
git add pyproject.toml uv.lock .github/workflows/ci.yml
git rm requirements.txt requirements-dev.txt
git commit -m "Migrate from pip to uv for dependency management"
```

**Result**:
- Modern `pyproject.toml` replaces requirements files
- `uv.lock` ensures reproducible installs
- Faster dependency resolution and installation
- Simplified CI/CD configuration
- Better dependency group organization

---

## Example 4: Setting Up a Monorepo Workspace

**Scenario**: You're building a project with multiple packages: a shared library, an API service, and a CLI tool that all share common dependencies.

**Steps**:

1. Create workspace structure
2. Configure workspace root
3. Create workspace members
4. Link workspace dependencies
5. Build and test

**Code**:

```bash
# 1. Create root project
mkdir my-monorepo
cd my-monorepo

# 2. Initialize root with workspace configuration
uv init --bare

# Edit pyproject.toml to add workspace config
cat > pyproject.toml << 'EOF'
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv]
managed = true
EOF

# 3. Create workspace members
mkdir -p packages

# Create shared library
cd packages
uv init shared-lib --lib --build-backend hatchling
cd shared-lib
uv add pydantic sqlalchemy

cat > src/shared_lib/models.py << 'EOF'
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
EOF

# Create API service
cd ..
uv init api-service --app
cd api-service

# Add shared-lib as workspace dependency
cat >> pyproject.toml << 'EOF'

[tool.uv.sources]
shared-lib = { workspace = true }
EOF

uv add fastapi uvicorn shared-lib

cat > main.py << 'EOF'
from fastapi import FastAPI
from shared_lib.models import User

app = FastAPI()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return User(id=user_id, name="Test", email="test@example.com")
EOF

# Create CLI tool
cd ..
uv init cli-tool --app
cd cli-tool

# Add shared-lib as workspace dependency
cat >> pyproject.toml << 'EOF'

[tool.uv.sources]
shared-lib = { workspace = true }
EOF

uv add typer rich shared-lib

cat > main.py << 'EOF'
import typer
from rich.console import Console
from shared_lib.models import User

app = typer.Typer()
console = Console()

@app.command()
def show_user(user_id: int):
    user = User(id=user_id, name="Alice", email="alice@example.com")
    console.print(f"User: {user.name} ({user.email})")

if __name__ == "__main__":
    app()
EOF

# 4. Return to root and lock workspace
cd ../..
uv lock

# 5. Run components
# Run API service
uv run --package api-service uvicorn main:app

# Run CLI tool
uv run --package cli-tool python main.py show-user 1

# 6. Build specific packages
uv build --package shared-lib
uv build --package api-service
```

**Result**:
- Single lockfile for entire workspace
- Shared dependencies deduplicated
- Local packages linked without publishing
- Independent package development
- Coordinated versioning and releases

---

## Example 5: Using uvx for Quick Tool Execution

**Scenario**: You need to run various Python CLI tools without permanently installing them or polluting your global environment.

**Steps**:

1. Run tools directly with uvx
2. Use specific versions
3. Add plugins and extensions
4. Run from different packages

**Code**:

```bash
# Run ruff to check code (no installation)
uvx ruff check .

# Run black to format code
uvx black --check .

# Create a project scaffold with cookiecutter
uvx cookiecutter gh:audreyr/cookiecutter-pypackage

# Use specific version of httpie
uvx --from 'httpie>=3.0,<4.0' http GET https://api.github.com/users/astral-sh

# Run mkdocs with material theme plugin
uvx --with mkdocs-material mkdocs serve

# Generate requirements from pyproject.toml
uvx --from pip-tools pip-compile pyproject.toml

# Run pytest with specific plugins
uvx --with pytest-cov --with pytest-asyncio pytest --cov

# Execute one-off Python with packages
uvx --with requests --with rich python << 'EOF'
import requests
from rich import print

response = requests.get("https://api.github.com/repos/astral-sh/uv")
data = response.json()
print(f"[bold green]uv[/bold green] has {data['stargazers_count']} stars!")
EOF

# Check package metadata
uvx --from pkginfo pkginfo dist/my_package-1.0.0-py3-none-any.whl

# Run IPython with data science packages
uvx --with pandas --with matplotlib --with numpy ipython

# Use tool from different package name
uvx --from flask flask --version
```

**Result**:
- No permanent installation required
- Isolated environment per execution
- Can specify exact versions and plugins
- Perfect for CI/CD scripts
- No global environment pollution

---

## Example 6: Docker Multi-Stage Build with uv

**Scenario**: Create an optimized Docker image for a Python application with minimal size and build time.

**Steps**:

1. Create Dockerfile with multi-stage build
2. Leverage uv's speed for fast builds
3. Separate dependencies from code for caching
4. Use virtual environment in final image

**Code**:

```dockerfile
# Dockerfile
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies into .venv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Build the application if needed
RUN uv build

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/src ./src

# Add .venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run application
CMD ["python", "-m", "src.main"]
```

```bash
# Build image
docker build -t my-app:latest .

# Run container
docker run -p 8000:8000 my-app:latest

# For development with live reload
cat > Dockerfile.dev << 'EOF'
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Mount code as volume for live reload
VOLUME /app/src

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
EOF

# Build and run dev image
docker build -f Dockerfile.dev -t my-app:dev .
docker run -p 8000:8000 -v $(pwd)/src:/app/src my-app:dev
```

**Result**:
- Fast Docker builds using uv's speed
- Efficient layer caching (dependencies separate from code)
- Minimal final image size
- Development and production configurations
- Reproducible builds with uv.lock

---

## Example 7: CI/CD with GitHub Actions and Trusted Publishing

**Scenario**: Set up complete CI/CD pipeline with testing, linting, and automatic PyPI publishing using GitHub's trusted publishing.

**Steps**:

1. Create CI workflow for testing
2. Create publishing workflow with trusted publishing
3. Configure repository settings
4. Test and release

**Code**:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --frozen --all-extras

      - name: Run tests
        run: uv run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        with:
          files: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - run: uv python install 3.12
      - run: uv sync --frozen

      - name: Run ruff
        run: uv run ruff check .

      - name: Run mypy
        run: uv run mypy .

      - name: Check formatting
        run: uv run ruff format --check .
```

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/my-package
    permissions:
      id-token: write  # Required for trusted publishing
      contents: read

    steps:
      - uses: actions/checkout@v5

      - uses: astral-sh/setup-uv@v6

      - name: Set up Python
        run: uv python install 3.13

      - name: Build distributions
        run: uv build

      - name: Smoke test
        run: |
          uv run --isolated --no-project \
            --with dist/*.whl \
            python -c "import my_package; print(my_package.__version__)"

      - name: Publish to PyPI
        run: uv publish
        # Uses OIDC trusted publishing - no token needed!
```

**Setup Instructions**:

```bash
# 1. On PyPI (https://pypi.org):
#    - Go to Publishing settings
#    - Add GitHub as trusted publisher
#    - Enter: owner/repo, workflow: publish.yml, environment: pypi

# 2. Create release
git tag v1.0.0
git push origin v1.0.0

# 3. GitHub Actions will:
#    - Run tests on multiple OS/Python versions
#    - Run linters and type checkers
#    - Build distributions
#    - Publish to PyPI automatically
```

**Result**:
- Complete CI pipeline with matrix testing
- Automated linting and type checking
- Secure publishing without manual tokens
- Fast builds with uv caching
- Multi-platform testing
- Automatic PyPI releases on tags

---

[← Back to README](../README.md)
