import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

# 데이터 로드 및 전처리
attendance_data = pd.read_csv('./kbo_attendance.csv')
attendance_data['Date'] = pd.to_datetime(attendance_data['Date'], format='%Y/%m/%d')
attendance_data['Attendance'] = attendance_data['Attendance'].str.replace(',', '').astype(int)

# 특성 추출: 연도, 월, 일
attendance_data['Year'] = attendance_data['Date'].dt.year
attendance_data['Month'] = attendance_data['Date'].dt.month
attendance_data['Day'] = attendance_data['Date'].dt.day

# 범주형 데이터(구장)에 대한 원-핫 인코딩
encoder = OneHotEncoder(sparse_output=False)
location_encoded = encoder.fit_transform(attendance_data[['Location']])

# 모든 특성을 결합하여 입력 데이터 생성
features = np.concatenate([attendance_data[['Year', 'Month', 'Day']].values, location_encoded], axis=1)
target = attendance_data['Attendance']

# 데이터셋을 학습용과 테스트용으로 분리
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# 선형 회귀 모델 학습
model = LinearRegression()
model.fit(X_train, y_train)

def predict_attendance_with_probability(year, month, day, location):
    """
    특정 연도, 월, 일, 구장에 대한 예상 관중 수와 티켓팅 확률을 예측합니다.
    
    Parameters:
        year (int): 예측하려는 연도
        month (int): 예측하려는 월
        day (int): 예측하려는 일
        location (str): 예측하려는 구장
    
    Returns:
        tuple: 예측된 관중 수와 티켓팅 확률(0-100%)
    """
    # 입력 날짜와 구장에 대한 특성 벡터 생성
    location_vector = encoder.transform([[location]]).flatten()
    input_features = np.concatenate([[year, month, day], location_vector])

    # 모델을 사용하여 관중 수 예측
    predicted_attendance = model.predict([input_features])[0]

    # 관중 수를 기반으로 티켓팅 확률(퍼센트) 계산
    max_attendance = attendance_data['Attendance'].max()
    ticketing_probability = min(100, (predicted_attendance / max_attendance) * 100)
    ticketing_probability = max(0, ticketing_probability)  # 확률을 0~100 사이로 제한

    return predicted_attendance, ticketing_probability

# 사용 예시
if __name__ == "__main__":
    year, month, day, location = 2025, 8, 9, "사직"
    predicted_attendance, ticketing_probability = predict_attendance_with_probability(year, month, day, location)
    print(f"Predicted Attendance: {predicted_attendance:.2f}")
    print(f"Ticketing Probability: {ticketing_probability:.2f}%")