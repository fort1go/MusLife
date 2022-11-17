from PyQt5.QtWidgets import *
from data_base import see_music, delete_music, check_music_in_db, add_to_db, length, create_to_db, changes
from getpass import getuser


class CreatePlayList(QDialog):
    def __init__(self):
        super(CreatePlayList, self).__init__()
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Создать Плейлист')

        self._text = QLabel(self)
        self._text.move(20, 20)
        self._text.setText('Введите название плейлиста:')

        self._input = QLineEdit(self)
        self._input.move(20, 40)
        self._input.resize(360, 60)

        self._btn = QPushButton(self)
        self._btn.move(20, 120)
        self._btn.resize(360, 50)
        self._btn.setText('Создать')

        self._warning = QLabel(self)
        self._warning.move(20, 240)
        self._warning.resize(450, 30)
        self._warning.setText('')

        self._list = QLabel(self)
        self._list.move(160, 180)
        self._list.setText("Плейлисты:")

        self._combo = QComboBox(self)
        self._combo.move(20, 200)
        self._combo.resize(360, 30)
        with open(f'C:\\Users\{getuser()}\MusLife\playlist.txt', 'r', encoding='utf-8') as f:
            playlists = f.read().split('\n')
        self._combo.addItems(playlists)

        self._btn.clicked.connect(self._create)

    def _create(self):
        try:
            if self._input.text():
                if ' ' not in self._input.text():
                    with open(f'C:\\Users\{getuser()}\MusLife\playlist.txt', 'r', encoding='utf-8') as f:
                        playlists = f.read().split('\n')
                    tmp = playlists
                    if self._input.text() not in playlists:
                        create_to_db(self._input.text())
                        with open(f'C:\\Users\{getuser()}\MusLife\playlist.txt', 'w', encoding='utf-8') as f:
                            f.write('\n'.join(tmp))
                            f.write('\n' + self._input.text())
                        self.close()
                    else:
                        self._warning.setText('Такой плейлист уже есть')
                else:
                    self._warning.setText('В названии не должно быть пробелов')
            else:
                self._warning.setText('Вы ничего не ввели')
        except:
            self._warning.setText("В названии не должны присутсвовать специальные символы")


class DeletePlaylist(QDialog):
    def __init__(self):
        super(DeletePlaylist, self).__init__()

        self.setGeometry(300, 300, 400, 70)
        self.setWindowTitle('Warning')

        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText('Плейлист "music" является системным, его нельзя удалить!')

        self.btn = QPushButton(self)
        self.btn.move(300, 40)
        self.btn.resize(80, 25)
        self.btn.setText('ОК')

        self.btn.clicked.connect(self.stop)

    def stop(self):
        self.close()


class OpenPlayList(QDialog):
    def __init__(self, table):
        super(OpenPlayList, self).__init__()

        self.fname = "NO CONNECT"

        self.table = table
        self.args = see_music(table)
        self._list = list(map(lambda x: '_'.join(x[0:2]), self.args))
        if not len(self.args):
            self.nameMusic = ""
        else:
            self.nameMusic = self._list[0]

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Плейлист')

        self.btn = QPushButton(self)
        self.btn.move(150, 20)
        self.btn.resize(200, 60)
        self.btn.setText('Выбрать песню')

        self.t1 = QLabel(self)
        self.t1.move(20, 90)
        self.t1.setText("Введите название:")

        self.t2 = QLabel(self)
        self.t2.move(190, 90)
        self.t2.setText("Введите автора:")

        self.name = QLineEdit(self)
        self.name.move(20, 120)
        self.name.resize(150, 50)

        self.author = QLineEdit(self)
        self.author.move(190, 120)
        self.author.resize(150, 50)

        self.add = QPushButton(self)
        self.add.move(360, 120)
        self.add.resize(120, 50)
        self.add.setText('Добавить')

        self.combo = QComboBox(self)
        self.combo.addItems(self._list)
        self.combo.move(20, 190)
        self.combo.resize(320, 50)
        self.combo.activated[str].connect(self.onActivated)

        self.delete = QPushButton(self)
        self.delete.move(360, 190)
        self.delete.resize(120, 50)
        self.delete.setText('Удалить')

        self.lbl = QLabel(self)
        self.lbl.move(20, 260)
        self.lbl.setText("")
        self.lbl.resize(450, 60)

        self.btn.clicked.connect(self.open_music)
        self.add.clicked.connect(self.add_to_music)
        self.delete.clicked.connect(self.delete_to_music)

    def open_music(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать песню', '', '*.mp3')[0]

    def add_to_music(self):
        try:
            if self.fname == "NO CONNECT":
                self.lbl.setText("Выберите песню!")
            else:
                music = check_music_in_db(self.table, self.fname)
                if not check_music_in_db(self.table, self.fname):
                    _len = length(self.table) + 1
                    name = self.name.text()
                    author = self.author.text()
                    if name and author:
                        add_to_db(_len, author, name, self.fname, self.table)
                        self.combo.clear()
                        self.args = see_music(self.table)
                        self._list = list(map(lambda x: '_'.join(x[0:2]), self.args))
                        self.combo.addItems(self._list)
                        self.name.setText("")
                        self.author.setText("")
                    else:
                        self.lbl.setText(f"""Введите название и автора песни""")
                else:
                    self.lbl.setText(f"Данная песня уже есть в плейлисте\nНазвание: {music[0]}    Автор: {music[1]}\n"
                                     f"Путь: {self.fname}")
        except:
            self.lbl.setText("Произошла Ошибка. Повторите попытку позднее.")

    def delete_to_music(self):
        try:
            if not self._list and not self.nameMusic:
                self.lbl.setText("В плейлисте нет песен")
            else:
                if self.table != 'music':
                    name, author = self.nameMusic.split('_')
                    location = False
                    for i in self._list:
                        if i.split('_')[0] == name and author == i.split('_')[1]:
                            location = True
                            break
                    if location:
                        delete_music(self.table, name, author)
                    self.combo.clear()
                    self.args = see_music(self.table)
                    self._list = list(map(lambda x: '_'.join(x[0:2]), self.args))
                    self.combo.addItems(self._list)
                    self.lbl.setText("")
                else:
                    self.lbl.setText("Из плейлиста music нельзя ничего удалять")
        except:
            self.lbl.setText("Выберите песню!")

    def onActivated(self, text):
        self.nameMusic = text


class PlayPlayList(QDialog):
    def __init__(self, con):
        super(PlayPlayList, self).__init__()

        self.table = con
        self.args = []

        with open(f'C:\\Users\{getuser()}\MusLife\playlist.txt', 'r', encoding='utf-8') as f:
            self.args = f.read().split('\n')

        self.setGeometry(300, 300, 500, 160)
        self.setWindowTitle("Плейлисты")

        self.text = self.args[0]

        self.combo = QComboBox(self)
        self.combo.addItems(self.args)
        self.combo.move(20, 20)
        self.combo.resize(460, 50)
        self.combo.activated[str].connect(self.onActivated)

        self.btn = QPushButton(self)
        self.btn.move(20, 90)
        self.btn.resize(460, 50)
        self.btn.setText("Выбрать")

        self.btn.clicked.connect(self.click)

    def onActivated(self, text):
        self.text = text

    def click(self):
        self.table = self.text
        result = []
        for i in changes(self.table):
            result.append(i[0])
        with open('play.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(result))
        self.close()