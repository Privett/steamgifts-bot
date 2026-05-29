import cloudscraper
from bs4 import BeautifulSoup

from typing import Optional
import random
import time
import os

from module.file import File

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import sys
import typer

import platform

base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)

headler={}

timeout = 900
pages = 1

os_name = platform.system()
if os_name == "Windows":
    import winreg

scraper = cloudscraper.create_scraper()
app = typer.Typer()

def create_config_file():
    global data_write
    data_write = {
        "Default": {"PHPSESSID": None, "filter_url": None, "ignored_filter": ""},
        "Discord": {"webhook": None, "token": None, "chat_id": 0, "user_id": 0},
        "Telegram": {"token": None, "user_id": 0}
    }
    def ini_file():
        ini.read()
        for section, key_value in data_write.items():
            ini_n = 0
            for key, value in key_value.items():
                if ini.get(section, key):
                    ini_n+=1
            if ini_n != len(key_value):
                if os.path.exists("config.ini"):
                    if os.path.exists("config.ini.old"):
                        os.remove("config.ini.old")
                    os.rename("config.ini", "config.ini.old")
                ini.write(section, key_value)
    def json_file():
        for section, key_value in data_write.items():
            for key, value in key_value.items():
                if jsonf.read().get(section, {}).get(key, "none") != "none":
                    continue
                else:
                    if os.path.exists("config.json"):
                        if os.path.exists("config.json.old"):
                            os.remove("config.json.old")
                        os.rename("config.json", "config.json.old")
                    jsonf.write(data_write)
                    break
    
    if file_format == "ini":
        ini_file()
    elif file_format == "json":
        json_file()
    else:
        print(":(")

def load_file_data():
    data_write_type = {
        "Default": {"PHPSESSID": str, "filter_url": str, "ignored_filter": str},
        "Discord": {"webhook": str, "token": str, "chat_id": int, "user_id": int},
        "Telegram": {"token": str, "user_id": int}
    }
    def load_ini():
        global default_data, send2me_data, discord_data, telegram_data
        discord_data = {}
        telegram_data = {}
        default_data = {}
        send2me_data = {}
        ini.read()
        for section, key_value in data_write_type.items():
            for key, value in key_value.items():
                if section.lower() == "default":
                    data = ini.get(section, key, value)
                    if str == value and data.lower() == "none":
                        data = None
                    default_data[key] = data
                elif section.lower() == "discord":
                    data = ini.get(section, key, value)
                    if str == value and data.lower() == "none":
                        data = None
                    discord_data[key] = data
                elif section.lower() == "send2me":
                    data = ini.get(section, key, value)
                    if str == value and data.lower() == "none":
                        data = None
                    send2me_data[key] = data
                elif section.lower() == "telegram":
                    data = ini.get(section, key, value)
                    if str == value and data.lower()  == "none":
                        data = None
                    telegram_data[key] = data

    def load_json():
        global default_data, send2me_data, discord_data, telegram_data
        discord_data = {}
        telegram_data = {}
        default_data = {}
        send2me_data = {}
        for section, key_value in jsonf.read().items():
            for key, value in key_value.items():
                if section.lower() == "default":
                    default_data[key] = value
                elif section.lower() == "discord":
                    discord_data[key] = value
                elif section.lower() == "send2me":
                    send2me_data[key] = value
                elif section.lower() == "telegram":
                    telegram_data[key] = value

    if file_format == "ini":
        load_ini()
    elif file_format == "json":
        load_json()
    else:
        print(":(")

def load_file():
    global ini, jsonf
    
    if file_format == "ini":
        print("load: ini")
        if not os.path.exists("config.ini"): open("config.ini", "w")
        ini = File("config.ini").ini
    elif file_format == "json":
        print("load: json")
        if not os.path.exists("config.json"): open("config.json", "w")
        jsonf = File("config.json").jsonf
    
    create_config_file()

def send_to_dashboard():
    pass

