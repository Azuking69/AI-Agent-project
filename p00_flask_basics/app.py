from flask import Flask, render_template, request

#  １）アプリ作成
app= Flask(__name__)

#  ３）ルーティング
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', name="AI Agent 수강생")

@app.route("/hello", methods=['GET'])
def hello():
    return "안녕하세요! 이건 문자열을 그대로 돌려주는 가장 단순한 라우트입나다."

@app.route("/greet/<name>", methods=['GET'])
def greet(name):
    return f"{name}님, 반갑습니다!"

@app.route("/add", methods=['GET'])
def add():
    # args： クエリパラメータ(a, b)を取得するための辞書
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)

    if a is None or b is None:
        return {"error": "정수 쿼리 파라미터 a, b가 모두 필요합니다."}, 400
    
    return {"a": a, "b": b, "sum": a + b}
    
@app.route("/echo", methods=['POST'])
def echo():
    data = request.get_json(silent=True)or{}
    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return {"error": "text 필드(문자열)가 필요합니다."}, 400
        
    return {"echo": text, "length": len(text)}

#  ２）起動
if __name__ == '__main__':
    app.run(debug=True, port=5000)
