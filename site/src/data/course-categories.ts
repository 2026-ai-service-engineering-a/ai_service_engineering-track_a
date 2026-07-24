import { buildTree, type Category } from 'stack-site-builder/lib/category-tree';

/**
 * `courses` 컬렉션의 분류 체계 — Track A의 과정 구조를 그대로 따른다:
 * 전반부 공통 기반(1~9회차), 후반부 개인 프로젝트(10~14회차).
 */
export const courseCategories: Category[] = [
  {
    id: 'foundation',
    label: { ko: '공통 기반 (1~9회차)' },
    description: {
      ko: '개발환경·LLM API·데이터·임베딩·RAG·FastAPI·UI — 모두가 함께 정렬하는 공통 기술 스택 실습',
    },
  },
  {
    id: 'project',
    label: { ko: '개인 프로젝트 (10~14회차)' },
    description: {
      ko: '기획 → MVP → 배포 → 문서화 → 발표 — 트랙별 개인 AI 데모 서비스 완성',
    },
  },
  {
    id: 'course-uncategorized',
    label: { ko: '미분류' },
    description: {
      ko: '아직 분류에 들어가지 않은 강의',
    },
  },
];

export const courseTree = buildTree(courseCategories);

/** Validation map for content.config.ts (strict category ids at build time). */
export const courseCategoryMap = courseTree.map;

/** Id of the fallback category that holds courses without a real category. */
export const UNCATEGORIZED_COURSE = 'course-uncategorized';

/** Resolve a course's `category` to a real tree id (unknown → uncategorized). */
export const courseCatOf = (category?: string | null): string =>
  category && courseTree.map.has(category) ? category : UNCATEGORIZED_COURSE;
