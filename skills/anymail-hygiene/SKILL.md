---
name: anymail-hygiene
description: "Use when the user wants to keep anymail sending safe and compliant: block an address or a whole domain, review or lift exclusions, pause campaigns when something looks wrong, check mailbox and domain health (SPF, DKIM, DMARC, daily limits), or handle a GDPR erasure request. Triggers on: \"don't email this company\", \"block this domain\", \"unsubscribe this person\", \"check my domains\", \"pause everything\", \"delete this person's data\", \"GDPR request\"."
---

# anymail hygiene

Exclusions, health checks and erasure. Several actions here cannot be undone or restart sending, so each one is confirmed.

- Rate limit: about 30 tool calls a minute per token (60 requests, each tool call counts twice). If a tool returns HTTP 429, wait the number of seconds it gives in "Retry after N seconds" before the next call; do not retry immediately.

## Exclude
- `add_suppression` takes an email address (`jane@acme.com`) or a bare domain (`acme.com`). A domain blocks everyone at that company, in every campaign, from the next send attempt. Never suppress a public mail provider domain (gmail.com, outlook.com, yahoo.com, icloud.com, wp.pl and the like); suppress the single address instead.
- HTTP 409 with `code: "duplicate"` means it was already excluded. Report it as done.
- Review exclusions with `list_suppressions` (`kind` email or domain). It has no search, so finding one entry means paging (100 per page); entries on anymail's global list are not shown and cannot be lifted.
- Lifting one with `delete_suppression` (by id) makes the person reachable again: confirm first, and ask why if the address came from an unsubscribe.

## Health check
1. `list_mailboxes`: status, daily limit, sent today and domain health for every mailbox in one call.
2. `list_domains` for the per-domain view of SPF, DKIM and DMARC if needed.
3. Report in plain words what is not ok and what to fix in DNS. A brand new mailbox should start with a low daily limit and grow over a few weeks.
4. Change a mailbox's `daily_limit`, `from_name` or `active` with `update_mailbox` after the user agrees. The current signature cannot be read through the API, so change `signature` only when the user gives the complete new text.

## Something looks wrong
If bounces or complaints spike, or the user is unsure about a list, `pause_campaign` stops new sends and keeps everyone in place. `resume_campaign` restarts sending real email: call it only after the user approves. Prefer pausing over `stop_campaign`, which ends a campaign for good and needs explicit confirmation.

## GDPR erasure
For "delete my data" requests: find the person by exact address with `list_prospects` (`email=`), not a substring search, show who it is, and after explicit confirmation call `delete_prospect` with `mode=anonymize`. Always pass `mode` explicitly: without it the call defaults to `delete`. That wipes personal data, puts the address on the suppression list so it is never emailed again, stops active enrollments and is audited. `mode=delete` removes the record without suppressing the address, so a later import could email them again; use it only for test data, and confirm it like anonymize. Both are irreversible.

## Notifications
To get events elsewhere (bounces, unsubscribes, positive replies), `create_webhook` subscribes a public HTTPS URL to one event; `list_webhooks` lists them; `delete_webhook` stops deliveries at once, so confirm before calling it.
