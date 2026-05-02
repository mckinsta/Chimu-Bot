import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from db import add_movie, get_movie

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 🔁 temp storage
pending = {}

# 🎥 STEP 1: receive video
async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    file = update.message.video or update.message.document
    if not file:
        return

    pending[update.effective_user.id] = file.file_id

    await update.message.reply_text("📥 Video received!\nNow send: MovieName 1")

# 📝 STEP 2: receive name
async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.effective_user.id not in pending:
        return

    text = update.message.text

    try:
        name, part = text.rsplit(" ", 1)
        part = int(part)
    except:
        await update.message.reply_text("❌ Format: MovieName 1")
        return

    file_id = pending.pop(update.effective_user.id)

    add_movie(name, part, file_id)

    await update.message.reply_text(f"✅ Saved: {name} Part {part}")

# 🔍 SEARCH
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = get_movie(update.message.text)

    if not results:
        await update.message.reply_text("❌ Not found")
        return

    for file_id in results:
        await update.message.reply_video(file_id[0])

# 🚀 MAIN
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, receive_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("Bot running 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
