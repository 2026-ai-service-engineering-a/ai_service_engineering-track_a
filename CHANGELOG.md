# Changelog

AI 서비스 엔지니어링 Track A 강의 사이트의 주요 변경 사항을 기록한다.

형식은 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)를 따르고,
[유의적 버전](https://semver.org/lang/ko/)을 준수한다. 릴리스는 저장소 루트의
git 태그(`vX.Y`)로, 사이트 버전은 `site/package.json`으로 관리한다.

## [1.2.0] - 2026-07-30

### 추가

- **2주차 교안 (session-02)**: "컨테이너 개발환경과 팀 워크플로". docker compose로
  app+db를 함께 띄우고, Git Flow 회전(feature 브랜치 → PR → CI → 머지)으로 이미
  동작하는 회의실 예약 서비스에 AI 에이전트를 얹는다. 기존 서비스 함수를 감싼
  도구(검색·가용·예약 생성·취소·예약 내역 조회), 자연어 채팅 UI, 대화 이어가기(DB
  무상태), 권한 코드 강제·재시도·폴백·루프 가드까지 다룬다
- **2주차 슬라이드 덱 (session-02)**: 커버·브리핑, 환경 투어, Git Flow 회전, 채팅
  UI, 예약 내역 조회, v1.5 SQL 콘솔, 마무리로 구성한 라이브 세션용 덱
- **LLM 멀티 프로바이더 구성**: session-02의 LiteLLM 층을 Gemini(기본
  `gemini/gemini-2.5-flash`)·Claude(`claude-3-haiku-20240307`)·OpenAI(`gpt-4.1-mini`)
  셋으로 확장하고, 프로바이더 키를 `.env`로 관리하며 실패 시 폴백 체인을 구성한다
- **v1.5 추가 과정 (관리자 전용, 선택)**: 자연어를 SQL로 옮겨 DB를 조회하는
  개발자·분석가용 도구. 전용 관리자 계정, 읽기 전용 롤, 단일 `SELECT` 파싱, 민감
  컬럼을 가린 리포팅 뷰의 다층 방어로 가둔다
- **session-02 "0. 사전 준비" 섹션**: git·Docker 설치 안내(Windows·Mac)

### 변경

- **stack-site-builder 1.23.1로 업데이트**
- **한글 줄표(`—`) 금지 규칙 도입**: `docs/writing-rules.md`에 규칙을 추가하고 전
  콘텐츠에서 줄표를 제거했으며, `scripts/check-style.py`가 이를 강제한다
- **리스트 선호·긴 문단 하드 브레이크 규칙 추가**: 나열형 내용은 리스트로 나누고,
  이어지는 긴 산문 문단은 하드 브레이크로 문장을 나눈다
- **1주차 자료(session-01) 정리**: 줄표 제거와 표현 다듬기 반영
- **VOD·영상 참조 정리**: 1·2주차 강의 자료에서 영상 아카이브 언급을 걷어내고
  코드·프롬프트 공개 중심으로 바꿨다

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
