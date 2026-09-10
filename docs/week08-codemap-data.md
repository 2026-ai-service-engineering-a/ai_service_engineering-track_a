# week08 코드 지도 데이터

`<CodeMap />`(8주차 3장 4절). `week08-service-lab`의 심볼과 호출 관계를 손으로
적지 않고 **저장소를 파싱해** 만든 기록이다.

## 어떻게 만드나

```sh
python3 scripts/build-week08-codemap.py ../week08-service-lab
# → site/src/data/week08-codemap.json
```

읽는 것은 `core/` · `api/` · `mcp_server/` · `clients/py_client.py`이고
`tests/`와 `__init__.py`는 뺀다. `ast`로 파싱해 다음을 뽑는다.

- **심볼**: 클래스·데이터클래스·함수·메서드. 데코레이터를 보고 FastAPI
  라우트(`@app.post`)와 MCP 도구(`@mcp.tool`)를 따로 표시한다
- **시그니처·줄 번호·docstring 첫 줄**
- **호출**: 함수 본문의 `Call` 노드를 import 표(`from core import service` 등)로
  풀어 저장소 안의 심볼로 이어지는 것만 남긴다

## 2026-09-10 실측

| | 수 |
| --- | --- |
| 모듈 | 13 |
| 심볼 | 60 (함수 29 · 클래스 12 · 메서드 6 · 라우트 6 · MCP 도구 4 · 데이터클래스 3) |
| 호출 | 45 |

교안이 이 데이터에 기대어 주장하는 것 넷이다. 다시 뜰 때 이 넷이 그대로인지
확인한다.

- `core.service:plan`을 부르는 곳이 셋이다 (`api.main:plan` ·
  `api.main:plan_blocking` · `mcp_server.server:plan_trip`)
- `core.service:plan_events`를 부르는 곳이 둘이다 (`plan` · `plan_stream`)
- **코어의 어느 심볼도 `api`나 `mcp_server`를 부르지 않는다.** import 방향이
  한쪽이라는 증거다
- 코어에서 모델로 나가는 길은 `core.llm:completion` 하나다

## 다시 뜰 때 유의할 점

- 호출 해석은 정적이다. 변수에 담아 부르거나 동적으로 부르는 호출은 놓친다.
  8주차 저장소는 그런 호출을 쓰지 않는다
- 저장소 경로가 인자다. 기본값은 `../week08-service-lab`
- 심볼 수가 크게 바뀌면 교안 3장 4절의 문장(위 넷)도 함께 확인한다
