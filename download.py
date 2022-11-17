from bs4 import BeautifulSoup
from data_base import length, check_add_music_main
from getpass import getuser
import requests


class Download:
    # скачивает
    def download(self, n):
        try:
            from data_base import add_to_db
            if self.treks:
                if n in self.treks.keys():
                    self.index = n
                    _length = length('music')
                    _length, author, name = _length + 1, self.treks[n][0], self.treks[n][1]
                    position = f"C:\\Users\{getuser()}\MusLife\music\{name}_{author}.mp3"
                    _url = self.treks[self.index][2]
                    process = self.download_music(self.treks[self.index][0], self.treks[self.index][1],
                                                  self.treks[self.index][2])
                    if process == 'ок':
                        if not check_add_music_main('music', name, author, position):
                            add_to_db(_length, author, name, position, 'music')
                    else:
                        return 'ошибка'
                else:
                    return 'ошибка'
        except:
            return 'ошибка'

    # скачивает песню с сайта
    def download_music(self, author, name, s_n_p):
        try:
            s_n_d = BeautifulSoup(requests.get(s_n_p).text,
                                  'lxml').find('a',
                                               class_='onesongblock-down psv_btn rtform-red no-ajax cu-exclude').get(
                'href')
            with open(f"C:\\Users\{getuser()}\MusLife\music\{name}_{author}.mp3", 'wb') as f:
                f.write(requests.get(s_n_d).content)
            return 'ок'
        except:
            return 'ошибка'

    # собирает информацию о песне
    def information_music(self, search):
        try:
            self.treks = dict()
            self.id = 1
            self.musics = BeautifulSoup(
                requests.get(f'https://dydki.info/?mp3={search}').text, 'lxml'
            )
            for music in self.musics.find_all('div', class_='chkd'):  # создаёт словарь в котором песни
                link = music.find('a', class_='link cu-exclude').get('href')
                link = f'https://dydki.info{link}'
                author = music.find('a', class_='track__artist').text
                name = music.find('a', class_='track__title').text
                self.treks[self.id] = [author, name, link]
                self.id += 1
            return self.treks
        except:
            self.musicList.clear()
            self.musicList.addItem('Что-то не так с интернетом')
            return {}

    def search(self, n):
        if n in self.treks.keys():
            return self.treks[n][:2]