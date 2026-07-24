import { buildTree, type Category } from 'stack-site-builder/lib/category-tree';

/**
 * `articles` 컬렉션의 분류 체계 — 공지와 강의 노트가 중심.
 */
export const articleCategories: Category[] = [
  {
    id: 'notice',
    label: { ko: '공지' },
    description: {
      ko: '과정 운영 관련 공지사항',
    },
  },
  {
    id: 'lecture-note',
    label: { ko: '강의 노트' },
    description: {
      ko: '회차 진행 후 정리하는 보충 노트와 실습 팁',
    },
  },
  {
    id: 'article-uncategorized',
    label: { ko: '미분류' },
    description: {
      ko: '아직 분류에 들어가지 않은 글',
    },
  },
];

export const articleTree = buildTree(articleCategories);

/** Id of the fallback category that holds articles without a real category. */
export const UNCATEGORIZED_ARTICLE = 'article-uncategorized';

/** Resolve an article's `category` to a real tree id (unknown → uncategorized). */
export const articleCatOf = (category?: string | null): string =>
  category && articleTree.map.has(category) ? category : UNCATEGORIZED_ARTICLE;
