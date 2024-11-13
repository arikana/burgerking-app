from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
# CORS 설정: 모든 출처 허용 및 Preflight 요청(OPTIONS 메서드) 허용
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def load_menu():
    with open('menu.json', 'r', encoding='utf-8') as file:
        return json.load(file)

menu = load_menu()

@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    # Preflight 요청에 대한 응답 처리
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # POST 요청 처리
    data = request.get_json()
    budget = data.get("budget", 0)

    options = [item for item in menu if item['price'] <= budget]

    if not options:
        return jsonify({"name": "추천할 메뉴가 없습니다.", "price": 0})

    recommendation = random.choice(options)
    return jsonify(recommendation)

@app.route("/")
def home():
    return "Welcome to BurgerKing API!"

if __name__ == "__main__":
    app.run(debug=True)
