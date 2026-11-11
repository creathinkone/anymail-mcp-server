---
name: anymail-campaign
description: "Use when the user wants to create, write or change a cold email campaign in anymail: pick sending mailboxes, choose the audience, write a 3-step sequence, add an A/B test, set the schedule and start it. Never starts sending without explicit approval. Triggers on: \"build a campaign\", \"new outreach sequence\", \"write a cold email sequence for...\", \"set up an A/B test\", \"start the campaign\", \"change the schedule\"."
---

# anymail campaign

Builds a campaign as a draft, shows it, and starts it only when the user says so. Uses the anymail MCP tools.

## Rules

- `start_campaign` sends real email to real people. Call it only after the user has seen the full sequence and the audience size, and said "start" (or an equivalent) in this conversation. Approval to draft is not approval to send.
- `stop_campaign` ends a campaign for good and cannot be undone. Call it only after the user confirms they want it ended, not paused. For a temporary halt use `pause_campaign`.
- `delete_campaign` (drafts only), `delete_step` and `delete_variant` are permanent. Confirm before calling them.
- Do not invent prospect data. A snippet such as `{{first_name}}` blocks `start_campaign` (409) if any enrolled prospect lacks the field. Give it a fallback, `{{first_name|there}}`, or use it only when every prospect has the field.
- Rate limit: about 30 tool calls a minute per token (60 requests, each tool call counts twice). If a tool returns HTTP 429, wait the number of seconds it gives in "Retry after N seconds" before the next call; do not retry immediately.

## Flow

### 1. Goal and audience
Ask in one message what the campaign offers, to whom, and in what tone, unless the user already said. Ask which language the emails should be in.

### 2. Sending setup
Call `list_mailboxes` and `list_domains`. Keep active mailboxes whose domain has SPF, DKIM and DMARC ok. If a domain is not ok, say what is missing and recommend fixing it before sending. Mention each mailbox's daily limit and how much it already sent today: limits are shared with every other campaign using the same mailbox, and the campaign's own `daily_enroll_limit` caps it further, so the sum of the limits is the most the campaign can get, not what it will get.

### 3. Audience
Find prospects with `search_prospects` or `list_prospects` (status `not_contacted` is a good default). There is no total count endpoint: lists come in pages of up to 100. Fetch at most 5 pages (500 people), show five example names and the number found, and say "at least N" if more pages remain. Ask before paging further for a very large audience. If the list must come from outside anymail, switch to the anymail-import skill first.

### 4. Draft
`create_campaign` with a descriptive name, `mailbox_ids` and `prospect_ids`.

Write the steps with `add_step`:
- Step 1: subject plus a short plain-text body (60-120 words), one clear ask.
- Steps 2 and 3: empty subject so they stay in the thread, `delay_days` 3 and 4, each shorter than the one before and adding something new, not "just following up".
- Plain text (`content_format` plain) unless the user asks for HTML.

Offer one A/B test on step 1 with `add_variant`. Test one thing at a time, usually the subject.

### 5. Schedule
Ask about sending hours and days if the user cares; otherwise the workspace schedule applies. Set them with `update_campaign` (`schedule`, `timezone`, `use_prospect_timezone`, `daily_enroll_limit`).

### 6. Review
Call `list_steps` and show the whole sequence, the mailboxes, the audience size and the schedule. Ask for changes; apply them with `update_step` or `update_variant`.

### 7. Start
Only after explicit approval: `start_campaign`. On 409, read the issues it returns (empty step, missing fields, prospects active elsewhere), explain them in plain words and propose a fix.

## Changing a running campaign
Steps and mailboxes can be edited only while the campaign is a draft or paused. Suggest `pause_campaign`, make the change, show it, then `resume_campaign` (or `start_campaign`) after approval.
