# Agent Skills

> My personal collection of agent skills for everyday development workflows.

Agent Skills are folders of instructions, scripts, and resources that AI coding agents can discover and use to perform specialized tasks. This repository contains skills I've built and curated for my own use—feel free to use them, fork them, or use them as inspiration for your own.

## Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| [`commit`](./skills/commit) | Conventional commit automation with intelligent type/scope detection | `/commit` |
| [`pr-review`](./skills/pr-review) | Process unresolved GitHub PR discussions automatically | `/pr-review [url]` |
| [`rename-branch`](./skills/rename-branch) | Rename branches based on changes following conventions | `/rename-branch` |
| [`hwp`](./skills/hwp) | Read Korean HWP/HWPX word processor files | `/hwp [file]` |

## Installation

Install skills using [add-skill](https://github.com/vercel-labs/add-skill):

```bash
# Install all skills from this repository
npx add-skill pitzcarraldo/skills

# Install a specific skill
npx add-skill pitzcarraldo/skills -s commit
npx add-skill pitzcarraldo/skills -s pr-review
npx add-skill pitzcarraldo/skills -s rename-branch
npx add-skill pitzcarraldo/skills -s hwp
```

### Supported Agents

These skills work with any agent that follows the [Agent Skills specification](https://github.com/anthropics/agent-skill-spec):

- [Claude Code](https://claude.ai/code)
- [Codex](https://openai.com/codex)
- [Cursor](https://cursor.sh)
- And [more...](https://github.com/vercel-labs/add-skill#supported-agents)

### Skill-specific Dependencies

Some skills require additional tools:

**pr-review** requires [GitHub CLI](https://cli.github.com/):
```bash
brew install gh && gh auth login
```

**hwp** requires Python libraries:
```bash
pip install python-hwpx pyhwp
```

## What's Inside

### commit

Analyzes staged git changes and creates commits following [Conventional Commits](https://conventionalcommits.org/).

- Auto-detects commit type (`feat`, `fix`, `docs`, `refactor`, etc.)
- Extracts scope from file paths
- Generates imperative mood descriptions
- Adds Co-Authored-By footer

### pr-review

Processes unresolved GitHub PR review discussions.

- Fetches discussions via GitHub GraphQL API
- Validates feedback against current code state
- Creates todos for valid feedback
- Posts clarifying responses for misunderstandings
- Auto-resolves addressed discussions

### rename-branch

Renames branches to follow conventional naming patterns.

- Analyzes diff against base branch
- Generates `type/description` format names
- Handles edge cases (detached HEAD, protected branches)
- Provides remote update instructions

### hwp

Reads Korean Hangul Word Processor files (.hwp, .hwpx).

- Supports legacy HWP 5.x and modern HWPX formats
- Extracts text with structure preservation
- Handles tables and complex formatting

## Creating Your Own Skills

Each skill is a folder inside `skills/` containing a `SKILL.md` file:

```
skills/
└── skill-name/
    └── SKILL.md
```

The `SKILL.md` requires YAML frontmatter:

```yaml
---
name: skill-name
description: What this skill does and when to use it
user-invocable: true
---

# Skill Title

Instructions for the agent...
```

See the [Agent Skills specification](https://github.com/anthropics/agent-skill-spec) for details.

## Related Resources

- [anthropics/skills](https://github.com/anthropics/skills) — Official Anthropic skills collection
- [openai/skills](https://github.com/openai/skills) — OpenAI's skills catalog
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel's curated skills
- [vercel-labs/add-skill](https://github.com/vercel-labs/add-skill) — CLI tool for installing skills

## License

MIT
