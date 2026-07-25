import { buildTree, type Category } from 'stack-site-builder/lib/category-tree';

export type { Category } from 'stack-site-builder/lib/category-tree';

/**
 * `stacks` 컬렉션(테마 코어 도구 카탈로그)의 분류 체계 — 과정에서 실제로 쓰는
 * "사용 도구" 카탈로그로 활용한다. 홈은 cards 템플릿이라 카탈로그 홈을 거치지
 * 않고, 홈의 "사용 도구" 카드가 부모 카테고리 페이지(`/categories/tools/`)로
 * 연결한다 — 이 페이지는 서브트리(개발 도구 + 참고 사이트)의 도구를 모두 모아
 * 보여준다.
 */
const categories: Category[] = [
  {
    id: 'tools',
    label: { ko: '사용 도구' },
    description: { ko: '과정에서 실제로 쓰는 도구와 참고 사이트' },
    detail: {
      ko: '강의·실습·프로젝트에서 실제로 쓰는 에디터·컨테이너·AI 개발 유틸리티와, 버전·스택을 확인하는 참고 사이트를 모았습니다.',
    },
    children: [
      {
        id: 'dev-tools',
        label: { ko: '개발 도구' },
        description: { ko: '에디터·컨테이너·AI 개발 유틸리티' },
      },
      {
        id: 'reference-sites',
        label: { ko: '참고 사이트' },
        description: { ko: '버전·수명주기·스택 카탈로그 등 참고 자료' },
      },
    ],
  },
];

/** Top-level categories (homepage sections), in display order. */
export const rootCategories = categories;

const tree = buildTree(categories);

/** Every node by id (top-level and nested). */
export const categoryMap = tree.map;

/** All category ids, for static path generation. */
export const allCategoryIds = tree.allIds;

/** Root → node chain for an id (its breadcrumb path). Empty if unknown. */
export const pathOf = tree.pathOf;

/** Direct children of a node (empty for leaves). */
export const childrenOf = tree.childrenOf;

/** A node's id plus all of its descendants' ids (for subtree roll-up). */
export const descendantIds = tree.descendantIds;

/** The top-level ancestor id of a node (itself if already top-level). */
export function rootIdOf(id: string): string {
  const path = pathOf(id);
  return path.length ? path[0].id : id;
}
