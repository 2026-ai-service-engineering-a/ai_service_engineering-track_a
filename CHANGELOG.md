# Changelog

AI 서비스 엔지니어링 Track A 강의 사이트의 주요 변경 사항을 기록한다.

형식은 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)를 따르고,
[유의적 버전](https://semver.org/lang/ko/)을 준수한다. 릴리스는 저장소 루트의
git 태그(`vX.Y`)로, 사이트 버전은 `site/package.json`으로 관리한다.

## [1.1.0] - 2026-07-25

### 추가

- **사용 도구 카탈로그**: 테마의 `stacks` 컬렉션으로 "사용 도구" 카탈로그를
  구성했다. 개발 도구(VS Code, Docker, Orca)와 참고 사이트(endoflife.date,
  awesome-ai-stack)를 카드·상세 페이지로 제공하고, 카테고리 브라우즈
  (`/categories/tools/`)로 묶어 본다. 헤더 내비의 "사용 도구" 항목과 홈 카드
  양쪽에서 진입한다
- **소개 페이지 "주요 링크 및 안내"**: Awesome AI Stack 링크와 LLM 프로바이더
  콘솔(Google AI Studio, Claude, OpenAI, Ollama, Groq) 참고 표

### 변경

- **stack-site-builder 1.22.0으로 업데이트**: cards 홈에서도 카탈로그 Browse
  내비를 쓰도록 `home.browse`를 지원한다. 이 값으로 헤더에 "사용 도구" 항목을
  붙여 native 카탈로그 페이지로 연결한다
- **명사형 종결 마침표 규칙 전면 적용**: 서술형(`합니다`/`입니다`)에만 마침표를
  붙이고 명사형(`트랙`/`정리` 등 체언 종결)에는 붙이지 않는다. 규칙을
  `docs/writing-rules.md`에 추가하고 문서 전반에 반영했다
- **홈 히어로 줄바꿈 정리**: 최대 폭에서 마지막 단어가 홀로 넘어가지 않도록
  세 줄 균형으로 조정했다

## [1.0.0] - 2026-07-25

### 추가

- **강의 사이트**: stack-site-builder 기반 Astro 사이트(`site/`)이며 한국어 단일
  로케일, cards 홈이며 강의·글·슬라이드·개념·용어집·소개 섹션을 쓴다
- **Docker 실행**: 저장소 루트에서 `docker compose up`으로 사이트를 구동하고,
  `docker compose -f docker-compose.dev.yml up`으로 편집·핫리로드로 본다
- **1주차 교안**: 상세 강의 문서(`session-01`)와 슬라이드 덱: AI 서비스
  전주기(5레이어), 엔지니어링 사다리(프롬프트 → 컨텍스트 → 하네스), 분식집 주문
  에이전트 라이브 빌드, v0.1/v0.2/v1.0 코드 구조 분석과 인젝션 방어, 프로젝트
  트랙, 개인 repo 실습. 시연 저장소 `week01-order-agent`와 연계한다
- **주차별 운영안**: 소개 페이지에 1\~9주(공통 역량)·10\~14주(개인 프로젝트) 표
- **글**: 안내글(로컬에서 강의 자료 보기)과 강의 노트(Docker/Docker Compose 입문)
- **용어집**: LLM·RAG·임베딩·벡터DB·에이전트·가드레일·프롬프트 인젝션·Docker 등
  본문에서 `[[용어]]`로 링크되는 용어 정의
- **문서·규칙**: 작성 규칙(`writing-rules`), 문서 규칙(`documentation-rules`),
  git flow(`git-workflow`), 문서 스타일 검사 스크립트(`scripts/check-style.py`),
  AI 도구용 가이드(`CLAUDE.md`)
