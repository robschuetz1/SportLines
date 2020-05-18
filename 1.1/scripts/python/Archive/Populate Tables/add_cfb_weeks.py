import sqlite3
import requests


def lengthen_id(init):
	    output = str(init)
	    while len(output) < 5:
	        output = '0' + output
	    return output

conn = sqlite3.connect('C:\\Users\\rschuetz\\Downloads\\sport_lines (2)\\sport_lines\\sqlite3\\sport_lines.db')
cursor = conn.cursor()

url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?group=80&dates='
group_id = 80
inc_id = 1
i = 2005
while i < 2020:
    try:
        x_url = url + str(i) + '1010'
        data = requests.get(x_url)
        j_data = data.json()
        start_date = j_data.get("leagues")[0].get("calendarStartDate")[:10]
        end_date = j_data.get("leagues")[0].get("calendarEndDate")[:10]
        weeks = []
        for calendar in j_data.get("leagues")[0].get("calendar"):
                for entry in calendar.get("entries"):
                        if entry.get("label") == 'Bowls':
                                weeks.append([str(group_id) + '-' + lengthen_id(inc_id), group_id, start_date, end_date, entry.get("label"), entry.get("startDate")[:10], entry.get("endDate")[:10]])
                                inc_id = inc_id + 1
                        if entry.get("label") != 'All-Star' and entry.get("label") != 'Bowls':
                                weeks.append([str(group_id) + '-' + lengthen_id(inc_id), group_id, start_date, end_date, entry.get("value"), entry.get("startDate")[:10], entry.get("endDate")[:10]])
                                inc_id = inc_id + 1

        for week in weeks:
            print (week)
            #print ('insert into weeks values ("' + week[0] + '", ' + str(week[1]) + ', "' + week[2] + '", "' + week[3] + '", "' + week[4] + '", "' + week[5] + '", "' + week[6] + '")')
            cursor.execute('insert into weeks values ("' + week[0] + '", ' + str(week[1]) + ', "' + week[2] + '", "' + week[3] + '", "' + week[4] + '", "' + week[5] + '", "' + week[6] + '")')
    
    except:
        inc_id = 1
        print ('Bummer, link to the ' + str(i) + ' season has not been added')
    i = i + 1

conn.commit()
conn.close()
