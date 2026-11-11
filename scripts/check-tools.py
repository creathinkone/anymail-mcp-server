#!/usr/bin/env python3
"""Check that every tool name the skills mention exists on the anymail MCP server.

Usage:
  ANYMAIL_API_TOKEN=... python3 scripts/check-tools.py      # against the live tools/list
  python3 scripts/check-tools.py names.txt                  # against a file, one tool name per line
"""
import json, os, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERBS = r"(?:list|get|create|update|delete|add|start|stop|pause|resume|enrol|classify|reply|search)"
MENTION = re.compile(rf"`({VERBS}_[a-z_]+)`")

def live_tools():
    req = urllib.request.Request(
        "https://app.anymail.watch/api/mcp",
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode(),
        headers={
            "Authorization": "Bearer " + os.environ["ANYMAIL_API_TOKEN"],
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return {t["name"] for t in json.load(r)["result"]["tools"]}

known = set(pathlib.Path(sys.argv[1]).read_text().split()) if len(sys.argv) > 1 else live_tools()
missing = {}
for skill in sorted(ROOT.glob("skills/*/SKILL.md")):
    for name in set(MENTION.findall(skill.read_text())) - known:
        missing.setdefault(name, []).append(skill.parent.name)
for name, skills in sorted(missing.items()):
    print(f"MISSING {name}: {', '.join(skills)}")
print(f"{len(known)} tools known, {len(missing)} missing")
sys.exit(1 if missing else 0)
