import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# ================= AUTO DELETE =================
async def send_and_delete(context: ContextTypes.DEFAULT_TYPE, chat_id, file_id):
    msg = await context.bot.send_video(chat_id, file_id)

    # ⏳ 5 minutes = 300 seconds
    await asyncio.sleep(300)

    try:
        await context.bot.delete_message(chat_id, msg.message_id)
    except:
        pass


# ================= WRAPPER FUNCTION =================
async def send_temp_movie(update: Update, context: ContextTypes.DEFAULT_TYPE, file_id):
    chat_id = update.effective_chat.id
    await send_and_delete(context, chat_id, file_id)
