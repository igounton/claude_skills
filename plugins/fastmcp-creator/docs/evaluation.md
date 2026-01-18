# Evaluation Framework Guide

This guide covers the evaluation framework included with fastmcp-creator for testing MCP server effectiveness.

## Overview

The evaluation framework tests whether LLMs can effectively use your MCP server to answer realistic, complex questions. It automates the testing process and provides pass/fail metrics.

## Quick Start

### Installation

```bash
# Install evaluation dependencies
pip install -r skills/fastmcp-creator/scripts/requirements.txt
```

**Dependencies** (from requirements.txt):
- anthropic
- mcp

### Basic Usage

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_api_key

# Run evaluation against STDIO server
python skills/fastmcp-creator/scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_mcp_server.py \
  evaluation.xml
```

## Command-Line Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `-t, --transport` | Transport type: `stdio` or `http` | Yes | - |
| `-c, --command` | Command to run server (for stdio) | If stdio | - |
| `-a, --args` | Additional arguments for server | No | - |
| `-u, --url` | Server URL (for http) | If http | - |
| `evaluation_file` | Path to evaluation XML file | Yes | - |

## Evaluation File Format

Evaluations are defined in XML format:

```xml
<evaluation>
  <qa_pair>
    <question>What is the most popular repository in the kubernetes organization?</question>
    <answer>kubernetes</answer>
  </qa_pair>
  <qa_pair>
    <question>How many contributors does the prometheus/prometheus repository have?</question>
    <answer>425</answer>
  </qa_pair>
</evaluation>
```

## Creating Effective Evaluations

### Question Requirements

Each question must be:

1. **Independent** - Not dependent on other questions in the evaluation
2. **Read-only** - Only non-destructive operations required
3. **Complex** - Requiring multiple tool calls and deep exploration
4. **Realistic** - Based on real use cases humans would care about
5. **Verifiable** - Single, clear answer that can be verified by string comparison
6. **Stable** - Answer won't change over time

### Question Generation Process

1. **Tool Inspection** - List available tools and understand capabilities
   ```bash
   # Review your MCP server tools
   python -c "import my_server; print(my_server.mcp.list_tools())"
   ```

2. **Content Exploration** - Use READ-ONLY operations to explore available data
   ```bash
   # Manually test read-only tools
   python -c "import my_server; print(my_server.list_items(limit=5))"
   ```

3. **Question Generation** - Create 10 complex, realistic questions
   - Require multiple tool calls
   - Test different aspects of your server
   - Cover edge cases and complex queries

4. **Answer Verification** - Solve each question yourself to verify answers
   - Manually use your tools to find the answer
   - Document the answer in XML
   - Ensure the answer is stable and won't change

### Example Evaluation Scenarios

**GitHub MCP Server:**
```xml
<evaluation>
  <qa_pair>
    <question>Which repository in the microsoft organization has the most stars?</question>
    <answer>vscode</answer>
  </qa_pair>
  <qa_pair>
    <question>How many open issues are there in the facebook/react repository?</question>
    <answer>873</answer>
  </qa_pair>
</evaluation>
```

**Slack MCP Server:**
```xml
<evaluation>
  <qa_pair>
    <question>What is the description of the #general channel?</question>
    <answer>Company-wide announcements and work-based matters</answer>
  </qa_pair>
  <qa_pair>
    <question>How many messages were sent in #engineering-team today?</question>
    <answer>47</answer>
  </qa_pair>
</evaluation>
```

## Transport Types

### STDIO Transport

For servers that communicate via standard input/output:

```bash
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_mcp_server.py \
  evaluation.xml
```

**Parameters:**
- `-c, --command`: Interpreter or runtime (e.g., `python`, `node`, `uv run`)
- `-a, --args`: Server script path and any arguments

**Example Commands:**
```bash
# Python with direct invocation
-c python -a server.py

# Python with module invocation
-c python -a "-m my_package.server"

# Node.js TypeScript server
-c node -a "dist/server.js"

# Using uv for Python
-c "uv run" -a "python server.py"
```

### HTTP Transport

For servers running on HTTP:

```bash
# Start your server first
python my_mcp_server.py --port 8000 &

# Run evaluation
python scripts/evaluation.py \
  -t http \
  -u http://localhost:8000 \
  evaluation.xml
```

## Understanding Results

### Output Format

```
Running evaluation: evaluation.xml
Transport: stdio (python my_mcp_server.py)

Question 1/10: What is the most popular repository in the kubernetes organization?
Expected: kubernetes
Got: kubernetes
✓ PASS

Question 2/10: How many contributors does the prometheus/prometheus repository have?
Expected: 425
Got: 428
✗ FAIL (close but not exact match)

...

