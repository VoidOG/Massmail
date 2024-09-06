import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4'

# Define authorized users by their User IDs
authorized_users = [6663845789, 6551446148, 6698364560, 1110013191]

# Define sender emails and passwords
senders = [
    {"email": "imvoid1001@gmail.com", "password": "mjmkalzfveddvkmr"},
    {"email": "massacres1001@gmail.com", "password": "vjkfmjnsiiajkbzh"},
    {"email": "usaa45600@gmail.com", "password": "bwgdiqehvemfitjx"},
    {"email": "lolwhosucks@gmail.com", "password": "rssrsfmnpmzjtcxl"},
    {"email": "", "password": "urpcznlkyazksbsr"}
]

# SMTP server details
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Maximum emails allowed per session and per day
MAX_EMAILS_PER_SESSION = 50
MAX_EMAILS_PER_DAY = 500

# Email counters to track daily usage
email_counters = {}

# Define stages for the conversation handler
RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(5)


def send_email(recipient, sender_email, sender_password, subject, body):
    """Function to send an email using specified sender credentials."""
    try:
        # Set up the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP SSL session and send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True  # Return True if the email is sent successfully

    except Exception as e:
        print(f'Failed to send email from {sender_email} to {recipient}: {e}')
        return False  # Return False if the email fails to send


