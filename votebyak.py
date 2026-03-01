import logging
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ===== CONFIG =====
BOT_TOKEN = "8480674536:AAFCDGEKcTXRfMdMYb4b3BtYkxD6fT9OoO0"
CHANNEL_CHAT_ID = -1002807063655
CHANNEL_LINK = "https://t.me/+UmlcI4WmOuFmYzVl"

logging.basicConfig(level=logging.INFO)

EMOJIS = ["🥰", "😍", "❣️", "💘"]

active_votes = {}
voted_users = {}

def bold_text(text):
    bold_map = {
        "a":"𝐚","b":"𝐛","c":"𝐜","d":"𝐝","e":"𝐞","f":"𝐟","g":"𝐠","h":"𝐡","i":"𝐢",
        "j":"𝐣","k":"𝐤","l":"𝐥","m":"𝐦","n":"𝐧","o":"𝐨","p":"𝐩","q":"𝐪","r":"𝐫",
        "s":"𝐬","t":"𝐭","u":"𝐮","v":"𝐯","w":"𝐰","x":"𝐱","y":"𝐲","z":"𝐳",
        "A":"𝐀","B":"𝐁","C":"𝐂","D":"𝐃","E":"𝐄","F":"𝐅","G":"𝐆","H":"𝐇","I":"𝐈",
        "J":"𝐉","K":"𝐊","L":"𝐋","M":"𝐌","N":"𝐍","O":"𝐎","P":"𝐏","Q":"𝐐","R":"𝐑",
        "S":"𝐒","T":"𝐓","U":"𝐔","V":"𝐕","W":"𝐖","X":"𝐗","Y":"𝐘","Z":"𝐙"
    }
    return "".join(bold_map.get(c, c) for c in text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please Send your Name")

async def create_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    styled_name = bold_text(name)
    emoji = random.choice(EMOJIS)

    message = await context.bot.send_message(
        chat_id=CHANNEL_CHAT_ID,
        text=f"{styled_name}\n\n<b>@Team_NovaG</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji} 0", callback_data="vote")]
        ])
    )

    active_votes[message.message_id] = {
        "emoji": emoji,
        "count": 0
    }

    voted_users[message.message_id] = set()

    vote_link = f"https://t.me/c/{str(CHANNEL_CHAT_ID)[4:]}/{message.message_id}"

    await update.message.reply_text(
        f"✅ 𝐕𝐨𝐭𝐞 𝐂𝐫𝐞𝐚𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!\n\n"
        f"📢 Channel Link:\n{CHANNEL_LINK}\n\n"
        f"🗳 Direct Vote Link:\n{vote_link}\n"
        f"\n━━━━━━━━━━━━━━━"
        f"\n MADE BY  𝐀𝐍𝐔𝐑𝐀𝐆 𝐒𝐈𝐍𝐆𝐇 💘"
        f"\n━━━━━━━━━━━━━━━"
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message_id = query.message.message_id
    user_id = query.from_user.id

    if message_id not in active_votes:
        return

    if user_id in voted_users[message_id]:
        await query.answer("Already Voted ❌")
        return

    voted_users[message_id].add(user_id)
    active_votes[message_id]["count"] += 1

    data = active_votes[message_id]

    await context.bot.edit_message_reply_markup(
        chat_id=CHANNEL_CHAT_ID,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"{data['emoji']} {data['count']}",
                callback_data="vote"
            )]
        ])
    )

    await query.answer("Vote Counted ❤️")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_vote))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()