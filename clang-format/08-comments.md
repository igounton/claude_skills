# Comments & Miscellaneous Options

[← Prev: Languages](07-languages.md) | [Back to Index](index.md) | [Next: Advanced →](09-advanced.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Comment formatting and miscellaneous options.

## Comment Formatting

### ReflowComments

Reflow comment text to fit within ColumnLimit.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
// This is a very long comment that will be automatically
// reflowed to fit within the column limit when enabled
```

`false`:
```cpp
// This is a very long comment that will not be reflowed even if it exceeds column limit
```

### CommentPragmas

Regular expression for special comment pragmas.

**Type:** `String`
**Default:** `^\\s*IWYU pragma:`

Comments matching this regex will not be reflowed.

**Example:**

```yaml
CommentPragmas: '^ IWYU pragma:|^ NOLINT'
```

```cpp
// IWYU pragma: keep
// NOLINT - this comment won't be reflowed
```

### FixNamespaceComments

Add/fix end-of-namespace comments.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
namespace longNamespaceName {
void foo();
} // namespace longNamespaceName
```

Automatically adds `// namespace name` for long namespaces.

### CompactNamespaces

Put short namespaces on single line.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
namespace Foo { namespace Bar {
}}
```

`false`:
```cpp
namespace Foo {
namespace Bar {
}
}
```

## Macros

### AttributeMacros

List of macros that behave like attributes.

**Type:** `List of Strings`

**Example:**

```yaml
AttributeMacros:
  - __capability
  - __output
  - __unused
```

```cpp
__capability void* x;
```

### ForEachMacros

List of macros that behave like foreach loops.

**Type:** `List of Strings`

**Example:**

```yaml
ForEachMacros:
  - FOREACH
  - Q_FOREACH
  - BOOST_FOREACH
```

```cpp
FOREACH(item, list) {
  doSomething(item);
}
```

### IfMacros

List of macros that behave like if statements.

**Type:** `List of Strings`

**Example:**

```yaml
IfMacros:
  - IF
  - KJ_IF_MAYBE
```

### StatementAttributeLikeMacros

Macros that should be treated as statement attributes.

**Type:** `List of Strings`

### StatementMacros

Macros that should be treated as complete statements.

**Type:** `List of Strings`

**Example:**

```yaml
StatementMacros:
  - Q_UNUSED
  - QT_REQUIRE_VERSION
```

### TypenameMacros

Macros that introduce type names.

**Type:** `List of Strings`

**Example:**

```yaml
TypenameMacros:
  - STACK_OF
  - LIST
```

### WhitespaceSensitiveMacros

Macros where whitespace is significant.

**Type:** `List of Strings`

**Example:**

```yaml
WhitespaceSensitiveMacros:
  - STRINGIZE
  - PP_STRINGIZE
```

## Line Endings and Formatting Control

### DeriveLineEnding

Automatically detect line ending style.

**Type:** `Boolean`
**Default:** `true`

### UseCRLF

Use Windows-style line endings (CRLF).

**Type:** `Boolean`
**Default:** `false`

**Example:**

`true` - Use `\r\n` (Windows)
`false` - Use `\n` (Unix/Linux/Mac)

### DisableFormat

Completely disable formatting.

**Type:** `Boolean`

When `true`, clang-format won't modify the file at all.

### InsertNewlineAtEOF

Insert newline at end of file.

**Type:** `Boolean`

Ensures file ends with a newline character.

### KeepFormFeed

Keep form feed characters.

**Type:** `Boolean`

Preserves ASCII form feed characters (\\f) in source.

## Trailing Commas

### InsertTrailingCommas

Automatically insert trailing commas.

**Type:** `TrailingCommaStyle`
**Values:**
- `None` - Don't insert trailing commas
- `Wrapped` - Insert trailing commas in wrapped function calls

**Example:**

`Wrapped` (JavaScript):
```javascript
const x = {
  a: 1,
  b: 2,  // trailing comma added
};
```

### EnumTrailingComma

Insert trailing comma for enum values.

**Type:** `Boolean`

## Integer Literals

### IntegerLiteralSeparator

Configure digit separators in integer literals.

**Type:** `IntegerLiteralSeparatorStyle`
**Sub-options:**
- `Binary` - Separator for binary literals (0b)
- `BinaryMinDigits` - Minimum digits for binary
- `Decimal` - Separator for decimal
- `DecimalMinDigits` - Minimum digits for decimal
- `Hex` - Separator for hexadecimal
- `HexMinDigits` - Minimum digits for hex

**Example:**

```yaml
IntegerLiteralSeparator:
  Binary: 4
  Decimal: 3
  Hex: 2
```

```cpp
int a = 100'000'000;   // Decimal separator every 3 digits
int b = 0b1010'1010;   // Binary separator every 4 digits
int c = 0xDEAD'BEEF;   // Hex separator every 2 digits
```

## Empty Lines

### EmptyLineAfterAccessModifier

Add empty line after access modifiers.

**Type:** `EmptyLineAfterAccessModifierStyle`
**Values:**
- `Never`, `Leave`, `Always`

**Example:**

`Always`:
```cpp
class Foo {
private:

  int x;
public:

  void bar();
};
```

### EmptyLineBeforeAccessModifier

Add empty line before access modifiers.

**Type:** `EmptyLineBeforeAccessModifierStyle`
**Values:**
- `Never`, `Leave`, `Always`, `LogicalBlock`

**Example:**

`Always`:
```cpp
class Foo {
  int x;

private:
  int y;

public:
  void bar();
};
```

## Pointer and Reference Alignment

### PointerAlignment

Alignment of pointers and references.

**Type:** `PointerAlignmentStyle`
**Values:**
- `Left` - Align to left
- `Right` - Align to right
- `Middle` - Align to middle

**Examples:**

`Left`:
```cpp
int* a;
int& b;
```

`Right`:
```cpp
int *a;
int &b;
```

`Middle`:
```cpp
int * a;
int & b;
```

### DerivePointerAlignment

Derive pointer alignment from existing code.

**Type:** `Boolean`

When `true`, overrides `PointerAlignment` based on majority style in file.

### ReferenceAlignment

Separate alignment for references (overrides PointerAlignment for references).

**Type:** `ReferenceAlignmentStyle`
**Values:**
- `Pointer` - Same as pointers
- `Left`, `Right`, `Middle`

## Qualifier Alignment

### QualifierAlignment

Position of const/volatile qualifiers.

**Type:** `QualifierAlignmentStyle`
**Values:**
- `Leave` - Don't change
- `Left` - const int
- `Right` - int const
- `Custom` - Use QualifierOrder

**Example:**

`Left`:
```cpp
const int a;
const int* b;
```

`Right`:
```cpp
int const a;
int const* b;
```

### QualifierOrder

Custom qualifier order when `QualifierAlignment: Custom`.

**Type:** `List of Strings`

**Example:**

```yaml
QualifierAlignment: Custom
QualifierOrder:
  - inline
  - static
  - constexpr
  - const
  - volatile
  - type
```

## Common Patterns

### Namespace and Comment Handling

```yaml
FixNamespaceComments: true
CompactNamespaces: false
ReflowComments: true
CommentPragmas: '^ IWYU pragma:|^ NOLINT'
```

### Line Endings

```yaml
DeriveLineEnding: true
UseCRLF: false
InsertNewlineAtEOF: true
```

### Pointer Style (Left-Aligned)

```yaml
PointerAlignment: Left
ReferenceAlignment: Left
DerivePointerAlignment: false
```

### Pointer Style (Right-Aligned)

```yaml
PointerAlignment: Right
ReferenceAlignment: Right
DerivePointerAlignment: false
```

## Tips

1. **Comment Reflow**: Disable `ReflowComments` if you have carefully formatted comments
2. **Namespace Comments**: `FixNamespaceComments` helps navigate large codebases
3. **Macro Lists**: Maintain accurate macro lists for correct formatting
4. **Pointer Alignment**: Choose one style and enforce it with `DerivePointerAlignment: false`
5. **Line Endings**: Use `DeriveLineEnding: true` for mixed-platform teams
6. **Trailing Commas**: Useful in JavaScript/TypeScript for cleaner diffs
7. **Integer Separators**: Improves readability of large numeric literals

## See Also

- [Spacing](05-spacing.md) - Control whitespace
- [Languages](07-languages.md) - Language-specific options
- [Advanced](09-advanced.md) - Experimental features
- [Full Style Options Reference](reference/clang-format-style-options.md)

---

[← Prev: Languages](07-languages.md) | [Back to Index](index.md) | [Next: Advanced →](09-advanced.md)
