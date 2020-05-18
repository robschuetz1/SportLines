import requests
import json
import sqlite3
import datetime from datetime

today = datetime.now()

scores_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?group=80'
data = requests.get(scores_url)
j_data = data.json()
current_season = [datetime.strptime((j_data.get("leagues")[0].get("season").get("startDate"))[:10],'%Y-%m-%d'),datetime.strptime((j_data.get("leagues")[0].get("season").get("endDate"))[:10],'%Y-%m-%d')]
current_week = j_data.get("week").get("number")

if current_season[0] < datetime.now() < current_season[1]:
    conn = sqlite3.connect('C:\Program Files\sport_lines\sqlite3\sport_lines.db')
    cursor = conn.cursor()
    query_results = cursor.execute("select week from cfb_weeks limit 1 order by year desc, week")
    try:
        for x in query_results:
            if x[0] != current_season[0] or x[2] != current_week:
                cursor.execute("insert into cfb_weeks values (" + str(current_season[0]) + ", " + str(current_season[1]) + ", " + str(current_week) + ")")
                print ('Week ' + str(current_week) + ' of the ' + str(current_season[0].year) + ' - ' + str(current_season[1].year) + ' season has been added!')
            else:
                print ('No need to add any weeks')
    except:
            print ('There was an error assessing the need to add week ' + str(current_week) + ' of the ' + str(current_season[0].year) + ' ' + str(current_season[1].year) + ' season')

conn.commit()
conn.close()
