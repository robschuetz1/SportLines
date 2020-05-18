import requests
import json
import sqlite3

game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event='
error_log = []
group_id = '80' #CFB ESPN Group ID


conn = sqlite3.connect('C:\\users\\rschuetz\\downloads\\sport_lines (2)\\sport_lines\\\sqlite3\\sport_lines.db')
cursor = conn.cursor()
query_results = cursor.execute("select game_id from games where week in ('4','5','6','7')")
games = []
for x in query_results:
        games.append(x[0])


for game_id in games:
        team_info = []
        drive_info = []
        fail = 0
        
        try:
                game_data = requests.get(game_url + game_id)
                j = game_data.json()
                for team in j.get("boxscore").get("teams"):
                        team_info.append([team.get("team").get("abbreviation"), team.get("team").get("id")])
                drives = j.get("drives").get("previous")

                for drive in drives:
                        drive_id = drive.get("id")

                        for team in team_info:
                                if team[0] == drive.get("team").get("abbreviation"):
                                        team_id = team[1]
                        start_time = drive.get("start").get("clock").get("displayValue")
                        start_quarter = drive.get("start").get("period").get("number")
                        try:
                                end_time = drive.get("end").get("clock").get("displayValue")
                        except:
                        	end_time = '0:00'
                        end_quarter = drive.get("end").get("period").get("number")
                        play_count = drive.get("offensivePlays")
                        yards_to_go = drive.get("start").get("yardLine")
                        if drive.get("start").get("text").find(drive.get("team").get("abbreviation")) != -1 and drive.get("start").get("yardLine") < 50:
                                yards_to_go = 100 - drive.get("start").get("yardLine")
                        else:
                                yards_to_go = drive.get("start").get("yardLine")
                        yards = drive.get("yards")
                        result = drive.get("result")
                        drive_info.append([group_id, game_id, drive_id, team_id, str(start_quarter), start_time, str(end_quarter), end_time, str(play_count), str(yards_to_go), str(yards), result])


        except: error_log.append(game_id)
        
        for x in drive_info:
            try:
                    cursor.execute('INSERT INTO drives values ("' + x[0] + '", "' + x[1] + '", "' + x[2] + '", "' + x[3] + '", "' + x[4] + '", "' + x[5] + '", "' + x[6] + '", "' + x[7] + '", "' + x[8] + '", "' + x[9] + '", "' + x[10] + '", "' + x[11] + '")')
                    #print ('INSERT INTO drives values ("' + x[0] + '", "' + x[1] + '", "' + x[2] + '", "' + x[3] + '", "' + x[4] + '", "' + x[5] + '", "' + x[6] + '", "' + x[7] + '", "' + x[8] + '", "' + x[9] + '", "' + x[10] + '", "' + x[11] + '")')
            except:
                    fail = fail + 1
                    

        if fail == 0:
                print (game_id + ' added succesfully')
        else:
                print (game_id + ' had some errors')
                error_log.append(game_id)

conn.commit()
conn.close()

error_message  = 'The following games had drives that were not added: '

for error in error_log:
        error_message = error_message + error + ', '
        
if error_message != 'The following games had drives that were not added: ':
        print (error_message[:-2])
