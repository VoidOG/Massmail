import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

BOT_TOKEN = "6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4"
authorized_users = [6663845789, 6551446148, 6698364560, 1110013191]
owner_id = 6663845789

senders = [
    {"email": "imvoid1001@gmail.com", "password": "mjmkalzfveddvkmr"},
    {"email": "massacres1001@gmail.com", "password": "vjkfmjnsiiajkbzh"},
    {"email": "usaa45600@gmail.com", "password": "bwgdiqehvemfitjx"},
    {"email": "lolwhosucks@gmail.com", "password": "rssrsfmnpmzjtcxl"},
    {"email": "Yourmomsucksmine69@gmail.com", "password": "urpcznlkyazksbsr"},
    {"email": "unknowntikku@gmail.com", "password": "dffiufucyixcfzfq"},
    {"email": "unknownsultan123@gmail.com", "password": "wetqhcxcvbtmmavc"},
    {"email": "bhaisalmon6969@gmail.com", "password": "ducrkxtufoqemdbt"}
]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

MAX_EMAILS_PER_SESSION = 50
MAX_EMAILS_PER_DAY = 800

email_counters = {}
user_list = set()

RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY, BROADCAST_MESSAGE = range(6)

def reset_daily_counters():
    """Function to reset the daily email counters."""
    global email_counters
    email_counters.clear()

def send_email(recipient, sender_email, sender_password, subject, body):
    """Function to send an email using specified sender credentials."""
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True

    except Exception as e:
        print(f'𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗌𝖾𝗇𝖽 𝖾𝗆𝖺𝗂𝗅 𝖿𝗋𝗈𝗆 {sender_email} 𝗍𝗈 {recipient}: {e}')
        return False

def start(update: Update, context: CallbackContext):
    """Start the conversation and send a welcome message with buttons and an image."""
    user_id = update.message.from_user.id
    user_list.add(user_id)  

    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @Cenzeo)
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/Alcyonebots"),
         InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/Alcyone_Support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = ""
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

    welcome_message = (
        "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗠𝗮𝘀𝘀 𝗠𝗮𝗶𝗹 𝖻𝗈𝗍 𝖻𝗒 𝗔𝗹𝗰𝘆𝗼𝗻𝗲\n\n"
        "𝖳𝗁𝖾 𝗎𝗅𝗍𝗂𝗆𝖺𝗍𝖾 𝖻𝗎𝗅𝗄 𝖾𝗆𝖺𝗂𝗅 𝗍𝗈𝗈𝗅 𝖽𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋 𝗍𝗁𝗈𝗌𝖾 𝗐𝗁𝗈 𝗍𝗁𝗂𝗇𝗄 𝖻𝗂𝗀.\n"
        "𝖣𝗋𝗈𝗉 𝗒𝗈𝗎𝗋 𝗋𝖾𝖼𝗂𝗉𝗂𝖾𝗇𝗍'𝗌 𝖾𝗆𝖺𝗂𝗅 𝖨𝖣 𝖺𝗇𝖽 𝗐𝖺𝗍𝖼𝗁 𝗂𝗍 𝖻𝗈𝗆𝖻𝖾𝖽!"
        "𝖳𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝗍𝗁𝖾 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗌𝖾𝗇𝖽 /cancel 𝗍𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝗌𝖾𝗇𝖽 /start 𝖿𝗈𝗋 𝗇𝖾𝗐 𝗌𝖾𝗌𝗌𝗂𝗈𝗇"
    )

    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return RECIPIENT

def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @Cenzeo")
        return ConversationHandler.END

    context.user_data['recipient'] = update.message.text
    update.message.reply_text("𝖦𝗈𝗍 𝗂𝗍. 𝖭𝗈𝗐, 𝗁𝗂𝗍 𝗆𝖾 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝗌𝗎𝖻𝗃𝖾𝖼𝗍 𝗈𝖿 𝗍𝗁𝖾 𝖾𝗆𝖺𝗂𝗅.")
    return SUBJECT

def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @𝖢𝖾𝗇𝗓𝖾𝗈")
        return ConversationHandler.END

    context.user_data['subject'] = update.message.text
    update.message.reply_text("𝖲𝗎𝖻𝗃𝖾𝖼𝗍 𝗅𝗈𝖼𝗄𝖾𝖽. 𝖭𝗈𝗐, 𝖽𝗋𝗈𝗉 𝗍𝗁𝖾 𝖻𝗈𝖽𝗒 𝗈𝖿 𝗍𝗁𝖾 𝖾𝗆𝖺𝗂𝗅.")
    return BODY

