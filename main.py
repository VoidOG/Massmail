import logging
import threading
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
MAX_EMAILS_PER_DAY = 80
email_counter = 0
email_senders = {
    "imvoid1001@gmail.com": "mjmkalzfveddvkmr",
    "massacres1001@gmail.com": "vjkfmjnsiiajkbzh"
}
user_stats = {}

# Define states for ConversationHandler
CHOOSING, TYPING_REPLY = range(2)

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

                logger.info(f"Email sent successfully from {email}")
                break
            except Exception as e:
                logger.error(f"Error sending email from {email}: {e}")
    except Exception as e:
        logger.error(f"Error in sending email: {e}")

# Command handlers
def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Developer", url="https://t.me/Cenzeo")],
        [InlineKeyboardButton("Channel", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "👾 Welcome to Mass Mail Bot! 🚀\n\n"
        "Choose to use a single or multiple recipients. Use /send to start sending emails.\n"
        "For more info, use /help.\n\n"
        "Developer: [Cenzo](https://t.me/Cenzeo)"
    )

    update.message.reply_photo(photo="https://telegra.ph/file/0b4853eb7a9d860f3e73b.jpg", caption=welcome_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    return CHOOSING

def help_command(update: Update, context: CallbackContext) -> None:
    help_message = (
        "🛠️ **Help Menu**\n\n"
        "1. **/start** - Start the bot and get a welcome message.\n"
        "2. **/send** - Begin sending emails. The bot will guide you through the process.\n"
        "3. **/cancel** - Cancel the current operation.\n"
        "4. **/stats** - View global email sending statistics (requires passcode).\n\n"
        "For more information or assistance, contact the developer."
    )
    update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def send_email_handler(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Single Recipient", callback_data='single')],
        [InlineKeyboardButton("Multiple Recipients", callback_data='multiple')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose email sending mode:', reply_markup=reply_markup)
    return CHOOSING

def handle_choice(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    if query.data == 'single':
        query.edit_message_text(text="You have selected Single Recipient. Please enter the recipient email.")
        return TYPING_REPLY
    elif query.data == 'multiple':
        query.edit_message_text(text="You have selected Multiple Recipients. Please upload a CSV file with recipient emails.")
        return TYPING_REPLY

def receive_recipient_email(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user.id
    recipient = update.message.text
    context.user_data['recipient'] = recipient
    update.message.reply_text("Enter the subject of the email:")
    return TYPING_REPLY

def receive_subject(update: Update, context: CallbackContext) -> int:
    context.user_data['subject'] = update.message.text
    update.message.reply_text("Enter the body of the email:")
    return TYPING_REPLY

def receive_body(update: Update, context: CallbackContext) -> int:
    recipient = context.user_data.get('recipient')
    subject = context.user_data.get('subject')
    body = update.message.text

    update.message.reply_text('Sending email...')
    threading.Thread(target=send_email, args=(recipient, subject, body)).start()

    global email_counter
    email_counter += 1
    if email_counter >= MAX_EMAILS_PER_DAY:
        update.message.reply_text('Daily email limit reached.')

    update.message.reply_text('Email sent successfully.')
    return ConversationHandler.END

def stats(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_stats:
        today_stats, weekly_stats, overall_stats = user_stats[user_id]
        update.message.reply_text(
            f"📊 **Email Stats**\n\n"
            f"**Today's Emails:** {today_stats}\n"
            f"**This Week's Emails:** {weekly_stats}\n"
            f"**Overall Emails:** {overall_stats}\n"
        )
    else:
        update.message.reply_text('No stats available for this user.')

def main() -> None:
    # Initialize the bot with your token
    updater = Updater("6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define the ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('send', send_email_handler)],
        states={
            CHOOSING: [CallbackQueryHandler(handle_choice)],
            TYPING_REPLY: [
                MessageHandler(Filters.text & ~Filters.command, receive_recipient_email),
                MessageHandler(Filters.text & ~Filters.command, receive_subject),
                MessageHandler(Filters.text & ~Filters.command, receive_body)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('stats', stats))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
