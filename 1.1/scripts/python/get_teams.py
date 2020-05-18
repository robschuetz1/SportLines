import requests
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
group_id = '80'

conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (2)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games where week is not null")

games = []
team_ids = []

for x in query_results:
    games.append(x[0])

try:
    query_results = cursor.execute("select distinct team_id from teams where group_id = '80'")
    for team in query_results:
        team_ids.append(team[0])
        
except:
    print ("couldn't grab the existing teams!")



team_info = []


for game_id in games:
    print (game_id)
    r = requests.get(game_url + game_id)
    j = r.json()
    jb = j.get("boxscore").get("teams")
    for team in jb:
        try:
            team_id = team.get("team").get("id")
            team_abbr = team.get("team").get("abbreviation")
            team_loc = team.get("team").get("location")
            team_name = team.get("team").get("name")
            
            team_info.append([team_id, team_abbr, team_loc, team_name])
        except:
            print ('Had an issue with ' + game_id)


team_count = 0

for team in team_info:
    flag = 0
    for y in team_ids:
        if y != team[0]:
            flag = 1
    if flag == 0:
        cursor.execute('insert into teams values("' + group_id + '", "' + team[0] + '", "' + team[1] + '", "' + team[2] + '", "' + team[3] + '")')
        #print('insert into teams values("' + group_id + '", "' + team[0] + '", "' + team[1] + '", "' + team[2] + '", "' + team[3] + '")')
        team_count = team_count + 1

print(str(team_count) + ' teams have been added to the database')

conn.commit()
conn.close()
