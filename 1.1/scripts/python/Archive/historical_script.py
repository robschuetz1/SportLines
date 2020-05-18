years = ['2015','2016',2017','2018']
weeks = ['1','2','3','4','5','6','7','8','9,'10','11','12','13','14','15','Bowls']
for x in years:
	for y in weeks:
		url = 'http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?group=80&year=' + x + '&week=' + y
		r = requests.get(url)
		j = r.json()
		