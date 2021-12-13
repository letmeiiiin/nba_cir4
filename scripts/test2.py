import time
import asyncio, aiohttp
from aiomultiprocess import Pool
from pprint import pprint

# Scraping with &redirect=no sets US website, no need to set cookies, main page : https://www.nba.com/?&redirect=no
# https://www.nba.com/stats/?&redirect=no
# https://www.nba.com/stats/teams

# https://www.nba.com/stats/players
# https://www.nba.com/stats/players/advanced/?sort=TEAM_ABBREVIATION&dir=-1

# https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight=

#body > main > div > div > div.landing-page-content > div.inner__sidebar.inner__sidebar-next.\[.columns.\/.large-3.\] > section:nth-child(1) > div > div > div:nth-child(2)
#/html/body/main/div/div/div[3]/div[2]/section[1]/div/div/div[2]
# Players stats by seasons

headers = {
	'Connection': 'keep-alive',
	'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
	'DNT': '1',
	'sec-ch-ua-mobile': '?0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.20 Safari/537.36 Edg/97.0.1072.21',
	'Accept': 'application/json, text/plain, */*',
	'x-nba-stats-token': 'true',
	'x-nba-stats-origin': 'stats',
	'sec-ch-ua-platform': '"Linux"',
	'Origin': 'https://www.nba.com',
	'Sec-Fetch-Site': 'same-site',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Dest': 'empty',
	'Referer': 'https://www.nba.com/',
	'Accept-Language': 'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

leaguedashplayerstats_params = (
	('College', ''),
	('Conference', ''),
	('Country', ''),
	('DateFrom', ''),
	('DateTo', ''),
	('Division', ''),
	('DraftPick', ''),
	('DraftYear', ''),
	('GameScope', ''),
	('GameSegment', ''),
	('Height', ''),
	('LastNGames', '0'),
	('LeagueID', '00'),
	('Location', ''),
	('MeasureType', 'Advanced'),
	('Month', '0'),
	('OpponentTeamID', '0'),
	('Outcome', ''),
	('PORound', '0'),
	('PaceAdjust', 'N'),
	('PerMode', 'PerGame'),
	('Period', '0'),
	('PlayerExperience', ''),
	('PlayerPosition', ''),
	('PlusMinus', 'N'),
	('Rank', 'N'),
	('Season', '2021-22'),
	('SeasonSegment', ''),
	('SeasonType', 'Regular Season'),
	('ShotClockRange', ''),
	('StarterBench', ''),
	('TeamID', '0'),
	('TwoWay', '0'),
	('VsConference', ''),
	('VsDivision', ''),
	('Weight', ''),
)

leaguedashplayerstats_params = dict(leaguedashplayerstats_params)

def gen_seasons():
	seasons = []
	end = (2021,22)
	start = (1996,97)
	i = start[0]
	j = start[1]
	while i <= end[0]:
		if j % 100 == 0:
			j = 0
		season = f"{i}-{j}"    
		if j <= 9:
			season = f"{i}-0{j}"
		seasons.append(season)
		i+=1
		j+=1

	return seasons

seasons_dates = gen_seasons()
players_stats_by_seasons = []

async def fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

async def fetch_all(urls):
	async with aiohttp.ClientSession() as session:
		texts = await asyncio.gather(*[
			fetch(session, url)
			for url in urls
		])
		#print(texts)
		return texts

years_to_fetch = [f'https://en.wikipedia.org/wiki/{year}' for year in range(1990, 2020)]

async def main():
	await asyncio.gather(fetch_all(years_to_fetch))

if __name__ == '__main__':
	s = time.perf_counter()
	asyncio.run(main())
	#session.close()
	elapsed = time.perf_counter() - s
	print(f"Script executed in {elapsed:0.2f} seconds.")
	