from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3

conn = sqlite3.connect("movies.db", check_same_thread=False)
cur = conn.cursor()

# 🔐 CHANGE THIS ID (तुझा Telegram ID)
ADMIN_ID = 1489423238

# ================= CHECK ADMIN =================
def is_admin(user_id):
    return user_id == ADMIN_ID

# ================= ADMIN PANEL =================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Access Denied")
        return

    keyboard = [
        [InlineKeyboardButton("📊 Total Movies", callback_data="total")],
        [InlineKeyboardButton("🗑 Delete Movie", callback_data="delete")],
    ]

    await update.message.reply_text(
        "🔐 Admin Panel",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CALLBACK HANDLER =================
async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text("❌ No Access")
        return

    data = query.data

    # 📊 TOTAL MOVIES
    if data == "total":
        cur.execute("SELECT COUNT(*) FROM movies")
        count = cur.fetchone()[0]

        await query.message.reply_text(f"📊 Total Movies: {count}")

    # 🗑 DELETE ALL (simple version)
    elif data == "delete":
        cur.execute("DELETE FROM movies")
        conn.commit()

        await query.message.reply_text("🗑 All Movies Deleted")
