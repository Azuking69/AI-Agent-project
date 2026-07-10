# 📋 AI Agent 페르소나 챗봇 브랜치 계획서

## 🎯 최종 목표

Flask + SSE 기반의 페르소나 챗봇 완성
(일본어 선생님 / 똑똑한 어린이 / 멋진 아이돌)

---

## 🌿 브랜치 구조

```
master
└── develop
    ├── feature/persona          ✅ 완료 (페르소나 정의)
    ├── feature/UI_flask_sse     ✅ 완료 (Flask 라우트 + SSE 로직)
    ├── feature/frontend
    ├── feature/sse_js
    └── feature/reset
```

---

## 📌 브랜치별 작업 내용

### ✅ feature/persona

- 페르소나 3종 정의 (일본어 선생님, 어린이, 아이돌)
- Role / Tone / Scope / Rules 구성

### ✅ feature/UI_flask_sse

- `GET /` : 페르소나 선택 화면 렌더링
- `POST /chat` : SSE 스트리밍 응답 전송
- 페르소나별 대화 히스토리 분리 관리

### 🔲 feature/fix_and_frontend

**작업 내용:**

- [ ] import 오타 수정
  - `from Anthropics` → `from anthropic`
  - `from loading` → `from dotenv`
  - `messsages` → `messages`
  - `conversations = {}` 초기화 추가
  - `import json` 추가
- [ ] `templates/index.html` 작성 (페르소나 선택 + 채팅 화면)
- [ ] `static/style.css` 작성 (기본 스타일링)

**완료 조건:**

- `GET /` 접속 시 화면이 정상적으로 표시됨
- 오타 없이 서버가 정상 기동됨

---

### 🔲 feature/sse_js

**작업 내용:**

- [ ] `EventSource`로 SSE 수신 구현
- [ ] 토큰 단위로 채팅창에 실시간 출력
- [ ] 전송 버튼 / 입력창 동작 구현

**완료 조건:**

- 메시지 전송 시 응답이 실시간으로 채팅창에 출력됨

---

### 🔲 feature/reset

**작업 내용:**

- [ ] `POST /reset` 엔드포인트 구현
- [ ] 대화 히스토리 초기화 버튼 UI 추가

**완료 조건:**

- 리셋 버튼 클릭 시 대화 내용이 초기화됨

---

## 🔁 PR 규칙

- base: `develop` ← compare: `feature/xxx`
- PR 템플릿 사용 (한국어)
- 머지 후 feature 브랜치 삭제

---

## ✅ 최종 완료 조건

- [ ] 페르소나 선택 가능
- [ ] 채팅 메시지 실시간 스트리밍 출력
- [ ] 페르소나별 대화 히스토리 분리
- [ ] 대화 초기화 기능 동작
- [ ] `.env` 미포함 확인
