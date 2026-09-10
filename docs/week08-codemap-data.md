# week08 코드 지도 데이터

`<SymbolMap />`이 읽는 데이터. `week08-service-lab`의 심볼과 관계를 손으로
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
- **`ai`**: 그 함수 본문이 litellm의 completion을 부른다. 값만 계산하는
  `completion_cost`는 이름을 좁혀 걸러낸다
- **`reaches`**: 부르다 보면 그 자리에 닿는다 (`call`·`construct`만 따라간다)
- **호출**: 함수 본문의 `Call` 노드를 import 표(`from core import service` 등)로
  풀어 저장소 안의 심볼로 이어지는 것만 남긴다

## 2026-09-10 실측

| | 수 |
| --- | --- |
| 모듈 | 13 |
| 심볼 | 61 (함수 30 · 클래스 12 · 메서드 6 · 라우트 6 · MCP 도구 4 · 데이터클래스 3) |
| 관계 | 63 (호출 35 · 사용 13 · 파라미터 8 · 리턴 5 · 상속 2) |
| `ai` | 1 (`core.llm:completion`) |
| `reaches` | 9 |

관계는 다섯 종류로 나눈다: `call`(호출) · `construct`(사용) · `returns`(리턴) ·
`param`(파라미터) · `inherits`(상속)

교안이 이 데이터에 기대어 주장하는 것 넷이다. 다시 뜰 때 이 넷이 그대로인지
확인한다.

- `core.service:plan`을 부르는 곳이 셋이다 (`api.main:plan` ·
  `api.main:plan_blocking` · `mcp_server.server:plan_trip`)
- `core.service:plan_events`를 부르는 곳이 둘이다 (`plan` · `plan_stream`)
- **코어의 어느 심볼도 `api`나 `mcp_server`를 부르지 않는다.** import 방향이
  한쪽이라는 증거다
- 코어에서 모델로 나가는 길은 `core.llm:completion` 하나다

## 지도의 AI 배지

배지는 데이터에 그대로 들어 있지 않다. `<SymbolMap />`이 그림마다 계산한다.
그림에 그려진 심볼 중 `reaches`인 것을 모으고, 그중 **같은 그림 안에 더 깊은
다음 단이 없는 것**에만 붙인다. 그래서 같은 심볼이라도 그림에 따라 배지가
붙기도 하고 안 붙기도 한다.

| 지도 | 배지가 붙는 심볼 |
| --- | --- |
| `core.service` (3장 1절) | `core.react:run_iter` |
| `core.llm` (3장 1절) | `core.llm:completion` |
| `api.errors` · `core.errors` (4장 3절) | 없음 |
| `mcp_server.server` (5장 2절) | `core.service:plan` |

## 다시 뜰 때 유의할 점

- 호출 해석은 정적이다. 변수에 담아 부르거나 동적으로 부르는 호출은 놓친다.
  8주차 저장소는 그런 호출을 쓰지 않는다
- 저장소 경로가 인자다. 기본값은 `../week08-service-lab`
- 심볼 수가 크게 바뀌면 교안 3장의 문장(위 넷)도 함께 확인한다
- **`ai`가 둘 이상이면 그 자체가 신호다.** 모델로 나가는 길이 하나라는 8주차의
  주장이 깨진 것이므로, 교안을 고치기 전에 저장소를 먼저 본다
