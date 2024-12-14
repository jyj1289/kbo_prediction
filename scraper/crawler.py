import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# URL setup
url_base = 'https://www.koreabaseball.com/Record/Crowd/{category}'
category = 'GraphDaily.aspx'
url = url_base.format(category=category)

# Requesting the data
req = requests.get(url)
html = req.text
soup = bs(html, 'html.parser')

# Finding the table with the class 'tData'
table = soup.find('table', attrs={'class': 'tData'})

# Extracting data from each row in the table
data = []
for row in table.select('tr.order'):
    cols = row.find_all('td')
    if cols:
        date = cols[0].text.strip()
        day_of_week = cols[1].text.strip()
        home_team = cols[2].text.strip()
        away_team = cols[3].text.strip()
        location = cols[4].text.strip()
        attendance = cols[5].text.strip()
        data.append([date, day_of_week, home_team, away_team, location, attendance])

# Converting list of data into a DataFrame
df = pd.DataFrame(data, columns=['Date', 'Day of Week', 'Home Team', 'Away Team', 'Location', 'Attendance'])

# Output to CSV
df.to_csv('kbo_attendance.csv', index=False)
print("CSV file has been created.")
