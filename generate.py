from datetime import datetime, timedelta
import json

# Define teams and locations
teams = ["롯데", "NC", "두산", "LG", "KIA", "한화", "삼성", "SSG", "KT", "키움"]
locations = {
    "롯데": "사직",
    "NC": "창원",
    "두산": "잠실",
    "LG": "잠실",
    "KIA": "광주",
    "한화": "대전",
    "삼성": "대구",
    "SSG": "문학",
    "KT": "수원",
    "키움": "고척"
}

# Initialize variables
start_date = datetime(2025, 3, 22)
end_date = datetime(2025, 5, 31)

# Generate schedule
schedule = {}
current_date = start_date

while current_date <= end_date:
    if current_date.weekday() != 0:  # Exclude Mondays
        month_key = current_date.strftime("%Y-%m")
        if month_key not in schedule:
            schedule[month_key] = []
        
        # Assign matches (3-day cycles)
        for i in range(0, len(teams), 2):  # Pair teams in order
            home_team = teams[i]
            away_team = teams[i + 1]
            match = {
                "date": current_date.strftime("%Y-%m-%d"),
                "home_team": home_team,
                "away_team": away_team,
                "location": locations[home_team]
            }
            schedule[month_key].append(match)
    
    # Move to the next day
    current_date += timedelta(days=1)
    # Rotate teams every 3 days
    if (current_date - start_date).days % 3 == 0:
        teams = teams[1:] + teams[:1]  # Rotate the list of teams

# Save to JSON file
json_output_path = "./data/kbo_schedule.json"
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=4)
