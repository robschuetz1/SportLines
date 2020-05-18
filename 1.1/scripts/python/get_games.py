import requests
import json
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
error_log = []
group_id = '80' #CFB ESPN Group ID

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

conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (2)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select substr(season_start,0,5), week from weeks where date('now') > date(week_start) and substr(season_start,0,5) = '2019' order by date(week_start)")
game_weeks = []
for x in query_results:
        game_weeks.append([x[0],x[1]])

for row in game_weeks:
        print(row)
        scores_url = 'https://www.espn.com/college-football/scoreboard?group=80&year=' + row[0] + '&week=' + row[1]
        scores_page_src = requests.get(scores_url)
        score_src_str = str(scores_page_src.content)
        games_info = []

        
        game_ids = get_game_ids(score_src_str)
        
        
        for id_no in game_ids:
            print(id_no)
            try: game_data = requests.get(game_url + id_no)
            except: print('awww shucks')
            
            j = game_data.json()
            
            try: zip_code = j.get("gameInfo").get("venue").get("address").get("zipCode")
            except: print('aww shucks, no ZIP!')

            try: attendance = j.get("gameInfo").get("attendance")
            except: print('aww shucks, no attendance!')

            try: date = j.get("header").get("competitions")[0].get("date")[:10]
            except: print('aww shucks, no date!')

            try: time = j.get("header").get("competitions")[0].get("date")[11:-1]
            except: print('aww shucks, no time!')

            try: neutral_site = j.get("header").get("competitions")[0].get("neutralSite")
            except: print('aww shucks, no neutral site distinction!')
            try:
                    for team in j.get("header").get("competitions")[0].get("competitors"):
                        if team.get("homeAway") == 'home':
                                home_team_id = team.get("id")
                                home_team_score = team.get("score")
                                home_team_rank = team.get("rank")
                        if team.get("homeAway") == 'away':
                                away_team_id = team.get("id")
                                away_team_score = team.get("score")
                                away_team_rank = team.get("rank")
            except:
                        print('Unable to get team data')
            try:
                    pc = j.get("pickcenter")[0]
                    over_under = pc.get("overUnder")
                    spread = str(pc.get("spread"))
                    if pc.get("homeTeamOdds").get("favorite") == False:
                            home_team_spread = spread.strip('-')
                    else:
                            home_team_spread = spread
                    home_team_spread_odds = pc.get("homeTeamOdds").get("spreadOdds")
                    home_team_ml = pc.get("homeTeamOdds").get("moneyLine")
                    if pc.get("awayTeamOdds").get("favorite") == False:
                            away_team_spread = spread.strip('-')
                    else:
                            away_team_spread = spread
                    away_team_spread_odds = pc.get("awayTeamOdds").get("spreadOdds")
                    away_team_ml = pc.get("awayTeamOdds").get("moneyLine")

            except:
                spread = 'No odds data available'

            if home_team_score != None:
                    games_info.append([group_id, id_no, row[0], row[1], date, time, zip_code, str(neutral_site), str(attendance), str(over_under), home_team_id, home_team_score, str(home_team_rank), str(home_team_spread), str(home_team_spread_odds), str(home_team_ml), away_team_id, away_team_score, str(away_team_rank),  str(away_team_spread), str(away_team_spread_odds), str(away_team_ml)])
        
        for x in games_info:
            try:
                    cursor.execute('INSERT INTO games values ("' + x[0] + '", "' + x[1] + '", "' + x[2] + '", "' + x[3] + '", "' + x[4] + '", "' + x[5] + '", "' + x[6] + '", "' + x[7] + '", "' + x[8] + '", "' + x[9] + '", "' + x[10] + '", "' + x[11] + '", "' + x[12] + '", "' + x[13] + '", "' + x[14] + '", "' + x[15] + '", "' + x[16] + '", "' + x[17] + '", "' + x[18] + '", "' + x[19] + '", "' + x[20] + '", "' + x[21] + '")')
                    print (x[1] + ' added succesfully')
            except:
                    error_log.append(x[1])
                    print (x[1] + ' failed to add')

conn.commit()
conn.close()
error_message  = 'The following games were not added: '
for error in error_log:
        error_message = error_message + error + ', '
if error_message != []:
        print (error_message[:-2])

        
    

