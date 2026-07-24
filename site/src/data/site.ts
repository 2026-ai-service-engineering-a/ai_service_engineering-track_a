import type { SectionKey } from 'stack-site-builder';

/**
 * 사이트 정체성 — 테마가 `@aas-data/site` alias로 읽어간다.
 * UI 문자열 오버라이드 키는 테마의 src/i18n/ui.ts와 동일하다.
 */
export const site = {
  /** 헤더와 홈 타이틀에 표시. */
  name: 'AI 서비스 엔지니어링 Track A',
  /** 콘텐츠가 사는 저장소 — 샘플 폴더 링크 등이 여기를 가리킨다. */
  repoUrl: 'https://github.com/2026-ai-service-engineering-a/ai_service_engineering-track_a',
  /** 빌드 시 GitHub API 호출(스타 수 등)에 쓰는 User-Agent. */
  buildUserAgent: 'aise-track-a-site',
  /** 저장소가 private이므로 헤더의 GitHub 링크는 숨긴다. */
  repoNav: false,
  /**
   * 이 사이트가 제공하는 로케일. 강의 자료가 한국어뿐이라 ko 단일 로케일 —
   * astro.config의 `i18n.defaultLocale`과 첫 항목이 일치해야 한다.
   */
  locales: [{ code: 'ko', label: '한국어', dateLocale: 'ko-KR' }] as {
    code: string;
    label: string;
    dateLocale?: string;
  }[],
  /**
   * 섹션 구성: 강의(courses)·글(articles)·슬라이드(slides)·개념(concepts)·
   * 용어집(glossary)·소개(pages)를 쓴다.
   * - courses는 opt-in이라 명시적으로 켠다 (src/data/course-categories.ts 필요).
   * - samples(실행 샘플)는 쓰지 않으므로 끈다.
   * - concepts/articles/slides/glossary/pages는 기본 on이라 그대로 둔다.
   * - products/papers(논문)는 기본 off(opt-in)라 그대로 둔다.
   * - 도구 카탈로그(stacks)는 테마 코어라 항상 켜져 있지만, cards 홈을 쓰고
   *   콘텐츠를 만들지 않는 것으로 사실상 비활성화한다.
   */
  sections: {
    courses: true,
    samples: false,
  } satisfies Partial<Record<SectionKey, boolean>>,
  /**
   * 데이터 주도 cards 홈 — 기본 홈(스택 카탈로그) 대신 강의 사이트에 맞는
   * 히어로 + 바로가기 카드 + CTA 구성을 쓴다. 내부 href는 로케일 프리픽스
   * 없이 쓰면 렌더 시 현재 로케일이 붙는다.
   */
  home: {
    template: 'cards' as const,
    hero: {
      title: 'AI 서비스 엔지니어링 — Track A',
      subtitle:
        '공통 기술 스택 실습(1~9주차)으로 기초를 정렬하고,<br>개인별 배포 가능한 오픈소스 기반<br>AI 데모 서비스(10~14주차)를 완성하는 14주 실습 트랙',
    },
    cardsTitle: '바로가기',
    cards: [
      {
        href: '/course/',
        name: '강의',
        description: '주차별 강의 자료와 실습 가이드 —<br>환경 구축부터 RAG, FastAPI, 배포까지',
        tags: ['1~9주차 공통 역량', '10~14주차 개인 프로젝트'],
      },
      {
        href: '/slides/',
        name: '슬라이드',
        description: '주차별 강의 슬라이드 —<br>브라우저에서 바로 보는 프레젠테이션',
        tags: ['프레젠테이션'],
      },
      {
        href: '/concept/',
        name: '개념',
        description: 'LLM·프롬프트, 임베딩·벡터DB, RAG, 서비스화 등<br>과정을 관통하는 핵심 개념 정리',
        tags: ['LLM', 'RAG', '서빙'],
      },
      {
        href: '/article/',
        name: '글',
        description: '공지사항과 강의 노트, 실습 팁',
        tags: ['공지', '강의 노트'],
      },
      {
        href: '/categories/tools/',
        name: '사용 도구',
        description: '과정에서 실제로 쓰는 에디터·컨테이너·유틸리티와<br>버전·스택 확인용 참고 사이트',
        tags: ['VS Code', 'Docker', '참고 사이트'],
      },
    ],
    cta: {
      title: '과정이 처음이신가요?',
      description: '트랙 구성, 커리큘럼, 선행 요건은<br>소개 페이지에서 확인하세요.',
      button: { label: '과정 소개 보기', href: '/about/' },
    },
  },
  /** 테마 UI 문자열의 로케일별 오버라이드. */
  ui: {
    ko: {
      'site.tagline':
        'AI 서비스 엔지니어링 Track A — 14주 실습 트랙의 강의 자료, 슬라이드, 개념 정리, 용어집',
    },
  } as Record<string, Record<string, string>>,
};

export type SiteConfig = typeof site;
