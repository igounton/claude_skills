---
description: Forces the Scientific Delegation Framework (SKILL.md). Use when assigning work to a sub-agent.
---

Step 1: Analyze the task. Do you have the "WHERE, WHAT, WHY"? Step 2: Construct the prompt using the STRICT template below.

---

**TEMPLATE TO GENERATE:**

Your ROLE_TYPE is sub-agent.

[Task Identification]

OBSERVATIONS (Factual only):

- [Verbatim error messages]
- [Exact file:line references]
- [Environment state]
- [NO interpretations or "I think"]

DEFINITION OF SUCCESS (The "WHAT"):

- [Specific measurable outcome]
- [Acceptance criteria]
- [Verification method]

CONTEXT (The "WHERE" & "WHY"):

- Location: [Where to look]
- Scope: [Boundaries]
- Constraints: [Hard requirements vs Preferences]

AVAILABLE RESOURCES:

- [List available MCP tools]
- [Reference docs with @filepath]

YOUR TASK:

1. Run `/verify` (as completion criteria guide).
2. Perform comprehensive context gathering.
3. Form hypothesis -> Experiment -> Verify.
4. Implement solution.
5. Only report completion after `/verify` criteria are met.

---

**DELEGATION RULES (CHECK BEFORE SENDING):**

1. **Formula:** Delegation = Observations + Success Criteria + Resources - Assumptions - Micromanagement.
2. **Micromanagement vs Constraints:** - **Forbidden:** Telling the agent _how_ to implement a fix (e.g., "Change line 42 to X").
   - **Allowed:** Telling the agent _constraints_ (e.g., "Must use the 'requests' library").
3. **No Assumptions:** Do NOT say "The issue is probably..."
4. **Scope:** If a code smell is found, instruct agent to audit the _entire pattern_, not just the single instance.
