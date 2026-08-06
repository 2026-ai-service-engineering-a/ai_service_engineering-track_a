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
  sse: {
    label: 'SSE',
    def: 'Server-Sent Events. HTTP 연결 하나를 열어둔 채 서버가 클라이언트로 이벤트를 단방향으로 흘려보내는 웹 표준(Content-Type: text/event-stream). 브라우저는 EventSource로 소비한다. LLM 토큰 스트리밍과 작업 진행 상황 전달에 흔히 쓰이며, WebSocket과 달리 일반 HTTP라 가볍다.',
  },
};
