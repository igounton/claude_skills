# Usage Examples

This document provides concrete, real-world examples of using the Conventional Commits plugin with Claude Code.

## Example 1: Creating a Feature Commit

**Scenario**: You've added a new user profile page to your web application.

**Steps**:

1. Stage your changes:
   ```bash
   git add src/pages/UserProfile.tsx src/components/ProfileCard.tsx
   ```

2. Ask Claude:
   ```text
   Create a commit message for these changes
   ```

3. Claude analyzes the diff and produces:
   ```text
   feat(profile): add user profile page with editable fields

   Implemented new UserProfile page that displays user information
   with inline editing capability. Added ProfileCard component for
   reusable profile display across the application.

   Refs: #234
   ```

**Result**: Clean, semantic commit that will trigger a MINOR version bump and appear in the changelog under "Features".

---

## Example 2: Bug Fix with Scope

**Scenario**: You fixed a crash that occurred when users entered empty input in the search field.

**Steps**:

1. Stage the fix:
   ```bash
   git add src/components/SearchBar.tsx src/utils/validation.ts
   ```

2. Ask Claude:
   ```text
   Write a commit message for this bug fix
   ```

3. Claude produces:
   ```text
   fix(search): prevent crash on empty search input

   Added null/empty validation before processing search queries.
   Previously, empty input caused undefined access errors.

   Fixes: #456
   ```

**Result**: Commit triggers PATCH version bump, appears in changelog under "Bug Fixes".

---

## Example 3: Breaking Change with Migration Guide

**Scenario**: You're removing support for Node 14 and requiring Node 18+.

**Steps**:

1. Update package.json and CI configuration:
   ```bash
   git add package.json .github/workflows/test.yml docs/upgrade-guide.md
   ```

2. Ask Claude:
   ```text
   Create a breaking change commit for dropping Node 14 support
   ```

3. Claude produces:
   ```text
   chore!: drop support for Node 14

   Remove Node 14 from CI test matrix and update minimum version
   requirement to Node 18 LTS.

   BREAKING CHANGE: Node.js 14 is no longer supported. Projects must
   upgrade to Node 18 or later. See docs/upgrade-guide.md for migration
   instructions.

   Refs: #789
   ```

**Result**: Triggers MAJOR version bump, prominently displayed in changelog with migration guidance.

---

## Example 4: Documentation Update

**Scenario**: You updated the API reference documentation to fix typos and clarify examples.

**Steps**:

1. Stage documentation changes:
   ```bash
   git add docs/api-reference.md README.md
   ```

2. Ask Claude:
   ```text
   Commit these documentation updates
   ```

3. Claude produces:
   ```text
   docs: clarify API authentication examples

   Fixed typos in authentication section and added clearer code
   examples showing JWT token usage. Updated README with link to
   full API reference.
   ```

**Result**: Documentation-only commit, won't trigger version bump but appears in changelog.

---

## Example 5: Performance Optimization

**Scenario**: You optimized database queries to reduce API response time.

**Steps**:

1. Stage the optimizations:
   ```bash
   git add src/services/database.ts src/api/users.ts
   ```

2. Ask Claude:
   ```text
   Write a commit message for these performance improvements
   ```

3. Claude produces:
   ```text
   perf(api): reduce user query response time by 60%

   Implemented query result caching and optimized JOIN operations.
   Benchmark shows average response time reduced from 250ms to 100ms
   for user profile endpoints.

   Refs: #321
   ```

**Result**: Performance improvement documented, helps track optimization efforts in changelog.

---

## Example 6: Refactoring Without Functional Changes

**Scenario**: You extracted complex authentication logic into a separate module for better maintainability.

**Steps**:

1. Stage refactored files:
   ```bash
   git add src/auth/ src/utils/auth.ts src/middleware/authenticate.ts
   ```

2. Ask Claude:
   ```text
   Commit this authentication refactoring
   ```

