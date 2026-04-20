---
name: standup
description: Draft a daily standup from the current user's Slack, GitHub, Linear, and Google Calendar activity. Use when the user asks to create, prepare, or summarize a standup/status update from connected app activity; to collect a user's work for a date; or to verify whether Slack, GitHub, Linear, and Google Calendar connectors/MCP tools are available before drafting a standup.
---

# Standup

## Overview

Use this skill to collect the current user's activity from Slack, GitHub, Linear, and Google Calendar, then draft a standup in the team's Sup/Standup format. Default to KST. If the user does not specify an activity date, use the previous working day.

## Workflow

1. Check connector availability before collecting data.
   - Discover available tool namespaces in the current session. Each data source may be provided by different MCP servers depending on the platform (Codex, Claude Code, etc.).
   - Slack: look for any Slack-related MCP tools (e.g., `mcp__codex_apps__slack`, `mcp__slack__`, or similar).
   - GitHub: look for any GitHub MCP tools (e.g., `mcp__codex_apps__github`, `mcp__github__`, or similar).
   - Linear: look for any Linear MCP tools (e.g., `mcp__codex_apps__linear_mcp_server`, `mcp__linear__`, or similar).
   - Google Calendar: look for any Google Calendar MCP tools (e.g., `mcp__codex_apps__google_calendar`, `mcp__google_calendar__`, or similar).
   - If multiple tool families exist for the same source, prefer the one with richer functionality.
   - If a source is unavailable, continue with available sources and disclose the gap.

2. Resolve the activity date.
   - Use KST for all date interpretation.
   - If the user provides a date, use that exact KST calendar date as the activity date.
   - If no date is provided, use the previous working day in Korea: Monday -> previous Friday; Tuesday-Friday -> previous day. If today is Saturday or Sunday, use the preceding Friday.
   - Treat the activity date as the source for the "yesterday / previous workday" section. For a normal current standup, draft the "today" section from explicit current plans, open PRs/issues, and unfinished carry-over work.
   - If the user asks for a standup for a past date, use that date's submitted plan when available instead of inferring from the present.
   - Compute both KST day boundaries and UTC/Unix equivalents for tools that need timestamps.

3. Identify the current user in each source.
   - For each available source, use profile/identity tools to resolve the current user. The exact tool names vary by platform.
   - Slack: read the current profile; if the user ID is not visible, search users by the profile email/name.
   - GitHub: read the authenticated login/profile (e.g., `get_me`, `get_user_login`, or equivalent).
   - Linear: read the authenticated profile, or use `"me"` where supported.
   - Google Calendar: read the current calendar profile; use the primary calendar unless the user specifies another calendar.

4. Collect activity from each available source.
   - Read `references/tool-queries.md` for source-specific query recipes.
   - Include comments, PRs, commits, issue updates, Slack messages, threads, files, and calendar events when available.
   - First look for the user's submitted Sup/Standup response for the activity date. Use it as an anchor when found, then augment it with Slack, GitHub, and Linear evidence.
   - For Slack bot/standup messages, parse `attachments[]` as well as top-level text and blocks. The Slack connector may hide legacy attachments, so direct Slack API fallback may be needed if the user provides a token.
   - For GitHub search results, fetch important PR metadata before final synthesis so merged/open/draft state is accurate.
   - For Linear, immediately fall back to structured issue tools if the app research tool is unavailable or returns a tool-not-found/invalid-argument error.
   - For Google Calendar, use meetings as context for business activity, interviews, 1:1s, customer calls, planning, and external commitments. Do not over-weight routine calendar blocks unless they explain the day's work.

5. Normalize and synthesize.
   - Deduplicate repeated connector output and bot fallback text.
   - Group activity by project/product area when possible.
   - Separate completed work from likely carry-over work.
   - Group multiple split PRs under one user-facing initiative when they represent one rollout.
   - Merge calendar events with matching Slack/GitHub/Linear evidence into the same initiative instead of creating separate meeting bullets.
   - Merge lightweight conversations, confirmations, links, environment-variable guidance, and support replies into the relevant larger work item. Do not make them standalone bullets unless they produced a concrete deliverable or unblocked a cross-team incident.
   - Treat blockers conservatively: include only explicit blockers or clear unresolved failures. If none are found, say no blockers were found.
   - Do not copy sensitive internal URLs from Slack, such as cloud console, secrets manager, private DM, or credential-related links, into the final standup. Summarize the action instead.

6. Draft the standup.
   - Read `references/standup-format.md` for the output template.
   - Return the draft in chat unless the user explicitly asks to post or draft it in Slack.
   - Include a short source coverage note after the draft: sources checked, missing sources, and any confidence caveats.

## Quality Bar

- Prefer concrete activity over generic wording.
- Keep the standup concise enough to paste into Sup/Slack.
- Do not invent work from calendar-like assumptions.
- If today's plan is not explicit in the data, infer only from still-open PRs/issues and label it as a suggested continuation.
- Preserve product names, issue keys, PR numbers, and links when they help the user verify the draft.
