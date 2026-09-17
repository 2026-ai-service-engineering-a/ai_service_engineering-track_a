# week09 AG-UI 이벤트 실측 기록

9주차 교안 4장 3절에 실린 이벤트 스트림과 `<StateDelta />`의 첫 두 항목이
나온 자리. 손으로 옮겨 적은 예시가 아니라 **`ag-ui-protocol` SDK로 띄운
엔드포인트에 붙어 받아 적은 것**이다.

## 어떻게 만드나

랩을 띄우고 붙는다. 처음 캡처는 랩이 생기기 전 최소 골격으로 떴지만, 지금은
`week09-report-copilot` v1.1이 직접 흘리는 것을 받아 적는다.

```sh
cd ../week09-report-copilot
docker compose up -d && docker compose exec api python -m scripts.load_data
curl -s -N -X POST localhost:8000/agent \
  -H 'accept: text/event-stream' -H 'content-type: application/json' \
  -d '{"thread_id":"t-demo","run_id":"r-001","state":{},
       "messages":[{"id":"m1","role":"user","content":"8월 박스오피스 리포트 국적별로 만들어줘"}],
       "tools":[],"context":[],"forwarded_props":{}}'
```

각본 대역으로 돌기 때문에 키가 없어도 같은 스트림이 나온다. 가짜인 것은
무엇을 부를지 정하는 판단 하나이고, 질의도 숫자도 상태 패치도 진짜다.

## 2026-09-17 실측

| | 값 |
| --- | --- |
| `ag-ui-protocol` | 0.1.22 |
| fastapi · pydantic | 0.141.1 · 2.13.5 |
| 이벤트 종류 (`EventType` 멤버) | **36** |
| 전송 | SSE (`text/event-stream`) |
| 한 실행이 흘린 이벤트 | 43 (리포트 요청 한 번) |
| 그중 모델 호출 | 8회 · $0.0096 |

교안이 이 캡처에 기대어 주장하는 것 넷이다.

- **프레임은 `data: {…}` 한 줄에 빈 줄 하나.** 3주차에 배운 SSE 그대로이고
  새 전송 규약이 아니다
- **선 위에서는 camelCase다.** 파이썬 필드는 `thread_id`인데 나갈 때
  `threadId`가 된다. 브라우저 콘솔에서 파이썬 이름으로 찾으면 없다
- **도구 인자도 조각으로 흐른다.** `TOOL_CALL_ARGS`가 두 프레임으로 나뉘어
  왔다. 모델이 JSON을 토큰 단위로 뱉기 때문이다
- **`STATE_DELTA`의 `delta`는 JSON Patch 배열이다.** `op`·`path`·`value`가
  그대로 들어간다. `/sections/-`는 배열 끝에 붙이라는 RFC 6902의 표기다

`<StateDelta />`가 쓰는 값도 여기서 나온다. 결론의 85.3%는 지어낸 수가 아니라
2026년 8월 실제 집계다. 미국 16,590,261명, 전체 19,451,487명이다.

교안 5장 3절의 크기 비교는 `examples/02_state_delta.py`가 찍은 것이다.

```plaintext
리포트 통째로 만들기   패치 3,770B vs 스냅샷 2,088B
차트 종류 바꾸기      패치    64B vs 스냅샷 2,087B
섹션 하나 빼기        패치    41B vs 스냅샷 1,562B
```

**첫 줄에서는 패치가 스냅샷보다 크다.** 숨기지 않고 교안에도 그대로 적었다.
패치가 값을 하는 것은 그다음부터다.

## `RunAgentInput`이 실어 오는 것

v1 챗 위젯과의 차이가 여기 있다. SDK에서 그대로 확인한 필드다.

| 필드 | 타입 | 필수 |
| --- | --- | --- |
| `thread_id` · `run_id` | str | 예 |
| `parent_run_id` | str? | 아니오 |
| **`state`** | Any | 아니오 |
| `messages` | list[Message] | 예 |
| **`tools`** | list[Tool] | 예 |
| `context` | list[Context] | 예 |
| `forwarded_props` | Any | 예 |
| `resume` | list[ResumeEntry]? | 아니오 |

`state`와 `tools`가 요청에 있다는 것이 교안 3장의 점선을 실선으로 바꾸는
자리다.

## 이벤트 36종의 갈래

| 갈래 | 멤버 |
| --- | --- |
| 수명주기 | `RUN_STARTED` · `RUN_FINISHED` · `RUN_ERROR` · `STEP_STARTED` · `STEP_FINISHED` |
| 텍스트 | `TEXT_MESSAGE_START` · `CONTENT` · `END` · `CHUNK` |
| 도구 | `TOOL_CALL_START` · `ARGS` · `END` · `CHUNK` · `RESULT` |
| 상태 | `STATE_SNAPSHOT` · `STATE_DELTA` · `MESSAGES_SNAPSHOT` |
| 추론 | `REASONING_*` 7종 · `THINKING_*` 5종(구판) |
| 진척 | `ACTIVITY_SNAPSHOT` · `ACTIVITY_DELTA` |
| 하위 에이전트 | `SUBAGENT_STARTED` · `SUBAGENT_FINISHED` · `SUBAGENT_ERROR` |
| 그 밖 | `RAW` · `CUSTOM` |

랩이 쓰는 것은 열두 종이다. **규격이 크다고 다 써야 하는 것은 아니다.**

## 다시 뜰 때 유의할 점

- **버전 핀을 박는다.** 이벤트가 늘고 필드가 붙는 중이다. 교안의 "36종"과
  이벤트 이름은 0.1.22 기준이고, 올리면 이 문서와 교안 4장 4절을 함께 고친다
- `THINKING_*`은 구판이고 `REASONING_*`으로 갈음됐다. 새로 쓸 때 고르지 않는다
- `EventEncoder(accept=...)`에 `Accept` 헤더를 그대로 넘긴다. 헤더가 없으면
  기본이 SSE다
- 캡처를 다시 뜨면 `messageId`와 `toolCallId`가 달라진다. 교안에 박힌 값은
  그 순간의 것이고, 값 자체에 뜻이 있지는 않다

## 프런트엔드 도구의 왕복

승인 카드는 루프를 멈춰 기다리지 않는다. **두 번 돈다.**

```plaintext
① "이 리포트 발행해줘"
   CUSTOM route=publish llm_calls=0
   TOOL_CALL_START  confirm_publish
   TOOL_CALL_ARGS   {"summary": "…", "sectionCount": 2, "period": "…"}
   TOOL_CALL_END
   RUN_FINISHED                     ← TOOL_CALL_RESULT가 없다

② forwardedProps.toolResult = {"name":"confirm_publish","value":"approved"}
   STATE_DELTA  replace /publishedAt "2026-09-17T03:41:15+00:00"
   TEXT_MESSAGE_CONTENT "발행했습니다. 섹션 2개가 …"
```

`TOOL_CALL_RESULT`가 오지 않는 것이 프런트엔드 도구의 표시다. 그 자리를
화면이 채운다. 두 요청 다 모델 호출은 0회다.
