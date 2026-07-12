import json
import time
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

app = Flask(__name__)
client = Anthropic()

# モデル作成
MODELS = {
    "haiku": {
        "id": "claude-haiku-4-5-20251001",
        "name": "Haiku 4.5",
        "description": "A model specialized in generating haikus.",
    },
    "sonnet": {
        "id": "claude-sonnet-4-6",
        "name": "Sonnet 4.6",
        "description": "A model specialized in complex reasoning and analysis.",
    },
    "opus": {
        "id": "claude-opus-4-8",
        "name": "Opus 4.8",
        "description": "A model specialized in creative writing and storytelling.",
    }
}

# modelsのリストを作成
conversations: dict[str, list] = {}

# ルートの設定
# 最初の画面
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", models=MODELS)


# チャット画面
@app.route("/chat", methods=["POST"])
def chat():
    # リクエストからJSONデータを取得
    data = request.json
    model_key = data["model"]
    user_message = data["message"]
    # temperatureとmax_tokensを取得（デフォルト値を設定）
    temperature = float(data.get("temperature", 1.0))
    max_tokens = int(data.get("max_tokens", 1024))
    # defaultのsession_idを設定
    session_id = data.get("session_id", "default")

    # 会話履歴を取得または初期化
    conv_key = f"{session_id}_{model_key}"
    if conv_key not in conversations:
        conversations[conv_key] = []
    
    # ユーザーのメッセージを会話履歴に追加
    history = conversations[conv_key]
    history.append({"role": "user", "content": user_message})

    # モデルIDを取得
    model_id = MODEL[model_key]["id"]


    # ストリーミング応答を生成するジェネレーター関数
    def generate():
        start_time = time.perf_counter()

        # AnthropicのストリーミングAPIを使用して応答を生成
        # strem
        with client.messages.stream(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=history
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                full_response += text
                yield f"data: {json.dumps({'text': text})}\n\n"
            
            # 会話履歴にアシスタントの応答を追加
            history.append({"role": "assistant", "content": full_response})

            # 使用トークン数と経過時間を計算して送信
            elapsed = round(time.perf_counter() - start_time, 2)
            usage = stream.get_final_message().usage
            yield f"data: {json.dumps({'done': True, 'input_tokens': usage.input_tokens, 'output_tokens': usage.output_tokens, 'elapsed': elapsed})}\n\n"

    # ストリーミング応答を返す
    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
    )


@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    ssession_id = data.get("session_id", "default")
    model_key = data.get("model", "")
    conv_key = f"{session_id}_{model_key}"
    convaersations.pop(conv_key, None)
    return {"status": "ok"}


# 実行
if __name__ == "__main__":
    app.run(debug=True, port=5000)