def get_data(url: str):
    response = scraper.get(url, cookies={"PHPSESSID": default_data["PHPSESSID"]})
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_page():
    global xsrf_token, point, won_game, account_name
    soup = get_data("https://www.steamgifts.com")
    xsrf_input = soup.find("input", {"type": "hidden", "name": "xsrf_token"})
    xsrf_token = xsrf_input["value"] if xsrf_input else ""
    
    point_span = soup.find("span", {"class": "nav__points"})
    point = int(point_span.text) if point_span else 0

    notification = soup.find("div", {"class": "nav__notification fade_infinite"})
    won_game = notification.text.strip() if notification else 0

    avatar_wrap = soup.find("a", {"class": "nav__avatar-outer-wrap"})
    if avatar_wrap and avatar_wrap.has_attr('href'):
        account_name = avatar_wrap["href"].removeprefix('/user/')
    else:
        account_name = ""

def entry_gift(game_code: str):
    payload = {'xsrf_token': xsrf_token, 'do': 'entry_insert', 'code': game_code}
    response_post = scraper.post("https://www.steamgifts.com/ajax.php", data=payload, cookies={"PHPSESSID": default_data["PHPSESSID"]})
    
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
        print(f'⚙️  Proccessing games from {page} page.')
        soup = get_data(default_data["filter_url"] % page)

        try:
            for game in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['giveaway__row-inner-wrap']):
                if point < 6:
                    os.system("cls")
                    print('😴 Sleeping to get 6 points')
                    time.sleep(timeout)
                    run()
                    break
                game_heads = game.find("h2", {"class": "giveaway__heading"})
                game_heads_name = game_heads.find("a", {"class": "giveaway__heading__name"})
                game_code = game_heads_name["href"].split("/")[2]
                game_name = game_heads_name.text
                if any(word.lower() in game_name.lower() for word in ignored_filter):
                    print(f"❌ Ignored: {game_name}")
                    continue
                
                for i in game_heads.find_all("span", {"class": "giveaway__heading__thin"}):
                    if "copies" in i.text.lower():
                        pass
                    else:
                        game_point = int(i.text.replace("(","").replace("P)",""))
                        
                time_s = random.uniform(1.0, 3.0)
                time.sleep(time_s)
                
                if game_point <= point:
                    text, point = entry_gift(game_code)
                    print(text, f"Point: {point}", f"Time: {time_s:.2f}")
                else:
                    print(f"😐 Not enough points to enter: {game_name}")
            
            page+=1
        except AttributeError as ex:
            break
    print('😐 List of games is ended. Waiting 2 min to update...')
    time.sleep(120)
    os.system("cls")

def run():
    get_page()
    get_games()

@app.callback(invoke_without_command=True)
def cli_run(ctx: typer.Context):
    if ctx.invoked_subcommand: return
    cli()

