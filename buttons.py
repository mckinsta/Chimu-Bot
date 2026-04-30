from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def movie_buttons(name, parts):
    keyboard = []
    for p in parts:
        keyboard.append([InlineKeyboardButton(f"🎬 Part {p}", callback_data=f"{name}:{p}")])

    return InlineKeyboardMarkup(keyboard)
