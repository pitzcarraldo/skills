#!/usr/bin/env python3
"""
List coding agent sessions for the current working directory.
Supports Claude Code and Codex sessions.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def get_claude_sessions(cwd: str) -> list[dict[str, Any]]:
    """Find Claude Code sessions for the current working directory."""
    sessions = []
    history_path = Path.home() / ".claude" / "history.jsonl"

    if not history_path.exists():
        return sessions

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    project = entry.get("project", "")
                    if project and os.path.samefile(project, cwd):
                        session_id = entry.get("sessionId", "unknown")
                        display = entry.get("display", "")[:60]
                        timestamp = entry.get("timestamp", 0)
                        dt = datetime.fromtimestamp(timestamp / 1000)

                        sessions.append({
                            "agent": "claude",
                            "session_id": session_id,
                            "summary": display[:50] + "..." if len(display) > 50 else display,
                            "last_active": dt.strftime("%Y-%m-%d %H:%M"),
                            "timestamp": timestamp,
                        })
                except (json.JSONDecodeError, OSError):
                    continue
    except Exception as e:
        print(f"Warning: Could not read Claude history: {e}", file=sys.stderr)

    # Deduplicate by session_id, keeping the most recent entry
    seen = {}
    for session in sorted(sessions, key=lambda x: x["timestamp"], reverse=True):
        if session["session_id"] not in seen:
            seen[session["session_id"]] = session

    return list(seen.values())


def get_codex_sessions(cwd: str) -> list[dict[str, Any]]:
    """Find Codex sessions for the current working directory."""
    sessions = []
    codex_sessions_path = Path.home() / ".codex" / "sessions"

    if not codex_sessions_path.exists():
        return sessions

    try:
        for year_dir in codex_sessions_path.iterdir():
            if not year_dir.is_dir():
                continue
            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir():
                    continue
                for session_dir in month_dir.iterdir():
                    if not session_dir.is_dir():
                        continue

                    session_id = session_dir.name
                    state_path = session_dir / "state.json"

                    if state_path.exists():
                        try:
                            with open(state_path, "r", encoding="utf-8") as f:
                                state = json.load(f)

                            # Check if this session is for the current working directory
                            session_cwd = state.get("cwd", "")
                            if session_cwd and os.path.samefile(session_cwd, cwd):
                                # Get last message for summary
                                messages = state.get("messages", [])
                                summary = ""
                                if messages:
                                    last_msg = messages[-1]
                                    content = last_msg.get("content", "")
                                    if isinstance(content, list):
                                        # Handle complex content structure
                                        for item in content:
                                            if isinstance(item, dict) and "text" in item:
                                                summary = item["text"]
                                                break
                                    elif isinstance(content, str):
                                        summary = content
                                    summary = summary[:50] + "..." if len(summary) > 50 else summary

                                # Get last modified time
                                mtime = state_path.stat().st_mtime
                                dt = datetime.fromtimestamp(mtime)

                                sessions.append({
                                    "agent": "codex",
                                    "session_id": session_id,
                                    "summary": summary or "(no messages)",
                                    "last_active": dt.strftime("%Y-%m-%d %H:%M"),
                                    "timestamp": int(mtime * 1000),
                                })
                        except (json.JSONDecodeError, OSError):
                            continue
    except Exception as e:
        print(f"Warning: Could not read Codex sessions: {e}", file=sys.stderr)

    return sessions


def format_sessions(sessions: list[dict[str, Any]]) -> str:
    """Format sessions as a table."""
    if not sessions:
        return "No sessions found for current directory."

    # Sort by timestamp (most recent first)
    sessions = sorted(sessions, key=lambda x: x["timestamp"], reverse=True)

    # Calculate column widths
    agent_width = max(len(s["agent"]) for s in sessions)
    id_width = min(24, max(len(s["session_id"]) for s in sessions))
    time_width = 16

    lines = []
    header = f"{'Agent':<{agent_width}}  {'Session ID':<{id_width}}  {'Last Active':<{time_width}}  Summary"
    lines.append(header)
    lines.append("-" * len(header))

    for session in sessions:
        agent = session["agent"]
        sid = session["session_id"][:id_width]
        time = session["last_active"]
        summary = session["summary"]
        lines.append(f"{agent:<{agent_width}}  {sid:<{id_width}}  {time:<{time_width}}  {summary}")

    return "\n".join(lines)


def main():
    cwd = os.getcwd()

    all_sessions = []
    all_sessions.extend(get_claude_sessions(cwd))
    all_sessions.extend(get_codex_sessions(cwd))

    print(format_sessions(all_sessions))


if __name__ == "__main__":
    main()
