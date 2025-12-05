---
name: is-it-done
description: Rigorous self-assessment to verify if a task is truly complete and working
---

# IS IT DONE? - Task Completion Verification Protocol

## STOP. Before claiming anything is "done", "fixed", or "working", answer these questions

### 1. TASK IDENTIFICATION

What type of task am I working on?

- [ ] **FIX**: Resolving a bug or broken functionality
- [ ] **FEATURE**: Adding new functionality
- [ ] **REFACTOR**: Restructuring existing code
- [ ] **DOCUMENTATION**: Creating or updating documentation
- [ ] **ENABLEMENT**: Adding tooling, CI/CD, or developer experience improvements
- [ ] **INVESTIGATION**: Research, debugging, or analysis

### 2. FUNDAMENTAL UNDERSTANDING CHECK

**Do I understand that exit code 0 means:**

- ✅ The command executed without throwing an uncaught exception
- ✅ The process terminated normally (not crashed, not killed)
- ❌ NOT that the program did what it was supposed to do
- ❌ NOT that the program achieved its functional goal
- ❌ NOT that the output is correct

**My definitions MUST be:**

- **"works"** = executes AND produces expected behavior when used in ALL functional scenarios
- **"fixed"** = original problem NO LONGER occurs when tested in realistic scenario
- **NOT** "passes linters" or "compiles without errors"

### 3. TASK-SPECIFIC VERIFICATION CHECKLISTS

#### IF FIXING A BUG

- [ ] Did I reproduce the original problem and observe the failure?
- [ ] Did I create an isolated test case that fails before my fix?
- [ ] After applying my fix, does that SAME test now pass?
- [ ] Did I test edge cases and error conditions?
- [ ] Did I verify the fix in the actual usage context, not just in isolation?
- [ ] Can I show evidence of: problem → fix → verification?

#### IF ADDING A FEATURE

- [ ] Did I test the feature in its intended use context?
- [ ] Did I verify ALL acceptance criteria are met?
- [ ] Did I test error handling and edge cases?
- [ ] Did I verify integration with existing functionality?
- [ ] Can I demonstrate the feature working end-to-end?
- [ ] Did I test with realistic data/scenarios, not just happy path?

#### IF REFACTORING

- [ ] Did I create tests proving original functionality BEFORE refactoring?
- [ ] Do those SAME tests still pass after refactoring?
- [ ] Did I verify performance hasn't degraded?
- [ ] Did I check all dependent code still functions?
- [ ] Can I prove behavior is identical before and after?

#### IF DOCUMENTATION

- [ ] Did I verify all code examples actually run?
- [ ] Did I test all commands/instructions work as written?
- [ ] Did I validate links and references are correct?
- [ ] Would someone following this documentation succeed?

#### IF ENABLEMENT/TOOLING

- [ ] Did I test the tool/pipeline in realistic conditions?
- [ ] Did I verify it handles both success AND failure cases?
- [ ] Did I test with real project data, not just test data?
- [ ] Does it provide useful output/feedback to users?
- [ ] Did I verify it integrates properly with existing workflows?

### 4. QUALITY GATES ASSESSMENT

**Have I verified against**

- [ ] Pre-commit hooks (if they exist)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Linting (syntax/style - necessary but NOT sufficient)
- [ ] Type checking (correctness - necessary but NOT sufficient)
- [ ] CI pipeline checks
- [ ] Manual testing in realistic scenarios

### 5. EVIDENCE COLLECTION

**What evidence can I provide that this ACTUALLY works?**

- [ ] Terminal output showing the problem reproducing
- [ ] Terminal output showing the problem fixed
- [ ] Test execution results (not just exit codes)
- [ ] Actual output/behavior demonstration
- [ ] Before/after comparisons
- [ ] Error handling verification

### 6. USER PERSPECTIVE CHECK

As an Engineer and Scientist, the user expects:

**Rigor**:

- [ ] Have I tested systematically, not randomly?
- [ ] Have I verified claims with evidence, not assumptions?

**Reproducibility**:

- [ ] Can the user reproduce my verification steps?
- [ ] Are my test scenarios clearly defined?

**Completeness**:

- [ ] Have I tested the full scope of changes?
- [ ] Have I considered unintended side effects?

**Honesty**:

- [ ] Am I being truthful about what I've actually tested?
- [ ] Am I distinguishing between "should work" and "verified to work"?

### 7. FINAL ASSESSMENT

**Can I honestly answer YES to ALL of these?**

- [ ] I have EXECUTED the code in its intended context
- [ ] I have OBSERVED the expected behavior
- [ ] I have TESTED failure scenarios
- [ ] I have VERIFIED no regressions
- [ ] I have EVIDENCE to support my claims
- [ ] I am NOT just assuming it works based on:
  - [ ] Exit code 0
  - [ ] Passing linters
  - [ ] Successful compilation
  - [ ] "It looks right"

## THE GOLDEN RULE

**If you cannot demonstrate it working in practice, it is NOT done.**

A pull request that "should work" but hasn't been tested is a LIABILITY, not an asset.

## RED FLAGS - If you find yourself saying

- "It passes all the linters" → NOT verification of functionality
- "It exits with code 0" → NOT proof it works
- "The code looks correct" → NOT evidence
- "It should work" → You haven't tested it
- "I've updated the code" → But have you verified the behavior?

## PROPER VERIFICATION WORKFLOW

1. **REPRODUCE** the issue/requirement
2. **IMPLEMENT** the solution
3. **VERIFY** with actual execution
4. **DOCUMENT** the evidence
5. **CONFIRM** no regressions
6. Only THEN claim it's "done"

---

**Remember**: The user trusts you to deliver working solutions, not syntactically correct code that might work. Build that trust through rigorous verification, not optimistic assumptions.
