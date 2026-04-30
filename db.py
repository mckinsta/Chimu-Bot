import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

# ================= TABLE =================
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")

conn.commit()

# ================= CLEAN NAME =================
def clean(name):
    return name.lower().strip().replace(".mp4", "")

# ================= ADD MOVIE =================
def add_movie(name, part, file_id):
    name = clean(name)

    cur.execute(
        "INSERT INTO movies VALUES (?, ?, ?)",
        (name, part, file_id)
    )
    conn.commit()

# ================= GET PARTS =================
def get_parts(name):
    name = clean(name)

    cur.execute("SELECT part FROM movies WHERE name=?", (name,))
    return [i[0] for i in cur.fetchall()]

# ================= GET SPECIFIC PART =================
def get_movie(name, part):
    name = clean(name)

    cur.execute(
        "SELECT file_id FROM movies WHERE name=? AND part=?",
        (name, part)
    )

    data = cur.fetchone()
    return data[0] if data else None
