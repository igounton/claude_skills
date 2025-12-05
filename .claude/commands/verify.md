---
description: Run a rigorous self-assessment checklist before marking any task as complete.
---

STOP. You are NOT done yet. You must generate the following checklist and provide EVIDENCE for every item.

### 1. TASK TYPE & STRATEGY

- [ ] **Type:** FIX / FEATURE / REFACTOR / DOCS / INVESTIGATION
- [ ] **Strategy:** Executable verification vs. Static verification?

### 2. THE "WORKS" CHECK (Choose A or B)

**A. FOR CODE (Executable):**

- [ ] **Execution:** Terminal output showing successful run? (Exit code 0 is NOT enough).
- [ ] **Regression:** Evidence that existing tests still pass?
- [ ] **Edge Cases:** Evidence of testing failure scenarios?

**B. FOR STATIC ASSETS (Docs, Configs, Analysis):**

- [ ] **Accuracy:** Verified against source code/schema?
- [ ] **Clarity:** Does it follow the established format?
- [ ] **Validity:** Do links/references resolve?

### 3. THE "FIXED" CHECK

- [ ] **Reproduction:** Did I observe the pre-fix state?
- [ ] **Resolution:** Does the original problem NO LONGER occur?

### 4. QUALITY GATES

- [ ] Pre-commit hooks passed?
- [ ] Linting passed? (Necessary, but not sufficient).

### 5. HONESTY CHECK

- [ ] Did I verify the _full scope_?
- [ ] Am I distinguishing between "should work" and "verified to work"?
- [ ] Can I answer YES to: "I have VALIDATED this output in its intended context"?

**THE GOLDEN RULE:** If you cannot demonstrate it working in practice with evidence, it is NOT done.