def start(update: Update, context: CallbackContext):
    """Start the conversation and send a welcome message with buttons and an image."""
    # Keyboard buttons with links
    keyboard = [
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Cenzeo"),
         InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome image
    image_url = "https://telegra.ph/file/0b4853eb7a9d860f3e73b.jpg"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

    # Welcome message with OG vibe
    welcome_message = (
        "**👾 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴍᴀss ᴍᴀɪʟ 👾 **\n\n"
        "ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ʙᴜʟᴋ ᴇᴍᴀɪʟ ᴛᴏᴏʟ ᴅᴇsɪɢɴᴇᴅ ғᴏʀ ᴛʜᴏsᴇ ᴡʜᴏ ᴛʜɪɴᴋ ʙɪɢ. "
        "ʜᴇʀᴇ, ʏᴏᴜ ᴡɪᴇʟᴅ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴛᴏ sᴇɴᴅ ᴇᴍᴀɪʟs ᴀᴛ sᴄᴀʟᴇ ᴡɪᴛʜ ᴘʀᴇᴄɪsɪᴏɴ ᴀɴᴅ ᴄᴏɴᴛʀᴏʟ.\n\n"
        "ᴄʀᴇᴀᴛᴇᴅ ʙʏ ᴛʜᴇ ᴄᴇɴᴢᴏ, ғᴏʀ ᴛʜᴏsᴇ ᴡʜᴏ ʀᴇғᴜsᴇ ᴛᴏ sᴇᴛᴛʟᴇ.\n\n"
        "⚙️ ʟᴇᴛ’s ɢᴇᴛ ᴛᴏ ᴡᴏʀᴋ, sᴏʟᴅɪᴇʀ. ᴛɪᴍᴇ ᴛᴏ ᴍᴀᴋᴇ ᴀɴ ɪᴍᴘᴀᴄᴛ. ⚙️"
    )

    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return RECIPIENT


def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    context.user_data['recipient'] = update.message.text
    update.message.reply_text('📧 ɢᴏᴛ ɪᴛ. ɴᴏᴡ, ʜɪᴛ ᴍᴇ ᴡɪᴛʜ ᴛʜᴇ sᴜʙᴊᴇᴄᴛ ᴏғ ᴛʜᴇ ᴇᴍᴀɪʟ.')
    return SUBJECT


def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    context.user_data['subject'] = update.message.text
    update.message.reply_text('📝 sᴜʙᴊᴇᴄᴛ ʟᴏᴄᴋᴇᴅ ᴀɴᴅ ʟᴏᴀᴅᴇᴅ. ɴᴏᴡ, ᴅʀᴏᴘ ᴛʜᴇ ʙᴏᴅʏ ᴏғ ᴛʜᴇ ᴇᴍᴀɪʟ.')
    return BODY


def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    context.user_data['body'] = update.message.text
    update.message.reply_text(f'✍️ ʙᴏᴅʏ ʀᴇᴄᴇɪᴠᴇᴅ. ʜᴏᴡ ᴍᴀɴʏ ᴇᴍᴀɪʟs ᴀʀᴇ ᴡᴇ ғɪʀɪɴɢ ᴏғғ ᴛᴏᴅᴀʏ? (ᴍᴀx {MAX_EMAILS_PER_SESSION})')
    return NUMBER_OF_EMAILS


def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    try:
        user_id = update.message.from_user.id
        number_of_emails = int(update.message.text)

        # Check the user's daily limit
        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text(f'⚠️ ᴅᴀɪʟʏ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ. ʏᴏᴜ ᴄᴀɴ sᴇɴᴅ ᴜᴘ ᴛᴏ {remaining} ᴍᴏʀᴇ ᴇᴍᴀɪʟs ᴛᴏᴅᴀʏ.')
            number_of_emails = remaining

        # Check the session limit
        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'⚠️ ʏᴏᴜ’ve ʀᴇǫᴜᴇsᴛᴇᴅ {number_of_emails} ᴇᴍᴀɪʟs. ᴛʜᴇ ᴍᴀx ᴄᴀᴘ ᴘᴇʀ sᴇssɪᴏɴ ɪs {MAX_EMAILS_PER_SESSION}. sᴇᴛᴛɪɴɢ ᴛᴏ 50.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('📊 ɴᴜᴍʙᴇʀ ᴏғ ᴇᴍᴀɪʟs ʟᴏᴄᴋᴇᴅ ɪɴ. ɴᴏᴡ, sᴇᴛ ᴛʜᴇ ᴛɪᴍᴇ ᴅᴇʟᴀʏ (ɪɴ sᴇᴄᴏɴᴅs) ʙᴇᴛᴡᴇᴇɴ ᴇᴀᴄʜ ᴇᴍᴀɪʟ.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ʟᴇᴛ’s ᴛʀʏ ᴛʜᴀᴛ ᴀɢᴀɪɴ, ᴄʜᴀᴍᴘ.')
        return NUMBER_OF_EMAILS


def get_time_delay(update: Update, context: CallbackContext):
    """Store the time delay and start sending the emails."""
    try:
        context.user_data['time_delay'] = float(update.message.text)
        recipient = context.user_data['recipient']
        subject = context.user_data['subject']
        body = context.user_data['body']
        number_of_emails = context.user_data['number_of_emails']
        time_delay = context.user_data['time_delay']
        user_id = update.message.from_user.id

        # Initialize the user's email count if not already set
        email_counters.setdefault(user_id, 0)

        count = 0
        for _ in range(number_of_emails):
            # Randomly select a sender from the list
            sender = random.choice(senders)
            if send_email(
                recipient=recipient,
                sender_email=sender['email'],
                sender_password=sender['password'],
                subject=subject,
                body=body
            ):
                count += 1
                email_counters[user_id] += 1

                # Check if the daily limit has been reached
                if email_counters[user_id] >= MAX_EMAILS_PER_DAY:
                    update.message.reply_text("⛔ ᴅᴀɪʟʏ ᴇᴍᴀɪʟ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ. ᴄᴏɴsɪᴅᴇʀ ʀᴇsᴜᴍɪɴɢ ᴛᴏᴍᴏʀʀᴏᴡ.")
                    break

                update.message.reply_text(f"✅ {count} ᴇᴍᴀɪʟ{'s' ɪғ count > 1 ᴇʟsᴇ ''} sᴇɴᴛ. ᴋᴇᴇᴘ ɢᴏɪɴɢ, ᴡᴇ’ʀᴇ ᴊᴜsᴛ ɢᴇᴛᴛɪɴɢ sᴛᴀʀᴛᴇᴅ.")

            time.sleep(time_delay)

        update.message.reply_text("🎯 ᴍɪssɪᴏɴ ᴀᴄᴄᴏᴍᴘʟɪsʜᴇᴅ. ᴀʟʟ ᴇᴍᴀɪʟs ʜᴀᴠᴇ ʙᴇᴇɴ sᴇɴᴛ. ɢᴏᴏᴅ ᴡᴏʀᴋ.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('❌ ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ᴅᴇʟᴀʏ. ᴛʀʏ ᴀɢᴀɪɴ, sᴏʟᴅɪᴇʀ.')
        return TIME_DELAY


def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    update.message.reply_text('❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ. ᴜɴᴛɪʟ ɴᴇxᴛ ᴛɪᴍᴇ.')
    return ConversationHandler.END


def main():
    """Start the bot and handle commands."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, get_recipient)],
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            BODY: [MessageHandler(Filters.text & ~Filters.command, get_body)],
            NUMBER_OF_EMAILS: [MessageHandler(Filters.text & ~Filters.command, get_number_of_emails)],
            TIME_DELAY: [MessageHandler(Filters.text & ~Filters.command, get_time_delay)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add conversation handler to dispatcher
    dispatcher.add_handler(conversation_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
