from file import read, write
import json

import os
import sys

from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

import time
import threading
from requests import RequestException
import requests
from bs4 import BeautifulSoup
from fake_user import fa

if read('main.json')['user'][0]['UserCookies'] == "":
    cook = input('Please Send PHPSESSID Cookies : ')

    man = {
        "ste": "https://www.steamgifts.com/",
        "user": []
    }
    user = {
        "UserName": "",
        "UserCookies": cook
    }

    man["user"].append(user)

    write(man, 'main.json')

header = {"user-agent": fa}

cc = {'PHPSESSID': read('main.json')['user'][0]['UserCookies']}
http = read('main.json')['ste']
rss = requests.get(read('main.json')['ste'], cookies=cc, headers=header)
html = BeautifulSoup(rss.text, 'lxml')

user_name = html.find("a", {"class": "nav__avatar-outer-wrap"})['href']
user_name = user_name.removeprefix('/user/')

points = html.find('span', {'class': 'nav__points'}).text

won_game = html.find("div", {"class": "nav__notification fade_infinite"})

if won_game == None:
    won_game = 0
else:
    won_game = won_game.text

print(Panel('Version : 1.0.1' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))

point = input('point save : ')

cook = read('main.json')['user'][0]['UserCookies']

timeout = 900
pages = 1


def get_soup_from_page(url):
    global cookies 

    cookies = {'PHPSESSID': cook}
    r = requests.get(url, cookies=cookies, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')

    return soup

def game_won():
    global won_game
    won_game = html.find("div", {"class": "nav__notification fade_infinite"})

    if won_game == None:
        won_game = 0
    else:
        won_game = won_game.text

def get_page():
    global xsrf_token, points 

    if int(points) <= int(point):
        print(Panel('Version : 1.0.1' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))
        print('Not point bot stoped')
        time.sleep(1)
        os.system("cls")
        get_page()

    soup = get_soup_from_page(read('main.json')['ste'])

    xsrf_token = soup.find('input', {'name': 'xsrf_token'})['value']
    points = soup.find('span', {'class': 'nav__points'}).text  # storage points
    

# get codes of the games
def get_games():
    global game_name
    global pages

    n = 1
    while n <= pages:
        print('Proccessing games from %d page.' % n)

        soup = get_soup_from_page('https://www.steamgifts.com/giveaways/search?page=' + str(n))

        try:
            gifts_list = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['giveaway__row-inner-wrap'])

            for item in gifts_list:
                if int(points) == 0:
                    print('> Sleeping to get 6 points')
                    time.sleep(timeout)
                    get_games()
                    break

                game_cost = item.find_all('span', {'class': 'giveaway__heading__thin'})

                last_div = None
                for last_div in game_cost:
                    pass
                if last_div:
                    game_cost = last_div.getText().replace('(', '').replace(')', '').replace('P', '')

                game_name = item.find('a', {'class': 'giveaway__heading__name'}).text

                if int(points) - int(game_cost) < 0:
                    print('Not enough points to enter: ' + game_name)
                    continue
                elif int(points) - int(game_cost) > 0:
                    entry_gift(item.find('a', {'class': 'giveaway__heading__name'})['href'].split('/')[2])
                if time.sleep(2):
                    os.system("cls")
                    print(Panel('Version : 1.0.1' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))

                
            n = n+1
        except AttributeError as e:
            break
    os.system("cls")
    print('List of games is ended. Waiting 2 min to update...')
    time.sleep(120)
    get_page()
    get_games()


def entry_gift(code):
    payload = {'xsrf_token': xsrf_token, 'do': 'entry_insert', 'code': code}
    entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=cookies, headers=header)
    json_data = json.loads(entry.text)

    get_page()
    # print(json_data)

    # updating points after entered a giveaway
    if json_data['type'] == 'success':
        print('> Bot has entered giveaway: ' + game_name)
        time.sleep(5)

if __name__ == '__main__':
    game_won()
    get_page()
    get_games()
