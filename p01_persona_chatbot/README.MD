# 🤖 ペルソナチャットボット / 페르소나 챗봇

## 📌 概要 / 개요

Flask + SSE + Claude API を使った、ペルソナ切り替え可能なリアルタイムチャットボットです。
Flask + SSE + Claude API를 사용한 페르소나 전환 가능한 실시간 챗봇입니다.

---

## ✨ 機能 / 기능

- 🎭 ペルソナ選択 / 페르소나 선택（착한 일본인 / 똑똑한 어린이 / 멋진 아이돌）
- 💬 リアルタイムストリーミング応答（SSE） / 실시간 스트리밍 응답（SSE）
- 📝 Markdownレンダリング / Markdown 렌더링
- 🔄 会話履歴のリセット / 대화 히스토리 초기화
- 🗂️ ペルソナ別・セッション別の会話履歴管理 / 페르소나별·세션별 대화 히스토리 관리

---

## 🛠️ 技術スタック / 기술 스택

| 種別 / 종류                            | 技術 / 기술               |
| -------------------------------------- | ------------------------- |
| バックエンド / 백엔드                  | Python, Flask             |
| AI                                     | Claude API（Anthropic）   |
| フロントエンド / 프론트엔드            | HTML, CSS, JavaScript     |
| ストリーミング / 스트리밍              | SSE（Server-Sent Events） |
| Markdownレンダリング / Markdown 렌더링 | marked.js                 |
| 環境変数 / 환경변수                    | python-dotenv             |

---

## 📁 ディレクトリ構成 / 디렉토리 구성

```
p01_persona_chatbot/
├── app.py              # Flaskサーバー / Flask 서버
├── templates/
│   └── index.html      # チャットUI / 채팅 UI
├── static/
│   └── style.css       # スタイル / 스타일
├── .env                # APIキー（非公開）/ API 키 (비공개)
└── .gitignore
```

---

## ⚙️ セットアップ / 셋업

### 1. リポジトリをクローン / 리포지토리 클론

```bash
git clone https://github.com/Azuking69/AI-Agent-project.git
cd AI-Agent-project
```

### 2. 仮想環境を作成・有効化 / 가상환경 생성 및 활성화

```bash
py -3.13 -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 依存パッケージをインストール / 의존 패키지 설치

```bash
pip install flask anthropic python-dotenv
```

### 4. `.env`ファイルを作成 / `.env` 파일 생성

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 5. サーバーを起動 / 서버 실행

```bash
python p01_persona_chatbot/app.py
```

### 6. ブラウザでアクセス / 브라우저 접속

```
http://127.0.0.1:5000
```

---

## 🌿 ブランチ構成 / 브랜치 구성

```
master
└── develop
    ├── feature/persona          ✅ ペルソナ定義 / 페르소나 정의
    ├── feature/UI_flask_sse     ✅ Flaskルート + SSEロジック / Flask 라우트 + SSE 로직
    ├── feature/frontend         ✅ index.html + style.css
    ├── feature/sse_js           ✅ SSE受信処理 + Markdownレンダリング / SSE 수신 처리 + Markdown 렌더링
    ├── feature/reset            ✅ リセット機能 / 초기화 기능
    └── docs/readme              ✅ README
```

---

## 🚀 使い方 / 사용 방법

1. ページにアクセスしてペルソナを選択 / 페이지 접속 후 페르소나 선택
2. メッセージを入力して「Send」をクリック / 메시지 입력 후 「Send」클릭
3. AIがリアルタイムでストリーミング応答 / AI가 실시간으로 스트리밍 응답
4. 「Reset」で会話履歴をリセット / 「Reset」으로 대화 히스토리 초기화

---

## 📄 ライセンス / 라이선스

MIT License
