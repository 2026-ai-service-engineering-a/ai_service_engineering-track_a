# Git 워크플로

이 프로젝트는 **git flow** 기반으로 진행한다. 사람이든 AI든 동일하게 따른다.

## 브랜치 모델

| 브랜치 | 역할 |
| --- | --- |
| `main` | 릴리스 브랜치: 직접 커밋·머지 금지, release/hotfix를 통해서만 갱신 |
| `develop` | 통합 브랜치: 모든 feature 브랜치의 분기점이자 머지 대상 |
| `feature/<이름>` | 기능·콘텐츠 작업: `develop`에서 분기, `develop`으로 머지 (예: `feature/base_setup`) |
| `release/<버전>` | 릴리스 준비: `develop`에서 분기, `main`과 `develop` 양쪽으로 머지 |
| `hotfix/<이름>` | 긴급 수정: `main`에서 분기, `main`과 `develop` 양쪽으로 머지 |

- 새 작업은 항상 `develop`에서 `feature/*` 브랜치를 만들어 시작한다.
- `main`에는 직접 커밋하지 않는다. PR 대상도 기본적으로 `develop`이다.

## 커밋 규칙

- **커밋하면서 진행한다.** 작업을 작은 논리 단위로 나누고, 한 단위가 완결되면
  바로 커밋한다. 여러 작업의 변경을 워킹 트리에 쌓아두지 않는다.
- **한 커밋에는 한 가지 주제만 담는다.** 예: 사이트 스캐폴드 / docker 구성 /
  규칙 문서 추가는 각각 별도 커밋으로 나눈다.
- **커밋 전 검증**: 사이트(`site/`) 변경이 있으면 `cd site && pnpm build &&
  pnpm check`가 통과해야 한다. 렌더링에 영향 주는 변경(표·이스케이프 등)은
  해당 페이지를 열어 눈으로도 확인한다.
- **문서 스타일 검사**: md/mdx를 고쳤으면 `python3 scripts/check-style.py`도
  통과해야 한다. writing-rules 중 기계로 잡히는 항목(`).` 마침표 겹침, 취소선
  위험 물결표, MDX 꺾쇠 링크, 볼드 경계)을 검사한다.
- **스테이징 확인**: 커밋 전에 `git status`로 산출물(node_modules, dist 등)이
  섞이지 않았는지 확인한다.

## 커밋 메시지

- 제목은 **영어 명령형 한 줄** (기존 히스토리와 동일한 스타일):
  `Add lecture site under site/ (stack-site-builder based)`
- 필요하면 빈 줄 뒤 본문에 이유·맥락을 적는다. 제목만으로 충분하면 생략한다.
