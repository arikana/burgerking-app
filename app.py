from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
# 모든 출처에서의 CORS 허용
CORS(app, resources={r"/recommend": {"origins": "*"}})

def load_menu():
    with open('menu.json', 'r', encoding='utf-8') as file:
        return json.load(file)

menu = load_menu()

@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    # Preflight 요청 처리
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # POST 요청 처리
    data = request.get_json()
    budget = data.get("budget", 0)

    # 예산 이하의 메뉴 필터링
    options = [item for item in menu if item['price'] <= budget]

    # 추천 가능한 메뉴가 없는 경우
    if not options:
        return jsonify({"name": "추천할 메뉴가 없습니다.", "price": 0})

    # 랜덤 메뉴 추천
    recommendation = random.choice(options)
    return jsonify(recommendation)

@app.route("/")
def home():
    return "Welcome to BurgerKing API!"

if __name__ == "__main__":
    app.run(debug=True)
