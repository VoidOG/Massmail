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
MAX_EMAILS_PER_DAY = 500
email_counter = 0
email_senders = {
    "imvoid1003@gmail.com": "mjmkalzfveddvkmr",
    "massacres1001@gmail.com": "vjkfmjnsiiajkbzh",
    "usaa45600@gmail.com": "bwgdiqehvemfitjx",
    "lolwhosucks@gmail.com": "rssrsfmnpmzjtcxl",
    "Yourmomsucksmine69@gmail.com": "urpcznlkyazksbsr"
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

# Thread lock for email counter
email_counter_lock = threading.Lock()

# Email sending function
def send_email(recipient, subject, body):
    global email_counter
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
                
                with email_counter_lock:
                    email_counter += 1
                    print(f"ᴇᴍᴀɪʟ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ✅ ᴄᴏᴜɴᴛ: {email_counter}")
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
    help_text = (
        "**🆘 Hᴇʟᴘ**\n\n"
        "ɢᴜɪᴅᴇ ᴏɴ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ:\n\n"
        "**1. /send** - ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇɴᴅ ᴀɴ ᴇᴍᴀɪʟ. ʏᴏᴜ'ʟʟ ʙᴇ ᴀsᴋᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ʀᴇᴄɪᴘɪᴇɴᴛ, sᴜʙᴊᴇᴄᴛ, ᴀɴᴅ ʙᴏᴅʏ.\n"
        "**2. /help** - ᴅɪsᴘʟᴀʏs ᴛʜᴇsᴇ ʜᴇʟᴘ ᴏᴘᴛɪᴏɴs.\n"
        "**3. /cancel** - ᴀʙᴏʀᴛs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ.\n\n"
        "Fᴏʀ ᴀɴʏ ɪssᴜᴇs, ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ [sᴜᴘᴘᴏʀᴛ](https://t.me/Cenzeo)."
    )
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

def cancel(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss. Tʜɪs ʀᴇᴀʟᴍ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.")
        return ConversationHandler.END

    update.message.reply_text("❌ Cᴀɴᴄᴇʟʟᴇᴅ. ʜᴀᴠᴇ ᴀ ɴɪᴄᴇ ᴅᴀʏ!")
    return ConversationHandler.END

def send(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 Uɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss. Tʜɪs ʀᴇᴀʟᴍ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.")
        return ConversationHandler.END

    update.message.reply_text("✉️ Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʀᴇᴄɪᴘɪᴇɴᴛ ᴇᴍᴀɪʟ ᴀᴅᴅʀᴇss.")
    return GET_RECIPIENT

def get_recipient(update: Update, context: CallbackContext) -> int:
    context.user_data['recipient'] = update.message.text
    update.message.reply_text("📧 Nᴇxᴛ, ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ sᴜʙᴊᴇᴄᴛ ᴏғ ʏᴏᴜʀ ᴇᴍᴀɪʟ.")
    return GET_SUBJECT

def get_subject(update: Update, context: CallbackContext) -> int:
    context.user_data['subject'] = update.message.text
    update.message.reply_text("📝 Fɪɴᴀʟʟʏ, ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʙᴏᴅʏ ᴏғ ʏᴏᴜʀ ᴇᴍᴀɪʟ.")
    return GET_BODY

def get_body(update: Update, context: CallbackContext) -> int:
    recipient = context.user_data['recipient']
    subject = context.user_data['subject']
    body = update.message.text

    global email_counter
    if email_counter >= MAX_EMAILS_PER_DAY:
        update.message.reply_text(f"⚠️ Maximum daily limit of {MAX_EMAILS_PER_DAY} emails reached. Please try again tomorrow.")
        return ConversationHandler.END

    # Start a new thread for sending the email
    threading.Thread(target=send_email, args=(recipient, subject, body)).start()
    
    update.message.reply_text(f"✅ Email to {recipient} with subject '{subject}' has been queued for sending.")
    return ConversationHandler.END

def main() -> None:
    setup_database()

    # Initialize the Updater and pass it your bot's token.
    updater = Updater("6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4")

    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(CommandHandler("send", send))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('send', send)],
        states={
            GET_RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, get_recipient)],
            GET_SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            GET_BODY: [MessageHandler(Filters.text & ~Filters.command, get_body)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
