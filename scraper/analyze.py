import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from datetime import datetime

# Load the CSV data
attendance_data = pd.read_csv("./kbo_attendance.csv")

# Data preprocessing
attendance_data['Date'] = pd.to_datetime(attendance_data['Date'], format='%Y/%m/%d', errors='coerce')
attendance_data['Attendance'] = pd.to_numeric(attendance_data['Attendance'].str.replace(',', ''), errors='coerce')

# Creating additional features
attendance_data['Year'] = attendance_data['Date'].dt.year
attendance_data['Month'] = attendance_data['Date'].dt.month
attendance_data['Day'] = attendance_data['Date'].dt.day
attendance_data['Matchup'] = attendance_data['Home Team'] + ' vs ' + attendance_data['Away Team']

# Handling missing values
attendance_data.dropna(subset=['Date', 'Attendance', 'Location', 'Home Team', 'Away Team'], inplace=True)

# One-hot encoding for categorical features
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_features = attendance_data[['Location', 'Matchup']]
encoded_features = encoder.fit_transform(categorical_features)

# Combining features for the model
features = np.concatenate([
    attendance_data[['Year', 'Month', 'Day']].values,
    encoded_features
], axis=1)
target = attendance_data['Attendance']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Function to predict attendance and ticketing probability
def predict_attendance(date, location, home_team, away_team):
    year, month, day = date.year, date.month, date.day
    matchup = f"{home_team} vs {away_team}"
    
    input_data = pd.DataFrame({
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'Location': [location],
        'Matchup': [matchup]
    })
    
    encoded_input = encoder.transform(input_data[['Location', 'Matchup']])
    input_features = np.concatenate([
        input_data[['Year', 'Month', 'Day']].values,
        encoded_input
    ], axis=1)
    
    # Predict attendance
    predicted_attendance = model.predict(input_features)[0]
    max_attendance = attendance_data['Attendance'].max()
    
    # Calculate raw ticketing probability
    raw_ticketing_probability = max(0, 100 * (1 - (predicted_attendance / max_attendance)))
    
    # Adjust ticketing probability to range [40, 85]
    ticketing_probability = 40 + (raw_ticketing_probability * 0.45)
    ticketing_probability = min(85, max(40, ticketing_probability))  # Ensure within range
    
    return predicted_attendance, ticketing_probability



# Example usage
example_date = pd.Timestamp('2025-08-21')
example_location = "사직"
example_home_team = "롯데"
example_away_team = "삼성"

predicted_attendance, ticketing_probability = predict_attendance(
    example_date, example_location, example_home_team, example_away_team
)
print(f"Predicted Attendance: {predicted_attendance}")
print(f"Ticketing Probability: {ticketing_probability}%")
