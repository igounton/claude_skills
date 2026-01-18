# Configuration Templates Reference

This plugin includes seven production-ready `.clang-format` configuration templates optimized for common coding styles and scenarios.

## Templates Overview

| Template | Base Style | Use Case | Key Characteristics |
|----------|------------|----------|---------------------|
| google-cpp-modified | Google | General purpose C++ | 4-space indent, 120 column limit, balanced readability |
| linux-kernel | LLVM | Kernel/system programming | Tabs, K&R braces, Linux conventions |
| microsoft-visual-studio | Microsoft | Windows/Visual Studio development | Microsoft coding standards |
| modern-cpp17-20 | Google | Modern C++17/20 projects | Contemporary idioms, trailing return types |
| compact-dense | LLVM | Space-constrained environments | Minimal vertical space, compact formatting |
| readable-spacious | LLVM | Readability-focused projects | Extra spacing, Allman braces, clarity over density |
| multi-language | Various | Polyglot codebases | C++, JavaScript, Java in one config |

## Template Details

### google-cpp-modified.clang-format

**Description**: Modified Google C++ style with 4-space indentation and 120-character line limit.

**Base Style**: Google

**Key Settings**:
- `IndentWidth: 4` - 4 spaces for indentation
- `ColumnLimit: 120` - 120 characters per line
- `BreakBeforeBraces: Attach` - K&R style braces
- `AllowShortFunctionsOnASingleLine: Inline` - Compact short functions
- `PointerAlignment: Left` - `int* ptr` style

**Best For**:
- New C++ projects without strict style requirements
- Teams transitioning from other Google-style codebases
- Projects prioritizing readability with reasonable line lengths

**Example**:
```cpp
class Example {
 public:
    Example(int value) : value_(value) {}

    int getValue() const { return value_; }

    void processData(const std::vector<int>& data,
                     const std::string& name) {
        for (const auto& item : data) {
            // Process item
        }
    }

 private:
    int value_;
};
```

**Quick Test**:
```bash
cp assets/configs/google-cpp-modified.clang-format .clang-format
clang-format --dry-run src/main.cpp
```

---

### linux-kernel.clang-format

**Description**: Linux kernel coding standards with tabs and K&R brace style.

**Base Style**: LLVM (customized heavily)

**Key Settings**:
- `UseTab: Always` - Tabs for indentation
- `IndentWidth: 8` - 8-space tab width
- `ColumnLimit: 80` - 80 characters per line
- `BreakBeforeBraces: Linux` - Linux K&R brace style
- `PointerAlignment: Right` - `int *ptr` style

**Best For**:
- Linux kernel development
- System-level programming
- Projects following kernel conventions
- Embedded systems with kernel-style standards

**Example**:
```c
struct device {
	int id;
	char *name;
};

static int init_device(struct device *dev, const char *name)
{
	if (!dev || !name)
		return -EINVAL;

	dev->name = kmalloc(strlen(name) + 1, GFP_KERNEL);
	if (!dev->name)
		return -ENOMEM;

	strcpy(dev->name, name);
	return 0;
}
```

**Quick Test**:
```bash
cp assets/configs/linux-kernel.clang-format .clang-format
clang-format --dry-run src/driver.c
```

---

### microsoft-visual-studio.clang-format

**Description**: Microsoft coding standards commonly used in Visual Studio projects.

**Base Style**: Microsoft

**Key Settings**:
- `IndentWidth: 4` - 4 spaces for indentation
- `ColumnLimit: 120` - 120 characters per line
- `BreakBeforeBraces: Allman` - Braces on new lines
- `AllowShortBlocksOnASingleLine: Empty` - Empty blocks can be compact
- `PointerAlignment: Right` - `int *ptr` style

**Best For**:
- Windows application development
- Visual Studio / Visual C++ projects
- Teams using Microsoft coding standards
- .NET interop projects

**Example**:
```cpp
class WindowsService
{
public:
    WindowsService(LPCWSTR serviceName)
        : m_serviceName(serviceName)
    {
    }

    HRESULT Start()
    {
        if (m_isRunning)
        {
            return S_FALSE;
        }

        m_isRunning = true;
        return S_OK;
    }

private:
    LPCWSTR m_serviceName;
    bool m_isRunning = false;
};
```

