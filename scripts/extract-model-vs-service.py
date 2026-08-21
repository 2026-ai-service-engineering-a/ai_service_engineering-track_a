"""<ModelVsService /> 데이터 추출 — 같은 질문을 두 번, 도구 없이와 도구를 쥐여주고.

  cd week05-agent-lab && docker compose up -d
  docker compose exec -T lab python - < …/scripts/extract-model-vs-service.py > mvs.json

질문 하나를 두 방식으로 실제 호출한다.
  ① 도구 없이: 채팅만 붙인 모델. messages 하나 보내고 답을 받는다
  ② 도구를 쥐여주고: tools를 실어 보내고, 모델이 요청하면 실행해 되돌려준다

도구 구현은 목데이터다(실제 기상청을 부르지 않는다). 이 데모가 보이려는 것은
값이 아니라 구조이고, **모델의 응답은 전부 실제 호출 결과**다. 산수 질문은
정답을 코드로 계산해 두 답을 각각 채점한다.
"""

import json
import sys
from datetime import datetime

from litellm import completion

from agent.config import pick_model

# ── 목데이터 도구 ────────────────────────────────────────────────────
# 결정적이라 다시 뽑아도 같은 값이 나온다. 실제 API를 부르지 않는다.
WEATHER = {"서울": {"sky": "흐림", "temp_c": 24, "rain_prob": 60}}
NOW = "2026-08-21T14:35:00+09:00"
FILES = ["agent/", "examples/", "tests/", "README.md", "docker-compose.yml"]


def get_weather(city: str) -> dict:
    w = WEATHER.get(city)
    if not w:
        return {"error": f"지원하지 않는 도시: {city}. 지원 목록: {list(WEATHER)}"}
    return {"city": city, **w}


def get_current_time(timezone: str = "Asia/Seoul") -> dict:
    return {"timezone": timezone, "now": NOW}


def calculator(expression: str) -> dict:
    allowed = set("0123456789+-*/(). ")
    if set(expression) - allowed:
        return {"error": f"허용되지 않는 문자: {expression}"}
    return {"expression": expression, "result": eval(expression)}  # noqa: S307


def list_files(path: str = ".") -> dict:
    return {"path": path, "entries": FILES, "count": len(FILES)}


REGISTRY = {
    "get_weather": get_weather,
    "get_current_time": get_current_time,
    "calculator": calculator,
    "list_files": list_files,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "도시의 현재 날씨(하늘 상태·기온·강수확률)를 조회한다.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "도시 이름"}},
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "현재 시각을 ISO 8601 형식으로 조회한다.",
            "parameters": {
                "type": "object",
                "properties": {"timezone": {"type": "string", "description": "IANA 시간대"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "사칙연산 식을 정확히 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "예: 3847*29183"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "경로 아래의 파일·디렉터리 목록을 읽는다.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "조회할 경로"}},
            },
        },
    },
]

# ── 질문 ────────────────────────────────────────────────────────────
# hole: 이 질문이 드러내는 구멍. tool 없이 답할 수 없는 이유의 종류다.
QUESTIONS = [
    {
        "id": "weather",
        "hole": "지식",
        "q": "오늘 서울 날씨 어때? 우산 챙겨야 해?",
        "why": "학습이 끝난 시점 이후의 일은 모델 안에 없다",
    },
    {
        "id": "time",
        "hole": "지식",
        "q": "지금 몇 시야?",
        "why": "모델에는 시계가 없다",
    },
    {
        "id": "math",
        "hole": "정확성",
        "q": "3847 곱하기 29183은 얼마야? 숫자만 답해줘.",
        "why": "모델의 산수는 계산이 아니라 그럴듯한 확률이다",
        "truth": str(3847 * 29183),
    },
    {
        "id": "files",
        "hole": "행동",
        "q": "지금 이 폴더에 뭐가 들어 있어?",
        "why": "모델은 내 컴퓨터를 보지 못한다",
    },
    {
        "id": "plan",
        "hole": "없음",
        "q": "오사카 3박 4일 여행에서 꼭 가볼 곳 두 군데만 알려줘.",
        "why": "학습된 일반 지식으로 충분한 질문. 모든 것에 도구가 필요하지는 않다",
    },
]

SYSTEM = "당신은 사용자를 돕는 어시스턴트입니다. 간결하게 답하세요."


def ask_plain(model: str, question: str) -> str:
    """① 도구 없이 — 채팅만 붙인 모델."""
    resp = completion(
        model=model,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}],
    )
    return (resp.choices[0].message.content or "").strip()


def ask_with_tools(model: str, question: str) -> tuple[str, list[dict]]:
    """② 도구를 쥐여주고 — 요청이 오면 실행해 되돌려준다 (왕복 1회)."""
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    resp = completion(model=model, messages=messages, tools=TOOLS)
    message = resp.choices[0].message
    calls = []

    if message.tool_calls:
        messages.append(message.model_dump())
        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = REGISTRY[name](**args) if name in REGISTRY else {"error": f"미등록 도구: {name}"}
            calls.append({"name": name, "args": args, "result": result})
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )
        resp = completion(model=model, messages=messages, tools=TOOLS)
        message = resp.choices[0].message

    return (message.content or "").strip(), calls


def main() -> int:
    model = pick_model()
    out = {
        "model": model,
        "measuredAt": datetime.now().strftime("%Y-%m-%d"),
        "mockNote": "도구 구현은 목데이터다. 모델의 응답은 전부 실제 호출 결과다.",
        "questions": [],
    }

    for item in QUESTIONS:
        print(f"[{item['id']}] 도구 없이…", file=sys.stderr)
        plain = ask_plain(model, item["q"])
        print(f"[{item['id']}] 도구 쥐여주고…", file=sys.stderr)
        tooled, calls = ask_with_tools(model, item["q"])

        row = {
            "id": item["id"],
            "hole": item["hole"],
            "q": item["q"],
            "why": item["why"],
            "plain": {"answer": plain},
            "tooled": {"answer": tooled, "calls": calls},
        }
        if "truth" in item:
            row["truth"] = item["truth"]
            row["plain"]["correct"] = item["truth"] in plain.replace(",", "")
            row["tooled"]["correct"] = item["truth"] in tooled.replace(",", "")
        out["questions"].append(row)

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print(file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
