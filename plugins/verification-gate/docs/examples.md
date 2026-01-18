# Usage Examples

This document provides concrete, real-world examples of using the verification-gate plugin to prevent common failure patterns.

---

## Example 1: Preventing Dependency System Misalignment

**Scenario:** You encounter a `ModuleNotFoundError` for a missing Python package and need to fix the dependency issue.

**User Request:**
```
"Fix the ModuleNotFoundError for pydantic in cli.py"
```

**Without Verification Gate (Failure Pattern):**

```
Error: ModuleNotFoundError: No module named 'pydantic'

Claude's Response:
"I see the issue - pydantic is not installed. Let me fix this."

Action: uv sync

Result: ✗ WRONG
- Script uses PEP 723 inline metadata (# /// script)
- uv sync operates on pyproject.toml
- Different dependency systems!
- Error persists, requires 15+ additional tool calls to debug
```

**With Verification Gate (Success Pattern):**

```
Error: ModuleNotFoundError: No module named 'pydantic'

Checkpoint 1 - Hypothesis Stated:
"Hypothesis: pydantic is missing from dependencies, but I need to determine
which dependency system this script uses before proceeding."

Checkpoint 2 - Gather Evidence:
Read(file_path="cli.py", limit=50)
→ Lines 1-3: Found # /// script block
→ Lines 4-8: dependencies = ["httpx", "typer"]
→ Evidence: Script uses PEP 723 inline metadata, NOT pyproject.toml

Refined Hypothesis: "PEP 723 script missing pydantic in # /// script block"

Checkpoint 3 - Alignment Check:
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: PEP 723 inline # /// script block   │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     PEP 723 inline # /// script block   │
│                    (add pydantic to dependencies list)  │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   ✓ ALIGNED - same system             │
└─────────────────────────────────────────────────────────┘

Checkpoint 4 - Pattern-Matching Check:
✓ Read cli.py to verify PEP 723 usage
✓ Confirmed # /// script block exists in THIS file
✓ Verified current dependencies list
✓ Action based on project reality, not pattern-matching

VERIFICATION COMPLETE - EXECUTING ACTION
Edit(file_path="cli.py", old_string="dependencies = [\"httpx\", \"typer\"]",
     new_string="dependencies = [\"httpx\", \"typer\", \"pydantic\"]")

Result: ✓ CORRECT - Issue resolved in 3 tool calls
```

**Key Lesson:** Checkpoint 3 prevents system misalignment by forcing explicit comparison between hypothesis and action systems.

---

## Example 2: Configuration Investigation Before Action

**Scenario:** Application not respecting a newly set timeout configuration.

**User Request:**
```
"The app isn't using the 30-second timeout I set in config.yaml. Fix it."
```

**Without Verification Gate (Failure Pattern):**

```
Claude's Response:
"Config files usually need proper YAML formatting. Let me check and fix the syntax."

Action: Edit config.yaml to fix indentation

Result: ✗ WRONG
- Application reads timeout from env var TIMEOUT_SECONDS
- Env var overrides config file
- Config file is syntactically correct
- Issue unresolved, requires investigation into actual config loading
```

**With Verification Gate (Success Pattern):**

```
Checkpoint 1 - Hypothesis Stated:
"Initial hypothesis: Application not reading config.yaml correctly.
Need to verify how timeout configuration is loaded."

Checkpoint 2 - Gather Evidence:
Grep(pattern="timeout", path="src/", output_mode="content")
→ config_loader.py:45: timeout = os.getenv('TIMEOUT_SECONDS', config.get('timeout', 10))
→ config_loader.py:72: logger.debug(f"Using timeout: {timeout} (source: {'env' if 'TIMEOUT_SECONDS' in os.environ else 'config'})")

Read(file_path="src/config_loader.py", offset=40, limit=20)
→ Evidence: Environment variable TIMEOUT_SECONDS takes precedence over config file

Bash: echo $TIMEOUT_SECONDS
→ Output: 10
→ Evidence: Env var is set to 10, overriding config.yaml value of 30

Refined Hypothesis: "Env var TIMEOUT_SECONDS=10 overrides config.yaml timeout=30"

Checkpoint 3 - Alignment Check:
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: Environment variable                │
│                    TIMEOUT_SECONDS                      │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     Environment variable                │
│                    (unset or update TIMEOUT_SECONDS)   │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   ✓ ALIGNED - same system             │
└─────────────────────────────────────────────────────────┘

Checkpoint 4 - Pattern-Matching Check:
✓ Grep'd source code to find actual config loading logic
✓ Read config_loader.py to verify precedence
✓ Executed Bash to check current env var value
✓ Action based on THIS project's implementation, not assumptions

VERIFICATION COMPLETE - EXECUTING ACTION
Bash: unset TIMEOUT_SECONDS

Result: ✓ CORRECT - App now reads 30s from config.yaml
```

