# Spacing Options

[← Prev: Indentation](04-indentation.md) | [Back to Index](index.md) | [Next: Includes →](06-includes.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Fine-tune whitespace placement throughout your code.

## Parentheses and Brackets

### SpaceBeforeParens

Add space before opening parentheses.

**Type:** `SpaceBeforeParensStyle`
**Values:**
- `Never` - Never add space
- `ControlStatements` - Only before control statement parens
- `ControlStatementsExceptControlMacros` - Control statements except macros
- `NonEmptyParentheses` - Only if parentheses aren't empty
- `Always` - Always add space
- `Custom` - Use `SpaceBeforeParensOptions`

**Examples:**

`Never`:
```cpp
void f() {
  if(true) {
    f();
  }
}
```

`ControlStatements`:
```cpp
void f() {
  if (true) {
    f();
  }
}
```

`Always`:
```cpp
void f () {
  if (true) {
    f ();
  }
}
```

### SpaceBeforeParensOptions

Fine-grained control when `SpaceBeforeParens: Custom`.

**Sub-options:**
- `AfterControlStatements` (bool)
- `AfterForeachMacros` (bool)
- `AfterFunctionDeclarationName` (bool)
- `AfterFunctionDefinitionName` (bool)
- `AfterIfMacros` (bool)
- `AfterOverloadedOperator` (bool)
- `AfterRequiresInClause` (bool)
- `AfterRequiresInExpression` (bool)
- `BeforeNonEmptyParentheses` (bool)

### SpacesInParentheses

Add spaces inside parentheses.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
t f( Deleted & ) & = delete;
```

`false`:
```cpp
t f(Deleted &) & = delete;
```

### SpacesInSquareBrackets

Add spaces inside square brackets.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
int a[ 5 ];
```

`false`:
```cpp
int a[5];
```

### SpacesInAngles

Add spaces inside angle brackets.

**Type:** `SpacesInAnglesStyle`
**Values:**
- `Never`, `Always`, `Leave`

**Example:**

`Always`:
```cpp
static_cast< int >(arg);
std::vector< int > vec;
```

## Operators and Assignments

### SpaceBeforeAssignmentOperators

Add space before assignment operators.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
int a = 5;
a += 42;
```

`false`:
```cpp
int a= 5;
a+= 42;
```

### SpaceBeforeRangeBasedForLoopColon

Add space before colon in range-based for loop.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
for (auto v : values) {}
```

`false`:
```cpp
for (auto v: values) {}
```

### SpaceInEmptyBlock

Add space in empty blocks.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
void f() { }
while (true) { }
```

`false`:
```cpp
void f() {}
while (true) {}
```

## Casts and Templates

### SpaceAfterCStyleCast

Add space after C-style cast.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
(int) i;
```

`false`:
```cpp
(int)i;
```

### SpaceAfterLogicalNot

Add space after logical not operator (!).

**Type:** `Boolean`

**Example:**

`true`:
```cpp
! someExpression();
```

`false`:
```cpp
!someExpression();
```

### SpaceAfterTemplateKeyword

Add space after template keyword.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
template <int> void foo();
```

`false`:
```cpp
template<int> void foo();
```

### SpaceBeforeCaseColon

Add space before case colon.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
switch (x) {
  case 1 : break;
}
```

`false`:
```cpp
switch (x) {
  case 1: break;
}
```

### SpaceBeforeCpp11BracedList

Add space before C++11 braced list.

**Type:** `Boolean`

**Example:**

`true`:
```cpp
Foo foo { bar };
Foo {};
vector<int> { 1, 2, 3 };
new int[3] { 1, 2, 3 };
```

`false`:
```cpp
Foo foo{ bar };
Foo{};
vector<int>{ 1, 2, 3 };
new int[3]{ 1, 2, 3 };
```

### SpaceBeforeCtorInitializerColon

Add space before constructor initializer colon.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
Foo::Foo() : a(a) {}
```

`false`:
```cpp
Foo::Foo(): a(a) {}
```

### SpaceBeforeInheritanceColon

Add space before inheritance colon.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`true`:
```cpp
class Foo : Bar {}
```

`false`:
```cpp
class Foo: Bar {}
```

## Containers and Comments

### SpacesBeforeTrailingComments

Number of spaces before trailing comments.

**Type:** `Unsigned`
**Default:** `1`

**Example:**

`2`:
```cpp
void f() {
  if (true) {
    f();  // comment
  }       // comment
}
```

### SpacesInContainerLiterals

Add spaces in container literals.

**Type:** `Boolean`

**Example:**

`true` (JavaScript/JSON):
```javascript
var arr = [ 1, 2, 3 ];
obj = { a : 1, b : 2, c : 3 };
```

`false`:
```javascript
var arr = [1, 2, 3];
obj = {a: 1, b: 2, c: 3};
```

### SpacesInLineCommentPrefix

Spaces in line comment prefix.

**Type:** `SpacesInLineComment`
**Sub-options:**
- `Minimum` - Minimum spaces
- `Maximum` - Maximum spaces

**Example:**

`Minimum: 1, Maximum: -1` (no max):
```cpp
//A comment
// A comment
//  A comment
```

### SpaceAroundPointerQualifiers

Configure spaces around pointer qualifiers.

**Type:** `SpaceAroundPointerQualifiersStyle`
**Values:**
- `Default`, `Before`, `After`, `Both`

**Examples:**

`Default`:
```cpp
void* const* x = NULL;
```

`Before`:
```cpp
void *const *x = NULL;
```

`After`:
```cpp
void* const* x = NULL;
```

`Both`:
```cpp
void * const * x = NULL;
```

## Bit Fields

### BitFieldColonSpacing

Spacing around bit field colon.

**Type:** `BitFieldColonSpacingStyle`
**Values:**
- `Both` - Add spaces on both sides
- `None` - No spaces
- `Before` - Space before only
- `After` - Space after only

**Examples:**

`Both`:
```cpp
unsigned bf : 2;
```

`None`:
```cpp
unsigned bf:2;
```

`Before`:
```cpp
unsigned bf :2;
```

`After`:
```cpp
unsigned bf: 2;
```

## Empty Lines

### MaxEmptyLinesToKeep

Maximum consecutive empty lines to keep.

**Type:** `Unsigned`
**Default:** `1`

**Example:**

`1`:
```cpp
int f() {
  int = 1;

  return i;
}
```

`2`:
```cpp
int f() {
  int i = 1;


  return i;
}
```

### KeepEmptyLinesAtTheStartOfBlocks

Keep empty lines at start of blocks.

**Type:** `Boolean`
**Default:** `true`

**Example:**

`false`:
```cpp
void f() {
  foo();
}
```

`true`:
```cpp
void f() {

  foo();
}
```

### KeepEmptyLinesAtEOF

Keep empty lines at end of file.

**Type:** `Boolean`

## Common Patterns

### Minimal Spacing (Compact)

```yaml
SpaceBeforeParens: Never
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBlock: false
SpacesInParentheses: false
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: false
SpaceAfterLogicalNot: false
SpacesBeforeTrailingComments: 1
MaxEmptyLinesToKeep: 1
```

### Standard Spacing

```yaml
SpaceBeforeParens: ControlStatements
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBlock: false
SpacesInParentheses: false
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: false
SpaceAfterLogicalNot: false
SpaceAfterTemplateKeyword: true
SpaceBeforeCpp11BracedList: false
SpacesBeforeTrailingComments: 2
MaxEmptyLinesToKeep: 1
KeepEmptyLinesAtTheStartOfBlocks: false
```

### Generous Spacing (Readable)

```yaml
SpaceBeforeParens: ControlStatements
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBlock: true
SpacesInParentheses: false
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: true
SpaceAfterLogicalNot: true
SpaceAfterTemplateKeyword: true
SpaceBeforeCpp11BracedList: true
SpacesBeforeTrailingComments: 2
MaxEmptyLinesToKeep: 2
KeepEmptyLinesAtTheStartOfBlocks: true
```

## Tips

1. **Consistency**: Apply spacing rules uniformly across the codebase
2. **Readability**: More spaces can improve readability but increase line length
3. **Language Conventions**: Some languages have strong spacing conventions
4. **Trailing Comments**: Use at least 2 spaces before trailing comments for clarity
5. **Empty Lines**: Limit `MaxEmptyLinesToKeep` to prevent excessive whitespace
6. **Containers**: Enable `SpacesInContainerLiterals` for JSON/JavaScript readability

## See Also

- [Alignment](01-alignment.md) - Align code elements
- [Indentation](04-indentation.md) - Control indentation
- [Breaking](02-breaking.md) - Control line breaks
- [Full Style Options Reference](reference/clang-format-style-options.md)

---

[← Prev: Indentation](04-indentation.md) | [Back to Index](index.md) | [Next: Includes →](06-includes.md)
