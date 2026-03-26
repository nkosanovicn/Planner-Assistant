import sqlite3
import json
import os

MY_DIR = os.path.dirname(__file__)
SQL_PATH = os.path.join(MY_DIR,'..','data', "todo.db")
DONE_PATH = os.path.join(MY_DIR,'..','data', "done.db")
PROFILE_PATH = os.path.join(MY_DIR,'..','data', "profile.db")

def create_table():

    with sqlite3.connect(SQL_PATH) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY, task TEXT)')
        conn.commit()
        
    with sqlite3.connect(DONE_PATH) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS done(id INTEGER PRIMARY KEY, task TEXT)')
        conn.commit()

def add_data(task):

    with sqlite3.connect(SQL_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO todo(task) VALUES (?)', (task, ))
        conn.commit()

def view_todo():

    with sqlite3.connect(SQL_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM todo')
        data = c.fetchall()
    return data

def view_done():

    with sqlite3.connect(DONE_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM done')
        data = c.fetchall()
    return data

def todo_to_done(id, task):

    with sqlite3.connect(SQL_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM todo WHERE (id, task) = (?, ?)', (id, task))
        conn.commit()

    with sqlite3.connect(DONE_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO done(task) VALUES (?)', (task, ))
        conn.commit()

def done_to_todo(id, task):

    with sqlite3.connect(DONE_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM done WHERE (id, task) = (?, ?)', (id, task))
        conn.commit()
        
    with sqlite3.connect(SQL_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO todo(task) VALUES (?)', (task, ))
        conn.commit()

def delete(id, task):

    with sqlite3.connect(DONE_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM done WHERE (id, task) = (?, ?)', (id, task))
        conn.commit()

def profile_update(profile):
    with sqlite3.connect(PROFILE_PATH) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS profile(key TEXT PRIMARY KEY, value TEXT)')
        conn.commit()

        for k, v in profile.items():
            v = json.dumps(v) if isinstance(v, list) else v
            c.execute(
                'INSERT OR REPLACE INTO profile(key, value) VALUES (?, ?)',
                (k, v)
            )
        conn.commit()