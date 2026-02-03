# Code Review Skill

Compare the current working branch with origin/main and perform a comprehensive code review.

## Instructions

1. First, fetch the latest changes from origin to ensure we have the most up-to-date main branch:
   ```bash
   git fetch origin main
   ```

2. Get the current branch name and show the comparison context:
   ```bash
   git branch --show-current
   git log origin/main..HEAD --oneline
   ```

3. Get the diff between origin/main and the current branch (committed changes):
   ```bash
   git diff origin/main...HEAD --stat
   git diff origin/main...HEAD
   ```

4. Get uncommitted changes (staged and unstaged):
   ```bash
   git status
   git diff --staged --stat
   git diff --staged
   git diff --stat
   git diff
   ```

5. List untracked files that may need to be included:
   ```bash
   git ls-files --others --exclude-standard
   ```
   For new untracked files, read them to include in the review.

6. Analyze the changes and provide a code review with the following structure:

### Review Format

**Summary**: Brief overview of what the changes accomplish

**Files Changed**: List of modified files with a brief description of changes

**Code Review Findings**:

For each significant change, evaluate:
- **Correctness**: Does the code work as intended?
- **Security**: Are there any security vulnerabilities (OWASP top 10)?
- **Performance**: Any performance concerns?
- **Maintainability**: Is the code readable and maintainable?
- **Best Practices**: Does it follow project conventions?
- **Dead Code**: Is there any added but unused code (functions, variables, imports)?
- **Duplication**: Are there any redundant implementations from refactoring?
- **Conciseness**: Is the code unnecessarily verbose or overcomplicated?
- **Minimal Changes**: Could the same goal be achieved with fewer modifications?

Categorize findings as:
- 🔴 **Critical**: Must fix before merge
- 🟡 **Warning**: Should be addressed
- 🟢 **Suggestion**: Nice to have improvements
- 💡 **Note**: Observations or questions

**Testing Considerations**: What tests should be added or verified?

**Overall Assessment**: Ready to merge / Needs changes / Needs discussion

## Additional Guidelines

- Focus on substantive issues, not style (formatters handle that)
- Consider the context from CLAUDE.md project rules
- Check for proper error handling
- Verify that new code follows existing patterns in the codebase
- Look for potential edge cases
- Ensure no secrets or sensitive data are committed
- Identify unused imports, functions, or variables that were added
- Look for copy-pasted code that could be consolidated
- Suggest simpler alternatives when code is overly complex
- Question if the scope of changes is appropriate for the stated goal
