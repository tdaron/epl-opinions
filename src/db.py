import sqlite3
from .cours import Cours

conn = sqlite3.connect("sqlite.db")
cur = conn.cursor()

def setup_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cours (
        code TEXT PRIMARY KEY,
        name TEXT,
        url TEXT,
        description TEXT,
        content TEXT,
        teachers TEXT
    )
    """)
    
def save_cours(cours_dict):
    data = [(c.code, c.name, c.url, c.description, c.content, c.teachers)
            for c in cours_dict.values()]
    cur.executemany("""
    INSERT OR REPLACE INTO cours
    (code, name, url, description, content, teachers)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()

def read_cours_from_db():
    cours_dict = {}
    cur.execute("SELECT code, name, url, description, content, teachers FROM cours")
    rows = cur.fetchall()
    for row in rows:
        c = Cours(
            code=row[0],
            name=row[1],
            url=row[2],
            description=row[3],
            content=row[4],
            teachers=row[5]
        )
        cours_dict[c.url] = c
    print(f"Loaded {len(cours_dict)} courses from the database.")
    return cours_dict
