---
name: session-handoff
description: List and resume previous coding agent sessions by loading their context into the current session. Use when the user wants to (1) see previous sessions for the current directory with summaries, (2) continue work from a previous session by loading its full conversation context, (3) recover work from an interrupted session, or (4) transfer context between sessions. Supports Claude Code and Codex sessions.
---

# Session Handoff

Load previous coding agent session context into the current conversation to continue work seamlessly.

## Supported Agents

- **Claude Code**: Sessions from `~/.claude/history.jsonl`
- **Codex**: Sessions from `~/.codex/sessions/YYYY/MM/<id>/`

## Usage Patterns

### List Sessions

When user asks to see previous sessions:

```python
# Run the list script
python3 .agents/skills/session-handoff/scripts/list_sessions.py
```

Output format:
```
Agent   Session ID              Last Active       Summary
claude  abc123...               2025-01-20 14:30  작업 내용 요약...
codex   def456...               2025-01-19 09:15  다른 작업 내용...
```

### Resume a Session

When user specifies a session to continue (e.g., "세션 abc123 이어하기"):

1. Identify the agent type from the session ID format or previous list output
2. Load the session's conversation history
3. Present the context to the user in a clear format
4. Confirm successful handoff

**For Claude Code sessions**:
- Parse `~/.claude/history.jsonl`
- Filter entries by the specified `sessionId`
- Extract all messages with that session ID
- Present chronological conversation history

**For Codex sessions**:
- Locate session in `~/.codex/sessions/YYYY/MM/<session-id>/state.json`
- Parse the `messages` array
- Convert to readable conversation format
- Present the full context

### Context Presentation Format

When resuming, present the loaded context clearly:

```
# 세션 핸드오프 완료

**세션 ID**: <session-id>
**Agent**: <agent-type>
**마지막 활동**: <timestamp>

## 이전 대화 내용

<formatted conversation history>

---

이어서 작업하겠습니다. 무엇을 도와드릴까요?
```

## Implementation Notes

- Sessions are filtered by the current working directory (`cwd`)
- Only sessions matching the current project directory are shown/loaded
- Sessions are sorted by last activity (most recent first)
- Claude Code: Multiple entries share the same `sessionId` - group and deduplicate
- Codex: Each session has a unique directory with `state.json`

## Resources

- **scripts/list_sessions.py**: Scan and list sessions for current directory
- **references/agent-formats.md**: Detailed session format specifications
