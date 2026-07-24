# CLAUDE.md

AI 서비스 엔지니어링 Track A — 14회차 실습 트랙의 강의 자료·예제 코드 저장소.
이 문서는 이 저장소에서 작업하는 AI 도구를 위한 가이드다.

## 저장소 구조

- `site/` — stack-site-builder 기반 Astro 강의 사이트. 강의·슬라이드·개념·용어집·글.
  콘텐츠 작성 위치와 규칙은 `site/README.md` 참고.
- `docs/` — 콘텐츠 작성 규칙(`writing-rules.md`)과 회차별 강의 문서·실습 가이드 자리.
- `src/`, `tests/`, `pyproject.toml` — 회차별 Python 예제 코드 자리 (추가 예정)
  — 사이트 소스는 `site/src/`에 있다.

## Git 워크플로 — git flow

이 프로젝트는 **git flow** 기반으로 진행한다.

| 브랜치 | 역할 |
| --- | --- |
| `main` | 릴리스 브랜치 — 직접 커밋·머지 금지, release/hotfix를 통해서만 갱신 |
| `develop` | 통합 브랜치 — 모든 feature 브랜치의 분기점이자 머지 대상 |
| `feature/<이름>` | 기능·콘텐츠 작업 — `develop`에서 분기, `develop`으로 머지 (예: `feature/base_setup`) |
| `release/<버전>` | 릴리스 준비 — `develop`에서 분기, `main`과 `develop` 양쪽으로 머지 |
| `hotfix/<이름>` | 긴급 수정 — `main`에서 분기, `main`과 `develop` 양쪽으로 머지 |

규칙:

- 새 작업은 항상 `develop`에서 `feature/*` 브랜치를 만들어 시작한다.
- `main`에는 직접 커밋하지 않는다. PR 대상도 기본적으로 `develop`이다.
- 커밋·PR 전에 사이트 변경이 있으면 `cd site && pnpm build && pnpm check`가 통과해야 한다.

## 개발 명령

```sh
# repo 루트에서 — Docker (Node/pnpm 설치 불필요)
docker compose up                            # 보기 전용 (소스 내장)
docker compose -f docker-compose.dev.yml up  # site/ 바인드 마운트 + 핫리로드

# site/ 에서 — 로컬 pnpm
pnpm dev / pnpm build / pnpm check
```

## 콘텐츠 작성 규칙

문장 스타일·마크다운 이스케이프·슬라이드 줄바꿈 등 작성 규칙은
**`docs/writing-rules.md`**를 따른다. 핵심 요약:

- 표 안의 파이프는 `\|`로 이스케이프한다 (위키링크 포함: `[[llm\|LLM]]`)
- 물결표 범위 표기는 `1\~9회차`처럼 이스케이프한다 (한 문단에 `~` 두 개면 취소선)
- 닫는 괄호로 끝나는 문장에는 마침표를 겹치지 않는다 — `).` 금지
- `[[용어]]` 위키링크는 `site/src/data/glossary.mjs` 등록 용어만 (미등록은 빌드 실패)
- 슬라이드는 작성·수정 후 브라우저에서 줄바꿈이 어색하지 않은지 확인한다
