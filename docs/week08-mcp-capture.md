# week08 MCP 실측 기록

교안 5장의 `<McpTools />`가 읽는 데이터. **돌고 있는 MCP 서버에 실제로 붙어**
오간 JSON-RPC를 그대로 받아 적은 것이다. 손으로 옮긴 예시가 아니다.

## 어떻게 만드나

```sh
cd ../week08-service-lab
LLM_MODE=offline docker compose up -d --force-recreate mcp   # 각본 대역으로
cd -
python3 scripts/capture-week08-mcp.py ../week08-service-lab http://localhost:8010/mcp
# → site/src/data/week08-mcp.json
```

`LLM_MODE=offline`으로 뜨는 이유가 있다. 5장은 게이트웨이를 켜기 전(8장 이전)
자리이고, 수강생이 그 시점에 보는 것과 같은 응답이어야 한다. 키가 걸린 채로
뜬 컨테이너에 붙으면 `tools/call` 결과가 에러 문자열로 박힌다.

받아 적는 것은 셋이다.

- **`initialize`**: 서버 이름·버전·프로토콜 버전
- **`tools/list`**: 도구 넷의 이름·설명·`inputSchema`
- **`tools/call`**: 도구마다 한 번씩, 요청과 응답 그대로

파이썬 원본은 서버에 묻지 않고 `mcp_server/server.py`를 `ast`로 파싱해
데코레이터째로 잘라 온다. 왼쪽(코드)과 오른쪽(스키마)이 같은 순간의 같은
저장소에서 나와야 "손으로 쓴 스키마가 없다"는 5장의 주장이 성립한다.

## 2026-09-10 실측

| | 값 |
| --- | --- |
| 서버 | `travel-planner` 1.30.0 |
| 프로토콜 | `2025-06-18` |
| 도구 | 4 (`plan_trip` · `search_places` · `estimate_travel_time` · `calc_budget`) |
| 전송 | streamable HTTP, `http://localhost:8010/mcp` |

교안이 이 데이터에 기대어 주장하는 것 셋이다.

- 스키마를 손으로 쓴 곳이 한 군데도 없다. `inputSchema`의 `properties` ·
  `required` · `default`가 전부 시그니처에서 나온다
- **docstring이 통째로 `description`이 된다.** 첫 줄만이 아니다.
  `plan_trip`의 `예: "오사카 2박 3일 2명, 보통 스타일로"`까지 모델이 읽는다
- `plan_trip` 한 번의 응답에 `usage.llm_calls`가 들어 있다. 통째로 내어놓으면
  그 비용이 우리 지갑에서 나간다는 5장 2절의 근거다

## 다시 뜰 때 유의할 점

- 컨테이너가 떠 있어야 한다. 꺼져 있으면 연결 거부로 끝난다
- `mcp` 컨테이너를 다시 만든 뒤에 돌린다. 옛 컨테이너는 옛 환경변수를 쥐고 있다
- 캡처가 끝나면 `docker compose up -d --force-recreate mcp`로 되돌린다
- 서버 버전이 바뀌면 `serverInfo.version`과 프로토콜 날짜가 함께 바뀐다.
  교안 본문에는 두 값을 적지 않고 위젯이 데이터에서 읽어 보여 준다
