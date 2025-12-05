---
description: Forces the Scientific Method for complex problem solving (Debugging, Architecture, Refactoring).
---

You are entering **Deep Reasoning Mode**. Trigger this only for: **Debugging**, **Architecture**, or **Complex Refactoring**. (Do not use for trivial tasks like typo fixes).

### 1. Observation

List ONLY factual observations (logs, errors, file contents). _No interpretations yet._

### 2. Hypothesis Formulation

- **$H_0$ (Null Hypothesis):** The system is working as intended; the error is environmental/configuration.
- **$H_A$ (Alternative Hypothesis):** The error is caused by [Specific Cause].

### 3. Prediction

"If $H_A$ is true, then observing [Component X] will reveal [Y]."

### 4. Experiment Plan (Tree-of-Thought)

Design a test to falsify $H_0$.

- Path A: Check [X]. Expected: [Y].
- Path B: Check [Z]. Expected: [Q].

### 5. Execution Control

- Are there confounding variables (caching, environment vars)?
- How will you isolate them?

**PROCEED:** Execute the Experiment Plan using available tools.