**Key Lesson:** Checkpoint 2 forces evidence gathering before action, preventing assumptions about "how configs usually work."

---

## Example 3: Build Failure Investigation

**Scenario:** npm build fails with a module resolution error.

**User Request:**
```
"npm build is failing with 'Cannot find module'. Fix it."
```

**Without Verification Gate (Failure Pattern):**

```
Claude's Response:
"Module resolution errors usually mean dependencies aren't installed."

Action: npm install

Result: ✗ WRONG
- Dependencies were installed
- Issue is stale node_modules from previous major version upgrade
- Requires rm -rf node_modules && npm install
- Pattern-matching led to incomplete solution
```

**With Verification Gate (Success Pattern):**

```
Checkpoint 1 - BLOCKED:
Cannot state hypothesis without investigation.
Need to understand what's failing and why.

Investigation Phase:
Bash: npm build 2>&1 | head -20
→ Output: Error: Cannot resolve './components/NewFeature'
→ Evidence: Specific module can't be found

Read(file_path="src/components/NewFeature.tsx")
→ File exists, so not missing file

Bash: stat node_modules/.package-lock.json package-lock.json package.json --format="%n: %Y"
→ node_modules/.package-lock.json: 1704067200 (Jan 1 2024)
→ package-lock.json: 1736812800 (Jan 14 2025)
→ package.json: 1736812800 (Jan 14 2025)
→ Evidence: node_modules is from old install before lock file update

Checkpoint 1 - Hypothesis Stated:
"Hypothesis: node_modules is stale (from before package-lock.json update).
Module resolution fails because cached modules don't match current dependency graph."

Checkpoint 2 - Verified:
✓ Compared timestamps: node_modules older than lock file
✓ Build error shows resolution failure, not missing package
✓ NewFeature.tsx exists in source
✓ Evidence confirms stale cache hypothesis

Checkpoint 3 - Alignment Check:
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: node_modules cache                  │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     node_modules cache                  │
│                    (remove and reinstall)               │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   ✓ ALIGNED - same system             │
└─────────────────────────────────────────────────────────┘

Checkpoint 4 - Pattern-Matching Check:
✓ Investigated THIS project's specific error
✓ Checked timestamps to verify staleness
✓ Confirmed file exists but resolution fails
✓ Action targets verified root cause, not generic "npm install"

VERIFICATION COMPLETE - EXECUTING ACTION
Bash: rm -rf node_modules && npm install

Result: ✓ CORRECT - Build succeeds
```

**Key Lesson:** Checkpoint 1 blocks execution until specific hypothesis formed. Generic "dependency issues" isn't sufficient.

---

## Example 4: Docker Container Networking Issue

**Scenario:** Service in Docker container can't reach external API.

**User Request:**
```
"The API service in the container is getting connection timeouts. Fix the networking."
```

**Without Verification Gate (Failure Pattern):**

```
Claude's Response:
"Docker networking issues usually need bridge network configuration."

Action: docker network create custom-bridge && restart container

Result: ✗ WRONG
- Container is correctly on default bridge
- Issue is container firewall rules blocking egress
- Created unnecessary network
- Problem persists
```

**With Verification Gate (Success Pattern):**

```
Checkpoint 1 - Hypothesis Formation:
"Need to determine if issue is Docker network layer, container config, or host firewall."

Investigation:
Bash: docker inspect api-service | grep -A 10 "NetworkSettings"
→ Evidence: Container on default bridge, has IP address

Bash: docker exec api-service curl -v https://api.example.com
→ Error: Connection timeout after 5000ms
→ Evidence: Issue is from inside container

Bash: curl https://api.example.com
→ Success: Response 200 OK
→ Evidence: Host can reach API, container cannot

Read(file_path="docker-compose.yml")
→ Lines 45-50: Shows container has custom iptables rules

Bash: docker exec api-service iptables -L OUTPUT
→ Output: Chain OUTPUT (policy DROP)
→ Evidence: Container egress blocked by firewall policy

Checkpoint 1 - Hypothesis Stated:
"Hypothesis: Container has DROP policy on OUTPUT chain, blocking egress to external APIs"

Checkpoint 2 - Verified:
✓ docker inspect showed network config (not the issue)
✓ curl from host succeeded (host networking works)
✓ curl from container failed (container networking blocked)
✓ iptables showed DROP policy on OUTPUT
✓ Evidence confirms iptables hypothesis

Checkpoint 3 - Alignment Check:
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: Container iptables OUTPUT chain     │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     Container iptables OUTPUT chain     │
│                    (add ACCEPT rule for API)            │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   ✓ ALIGNED - same system             │
└─────────────────────────────────────────────────────────┘

Checkpoint 4 - Pattern-Matching Check:
✓ Tested network from both host and container
✓ Inspected actual container configuration
✓ Verified iptables rules in THIS container
✓ Not assuming "Docker networking usually needs..."

VERIFICATION COMPLETE - EXECUTING ACTION
Bash: docker exec api-service iptables -A OUTPUT -d api.example.com -j ACCEPT

Result: ✓ CORRECT - Container can now reach API
```

