# Usage Examples

Concrete, real-world examples of using the pypi-readme-creator plugin.

## Example 1: Creating README for a CLI Tool Package

**Scenario**: You've developed a command-line tool for managing configuration files and need a README that appeals to both Python developers and CLI users.

**Invocation**:

```
@pypi-readme-creator

Create a README.md for my CLI tool package "config-manager" that:
- Shows installation via pip and pipx
- Demonstrates basic CLI usage with example commands
- Includes a Python API section for programmatic use
- Features: YAML/TOML/JSON support, environment variable expansion, schema validation
- Python 3.11+ required
- Links to docs at https://config-manager.readthedocs.io
- MIT license
```

**Generated Structure**:

```markdown
# config-manager

![PyPI version](https://img.shields.io/pypi/v/config-manager.svg)
![Python versions](https://img.shields.io/pypi/pyversions/config-manager.svg)

Powerful configuration file manager with schema validation and environment variable expansion.

## Installation

### As a CLI tool

```bash
pipx install config-manager
```

### As a Python library

```bash
pip install config-manager
# or
uv add config-manager
```

## Quick Start

### Command Line

```bash
# Validate configuration
config-manager validate config.yaml

# Merge multiple configs
config-manager merge base.yaml overrides.yaml -o final.yaml
```

### Python API

```python
from config_manager import ConfigManager

manager = ConfigManager("config.yaml")
config = manager.load()
print(config.database.host)  # Outputs: localhost
```

[Rest of README with features, documentation link, license...]
```

**Result**: A dual-purpose README that serves both CLI users (who may not write Python) and developers (who want API documentation).

---

## Example 2: Converting Sphinx Docs to PyPI README

**Scenario**: You have comprehensive Sphinx documentation and want to automatically generate a PyPI-compliant README from your docs/index.rst without maintaining two separate files.

**Steps**:

```
@pypi-readme-creator

Help me set up sphinx-readme for my package "data-pipeline".

Current structure:
- docs/index.rst - main documentation entry
- docs/installation.rst - installation guide
- docs/quickstart.rst - quick start guide
- docs/api.rst - API reference with :py:func: roles

I want README.rst to include content from index.rst and quickstart.rst,
but skip the API reference since it uses Sphinx autodoc.
```

**Generated Configuration**:

**1. Install sphinx-readme**:

```bash
uv add --group docs sphinx-readme
```

**2. Update docs/conf.py**:

```python
# Add to extensions list
extensions = [
    'sphinx_readme',
    # ... other extensions
]

# Configure sphinx-readme
readme_config = {
    'src_file': 'index.rst',
    'out_file': '../README.rst',
}
```

**3. Update docs/index.rst** to create a PyPI-friendly section:

```rst
Welcome to data-pipeline
=========================

A high-performance data processing pipeline for ETL workflows.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   api

PyPI Package Description
------------------------

data-pipeline provides a simple yet powerful framework for building
data processing pipelines with support for parallel execution, error
handling, and monitoring.

Key Features:

* Parallel processing with configurable workers
* Built-in retry logic and error handling
* Real-time monitoring and metrics
* Type-safe pipeline definitions

Quick Start
-----------

.. include:: quickstart.rst
   :start-after: installation-end
   :end-before: advanced-usage
```

**4. Build and validate**:

```bash
# Generate README.rst
uv run sphinx-build -b html docs/ docs/_build/html

# Verify README was created
ls -l README.rst

# Validate PyPI rendering
uv build
uv run --with twine twine check dist/*
```

**Result**: Automatically generated README.rst that stays synchronized with Sphinx documentation, with Sphinx-specific roles converted to PyPI-compatible equivalents.

---

## Example 3: Fixing README Validation Errors

**Scenario**: Your package is ready to publish but `twine check` reports errors in your README.rst file.

**Error Output**:

```
Checking dist/mypackage-1.0.0.tar.gz: FAILED
  `long_description` has syntax errors in markup and would not be rendered on PyPI.
    line 45: Error: Unknown interpreted text role "py:func".
    line 67: Error: Unknown directive type "automodule".
    line 89: Warning: Unexpected indentation.
```

**Invocation**:

```
@pypi-readme-creator

My README.rst fails twine check with these errors:
- Line 45: Unknown interpreted text role "py:func"
- Line 67: Unknown directive type "automodule"
- Line 89: Unexpected indentation

Here's the relevant content around those lines:

Line 45: See :py:func:`mypackage.process` for details.
Line 67: .. automodule:: mypackage.core
Line 89: (code block with indentation issue)

Fix these to be PyPI-compliant.
```

**Fixes Provided**:

**Line 45 - Sphinx Role**:

```rst
❌ Before:
See :py:func:`mypackage.process` for details.

✓ After:
See ``mypackage.process()`` for details.

# Or with external link:
See `mypackage.process() <https://mypackage.readthedocs.io/api.html#mypackage.process>`_ for details.
```

**Line 67 - Sphinx Directive**:

```rst
❌ Before:
.. automodule:: mypackage.core
   :members:

✓ After:
API Reference
-------------

For complete API documentation, see https://mypackage.readthedocs.io/api.html

