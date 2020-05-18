import requests
import json
import sqlite3
week = 7
game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
scores_url = 'https://www.espn.com/college-football/scoreboard?group=80&week=' + str(week)
scores_page_src = requests.get(scores_url)
score_src_str = str(scores_page_src.content)
games_info = []

def get_game_ids(page_source):
	s = 'college-football/game/_/gameId/'
	str_len = len(s)
	game_ids = []
	start_pos = 0
	while 1 == 1:
		result = page_source.find(s,start_pos)
		if result != -1:
			game_ids.append(page_source[result + str_len : result + str_len + 9])
			start_pos = result + 1
		else:
			break
	return game_ids


game_ids = get_game_ids(score_src_str)


for id_no in game_ids:
    teams = []
    game_data = requests.get(game_url + id_no)
    for team in game_data.json().get("boxscore").get("teams"):
        teams.append(team.get("team").get("displayName"))
    try:
        spread = game_data.json().get("pickcenter")[0].get("details")
    except:
        spread = 'No spread available'
    games_info.append([id_no, teams, spread])


if games_info != []:
        conn = sqlite3.connect('C:\Program Files\sport_lines\sqlite3\sport_lines.db')
        cursor = conn.cursor()

for x in games_info:
    try:
            cursor.execute('INSERT INTO games (espn_id, home_team, away_team, spread) VALUES (' + x[0] + ', "' + x[1][0] + '", "' + x[1][1] + '", "' + x[2] + '")')
            print (x[0] + ' added succesfully')
    except:
            print (x[0] + ' failed to add')

conn.commit()
conn.close()

        
    

