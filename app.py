from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

def load_menu():
    try:
        with open('menu.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("menu.json 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        print("menu.json 파일을 읽을 수 없습니다. JSON 형식을 확인하세요.")
        return []

menu = load_menu()

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    budget = data.get("budget", 0)

    # 예산이 0 이하로 들어오지 않도록 기본값 설정
    if budget <= 0:
        return jsonify({"error": "유효한 예산을 입력해주세요."}), 400

    # 예산 이하의 메뉴를 필터링
    options = [item for item in menu if item['price'] <= budget]

    # 추천 가능한 메뉴가 없을 때
    if not options:
        return jsonify({"name": "추천할 메뉴가 없습니다.", "price": 0})

    # 랜덤으로 메뉴 추천
    recommendation = random.choice(options)
    return jsonify(recommendation)

# 홈 페이지에 대한 라우트를 추가합니다
@app.route("/")
def home():
    return "Welcome to BurgerKing API!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
