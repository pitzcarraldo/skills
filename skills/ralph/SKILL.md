---
name: ralph
description: "Implementation of the Ralph Loop technique - continuous self-referential AI loops for interactive iterative development. Run the agent in a while-true loop with the same prompt until task completion."
allowed-tools: Read Write Bash Grep Glob
metadata:
  tags: ralph, ralph-loop, iterative-loop, self-referential, completion-promise
  platforms: Any coding agent that can read files, edit files, and run local commands
  keyword: ralph
  version: 2.0.0
  source: "Based on Ralph Loop technique by Geoffrey Huntley (https://ghuntley.com/ralph/)"
  author:
    name: Daisy Hollman
    email: daisy@anthropic.com
---

# Ralph Loop

Implementation of the Ralph Loop technique for iterative, self-referential AI development loops.

## What is Ralph?

Ralph is a development methodology based on continuous AI agent loops. As Geoffrey Huntley describes it: **"Ralph is a Bash loop"** - a simple `while true` that repeatedly feeds an AI agent a prompt file, allowing it to iteratively improve its work until completion.

The technique is named after Ralph Loop from The Simpsons, embodying the philosophy of persistent iteration despite setbacks.

### Core Concept

This skill implements Ralph using a **Stop hook** that intercepts the agent's exit attempts:

```bash
# You run ONCE:
/ralph-loop "Your task description" --completion-promise "DONE"

# Then the agent automatically:
# 1. Works on the task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds the SAME prompt back
# 5. Repeat until completion
```

The loop happens **inside your current session** - you don't need external bash loops. The Stop hook creates the self-referential feedback loop by blocking normal session exit.

This creates a **self-referential feedback loop** where:
- The prompt never changes between iterations
- The agent's previous work persists in files
- Each iteration sees modified files and git history
- The agent autonomously improves by reading its own past work in files

## Quick Start

```bash
/ralph-loop "Build a REST API for todos. Requirements: CRUD operations, input validation, tests. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 50
```

The agent will:
- Implement the API iteratively
- Run tests and see failures
- Fix bugs based on test output
- Iterate until all requirements met
- Output the completion promise when done

## Commands

### /ralph-loop

Start a Ralph loop in your current session.

**Usage:**
```bash
/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"
```

**Options:**
- `--max-iterations <n>` - Stop after N iterations (default: unlimited)
- `--completion-promise <text>` - Phrase that signals completion

Execute the setup script to initialize the Ralph loop:

```bash
"~/.agents/skills/ralph/scripts/setup-ralph-loop.sh" $ARGUMENTS
```

Please work on the task. When you try to exit, the Ralph loop will feed the SAME PROMPT back to you for the next iteration. You'll see your previous work in files and git history, allowing you to iterate and improve.

CRITICAL RULE: If a completion promise is set, you may ONLY output it when the statement is completely and unequivocally TRUE. Do not output false promises to escape the loop, even if you think you're stuck or should exit for other reasons. The loop is designed to continue until genuine completion.

### /cancel-ralph

Cancel the active Ralph loop.

1. Check if `.ralph/ralph-loop.local.md` exists using Bash: `test -f .ralph/ralph-loop.local.md && echo "EXISTS" || echo "NOT_FOUND"`

2. **If NOT_FOUND**: Say "No active Ralph loop found."

3. **If EXISTS**:
   - Read `.ralph/ralph-loop.local.md` to get the current iteration number from the `iteration:` field
   - Remove the file using Bash: `rm .ralph/ralph-loop.local.md`
   - Report: "Cancelled Ralph loop (was at iteration N)" where N is the iteration value

### /help

#### What is the Ralph Loop Technique?

The Ralph Loop technique is an iterative development methodology based on continuous AI loops, pioneered by Geoffrey Huntley.

**Core concept:**
```bash
while :; do
  cat PROMPT.md | coding-agent --continue
done
```

The same prompt is fed to the agent repeatedly. The "self-referential" aspect comes from the agent seeing its own previous work in the files and git history, not from feeding output back as input.

**Each iteration:**
1. The agent receives the SAME prompt
2. Works on the task, modifying files
3. Tries to exit
4. Stop hook intercepts and feeds the same prompt again
5. The agent sees its previous work in the files
6. Iteratively improves until completion

The technique is described as "deterministically bad in an undeterministic world" - failures are predictable, enabling systematic improvement through prompt tuning.

#### Key Concepts

##### Completion Promises

To signal completion, the agent must output a `<promise>` tag:

```
<promise>TASK COMPLETE</promise>
```

The stop hook looks for this specific tag. Without it (or `--max-iterations`), Ralph runs infinitely.

##### Self-Reference Mechanism

The "loop" doesn't mean the agent talks to itself. It means:
- Same prompt repeated
- The agent's work persists in files
- Each iteration sees previous attempts
- Builds incrementally toward goal

## Prompt Writing Best Practices

### 1. Clear Completion Criteria

❌ Bad: "Build a todo API and make it good."

✅ Good:
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs
- Output: <promise>COMPLETE</promise>
```

### 2. Incremental Goals

❌ Bad: "Create a complete e-commerce platform."

✅ Good:
```markdown
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)

Output <promise>COMPLETE</promise> when all phases done.
```

### 3. Self-Correction

❌ Bad: "Write code for feature X."

✅ Good:
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
7. Output: <promise>COMPLETE</promise>
```

### 4. Escape Hatches

Always use `--max-iterations` as a safety net to prevent infinite loops on impossible tasks:

```bash
# Recommended: Always set a reasonable iteration limit
/ralph-loop "Try to implement feature X" --max-iterations 20

# In your prompt, include what to do if stuck:
# "After 15 iterations, if not complete:
#  - Document what's blocking progress
#  - List what was attempted
#  - Suggest alternative approaches"
```

**Note**: The `--completion-promise` uses exact string matching, so you cannot use it for multiple completion conditions (like "SUCCESS" vs "BLOCKED"). Always rely on `--max-iterations` as your primary safety mechanism.

## Philosophy

Ralph embodies several key principles:

### 1. Iteration > Perfection
Don't aim for perfect on first try. Let the loop refine the work.

### 2. Failures Are Data
"Deterministically bad" means failures are predictable and informative. Use them to tune prompts.

### 3. Operator Skill Matters
Success depends on writing good prompts, not just having a good model.

### 4. Persistence Wins
Keep trying until success. The loop handles retry logic automatically.

## When to Use Ralph

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement (e.g., getting tests to pass)
- Greenfield projects where you can walk away
- Tasks with automatic verification (tests, linters)

**Not good for:**
- Tasks requiring human judgment or design decisions
- One-shot operations
- Tasks with unclear success criteria
- Production debugging (use targeted debugging instead)

## Real-World Results

- Successfully generated 6 repositories overnight in Y Combinator hackathon testing
- One $50k contract completed for $297 in API costs
- Created entire programming language ("cursed") over 3 months using this approach

## Learn More

- Original technique: https://ghuntley.com/ralph/
- Ralph Orchestrator: https://github.com/mikeyobrien/ralph-orchestrator
