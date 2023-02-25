from file import read, write
import json

import os
import sys

from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

import time
import random
import threading
from requests import RequestException
import requests
from bs4 import BeautifulSoup
from fake_user import fa

while True:
    inpt = input(' : ')

# Setings

    if inpt == ('help' or 'Help'):
        os.system("cls")
        help_com = f'seting : Settings \nstats : Your Statistics \nstart : Launch Bot'
        print(Panel(help_com, title='Help'), "\n")

    elif inpt == ('stats' or 'Stats'):
        if read('settings.json')['user'][0]['PHPSESSID'] == "":
            os.system("cls")
            print('Please go to seting, cookies and set cookies')

        else:
            os.system("cls")
            if read('settings.json')['user'][0]['fake_user'] == ('random' or 'Random'):
                header = {"user-agent": fa}
            else:
                header = {"user-agent": read('settings.json')['user'][0]['fake_user']}

            proxie_inp = read('settings.json')['proxy']
            if proxie_inp == ('one' or 'One'):
                proxie = read('proxies.json')['proxies'][0]['proxie']
                proxie = {'http': f"http://{proxie}"}
            elif proxie_inp == ('all' or 'All'):
                proxie = read('proxies.json')['proxies'][random.randint(0, 836)]['proxie']
                proxie = {'http': f"http://{proxie}"}
        
            cooki = {'PHPSESSID': read('settings.json')['user'][0]['PHPSESSID']}
            link = read('settings.json')['https'] + read('settings.json')['link']
            r = requests.get(link, cookies=cooki, headers=header, proxies=proxie)
            html = BeautifulSoup(r.text, 'lxml')

            user_name = html.find("a", {"class": "nav__avatar-outer-wrap"})['href']
            user_name = user_name.removeprefix('/user/')

            points = html.find('span', {'class': 'nav__points'}).text

            won_game = html.find("div", {"class": "nav__notification fade_infinite"})

            if won_game == None:
                won_game = 0
            else:
                won_game = won_game.text
        
            mess = f'Name : {user_name} \nPoint : {points} \nGame Won : {won_game}'
            print(Panel(mess, title='Version : 1.0.3'))

    elif inpt == ('seting' or 'Seting'):
        seting_com = f'cookies : Change Cookies \nproxy : Use Proxy \nusag : user-agent \nsave : Point Save \nexit, leave : Exit settings'
        while True:
            os.system("cls")
            print(Panel(seting_com, title=f'Seting'), "\n")
            inpt = input(' : ')
            if inpt == ('save' or 'Save'):
                inpt = input('Point Save : ')

                with open('settings.json') as f:
                    point_int = json.load(f)
                point_int['user'][0]['point_save'] = inpt

                write(point_int, 'settings.json')

                if inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                    os.system("cls")
                    print(f'You are out of Cookie settings.', '\n')

            elif inpt == ('cookies' or 'Cookies'):
                os.system("cls")
                print(Panel(f'rewrite : Change Cookies \nexit, leave: Leave as it was', title='Cookies'), "\n")
                inpt = input(' : ')
                if inpt == ('rewrite' or 'Rewrite'):
                    os.system("cls")
                    inpt = input('Enter New PHPSESSID Cookie : ')

                    with open('settings.json') as f:
                        cookie = json.load(f)
                    cookie['user'][0]['PHPSESSID'] = inpt

                    write(cookie, 'settings.json')
                    os.system("cls")

                elif inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                    os.system("cls")
                    print(f'You are out of Cookie settings.', '\n')
                    
                else:
                    os.system("cls")
                    print(f'Sorry, there is no such command.', '\n')

            elif inpt == ('proxy' or 'Proxy'):
                os.system("cls")
                print(Panel(f'rewrite : Change Proxy \nexit, leave: Leave as it was', title='Proxy'), '\n')
                inpt = input(' : ')
                if inpt == ('rewrite' or 'Rewrite'):
                    while True:
                        os.system("cls")
                        inpt = input('Use one or all proxies : ')
                    
                        if inpt == ('one' or 'One'):
                            with open('settings.json') as f:
                                proxy = json.load(f)
                            proxy['proxy'] = inpt

                            write(proxy, 'settings.json')
                            os.system("cls")
                            break
                        elif inpt == ('all' or 'All'):
                            with open('settings.json') as f:
                                proxy = json.load(f)
                            proxy['proxy'] = inpt

                            write(proxy, 'settings.json')
                            os.system("cls")
                            break
                        elif inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                            os.system("cls")
                            print(f'You are out of settings.', '\n')
                            break
                        else:
                            os.system("cls")
                            print(f"I asked you to do it right, otherwise the program won't work.", '\n')

                elif inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                    os.system("cls")
                    print(f'You are out of Proxy settings.', '\n')
                    
                else:
                    os.system("cls")
                    print(f'Sorry, there is no such command.', '\n')

            elif inpt == ('usag' or 'Usag'):
                os.system("cls")
                print(Panel(f'rewrite : Change User Agent \nexit, leave: Leave as it was', title='User Agent'), '\n')
                inpt = input(' : ')
                if inpt == ('rewrite' or 'Rewrite'):
                    os.system("cls")
                    print(Panel(f'Either randomly, or your own but not 2 letters, otherwise they can ban'), '\n')
                    inpt = input("Enter User-Agent : ")
                    
                    with open('settings.json') as f:
                        fake_user = json.load(f)
                    fake_user['user'][0]['fake_user'] = inpt

                    write(fake_user, 'settings.json')
                    os.system("cls")

                elif inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                    os.system("cls")
                    print(f'You are out of User-Agent settings.', '\n')
                    
                else:
                    os.system("cls")
                    print(f'Sorry, there is no such command.', '\n')

            elif inpt == ('exit' or 'Exit' ) or ( 'leave' or 'Leave'):
                os.system("cls")
                print(f'You are out of settings.', '\n')
                break
            else:
                os.system("cls")
                print(f'Sorry, there is no such command.', '\n')

    elif inpt == ('start' or 'Start'):
        os.system("cls")
        break
    else:
        os.system("cls")
        print(f'Sorry, there is no such command.', '\n')

