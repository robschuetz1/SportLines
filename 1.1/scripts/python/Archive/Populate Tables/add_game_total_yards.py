import requests
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='

conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (2)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games")
games = []

game_totals = []

for x in query_results:
    games.append(x[0])

for game_id in games:
    r = requests.get(game_url + game_id)
    j = r.json()
    jb = j.get("boxscore").get("teams")
    for team in jb:
        try:
            team_id = team.get("team").get("id")
            for stat in team.get("statistics"):
                if stat.get("name") ==  'completionAttempts':
                    total_pass_attempts = stat.get("displayValue")[-2:]
                if stat.get("name") ==  'netPassingYards':
                    total_pass_yards = stat.get("displayValue")
                if stat.get("name") ==  'rushingAttempts':
                    total_rush_attempts = stat.get("displayValue")
                if stat.get("name") ==  'rushingYards':
                    total_rush_yards = stat.get("displayValue")
                if stat.get("name") ==  'possessionTime':
                    time_of_possession = stat.get("displayValue")
            game_totals.append([game_id, team_id, total_pass_attempts, total_pass_yards, total_rush_attempts, total_rush_yards, time_of_possession])
        except:
            print ('Had an issue with ' + game_id)

for game in game_totals:
    cursor.execute('insert into game_yard_totals values("' + game[0] + '", "' + game[1] + '", "' + game[2] + '", "' + game[3] + '", "' + game[4] + '", "' + game[5] + '", "' + game[6] + '")')
    #print('insert into game_yard_totals values("' + game[0] + '", "' + game[1] + '", "' + game[2] + '", "' + game[3] + '", "' + game[4] + '", "' + game[5] + '", "' + game[6] + '")')


conn.commit()
conn.close()
