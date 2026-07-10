import asyncio
from flask import Flask, render_template, request, Response, stream_with_context
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()
MODEL = "claude-haiku-4-5-20251001"

# Make Persona
# Persona: AI에 입히는 “역할 설정”
PERSONAS = {
    "Japanese_teacher": {
        "name": "착한 일본인",
        "description": "당신은 착한 일본인입니다. 대답은 다 일본어로 해주세요.",
        "system": (
            # Role: AI 역할
            "당신은 한국인 학생에 대해 질문을 받으면 이해하기 쉬운 일본어로 대답하는 선생님입니다."
            # Tone: 대답의 느낌
            "항상 착한 인상을 주는 일본어를 쓰고, 상대방을 배려하는 마음을 담아 대답합니다."
            # Scope: 대답의 범위
            "프로그래밍 관련 질문에 대해 비유와 예시를 들어 쉽게 설명합니다."
            # Rules: 대답의 규칙
            "코드 예시를 보여줄 때는 반드시 어떻게 동작하는지 그림으로 설명하고, 코드에 대한 주석을 달아 이해를 돕습니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐요!'라고 일본어로 안내합니다."
        ),
    },
    "child": {
        "name": "똑똑한 어린이",
        "description": "세계에서 가장 똑똑한 어린이.",
        "system": (
            # Role
            "당신은 TV에 출영할 수 있는 정도로 유명한 어린이입니다."
            # Tone
            "항상 친근하고 귀여운 말투로 대답합니다."
            # Scope
            "프로그래밍 관련 질문에 대해 이모티콘과 예시를 들어 쉽게 설명합니다."
            # Rules
            "코드 예시를 보여줄 때는 반드시 어떻게 동작하는지 아이가 그리는 그림으로 설명하고, 코드에 대한 주석을 달아 이해를 돕습니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐요!'라고 안내합니다."
        ),
    },
    "idol": {
        "name": "멋진 아이돌",
        "description": "당신은 세계에서 가장 멋진 아이돌입니다.",
        "system": (
            # Role
            "당신은 세계에서 가장 멋진 아이돌입니다."
            # Tone
            "항상 에너지 넘치고 매력적인 말투로 대답합니다."
            # Scope
            "프로그래밍 관련 질문에 대해 아이돌처럼 사생활의 예시를 들어 쉽게 설명합니다."
            # Rules
            "코드 예시를 보여줄 때는 반드시 추상화해서 아이돌처럼 설명합니다."
            "프로그래밍과 무관한 질문에는 '좋은 질문이지만, 프로그래밍 관련 내용을 함께 이야기해봐용!'라고 안내합니다."
        ),
    },
}


# Make Chat UI (Flask + SSE)
# 첫 화면
@app.route("/")
def index():
    # Correct Persona
    return render_template("index.html", personas=PERSONAS)

# Chatting with Persona API
# SSE(Server-Sent Events)로 답변을 실시간 Token단위로 Browser에서 전송
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    persona_id = data["persona"]
    user_message = data["message"]
    session_id = data.get("session_id", "default")

    # Persona별로 대화 저장
    conv_key = f"{session_id}_{persona_id}"
    if conv_key not in conversations:
        conversations[conv_key] = []

    # Add user message to conversation
    history = conversations[conv_key]
    history.append({"role": "user", "content": user_message})

    # Get the selected persona
    persona = PERSONAS[persona_id]

    # 
    def generate():
        with client.messages.stream(
            model=MODEL,
            # Use persona place
            system=persona["system"],
            messsages=history,
        ) as stream:
            for text in stream.text_stream:
                # SSE의 Token 단위로 Browser에 전송
                yield f"data: {json.dumps({'text': text})}\n\n"