import { buildTree, type Category } from 'stack-site-builder/lib/category-tree';

export type { Category } from 'stack-site-builder/lib/category-tree';

/**
 * `stacks` 컬렉션(테마 코어 도구 카탈로그)의 분류 체계. 이 사이트는 도구
 * 카탈로그를 쓰지 않으므로(cards 홈 + 콘텐츠 없음) 플레이스홀더 노드 하나만
 * 둔다 — 테마 코어가 `@aas-data/categories`를 항상 import하기 때문에 파일
 * 자체는 필요하다.
 */
const categories: Category[] = [
  {
    id: 'uncategorized',
    label: { ko: '미분류' },
    description: {
      ko: '아직 분류에 들어가지 않은 도구',
    },
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
