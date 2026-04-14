"""
app.py — Nova Chatbot · Flask Entry Point
Run: python app.py  →  open http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify, render_template
from chatbot.logic import generate_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"reply": "I didn't receive a proper message."}), 400
    user_input = data["message"].strip()
    if not user_input:
        return jsonify({"reply": "You sent an empty message!"}), 200
    return jsonify({"reply": generate_response(user_input)}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)