3. Claude produces:
   ```text
   refactor(auth): extract authentication logic into dedicated module

   Moved auth-related functions from utils and middleware into new
   src/auth directory. Created AuthService class to centralize
   authentication operations. No functional changes.
   ```

**Result**: Clear indication that code structure changed but behavior remained the same.

---

## Example 7: Multiple Related Commits (Atomic Commits)

**Scenario**: You're adding a new feature that naturally splits into multiple atomic commits.

**Steps**:

1. First commit (data model):
   ```bash
   git add src/models/Comment.ts
   git commit -m "feat(models): add Comment model with validation"
   ```

2. Second commit (API endpoint):
   ```bash
   git add src/api/comments.ts
   git commit -m "feat(api): add comments CRUD endpoints"
   ```

3. Third commit (UI):
   ```bash
   git add src/components/CommentList.tsx src/components/CommentForm.tsx
   git commit -m "feat(ui): add comment display and submission components"
   ```

**Result**: Clear progression of work, easier to review and revert if needed.

---

## Example 8: Squash Merge with Conventional Commits

**Scenario**: Your team uses squash merging, and you need to clean up multiple WIP commits from a PR.

**Steps**:

1. Review PR changes:
   ```bash
   git diff main...feature-branch
   ```

2. Ask Claude:
   ```text
   Create a single conventional commit message summarizing this PR that adds real-time notifications
   ```

3. Claude produces:
   ```text
   feat(notifications): implement real-time notification system

   Added WebSocket-based notification system with browser notifications
   support. Users receive instant updates for mentions, replies, and
   system alerts. Implemented notification preferences UI.

   Includes:
   - WebSocket connection management with auto-reconnect
   - Browser notification API integration
   - Notification center UI component
   - User preferences for notification types

   Refs: #567
   ```

4. Use this message when squash merging on GitHub/GitLab.

**Result**: Clean commit history on main branch, comprehensive changelog entry.

---

## Example 9: CI/CD Configuration Update

**Scenario**: You added a new deployment stage to your CI pipeline.

**Steps**:

1. Stage CI configuration:
   ```bash
   git add .github/workflows/deploy.yml
   ```

2. Ask Claude:
   ```text
   Commit this CI/CD update
   ```

3. Claude produces:
   ```text
   ci: add staging deployment workflow

   Created new workflow to deploy to staging environment on push to
   develop branch. Includes smoke tests and automatic rollback on
   failure.
   ```

**Result**: Infrastructure changes clearly documented, won't trigger version bump.

---

## Example 10: Dependency Updates

**Scenario**: You updated several npm dependencies to fix security vulnerabilities.

**Steps**:

1. Stage dependency changes:
   ```bash
   git add package.json package-lock.json
   ```

2. Ask Claude:
   ```text
   Commit these security dependency updates
   ```

3. Claude produces:
   ```text
   build(deps): upgrade dependencies to fix security vulnerabilities

   Updated axios to 1.6.5 (CVE-2023-XXXXX), express to 4.18.2, and
   lodash to 4.17.21. All updates are patch versions with no breaking
   changes.

   Refs: #890
   ```

**Result**: Security updates clearly marked, easily auditable in commit history.

---

## Example 11: Team Onboarding - Setting Up Validation

**Scenario**: You're setting up conventional commits validation for your team.

**Steps**:

1. Install commitlint:
   ```bash
   npm install --save-dev @commitlint/cli @commitlint/config-conventional
   ```

2. Ask Claude:
   ```text
   Set up commitlint with husky for enforcing conventional commits
   ```

3. Claude creates configuration files and commits:
   ```text
   build: add commitlint for conventional commit enforcement

   Installed commitlint with Angular conventional config and configured
   husky to validate commit messages. All commits must now follow
   Conventional Commits specification.

   Team members should run `npm install` to enable hooks.
   ```

4. Add branch protection requiring passing checks.

**Result**: Automated enforcement prevents non-conforming commits from entering the repository.

---

## Example 12: Generating Changelog for Release

**Scenario**: You're preparing a release and need to generate a changelog from conventional commits.

**Steps**:

1. Ask Claude:
   ```text
   Generate a changelog from conventional commits between v1.2.0 and HEAD
   ```

2. Claude runs:
   ```bash
   git log v1.2.0..HEAD --pretty=format:"%s"
   ```

3. Claude produces markdown changelog:
   ```markdown
   # v1.3.0 (2025-01-18)

   ## Features

   - **profile**: add user profile page with editable fields (#234)
   - **notifications**: implement real-time notification system (#567)
   - **api**: add comments CRUD endpoints (#245)

   ## Bug Fixes

   - **search**: prevent crash on empty search input (#456)
   - **auth**: handle token expiration correctly (#678)

   ## Performance Improvements

   - **api**: reduce user query response time by 60% (#321)
   ```

**Result**: Professional changelog ready for GitHub release or CHANGELOG.md file.

---

## Example 13: Reverting a Previous Commit

**Scenario**: A feature introduced a critical bug and needs to be reverted.

**Steps**:

1. Identify problematic commit:
   ```bash
   git log --oneline
   # abc1234 feat(notifications): implement real-time notification system
   ```

2. Ask Claude:
   ```text
   Create a revert commit for abc1234
   ```

3. Claude produces:
   ```text
   revert: feat(notifications): implement real-time notification system

   This reverts commit abc1234.

   Reverting due to WebSocket memory leak causing server instability
   in production. Will reimplement with proper connection cleanup.

   Refs: abc1234, #901
   ```

**Result**: Clear audit trail showing what was reverted and why.

---

## Example 14: Monorepo with Scopes

**Scenario**: You're working in a monorepo with multiple packages.

**Steps**:

1. Update frontend package:
   ```bash
   git add packages/web-app/src/
   ```

2. Ask Claude:
   ```text
   Commit this frontend change using appropriate scope
   ```

3. Claude produces:
   ```text
   feat(web-app): add dark mode toggle to settings

   Implemented dark mode switch in user settings with system preference
   detection. Theme preference persists across sessions.
   ```

4. Update backend package:
   ```bash
   git add packages/api/src/
   ```

5. Claude produces separate commit:
   ```text
   feat(api): add user preferences endpoint

   New endpoint to store and retrieve user preferences including theme
   selection, notification settings, and language preference.
   ```

**Result**: Clear separation of changes by package, easier to track package-specific changes.

---

## Example 15: Interactive Commit Message Creation

**Scenario**: You want Claude to help you craft a commit interactively.

**Steps**:

1. Start conversation:
   ```text
   I've made changes to add email verification. Help me write a proper conventional commit.
   ```

2. Claude asks:
   ```text
   Let me help you create a conventional commit. First, let me see what changed:
   ```

3. Claude runs `git diff --staged` and asks:
   ```text
   I see you've added email verification with token generation and validation.

   Questions:
   - Is this a breaking change? (Will existing users need to re-verify?)
   - What scope should we use? (auth, user, email?)
   - Are there any related issues?
   ```

4. You respond:
   ```text
   Not breaking, use scope "auth", relates to issue #445
   ```

5. Claude produces:
   ```text
   feat(auth): add email verification with token-based confirmation

   Implemented email verification flow using time-limited tokens.
   New users receive verification email upon registration. Existing
   users are automatically marked as verified.

   Features:
   - Token generation with 24-hour expiration
   - Resend verification email functionality
   - Email template with branded styling

   Refs: #445
   ```

**Result**: Collaborative approach ensures commit accurately reflects intent and context.

---

## Summary

These examples demonstrate:

- **Feature additions** with `feat` type
- **Bug fixes** with `fix` type
- **Breaking changes** using `!` and `BREAKING CHANGE`
- **Documentation**, **performance**, and **refactoring** commits
- **CI/CD** and **build** changes
- **Team workflows** with validation and squash merging
- **Monorepo** scope usage
- **Changelog generation** and **revert** commits

All examples follow the Conventional Commits v1.0.0 specification and integrate seamlessly with semantic versioning and changelog automation tools.