def cli():
    global file_format, ignored_filter
    url = "https://www.steamgifts.com"
    filter_url = {
        "All": f"{url}/giveaways/search?page=%d",
        "Wishlist": f"{url}/giveaways/search?page=%d&type=wishlist",
        "Recommended": f"{url}/giveaways/search?page=%d&type=recommended",
        "Multiple Copies": f"{url}/giveaways/search?page=%d&copy_min=2",
        "DLC": f"{url}/giveaways/search?page=%d&dlc=true",
        "Group": f"{url}/giveaways/search?page=%d&type=group",
        "New": f"{url}/giveaways/search?page=%d&type=new",
    }
    ignored_filter = []

    nav = {
        "keys": {
            "select": {
                "answer": [{"key": "enter"}, {"key": "right"}],
                "skip": [{"key": "q"}, {"key": "Q"}, {"key": "й"}, {"key": "Й"}]
            },
            "confirm": {
                "confirm": [{"key": "y"}, {"key": "Y"}, {"key": "н"}, {"key": "Н"}],
                "reject": [{"key": "n"}, {"key": "N"}, {"key": "т"}, {"key": "Т"}],
                "skip": [{"key": "q"}, {"key": "Q"}, {"key": "й"}, {"key": "Й"}]
            },
            "checkbox": {
                "toggle": [{"key": "space"}, {"key": "right"}],
                "answer": [{"key": "enter"}, {"key": "left"}],
                "skip": [{"key": "q"}, {"key": "Q"}, {"key": "й"}, {"key": "Й"}]
            },
            "text": {
                "skip": [{"key": "q"}, {"key": "Q"}, {"key": "й"}, {"key": "Й"}]
            },
        },
        "instruction": {
            "select": "(↑↓ navigate, →/Enter confirm, Q/Exit)",
            "checkbox": "(↑↓ navigate, →/Space select, ←/Enter confirm, Q/Exit)",
            "text": "(Q/Exit)",
        },
        "instruction not exit": {
            "select": "(↑↓ navigate, →/Enter confirm)",
            "checkbox": "(↑↓ navigate, →/Space select, ←/Enter confirm)",
            "text": "",
        },
    }

    def Choice2lower(data: list):
        data_list=[]
        for key in data:
            if key:
                data_list.append(Choice(key.lower(), key))
        return data_list
    
    def select_format(exit: Optional[bool] = False):
        return inquirer.select(
            message="Select config format:",
            choices=Choice2lower(["ini", "json"]),
            instruction=nav["instruction not exit"]["select"] if not exit else nav["instruction"]["select"],
            keybindings=nav["keys"]["select"],
            mandatory = not exit,
            mandatory_message = "Exit is unavailable"
        ).execute()
    
    cfg = File("config.cfg").ini
    if not os.path.exists("config.cfg"):
        fmt = select_format()
        cfg.write("App", {"file_format": fmt})
        file_format = fmt
    else:
        cfg.read()
        file_format = cfg.get("App", "file_format").lower()
        if file_format not in ["ini", "json"]:
            fmt = select_format()
            cfg.write("App", {"file_format": fmt})
    
    load_file()
    load_file_data()

    while True:
        browses = inquirer.select(
            message="Main Menu:",
            choices=Choice2lower(["Start", "Settings"]),
            keybindings=nav["keys"]["select"],
            instruction=nav["instruction"]["select"],
            mandatory=False
        ).execute()

        if browses is None:
            sys.exit()

        elif browses == "start":
            ini.read()
            ignored_filter=ini.get("Default", "ignored_filter", str).split(",")
            os.system("cls")
            load_file_data()
            while True:
                run()
        
        elif browses == "settings":
            while True:
                key=None
                auto_run=""
                if os_name == "Windows":
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                    try:
                        winreg.QueryValueEx(key, "SGB by Pritvett")
                        auto_run="Remove to auto run"
                    except FileNotFoundError:
                        auto_run="Add to auto run"

                    settings_browse = inquirer.select(
                        message="Settings:",
                        choices=Choice2lower(["Change Cookies", "Game Filter", "Ignore Filter", "File Format", "Merge old config", auto_run]),
                        keybindings=nav["keys"]["select"],
                        instruction=nav["instruction"]["select"],
                        mandatory=False
                    ).execute()

                    if settings_browse is None:
                        break

                    elif settings_browse == "change cookies":
                        change_cookies_PHPSESSID=inquirer.secret(
                        "Enter your PHPSESSID cookie:",
                        ).execute()

                        change_cookies_confirm = inquirer.confirm(
                            message="Are you sure?",
                            keybindings=nav["keys"]["confirm"]
                            ).execute()
                        
                        if change_cookies_confirm:
                            ini.update("Default", {"PHPSESSID": change_cookies_PHPSESSID})
                            print("Saved")

                    elif settings_browse == "game filter":
                        game_filter_browse = inquirer.select(
                            message="Select a giveaway filter:",
                            choices=[Choice(value=v, name=k) for k, v in filter_url.items()],
                            keybindings=nav["keys"]["select"],
                            instruction=nav["instruction"]["select"],
                            mandatory=False
                        ).execute()
                        if game_filter_browse:
                            game_filter_confirm = inquirer.confirm(
                                message="Are you sure?",
                                keybindings=nav["keys"]["confirm"]
                                ).execute()
                            
                            if game_filter_confirm:
                                ini.update("Default", {"filter_url": game_filter_browse.replace("%", "%%")})
                                print("Saved")
                    
                    elif settings_browse == "ignore filter":
                        ini.read()
                        data = ini.get("Default", "ignored_filter", str)
                        words = [w.strip() for w in data.split(',')]
                        ignored=inquirer.text(
                        message="Enter ignore words separated by commas (e.g. free, casino, ads):",
                        default=", ".join(words)
                        ).execute()

                        ignored_confirm = inquirer.confirm(
                            message="Are you sure?",
                            keybindings=nav["keys"]["confirm"]
                            ).execute()
                        
                        if ignored_confirm:
                            cleaned = ",".join([w.strip() for w in ignored.split(',')])
                            ini.update("Default", {"ignored_filter": cleaned})
                            print("Saved")

                    elif settings_browse == "file format":
                        fmt = select_format(exit=True)
                        if fmt: 
                            cfg.write("App", {"file_format": fmt})
                    
                    elif settings_browse == "merge old config":
                        select_file_format = inquirer.select(
                            message="Select a giveaway filter:",
                            choices=["ini", "json"],
                            keybindings=nav["keys"]["select"],
                            instruction=nav["instruction"]["select"],
                            mandatory=False
                        ).execute()
                        if select_file_format:
                            confirm_config_merge = inquirer.confirm(
                                message="Are you sure?",
                                keybindings=nav["keys"]["confirm"]
                            ).execute()

                            def merge_config(file_format):
                                diff = {}

                                if file_format == "ini":
                                    old = File("config.ini.old").ini
                                    new = File("config.ini").ini
                                    old.read()
                                    new.read()

                                    for section, keys in data_write.items():
                                        for key in keys:
                                            old_val = old.get(section, key)
                                            new_val = new.get(section, key)
                                            if old_val and old_val != new_val:
                                                diff[f"{section}.{key}"] = {"old": old_val, "new": new_val}
                                
                                elif file_format == "json":
                                    old = File("config.json.old").jsonf
                                    new = File("config.json").jsonf
                                    old_data = old.read()
                                    new_data = new.read()

                                    for section, keys in data_write.items():
                                        for key in keys:
                                            old_val = old_data.get(section, {}).get(key)
                                            new_val = new_data.get(section, {}).get(key)
                                            if old_val and old_val != new_val:
                                                diff[f"{section}.{key}"] = {"old": old_val, "new": new_val}
                                
                                if not diff:
                                    print("No differences found")
                                    return
                                
                                choices = [
                                    Choice(value=k, name=f"{k}: {v['new']} → {v['old']}")
                                    for k, v in diff.items()
                                ]

                                selected = inquirer.checkbox(
                                    message="Select values to restore:",
                                    choices=choices,
                                    instruction=nav["instruction"]["checkbox"],
                                    keybindings=nav["keys"]["checkbox"],
                                    mandatory=False,
                                    transformer=lambda result: ""
                                ).execute()

                                if select_file_format:
                                    for key in selected:
                                        section, param = key.split(".")
                                        if file_format == "ini":
                                            value = diff[key]["old"].replace("%", "%%") if "%" in diff[key]["old"] else diff[key]["old"]
                                            new.update(section, {param: value})
                                        elif file_format == "json":
                                            new_data[section][param] = diff[key]["old"]
                                            new.write(new_data)
                                    
                                    print("Merged")

                            if confirm_config_merge:
                                merge_config(select_file_format)

                    elif settings_browse == "add to auto run":
                        winreg.SetValueEx(key, "SGB by Pritvett", 0, winreg.REG_SZ, f'"{os.path.abspath(__file__)}" start')

                    elif settings_browse == "remove to auto run":
                        winreg.DeleteValue(key, "SGB by Pritvett")

@app.command()
def start():
    global file_format, ignored_filter
    cfg = File("config.cfg").ini
    if not os.path.exists("config.cfg"):
        print("Run python main.py (without start.bat) to configure the bot. It will auto-restart in 20s.")
        time.sleep(20)
        os.system("cls")
        cli()
        return
    cfg.read()
    file_format = cfg.get("App", "file_format").lower()
    load_file()
    load_file_data()
    ini.read()
    ignored_filter=ini.get("Default", "ignored_filter", str).split(",")
    while True:
        run()

if __name__ == '__main__':
    app()
