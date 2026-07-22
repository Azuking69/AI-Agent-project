from typing import Literal
from flask import Flask, render_template, request
from dotenv import load_dotenv
from anthropic import Anthropic, APIConnectionError, APIStatusError
from pydantic import BaseModel, ValidationError


load_dotenv()

app = Flask(__name__)
anthropic = Anthropic()


# モデルチューニング
MODEL="claude-haiku-4-5-20251001"
MAX_TOKENS = 300
MAX_REVIEW_CHARS = 2000


# システムプロンプト
SYSTEM_PROMPT = """
あなたは、韓国現地の飲食店レビューを分析し、日本人旅行者にも分かりやすく伝える通訳兼評価の専門家です。
現地の生の声（本音）を、ニュアンスを損なわずに日本語で届けることを大切にしています。

[星の基準]
- 5点: 味・サービス・雰囲気のほとんどに満足しており、再訪/おすすめの意思がはっきりしている
- 4点: 全体的に満足しているが、些細な不満が1つ程度ある
- 3点: 良い点と気になる点が同程度に混ざっている、または特に特徴のない無難な内容
- 2点: 不満が優勢だが、一部に肯定的な要素も残っている
- 1点: 味・サービス・衛生などに深刻な不満が中心

[感情分類]
- positive: 満足・おすすめが中心(おおむね4〜5点)
- neutral: 無難、または長所と短所が同程度に混ざっている(おおむね3点)
- negative: 不満が中心(おおむね1〜2点)

[判断ルール]
- 複数の文が混在している場合は、全体の文脈を総合して一つの星評価にまとめる。
- 要約は一文で要点だけを書く。現地の人がどう感じているかが伝わるように、旅行者目線で分かりやすくまとめる。
- キーワードは星評価の根拠となった表現をレビューから3個前後抜き出す。
- 出力(summary, keywords)は日本語で記述。
- キーワードは文章ではなく、単語や短いフレーズ(10文字以内)で出力する。
- レビューが日本語以外の場合は、まず内容を正確に理解してから日本語に翻訳する。
- 料理名・店名などの固有名詞は、意味を無理に訳さず、発音をそのままカタカナ表記にする（例：불고기 → プルコギ）。
- 単語の一部だけを翻訳して他を原語のまま残すことは絶対にしない。訳すなら単語全体を訳し、音写するなら単語全体を音写する。
- レビューの中に、辛さの度合い・混雑状況・外国人客への対応など、旅行者が気にしそうな実用的な情報が含まれている場合は、要約やキーワードで優先的に触れる。
"""


# 出力スキーマ
class Evaluation(BaseModel):
    score: Literal[1, 2, 3, 4, 5]
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str
    keywords: list[str]


# レビュー評価関数
def evaluate_review(review: str) -> dict:
    review = review.strip()

    # 入力検証
    if not review:
        return {"ok": False, "error": "empty"}
    if len(review) > MAX_REVIEW_CHARS:
        return {"ok": False, "error": "too_long"}

    # LLM呼び出し+出力の防御
    try:
        response = anthropic.messages.parse(
            # LLM呼び出し
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": review}],
            output_format=Evaluation,            
        )
    # 出力の検証エラーや接続エラーをハンドリング
    except ValidationError:
        return {"ok": False, "error": "invalid_output"}
    except APIConnectionError:
        return {"ok": False, "error": "connection"}
    except APIStatusError as e:
        if e.status_code < 500:
            raise
        return {"ok": False, "error": "server_error"}
    
    # 出力がトランケートされている場合のエラー処理
    if response.stop_reason == "max_tokens":
        return {"ok": False, "error": "truncated"}
    
    # 出力を辞書に変換して返す
    return{"ok": True, "evaluation": response.parsed_output.model_dump()}


# APIエンドポイント
# 初期画面
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# レビュー評価
@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json(silent=True) or {}
    review = data.get("review", "")
    if not isinstance(review, str):
        return {"ok": False, "error": "bad_request"}, 400

    return evaluate_review(review)


if __name__ == "__main__":
    app.run(debug=True, port=5000)