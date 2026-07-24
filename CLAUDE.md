# CLAUDE.md

AI 서비스 엔지니어링 Track A — 14회차 실습 트랙의 강의 자료·예제 코드 저장소.
이 문서는 이 저장소에서 작업하는 AI 도구를 위한 가이드다. **상세 규칙은
`docs/`에 있다** — 여기에는 요약과 링크만 둔다. 문서 목록은 `docs/README.md` 참고.

## 저장소 구조

- `site/` — stack-site-builder 기반 Astro 강의 사이트. 강의·슬라이드·개념·용어집·글.
  콘텐츠 작성 위치와 개발 명령은 `site/README.md` 참고.
- `docs/` — 규칙 문서(작성·문서화·git)와 회차별 강의 문서·실습 가이드 자리.
- `src/`, `tests/`, `pyproject.toml` — 회차별 Python 예제 코드 자리 (추가 예정)
  — 사이트 소스는 `site/src/`에 있다.

## Git 워크플로 — git flow (상세: `docs/git-workflow.md`)

- 새 작업은 항상 `develop`에서 `feature/*` 브랜치를 만들어 시작한다.
  `main`에는 직접 커밋하지 않는다. PR 대상도 기본적으로 `develop`이다.
- **커밋하면서 진행한다** — 논리 단위가 완결되면 바로 커밋하고, 여러 작업의
  변경을 워킹 트리에 쌓아두지 않는다. 한 커밋에는 한 가지 주제만 담는다.
- 커밋 전 검증: 사이트 변경이 있으면 `cd site && pnpm build && pnpm check`,
  md/mdx 문서 변경이 있으면 `python3 scripts/check-style.py` 통과 필수.
  커밋 메시지 제목은 영어 명령형 한 줄.

## 개발 명령

```sh
# repo 루트에서 — Docker (Node/pnpm 설치 불필요)
docker compose up                            # 보기 전용 (소스 내장)
docker compose -f docker-compose.dev.yml up  # site/ 바인드 마운트 + 핫리로드

# site/ 에서 — 로컬 pnpm
pnpm dev / pnpm build / pnpm check
```

## 콘텐츠·문서 작성 규칙 (상세: `docs/writing-rules.md`, `docs/documentation-rules.md`)

- 표 안의 파이프는 `\|`로 이스케이프한다 (위키링크 포함: `[[llm\|LLM]]`)
- 물결표 범위 표기는 `1\~9회차`처럼 이스케이프한다 (한 문단에 `~` 두 개면 취소선)
- 볼드가 괄호·따옴표로 끝나고 바로 뒤에 한글이 붙으면(`…(판단)**이고`) `**`가
  그대로 노출된다 — 문장을 다듬어 띄우거나 `<strong>` 태그를 쓴다
- `.mdx`에서 `<https://…>` 꺾쇠 자동 링크는 JSX로 해석되어 빌드 실패 —
  `[텍스트](URL)` 또는 코드 스팬을 쓴다
- 닫는 괄호로 끝나는 문장에는 마침표를 겹치지 않는다 — `).` 금지
- `[[용어]]` 위키링크는 `site/src/data/glossary.mjs` 등록 용어만 (미등록은 빌드 실패)
- 슬라이드는 작성·수정 후 브라우저에서 줄바꿈이 어색하지 않은지 확인한다
- 상세 규칙은 한 곳(docs)에만 두고 다른 문서에서는 링크한다
