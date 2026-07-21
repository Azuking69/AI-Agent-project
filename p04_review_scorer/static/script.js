// HTMLを分離して、JavaScriptを整理する
// 変数定義
const fileInput = document.getElementById("file");
const reviewInput = document.getElementById("review");
const evBtn = document.getElementById("evBtn");
const result = document.getElementById("result");

// 1. ファイル読み取り
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  // ファイルが選択されていない場合は何もしない
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    reviewInput.value = reader.result;
  };
  reader.readAsText(file, "UTF-8");
});

// 2. エラーメッセージ
const ERROR_MESSAGES = {
  empty: "テキストが空です。",
  too_long: "テキストが長すぎます。もう少し短くしてください。",
  invalid_output: "評価結果の形式が正しくありません。もう一度お試しください。",
  truncated: "応答が途中で切れました。もう一度お試しください。",
  connection:
    "サーバーに接続できませんでした。しばらくしてからもう一度お試しください。",
  server_error:
    "一時的なサーバーエラーです。しばらくしてからもう一度お試しください。",
  bad_request: "リクエストの形式が正しくありません。",
};

// 3. 評価ボタンをクリックしたときの処理
evBtn.addEventListener("click", async () => {
  const review = reviewInput.value;
  // innerHTML: Webページ上のHTML要素の中身を取得したり、
  // 新しい内容に書き換えたりするためのJSのプロパティ
  result.innerHTML = "<p class='hint'>レビューを分析中…</p>";
  // 評価ボタンを無効化して、連打を防止
  evBtn.disabled = true;

  try {
    // fetch APIを使って、FlaskサーバーにレビューをJSON形式で送信
    const response = await fetch("/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ review }),
    });

    const data = await response.json();

    // data.okがtrueならrenderResultを呼び出し、
    // falseならrenderErrorを呼び出す
    result.innerHTML = data.ok
      ? renderResult(data.evaluation)
      : renderError(data.error);
  } catch (error) {
    result.innerHTML = renderError("connection");
  } finally {
    evBtn.disabled = false;
  }
});

// 4. レビュー評価結果をHTMLにレンダリングする関数
function renderResult(evaluation) {
  const stars = "★".repeat(evaluation.score) + "☆".repeat(5 - evaluation.score);
  // キーワードの配列をHTMLのspanタグで囲んで、スペースで結合する
  const keywords = evaluation.keywords
    .map((k) => `<span>${escapeHtml(k)}</span>`)
    .join(" ");
  return `
    <div class="card">
        <div class="stars">${stars} <small>(${evaluation.score}/5)</small>
            <span class="badge ${evaluation.sentiment}">${evaluation.sentiment}</span>
        </div>
        <p class="summary"><b>要約:</b> · ${escapeHtml(evaluation.summary)}</p>
        <div class="keywords"><b>キーワード:</b> ${keywords}</div>
    </div>
    `;
}

// 5. エラーメッセージをレンダリングする関数
function renderError(code) {
  const message = ERROR_MESSAGES[code] || "不明なエラーが発生しました。";
  return `<p class="error">⚠ ${message} <small>(${code})</small></p>`;
}

// 6. LLMの出力をHTMLに安全に表示するための関数
function escapeHtml(escapeStr) {
  const div = document.createElement("div");
  div.textContent = escapeStr;
  return div.innerHTML;
}