Core functions:

* ``process(data, **options)`` - Process input data
* ``validate(schema)`` - Validate data against schema
* ``export(format='json')`` - Export results
```

**Line 89 - Indentation**:

```rst
❌ Before:
.. code-block:: python

import mypackage  # No blank line after directive, wrong indent

✓ After:
.. code-block:: python

   import mypackage  # Blank line + 3-space indent
   result = mypackage.process("data")
```

**Validation**:

```bash
# Test RST syntax
uv run --with docutils rst2html.py README.rst /dev/null

# Rebuild and recheck
uv build
uv run --with twine twine check dist/*
```

**Expected Output**:

```
Checking dist/mypackage-1.0.0-py3-none-any.whl: Passed
Checking dist/mypackage-1.0.0.tar.gz: Passed
```

**Result**: All PyPI validation errors resolved, README renders correctly on PyPI.

---

## Example 4: Creating README for Data Science Package

**Scenario**: You've created a machine learning library and need a README that appeals to data scientists with code examples, performance metrics, and visualization.

**Invocation**:

```
@pypi-readme-creator

Create a README.md for my ML package "fast-inference" targeting data scientists.

Package details:
- Name: fast-inference
- Description: High-performance inference engine for scikit-learn and PyTorch models
- Key features: 50x faster than native, GPU support, batch processing, ONNX export
- Installation: pip install fast-inference
- Python 3.11+ with optional GPU support
- Show a performance comparison table
- Include code example with scikit-learn model
- Link to Jupyter notebook examples
- Apache 2.0 license
```

**Generated README**:

```markdown
# fast-inference

![PyPI version](https://img.shields.io/pypi/v/fast-inference.svg)
![Python versions](https://img.shields.io/pypi/pyversions/fast-inference.svg)
![License](https://img.shields.io/pypi/l/fast-inference.svg)

High-performance inference engine for scikit-learn and PyTorch models. Achieve up to 50x faster predictions with GPU acceleration and optimized batch processing.

## Features

- **50x Faster** - Optimized inference engine outperforms native implementations
- **GPU Acceleration** - Seamless CUDA support for PyTorch and compatible models
- **Batch Processing** - Efficient batch inference with automatic memory management
- **ONNX Export** - Convert models to ONNX format for deployment
- **Zero-Copy Operations** - Minimize memory overhead during inference
- **Type Safety** - Full type hints and runtime validation

## Installation

### Basic Installation

```bash
pip install fast-inference
# or
uv add fast-inference
```

### With GPU Support

```bash
pip install fast-inference[gpu]
```

## Quick Start

```python
from sklearn.ensemble import RandomForestClassifier
from fast_inference import optimize

# Train your model as usual
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Optimize for fast inference
fast_model = optimize(model)

# Predict with 50x speedup
predictions = fast_model.predict(X_test)
```

## Performance

| Model Type | Native | fast-inference | Speedup |
|------------|--------|----------------|---------|
| Random Forest (100 trees) | 245ms | 4.8ms | 51x |
| XGBoost (1000 estimators) | 180ms | 6.2ms | 29x |
| PyTorch CNN (ResNet-50) | 89ms | 2.1ms | 42x |

Benchmarked on: Intel i9-12900K, NVIDIA RTX 4090, 32GB RAM

## Examples

### Batch Processing

```python
import numpy as np
from fast_inference import optimize, BatchPredictor

# Optimize model for batch inference
fast_model = optimize(model, batch_size=256)

# Process large dataset efficiently
X_large = np.random.randn(1_000_000, 10)
predictions = fast_model.predict(X_large)  # Automatically batched
```

### GPU Acceleration

```python
# Enable GPU acceleration
fast_model = optimize(model, device='cuda')

# Inference runs on GPU automatically
predictions = fast_model.predict(X_test)
```

### ONNX Export

```python
from fast_inference import export_onnx

# Export optimized model
export_onnx(fast_model, "model.onnx", input_shape=(None, 10))
```

## Documentation

- [Full Documentation](https://fast-inference.readthedocs.io)
- [API Reference](https://fast-inference.readthedocs.io/api)
- [Jupyter Notebook Examples](https://github.com/user/fast-inference/tree/main/examples)
- [Performance Benchmarks](https://fast-inference.readthedocs.io/benchmarks)

## Requirements

- Python 3.11+
- NumPy >= 1.24
- scikit-learn >= 1.3 (optional)
- PyTorch >= 2.0 (optional)
- CUDA 11.8+ (for GPU support)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Citation

If you use fast-inference in research, please cite:

```bibtex
@software{fast_inference,
  title = {fast-inference: High-Performance ML Inference},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/user/fast-inference}
}
```
```

**Result**: Data science-focused README with performance metrics, multiple examples, clear feature highlights, and academic citation format.

---

## Example 5: Testing README Before Publication

**Scenario**: You want to ensure your README renders perfectly before publishing to PyPI for the first time.

**Complete Validation Workflow**:

```
@pypi-readme-creator

Walk me through the complete validation workflow for my package "api-toolkit".
I want to test locally, on TestPyPI, then publish to production PyPI.

Current state:
- README.md is complete
- pyproject.toml has readme = "README.md"
- Package is ready to build
```

**Step-by-Step Guide**:

**1. Local Validation**:

```bash
# Preview Markdown as GitHub renders it
uvx grip README.md
# Opens browser at http://localhost:6419 - verify rendering

# Alternative: Convert to HTML for offline viewing
uv run --with markdown markdown README.md > preview.html
xdg-open preview.html  # Linux
open preview.html      # macOS
```

**2. Build Package**:

```bash
# Clean previous builds
rm -rf dist/

# Build with uv
uv build

# Verify outputs
ls -lh dist/
# Should show:
# api_toolkit-1.0.0-py3-none-any.whl
# api_toolkit-1.0.0.tar.gz
```

**3. Validate with Twine**:

```bash
# Check README will render on PyPI
uv run --with twine twine check dist/*

# Expected output:
# Checking dist/api_toolkit-1.0.0-py3-none-any.whl: Passed
# Checking dist/api_toolkit-1.0.0.tar.gz: Passed
```

**4. Test on TestPyPI**:

```bash
# Upload to TestPyPI (requires account and token)
uv run --with twine twine upload --repository testpypi dist/*

# Visit TestPyPI page
# https://test.pypi.org/project/api-toolkit/

# Verify:
# - README renders correctly
# - All sections display properly
# - Links work (some may break on TestPyPI, that's normal)
# - Code blocks have syntax highlighting
# - Badges display
```

**5. Test Installation from TestPyPI**:

```bash
# Create clean environment
uv venv test-env
source test-env/bin/activate  # Linux/macOS
# or: test-env\Scripts\activate  # Windows

# Install from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ api-toolkit

# Test basic functionality
python -c "import api_toolkit; print(api_toolkit.__version__)"

# Deactivate and clean up
deactivate
rm -rf test-env
```

**6. Publish to Production PyPI**:

```bash
# If everything looks good on TestPyPI
uv run --with twine twine upload dist/*

# Visit production PyPI page
# https://pypi.org/project/api-toolkit/

# Verify final rendering
```

**7. Post-Publication Checks**:

```bash
# Install from production PyPI
uv pip install api-toolkit

# Verify installation
python -c "import api_toolkit; print(api_toolkit.__version__)"

# Check PyPI page for:
# - README displays correctly
# - Project links work
# - Classifiers show properly
# - Version matches
```

**Result**: Complete confidence that README renders correctly before permanent publication to PyPI.

---

## Example 6: Choosing Between Markdown and RST

**Scenario**: You're starting a new Python project and unsure which README format to use.

**Invocation**:

```
@pypi-readme-creator

Help me decide between README.md and README.rst for my new project.

Project context:
- Web API client library
- Will have Sphinx documentation on Read the Docs
- Team familiar with both formats
- Need tables for endpoint reference
- Want good GitHub and PyPI rendering
```

**Analysis and Recommendation**:

**Markdown Advantages for Your Project**:

1. **GitHub Integration** - Better default rendering, task lists, alerts
2. **Team Familiarity** - More developers know Markdown than RST
3. **Simpler Syntax** - Easier to write and maintain
4. **Table Support** - GFM tables are simpler than RST tables
5. **Tooling** - Better editor support and preview tools

**Markdown Disadvantages**:

1. **Sphinx Separation** - Can't reuse Sphinx content directly (but sphinx-readme helps)
2. **Advanced Features** - RST has more directive types

**reStructuredText Advantages**:

1. **Sphinx Native** - Can use sphinx-readme to generate from docs
2. **Advanced Tables** - More table formatting options
3. **Directives** - More structured content capabilities

**reStructuredText Disadvantages**:

1. **Steeper Learning Curve** - More complex syntax
2. **Preview Tools** - Fewer good preview options
3. **PyPI Limitations** - Can't use Sphinx extensions anyway

**Recommendation for Your Project**:

**Use Markdown (README.md)** because:

```markdown
✓ Your team is comfortable with both → choose simpler
✓ GitHub-first workflow → Markdown renders better
✓ Table needs → GFM tables are cleaner
✓ Sphinx docs separate → Use sphinx-readme if needed later
```

**Implementation**:

```toml
# pyproject.toml
[project]
readme = "README.md"
```

```markdown
# api-client

Python client for the Example API.

## Installation

```bash
pip install api-client
```

## Quick Start

```python
from api_client import Client

client = Client(api_key="your-key")
response = client.users.list()
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user details |

## Documentation

Full documentation: https://api-client.readthedocs.io
```

**Result**: Clear decision framework based on project needs, with concrete recommendation and implementation.

---

## Summary

These examples demonstrate:

1. **README Generation** - Creating from scratch for various package types
2. **Format Conversion** - Working with Markdown and reStructuredText
3. **Error Resolution** - Fixing PyPI validation failures
4. **Sphinx Integration** - Leveraging existing documentation
5. **Validation Workflow** - Testing before publication
6. **Format Selection** - Choosing the right format for your project

For more information, see the main [README.md](../README.md) and skill reference files in the `skills/pypi-readme-creator/references/` directory.
