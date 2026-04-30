from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3

TOKEN = "8350441049:AAHEaYW3qaJPT0k761ScXDUqgufhwomSErI"

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

# ================= CLEAN NAME =================
def clean(name):
    return name.lower().strip().replace(".mp4", "")

# ================= SAVE MOVIE =================
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        name = update.message.caption or "unknown"
        name = clean(name)

        cur.execute(
            "INSERT INTO movies VALUES (?, ?, ?)",
            (name, 1, file_id)
        )
        conn.commit()

        await update.message.reply_text("Movie saved 👍")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ready 👍 Send movie with caption")

# ================= SEARCH =================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = clean(update.message.text)

    cur.execute("SELECT file_id FROM movies WHERE name=?", (text,))
    data = cur.fetchone()

    if data:
        from premium import send_temp_movie
        await send_temp_movie(update, context, file_id)
    else:
        await update.message.reply_text("Movie not found 😢")

# ================= APP =================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, save_movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CallbackQueryHandler(admin_button))
print("Bot starting...")
app.run_polling(drop_pending_updates=True)
