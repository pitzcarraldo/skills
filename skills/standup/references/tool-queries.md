# Tool Queries

## Connector Availability

Check the available tool namespaces in the current session. A source is available when at least one matching namespace/tool family exists. Different platforms (Codex, Claude Code, etc.) expose different MCP tool namespaces.

Known tool families per source (use whichever is available):

- Slack: `mcp__codex_apps__slack`, `mcp__slack__`, or any `slack`-prefixed MCP tools
- GitHub: `mcp__codex_apps__github`, `mcp__github__`, or any `github`-prefixed MCP tools
- Linear: `mcp__codex_apps__linear_mcp_server`, `mcp__linear__`, or any `linear`-prefixed MCP tools
- Google Calendar: `mcp__codex_apps__google_calendar`, `mcp__google_calendar__`, or any `calendar`-prefixed MCP tools

When multiple tool families exist for the same source, prefer the one with richer functionality. If a tool namespace is not present, do not suggest installing unless the user explicitly asks for setup. Continue with available sources.

## Slack

Find the current user:

- Use the available Slack profile tool (e.g., `slack_read_user_profile`, `read_user_profile`, or equivalent) without `user_id`.
- If the result lacks a user ID, use the returned email/name with the user search tool (e.g., `slack_search_users`, `search_users`, or equivalent).

Collect activity for the target KST day:

- Use the available Slack search tool (e.g., `slack_search_public_and_private`, `search_messages`, or equivalent).
- Search messages with `from:<@USERID>` and date filters, for example `from:<@U123> after:2026-04-17 before:2026-04-18`.
- Use `content_types: "messages,files"`, `include_context: true`, and `sort: "timestamp"` when supported by the tool.
- If results are sparse or date filtering looks timezone-sensitive, broaden the query by one day on either side and manually keep only messages whose displayed timestamp falls on the target KST date.
- If a result is in a thread or looks important, call `slack_read_thread`.
- Search files separately with `from:<@USERID> has:file` for the same date range.
- Search the user's Sup DM and `#standup` when the user has already submitted a standup response. Sup prompts/responses may appear in DMs rather than in the public standup channel.

Important parsing rule:

- Slack standup/Sup bot messages often put content in legacy `attachments[]`, not top-level `text`.
- When using raw Slack API, parse:
  - `message.text`
  - `message.blocks`
  - `message.attachments[].pretext`
  - `message.attachments[].title`
  - `message.attachments[].text`
  - `message.attachments[].fields`
  - `message.attachments[].fallback`
  - `message.attachments[].blocks`
  - `message.files[]`

If the connector output hides attachments and the user provides a Slack bot token, direct API calls can use:

- `conversations.history`
- `conversations.replies`
- `users.info`
- `files.info` only when the token has `files:read`

Never print or persist user-provided tokens. Feed tokens through stdin or environment variables with shell echo disabled.

Final-output safety:

- Redact or omit cloud console, Secrets Manager, private channel/DM, and credential-related URLs from the standup draft.
- Keep the work item, for example "Clix console dev Auth0/management API env setup", instead of the sensitive link.
- Usually treat environment setup replies, access/invite help, deployment timeout comments, and simple confirmations as supporting context. Merge them into a broader initiative such as migration stabilization, deployment automation, or incident follow-up.
- File search may return metadata without readable bytes when `files:read` is missing. Mention the scope gap only in the coverage note when file contents would matter.

## GitHub

Find the current user:

- Use the available GitHub identity tool (e.g., `get_user_login`, `get_profile`, `get_me`, or equivalent) to resolve the authenticated user.

Collect activity for the target date:

- Pull requests:
  - Search `author:<login> updated:YYYY-MM-DD..YYYY-MM-DD` using the available PR search tool (e.g., `search_pull_requests`, `list_pull_requests`, or equivalent).
  - Search `commenter:<login> updated:YYYY-MM-DD..YYYY-MM-DD`.
  - Read key PRs for status, merged/open state, review comments, and changed files using the PR read tool (e.g., `pull_request_read`, `get_pull_request`, or equivalent).
  - Fetch detailed PR info for important PRs before deciding whether to list work as completed, merged, waiting for review, or carry-over.
- Issues:
  - Search `involves:<login> updated:YYYY-MM-DD..YYYY-MM-DD` using the available issue search tool (e.g., `search_issues`, `list_issues`, or equivalent).
  - Use issue comments when the issue appears to contain the user's work.
- Commits:
  - Use the available commit search or list tool (e.g., `search_code`, `list_commits`, or equivalent).
  - Query with `author:<login> author-date:YYYY-MM-DD..YYYY-MM-DD`.
  - If a local repo is relevant, `git log --author=<login> --since=<start> --until=<end>` can supplement connector results.
  - Treat merge commits as evidence that PRs landed, not as separate standalone work items unless the commit message itself describes distinct work.

Summarize GitHub activity by outcome:

- Merged/deployed PRs
- Open PRs awaiting review
- Review/comment activity
- Commits or branches that indicate unfinished work
- PR chains that implement one rollout, such as runtime baseline -> Lambda -> SES -> Route53, should usually become one concise standup bullet.

## Linear

Find the current user:

- Use the available Linear profile/identity tool (e.g., `get_profile`, `get_user` with `"me"`, or equivalent).
- Use `"me"` in supported list calls when a direct profile tool is not available.

Collect activity for the target date:

- If a research/search tool is available, try it first. If it returns a tool-not-found or dispatch error, stop retrying and fall back to structured tools.
- Use the issue list tool (e.g., `list_issues`) with `assignee: "me"` and `updatedAt` set to the target day start.
- Also search/fetch issue IDs discovered in GitHub PR bodies or Slack activity, even if `list_issues` returns no direct updates for the current user.
- Include created issues, completed issues, status changes, comments, blocked/related issues, and project updates.
- For candidate issues, call `get_issue` and `list_comments` when details are needed.
- If no direct Linear activity is found, report that Linear had no direct user-updated issues and use linked issues only as context.

Normalize Linear activity by:

- Issue identifier and title
- State transition
- Project/customer context
- Explicit blockers or dependencies

## Google Calendar

Find the current user and calendar:

- Use the available calendar profile tool (e.g., `get_profile`, or equivalent) when available.
- Use `primary` unless the user names another calendar.
- Use KST bounds for the target day, passed as full RFC3339 datetimes with explicit UTC offsets.

Collect events for the target KST day:

- Use the available event search/list tool (e.g., `search_events`, `list_events`, or equivalent) with `calendar_id: "primary"`, `time_min`, `time_max`, and `timezone_str: "Asia/Seoul"` (or equivalent parameters).
- Use an empty or broad query when the goal is a full-day activity scan.
- Page through bounded results if a `next_page_token` is returned.
- For important events, call `read_event` when the summary is insufficient or links/attendees clarify the work.

Use calendar results as context:

- Include customer calls, interviews, 1:1s, planning, product syncs, external meetings, and explicit focus blocks when they explain the day's work.
- Merge routine meetings into larger work bullets when Slack/GitHub/Linear evidence shows what was done.
- Avoid listing every meeting as a separate bullet. A calendar-heavy day can become one concise bullet such as "고객/파트너 미팅 및 1:1 진행".
- Do not expose private event links, meeting URLs, guest email lists, or sensitive descriptions in the final draft unless the user explicitly asks for detail.
- Calendar alone can support a meeting/activity bullet, but not a code/project deliverable claim.
