#!/usr/bin/env node
/**
 * SessionStart hook that injects RT-IAC checkpoint reminder into context.
 * Cross-platform (works on Windows, macOS, Linux).
 */

const output = {
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: `<rt-iac-checkpoint>
RT-IAC CHECKPOINT REQUIRED: Before creating plans, delegating to agents, or defining acceptance criteria for any spec, PRD, ticket, RFC, or multi-step engineering task, invoke the rt-iac skill to perform Reverse Thinking - Information Completeness Assessment. Block planning until prerequisites are verified.
</rt-iac-checkpoint>`
  }
};

console.log(JSON.stringify(output));