if read('settings.json')['user'][0]['PHPSESSID'] == "":
    cook = input('Please Send PHPSESSID Cookies : ')

    with open('settings.json') as f:
        cookie = json.load(f)
    cookie['user'][0]['PHPSESSID'] = cook

    write(cookie, 'settings.json')

point = read('settings.json')['user'][0]['point_save']

if read('settings.json')['user'][0]['fake_user'] == ('random' or 'Random'):
    header = {"user-agent": fa}
else:
    header = {"user-agent": read('settings.json')['user'][0]['fake_user']}

proxie_inp = read('settings.json')['proxy']
if proxie_inp == ('one' or 'One'):
    proxie = read('proxies.json')['proxies'][0]['proxie']
    proxie = {'http': f"http://{proxie}"}
elif proxie_inp == ('all' or 'All'):
    proxie = read('proxies.json')['proxies'][random.randint(0, 836)]['proxie']
    proxie = {'http': f"http://{proxie}"}

cc = {'PHPSESSID': read('settings.json')['user'][0]['PHPSESSID']}
link = read('settings.json')['https'] + read('settings.json')['link']
rss = requests.get(link, cookies=cc, headers=header, proxies=proxie)
html = BeautifulSoup(rss.text, 'lxml')

user_name = html.find("a", {"class": "nav__avatar-outer-wrap"})['href']
user_name = user_name.removeprefix('/user/')

points = html.find('span', {'class': 'nav__points'}).text

won_game = html.find("div", {"class": "nav__notification fade_infinite"})

if won_game == None:
    won_game = 0
else:
    won_game = won_game.text

print(Panel('Version : 1.0.3' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))

cook = read('settings.json')['user'][0]['PHPSESSID']

timeout = 900
pages = 1


def get_soup_from_page(url):
    global cookies 

    cookies = {'PHPSESSID': cook}
    r = requests.get(url, cookies=cookies, headers=header, proxies=proxie)
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
        print(Panel('Version : 1.0.3' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))
        print('Not point bot stoped')
        time.sleep(1)
        os.system("cls")
        get_page()

    soup = get_soup_from_page(read('settings.json')['https'] + read('settings.json')['link'])

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
                    print(Panel('Version : 1.0.3' '\n' f'Name : {user_name}' '\n' f'Point : {points}' '\n' f'Game Won : {won_game}'))

                
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
    entry = requests.post('https://www.steamgifts.com/ajax.php', data=payload, cookies=cookies, headers=header, proxies=proxie)
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
