---
description: Detects hallucinations, timeline fabrications, and unverified assumptions in agent output.
---

# Hallucination Audit

**Workflow Reference**: See [Master Workflow](./../knowledge/workflow-diagrams/master-workflow.md) for how this command fits into the verification stage of the agentic workflow.

Review the target content for these **HALLUCINATION TRIGGERS**:

### 1. Assumption Language (The "Guessing" Trigger)

_Scan for:_ "I think", "likely", "probably", "seems like", "should be", "assume". _Action:_ If found, FLAG as **Context Poisoning**. You must verify these with tools immediately.

### 2. Project Management Language (The "Human" Trigger)

_Scan for:_ "Week 1", "Sprint 2", "Phase 1 (Jan)", "Q1". _Exception:_ Technical timeouts or cache expirations (e.g., "Expires in 1h") are ALLOWED. _Action:_ **DELETE** scheduling language. Replace with **Priority Ordering** and **Dependencies**.

### 3. Pseudo-Quantification (The "Fake Rigor" Trigger)

_Scan for:_ "8.5/10", "70% improvement", "100% consensus". _Action:_ If no calculation methodology is shown, this is a hallucination. Request **Observable Evidence**.

### 4. Completeness Claims

_Scan for:_ "All files checked", "Comprehensive analysis". _Action:_ Verify the file count via `Glob`. If count mismatches, FLAG as **Incomplete Verification**.

### 5. Micromanagement (The "Trust" Trigger)

_Scan for:_ Specific line edits ("Change line 42") in a delegation prompt. _Action:_ FLAG as **Prescription**. Remove and replace with "Success Criteria" unless it is a strict User Constraint.

**OUTPUT:** Pass/Fail assessment. If Fail, list specific triggers found and the required correction.
