import pandas as pd
import json

# Load the CSV file
file_path = './kbo_attendance.csv'
df = pd.read_csv(file_path)

# Remove commas and convert 'Attendance' column to numeric
df['Attendance'] = df['Attendance'].replace({',': ''}, regex=True).astype(int)

# Group by 'Location' and 'Day of Week', and calculate the mean attendance
average_attendance = df.groupby(['Location', 'Day of Week'])['Attendance'].mean().unstack()

# Convert the result to a dictionary format
average_attendance_json = {}
for stadium, row in average_attendance.iterrows():
    average_attendance_json[stadium] = {
        '화': round(row.get('화', 0) if not pd.isna(row.get('화', 0)) else 0),
        '수': round(row.get('수', 0) if not pd.isna(row.get('수', 0)) else 0),
        '목': round(row.get('목', 0) if not pd.isna(row.get('목', 0)) else 0),
        '금': round(row.get('금', 0) if not pd.isna(row.get('금', 0)) else 0),
        '토': round(row.get('토', 0) if not pd.isna(row.get('토', 0)) else 0),
        '일': round(row.get('일', 0) if not pd.isna(row.get('일', 0)) else 0)
    }

# Save the JSON to a file
output_path = 'attendance_mean.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(average_attendance_json, json_file, ensure_ascii=False, indent=4)

print(f"Average attendance JSON saved to {output_path}")
