from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram import Update
from admin import admin_panel, admin_button
from premium import send_temp_movie
import sqlite3

TOKEN = "PUT_YOUR_TOKEN_HERE"

# ================= DB =================
conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    name TEXT,
    part INTEGER,
    file_id TEXT
)
""")
conn.commit()

# ================= CLEAN =================
def clean(name):
    return name.lower().strip().replace(".mp4", "")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Bot ready! Send movie with caption")

# ================= SAVE =================
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.video:
        return

    if not update.message.caption:
        await update.message.reply_text("❌ Caption madhe movie name dya")
        return

    file_id = update.message.video.file_id
    name = clean(update.message.caption)

    print("SAVED:", name)

    cur.execute(
        "INSERT INTO movies VALUES (?, ?, ?)",
        (name, 1, file_id)
    )
    conn.commit()

    await update.message.reply_text("✅ Movie saved 👍")

# ================= SEARCH =================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    text = clean(update.message.text)

    print("SEARCH:", text)

    cur.execute("SELECT name FROM movies")
    print("ALL MOVIES:", cur.fetchall())

    cur.execute(
        "SELECT file_id FROM movies WHERE name LIKE ?",
        (f"%{text}%",)
    )
    data = cur.fetchone()

    if data:
        file_id = data[0]
        await send_temp_movie(update, context, file_id)
    else:
        await update.message.reply_text("❌ Movie not found 😢")

# ================= APP =================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# ✅ Save only videos (with or without caption)
app.add_handler(MessageHandler(filters.VIDEO, save_movie))

# ✅ IMPORTANT FIX: ignore captions (video text)
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND & ~filters.Caption(True),
    search
))

app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CallbackQueryHandler(admin_button))

print("🚀 Bot starting...")
app.run_polling(drop_pending_updates=True)
