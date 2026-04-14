---
name: review-and-fix
description: CodeRabbit으로 코드 리뷰를 실행하고 발견된 이슈를 자동 수정한 뒤, 다시 리뷰하고 수정하는 과정을 이슈가 없을 때까지 반복하는 자율 루프 스킬. Use when the user says "review and fix", "리뷰하고 수정", "코드래빗 리뷰 반복", "review loop", "자동 리뷰 수정", or wants an autonomous CodeRabbit review-fix cycle until clean.
---

# Review and Fix

CodeRabbit CLI로 리뷰 실행 → 이슈 수정 → 재리뷰를 이슈가 없을 때까지 반복하는 자율 루프.

## Prerequisites

```bash
coderabbit --version 2>/dev/null || echo "NOT_INSTALLED"
coderabbit auth status 2>&1
```

If CLI version is lower than `0.4.0`, update first:

```bash
coderabbit update
coderabbit --version
```

If CLI is still not installed or version is still lower than `0.4.0`:

```
CodeRabbit CLI가 설치되어 있지 않거나 버전이 낮습니다.
설치: https://www.coderabbit.ai/cli
인증: coderabbit auth login
```

## Workflow

### Step 0: Load AGENTS.md

Search for `AGENTS.md` in the repository root. If found, follow its build/lint/test/commit guidance throughout.

### Step 1: Determine Review Scope

Check arguments or ask the user:

| Flag | Scope |
|------|-------|
| (default) | All changes (`-t all`) |
| `--uncommitted` | Uncommitted only (`-t uncommitted`) |
| `--committed` | Committed only (`-t committed`) |
| `--base <branch>` | Compare against branch (`--base <branch>`) |

### Step 2: Run CodeRabbit Review

```bash
coderabbit review --agent [scope flags]
```

Parse the output. The `--agent` flag produces minimal structured output optimized for AI agents.

### Step 3: Parse and Classify Findings

Extract each finding and classify by severity:

| Severity | Label | Action |
|----------|-------|--------|
| Critical/High | CRITICAL | Must fix |
| Medium | WARNING | Should fix |
| Minor/Low/Info | INFO | Skip (log only) |

**If no Critical or Warning findings → EXIT with success message.**

Display findings table:

```
Review Cycle #N - Findings

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 1 | CRITICAL | ... | file.ts:42 |
| 2 | WARNING  | ... | file.ts:89 |
| 3 | INFO     | ... | file.ts:12 |

Fixing N issue(s) (Critical + Warning)...
```

### Step 4: Fix Issues

For each Critical and Warning finding (Critical first):

1. Read the relevant file and surrounding context
2. Understand the issue from the CodeRabbit output
3. Apply the fix using Edit tool
4. Log: `Fixed: [Issue] at [Location]`

Skip INFO-level findings — log them but do not fix.

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
   │ Any Critical   │──No──→ EXIT (success)
   │ or Warning?    │
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
- No Critical or Warning findings remain
- Max 5 iterations reached (warn user and stop)
- Same issue appears 2+ times unchanged (skip it, warn user)

### Step 7: Summary

After the loop exits, display:

```
Review & Fix Complete

Iterations: N
Total issues found: X
  - Fixed: Y
  - Skipped (INFO): Z
  - Persistent (unfixable): W

Files modified:
  - path/to/file-a.ts
  - path/to/file-b.ts
```

## Key Rules

- **Auto-fix Critical and Warning only** — INFO findings are logged but not fixed
- **Re-run review after each fix cycle** — do not assume fixes are correct
- **Track persistent issues** — if the same issue appears twice after fix attempts, skip it and warn the user
- **Max 5 iterations** — prevent infinite loops
- **Run project validation** — lint/build/test between fix and re-review when possible
- **Do not commit automatically** — after the loop exits, let the user decide when to commit
