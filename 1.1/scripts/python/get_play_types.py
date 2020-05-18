import requests
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
play_types = []

conn = sqlite3.connect('C:\\users\\rschuetz\\documents\\sport_lines\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games where week in (1,2,3)")
games = []
for x in query_results:
    games.append(x[0])

def get_play_types(drive):
    for x in jd:
        plays = x.get("plays")
        for play in plays:
                play_type = play.get("type").get("text")
                present = 0
                for z in play_types:
                    if play_type == z:
                        present = 1
                if present == 0:
                    play_types.append(play_type)

for x in games:
    r = requests.get(game_url + x)
    j = r.json()
    jd = j.get("drives").get("previous")
    try:
        get_play_types(jd)
    except:
        print('bleh')
