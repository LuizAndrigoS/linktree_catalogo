import sqlite3

conn = sqlite3.connect('catalogos.db')
conn.execute("""
CREATE TABLE catalogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    link TEXT NOT NULL
)
""")
conn.close()