from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack", methods=["POST"])
def handle_slash_command():
    data = request.form
    company_name = data.get("text")

    response_text = f"🔍 会社名「{company_name}」で検索します！（ここにDrive検索結果が入ります）"

    return jsonify({
        "response_type": "in_channel",
        "text": response_text
    })

if __name__ == "__main__":
    app.run(port=5000)
