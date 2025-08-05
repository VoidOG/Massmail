from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, CallbackContext
import random
import os

BOT_TOKEN = '6795292888:AAFieL0kTHvKUO7XkkIxeRqBNOsRgmUpJ88'
authorized_users = [6663845789, 6551446148, 6698364560, 1110013191]

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

MAX_EMAILS_PER_SESSION = 130000
MAX_EMAILS_PER_DAY = 130000

email_counters = {}

RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(5)

# Load SMTP accounts from file (format: smtp.office365.com|587|email|password)
SMTP_FILE_PATH = "/storage/emulated/0/SMTP.txt"

def load_smtp_accounts(filename):
    accounts = []
    if not os.path.exists(filename):
        print(f"SMTP file not found: {filename}")
        return accounts
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                smtp_server, port, email, password = parts
                if smtp_server == SMTP_SERVER and int(port) == SMTP_PORT:
                    accounts.append({"email": email, "password": password})
    return accounts

senders = load_smtp_accounts(SMTP_FILE_PATH)

def send_email(recipient, sender_email, sender_password, subject, body):
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f'Failed to send email from {sender_email} to {recipient}: {e}')
        return False


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text(
            "𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗽𝗲𝗿𝗺𝗶𝘁𝘁𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁\n≡ 𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾.\n⩉ 𝖳𝗈 𝗏𝗂𝖾𝗐 𝗉𝗅𝖺𝗇𝗌, 𝗁𝗂𝗍 /𝖻𝗎𝗒")
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
        "≡ 𝖡𝗎𝗒 𝗈𝗎𝗋 𝖻𝗈𝗍 𝖻𝗈𝗍'𝗌 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝗍𝗈 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝗌𝖾𝖺𝗆𝗅𝖾𝗌𝗌𝗅𝗒\n"
        "⩉ 𝖳𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝗍𝗁𝖾 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗌𝖾𝗇𝖽 /cancel 𝗍𝗈 𝗍𝖾𝗋𝗆𝗂𝗇𝖺𝗍𝖾 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝗌𝖾𝗇𝖽 /start 𝖿𝗈𝗋 𝗇𝖾𝗐 𝗌𝖾𝗌𝗌𝗂𝗈𝗇\n"
        "⌕ 𝖳𝗈 𝗏𝗂𝖾𝗐 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝗉𝗅𝖺𝗇𝗌, 𝖼𝗅𝗂𝖼𝗄 /buy"
    )

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=caption, reply_markup=reply_markup)


def mail(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗽𝗲𝗿𝗺𝗶𝘁𝘁𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗁𝗂𝘀 𝗯𝗼𝘁\n≡ 𝖡𝗎𝗒 𝗆𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝗈𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗍𝗈 𝖿𝗋𝖾𝖾𝗅𝗒 𝗆𝖺𝗌𝗌 𝗆𝖺𝗂𝗅 𝖺𝗇𝗒𝗐𝗁𝖾𝗋𝖾.\n⩉ 𝖳𝗈 𝗏𝗂𝖾𝗐 𝗉𝗅𝖺𝗇𝗌, 𝗁𝗂𝗍 /𝖻𝗎𝗒.")
        return

    if not senders:
        update.message.reply_text("No SMTP accounts loaded! Contact admin.")
        return

    update.message.reply_text(
        "𝖫𝖾𝗍'𝗌 𝗌𝗍𝖺𝗋𝗍 𝗌𝖾𝗇𝖽𝗂𝗇𝗀 𝖾𝗆𝖺𝗂𝗅𝗌!\n"
        "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗍𝗁𝖾 𝗋𝖾𝖼𝗂𝗉𝗂𝖾𝗇𝗍'𝗌 𝖾𝗆𝖺𝗂𝗅 𝖺𝖽𝖽𝗋𝖾𝗌𝗌."
    )
    return RECIPIENT


def get_recipient(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['recipient'] = update.message.text
    update.message.reply_text('Now, send me the subject of the email.')
    return SUBJECT


def get_subject(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['subject'] = update.message.text
    update.message.reply_text('Now, drop the body of the email.')
    return BODY


def get_body(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['body'] = update.message.text
    update.message.reply_text(f'How many emails to send? Max {MAX_EMAILS_PER_SESSION}')
    return NUMBER_OF_EMAILS


def get_number_of_emails(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    try:
        number_of_emails = int(update.message.text)
        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text(f'⚠️ Daily limit reached.')
            number_of_emails = remaining

        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'You requested {number_of_emails} emails. Max per session is {MAX_EMAILS_PER_SESSION}. Setting to {MAX_EMAILS_PER_SESSION}.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('Now, set the time delay (in seconds) between each email.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('Invalid input, try again.')
        return NUMBER_OF_EMAILS


def get_time_delay(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("You are not permitted to use this bot.")
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
                    update.message.reply_text("Bot's Daily email limit reached. Try again tomorrow.")
                    break

                update.message.reply_text(f"✅ {count} email{'s' if count > 1 else ''} sent. Waiting for {time_delay} seconds.")

            time.sleep(time_delay)

        update.message.reply_text("🎯 Mission accomplished. All emails have been sent successfully. Good work.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Invalid delay, try again.')
        return TIME_DELAY


def cancel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    update.message.reply_text('❌ Operation aborted, until next time.')
    return ConversationHandler.END


# Remove /buy and related handlers if you want - this is your original with SMTP accounts loaded from file in place of `senders`.

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('mail', mail))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('mail', mail)],
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

    # If you want to remove buy & plan buttons, do not add those CallbackQueryHandlers

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
