import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# 🔐 Get DB URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found! Railway variables check kar.")

# 🔌 Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 🧱 Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")
conn.commit()


# ➕ Add movie
def add_movie(name, part, file_id):
    cur.execute(
        "INSERT INTO movies (name, part, file_id) VALUES (%s, %s, %s)",
        (name.lower().strip(), part, file_id)
    )
    conn.commit()


# 🔍 Get movie
def get_movie(name):
    cur.execute(
        "SELECT file_id FROM movies WHERE name=%s ORDER BY part",
        (name.lower().strip(),)
    )
    return cur.fetchall()


# ❌ Optional: delete movie
def delete_movie(name):
    cur.execute(
        "DELETE FROM movies WHERE name=%s",
        (name.lower().strip(),)
    )
    conn.commit()
