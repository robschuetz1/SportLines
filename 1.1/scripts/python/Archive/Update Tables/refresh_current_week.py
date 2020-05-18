import requests
import json
import sqlite3
from datetime import datetime

def increment_id(s):
	    output = int(s[len(s)-5:]) + 1
	    output = str(output)
	    while len(output) < 5:
	        output = '0' + output
	    return output

today = datetime.now()

group_id = '80' #ESPN CFB Group ID
scores_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?group=' + group_id
data = requests.get(scores_url)
j_data = data.json()
current_season = [datetime.strptime((j_data.get("leagues")[0].get("season").get("startDate"))[:10], '%Y-%m-%d'),datetime.strptime((j_data.get("leagues")[0].get("season").get("endDate"))[:10], '%Y-%m-%d')]
current_season_str = [(j_data.get("leagues")[0].get("season").get("startDate"))[:10],(j_data.get("leagues")[0].get("season").get("endDate"))[:10]]
current_week = j_data.get("week").get("number")
for calendar in j_data.get("leagues")[0].get("calendar"):
    for entry in calendar.get("entries"):
        if int(entry.get("value")) == current_week:
            current_week_range = [entry.get("startDate")[:10], entry.get("endDate")[:10]]


conn = sqlite3.connect('C:\Program Files\sport_lines\sqlite3\sport_lines.db')
cursor = conn.cursor()

if current_season[0] < datetime.now() < current_season[1]:
    query_results = cursor.execute("select week_id, season_start, week_start from weeks where group_id = " + group_id + " order by season_start desc, week_start desc limit 1")
    try:
        for x in query_results:
            if x[1] != current_season_str[0] or datetime.strptime(x[2],'%Y-%m-%d') < datetime.strptime(current_week_range[1],'%Y-%m-%d'):
                print ("insert into weeks values ('" + str(group_id) + "-" + increment(x[0]) + "', " + group_id + ", '" + current_season_str[0] + "', '" + current_season_str[1] + "', '" + str(current_week) + + "', '" + current_week_range[0] + "', '" + current_week_range[1] +  "')")
                cursor.execute("insert into weeks values ('" + str(group_id) + "-" + increment(x[0]) + "', " + group_id + ", '" + current_season_str[0] + "', '" + current_season_str[1] + "', '" + str(current_week) + + "', '" + current_week_range[0] + "', '" + current_week_range[1] +  "')")
                print ('Week ' + str(current_week) + ' of the ' + str(current_season[0].year) + ' - ' + str(current_season[1].year) + ' season has been added!')
            else:
                print ('No need to add any weeks')
    except:
            print ('There was an error assessing the need to add week ' + str(current_week) + ' of the ' + str(current_season[0].year) + ' - ' + str(current_season[1].year) + ' season')

conn.commit()
conn.close()
