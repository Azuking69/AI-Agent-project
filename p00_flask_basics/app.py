from flask import Flask, render_template, request

#  １）アプリ作成
app= Flask(__name__)

#  ３）ルーティング
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', name="AI Agent 수강생")

#  ２）起動
if __name__ == '__main__':
    app.run(debug=True, port=5000)
