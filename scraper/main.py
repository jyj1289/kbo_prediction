from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from analyze import predict_attendance
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 요청 데이터 파싱
        data = request.get_json()
        date_str = data.get('date')  # ISO 8601 형식 날짜 (예: "2025-10-11")
        location = str(data.get('location'))
        home_team = str(data.get('home_team'))
        away_team = str(data.get('away_team'))
        
        # 날짜 변환 및 유효성 검증
        try:
            date = pd.Timestamp(date_str)  # ISO 8601 문자열을 Timestamp로 변환
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        # 예측 수행
        predicted_attendance, ticketing_probability = predict_attendance(
            date, location, home_team, away_team
        )
        
        # 응답 생성
        response = {
            "predicted_attendance": round(predicted_attendance),
            "ticketing_probability": round(ticketing_probability, 2)
        }
        return jsonify(response), 200
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
