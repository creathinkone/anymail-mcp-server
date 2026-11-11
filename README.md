# anymail MCP server

Remote [Model Context Protocol](https://modelcontextprotocol.io) server for [anymail](https://anymail.watch), a cold email outreach tool. It lets an MCP client (Claude, Cursor, or anything that speaks Streamable HTTP) manage prospects, campaigns, replies, mailboxes and webhooks in your anymail workspace.

**This repository holds the registry manifest and documentation only.** The server is hosted by anymail and its source is proprietary.

| | |
|---|---|
| Endpoint | `https://app.anymail.watch/api/mcp` |
| Transport | Streamable HTTP, stateless |
| Auth | `Authorization: Bearer <token>`, a workspace API token (anymail → Settings → Integrations → API tokens) |
| Scope | Exactly what the anymail REST API v1 allows: same validation, workspace isolation and rate limit |

## Connect

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

## License

The files in this repository are MIT licensed.
