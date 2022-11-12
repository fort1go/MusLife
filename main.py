import requests
import telebot
from time import sleep
from bs4 import BeautifulSoup as b

vse_podsayti = list()

bot = telebot.TeleBot('5061487172:AAFgTi1TN_WfNAJu3jQyb666MWosv6JJpms')
URL_online_sayta = 'https://soccer365.ru/online/&tab=1'
soup_online = b(requests.get(URL_online_sayta).text, 'lxml')
new_list = list()


def skan_osnovnogo_sayta():  # Эта штука проходит по сайту и собирает все линк'и на будущие игры
    soup_online = b(requests.get(URL_online_sayta).text, 'lxml')
    # И кидает их в лист 'vse_podsayti'
    for link in soup_online.find_all('div', class_='game_block online'):  # Функция уже работает, проверку провёл
        link_href = link.find('a').get('href')
        if 'live' in link_href:
            vse_podsayti.append(f'https://soccer365.ru{link_href}')
        else:
            continue
    print(vse_podsayti)


def skan_podsaytov():  # Проходится по всем подсайтам и собирает данные по кофф.
    for URL_podsayta in vse_podsayti:  # Функция уже работает, проверку провёл
        r2 = requests.get(URL_podsayta)
        soup_podsayt = b(r2.text, 'lxml')

        teamleft = soup_podsayt.find('div', class_='live_game_ht').text  # Находит команды
        teamright = soup_podsayt.find('div', class_='live_game_at').text

        goals = list()
        for goal in soup_podsayt.find_all('div', class_="live_game_goal"):  # Находит их счёт
            goals.append(goal.text)
        goalleft = goals[0]
        goalright = goals[1]

        time = soup_podsayt.find('div', class_='live_game_status')
        if time is not None and 'Перерыв' not in time.text:
            time = str(time.text)[1:-6]
            koefs = list()
            for koef in soup_podsayt.find_all('span', class_="koeff"):  # Находит коэфицент победы
                koefs.append(koef.text)
            try:
                kl = koefs[0]
                kr = koefs[2]
            except Exception:
                return None

            if (1.1 <= float(kl) <= 1.5) or (1.1 <= float(kr) <= 1.5):
                if 40 >= int(time) >= 10:
                    if int(goalright) == 0 and int(goalleft) == 0:
                        if URL_podsayta not in new_list:
                            game = (f'Команда: {teamleft[1:]}Счёт: {goalleft[1:]}Коф на победу: {kl} \n\n'
                                    f'Команда: {teamright[1:]}Счёт: {goalright[1:]}Коф на победу: {kr} \n'
                                    f'Ссылка на игру: {URL_podsayta}\n')
                            bot.send_message(-1001765456131, game)
                            print(game)
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue


def start(res=False):
    print('blob')
    try:
        while True:
            skan_osnovnogo_sayta()
            skan_podsaytov()
            vse_podsayti.clear()
            sleep(150)
    except Exception:
        start()


start()
