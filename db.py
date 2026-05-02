import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")
conn.commit()

def add_movie(name, part, file_id):
    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (%s, %s, %s)",
        (name.lower().strip(), part, file_id)
    )
    conn.commit()

def get_movie(name):
    cur.execute(
        "SELECT file_id FROM movies WHERE name=%s ORDER BY part",
        (name.lower().strip(),)
    )
    return cur.fetchall()
