import sqlite3
from .cours import Cours

DB_FILE = "sqlite.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

def setup_tables():
    print("Creating..")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cours (
        code TEXT PRIMARY KEY,
        programs TEXT,
        name TEXT,
        url TEXT,
        description TEXT,
        content TEXT,
        teachers TEXT
    )
    """)

def clear_database():
    print("Clearing..")
    cur.execute("""
    DROP TABLE IF EXISTS cours
    """)
    
def save_cours(cours_dict):
    data = [(c.code, ",".join(c.programs), c.name, c.url, c.description, c.content, c.teachers)
            for c in cours_dict.values()]
    cur.executemany("""
    INSERT OR REPLACE INTO cours
    (code, programs, name, url, description, content, teachers)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()

def read_cours_from_db():
    cours_dict = {}
    cur.execute("SELECT code, programs, name, url, description, content, teachers FROM cours")
    rows = cur.fetchall()
    for row in rows:
        c = Cours(
            code=row[0],
            programs=row[1].split(","),
            name=row[2],
            url=row[3],
            description=row[4],
            content=row[5],
            teachers=row[6]
        )
        cours_dict[c.url] = c
    print(f"Loaded {len(cours_dict)} courses from the database.")
    return cours_dict
