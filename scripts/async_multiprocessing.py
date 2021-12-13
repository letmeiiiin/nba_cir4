import asyncio,time
from aiohttp import request
from aiomultiprocess import Pool
from playwright.async_api import async_playwright

# Scraping with &redirect=no sets US website, no need to set cookies, main page : https://www.nba.com/?&redirect=no
# https://www.nba.com/stats/?&redirect=no
# https://www.nba.com/stats/teams

# https://www.nba.com/stats/players
# https://www.nba.com/stats/players/advanced/?sort=TEAM_ABBREVIATION&dir=-1

# https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight=

#body > main > div > div > div.landing-page-content > div.inner__sidebar.inner__sidebar-next.\[.columns.\/.large-3.\] > section:nth-child(1) > div > div > div:nth-child(2)
#/html/body/main/div/div/div[3]/div[2]/section[1]/div/div/div[2]
# Players stats by seasons

async def get(url):
    async with request("GET", url) as response:
        return await response.text("utf-8")

async def scrape_3():
    print("scraping_3...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close() 
    print("finished scraping_3")

async def scrape_2():
    print("scraping_2...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close() 
    print("finished scraping_2")    

async def scrape_multiprocess():
    urls = ["http://playwright.dev"]
    async with Pool() as pool:
        async for result in pool.map(get, urls):
            print(result.title())
            
async def main():
    await asyncio.gather(scrape_multiprocess(), scrape_2(), scrape_3())

if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Script executed in {elapsed:0.2f} seconds.")
    