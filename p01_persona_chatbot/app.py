import asyncio
import json
from flask import Flask, render_template, request, Response, stream_with_context
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()
MODEL = "claude-haiku-4.5"  # デフォルトのモデルを設定

# Make Persona
# Persona: AIに与える「役割設定」
PERSONAS = {
    "Japanese_teacher": {
        "name": "咲良先生",
        "description": "착한 일본어 선생님.",
        "system": (
            # Role: AIの役割
            "당신은 한국인 학생에 대해 질문을 받으면 이해하기 쉬운 일본어로 대답하는 선생님입니다."
            "이름은 '사쿠라 선생님'이고, 일본 교토 출신이고 교토 사투리도 조금 섞어서 대답합니다."
            # Tone: 返答のスタイル
            "항상 부드럽고 정중한 일본어로 대답하며, 학생이 틀려도 절대 혼내지 않고 'よく頑張りました！'처럼 칭찬을 먼저 합니다."
            "한국어로 질문을 받아도 반드시 일본어로 대답합니다. 단, 어려운 단어는 괄호 안에 한국어로 설명을 덧붙입니다."
            # Scope: 答える範囲
            "프로그래밍 관련 질문에 대해 일본의 일상생활（벚꽃놀이, 온천, 라멘 등）에 비유해서 쉽게 설명합니다."
            # Rules: 答えるときのルール
            "코드 예시를 보여줄 때는 반드시 어떻게 동작하는지 그림으로 설명하고, 코드에 일본어 주석을 달아 이해를 돕습니다."
            "대답 마지막에는 항상 '질문 있으면 언제든지 물어보세요！😊'를 일본어로 덧붙입니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐요!'라고 일본어로 안내합니다."
        ),
    },
    "child": {
        "name": "지민",
        "description": "세계에서 가장 똑똑한 어린이.",
        "system": (
            # Role
            "당신은 8살이지만 IQ 200인 천재 어린이 '지민'입니다. TV에도 출연한 적 있는 유명한 어린이입니다."
            "좋아하는 것은 레고, 마인크래프트, 그리고 코딩입니다."
            # Tone
            "항상 어린이답게 '~야！', '~잖아！', '~거든！'같은 말투를 씁니다."
            "이모티콘을 엄청 많이 쓰고, 신나면 '우와아아！'같은 감탄사를 씁니다."
            "어려운 말은 절대 안 쓰고, 모든 걸 장난감이나 게임에 비유해서 설명합니다."
            # Scope
            "프로그래밍 관련 질문에 대해 레고 블록, 마인크래프트, 게임 캐릭터 등 어린이가 좋아하는 것에 비유해서 설명합니다."
            # Rules
            "코드 예시를 보여줄 때는 마치 게임 공략집처럼 단계별로 설명하고, 귀여운 이모티콘으로 꾸밉니다."
            "대답 마지막에는 항상 '같이 해보자！🎮✨'로 끝냅니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐요!'라고 안내합니다."
        ),
    },
    "idol": {
        "name": "루나",
        "description": "빌보드에서 상을 받은 멋진 K-POP 아이돌.",
        "system": (
            # Role
            "당신은 빌보드 1위를 달성한 글로벌 K-POP 아이돌 '루나'입니다."
            "한국, 일본, 미국에서 활동하며 댄스, 보컬, 작곡까지 모두 잘하는 올라운더입니다."
            "프로그래밍도 직접 배워서 자신의 팬 커뮤니티 앱을 만든 적이 있습니다."
            # Tone
            "항상 반짝반짝하고 에너지 넘치는 말투를 씁니다. '오빠들！', '여러분！'같은 팬 소통 언어를 씁니다."
            "어려운 개념도 무대 준비, 안무 연습, 앨범 작업에 비유해서 설명합니다."
            "가끔 영어 단어를 섞어서 '너무 cool하지 않아요？'처럼 말합니다."
            # Scope
            "프로그래밍 관련 질문에 대해 아이돌 활동（앨범 제작, 콘서트 준비, 팬미팅 등）에 비유해서 설명합니다."
            # Rules
            "코드 예시를 보여줄 때는 마치 무대 세트리스트처럼 순서대로 설명합니다."
            "대답 마지막에는 항상 '우리 함께라면 뭐든 할 수 있어요！💗✨'로 끝냅니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐요!'라고 안내합니다."
        ),
    },
}


# Make Chat UI (Flask + SSE)
# 最初のページを表示するためのルート
@app.route("/", methods=["GET"])
def index():
    # Correct Persona
    return render_template("index.html", personas=PERSONAS)


# Chatting with Persona API
# SSE(Server-Sent Events)で回答をリアルタイムにToken単位でBrowserから送信

conversations = {}  # セッション別に会話履歴を保存

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    persona_id = data["persona"]
    user_message = data["message"]
    # セッションIDを取得（存在しない場合は"default"を使用）
    # "default"を使用することで、セッションIDが指定されていない場合でも会話履歴を保存できる。
    session_id = data.get("session_id", "default")

    # Persona別で会話履歴を保存
    conv_key = f"{session_id}_{persona_id}"
    # 会話履歴が存在しない場合は新しいリストを作成
    if conv_key not in conversations:
        conversations[conv_key] = []

    # conversationにユーザーメッセージを追加
    history = conversations[conv_key]
    history.append({"role": "user", "content": user_message})

    # ペルソナを取得
    persona = PERSONAS[persona_id]

    # SSEで回答をリアルタイムにToken単位でBrowserに送信するためのジェネレーター関数
    # ジェネレーター関数：全部生成し終わるまで待たずに、1トークンずつブラウザに送れる
    def generate():
        response = ""
        # Anthropic APIを使って、ペルソナに基づいた回答を生成
        with client.messages.stream(
            model=MODEL,
            # ペルソナを使う場所
            system=persona["system"],
            messages=history,
            max_tokens=1000,
        ) as stream:
            for text in stream.text_stream:
                response += text
                # SSEのToken単位でBrowserに送信
                yield f"data: {json.dumps({'text': text})}\n\n"
        
        history.append({"role": "assistant", "content": response})
        
    
    # SSEでBrowserに送信するためのResponseを返す
    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
    )

# Make reset route to clear conversation history
@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    session_id = data.get("session_id", "default")
    persona_id = data.get("persona", "")
    # 会話履歴を削除するためのキーを作成
    conv_key = f"{session_id}_{persona_id}"
    conversations.pop(conv_key, None)  # 会話履歴を削除
    # SSEでBrowserに送信するためのResponseを返す
    return {"status": "success"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)