Results: 8/10 passed (80%)
```

### Pass Criteria

- Exact string match (case-sensitive by default)
- Whitespace is normalized
- Answer must be complete and accurate

### Failure Analysis

Common failure reasons:

1. **Tool Discovery Issues** - LLM didn't find the right tool
   - Fix: Improve tool descriptions
   - Fix: Use more specific tool names

2. **Parameter Errors** - LLM used wrong parameters
   - Fix: Add examples to tool descriptions
   - Fix: Use more descriptive parameter names
   - Fix: Add validation with clear error messages

3. **Context Window Limits** - Response too long to process
   - Fix: Implement pagination
   - Fix: Add "concise" response option
   - Fix: Reduce default data returned

4. **Complex Reasoning Required** - Question too difficult
   - Consider: Simplify question
   - Consider: Break into multiple tools
   - Fix: Provide intermediate results

## Advanced Usage

### Custom Evaluation Scripts

You can extend the evaluation framework:

```python
from scripts.evaluation import run_evaluation
from scripts.connections import StdioConnection, HttpConnection

# Custom connection
conn = StdioConnection(command="python", args=["server.py"])

# Run evaluation
results = run_evaluation(
    connection=conn,
    evaluation_file="custom_eval.xml",
    verbose=True
)

# Analyze results
for qa, passed in zip(results['questions'], results['passed']):
    if not passed:
        print(f"Failed: {qa['question']}")
```

### Batch Testing

Test multiple servers or configurations:

```bash
#!/bin/bash

servers=(
  "server_v1.py"
  "server_v2.py"
  "server_optimized.py"
)

for server in "${servers[@]}"; do
  echo "Testing $server"
  python scripts/evaluation.py \
    -t stdio \
    -c python \
    -a "$server" \
    evaluation.xml
done
```

### Continuous Integration

Add evaluations to your CI pipeline:

```yaml
# .github/workflows/test.yml
name: MCP Server Tests

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r scripts/requirements.txt
      - name: Run evaluation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/evaluation.py \
            -t stdio \
            -c python \
            -a server.py \
            evaluation.xml
```

## Troubleshooting

### Connection Errors

**Problem**: "Failed to connect to MCP server"

**Solutions:**
```bash
# Verify server runs standalone
python my_mcp_server.py

# Check for syntax errors
python -m py_compile my_mcp_server.py

# Test with timeout to see startup errors
timeout 5s python my_mcp_server.py
```

### Import Errors

**Problem**: "ModuleNotFoundError" when running evaluation

**Solutions:**
```bash
# Install evaluation dependencies
pip install -r scripts/requirements.txt

# Verify your server dependencies are installed
pip install -r requirements.txt

# Use absolute imports in your server
```

### API Key Issues

**Problem**: "Authentication failed"

**Solutions:**
```bash
# Set API key environment variable
export ANTHROPIC_API_KEY=your_api_key

# Verify key is set
echo $ANTHROPIC_API_KEY

# Use .env file (not recommended for production)
echo "ANTHROPIC_API_KEY=your_api_key" > .env
```

### Evaluation Hangs

**Problem**: Evaluation script hangs indefinitely

**Solutions:**
- Server might be waiting for input - ensure STDIO mode is configured
- Check server logs for errors
- Reduce question complexity
- Add timeout to evaluation script

### Incorrect Answers

**Problem**: LLM consistently gets wrong answer

**Solutions:**
1. Manually test the question yourself
2. Verify the expected answer is correct
3. Check if answer has changed (use stable data)
4. Improve tool descriptions
5. Add examples to tool documentation

## Best Practices

### Do's

✓ Create 10-15 questions covering different aspects
✓ Test both simple and complex queries
✓ Verify answers manually before running evaluation
✓ Use stable, unchanging data for expected answers
✓ Include edge cases in your questions
✓ Run evaluations before each release
✓ Update evaluations as you add new tools

### Don'ts

✗ Don't use questions with changing answers (current time, trending topics)
✗ Don't include destructive operations (delete, update)
✗ Don't make questions dependent on each other
✗ Don't use ambiguous questions with multiple valid answers
✗ Don't skip manual verification of expected answers
✗ Don't test only happy paths - include edge cases

## Example: Complete Workflow

Here's a complete workflow for creating and running evaluations:

```bash
# 1. Set up evaluation environment
pip install -r skills/fastmcp-creator/scripts/requirements.txt
export ANTHROPIC_API_KEY=your_api_key

# 2. Explore your server's capabilities
python -c "import my_server; my_server.mcp.list_tools()"

# 3. Manually test some queries
python -c "import my_server; print(my_server.search_items('test'))"

# 4. Create evaluation.xml with 10 questions
cat > evaluation.xml << 'EOF'
<evaluation>
  <qa_pair>
    <question>Your complex question here</question>
    <answer>Expected answer</answer>
  </qa_pair>
  <!-- Add 9 more questions -->
</evaluation>
EOF

# 5. Run evaluation
python skills/fastmcp-creator/scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_server.py \
  evaluation.xml

# 6. Analyze results and iterate
# - Update tool descriptions if LLM used wrong tools
# - Simplify questions if too complex
# - Fix bugs if answers are incorrect
# - Add pagination if responses too large

# 7. Re-run until 90%+ pass rate
python skills/fastmcp-creator/scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_server.py \
  evaluation.xml
```

## References

- Main README: [../README.md](../README.md)
- Evaluation Guide: [../skills/fastmcp-creator/references/evaluation-guide.md](../skills/fastmcp-creator/references/evaluation-guide.md)
- Example Evaluation: [../skills/fastmcp-creator/scripts/example_evaluation.xml](../skills/fastmcp-creator/scripts/example_evaluation.xml)
