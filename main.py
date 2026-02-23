import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))

CHANNEL_LINK = "https://t.me/poetry_gram"


quotes = [
    "Some people leave, but their timing stays.",
    "Peace feels unfamiliar after chaos.",
    "You didn’t ask for much, just consistency.",
    "Not every silence means absence.",
    "You outgrew what once broke you.",
    "Closure sometimes arrives as acceptance.",
    "The heart remembers what the mind forgets.",
    "You were never hard to love — just hard to keep.",
    "Healing is quieter than hurting.",
    "Some chapters don’t end, they fade."
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖤 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✍️ Send Poem", callback_data="poem")],
        [InlineKeyboardButton("🤍 Confession", callback_data="confession")],
        [InlineKeyboardButton("✨ Need a line", callback_data="line")]
    ]
    await update.message.reply_text(
        "Welcome to Tangled.\nShare what you can't keep inside.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "poem":
        context.user_data["mode"] = "poem"
        await query.message.reply_text("Send your poem.")

    elif query.data == "confession":
        context.user_data["mode"] = "confession"
        await query.message.reply_text("Write your confession.")

    elif query.data == "line":
        await query.message.reply_text(random.choice(quotes))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    text = update.message.text

    if mode == "poem":
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"POEM:\n\n{text}"
        )
        await update.message.reply_text("Received 🖤")
        context.user_data.clear()

    elif mode == "confession":
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"CONFESSION:\n\n{text}"
        )
        await update.message.reply_text("Received 🖤")
        context.user_data.clear()

    else:
        await update.message.reply_text("Press /start first.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
