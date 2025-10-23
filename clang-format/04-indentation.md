# Indentation Options

[← Prev: Braces](03-braces.md) | [Back to Index](index.md) | [Next: Spacing →](05-spacing.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Control indentation behavior for various code constructs.

## Basic Indentation

### IndentWidth

Number of columns for each indentation level.

**Type:** `Unsigned`
**Default:** `2`

```yaml
IndentWidth: 4
```

**Example:**
```cpp
void function() {
    if (condition) {
        doSomething();
    }
}
```

### UseTab

Tab usage policy.

**Type:** `UseTabStyle`
**Values:**
- `Never` - Never use tabs
- `ForIndentation` - Use tabs for indentation, spaces for alignment
- `ForContinuationAndIndentation` - Use tabs for line continuation and indentation
- `AlignWithSpaces` - Use tabs for indentation, spaces for alignment (deprecated, use `ForIndentation`)
- `Always` - Use tabs for indentation and alignment

**Examples:**

`Never`:
```cpp
void f() {
••••int i;
}
```

`ForIndentation`:
```cpp
void f() {
→   int i;
}
```

`Always`:
```cpp
void f() {
→   int i;
}
```

### TabWidth

Visual width of a tab character.

**Type:** `Unsigned`
**Default:** `8`

```yaml
TabWidth: 4
```

Affects how existing tabs are displayed and formatted.

### ContinuationIndentWidth

Indent for line continuations.

**Type:** `Unsigned`
**Default:** `4`

```yaml
ContinuationIndentWidth: 4
```

**Example:**
```cpp
int var = function1() +
    function2();

result = longFunction(
    parameter1,
    parameter2);
```

## Access Modifiers

### AccessModifierOffset

Offset for access modifiers (public, private, protected).

**Type:** `Integer`
**Default:** `0`

Negative values indent left, positive values indent right.

**Examples:**

`AccessModifierOffset: -2`:
```cpp
class C {
public:
  void f();
};
```

`AccessModifierOffset: 0`:
```cpp
class C {
  public:
  void f();
};
```

`AccessModifierOffset: 2`:
```cpp
class C {
    public:
  void f();
};
```

### IndentAccessModifiers

Indent access modifiers

.

**Type:** `Boolean`
**Default:** `false`

**Example:**

`true`:
```cpp
class C {
    public:
        void f();
};
```

`false`:
```cpp
class C {
  public:
    void f();
};
```

## Case Labels and Switch

### IndentCaseLabels

Indent case labels from switch statement.

**Type:** `Boolean`
**Default:** `false`

**Examples:**

`false`:
```cpp
switch (fool) {
case 1:
  bar();
  break;
default:
  plop();
}
```

`true`:
```cpp
switch (fool) {
  case 1:
    bar();
    break;
  default:
    plop();
}
```

### IndentCaseBlocks

Indent case blocks.

**Type:** `Boolean`
**Default:** `false`

**Examples:**

`false`:
```cpp
switch (fool) {
case 1: {
  bar();
} break;
default: {
  plop();
}
}
```

`true`:
```cpp
switch (fool) {
case 1:
  {
    bar();
  }
  break;
default:
  {
    plop();
  }
}
```

## Preprocessor Directives

### IndentPPDirectives

Indent preprocessor directives.

**Type:** `PPDirectiveIndentStyle`
**Values:**
- `None` - Don't indent directives
- `AfterHash` - Indent after the hash
- `BeforeHash` - Indent before the hash

**Examples:**

`None`:
```cpp
#if FOO
#if BAR
#include <foo>
#endif
#endif
```

`AfterHash`:
```cpp
#if FOO
#  if BAR
#    include <foo>
#  endif
#endif
```

`BeforeHash`:
```cpp
#if FOO
  #if BAR
    #include <foo>
  #endif
#endif
```

## Special Constructs

### IndentGotoLabels

Indent goto labels.

**Type:** `Boolean`
**Default:** `true`

**Examples:**

`true`:
```cpp
int f() {
  if (foo()) {
  label1:
    bar();
  }
label2:
  return 1;
}
```

`false`:
```cpp
int f() {
  if (foo()) {
label1:
    bar();
  }
label2:
  return 1;
}
```

### IndentExternBlock

Indent extern blocks.

**Type:** `IndentExternBlockStyle`
**Values:**
- `AfterExternBlock` - Indent after extern
- `NoIndent` - Don't indent
- `Indent` - Indent extern block

**Examples:**

`AfterExternBlock`:
```cpp
extern "C" {
void f();
}

extern "C"
{
void g();
}
```

`NoIndent`:
```cpp
extern "C" {
void f();
}
```

`Indent`:
```cpp
extern "C" {
  void f();
}
```

### IndentRequiresClause

Indent C++20 requires clause.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
template <typename It>
  requires Iterator<It>
void sort(It begin, It end) {}
```

`false`:
```cpp
template <typename It>
requires Iterator<It>
void sort(It begin, It end) {}
```

### IndentWrappedFunctionNames

Indent wrapped function names after line break.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
LoooooooooooooooooooooooooooooongReturnType
    LoooooooooooooooooooongFunctionDeclaration();
```

`false`:
```cpp
LoooooooooooooooooooooooooooooongReturnType
LoooooooooooooooooooongFunctionDeclaration();
```

### ConstructorInitializerIndentWidth

Indent width for constructor initializers.

**Type:** `Unsigned`
**Default:** Uses `IndentWidth`

**Example:**

`ConstructorInitializerIndentWidth: 2`:
```cpp
Constructor()
  : member1(),
    member2() {}
```

## Language-Specific

### IndentExportBlock

Indent export blocks (JavaScript).

**Type:** `Boolean`

**Example:**

`true`:
```javascript
export {
  foo,
  bar
};
```

`false`:
```javascript
export {
foo,
bar
};
```

## Common Patterns

### Minimal Indentation (2 spaces)

```yaml
IndentWidth: 2
UseTab: Never
ContinuationIndentWidth: 2
AccessModifierOffset: -2
IndentCaseLabels: false
IndentCaseBlocks: false
IndentGotoLabels: true
IndentPPDirectives: None
IndentWrappedFunctionNames: false
```

### Standard Indentation (4 spaces)

```yaml
IndentWidth: 4
UseTab: Never
TabWidth: 4
ContinuationIndentWidth: 4
AccessModifierOffset: 0
IndentAccessModifiers: false
IndentCaseLabels: true
IndentCaseBlocks: false
IndentGotoLabels: true
IndentPPDirectives: AfterHash
IndentWrappedFunctionNames: true
```

### Tab-Based Indentation

```yaml
IndentWidth: 4
UseTab: ForIndentation
TabWidth: 4
ContinuationIndentWidth: 4
AccessModifierOffset: -4
IndentCaseLabels: true
IndentPPDirectives: AfterHash
```

### Large Indentation (8 spaces, Linux style)

```yaml
IndentWidth: 8
UseTab: Always
TabWidth: 8
ContinuationIndentWidth: 8
AccessModifierOffset: -8
IndentCaseLabels: false
IndentGotoLabels: false
IndentPPDirectives: None
```

## Tips

1. **Consistency**: Use the same indentation throughout your project
2. **Tab Width**: If using tabs, ensure `TabWidth` matches team editor settings
3. **Continuation**: Set `ContinuationIndentWidth` to help distinguish continuations from blocks
4. **Access Modifiers**: Negative `AccessModifierOffset` creates outdent effect
5. **Preprocessor**: Be careful with `IndentPPDirectives` in complex macro code
6. **Mixed Tabs/Spaces**: Avoid mixing; use `Never` or `ForIndentation` for consistent results

## See Also

- [Alignment](01-alignment.md) - Align code elements
- [Spacing](05-spacing.md) - Control whitespace
- [Braces](03-braces.md) - Configure brace placement
- [Full Style Options Reference](reference/clang-format-style-options.md)

---

[← Prev: Braces](03-braces.md) | [Back to Index](index.md) | [Next: Spacing →](05-spacing.md)
