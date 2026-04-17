import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIG ---
TOKEN = "8564199755:AAHp0alINxkFcHKKCDzgFMquJzYzpH6Zx6Q"

# --- CHANNEL DATA ---
CHANNELS = {
    "Psychology": [
        {"name": "Mind Matters India", "link": "https://t.me/mindmattersindia", "desc": "Mental health, OCD, anxiety in Indian context"},
        {"name": "Psychology Hindi", "link": "https://t.me/psychologyhindi", "desc": "Psychology concepts explained in Hindi"},
        {"name": "The Psychology Club", "link": "https://t.me/thepsychologyclub", "desc": "Daily psychology insights and research"},
    ],
    "History": [
        {"name": "Indian History Daily", "link": "https://t.me/indianhistorydaily", "desc": "Forgotten stories from Indian history"},
        {"name": "History of India", "link": "https://t.me/historyofindia", "desc": "Ancient to modern Indian history"},
        {"name": "Bharatvarsh", "link": "https://t.me/bharatvarsh", "desc": "Hindu civilisation and historical culture"},
    ],
    "Travel": [
        {"name": "India Travel Tips", "link": "https://t.me/indiatraveltips", "desc": "Budget travel, hidden gems across India"},
        {"name": "Backpacking India", "link": "https://t.me/backpackingindia", "desc": "Solo travel experiences and guides"},
        {"name": "Incredible India", "link": "https://t.me/incredibleindiachannel", "desc": "Photography and travel stories from India"},
    ],
}

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in CHANNELS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🇮🇳 *Indian Telegram Channel Finder*\n\nChoose a category to discover channels:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data

    if category not in CHANNELS:
        await query.edit_message_text("Category not found.")
        return

    channels = CHANNELS[category]
    text = f"📚 *{category} Channels*\n\n"
    for ch in channels:
        text += f"• [{ch['name']}]({ch['link']})\n  _{ch['desc']}_\n\n"

    keyboard = [[InlineKeyboardButton("⬅️ Back to Categories", callback_data="back")]]
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in CHANNELS]
    await query.edit_message_text(
        "🇮🇳 *Indian Telegram Channel Finder*\n\nChoose a category to discover channels:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- MAIN ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(category_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
