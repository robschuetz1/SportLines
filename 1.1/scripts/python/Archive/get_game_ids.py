import requests
url = 'https://www.espn.com/college-football/scoreboard?group=80'
src = requests.get(url)
src_str = str(src.content)

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

game_ids = get_game_ids(src_str)
