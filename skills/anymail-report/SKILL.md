---
name: anymail-report
description: "Use when the user asks how an anymail campaign or the whole outreach is doing: totals, funnel, reply rate, per-step and per-variant (A/B) results, and what to change. Read-only. Triggers on: \"how is the campaign doing\", \"campaign report\", \"which variant wins\", \"compare my campaigns\", \"weekly outreach summary\", \"which accounts are hot\"."
---

# anymail report

Read-only analysis. Read-only access is enough.

## Flow

### 1. Pick the scope
If the user did not name a campaign, call `list_campaigns` (status `active` first) and ask which one, or offer a summary of active campaigns. Each campaign costs at least one call; for more than 10 campaigns, ask which ones matter or summarise the 10 most recent.

Rate limit: about 30 tool calls a minute per token (60 requests, each tool call counts twice). If a tool returns HTTP 429, wait the number of seconds it gives in "Retry after N seconds" before the next call; do not retry immediately.

### 2. Collect
For each campaign: `get_campaign_stats` (totals, funnel, per step, per variant). Add `get_campaign` only when settings matter (mailboxes, schedule, status details); its totals repeat the stats.

### 3. Report
Keep it short. In this order:
- Status and age of the campaign, mailboxes used.
- Funnel: contacted, delivered, replied, reply rate, interested / maybe later / not interested.
- Problems: bounce rate and unsubscribes. anymail's Bounce shield pauses a campaign when bounces cross its threshold (5% by default, set per campaign), so a rising bounce rate is worth flagging well before that: it points to list quality or a domain problem.
- Per step: which step produces replies and where people drop off.
- Per variant: which one leads, and whether the sample is too small to call. With fewer than about 100 delivered per variant, say it is too early.
- Opens and clicks are weak signals (privacy proxies inflate opens; they are null when tracking is off). Do not base recommendations on opens alone.

End with at most three concrete changes (copy, timing, audience, mailboxes) and why each should help.

### Accounts
For "who is hot", call `list_companies` with `temperature=hot` (then `warm`) and `get_company` for the top few. Temperature fades as events age, so describe it as recent engagement, not intent.

### Several campaigns
When comparing, put the same numbers side by side and point out the one difference that most likely explains the gap. Do not rank campaigns with very different audiences as if they were comparable.
