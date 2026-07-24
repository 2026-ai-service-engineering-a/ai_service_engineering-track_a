import { buildTree, type Category } from 'stack-site-builder/lib/category-tree';

/**
 * `concepts` 컬렉션의 분류 체계 — 과정을 관통하는 핵심 개념을 세 축으로
 * 나눈다: LLM 활용, 검색(임베딩·벡터DB·RAG), 서비스화(API·UI·배포).
 */
export const conceptCategories: Category[] = [
  {
    id: 'llm',
    label: { ko: 'LLM·프롬프트' },
    description: {
      ko: 'LLM API, 토큰, 프롬프트 패턴, structured output 등 LLM 활용의 기본기',
    },
  },
  {
    id: 'retrieval',
    label: { ko: '임베딩·RAG' },
    description: {
      ko: '임베딩, 벡터DB, 유사도 검색, RAG 파이프라인 — 검색 기반 생성의 구성 요소',
    },
  },
  {
    id: 'serving',
    label: { ko: '서비스화·배포' },
    description: {
      ko: 'FastAPI 서비스화, UI(Streamlit·Gradio 등), 배포와 운영',
    },
  },
  {
    id: 'concept-uncategorized',
    label: { ko: '미분류' },
    description: {
      ko: '아직 분류에 들어가지 않은 개념',
    },
  },
];

export const conceptTree = buildTree(conceptCategories);

/** Id of the fallback category that holds concepts without a real category. */
export const UNCATEGORIZED_CONCEPT = 'concept-uncategorized';

/** Resolve a concept's `category` to a real tree id (unknown → uncategorized). */
export const conceptCatOf = (category?: string | null): string =>
  category && conceptTree.map.has(category) ? category : UNCATEGORIZED_CONCEPT;
