// @ts-check
/**
 * `[[용어]]` 위키링크의 중앙 용어집. 본문 어디서든 `[[llm]]`, `[[rag|RAG]]`처럼
 * 참조하면 빌드 시 해당 항목으로 링크된다 — 등록되지 않은 용어는 빌드가
 * 실패한다(의도된 동작). 항목 형태:
 *  - { label, def }              — 정의만 있는 용어 (용어집 페이지에 표시)
 *  - { label, concept: '<slug>' } — 개념 문서로 연결
 *  - { label, article: '<slug>' } — 글로 연결
 *  - { label, href }             — 외부 링크
 */
export const glossary = {
  llm: {
    label: 'LLM',
    def: '대량의 텍스트로 사전학습된 대형 언어 모델. 이 과정에서는 API 호출과 로컬 실행(Ollama 등) 양쪽으로 다룬다.',
  },
  rag: {
    label: 'RAG',
    concept: 'rag',
  },
  embedding: {
    label: '임베딩',
    def: '텍스트 등 데이터를 의미가 보존되는 고정 길이 숫자 벡터로 바꾼 표현. 유사도 검색의 기반이 된다.',
  },
  'vector-db': {
    label: '벡터 DB',
    def: '임베딩 벡터를 저장하고 유사도 검색을 제공하는 데이터베이스 — Chroma, Qdrant, pgvector 등.',
  },
  'structured-output': {
    label: 'Structured Output',
    def: 'LLM 응답을 JSON 스키마 등 정해진 구조로 강제해 받는 기법. 서비스 코드와 LLM을 안전하게 잇는 기본기.',
  },
  agent: {
    label: '에이전트',
    def: '도구를 부를지, 몇 번 부를지, 언제 멈출지를 모델이 스스로 결정하며 목표를 향해 반복하는 시스템. 모델 하나가 아니라 제어 루프·도구·데이터를 조립한 결과물이다.',
  },
  'prompt-engineering': {
    label: '프롬프트 엔지니어링',
    def: '모델에 줄 지시를 설계하는 일 — "무엇을 시킬 것인가". 엔지니어링 사다리의 1단.',
  },
  'context-engineering': {
    label: '컨텍스트 엔지니어링',
    def: '모델이 무엇을 언제 보는가를 설계하는 일 — retrieval, 메모리, 컨텍스트 조립. 엔지니어링 사다리의 2단.',
  },
  'harness-engineering': {
    label: '하네스 엔지니어링',
    def: '모델을 돌리는 기계 전체를 설계하는 일 — 제어 루프, 도구, 가드레일, 검증. 엔지니어링 사다리의 3단.',
  },
  guardrail: {
    label: '가드레일',
    def: '확률적인 모델 출력을 결정적인 코드로 보정·제한하는 장치. 예: 메뉴판 요청이면 모델이 도구를 건너뛰어도 메뉴판 표를 띄우는 폴백.',
  },
  'prompt-injection': {
    label: '프롬프트 인젝션',
    def: '입력(메시지나 문서)에 지시를 심어 모델이 원래 지시를 어기게 만드는 공격. 실질적인 방어는 프롬프트가 아니라 좁은 도구 권한과 결정적 코드 경계에서 나온다.',
  },
  litellm: {
    label: 'LiteLLM',
    def: '여러 LLM 프로바이더를 하나의 호출 인터페이스로 추상화하는 오픈소스 라이브러리. 모델 문자열만 바꾸면 코드 수정 없이 프로바이더가 교체된다.',
  },
  docker: {
    label: 'Docker',
    def: '애플리케이션을 실행 환경째 이미지로 묶어, 어느 컴퓨터에서든 같은 컨테이너로 실행하는 도구. "내 컴퓨터에서는 됐는데"를 없앤다.',
  },
  'docker-compose': {
    label: 'Docker Compose',
    def: '컨테이너 실행에 필요한 포트·볼륨·환경변수 설정을 compose.yml 파일 하나로 선언하고, docker compose up 한 번으로 띄우는 도구.',
  },
  'tool-calling': {
    label: 'Tool calling',
    def: '모델이 "이 함수를 이런 인자로 실행해 달라"는 요청을 구조화된 JSON으로 내놓고, 실행 결과를 다시 받아 답을 잇는 방식. 에이전트가 바깥 세계와 닿는 유일한 통로다.',
  },
  react: {
    label: 'ReAct',
    def: 'reasoning(다음 행동 판단) → action(도구 호출) → observation(결과 관찰)을 종료 조건까지 반복하는 가장 기본적인 에이전트 루프.',
  },
  'plan-execute': {
    label: 'Plan-and-Execute',
    def: '한 스텝씩 더듬는 대신 계획을 먼저 세우고 순차 실행하는 루프. 매 스텝마다 전체 히스토리를 다시 싣지 않아 ReAct보다 싸고 빠르다.',
  },
  reflexion: {
    label: 'Reflexion',
    def: '생성 결과를 평가자가 채점하고, 기준에 미달하면 피드백과 함께 다시 생성하는 루프. 생성과 검증을 분리하는 규율의 기본형이다.',
  },
  rewoo: {
    label: 'ReWOO',
    def: '중간 관찰 없이 계획 한 번으로 도구를 병렬 실행하는 루프. 왕복 횟수를 줄여 토큰을 아끼는 데 특화되어 있다.',
  },
  harness: {
    label: '하네스',
    def: '모델을 감싸는 실행 환경 전체. 시스템 프롬프트, 도구 정의, 컨텍스트 관리, 가드레일, 로깅이 모두 여기 들어간다. 같은 모델도 하네스가 성능을 가른다. 이것을 설계하는 일이 하네스 엔지니어링이다.',
  },
  'budget-guard': {
    label: 'Budget guard',
    def: '실행 중 누적 토큰·비용이 상한을 넘으면 경고하거나 중단시키는 장치. 스텝 한도가 루프의 보험이라면 이쪽은 지갑의 보험이다.',
  },
  mcp: {
    label: 'MCP',
    def: 'Model Context Protocol. 도구와 데이터를 표준 프로토콜로 주고받는 규격. 손으로 정의하던 도구를 서버가 내어놓고, 클라이언트가 목록을 받아 그대로 쓴다.',
  },
  langgraph: {
    label: 'LangGraph',
    def: '에이전트의 제어 흐름을 상태·노드·엣지의 그래프로 선언하는 프레임워크. 손으로 짠 루프를 선언적 구조로 옮기고, 영속성·중단·병렬 실행을 얹는다.',
  },
  supervisor: {
    label: 'Supervisor 패턴',
    def: '상위 에이전트가 하위 전문 에이전트들에게 일을 배분하고 결과를 모으는 멀티 에이전트 구조. 제어권은 늘 supervisor로 돌아온다.',
  },
  handoff: {
    label: 'Handoff 패턴',
    def: '에이전트가 다른 에이전트에게 제어권 자체를 넘기는 멀티 에이전트 구조. 넘겨받은 쪽이 대화를 이어받아 사용자에게 직접 답하고, 넘긴 쪽은 손을 뗀다.',
  },
  'release-ladder': {
    label: '릴리즈 사다리',
    def: '시연 저장소마다 v0.1에서 v1.0까지 태그를 밟아 올라가는 진행 방식. 태그 하나가 feature 하나의 완결이고, 어느 단이든 그 시점의 코드로 실행된다. 라이브로 코드를 만들어 가는 1~4주차 시연 저장소가 이 방식이고, 예제를 실행하는 5·6주차 실습 랩은 완성본 하나로 진행한다.',
  },
  sse: {
    label: 'SSE',
    def: 'Server-Sent Events. HTTP 연결 하나를 열어둔 채 서버가 클라이언트로 이벤트를 단방향으로 흘려보내는 웹 표준(Content-Type: text/event-stream). 브라우저는 EventSource로 소비한다. LLM 토큰 스트리밍과 작업 진행 상황 전달에 흔히 쓰이며, WebSocket과 달리 일반 HTTP라 가볍다.',
  },
};
