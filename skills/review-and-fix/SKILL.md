---
name: review-and-fix
description: Pre-push CodeRabbit review-fix loop. Runs local CodeRabbit review, fixes valid issues, and repeats until clean so the branch passes CodeRabbit review on push with no additional comments. Use when the user says "review and fix", "review loop", or wants to ensure the branch is CodeRabbit-clean before pushing.
---

# Review and Fix

Ensure the current branch passes CodeRabbit review **before pushing** — so that when the branch is pushed and CodeRabbit runs on the PR, it produces no new review comments.

This skill runs CodeRabbit CLI locally, validates and fixes real issues, and repeats the cycle until the review is clean.

## Prerequisites

```bash
coderabbit --version 2>/dev/null || echo "NOT_INSTALLED"
coderabbit auth status 2>&1
```

If CLI is not on the latest version, update first:

```bash
coderabbit update
coderabbit --version
```

If CLI is still not installed or not on the latest version:

```
CodeRabbit CLI is not installed or outdated.
Install: https://www.coderabbit.ai/cli
Auth:    coderabbit auth login
```

## Workflow

### Step 0: Load AGENTS.md

Search for `AGENTS.md` in the repository root. If found, follow its build/lint/test/commit guidance throughout.

### Step 1: Determine Review Scope

Check arguments or ask the user:

| Flag | Scope |
|------|-------|
| (default) | All changes vs `origin/main` (`-t all --base origin/main`) |
| `--uncommitted` | Uncommitted only vs `origin/main` (`-t uncommitted --base origin/main`) |
| `--committed` | Committed only vs `origin/main` (`-t committed --base origin/main`) |
| `--base <branch>` | Override base branch (`--base <branch>`) — defaults to `origin/main`, not local `main` |

**Always compare against the remote tracking branch (`origin/main`) instead of the local `main`**, since the local `main` may be stale. If a different base is required, pass `--base <branch>` explicitly.

Before running the review, ensure `origin/main` is up to date:

```bash
git fetch origin main
```

### Step 2: Run CodeRabbit Review

```bash
coderabbit review --agent --base origin/main [additional scope flags]
```

Parse the output. The `--agent` flag produces minimal structured output optimized for AI agents. The `--base origin/main` flag ensures the review compares against the remote tracking branch.

### Step 3: Parse, Classify, and Validate Findings

Extract each finding and perform a two-step evaluation:

#### 3.1 Severity Classification

| Severity | Label | Action |
|----------|-------|--------|
| Critical/High | CRITICAL | Must fix |
| Medium | WARNING | Should fix |
| Minor/Low/Info | INFO | Skip (log only) |

**If no Critical or Warning findings → EXIT with success message.**

#### 3.2 Finding Validation

Before fixing any Critical or Warning finding, validate whether it is a true positive:

**Read the actual code** at the reported location with sufficient surrounding context (10+ lines before and after). Then classify:

| Category | Criteria | Action |
|----------|----------|--------|
| **Valid** | Issue exists in current code and the suggestion is technically correct | Fix it |
| **False Positive** | Code already handles the concern, or the tool misread the implementation | Skip and log reason |
| **Context-Dependent** | Suggestion is technically valid but conflicts with project conventions, intentional design, or surrounding code patterns | Skip and log reason |
| **Already Addressed** | Issue was fixed in a recent commit or is handled elsewhere in the codebase | Skip and log reason |

**Validation checklist for each finding:**

1. Read the file and understand the actual code at the reported location
2. Check if the reported issue actually exists in the current code
3. Verify the suggestion doesn't break existing logic, types, or tests
4. Check if the pattern is intentional (e.g., project convention, framework requirement)
5. Look for related code that may already handle the concern (imports, base classes, middleware)

**Common false positive patterns to watch for:**
- Flagging intentional `any` types that are required by external APIs
- Suggesting error handling for cases the framework already catches
- Reporting unused variables that are destructured for side effects
- Recommending patterns that conflict with the project's established conventions
- Flagging missing null checks where the type system guarantees non-null

Display findings table with validation results:

```
Review Cycle #N - Findings

| # | Severity | Verdict | Issue | Location |
|---|----------|---------|-------|----------|
| 1 | CRITICAL | Valid   | ...   | file.ts:42 |
| 2 | WARNING  | False+  | ...   | file.ts:89 |
| 3 | WARNING  | Valid   | ...   | file.ts:102 |
| 4 | INFO     | —       | ...   | file.ts:12 |

Fixing 2 valid issue(s), skipping 1 false positive...
```

### Step 4: Fix Valid Issues

For each validated Critical and Warning finding (Critical first):

1. Read the relevant file and surrounding context
2. Understand the issue from the CodeRabbit output
3. Apply the fix using Edit tool
4. Log: `Fixed: [Issue] at [Location]`

Skip INFO-level findings and false positives — log them but do not fix.

### Step 5: Verify Fixes

Run project validation if available (from AGENTS.md):
- Lint: `pnpm lint` or equivalent
- Type check: `pnpm build` or `tsc --noEmit`
- Test: `pnpm test` if relevant files changed

If validation fails, fix the failure before proceeding.

### Step 6: Loop Decision

```
┌─────────────────────────────────┐
│  coderabbit review --agent      │
└──────────┬──────────────────────┘
           ▼
   ┌───────────────┐
   │ Any valid      │──No──→ EXIT (success)
   │ Critical or    │
   │ Warning?       │
   └───────┬───────┘
          Yes
           ▼
   ┌───────────────┐
   │ Fix issues     │
   │ Verify fixes   │
   └───────┬───────┘
           ▼
   ┌───────────────┐
   │ Re-run review  │──→ (back to top)
   └───────────────┘

   Max iterations: 5 (safety limit)
```

After fixing, go back to **Step 2** and re-run the review.

**Exit conditions:**
- No valid Critical or Warning findings remain
- Max 5 iterations reached (warn user and stop)
- Same issue appears 2+ times unchanged (skip it, warn user)

### Step 7: Summary

After the loop exits, display:

```
Review & Fix Complete

Iterations: N
Total issues found: X
  - Fixed: Y
  - False positives: F
  - Skipped (INFO): Z
  - Persistent (unfixable): W

Files modified:
  - path/to/file-a.ts
  - path/to/file-b.ts
```

## Key Rules

- **Validate before fixing** — read the actual code and confirm the issue is real before applying any change
- **Auto-fix valid Critical and Warning only** — INFO findings and false positives are logged but not fixed
- **Re-run review after each fix cycle** — do not assume fixes are correct
- **Track persistent issues** — if the same issue appears twice after fix attempts, skip it and warn the user
- **Max 5 iterations** — prevent infinite loops
- **Run project validation** — lint/build/test between fix and re-review when possible
- **Do not commit automatically** — after the loop exits, let the user decide when to commit