**Key Lesson:** Checkpoint 2 forces systematic investigation across different system layers before jumping to common solutions.

---

## Example 5: Python Script Execution Error

**Scenario:** Python script fails with import error despite package being installed.

**User Request:**
```
"Script fails with 'cannot import name XYZ from package'. Package is installed. Fix it."
```

**Without Verification Gate (Failure Pattern):**

```
Claude's Response:
"Import errors despite installation usually mean wrong Python environment."

Action: source venv/bin/activate && python script.py

Result: ✗ WRONG
- Script was already using correct venv
- Issue is trying to import renamed function (ABC → XYZ in v2.0)
- Package updated but script not updated
- Pattern-matching missed actual cause
```

**With Verification Gate (Success Pattern):**

```
Checkpoint 1 - Hypothesis Formation:
"Need to verify which Python environment, which package version, and what the import should be."

Investigation:
Bash: which python && python --version
→ /path/to/venv/bin/python 3.11.5
→ Evidence: Using venv, not system Python

Bash: python -c "import package; print(package.__version__)"
→ 2.1.0
→ Evidence: Package installed, version 2.1.0

Read(file_path="script.py", limit=20)
→ Line 5: from package import XYZ
→ Evidence: Script imports XYZ

mcp__Ref__ref_search_documentation(query="package v2.0 breaking changes migration")
→ Result: "v2.0: Renamed ABC to XYZ. v2.1: XYZ renamed back to ABC for compatibility"
→ Evidence: Function is ABC in v2.1, was XYZ only in v2.0

Checkpoint 1 - Hypothesis Stated:
"Hypothesis: Script uses import name from v2.0 (XYZ), but package v2.1 reverted to v1.x name (ABC)"

Checkpoint 2 - Verified:
✓ Confirmed correct venv in use
✓ Confirmed package v2.1 installed
✓ Read script to see import statement
✓ Checked docs for v2.1 API changes
✓ Evidence: Import name is wrong for current version

Checkpoint 3 - Alignment Check:
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: Python script import statement      │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     Python script import statement      │
│                    (change XYZ to ABC)                  │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   ✓ ALIGNED - same system             │
└─────────────────────────────────────────────────────────┘

Checkpoint 4 - Pattern-Matching Check:
✓ Verified Python env (not assuming wrong venv)
✓ Checked actual package version
✓ Read official docs for THIS version's API
✓ Not relying on "import errors usually mean..."

VERIFICATION COMPLETE - EXECUTING ACTION
Edit(file_path="script.py",
     old_string="from package import XYZ",
     new_string="from package import ABC")

Result: ✓ CORRECT - Script runs successfully
```

**Key Lesson:** Checkpoint 4 prevents jumping to "common causes" and forces verification against actual installed versions and documentation.

---

## Summary of Verification Benefits

| Without Verification Gate | With Verification Gate |
|---------------------------|------------------------|
| 15-30 tool calls to debug | 3-5 tool calls total |
| Multiple wrong hypotheses | Single correct hypothesis |
| Trial-and-error approach | Evidence-based approach |
| Pattern-matching errors | Project-reality verification |
| System misalignments | Enforced alignment check |
| 4000+ tokens wasted | 200-300 tokens for verification |

**ROI:** 5% verification cost → 95% error prevention

**Key Principle:** Verification gates implement defensive programming for LLM reasoning. Speed without verification is error propagation.

---

## Additional Resources

- [Skills Reference](./skills.md) - Detailed checkpoint documentation
- [Research Foundations](../skills/verification-gate/references/research-foundations.md) - Academic backing for verification approach
- [Failure Patterns](../skills/verification-gate/references/failure-patterns.md) - More real-world failure examples
- [README](../README.md) - Installation and setup
