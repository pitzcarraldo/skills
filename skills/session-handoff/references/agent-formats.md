# Agent Session Formats

Reference for coding agent session storage formats.

## Claude Code

**Storage Location**: `~/.claude/history.jsonl`

**Format**: JSON Lines (each line is a JSON object)

**Fields**:
- `display` (string): Message content/text
- `timestamp` (number): Unix timestamp in milliseconds
- `project` (string): Absolute path to working directory
- `sessionId` (string): UUID for the session
- `pastedContents` (object): Additional pasted content metadata

**Example**:
```json
{
  "display": "현재 디렉토리의 파일 목록 보여줘",
  "pastedContents": {},
  "timestamp": 1768918416727,
  "project": "/Users/user/myproject",
  "sessionId": "818d5ada-e10e-4418-b14b-5bd8b821f5f0"
}
```

**Session Identification**: Multiple entries share the same `sessionId`. Filter by `project` field to find sessions for specific directory.

## Codex

**Storage Location**: `~/.codex/sessions/YYYY/MM/<session-id>/`

**Format**: Directory-based with `state.json`

**Key Files**:
- `state.json`: Main session state including messages, cwd, model info
- Additional files may include attachments, exports, etc.

**state.json Fields**:
- `cwd` (string): Working directory path
- `messages` (array): Conversation messages
  - Each message has `role` ("user" | "assistant") and `content`
  - `content` can be string or array of content objects
- `model` (string): Model identifier (e.g., "gpt-5.4")
- `instructions` (string): System instructions

**Example state.json structure**:
```json
{
  "cwd": "/Users/user/myproject",
  "model": "gpt-5.4",
  "instructions": "You are Codex...",
  "messages": [
    {
      "role": "user",
      "content": [{"type": "text", "text": "Hello"}]
    },
    {
      "role": "assistant",
      "content": "Hi there!"
    }
  ]
}
```

## OpenCode

**Status**: Not yet implemented. OpenCode session format TBD.
