import pygame
from getpass import getuser
from download import Download
from interface import Interfeace
from dialog import CreatePlayList, DeletePlaylist, OpenPlayList, PlayPlayList
from data_base import delete_to_db, length, check, check_add_music_main
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


class Buttons(Download, Interfeace):
    def clickOnSearchingButton(self):
        self.messages.setText("")
        if self.searchingInput.text():
            self.musicList.clear()
            search = self.searchingInput.text()
            searching_musics = self.information_music(search)
            if searching_musics:
                for i in searching_musics.keys():
                    author, name = searching_musics[i][:2]
                    self.musicList.addItem(f"""Название: {name:40}\t\t\tАвтор: {author}""")
        else:
            self.musicList.clear()

    def clickOnDowload(self):
        self.messages.setText("")
        id = self.musicList.currentRow() + 1
        if id > 0:
            process = self.download(int(id))
            if process != 'ошибка':
                self.id = id
                self.messages.setText("Файл скачан")
            else:
                self.messages.setText("Произошла ошибка при загрузке")

    def clickOnAddPlaylist(self):
        try:
            self.messages.setText("")
            from data_base import add_to_db
            name_playlist = self.lineEdit_2.text()
            if self.id > 0:
                author, name = self.search(int(self.id))
                position = f"C:\\Users\{getuser()}\MusLife\music\{name}_{author}.mp3"
                _id = length(self.lineEdit_2.text())
                if (author, name, position) not in check(self.lineEdit_2.text()):
                    if not check_add_music_main(self.lineEdit_2.text(), name, author, position):
                        add_to_db(_id + 1, author, name, position, name_playlist)
            else:
                self.messages.setText('Вы ничего не выбрали')
        except:
            self.messages.setText('Возможно такого плейлиста нет')

    def clickOnPlayPlaylist(self):
        try:
            if self.flag3:
                self.flag = False
                self.flag3 = False
                window = PlayPlayList('music')
                window.show()
                window.exec()
                with open('play.txt', 'r', encoding='utf-8') as f:
                    file = f.read().split('\n')
                container = file
                self.pushButton_5.setIcon(QIcon('image2.png'))
                self.pushButton_5.setIconSize(QSize(90, 90))
                self.length_container = len(container)
                pygame.mixer.init()
                pygame.mixer.music.load(container[0])
                pygame.mixer.music.play()
                self.container = container
                self.count = 0
                self.flag = False
                self.flag3 = True
        except:
            self.flag3 = True

    def clickOnPlayMusic(self):
        try:
            self.pushButton_5.setIcon(QIcon('image2.png'))
            self.pushButton_5.setIconSize(QSize(90, 90))
            self.flag = False
            pygame.mixer.init()
            fname = QFileDialog.getOpenFileName(self, 'Выбрать песню', '', '*.mp3')[0]
            pygame.mixer.music.load(fname)
            pygame.mixer.music.play()
            self.container = []
        except:
            pass

    def clickOnPause(self):
        try:
            if self.flag:
                self.pushButton_5.setIcon(QIcon('image2.png'))
                self.pushButton_5.setIconSize(QSize(90, 90))
                pygame.mixer.music.unpause()
                self.flag = False
            else:
                self.pushButton_5.setIcon(QIcon('image3.png'))
                self.pushButton_5.setIconSize(QSize(90, 90))
                pygame.mixer.music.pause()
                self.flag = True
        except:
            pass


    def clickOnRewindButton(self):
        try:
            pygame.mixer.music.rewind()
            pygame.mixer.music.unpause()
            self.flag = False
            self.pushButton_5.setIcon(QIcon('image2.png'))
            self.pushButton_5.setIconSize(QSize(90, 90))
        except:
            pass

    def clickOnCreatePlaylist(self):
        if self.flag1:
            self.flag1 = False
            window = CreatePlayList()
            window.show()
            window.exec()
            self.playLists.clear()
            with open(f"C:\\Users\{getuser()}\MusLife\playlist.txt", 'r', encoding='utf-8') as f:
                playlists = f.read().split('\n')
                self.playLists.addItems(playlists)
            self.flag1 = True

    def clickOnDeletePlaylist(self):
        try:
            if self.namePlaylist != 'music':
                with open(f"C:\\Users\{getuser()}\MusLife\playlist.txt", 'r', encoding='utf-8') as f:
                    playlist = f.read().split('\n')
                if self.namePlaylist in playlist:
                    result = []
                    for i in playlist:
                        if i != self.namePlaylist:
                            result.append(i)
                    delete_to_db(self.namePlaylist)
                    self.playLists.clear()
                    self.playLists.addItems(result)
                    with open(f"C:\\Users\{getuser()}\MusLife\playlist.txt", 'w', encoding='utf-8') as f:
                        f.write('\n'.join(result))
                    self.namePlaylist = 'music'
            else:
                warning = DeletePlaylist()
                warning.show()
                warning.exec()
        except:
            pass

    def clickOnOpenPlaylist(self):
        if self.flag2:
            self.flag2 = False
            window = OpenPlayList(self.namePlaylist)
            window.show()
            window.exec()
            self.flag2 = True

    def slider(self):
        try:
            pygame.mixer.music.set_volume(self.verticalSlider.value() / 100)
        except:
            pass

    def clickOnRightButton(self):
        try:
            self.count += 1
            if self.count >= len(self.container):
                self.count -= len(self.container)
            pygame.mixer.music.load(self.container[self.count])
            pygame.mixer.music.play()
            self.flag = False
            self.pushButton_5.setIcon(QIcon('image2.png'))
            self.pushButton_5.setIconSize(QSize(90, 90))
        except:
            pass

    def clickOnLeftButton(self):
        try:
            self.count -= 1
            if self.count < 0:
                self.count += len(self.container)
            pygame.mixer.music.load(self.container[self.count])
            pygame.mixer.music.play()
            self.flag = False
            self.pushButton_5.setIcon(QIcon('image2.png'))
            self.pushButton_5.setIconSize(QSize(90, 90))
        except:
            pass
