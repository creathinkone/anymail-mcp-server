# anymail MCP server

Remote [Model Context Protocol](https://modelcontextprotocol.io) server for [anymail](https://anymail.watch), a cold email outreach tool. It lets an MCP client (Claude, Cursor, or anything that speaks Streamable HTTP) manage prospects, campaigns, replies, mailboxes and webhooks in your anymail workspace.

This repository is the public distribution of the anymail MCP server: the MCP Registry manifest, a Claude Code plugin and 6 guided skills. The server itself is hosted by anymail and its source is proprietary.

| | |
|---|---|
| Endpoint | `https://app.anymail.watch/api/mcp` |
| Transport | Streamable HTTP, stateless |
| Auth | `Authorization: Bearer <token>`, a workspace API token (anymail → Settings → Integrations → API tokens) |
| Scope | Exactly what the anymail REST API v1 allows: same validation, workspace isolation and rate limit |

## Install the Claude Code plugin

The plugin connects the MCP server and adds the skills below. It asks for your API token once and stores it as a sensitive plugin setting, not in a file in your project.

```
/plugin marketplace add creathinkone/anymail-mcp-server
/plugin install anymail@anymail
```

Or from the shell:

```bash
claude plugin install anymail --marketplace creathinkone/anymail-mcp-server
```

## Skills

Skills are optional: the MCP tools work on their own. The skills add guided workflows on top, with confirmation before anything sends email or cannot be undone.

| Skill | What it does |
|---|---|
| `anymail-campaign` | Checks mailboxes and domain health, picks the audience, drafts a 3-step sequence with an optional A/B test, sets the schedule. Starts sending only after you say so. |
| `anymail-replies` | Groups unread replies (interested, maybe later, not interested), fixes classifications with your OK, drafts answers and sends the ones you approve. |
| `anymail-report` | Funnel, reply rate, per-step and per-variant results, hot accounts, and at most three concrete changes. Read-only. |
| `anymail-import` | Turns a pasted list or CSV into prospects: maps fields, skips duplicates and bad rows, enrols in batches of up to 200. |
| `anymail-hygiene` | Blocks addresses or whole domains, checks SPF/DKIM/DMARC and mailbox limits, pauses campaigns, handles GDPR erasure. |
| `anymail-pipeline` | Runs a full outbound loop with other connected tools: find and enrich people (FullEnrich, Clay, Apollo...), import, launch, hand interested replies to your CRM. |

Ask in plain words, for example "review my replies" or "how is the Q4 campaign doing"; the matching skill loads by itself.

## Connect the MCP server only

Claude Code:

```bash
claude mcp add --transport http anymail https://app.anymail.watch/api/mcp \
  --header "Authorization: Bearer <token>"
```

Cursor (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "anymail": {
      "url": "https://app.anymail.watch/api/mcp",
      "headers": { "Authorization": "Bearer <token>" }
    }
  }
}
```

Full guide, other clients and the complete tool list: https://developers.anymail.watch/mcp-server/

## Tools

Read: `list_prospects`, `get_prospect`, `search_prospects`, `list_campaigns`, `get_campaign`, `get_campaign_stats`, `list_replies`, `list_inbox_messages`, `list_mailboxes`, `list_webhooks` and more.
Write: `create_prospect`, `create_campaign`, `start_campaign`, `pause_campaign`, `enrol_prospects`, `reply_to_message`, `classify_reply`, `create_webhook` and more.
Destructive tools (for example `delete_campaign`, `delete_prospect`) are marked with `destructiveHint`.

## Checking the skills

`scripts/check-tools.py` verifies that every tool a skill mentions exists on the server:

```bash
ANYMAIL_API_TOKEN=<token> python3 scripts/check-tools.py
```

## License

The files in this repository are MIT licensed.