**Quick Test**:
```bash
cp assets/configs/microsoft-visual-studio.clang-format .clang-format
clang-format --dry-run src/service.cpp
```

---

### modern-cpp17-20.clang-format

**Description**: Modern C++17/20 style embracing contemporary language features and idioms.

**Base Style**: Google (customized)

**Key Settings**:
- `Standard: c++20` - C++20 language standard
- `IndentWidth: 4` - 4 spaces for indentation
- `ColumnLimit: 120` - 120 characters per line
- `AllowShortLambdasOnASingleLine: All` - Compact lambdas
- `AlignConsecutiveDeclarations: true` - Align variable declarations
- `SpaceAfterTemplateKeyword: false` - `template<typename T>`

**Best For**:
- New C++17/20 projects
- Codebases using modern C++ features extensively
- Projects with concepts, ranges, coroutines
- Teams prioritizing modern idioms

**Example**:
```cpp
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<Numeric T>
class Calculator {
 public:
    auto add(T a, T b) const -> T { return a + b; }

    auto process(const std::vector<T>& values) const -> std::optional<T> {
        if (values.empty()) return std::nullopt;

        return std::accumulate(values.begin(), values.end(), T{},
                              [](T sum, T val) { return sum + val; });
    }
};
```

**Quick Test**:
```bash
cp assets/configs/modern-cpp17-20.clang-format .clang-format
clang-format --dry-run src/calculator.cpp
```

---

### compact-dense.clang-format

**Description**: Compact formatting style that minimizes vertical space usage.

**Base Style**: LLVM

**Key Settings**:
- `IndentWidth: 2` - 2 spaces for indentation
- `ColumnLimit: 100` - 100 characters per line
- `BreakBeforeBraces: Attach` - K&R style braces
- `AllowShortFunctionsOnASingleLine: All` - Aggressive function inlining
- `AllowShortIfStatementsOnASingleLine: AllIfsAndElse` - Compact conditionals
- `AllowShortLoopsOnASingleLine: true` - Single-line loops
- `KeepEmptyLinesAtTheStartOfBlocks: false` - Remove empty lines

**Best For**:
- Projects with strict line count limits
- Code review systems with limited vertical space
- Embedded systems with small displays
- Dense codebases prioritizing compactness

**Example**:
```cpp
class Compact {
 public:
  Compact() : value_(0) {}
  int getValue() const { return value_; }
  void setValue(int v) { value_ = v; }
  bool isValid() const { return value_ >= 0; }

 private:
  int value_;
};

void process(const std::vector<int>& data) {
  for (const auto& item : data) {
    if (item > 0) { processPositive(item); }
    else { processNegative(item); }
  }
}
```

**Quick Test**:
```bash
cp assets/configs/compact-dense.clang-format .clang-format
clang-format --dry-run src/compact.cpp
```

---

### readable-spacious.clang-format

**Description**: Spacious formatting style that prioritizes readability and clarity over density.

**Base Style**: LLVM

**Key Settings**:
- `IndentWidth: 4` - 4 spaces for indentation
- `ColumnLimit: 100` - 100 characters per line
- `BreakBeforeBraces: Allman` - Braces on new lines
- `AllowShortFunctionsOnASingleLine: None` - Always expand functions
- `AllowShortIfStatementsOnASingleLine: Never` - Always expand conditionals
- `AllowShortLoopsOnASingleLine: false` - Always expand loops
- `KeepEmptyLinesAtTheStartOfBlocks: true` - Preserve empty lines
- `MaxEmptyLinesToKeep: 2` - Allow breathing room

**Best For**:
- Educational codebases
- Projects prioritizing code readability
- Teams with developers of varying experience levels
- Code intended for documentation or presentation

**Example**:
```cpp
class Readable
{
public:
    Readable()
        : value_(0)
    {
    }

    int getValue() const
    {
        return value_;
    }

    void setValue(int v)
    {
        value_ = v;
    }

    bool isValid() const
    {
        return value_ >= 0;
    }

private:
    int value_;
};

void process(const std::vector<int>& data)
{
    for (const auto& item : data)
    {
        if (item > 0)
        {
            processPositive(item);
        }
        else
        {
            processNegative(item);
        }
    }
}
```

