🤖 モデルプレイグラウンド / 모델 플레이그라운드
📌 概要 / 개요
Flask + SSE + Claude API を使った、複数モデル・パラメータを比較できるプレイグラウンドです。
Flask + SSE + Claude API를 사용한 여러 모델·파라미터를 비교할 수 있는 플레이그라운드입니다.

✨ 機能 / 기능

🧠 モデル選択 / 모델 선택（Haiku 4.5 / Sonnet 4.6 / Opus 4.8）
🎚️ temperature・max_tokensのスライダー調整 / temperature·max_tokens 슬라이더 조절
💬 リアルタイムストリーミング応答（SSE） / 실시간 스트리밍 응답（SSE）
🗂️ モデル別・セッション別の会話履歴管理 / 모델별·세션별 대화 히스토리 관리
🔄 モデル切り替え時の自動リセット / 모델 전환 시 자동 초기화
📊 トークン使用量・所要時間の表示 / 토큰 사용량·소요 시간 표시

🛠️ 技術スタック / 기술 스택
種別 / 종류技術 / 기술バックエンド / 백엔드Python, FlaskAIClaude API（Anthropic）フロントエンド / 프론트엔드HTML, CSS, JavaScriptストリーミング / 스트리밍SSE（Server-Sent Events）環境変数 / 환경변수python-dotenv

📁 ディレクトリ構成 / 디렉토리 구성
p02_model_playground/
├── app.py # Flaskサーバー / Flask 서버
├── templates/
│ └── index.html # チャットUI / 채팅 UI
├── static/
│ └── style.css # スタイル / 스타일
├── .env # APIキー（非公開）/ API 키 (비공개)
└── .gitignore

⚙️ セットアップ / 셋업

1. リポジトリをクローン / 리포지토리 클론
   bashgit clone https://github.com/Azuking69/AI-Agent-project.git
   cd AI-Agent-project
2. 仮想環境を作成・有効化 / 가상환경 생성 및 활성화
   bashpy -3.13 -m venv venv

# Windows

.\venv\Scripts\activate

# Mac/Linux

source venv/bin/activate 3. 依存パッケージをインストール / 의존 패키지 설치
bashpip install flask anthropic python-dotenv 4. .envファイルを作成 / .env 파일 생성
ANTHROPIC_API_KEY=your_api_key_here 5. サーバーを起動 / 서버 실행
bashpython p02_model_playground/app.py 6. ブラウザでアクセス / 브라우저 접속
http://127.0.0.1:5000

🌿 ブランチ構成 / 브랜치 구성
master
└── develop
├── feature/02init_setup ✅ 初期設定 / 초기 설정
├── feature/02frontend ✅ index.html + style.css（SSE受信処理含む / SSE 수신 처리 포함）
├── feature/02model_select ✅ MODELS定義 + GET / + POST /chat + SSE / MODELS 정의 + GET / + POST /chat + SSE
├── feature/02reset ✅ リセット機能 + モデル切替時の自動リセット / 초기화 기능 + 모델 전환 시 자동 초기화
└── docs/02readme ✅ README

🚀 使い方 / 사용 방법

ページにアクセスしてモデルを選択 / 페이지 접속 후 모델 선택
temperature・max_tokensをスライダーで調整 / temperature·max_tokens를 슬라이더로 조절
メッセージを入力して「Send」をクリック / 메시지 입력 후「Send」클릭
AIがリアルタイムでストリーミング応答 / AI가 실시간으로 스트리밍 응답
「Reset」またはモデル切り替えで会話履歴をリセット / 「Reset」또는 모델 전환으로 대화 히스토리 초기화

⚖️ モデル比較 / 모델 비교
モデル速度 / 속도コスト / 비용向いてる作業 / 적합한 작업Haiku 4.5一番速い / 가장 빠름一番安い / 가장 저렴分類・抽出・簡単なQASonnet 4.6バランス型 / 균형中間 / 중간汎用・コーディング・分析Opus 4.8遅い / 느림高い / 비쌈複雑な推論・創作

📄 ライセンス / 라이선스
MIT License
