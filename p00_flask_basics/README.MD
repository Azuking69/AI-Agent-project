# 🌱 p00_flask_basics

## 📌 概要 / 개요

AIエージェントコース Chapter 1 の一環として作成した、Flaskの基礎を学ぶための練習プロジェクトです。
AI에이전트 코스 Chapter 1의 일환으로 작성한, Flask 기초를 배우기 위한 연습 프로젝트입니다.

---

## 🎯 目的 / 목적

Flaskの基本的な仕組み（ルーティング / クエリパラメータ / JSON応答 / render_template）を、実際に手を動かして理解する。
Flask의 기본적인 구조（라우팅 / 쿼리 파라미터 / JSON 응답 / render_template）를 직접 손으로 익힌다.

---

## ✨ 機能 / 기능

- 🌐 GET/POSTルーティングの基本 / GET/POST 라우팅 기초
- 🔎 クエリパラメータの受け取り / 쿼리 파라미터 수신
- 📦 JSON応答の返却 / JSON 응답 반환
- 🧩 URLパラメータの受け取り / URL 파라미터 수신
- 🖼️ render_templateによるHTML描画 / render_template를 통한 HTML 렌더링

---

## 🛠️ 技術スタック / 기술 스택

| 種別 / 종류                 | 技術 / 기술                    |
| --------------------------- | ------------------------------ |
| バックエンド / 백엔드       | Python, Flask                  |
| フロントエンド / 프론트엔드 | HTML, CSS, JavaScript（fetch） |

---

## 📁 ディレクトリ構成 / 디렉토리 구성

p00_flask_basics/
├── app.py # Flaskサーバー / Flask 서버
├── static/
│ └── style.css # スタイル / 스타일
├── templates/
│ └── index.html # 動作確認用UI / 동작 확인용 UI
├── .env # 環境変数（非公開）/ 환경변수(비공개)
└── venv/ # 仮想環境（非公開）/ 가상환경(비공개)

---

## 🌐 実装したルート / 구현한 라우트

| ルート          | メソッド | 内容 / 내용                                                                                          |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `/hello`        | GET      | 文字列をそのまま返す、一番シンプルなルート / 문자열을 그대로 반환하는 가장 단순한 라우트             |
| `/add`          | GET      | クエリパラメータ（a, b）を受け取り合計をJSONで返す / 쿼리 파라미터(a, b)를 받아 합계를 JSON으로 반환 |
| `/echo`         | POST     | JSON本文を受け取りecho・lengthを返す / JSON 본문을 받아 echo・length 반환                            |
| `/greet/<name>` | GET      | URLパラメータの名前を含む挨拶を返す / URL 파라미터의 이름을 포함한 인사말 반환                       |

---

## 💡 使用例 / 사용 예시

### GET /add

リクエスト / 요청: GET /add?a=3&b=5
レスポンス / 응답: {"a":3,"b":5,"sum":8}

### POST /echo

リクエスト / 요청: POST /echo Body: {"text": "안녕하세요"}
レスポンス / 응답: {"echo":"안녕하세요","length":5}

### GET /greet/<name>

リクエスト / 요청: GET /greet/민지
レスポンス / 응답: 민지님, 반갑습니다!

---

## ⚙️ セットアップ / 셋업

### 1. 仮想環境を作成・有効化 / 가상환경 생성 및 활성화

```bash
py -3.13 -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. 依存パッケージをインストール / 의존 패키지 설치

```bash
pip install flask
```

### 3. サーバーを起動 / 서버 실행

```bash
python app.py
```

### 4. ブラウザでアクセス / 브라우저 접속

http://127.0.0.1:5000

---

## 📄 ライセンス / 라이선스

MIT License
