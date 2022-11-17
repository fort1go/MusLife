from getpass import getuser
import os
import sqlite3


def create_DataBase():
    user = getuser()
    location = f"C:\\Users\{user}\MusLife\playlist_DB.sqlite"
    if not os.path.exists(location):
        con = sqlite3.connect(f"C:\\Users\{user}\MusLife\playlist_DB.sqlite")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS music(
            id INTEGER,
            name TEXT,
            author TEXT,
            location TEXT
        );""")
        con.commit()


def direction_music():
    user = getuser()
    location = f"C:\\Users\{user}\MusLife\music"
    if not os.path.isdir(location):
        os.mkdir(location)


def text_playlists():
    user = getuser()
    location = f"C:\\Users\{user}\MusLife\playlist.txt"
    if not os.path.exists(location):
        with open(location, 'w', encoding='utf-8') as f:
            f.write('music')


def createDirection():
    user = getuser()
    location = f"C:\\Users\{user}\MusLife"
    if not os.path.isdir(location):
        os.mkdir(location)