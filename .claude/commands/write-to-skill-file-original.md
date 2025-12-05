---
allowed-tools: *
argument-hint: "provide the full text to be processed, or a list of files to be processed."
description: "Text to LLM Optimized Text workflow instructions"
disable-model-invocation: false
---

You are tasked with rewriting a provided text to be optimized for LLM consumption. Your goal is to transform the input into a concise, technical instructions, reference material, and rules suitable for use by an LLM or an AI with comprehensive knowledge. The audience AI model that consumes the content you create has expert-level comprehension of all technical concepts. Assume complete familiarity with domain internals.

Here is the text to be transformed between the xml <text> tokens:

<text>
{{TEXT}}
</text>

When transforming text into RULES, CONDITIONS, and CONSTRAINTS, follow these best practices:

- Good rules are focused, imperative, actionable, and scoped.
- Keep rules concise. Under 500 lines is a good target
- Split significant concepts into multiple, composable rules
- Provide concrete examples or referenced files when helpful
- Avoid vague guidance. Write rules the way you would write a clear internal doc
- Use declarative phrasing ("The model must") for all instructions.
- Produce deterministic, flat ASCII text without using markdown for **bold** or **italic** or stylistic formatting. Headings to show hierarchy, and lists are welcome.
- Include explicit sections for identity, intent, task rules, issue handling, triggers, Table of Contents, and References.
- Preserve or expand structured examples found in the source text.

When the provided or parsed text involves multiple components — such as context, instructions, and examples — XML tags can be a game-changer. They help the LLM parse your prompts and instructions more accurately, leading to higher-quality outputs.

<Tip>**XML tip**: Use tags like `<instructions>`, `<example>`, and `<formatting>` to clearly separate different parts of your prompt. This prevents Claude from mixing up instructions with examples or context.</Tip>

## Why use XML tags?

- **Clarity:** Clearly separate different parts of your prompt and ensure your prompt is well structured.
- **Accuracy:** Reduce errors caused by Claude misinterpreting parts of your prompt.
- **Flexibility:** Easily find, add, remove, or modify parts of your prompt without rewriting everything.
- **Parseability:** Having Claude use XML tags in its output makes it easier to extract specific parts of its response by post-processing. Follow these rules when rewriting the text:

0. The first instruction should be a directive on how to read and apply the rules.
1. Maximize information density using technical jargon, dense long words, equations, and industry-specific terms.
2. Rephrase for accuracy and specificity.
3. Write as if addressing an expert, scientific, or academic audience.
4. Use only visible ASCII characters.
5. Write as lookup references for the AI consumer itself, which possesses comprehensive technical knowledge. Optimize as decision triggers and pattern-matching rules for an AI that already knows all technical details, not educational content.
6. Omit greetings, unnecessary text, and markdown formatting.
7. Keep the original text's description of how it would like its output structured if it is observed.

Optimizations: Use a precise, deterministic ACTION TRIGGER OUTCOME format in descriptions Include only essential tags that directly impact rule application Set clear priority levels between rules and instructions to resolve conflicts efficiently Provide concise positive and negative examples of rule application in practice Optimize for AI context window efficiency Remove any non-essential or redundant information Use standard glob patterns without quotes (e.g., .js,src/\*\*/.{ts,js}) Keep frontmatter descriptions full of TRIGGER's for when the rules or instructions should be used, thus maintaining clear intent for rule selection by the AI Agent Limit examples to essential patterns only.

Output: Format your output as one or more \*.md files as follows , the content between <file_content> xml tags is what would go into the file. Create your files following this naming: all-lower-case-with-hyphens.md <file_content>

---

name: [name of the skill if the file is SKILL.md or name of the file] description: The model must use this SKILL when: ACTION when TRIGGER to OUTCOME. <as many examples as fit in 600 characters> version: "1.0.0" last_updated: "<date and time>" [<metadata-key>:<any relevant metadata>] # Optional, but good for ambiguous topics to help add clarity and nuance

---

[Rewritten text goes here] </file_content>

## Example frontmatter of a SKILL.md file

name: python3-development description: 'The model must use this skill when : 1. working within any python project. 2. Python CLI applications with Typer and Rich are mentioned by the user. 2. tasked with Python script writing or editing. 3. building CI scripts or tools. 4. Creating portable Python scripts with stdlib only. 5. planning out a python package design. 6. running any python script or test. 7. writing tests (unit, integration, e2e, validation) for a python script, package, or application. Reviewing Python code against best practices or for code smells. 8. The python command fails to run or errors, or the python3 command shows errors. 9. pre-commit or linting errors occur in python files. 10. Writing or editing python code in a git repository.\n<hint>This skill provides : 1. the users preferred workflow patterns for test-driven development, feature addition, refactoring, debugging, and code review using modern Python 3.11+ patterns (including PEP 723 inline metadata, native generics, and type-safe async processing). 2. References to favored modules. 3. Working pyproject.toml configurations. 4. Linting and formatting configuration and troubleshooting. 5. Resource files that provide solutions to known errors and linting issues. 6. Project layouts the user prefers.</hint>' version: "1.1.0" last_updated: "2025-11-04" python_compatibility: "3.11+"

---
