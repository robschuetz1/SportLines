import requests
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
group_id = '80'

rush_play_types = ['Rush', 'Rushing Touchdown', 'Sack', 'Safety', 'Fumble Recovery (Own)']
pass_play_types = ['Pass Incompletion','Pass Reception', 'Passing Touchdown']
eop = ['End Period','End of Half']
penalty = ['Penalty']
turnover = ['Fumble Recovery (Opponent)','Pass Interception Return', 'Interception Return Touchdown','Defensive 2pt Conversion','Fumble Return Touchdown']
special_teams = ['Kickoff', 'Missed Field Goal Return Touchdown', 'Field Goal Missed', 'Field Goal Good', 'Missed Field Goal Return', 'Punt', 'Blocked Punt', 'Blocked Field Goal', 'Punt Return Touchdown', 'Kickoff Return (Offense)', 'Kickoff Return Touchdown']
other = ['Coin Toss']
categories = [[rush_play_types, 'Rush'], [pass_play_types, 'Pass'], [eop, 'End of Period'], [penalty, 'Penalty'], [turnover, 'Turnover'], [special_teams, 'Special Teams'], [other, 'Other']]
              
conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (2)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games where week in ('1','2','3','4','5','6','7')")
games = []
errors = []




def get_adj_yardage(play):
    if (play.get("text").lower().find('penalty') != -1 and play.get("type").get("text") != 'Penalty') or play.get("text").lower().find('fumble') != -1:
        search_strings = ['yds','yards','yd', 'yard', 'no gain','incomplete']
        play_info = [play.get("id"), play.get("type").get("text"), play.get("text").lower()]
        flag = 0
        position = []
        for s in search_strings:
            if play_info[2].find(s) != -1:
                try:
                    pos = play_info[2].find(s)
                    if s in ['no gain', 'incomplete']:
                        value = 0
                    else:
                        value = int(play_info[2][pos - 3: pos - 1].strip(' '))
                    flag = 1
                    position.append([pos, value])
                except:
                    pass
        if flag == 0:
            errors.append(play_info[2])
            is_error = 1
        else:
            is_error = 0
    
        first_pos = len(play_info[2])
        for p in position:
                if p[0] < first_pos:
                        first_pos = p[0]
                        final_value = p[1]
    
        if play_info[2][:first_pos].find('loss') != -1:
                final_value = -final_value
    
        return final_value


def get_plays(drive_data):
    for drive in drive_data:
        drive_id = drive.get("id")
        plays = drive.get("plays")
        for play in plays:
            print(play.get("id"))
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
            for c in categories:
                if play_type in c[0]:
                    play_category = c[1]
                if play.get("text").lower().find('fumble') != -1:
                    play_category = 'Turnover'
            if play_category in ('Other','Special Teams'):
                adj_yardage = yardage
            else:
                if str(get_adj_yardage(play)) != 'None':
                    adj_yardage = get_adj_yardage(play) #excludes penatly yards from yards gained/lossed
                else:
                    adj_yardage = yardage
            if play.get("text").lower().find('timeout') != -1:
                timeout_flag = 1
            else:
                timeout_flag = 0
            desc = play.get("text").lower()

            if timeout_flag == 0:
                plays_to_add.append([group_id, drive_id, team_id, play_id, play_category, str(quarter), clock, str(down), str(distance), str(scoring_play), str(start_yard_line), str(end_yard_line), str(adj_yardage), str(yardage), desc])
                #print ([drive_id, team_id, play_id, play_category, str(quarter), clock, str(down), str(distance), str(scoring_play), str(start_yard_line), str(end_yard_line), str(adj_yardage), str(yardage), desc])

for x in query_results:
    games.append(x[0])

play_count = 0
for game_id in games:
    plays_to_add = []
    r = requests.get(game_url + game_id)
    j = r.json()
    try:
        jd = j.get("drives").get("previous")
        get_plays(jd)
        print(game_id)
        for play in plays_to_add:
            play_count = play_count + 1
            cursor.execute('insert into plays values("' + play[0] + '", "' + play[1] + '", "' + play[2] + '", "' + play[3] + '", "' + play[4] + '", "' + play[5] + '", "' + play[6] + '", "' + play[7] + '", "' + play[8] + '", "' + play[9] + '", "' + play[10] + '", "' + play[11] + '", "' + play[12] + '", "' + play[13] + '", "' + play[14] + '")')
            #print('insert into plays values("' + play[0] + '", "' + play[1] + '", "' + play[2] + '", "' + play[3] + '", "' + play[4] + '", "' + play[5] + '", "' + play[6] + '", "' + play[7] + '", "' + play[8] + '", "' + play[9] + '", "' + play[10] + '", "' + play[11] + '", "' + play[12] + '", "' + play[13] + '")')
    except:
        print(game_id + ' bleh')

conn.commit()
conn.close()

print(str(play_count) + ' plays were added')
