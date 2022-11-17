import sys
from PyQt5 import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from buttons import Buttons
from function import *


class Window(QMainWindow, Buttons):
    def __init__(self):
        super(Window, self).__init__()

        uic.loadUi('projectYandexLyceum.ui', self)

        self.id = 0

        self.verticalSlider.setInvertedAppearance(False)
        self.verticalSlider.setValue(100)
        self.verticalSlider.valueChanged.connect(self.slider)

        self.searchingButton.clicked.connect(self.clickOnSearchingButton)
        self.dowload.clicked.connect(self.clickOnDowload)
        self.addPlaylist.clicked.connect(self.clickOnAddPlaylist)
        self.initUi()
        self.playLists.activated[str].connect(self.onActivated)
        self.createPlaylist.clicked.connect(self.clickOnCreatePlaylist)
        self.deletePlaylist.clicked.connect(self.clickOnDeletePlaylist)
        self.openPlaylist.clicked.connect(self.clickOnOpenPlaylist)
        self.playMusic.clicked.connect(self.clickOnPlayMusic)
        self.pushButton_5.clicked.connect(self.clickOnPause)
        self.rewindButton.clicked.connect(self.clickOnRewindButton)
        self.playPlaylist.clicked.connect(self.clickOnPlayPlaylist)
        self.pushButton_5.setIcon(QIcon('image2.png'))
        self.pushButton_5.setIconSize(QSize(90, 90))
        self.rewindButton.setIcon(QIcon('image4.png'))
        self.rewindButton.setIconSize(QSize(61, 61))
        self.right.clicked.connect(self.clickOnRightButton)
        self.right.setIcon(QIcon('image_right.png'))
        self.right.setIconSize(QSize(93, 41))
        self.left.clicked.connect(self.clickOnLeftButton)
        self.left.setIcon(QIcon('image_left.png'))
        self.left.setIconSize(QSize(93, 41))

        pixmap = QPixmap('image.png').scaled(861, 511)
        self.imageMusic.setPixmap(pixmap)
        pixmap = QPixmap('image_play.png').scaled(741, 321)
        self.label.setPixmap(pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    createDirection()
    create_DataBase()
    direction_music()
    text_playlists()
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())