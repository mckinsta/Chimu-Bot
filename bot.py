import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from db import add_movie, get_movie

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Movie Bot Ready!\nSend movie name.")

# SAVE MOVIE (ADMIN ONLY)
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("User ID:", update.effective_user.id)

    # 🔒 admin check
    if update.effective_user.id != ADMIN_ID:
        print("Not admin ❌")
        return

    if update.message.video or update.message.document:
        file = update.message.video or update.message.document
        caption = update.message.caption

        print("Caption:", caption)

        if not caption:
            await update.message.reply_text("❌ Caption tak: MovieName 1")
            return

        try:
            name, part = caption.rsplit(" ", 1)
            part = int(part)
        except:
            await update.message.reply_text("❌ Format wrong\nExample: KGF 1")
            return

        add_movie(name, part, file.file_id)

        print("Saved:", name, part, file.file_id)

        await update.message.reply_text(f"✅ Saved: {name} Part {part}")

# SEARCH MOVIE
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    results = get_movie(name)

    if not results:
        await update.message.reply_text("❌ Movie not found")
        return

    for file_id in results:
        msg = await update.message.reply_video(file_id[0])

        # ⏳ AUTO DELETE AFTER 5 MIN
        await asyncio.sleep(300)
        try:
            await msg.delete()
        except:
            pass

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, save_movie))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("Bot running 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
