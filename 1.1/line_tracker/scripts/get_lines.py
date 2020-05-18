import datetime
import requests
import sqlite3

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

def get_timestamp(str_time):
	month = str_time[:str_time.find('/')]
	if len(month) == 1:
		month = '0' + month
	day = str_time[str_time.find('/') + 1:str_time.find(' ')]
	if len(day) == 1:
		day = '0' + day
	if month == '01':
		year = '2020'
	else:
		year = '2019'

	hour = kickoff[kickoff.find(' ', kickoff.find(' ') + 1) + 1:kickoff.find(':')]
	if kickoff.find('PM') != -1 and hour != '12':
		hour = str(int(hour) + 12)
	minute = kickoff[kickoff.find(':') + 1: kickoff.find(' ', kickoff.find(':'))]
	time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':00'
	return time    


now = datetime.datetime.now() + datetime.timedelta(hours = 5)
now_s = now.strftime('%Y-%m-%d %H:%M:%S')
game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
group_id = '80' #CFB ESPN Group ID
scores_url = 'https://www.espn.com/college-football/scoreboard?group=80&year=2019&week=Bowls'
db_path = r'C:/Users/RSchuetz/Dropbox/Projects/Sport Lines/CFB/1.1/line_tracker/historical_lines.db'
db_game_ids = []
games_to_add = []
error_log = []

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games")
for x in query_results:
        db_game_ids.append(x[0])
        
print("Here are the db games:")
for game_id in db_game_ids:
        print(game_id)

scores_page_src = requests.get(scores_url)
score_src_str = str(scores_page_src.content)
c_game_ids = get_game_ids(score_src_str)

print("Here are the ESPN games:")
for game_id in c_game_ids:
        print(game_id)


for c in c_game_ids:
    i = 0
    for d in db_game_ids:
        if d == c:
            i = 1
    if i == 0:
        games_to_add.append(c)
        print(c + ' is a new game_id')

for game_id in games_to_add:
    r = requests.get(game_url + game_id)
    kickoff = r.json().get('header').get('competitions')[0].get('status').get('type').get('shortDetail')
    if kickoff != 'Final':
        print("insert into games values ('" + game_id + "', '" + get_timestamp(kickoff) + "')")
        cursor.execute("insert into games values ('" + game_id + "', '" + get_timestamp(kickoff) + "')")

conn.commit()

                           
games_info = []

query = 'select * from games'
query_results = cursor.execute(query)
for x in query_results:
        games_info.append([x[0], x[1]])

for game in games_info:
    go_flag = 0
    kickoff = datetime.datetime.strptime(game[1], '%Y-%m-%d %H:%M:%S')
    t_dif = kickoff - now
    print (t_dif.days, t_dif.seconds, 'TDIF 30_min: ', t_dif.seconds % 1800, '   ', 'TDIF 3 hours: ', t_dif.seconds % 10800)
    if t_dif.days == 0 and t_dif.seconds < 7200:
            go_flag = 1
    if t_dif.days == 0 and t_dif.seconds > 7200 and (t_dif.seconds % 1800) - 300 < 0:
            go_flag = 1
    if t_dif.days > 0 and (t_dif.seconds % 10800) - 300 < 0:
            go_flag = 1

    if go_flag == 1:
            print ('Grabbing the lines for game ' + game[0])

            r = requests.get(game_url + game[0])
            for line in r.json().get('pickcenter'):
                error_flag = 0
                try:
                    odd_maker = line.get('provider').get('name')
                    try:
                        spread = abs(float(line.get('spread')))
                    except:
                        spread = 0
                    flag = 0
                    favorite_id = 0
                    home_team_id = line.get('homeTeamOdds').get('teamId')
                    away_team_id = line.get('awayTeamOdds').get('teamId')
                    if line.get('awayTeamOdds').get('favorite') == True:
                        favorite_id = line.get('awayTeamOdds').get('teamId')
                        spread_odds = line.get('awayTeamOdds').get('spreadOdds')
                        money_line = abs(float(line.get('awayTeamOdds').get('moneyLine')))
                        flag = 1
                    if line.get('homeTeamOdds').get('favorite') == True:
                        favorite_id = line.get('homeTeamOdds').get('teamId')
                        spread_odds = line.get('homeTeamOdds').get('spreadOdds')
                        money_line = abs(float(line.get('homeTeamOdds').get('moneyLine')))
                        flag = 1
                    if flag == 0:
                        money_line = 0
                        spread_odds = 0
                except:
                    favorite_id = 0
                    spread_odds = 0
                    money_line = 0
                    error_flag = 1

                try:
                    cursor.execute("insert into lines values ('" + game[0] + "', '" + home_team_id +  "', '" + away_team_id + "', '" + odd_maker + "', '" + favorite_id + "', " + str(spread)+ ", " + str(spread_odds) + ", " + str(money_line) + ", " + str(error_flag) + ", '" + now_s + "')")
                except:
                    cursor.execute("insert into lines (game_id, fail_flag) values ('"  + game[0] + "', 1)")
                    print (game[0] + ' did not go through')


conn.commit()
conn.close()
    


