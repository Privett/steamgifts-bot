import cloudscraper
from bs4 import BeautifulSoup

import time
import os

cookies = {"PHPSESSID": ""}
headler={}

timeout = 900
pages = 1

scraper = cloudscraper.create_scraper()

def get_data(url):
    response = scraper.get(url, cookies=cookies)
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_page():
    global xsrf_token, point, won_game, avatar
    soup = get_data("https://www.steamgifts.com")
    xsrf_input = soup.find("input", {"type": "hidden", "name": "xsrf_token"})
    xsrf_token = xsrf_input["value"] if xsrf_input else ""
    
    point_span = soup.find("span", {"class": "nav__points"})
    point = int(point_span.text) if point_span else 0

    notification = soup.find("div", {"class": "nav__notification fade_infinite"})
    won_game = notification.text.strip() if notification else 0

    avatar_wrap = soup.find("a", {"class": "nav__avatar-outer-wrap"})
    if avatar_wrap and avatar_wrap.has_attr('href'):
        avatar = avatar_wrap["href"].removeprefix('/user/')
    else:
        avatar = ""

def entry_gift(game_code: str):
    html = get_data("https://www.steamgifts.com")
    if html.find("div", {"class": "sidebar__error is-disabled"}):
        return f"😭 Is the game available, or have you won it: {game_name}", point
    
    payload = {'xsrf_token': xsrf_token, 'do': 'entry_insert', 'code': game_code}
    response_post = scraper.post("https://www.steamgifts.com/ajax.php", data=payload, cookies=cookies)

    if response_post.status_code == 200:
        data = response_post.json()
        if data.get("type").lower() == "success":
            return f"😀 Bot has entered giveaway: {game_name}", int(data.get("points"))
        elif data.get("type").lower() == "error":
            return f"😭 Error: {game_name}", point
    else:
        return f"😭 Enter Status not 200: {game_name}", point

def get_games():
    global point
    global game_name, pages

    page = 1
    while page <= pages:
        print('Proccessing games from %d page.' % page)
        soup = get_data(f"https://www.steamgifts.com/giveaways/search?page={page}")

        try:
            for game in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['giveaway__row-inner-wrap']): #("div", {"class", "giveaway__row-inner-wrap"})
                game_heads = game.find("h2", {"class": "giveaway__heading"})
                game_heads_name = game_heads.find("a", {"class": "giveaway__heading__name"})
                game_code = game_heads_name["href"].split("/")[2]
                game_name = game_heads_name.text
                
                for i in game_heads.find_all("span", {"class": "giveaway__heading__thin"}):
                    if "copies" in i.text.lower():
                        pass
                    else:
                        game_point = int(i.text.replace("(","").replace("P)",""))
                
                time.sleep(1)
                
                if game_point <= point:
                    text, point = entry_gift(game_code)
                    print(text, point)
                else:
                    print(f"😐 Not enough points to enter: {game_name}")
            
            page+=1
        except AttributeError as ex:
            break
    print('😐 List of games is ended. Waiting 2 min to update...')
    os.system("cls")
    time.sleep(120)

if __name__ == '__main__':
    while True:
        get_page()
        get_games()
