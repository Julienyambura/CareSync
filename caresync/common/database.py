# Database helpers for CareSync (stub) 

import sqlite3
from datetime import date

DB_PATH = 'caresync.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY, name TEXT, dose TEXT, frequency TEXT, time TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS med_logs (
        id INTEGER PRIMARY KEY, med_id INTEGER, log_date TEXT, status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS moods (
        id INTEGER PRIMARY KEY, mood INTEGER, mood_emoji TEXT, mood_date TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS journals (
        id INTEGER PRIMARY KEY, entry TEXT, journal_date TEXT
    )''')
    conn.commit()
    conn.close()

def add_medication(name, dose, frequency, time):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO medications (name, dose, frequency, time) VALUES (?, ?, ?, ?)', (name, dose, frequency, time))
    conn.commit()
    conn.close()

def get_today_medications():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('SELECT * FROM medications')
    meds = c.fetchall()
    c.execute('SELECT med_id, status FROM med_logs WHERE log_date=?', (today,))
    logs = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return meds, logs

def log_medication(med_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('INSERT OR REPLACE INTO med_logs (med_id, log_date, status) VALUES (?, ?, ?)', (med_id, today, status))
    conn.commit()
    conn.close()

def add_mood(mood, mood_emoji):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('INSERT INTO moods (mood, mood_emoji, mood_date) VALUES (?, ?, ?)', (mood, mood_emoji, today))
    conn.commit()
    conn.close()

def get_moods():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT mood, mood_emoji, mood_date FROM moods ORDER BY mood_date DESC LIMIT 30')
    moods = c.fetchall()
    conn.close()
    return moods

def add_journal(entry):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('INSERT INTO journals (entry, journal_date) VALUES (?, ?)', (entry, today))
    conn.commit()
    conn.close()

def get_journals():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT entry, journal_date FROM journals ORDER BY journal_date DESC LIMIT 30')
    journals = c.fetchall()
    conn.close()
    return journals 