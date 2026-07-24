// @ts-check
// AI 서비스 엔지니어링 Track A 강의 사이트 — 사이트 수준 설정만 두고, 라우트·
// 컴포넌트·마크다운 파이프라인은 전부 stack-site-builder 테마가 제공한다.
// 강의 자료가 한국어 단일 언어이므로 로케일은 ko 하나만 쓴다(루트에서 서빙).
import { defineConfig } from 'astro/config';
import aasTheme from 'stack-site-builder';
import { glossary } from './src/data/glossary.mjs';
import { site } from './src/data/site';

// https://astro.build/config
export default defineConfig({
  // TODO: 배포 도메인 확정 시 변경 (sitemap/RSS의 절대 URL에 쓰인다).
  site: 'https://track-a.codecompose.net',
  base: '/',

  i18n: {
    locales: ['ko'],
    defaultLocale: 'ko',
    routing: {
      prefixDefaultLocale: false,
    },
  },

  // `sections`는 site.ts에서 선언해 여기로 전달 — 꺼진 섹션은 테마가 라우트
  // 주입을 건너뛰고, site.ts 쪽에서 헤더 내비 항목도 숨긴다.
  integrations: [aasTheme({ glossary, sections: site.sections })],
});
