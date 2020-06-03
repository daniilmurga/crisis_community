import sqlite3

def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect('anketa.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):

    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            text        TEXT NOT NULL
        )
    ''')

    conn.commit()


@ensure_connection
def add_message(conn, user_id: int, text: str):
    c = conn.cursor()
    c.execute('INSERT INTO user_message (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()

@ensure_connection
def check_club(conn):
    c = conn.cursor()
    c.execute('SELECT id, user_id FROM user_message')
    return c.fetchall()
