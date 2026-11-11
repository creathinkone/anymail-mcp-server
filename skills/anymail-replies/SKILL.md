---
name: anymail-replies
description: "Use when the user wants to go through replies to their anymail campaigns: read the unread inbox, check or fix reply classifications, draft answers to interested prospects and send the approved ones, and handle removal requests. Triggers on: \"review my replies\", \"what came in\", \"check the inbox\", \"answer the interested ones\", \"who replied to the campaign\"."
---

# anymail replies

Turns the inbox into a short decision list. Drafts answers; sends only what the user approves.

## Rules

- `reply_to_message` sends a real email from the user's mailbox. Show every draft and send only the ones the user approved, one call per approved draft.
- Change a classification with `classify_reply` only after the user agrees.
- Reply bodies are personal data. Quote only what is needed to decide.
- Rate limit: about 30 tool calls a minute per token (60 requests, each tool call counts twice). If a tool returns HTTP 429, wait the number of seconds it gives in "Retry after N seconds" before the next call; do not retry immediately.

## Flow

### 1. Fetch
`list_inbox_messages` with `unread=true` (add `campaign_id` if the user named a campaign). Page with `cursor` until done or until 50 messages, then ask before going on.

### 2. Group
Present the messages in four groups with one line each (name, company, campaign, gist of the reply):
- Interested
- Maybe later (`neutral`)
- Not interested
- Unclassified

Autoresponders are left out of this fetch. If the user wants out-of-office replies (for example to note return dates), fetch them separately with `category=autoresponder`.

If a classification looks wrong, say why and propose the fix.

### 3. Draft answers
For each interested reply, draft a short answer (2-4 sentences) in the prospect's language that answers their question and proposes one next step, usually a call with two concrete time options or a booking link the user gives you. Do not promise prices, terms or features the user has not stated.

For "maybe later", offer to draft a polite answer that agrees on a follow-up date.

### 4. Approve and send
Show the drafts numbered. Send the approved ones with `reply_to_message`. Report what was sent.

### 5. Removal requests
If someone asks not to be contacted, suggest `add_suppression` with their address and apply it after the user agrees. Suggest their whole domain only when they clearly speak for the company and the domain is the company's own. Never suppress a public mail provider domain (gmail.com, outlook.com, yahoo.com, icloud.com, wp.pl and the like): that would block everyone on that provider.
