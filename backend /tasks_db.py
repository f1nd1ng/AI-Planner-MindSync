# tasks_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                emotion TEXT,
                status TEXT
                )""")
    conn.commit()
    conn.close()

def save_task(task, emotion, status):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, emotion, status) VALUES (?, ?, ?)", (task, emotion, status))
    conn.commit()
    conn.close()
