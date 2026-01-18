# Integration Scripts Reference

This plugin includes three integration scripts for seamlessly incorporating clang-format into your development workflow.

## Scripts Overview

| Script | Purpose | Compatibility | Automation Level |
|--------|---------|---------------|------------------|
| pre-commit | Git hook for automatic formatting | pre-commit, prek, manual | Automatic on commit |
| vimrc-clang-format.vim | Vim format-on-save | Vim/Neovim | Automatic on save |
| emacs-clang-format.el | Emacs clang-format integration | Emacs | Automatic on save |

## Git Hook: pre-commit

**Location**: `assets/integrations/pre-commit`

**Purpose**: Automatically format staged files before committing, preventing unformatted code from entering the repository.

### Features

- Formats only staged files (preserves unstaged changes)
- Works with both pre-commit framework and manual git hooks
- Compatible with prek (Rust-based pre-commit alternative)
- Checks for clang-format availability before running
- Provides clear error messages if formatting fails

### Installation Methods

#### Method 1: Using pre-commit Framework (Recommended)

The [pre-commit framework](https://pre-commit.com/) automatically manages hooks and clang-format versions.

1. **Install pre-commit**:
   ```bash
   # Using pip
   pip install pre-commit

   # Using homebrew (macOS)
   brew install pre-commit

   # Using apt (Ubuntu/Debian)
   sudo apt install pre-commit
   ```

2. **Create `.pre-commit-config.yaml`** in your project root:
   ```yaml
   repos:
     - repo: https://github.com/pre-commit/mirrors-clang-format
       rev: v19.1.7  # Use the latest version
       hooks:
         - id: clang-format
           types_or: [c++, c, cuda]
   ```

3. **Install the hook**:
   ```bash
   pre-commit install
   ```

4. **Test**:
   ```bash
   # Run on all files
   pre-commit run --all-files

   # Run on staged files (automatic on commit)
   git add file.cpp
   git commit -m "test"
   ```

#### Method 2: Using prek Framework

[prek](https://github.com/thoughtpolice/prek) is a Rust-based alternative to pre-commit with identical configuration.

1. **Install prek**:
   ```bash
   cargo install prek
   ```

2. **Use same `.pre-commit-config.yaml`** as Method 1

3. **Install the hook**:
   ```bash
   prek install
   ```

4. **Test** (same as Method 1)

#### Method 3: Manual Git Hook

For projects that don't use pre-commit framework.

1. **Copy the hook script**:
   ```bash
   cp assets/integrations/pre-commit .git/hooks/pre-commit
   ```

2. **Make it executable**:
   ```bash
   chmod +x .git/hooks/pre-commit
   ```

3. **Ensure clang-format is in PATH**:
   ```bash
   which clang-format
   # Should print: /usr/bin/clang-format (or similar)
   ```

4. **Test**:
   ```bash
   git add file.cpp
   git commit -m "test"
   # Hook should run automatically
   ```

### Configuration

The hook respects your project's `.clang-format` configuration file. Ensure it exists in your project root or parent directories.

**Verify configuration detection**:
```bash
clang-format --dump-config src/file.cpp
```

### Behavior

**When you commit**:
1. Hook identifies staged files with supported extensions (.cpp, .h, .c, .cc, .cxx, .hpp)
2. Runs `clang-format -i` on each staged file
3. Re-stages the formatted files
4. Proceeds with commit

**If formatting fails**:
- Commit is aborted
- Error message indicates which file failed
- You can fix the issue and try again

**Skipping the hook** (when necessary):
```bash
git commit --no-verify -m "Skip formatting temporarily"
```

### Supported File Extensions

- C++: `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`, `.h`
- C: `.c`, `.h`
- Objective-C: `.m`, `.mm`
- CUDA: `.cu`, `.cuh`

### Troubleshooting

**Hook doesn't run**:
- Verify executable permissions: `ls -l .git/hooks/pre-commit`
- Check hook installed: `ls .git/hooks/pre-commit`
- For pre-commit framework: `pre-commit install --install-hooks`

**clang-format not found**:
- Install clang-format: `sudo apt install clang-format` (Ubuntu) or `brew install clang-format` (macOS)
- Verify in PATH: `which clang-format`

**Formatting fails on certain files**:
- Check .clang-format syntax: `clang-format --dump-config file.cpp`
- Test formatting manually: `clang-format -i file.cpp`

---

## Vim Integration: vimrc-clang-format.vim

**Location**: `assets/integrations/vimrc-clang-format.vim`

**Purpose**: Automatically format files when saving in Vim, providing instant feedback on code style.

### Features

- Format-on-save for C, C++, Objective-C, and Java files
- Respects project `.clang-format` configuration
- Silent operation (no interruptions)
- Works with both Vim and Neovim

### Installation

1. **Copy configuration to `.vimrc`**:
   ```bash
   cat assets/integrations/vimrc-clang-format.vim >> ~/.vimrc
   ```

   Or manually add this content to `~/.vimrc`:
   ```vim
   " clang-format integration
   function! ClangFormat()
       let l:lines = "all"
       execute 'silent !clang-format -i %'
       execute 'redraw!'
   endfunction

   " Auto-format on save for C/C++/Objective-C/Java
   autocmd BufWritePre *.c,*.cpp,*.cc,*.cxx,*.h,*.hpp,*.m,*.mm,*.java call ClangFormat()
   ```

2. **Reload Vim configuration**:
   ```vim
   :source ~/.vimrc
   ```

   Or restart Vim.

3. **Test**:
   - Open a C++ file: `vim test.cpp`
   - Make changes
   - Save: `:w`
   - File should be automatically formatted

### Configuration

The integration uses your project's `.clang-format` file automatically. No additional configuration needed.

**Customize file extensions**:
```vim
" Add more file types
autocmd BufWritePre *.c,*.cpp,*.h,*.proto call ClangFormat()

" Remove Java if not needed
autocmd BufWritePre *.c,*.cpp,*.cc,*.cxx,*.h,*.hpp call ClangFormat()
```

**Disable for specific files**:
```vim
" Skip formatting for this file only
:autocmd! BufWritePre <buffer>
```

**Temporary disable**:
```vim
" Disable all format-on-save
:autocmd! BufWritePre

" Re-enable by sourcing vimrc again
:source ~/.vimrc
```

### Advanced Features

**Manual formatting with keybinding**:
```vim
" Add to .vimrc
nnoremap <Leader>cf :call ClangFormat()<CR>

" Usage: Press <Leader>cf (usually \cf) to format
```

**Format visual selection only** (requires clang-format binary with range support):
```vim
function! ClangFormatRange()
    let l:start = line("'<")
    let l:end = line("'>")
    execute 'silent !clang-format -i --lines=' . l:start . ':' . l:end . ' %'
    execute 'redraw!'
endfunction

vnoremap <Leader>cf :call ClangFormatRange()<CR>
```

**Show formatting changes before saving**:
```vim
function! ClangFormatDiff()
    let l:original = getline(1, '$')
    call ClangFormat()
    let l:formatted = getline(1, '$')
    " Compare and show diff (implementation varies)
endfunction
```

### Troubleshooting

**Vim freezes on save**:
- Ensure `silent` keyword is present in command
- Check clang-format runs quickly: `time clang-format -i test.cpp`

**Formatting not applied**:
- Verify clang-format in PATH: `:!which clang-format`
- Test manually: `:!clang-format -i %`
- Check for `.clang-format` file: `:!clang-format --dump-config %`

**Undo/redo issues**:
- Formatting creates a new undo point
- Use `u` to undo formatting
- Save without formatting: `:autocmd! BufWritePre <buffer>` then `:w`

---

## Emacs Integration: emacs-clang-format.el

**Location**: `assets/integrations/emacs-clang-format.el`

**Purpose**: Integrate clang-format into Emacs for automatic formatting on save.

### Features

- Format-on-save for C, C++, Objective-C modes
- Uses clang-format-mode package
- Respects project `.clang-format` configuration
- Customizable keybindings

### Installation

1. **Install clang-format-mode package**:

   Add to your Emacs configuration (`~/.emacs` or `~/.emacs.d/init.el`):
   ```elisp
   ;; Using package.el
   (require 'package)
   (add-to-list 'package-archives
                '("melpa" . "https://melpa.org/packages/"))
   (package-initialize)

   ;; Install clang-format if not already installed
   (unless (package-installed-p 'clang-format)
     (package-refresh-contents)
     (package-install 'clang-format))
   ```

   Or using `use-package`:
   ```elisp
   (use-package clang-format
     :ensure t)
   ```

2. **Copy integration configuration**:
   ```bash
   cat assets/integrations/emacs-clang-format.el >> ~/.emacs
   ```

   Or manually add to `~/.emacs`:
   ```elisp
   ;; clang-format integration
   (require 'clang-format)

   ;; Format buffer on save
   (add-hook 'c-mode-hook
             (lambda () (add-hook 'before-save-hook 'clang-format-buffer nil 'local)))
   (add-hook 'c++-mode-hook
             (lambda () (add-hook 'before-save-hook 'clang-format-buffer nil 'local)))
   (add-hook 'objc-mode-hook
             (lambda () (add-hook 'before-save-hook 'clang-format-buffer nil 'local)))

   ;; Keybinding for manual formatting
   (global-set-key (kbd "C-c C-f") 'clang-format-buffer)
   (global-set-key (kbd "C-c C-r") 'clang-format-region)
   ```

3. **Reload Emacs configuration**:
   ```elisp
   M-x eval-buffer
   ```

   Or restart Emacs.

4. **Test**:
   - Open a C++ file: `C-x C-f test.cpp`
   - Make changes
   - Save: `C-x C-s`
   - Buffer should be automatically formatted

### Configuration

**Customize clang-format binary location**:
```elisp
(setq clang-format-executable "/usr/local/bin/clang-format")
```

**Use specific .clang-format file**:
```elisp
(setq clang-format-style-option "file:/path/to/.clang-format")
```

**Disable for specific projects**:
```elisp
;; In .dir-locals.el at project root
((c++-mode . ((eval . (remove-hook 'before-save-hook 'clang-format-buffer t)))))
```

**Add more modes**:
```elisp
(add-hook 'java-mode-hook
          (lambda () (add-hook 'before-save-hook 'clang-format-buffer nil 'local)))
```

### Usage

**Automatic**: Format-on-save is enabled for C/C++/Objective-C files.

**Manual**:
- Format entire buffer: `C-c C-f` or `M-x clang-format-buffer`
- Format selected region: `C-c C-r` or `M-x clang-format-region`

**Temporarily disable**:
```elisp
M-x remove-hook RET before-save-hook RET clang-format-buffer
```

**Re-enable**:
```elisp
M-x eval-buffer  ; Reload configuration
```

### Advanced Features

**Show changes before applying**:
```elisp
(setq clang-format-show-changes t)
```

**Customize keybindings**:
```elisp
;; Use different keys
(global-set-key (kbd "C-M-f") 'clang-format-buffer)
(define-key c++-mode-map (kbd "C-c f") 'clang-format-buffer)
```

**Format on save with confirmation**:
```elisp
(defun clang-format-buffer-smart ()
  "Ask before formatting."
  (interactive)
  (when (y-or-n-p "Format buffer with clang-format? ")
    (clang-format-buffer)))

(add-hook 'c++-mode-hook
          (lambda () (add-hook 'before-save-hook 'clang-format-buffer-smart nil 'local)))
```

### Troubleshooting

**clang-format package not found**:
- Ensure MELPA repository is configured
- Run `M-x package-refresh-contents`
- Manually install: `M-x package-install RET clang-format`

**Formatting not applied on save**:
- Verify hook installed: `M-x describe-variable RET before-save-hook`
- Check clang-format binary: `M-x shell-command RET which clang-format`
- Test manually: `M-x clang-format-buffer`

**Emacs freezes on save**:
- Check clang-format performance: `time clang-format -i test.cpp`
- Consider disabling format-on-save for large files

---

## Other Editor Integrations

While this plugin includes Vim and Emacs integrations, clang-format supports many other editors. See the [references/cli-usage.md](../skills/clang-format/references/cli-usage.md) file for setup instructions for:

- Visual Studio Code
- CLion / IntelliJ IDEA
- Sublime Text
- Atom
- Eclipse
- Qt Creator

## CI/CD Integration

For continuous integration setups, see [references/cli-usage.md](../skills/clang-format/references/cli-usage.md) for examples with:

- GitHub Actions
- GitLab CI
- Jenkins
- Travis CI
- CircleCI

## Summary

All integration scripts are designed to work seamlessly with your project's `.clang-format` configuration. Choose the integration(s) that match your workflow:

- **Git hook** - Enforce formatting at commit time
- **Vim integration** - Format automatically while editing
- **Emacs integration** - Format automatically while editing

Multiple integrations can be used simultaneously for a fully automated formatting workflow.
