import requests
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='

rush_play_types = ['Rush', 'Rushing Touchdown', 'Sack', 'Safety', 'Fumble Recovery (Own)']
pass_play_types = ['Pass Incompletion','Pass Reception', 'Passing Touchdown']
eop = ['End Period','End of Half']
penalty = ['Penalty']
turnover = ['Fumble Recovery (Opponent)','Pass Interception Return', 'Interception Return Touchdown','Defensive 2pt Conversion','Fumble Return Touchdown']
special_teams = ['Kickoff', 'Missed Field Goal Return Touchdown', 'Field Goal Missed', 'Field Goal Good', 'Missed Field Goal Return', 'Punt', 'Blocked Punt', 'Blocked Field Goal', 'Punt Return Touchdown', 'Kickoff Return (Offense)', 'Kickoff Return Touchdown']

conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (1)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games where week in (1)")
games = []

for x in query_results:
    games.append(x[0])

def get_plays(drive_data):
    for drive in drive_data:
        drive_id = drive.get("id")
        plays = drive.get("plays")
        for play in plays:
            team_id = play.get("start").get("team").get("id")
            play_id = play.get("id")
            play_type = play.get("type").get("text")
            quarter = play.get("period").get("number")
            clock = play.get("clock").get("displayValue")
            scoring_play = play.get("scoringPlay")
            if play.get("text").lower().find('penalty') != -1:
                has_penalty = 1
            else:
                has_penalty = 0
            down = play.get("start").get("down")
            distance = play.get("start").get("distance")
            start_yard_line = play.get("start").get("yardLine")
            end_yard_line = play.get("end").get("yardLine")
            yardage = play.get("statYardage")
            if play_type in rush_play_types:
                play_category = 'Rush'
            if play_type in pass_play_types:
                play_category = 'Pass'
            if play_type in eop:
                play_category = 'End of Period'
            if play_type in turnover:
                play_category = 'Turnover'
            if play_type in special_teams:
                play_category = 'Special Teams'
            if play_type == 'Penalty':
                play_category = 'Penalty'

            plays_to_add.append([drive_id, team_id, play_id, play_category, str(quarter), clock, str(down), str(distance), str(scoring_play), str(start_yard_line), str(end_yard_line), str(yardage)])    


for game_id in games:
    plays_to_add = []
    r = requests.get(game_url + game_id)
    j = r.json()
    jd = j.get("drives").get("previous")
    try:
        get_plays(jd)
        print(game_id)
        for play in plays_to_add:
            cursor.execute('insert into plays values("' + play[0] + '", "' + play[1] + '", "' + play[2] + '", "' + play[3] + '", "' + play[4] + '", "' + play[5] + '", "' + play[6] + '", "' + play[7] + '", "' + play[8] + '", "' + play[9] + '", "' + play[10] + '", "' + play[11] + '")')
    except:
        print(game_id + ' bleh')

conn.commit()
conn.close()
