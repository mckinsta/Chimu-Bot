import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ================= DB =================
conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    name TEXT,
    file_id TEXT
)
""")
conn.commit()

def add_movie(name, file_id):
    cur.execute("INSERT INTO movies VALUES (?, ?)", (name.lower(), file_id))
    conn.commit()

def get_movie(name):
    cur.execute("SELECT file_id FROM movies WHERE name=?", (name.lower(),))
    return cur.fetchall()

# ================= TEMP STORAGE =================
pending = {}

# ================= ADMIN: RECEIVE VIDEO =================
async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    file = update.message.video or update.message.document
    if not file:
        return

    pending[update.effective_user.id] = file.file_id

    await update.message.reply_text("📥 Video received!\nNow send: MovieName 1")

# ================= ADMIN: SAVE NAME =================
async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID or user_id not in pending:
        return

    text = update.message.text

    try:
        name, part = text.rsplit(" ", 1)
    except:
        await update.message.reply_text("❌ Format: MovieName 1")
        return

    file_id = pending.pop(user_id)

    add_movie(name, file_id)

    await update.message.reply_text(f"✅ Saved: {name}")

# ================= SEARCH =================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text

    results = get_movie(name)

    if not results:
        await update.message.reply_text("❌ Not found")
        return

    for row in results:
        await update.message.reply_video(row[0])

# ================= MAIN ROUTER =================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == ADMIN_ID and user_id in pending:
        await receive_name(update, context)
    else:
        await search(update, context)

# ================= MAIN =================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, receive_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🔥 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
