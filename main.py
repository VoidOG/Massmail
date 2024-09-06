import logging
import threading
import smtplib
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import sqlite3
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
MAX_EMAILS_PER_DAY = 80
email_counter = 0
email_senders = {
    "imvoid1003@gmail.com": "mjmkalzfveddvkmr",
    "massacres1001@gmail.com": "vjkfmjnsiiajkbzh",
    "usaa45600@gmail.com": "bwgdiqehvemfitjx"
}
AUTHORIZED_USERS = {6663845789, 6551446148, 6698364560, 1110013191}  # Add authorized user IDs here

# Define states for ConversationHandler
CHOOSE_MODE, GET_RECIPIENT, GET_SUBJECT, GET_BODY = range(4)

# Database setup
def setup_database():
    conn = sqlite3.connect('email_stats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS email_log (
                    id INTEGER PRIMARY KEY,
                    sender TEXT,
                    recipient TEXT,
                    subject TEXT,
                    body TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

# Log email sending details
def log_email(sender, recipient, subject, body):
    conn = sqlite3.connect('email_stats.db')
    c = conn.cursor()
    c.execute('INSERT INTO email_log (sender, recipient, subject, body) VALUES (?, ?, ?, ?)', 
              (sender, recipient, subject, body))
    conn.commit()
    conn.close()

# Fetch stats based on time period
def fetch_stats(period):
    conn = sqlite3.connect('email_stats.db')
    c = conn.cursor()
    
    now = datetime.now()
    if period == 'today':
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start_time = now - timedelta(days=now.weekday())  # Start of the week
    else:  # overall
        start_time = datetime.min  # Beginning of time

    c.execute('SELECT COUNT(*) FROM email_log WHERE timestamp >= ?', (start_time,))
    count = c.fetchone()[0]
    
    c.execute('SELECT sender, COUNT(*) FROM email_log WHERE timestamp >= ? GROUP BY sender', (start_time,))
    sender_counts = c.fetchall()
    
    conn.close()
    return count, sender_counts

# Email sending function
def send_email(recipient, subject, body):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 465

        for email, password in email_senders.items():
            try:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = recipient

                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(email, password)
                    server.sendmail(email, recipient, msg.as_string())

                logger.info(f"💥 Email sent successfully from {email}")
                log_email(email, recipient, subject, body)
                break
            except Exception as e:
                logger.error(f"🔥 Error sending email from {email}: {e}")
    except Exception as e:
        logger.error(f"⚠️ Error in sending email: {e}")

# Command handlers
def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss. Tʜɪs ʀᴇᴀʟᴍ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Cenzeo")],
        [InlineKeyboardButton("📢 Cʜᴀɴɴᴇʟ", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "**sᴛᴇᴘ ɪɴᴛᴏ ᴛʜᴇ ғᴜᴛᴜʀᴇ ᴏғ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ ᴡɪᴛʜ ᴍᴀss ᴍᴀɪʟ, ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴏᴏʟ ғᴏʀ ᴘᴇʀsᴏɴᴀʟɪᴢᴇᴅ ʙᴜʟᴋ ᴍᴇssᴀɢɪɴɢ. ᴇɴɢɪɴᴇᴇʀᴇᴅ ʙʏ [C Ξ N Z O](https://t.me/Cenzeo), ᴍᴀss ᴍᴀɪʟ sᴇᴀᴍʟᴇssʟʏ ᴄᴏᴍʙɪɴᴇs ᴀᴅᴠᴀɴᴄᴇᴅ ғᴇᴀᴛᴜʀᴇs wɪᴛʜ ᴇᴀsᴇ ᴏғ ᴜsᴇ, sᴇᴛᴛɪɴɢ ᴀ ɴᴇw sᴛᴀɴᴅᴀʀᴅ ɪɴ ᴏᴜᴛʀᴇᴀᴄʜ. ᴇғғᴏʀtlᴇssʟʏ dᴇʟɪᴠᴇʀ ᴛᴀɪʟᴏʀᴇᴅ ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴇʟᴇᴠᴀᴛᴇ ʏᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ sᴛʀᴀᴛᴇɢʏ ʟɪᴋᴇ ɴᴇvᴇʀ ʙᴇғᴏʀᴇ \n\n** "
        "Tʜɪs ɪs ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛᴇʀ ғᴏʀ ᴇᴍᴀɪʟ ᴅᴏᴍɪɴᴀᴛɪᴏɴ. Cʜᴏᴏsᴇ ʏᴏᴜʀ ᴍᴏᴅᴇ ᴀɴᴅ ʟᴇᴛ ᴛʜᴇ ᴄʜᴀᴏs ʙᴇɢɪɴ. 🎯\n\n"
        " **🔰 Cᴏᴍᴍᴀɴᴅs:**\n"
        " **👉 /send** - Bᴇɢɪɴ ʏᴏᴜʀ ᴇᴍᴀɪʟ ʀᴀɪᴅ.\n"
        " **👉 /help** - Lᴇᴀʀɴ ᴛʜᴇ ʀᴏᴘᴇs.\n"
        " **👉 /cancel** - Aʙᴏʀᴛ ᴍɪssɪᴏɴ.\n\n"
        " **👾 Dᴇᴠᴇʟᴏᴘᴇʀ:** [Cenzo](https://t.me/Cenzeo)"
    )

    update.message.reply_photo(photo="https://telegra.ph/file/0b4853eb7a9d860f3e73b.jpg", caption=welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    return ConversationHandler.END

def help_command(update: Update, context: CallbackContext) -> None:
    help_message = (
        " ** 🛠️ Mᴀss Mᴀɪʟ Cᴏᴍᴍᴀɴᴅ Lɪsᴛ**\n\n"
        " **⚡️ /start** - Sᴜᴍᴍᴏɴ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ.\n"
        " **⚡️ /send** - Exᴇᴄᴜᴛᴇ ʏᴏᴜʀ ᴇᴍᴀɪʟ ᴍɪssɪᴏɴ. ᴛʜᴇ ʙᴏᴛ ɢᴜɪᴅᴇs ʏᴏᴜ sᴛᴇᴘ-ʙʏ-sᴛᴇᴘ.\n"
        " **⚡️ /cancel** - Aʙᴏʀᴛ ᴀɴʏ ᴏɴɢᴏɪɴɢ ᴏᴘᴇʀᴀᴛɪᴏɴ. Dᴏɴ'ᴛ ᴡᴀsᴛᴇ ᴛɪᴍᴇ.\n"
        " **⚡️ /stats** - Sᴇᴄʀᴇᴛ ᴄᴏᴍᴍᴀɴᴅ. Rᴇvᴇᴀʟs ᴛʜᴇ ʙᴏᴛ's ɢʟᴏʙᴀʟ sᴛᴀᴛs. (Pᴀssᴄᴏᴅᴇ nᴇᴇᴅᴇᴅ)\n\n"
        " **🔍 Fᴏʀ mᴏʀᴇ, ᴛᴀᴘ ᴛʜᴇ dᴇᴠᴇʟᴏᴘᴇʀ ʟɪɴᴋ ʙᴇʟᴏᴡ. Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɪɴɴᴇʀ ᴄɪʀᴄʟᴇ.**"
    )
    update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('❌ Mɪssɪᴏɴ ᴀʙᴏʀᴛᴇᴅ. Sᴛᴀɴᴅɪɴɢ ᴅᴏᴡɴ.')
    return ConversationHandler.END

def send_email_handler(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ. Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ.")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("🎯 Sɪɴɢʟᴇ Rᴇᴄɪᴘɪᴇɴᴛ", callback_data='single')],
        [InlineKeyboardButton("💣 Mᴜʟᴛɪᴘʟᴇ Rᴇᴄɪᴘɪᴇɴᴛs", callback_data='multiple')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('🔥 Cʜᴏᴏsᴇ ʏᴏᴜʀ ᴛᴀʀɢᴇᴛ ᴍᴏᴅᴇ:', reply_markup=reply_markup)
    return CHOOSE_MODE

def handle_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in AUTHORIZED_USERS:
        query.answer(text="🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss.")
        return ConversationHandler.END

    query.answer()

    if query.data == 'single':
        query.edit_message_text(text="🎯 Yᴏᴜ sᴇʟᴇᴄᴛᴇᴅ Sɪɴɢʟᴇ Rᴇᴄɪᴘɪᴇɴᴛ. Eɴᴛᴇʀ ᴛʜᴇ ʀᴇᴄɪᴘɪᴇɴᴛ's ᴇᴍᴀɪʟ.")
        return GET_RECIPIENT
    elif query.data == 'multiple':
        query.edit_message_text(text="💣 Yᴏᴜ sᴇʟᴇᴄᴛᴇᴅ Mᴜʟᴛɪᴘʟᴇ Rᴇᴄɪᴘɪᴇɴᴛs. Uᴘʟᴏᴀᴅ ᴀ CSV ғɪʟᴇ wɪᴛʜ ʀᴇᴄɪᴘɪᴇɴᴛ ᴇᴍᴀɪʟs.")
        return GET_RECIPIENT

def receive_recipient_email(update: Update, context: CallbackContext) -> int:
    recipient = update.message.text
    context.user_data['recipient'] = recipient
    update.message.reply_text("📜 Eɴᴛᴇʀ ᴛʜᴇ sᴜʙᴊᴇᴄᴛ ᴏғ ʏᴏᴜʀ ᴇᴍᴀɪʟ:")
    return GET_SUBJECT

def receive_subject(update: Update, context: CallbackContext) -> int:
    subject = update.message.text
    context.user_data['subject'] = subject
    update.message.reply_text("✍️ Nᴏᴡ, ᴛʏᴘᴇ ᴏᴜᴛ ᴛʜᴇ ʙᴏᴅʏ ᴏғ ᴛʜᴇ ᴇᴍᴀɪʟ:")
    return GET_BODY

def receive_body(update: Update, context: CallbackContext) -> int:
    recipient = context.user_data.get('recipient')
    subject = context.user_data.get('subject')
    body = update.message.text

    update.message.reply_text('⚙️ Sᴇɴᴅɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴᴛᴏ ᴛʜᴇ ᴠᴏɪᴅ...')
    threading.Thread(target=send_email, args=(recipient, subject, body)).start()

    update.message.reply_text('✅ ᴇᴍᴀɪʟ sᴇɴᴛ. Mɪssɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇ.')
    return ConversationHandler.END

def stats(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ. Rᴇsᴛʀɪᴄᴛᴇᴅ ᴀʀᴇᴀ.")
        return

    if '911' in context.args:
        keyboard = [
            [InlineKeyboardButton("🕛 Tᴏᴅᴀʏ", callback_data='today')],
            [InlineKeyboardButton("📅 Wᴇᴇᴋʟʏ", callback_data='week')],
            [InlineKeyboardButton("📊 Oᴠᴇʀᴀʟʟ", callback_data='overall')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("**📊 Cʜᴏᴏsᴇ sᴛᴀᴛs ᴛᴏ ᴠɪᴇᴡ:**", reply_markup=reply_markup)
    else:
        update.message.reply_text("🛑 Pᴀssᴄᴏᴅᴇ ʀᴇQᴜɪʀᴇᴅ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ sᴛᴀᴛs. Sᴛᴀʏ ɪɴ ᴛʜᴇ ʟᴏᴏᴘ.")

def display_stats(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    period = query.data

    count, sender_counts = fetch_stats(period)
    stats_message = f"**📊 Eᴍᴀɪʟ Sᴛᴀᴛs ({period.capitalize()}):**\n\n"
    stats_message += f"**📨 Tᴏᴛᴀʟ ᴇᴍᴀɪʟs Sᴇɴᴛ:** {count}\n\n"
    
    if sender_counts:
        stats_message += "**📝 Dᴇᴛᴀɪʟᴇᴅ Bʀᴇᴀᴋᴅᴏᴡɴ ʙʏ Sᴇɴᴅᴇʀ:**\n"
        for sender, sent_count in sender_counts:
            stats_message += f"• **{sender}**: {sent_count} emails\n"
    else:
        stats_message += "⚠️ Nᴏ ᴇᴍᴀɪʟs sᴇɴᴛ ᴅᴜʀɪɴɢ ᴛʜɪs ᴘᴇʀɪᴏᴅ.\n"

    stats_message += "\n🚀 Sᴛᴀʏ sʜᴀʀᴘ, sᴛᴀʏ ʟᴇᴛʜᴀʟ."

    query.edit_message_text(text=stats_message, parse_mode=ParseMode.MARKDOWN)

def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning(f"⚠️ Update {update} caused error {context.error}")

def main() -> None:
    setup_database()  # Initialize the database for logging stats

    # Insert your bot token here
    updater = Updater("6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4", use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CommandHandler("stats", stats, pass_args=True))

    # Conversation handler for email sending
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("send", send_email_handler)],
        states={
            CHOOSE_MODE: [CallbackQueryHandler(handle_choice)],
            GET_RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, receive_recipient_email)],
            GET_SUBJECT: [MessageHandler(Filters.text & ~Filters.command, receive_subject)],
            GET_BODY: [MessageHandler(Filters.text & ~Filters.command, receive_body)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv_handler)

    # Callback query handler for stats buttons
    dp.add_handler(CallbackQueryHandler(display_stats, pattern='^today$|^week$|^overall$'))

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
