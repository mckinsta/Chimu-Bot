import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from db import get_movie

TOKEN = os.getenv("USER_BOT_TOKEN")

# 🔍 Search function
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text

    results = get_movie(name)

    if not results:
        await update.message.reply_text("❌ Movie not found")
        return

    # 🔗 Replace with your MAIN bot username
    BOT_USERNAME = "YOUR_SAVER_BOT_USERNAME"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📥 Watch Movie",
            url=f"https://t.me/{BOT_USERNAME}?start={name}"
        )]
    ])

    await update.message.reply_text(
        f"🎬 {name} found",
        reply_markup=keyboard
    )

# 🚀 Main
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("Search Bot Running 🔍")
    app.run_polling()

if __name__ == "__main__":
    main()
