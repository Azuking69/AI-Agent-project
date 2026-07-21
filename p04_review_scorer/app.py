from typing import Literal
from flask import Flask, render_template
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel


load_dotenv()

app = Flask(__name__)
anthropic = Anthropic()


# 出力スキーマ
class Evaluation(BaseModel):
    score: Literal[1, 2, 3, 4, 5]
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str
    keywords: list[str]


# システムプロンプト
SYSTEM_PROMPT = """
あなたは飲食店のレビューを分析し、星(1〜5)と感情を判定する評価の専門家です。

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
- 要約は一文で要点だけを書く。
- キーワードは星評価の根拠となった表現をレビューから3個前後抜き出す。

"""

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)