**Quick Test**:
```bash
cp assets/configs/readable-spacious.clang-format .clang-format
clang-format --dry-run src/readable.cpp
```

---

### multi-language.clang-format

**Description**: Multi-language configuration supporting C++, JavaScript, and Java with language-specific settings.

**Base Style**: Various (per language)

**Key Settings**:
- Separate configurations for each language using `Language:` blocks
- C++: Google style with 4-space indent
- JavaScript: 2-space indent, semicolons
- Java: 4-space indent, Allman braces

**Best For**:
- Polyglot codebases (mixed C++/Java/JavaScript)
- Projects with multiple language components
- Full-stack applications
- Cross-platform development

**Structure**:
```yaml
---
# Common settings
BasedOnStyle: Google
ColumnLimit: 100

---
# C++ specific
Language: Cpp
IndentWidth: 4
BreakBeforeBraces: Attach

---
# JavaScript specific
Language: JavaScript
IndentWidth: 2
SortIncludes: false

---
# Java specific
Language: Java
IndentWidth: 4
BreakBeforeBraces: Allman
```

**Example Usage**:

C++ code:
```cpp
class Example {
 public:
    void method() {
        // 4-space indent, attached braces
    }
};
```

JavaScript code:
```javascript
class Example {
  method() {
    // 2-space indent
  }
}
```

Java code:
```java
class Example
{
    void method()
    {
        // 4-space indent, Allman braces
    }
}
```

**Quick Test**:
```bash
cp assets/configs/multi-language.clang-format .clang-format
clang-format --dry-run src/main.cpp
clang-format --dry-run src/app.js
clang-format --dry-run src/Main.java
```

---

## Choosing a Template

### Decision Tree

1. **Do you have a specific style requirement?**
   - Linux kernel standards → `linux-kernel.clang-format`
   - Microsoft standards → `microsoft-visual-studio.clang-format`
   - Google standards → `google-cpp-modified.clang-format`
   - No specific requirement → Continue to 2

2. **What's your primary goal?**
   - Maximize readability → `readable-spacious.clang-format`
   - Minimize vertical space → `compact-dense.clang-format`
   - Modern C++ idioms → `modern-cpp17-20.clang-format`
   - General purpose → `google-cpp-modified.clang-format`

3. **Do you use multiple languages?**
   - Yes → Start with `multi-language.clang-format`
   - No → Use language-specific template from above

### Customizing Templates

All templates can be customized by:
1. Copy template to project root as `.clang-format`
2. Edit specific options (see [References Guide](./references-guide.md))
3. Test changes with `clang-format --dry-run`
4. Iterate until satisfied

Common customizations:
- Adjust `ColumnLimit` for your display width
- Modify `IndentWidth` for team preference
- Change `PointerAlignment` for pointer style
- Adjust `BreakBeforeBraces` for brace placement

## Template Compatibility

All templates are compatible with:
- clang-format version 10.0 and higher
- C++11 through C++20 (language-specific features)
- Multi-platform (Linux, macOS, Windows)

For older clang-format versions, some options may not be recognized. The tool will warn about unrecognized options but continue formatting with remaining settings.

## Testing Templates

Before committing to a template:

```bash
# Copy template to temporary location
cp assets/configs/google-cpp-modified.clang-format /tmp/test.clang-format

# Test on sample files
clang-format --style=file:/tmp/test.clang-format src/sample.cpp | diff - src/sample.cpp

# Test on entire project
find src -name '*.cpp' -o -name '*.h' | while read file; do
  clang-format --style=file:/tmp/test.clang-format "$file" | diff - "$file"
done

# If satisfied, copy to project
cp /tmp/test.clang-format .clang-format
```

## Source and Attribution

Templates are derived from:
- **google-cpp-modified**: [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- **linux-kernel**: [Linux Kernel Coding Style](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- **microsoft-visual-studio**: [Microsoft C++ Coding Standards](https://docs.microsoft.com/en-us/cpp/cpp/)
- **modern-cpp17-20**: [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- **compact-dense**: LLVM style with density optimizations
- **readable-spacious**: LLVM style with readability optimizations
- **multi-language**: Composite based on language-specific conventions

All templates have been tested on real-world codebases and refined for practical use.
