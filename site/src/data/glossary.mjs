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
};
