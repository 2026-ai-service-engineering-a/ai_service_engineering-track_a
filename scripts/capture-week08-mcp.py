#!/usr/bin/env python3
"""돌고 있는 MCP 서버에 실제로 붙어 오간 JSON-RPC를 받아 적는다.

교안 5장의 `<McpTools />` 데이터다. 손으로 옮겨 적은 예시가 아니라
**컨테이너가 진짜로 돌려준 응답**이라 저장소가 바뀌면 다시 뽑아야 한다.

    docker compose up -d mcp            # week08-service-lab에서
    python3 scripts/capture-week08-mcp.py [저장소 경로] [서버 주소]

파이썬 원본은 `mcp_server/server.py`를 파싱해 데코레이터째로 잘라 온다.
스키마를 손으로 쓰지 않았다는 것이 5장 1절의 요지이므로, 왼쪽(코드)과
오른쪽(스키마)이 같은 순간의 같은 저장소에서 나와야 말이 된다.
"""

from __future__ import annotations

import ast
import json
import sys
import urllib.request
from pathlib import Path

REPO = Path(sys.argv[1] if len(sys.argv) > 1 else "../week08-service-lab").resolve()
URL = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8010/mcp"
OUT = Path(__file__).resolve().parent.parent / "site/src/data/week08-mcp.json"
SERVER = REPO / "mcp_server/server.py"

PROTOCOL = "2025-06-18"
CLIENT = {"name": "week08-doc-capture", "version": "0"}

# 도구마다 한 번씩 실제로 불러 본다. 인자는 교안에서 쓰는 것과 같게 둔다
CALLS = [
    ("plan_trip", {"question": "오사카 2박 3일 2명, 보통 스타일로", "max_steps": 4}),
    ("search_places", {"city": "오사카", "category": "관광"}),
    ("estimate_travel_time", {"from_area": "난바", "to_area": "우메다"}),
    ("calc_budget", {"nights": 2, "people": 2, "style": "보통", "include_flight": True}),
]

session: dict[str, str | None] = {"id": None}


def rpc(payload: dict, *, notify: bool = False):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session["id"]:
        req.add_header("mcp-session-id", session["id"])
    with urllib.request.urlopen(req, timeout=120) as r:
        sid = r.headers.get("mcp-session-id")
        if sid:
            session["id"] = sid
        raw = r.read().decode()
    if notify:
        return None
    for line in raw.splitlines():           # streamable HTTP는 SSE 한 프레임으로 온다
        if line.startswith("data: "):
            return json.loads(line[6:])
    return json.loads(raw) if raw.strip() else None


def sources() -> dict[str, dict]:
    """`@mcp.tool()`이 붙은 함수를 데코레이터째로 잘라 낸다."""
    text = SERVER.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: dict[str, dict] = {}
    for node in ast.parse(text).body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any("mcp.tool" in ast.unparse(d) for d in node.decorator_list):
            continue
        start = min(d.lineno for d in node.decorator_list) - 1
        body = "\n".join(lines[start:node.end_lineno])
        doc = ast.get_docstring(node) or ""
        out[node.name] = {"source": body, "line": start + 1, "doc": doc}
    return out


def main() -> None:
    init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": CLIENT,
    }}
    init_res = rpc(init_req)
    rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, notify=True)

    list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    list_res = rpc(list_req)
    listed = {t["name"]: t for t in list_res["result"]["tools"]}

    src = sources()
    tools = []
    for i, (name, args) in enumerate(CALLS, start=3):
        call_req = {"jsonrpc": "2.0", "id": i, "method": "tools/call",
                    "params": {"name": name, "arguments": args}}
        tools.append({
            "name": name,
            "line": src[name]["line"],
            "source": src[name]["source"],
            "listed": listed[name],
            "call": {"request": call_req, "response": rpc(call_req)},
        })

    data = {
        "file": "mcp_server/server.py",
        "server": init_res["result"]["serverInfo"],
        "protocol": init_res["result"]["protocolVersion"],
        "handshake": [
            {"request": init_req, "response": init_res},
            {"request": {"jsonrpc": "2.0", "method": "notifications/initialized"},
             "response": None},
            {"request": list_req, "response": list_res},
        ],
        "tools": tools,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"서버 {data['server']['name']} {data['server']['version']} · 프로토콜 {data['protocol']}")
    print(f"도구 {len(tools)} · {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}")


if __name__ == "__main__":
    main()