def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @𝖢𝖾𝗇𝗓𝖾𝗈")
        return ConversationHandler.END

    context.user_data['body'] = update.message.text
    update.message.reply_text(f'𝖡𝗈𝖽𝗒 𝗋𝖾𝖼𝖾𝗂𝗏𝖾𝖽. 𝖧𝗈𝗐 𝗆𝖺𝗇𝗒 𝖾𝗆𝖺𝗂𝗅𝗌 𝖺𝗋𝖾 𝗐𝖾 𝖿𝗂𝗋𝗂𝗇𝗀 𝗈𝖿𝖿 𝗍𝗈𝖽𝖺𝗒? (Max {MAX_EMAILS_PER_SESSION})')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @𝖢𝖾𝗇𝗓𝖾𝗈")
        return ConversationHandler.END

    try:
        number_of_emails = int(update.message.text)

        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text(f"𝖣𝖺𝗂𝗅𝗒 𝗅𝗂𝗆𝗂𝗍 𝗋𝖾𝖺𝖼𝗁𝖾𝖽. 𝖸𝗈𝗎 𝖼𝖺𝗇 𝗌𝖾𝗇𝖽 𝗎𝗉 𝗍𝗈 {remaining} 𝗆𝗈𝗋𝖾 𝖾𝗆𝖺𝗂𝗅𝗌 𝗍𝗈𝖽𝖺𝗒.")
            number_of_emails = remaining

        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f"𝖬𝖺𝗑 𝖼𝖺𝗉 𝗂𝗌 {MAX_EMAILS_PER_SESSION} 𝖾𝗆𝖺𝗂𝗅𝗌. 𝖲𝖾𝗍𝗍𝗂𝗇𝗀 𝗍𝗈 {MAX_EMAILS_PER_SESSION}.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text("𝖭𝗎𝗆𝖻𝖾𝗋 𝗈𝖿 𝖾𝗆𝖺𝗂𝗅𝗌 𝗅𝗈𝖼𝗄𝖾𝖽. 𝖭𝗈𝗐, 𝗌𝖾𝗍 𝗍𝗁𝖾 𝗍𝗂𝗆𝖾 𝖽𝖾𝗅𝖺𝗒 (𝗂𝗇 𝗌𝖾𝖼𝗈𝗇𝖽𝗌) 𝖻𝖾𝗍𝗐𝖾𝖾𝗇 𝖾𝖺𝖼𝗁 𝖾𝗆𝖺𝗂𝗅.")
        return TIME_DELAY
    except ValueError:
        update.message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗇𝗎𝗆𝖻𝖾𝗋. 𝖳𝗋𝗒 𝖺𝗀𝖺𝗂𝗇.")
        return NUMBER_OF_EMAILS

def get_time_delay(update: Update, context: CallbackContext):
    """Store the time delay and start sending the emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 150 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @𝖢𝖾𝗇𝗓𝖾𝗈")
        return ConversationHandler.END

    try:
        context.user_data['time_delay'] = float(update.message.text)
        recipient = context.user_data['recipient']
        subject = context.user_data['subject']
        body = context.user_data['body']
        number_of_emails = context.user_data['number_of_emails']
        time_delay = context.user_data['time_delay']

        email_counters.setdefault(user_id, 0)

        count = 0
        for _ in range(number_of_emails):
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

                if email_counters[user_id] >= MAX_EMAILS_PER_DAY:
                    update.message.reply_text("𝖡𝗈𝗍'𝗌 𝖣𝖺𝗂𝗅𝗒 𝖾𝗆𝖺𝗂𝗅 𝗅𝗂𝗆𝗂𝗍 𝗋𝖾𝖺𝖼𝗁𝖾𝖽. 𝖳𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗍𝗈𝗆𝗈𝗋𝗋𝗈𝗐.")
                    break

                update.message.reply_text(f"✅ {count} 𝖾𝗆𝖺𝗂𝗅 {'s' if count > 1 else ''} 𝗌𝖾𝗇𝗍. 𝖶𝖺𝗂𝗍𝗂𝗇𝗀 𝖿𝗈𝗋 {time_delay} 𝗌𝖾𝖼𝗈𝗇𝖽𝗌.")
                time.sleep(time_delay)

        update.message.reply_text(f"{count} email {'s' if count > 1 else ''} 𝗌𝖾𝗇𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!")
        return ConversationHandler.END

    except ValueError:
        update.message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖣𝖾𝗅𝖺𝗒, 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇")
        return TIME_DELAY

def broadcast(update: Update, context: CallbackContext):
    """Broadcast a message to all users who interacted with the bot."""
    user_id = update.message.from_user.id

    if user_id != owner_id:
        update.message.reply_text("𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return

    update.message.reply_text("𝖲𝖾𝗇𝖽 𝗍𝗁𝖾 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍")
    return BROADCAST_MESSAGE

def handle_broadcast_message(update: Update, context: CallbackContext):
    """Send the broadcast message to all users."""
    message = update.message.text
    success_count = 0

    for user_id in user_list:
        try:
            context.bot.send_message(chat_id=user_id, text=message)
            success_count += 1
        except Exception as e:
            print(f"𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗌𝖾𝗇𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝗎𝗌𝖾𝗋 {user_id}: {e}")

    update.message.reply_text(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗌𝖾𝗇𝗍 𝗍𝗈 {success_count} 𝗎𝗌𝖾𝗋𝗌")

def cancel(update: Update, context: CallbackContext):
    """Cancel the current operation."""
    update.message.reply_text("𝖮𝗉𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽. 𝖸𝗈𝗎 𝖼𝖺𝗇 𝗌𝗍𝖺𝗋𝗍 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅𝗂𝗇𝗀 𝖺𝗀𝖺𝗂𝗇 𝖻𝗒 𝗌𝖾𝗇𝖽𝗂𝗇𝗀 /start")
    return ConversationHandler.END

def main():
    """Start the bot and set up handlers."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, get_recipient)],
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            BODY: [MessageHandler(Filters.text & ~Filters.command, get_body)],
            NUMBER_OF_EMAILS: [MessageHandler(Filters.text & ~Filters.command, get_number_of_emails)],
            TIME_DELAY: [MessageHandler(Filters.text & ~Filters.command, get_time_delay)],
            BROADCAST_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, handle_broadcast_message)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler('broadcast', broadcast))

    updater.job_queue.run_daily(lambda context: reset_daily_counters(), time=time(0, 0, 0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
