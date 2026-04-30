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

# 🔥 speed sathi index
cur.execute("CREATE INDEX IF NOT EXISTS idx_name ON movies(name)")
conn.commit()

# ================= CLEAN =================
def clean(name):
    return name.lower().strip().replace(".mp4", "")

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Bot ready!")

# ================= SAVE =================
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.video:
        return

    if not update.message.caption:
        await update.message.reply_text("❌ Caption madhe movie name dya")
        return

    file_id = update.message.video.file_id
    name = clean(update.message.caption)

    cur.execute(
        "INSERT INTO movies VALUES (?, ?, ?)",
        (name, 1, file_id)
    )
    conn.commit()

    await update.message.reply_text("✅ Saved")

# ================= SEARCH =================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = clean(update.message.text)

    cur.execute(
        "SELECT file_id FROM movies WHERE name LIKE ? LIMIT 1",
        (f"%{text}%",)
    )
    data = cur.fetchone()

    if data:
        file_id = data[0]

        # 🔥 FASTEST METHOD
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=file_id
        )
    else:
        await update.message.reply_text("❌ Movie not found")

# ================= APP =================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# 🎥 save
app.add_handler(MessageHandler(filters.VIDEO, save_movie))

# 🔍 search
app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    search
))

app.add_handler(CommandHandler("admin", admin_panel))
app.add_handler(CallbackQueryHandler(admin_button))

print("🚀 Fast Bot Started")
app.run_polling(drop_pending_updates=True)
