---
name: anymail-pipeline
description: "Use when the user wants an end-to-end outbound run that combines anymail with another connected tool: find or enrich people in a data tool (FullEnrich, Clay, Apollo or similar MCP), bring them into anymail, launch a campaign, and later push interested replies to a CRM. Triggers on: \"find leads and email them\", \"from Clay to anymail\", \"enrich and launch\", \"prospect and send a sequence\", \"send interested replies to my CRM\"."
---

# anymail pipeline

Orchestrates anymail with other MCP servers the user has connected. The anymail MCP server does not search for new people or write to CRMs, so in a conversation those steps run through the other connectors, and each one keeps its own costs and confirmations.

The anymail app itself has built-in integrations (for example lead search from Apollo, FullEnrich or Hunter straight into campaigns, and CRM automations such as creating a deal when a reply is marked interested). They are set up in the app, not through MCP. Ask the user whether they use them: if a CRM automation is on, do not also create CRM records by hand, or the deals will be duplicated.

## Before starting
Check which connectors are available. If no data tool is connected, say so and offer to work from a list the user provides (the anymail-import skill). Do not pretend a step ran.

## Flow

### 1. Define the target
Agree on the audience (roles, company size, industry, region), the number of people and the offer. State it back in two lines.

### 2. Find and enrich (other connector)
Use the data tool's own search and enrichment. If it costs credits, give its estimate and get approval before spending, following that tool's rules. Keep only contacts with a verified work email.

### 3. Exclude before importing
Suppressed addresses and domains need no pre-check: `enrol_prospects` and `start_campaign` skip them and report who was skipped. If a CRM is connected and the user wants it, drop existing customers and people in open deals before importing.

### 4. Import into anymail
Follow the anymail-import skill: map fields (put the enrichment data that personalises the copy into `custom_fields`), `create_prospect`, handle 409 as already existing.

### 5. Campaign
Follow the anymail-campaign skill to draft, review and, only with explicit approval, `start_campaign`.

### 6. Hand-off to CRM (optional)
After replies arrive, use the anymail-replies skill. If no anymail CRM automation covers it, create or update the person and deal for interested people through the CRM connector, after the user confirms field mapping and you check for duplicates. For an automatic flow instead, `create_webhook` on `positive_reply` can notify the user's own endpoint or automation tool.

## Report
At the end: how many found, enriched, excluded, imported, enrolled, and what is waiting on the user (approval to start, replies to review).
