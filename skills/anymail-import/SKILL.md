---
name: anymail-import
description: "Use when the user gives a list of contacts (pasted text, a CSV or spreadsheet file, an email signature, notes) and wants them added to anymail as prospects, optionally enrolled into a campaign. Maps columns, skips duplicates and bad rows, creates prospects one by one within the rate limit, enrols in batches and reports the result. Triggers on: \"import these contacts\", \"add these leads to anymail\", \"upload this CSV\", \"put these people in the campaign\", \"add prospect\"."
---

# anymail import

Gets contacts into anymail cleanly. Nothing is emailed by this skill: enrolling into a draft only prepares the audience, and enrolling into an active campaign is confirmed first.

## Rules

- Never guess an email address. Rows without one are skipped and listed.
- Confirm the column mapping before the first write.
- Enrolling into an **active** campaign means those people start receiving email. Ask before doing it.
- Rate limit: about 30 tool calls a minute per token (60 requests, each tool call counts twice). If a tool returns HTTP 429, wait the number of seconds it gives in "Retry after N seconds" before the next call; do not retry immediately. `create_prospect` is one call per person, so a list of 300 takes over 10 minutes: say so up front and report progress.

## Flow

### 1. Read and map
Read the list. Map columns to prospect fields:
- `email` (required)
- `first_name`, `last_name` (split a full-name column if needed)
- `company_name` when the list has a company column (it matters most for people on gmail.com and other public providers, who are otherwise not grouped under a company); never derive it yourself
- `timezone` (IANA, e.g. `Europe/Warsaw`) only from an explicit timezone column, or after the user confirms a mapping; a country is not enough (the US, Canada, Brazil or Australia span several zones) and the timezone decides send windows
- everything else useful goes to `custom_fields` as flat strings, numbers or booleans, with short snake_case keys, because campaign copy reads them as `{{key}}`. Do not use the built-in names `email`, `first_name`, `last_name`, `company`, `full_name`, `tags` or `unsubscribe_url` as keys: built-ins win and the custom value would never show (use e.g. `company_size`, `job_title`)

Show the mapping and the first five rows as they will be sent. List rows that will be skipped: no email, malformed email, duplicates inside the file.

### 2. Target campaign (optional)
If the user wants the people in a campaign, find it with `list_campaigns` and confirm its name and status.

### 3. Create
Call `create_prospect` per row. When the target campaign is a draft, pass `campaign_id` to create and enrol in one call.

HTTP 409 on `create_prospect` means the address already exists in the workspace. That is not a failure: note the email, and enrol it in step 4 by email (no lookup needed).

### 4. Enrol existing people
For people that already existed, or when the campaign is active (after approval), use `enrol_prospects` with up to 200 `emails` (or `prospect_ids`) per call. It reports per person who was skipped and why (already enrolled, suppressed, active in another campaign, missing snippet fields).

### 5. Report
Created, already existed, enrolled, skipped with reasons. If people were skipped for missing snippet fields, name the fields so the user can fill them or change the copy.

## Updating people
`update_prospect` replaces the full record: send every field you want to keep, because omitted names, timezone and custom fields are cleared. Read the person with `get_prospect` first.
