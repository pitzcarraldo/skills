# Standup Format

Use this format unless the user asks for a different style.

```md
오늘 컨디션(기분)이 어떤가요? How are you feeling today?
<short honest condition, if known; otherwise "good">

어제(지난 업무일) 무엇을 했나요? What did you work on yesterday?
- <completed or meaningfully progressed work>
- <include PR/issue references when useful>

오늘은 무엇을 할 건가요? What will you work on today?
- <planned continuation or next concrete work>
- <label inferred items only if the plan was not explicit>

작업을 방해/지연 시키는 것이 있나요? Are there any blockers?
<explicit blockers, or "없습니다.">
```

## Drafting Rules

- Write in Korean by default, preserving English product names and technical terms.
- Keep bullets short and paste-ready.
- When a Sup/Standup submission already exists for the activity date, preserve its condition and explicit submitted plan unless later source activity clearly supersedes it.
- Avoid overly broad buckets like "개발 업무" when source activity shows specific work.
- Use 3-6 bullets for yesterday when there is enough activity; use fewer when evidence is sparse.
- Use 2-5 bullets for today.
- Mention "추정" only for today's plan items inferred from open PRs/issues, not for observed past work.
- Put uncertainty in the coverage note, not inside every bullet.
- Do not include raw private links, cloud console links, Secrets Manager links, customer-sensitive details, or credential-related values in the draft.
- If many PRs belong to the same rollout, summarize the rollout and optionally include the most important PR numbers in parentheses.
- Exclude or merge simple conversations such as "confirmed", "shared a link", "answered which env var to use", "checked a deployment timeout", or "gave access/invitation guidance" unless that was the main deliverable.
- Prefer initiative-level bullets over chat-level bullets. For example, fold environment setup support into "Clix TypeScript migration/dev environment stabilization" instead of listing "Auth0 env var guidance" separately.
- Use Google Calendar to add meeting context, but avoid turning every event into a bullet. Merge product syncs, 1:1s, interviews, and customer calls into relevant work themes.
- Do not duplicate the same theme in both yesterday and today unless there is a clear next step.

## Coverage Note

After the standup draft, add a short note:

```md
확인한 소스: Slack, GitHub, Linear, Google Calendar
누락/제한: <missing connector, missing scope, sparse results, or "없음">
```

Omit the note only if the user explicitly asks for paste-only standup text.

## Source Handling Examples

- Existing Sup answers: use as the user's own baseline. Example: condition `So So`, yesterday `Finish Refactor Terraform Workflow`, today `Research Alert System Optimization / Keep, Deployment Setup`.
- Slack operational support: use as supporting evidence for larger initiatives. Example: fold "Clix console dev Auth0/management API env setup" into "Clix TypeScript migration/dev environment stabilization" unless the user explicitly wants detailed operational support items.
- GitHub merged PR chain: convert several linked PRs into one bullet. Example: "ops email receiver Lambda/SES/MX routing PR chain merge".
- Linear linked issue with no direct update: use it as context in the coverage note or supporting wording, not as a direct Linear activity claim.
- Google Calendar meetings: use them to support or add context. Example: fold "Weekly Product Sync" into product planning/work bullets, or summarize several calls as "고객/파트너 미팅 및 1:1 진행".
