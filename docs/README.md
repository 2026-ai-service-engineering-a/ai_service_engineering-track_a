# docs

저장소 운영·개발 규칙 문서와 주차별 강의 문서·실습 가이드

## 규칙 문서

- [writing-rules.md](writing-rules.md): 콘텐츠·문서 작성 규칙 (한글 문장
  스타일, 마크다운 이스케이프(표 파이프·물결표), 소프트 줄바꿈, 슬라이드
  줄바꿈 체크)
- [documentation-rules.md](documentation-rules.md): 문서의 위치·파일명·구성
  규칙
- [git-workflow.md](git-workflow.md): git flow 브랜치 모델과 커밋 규칙
  (커밋하면서 진행, 커밋 전 검증, 메시지 스타일)
- [deployment.md](deployment.md): GitHub Pages 배포 (공개 주소, base 경로,
  워크플로가 하는 일, 배포가 안 될 때)

## 인터랙티브 그림의 재현 기록

교안에 실리는 `<…/>` 컴포넌트는 전부 실측 데이터 위에 선다. 데이터를 어떻게
떴는지, 다시 뜰 때 무엇을 확인해야 하는지의 기록이다.

- [model-vs-service-data.md](model-vs-service-data.md): `<ModelVsService />`.
  같은 질문을 도구 없이·도구를 쥐여주고 두 번 실제 호출한 기록 (5주차 3장)
- [context-growth-data.md](context-growth-data.md): `<ContextGrowth />`.
  스텝마다 부푸는 messages 배열과 compact 전후의 토큰 실측 (6주차 3장)
- [harness-gates-port.md](harness-gates-port.md): `<HarnessGates />`.
  파이썬 원본과 브라우저 판정 모듈의 29건 대조 기록 (6주차 5장)

## 주차별 강의 문서

주차별 교안은 강의 사이트의 course 문서가 단일 원본이다.
`site/src/content/courses/ko/` (예: 1주차 `session-01.mdx`)에 있다.
슬라이드도 이 문서를 토대로 만든다. 운영용 보조 문서가 생기면 여기에 둔다.
