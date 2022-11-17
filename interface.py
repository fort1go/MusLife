from getpass import getuser


class Interfeace:
    def initUi(self):
        with open(f"C:\\Users\{getuser()}\MusLife\playlist.txt", 'r', encoding='utf-8') as f:
            playlists = f.read().split('\n')
        with open(f"play.txt", 'w', encoding='utf-8') as f:
            pass
        self.playLists.addItems(playlists)

        self.namePlaylist = 'music'

        self.flag1 = True
        self.flag2 = True
        self.flag3 = True

        self.count = 0
        self.container = []
        self.length_container = 0

    def onActivated(self, text):
        self.namePlaylist = text