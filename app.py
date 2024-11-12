from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

def load_menu():
    with open('menu.json', 'r', encoding='utf-8') as file:
        return json.load(file)

menu = load_menu()

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    budget = data.get("budget", 0)

    # 예산 이하의 메뉴를 필터링
    options = [item for item in menu if item['price'] <= budget]

    # 추천 가능한 메뉴가 없을 때
    if not options:
        return jsonify({"name": "추천할 메뉴가 없습니다.", "price": 0})

    # 랜덤으로 메뉴 추천
    recommendation = random.choice(options)
    return jsonify(recommendation)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
