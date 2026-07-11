markdown# 📋 p00_flask_basics 브랜치 계획서

## 🎯 최종 목표

Flask의 기본 라우팅, GET/POST 요청, 템플릿 렌더링을 직접 구현하여
`p01_persona_chatbot`에서 사용한 Flask + fetch 패턴의 기초를 이해한다.

---

## 🌿 브랜치 구조

```
master  ← 최종 완료 후 develop에서 머지
└── develop  ← 기반 브랜치 (초기 구성 포함)
    ├── feature/00_frontend
    ├── feature/00_backend
    └── docs/00_readme
```

---

## 📌 브랜치별 작업 내용

### ✅ develop（초기 구성 포함）

**작업 내용:**

- 프로젝트 폴더 구성 (`app.py`, `templates/`, `static/`)
- `.github/GitHub_PR_Template` 추가
- `.gitignore` 설정

---

### ✅ feature/00_frontend

**작업 내용:**

- `templates/index.html` 구현
  - `GET /hello`, `GET /greet/민지` 링크
  - `GET /add` : 숫자 2개 입력 → 쿼리 파라미터로 전송
  - `POST /echo` : 텍스트 입력 → JSON 본문으로 전송
  - fetch 요청/응답을 `<pre>` 태그로 시각화
- `static/style.css` 구현 (글래스모피즘 기반 UI)

---

### 🔲 feature/00_backend

**작업 내용:**

- [ ] `GET /` : `index.html` 렌더링 (`name` 변수 전달)
- [ ] `GET /hello` : 단순 텍스트 응답
- [ ] `GET /greet/<name>` : URL 파라미터로 이름을 받아 응답
- [ ] `GET /add?a=&b=` : 쿼리 파라미터로 두 숫자를 받아 합계 반환
- [ ] `POST /echo` : JSON 본문을 받아 그대로 반환

**완료 조건:**

- `더하기` 버튼 클릭 시 GET 요청 및 응답 정상 표시
- `보내기` 버튼 클릭 시 POST 요청 및 응답 정상 표시
- `/hello`, `/greet/민지` 링크 클릭 시 새 탭에서 정상 응답

---

### 🔲 docs/00_readme

**작업 내용:**

- [ ] README.md 작성 (일본어 / 한국어 병기)
  - 개요, 기능, 기술 스택, 셋업 방법, 라우트 목록

---

## 🔁 PR 규칙

- base: `develop` ← compare: `feature/xxx`
- 모든 feature 브랜치 머지 완료 후 `develop` → `master` 로 최종 머지
- PR 템플릿 사용 (한국어)
- 머지 후 feature 브랜치 삭제

---

## ✅ 최종 완료 조건

- [ ] `GET /`, `/hello`, `/greet/<name>` 정상 동작
- [ ] `GET /add` 쿼리 파라미터 처리 정상 동작
- [ ] `POST /echo` JSON 처리 정상 동작
- [ ] UI에서 요청/응답 시각화 확인
- [ ] `.env` 미포함 확인
- [ ] README 완성
