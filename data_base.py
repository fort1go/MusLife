def add_to_db(id: int, author: str, name: str, location: str, table_name: str) -> None:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    cur.execute(f"""
        INSERT INTO {table_name} VALUES ({id}, '{name}', '{author}', '{location}')""")
    con.commit()


def create_to_db(table_name: str) -> None:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER, name TEXT, author TEXT, location TEXT);""")
    con.commit()


def delete_to_db(table_name: str) -> None:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    cur.execute(f"""DROP TABLE {table_name};""")
    con.commit()


def changes(table_name: str) -> list:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""
                    SELECT location FROM {table_name}""").fetchall()
    return result


def check(table_name: str) -> list:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""
                SELECT name, author, location FROM {table_name}""").fetchall()
    return result


def length(table_name: str) -> int:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    res = cur.execute(f"""SELECT * FROM {table_name}""").fetchall()
    return len(res)


def see_music(table_name: str) -> list:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    res = cur.execute(f"""SELECT name, author, location FROM {table_name}""").fetchall()
    return res


def delete_music(table_name: str, name: str, author: str) -> None:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    cur.execute(f"""DELETE FROM {table_name} WHERE
        name = '{name}' AND author = '{author}'""")
    con.commit()


def check_music_in_db(table_name: str, _location: str) -> list:
    import sqlite3
    from getpass import getuser
    _loc = _location.split('/')
    name_file = _loc[-1]
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name, author, location FROM {table_name}""").fetchall()
    for i in result:
        if name_file in i[2]:
            return list(i)
    return []


def check_add_music_main(table_name: str, name: str, author: str, location: str) -> list:
    import sqlite3
    from getpass import getuser
    con = sqlite3.connect(f'C:\\Users\{getuser()}\MusLife\playlist_DB.sqlite')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name, author, location FROM {table_name} 
        WHERE name = '{name}' AND author = '{author}' AND location = '{location}'""").fetchall()
    return result