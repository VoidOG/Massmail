from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import random
import os

# ------------ BOT CONFIG -------------
BOT_TOKEN = '6795292888:AAFieL0kTHvKUO7XkkIxeRqBNOsRgmUpJ88'
authorized_users = [6663845789, 6551446148, 6698364560, 1110013191]

MAX_EMAILS_PER_SESSION = 130000
MAX_EMAILS_PER_DAY = 130000

email_counters = {}

RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(5)

# ------------ SMTP CONFIG -------------
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

# ------------ LOAD SMTP ACCOUNTS FROM FILE -------------
SMTP_FILE_PATH = "/storage/emulated/0/SMTP.txt"  # Change if needed based on your storage path

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
                # Only keep if smtp_server and port match the configured ones; else skip or adjust logic
                if smtp_server == SMTP_SERVER and int(port) == SMTP_PORT:
                    accounts.append({
                        "email": email,
                        "password": password
                    })
                else:
                    # Optionally handle different server/port combos here
                    pass
    return accounts

smtp_accounts = load_smtp_accounts(SMTP_FILE_PATH)

# ------------ EMAIL SEND FUNCTION -------------
def send_email(recipient, sender_email, sender_password, subject, body):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Failed to send email from {sender_email} to {recipient}: {e}")
        return False

# ------------ TELEGRAM HANDLERS -------------
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text(
            "You are not permitted to use this bot.\nPlease contact admin.")
        return ConversationHandler.END

    update.message.reply_text(
        "Welcome to Mass Mail bot.\nSend /mail to start sending bulk emails.\nSend /cancel to abort any operation."
    )

def mail(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text("You are not permitted to use this bot.")
        return ConversationHandler.END
    if not smtp_accounts:
        update.message.reply_text("No SMTP accounts available. Contact admin!")
        return ConversationHandler.END
    update.message.reply_text("Let's start sending emails! Please provide the recipient's email address.")
    return RECIPIENT

def get_recipient(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('Unauthorized user.')
        return ConversationHandler.END
    context.user_data['recipient'] = update.message.text
    update.message.reply_text('Now, send me the subject of the email.')
    return SUBJECT

def get_subject(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('Unauthorized user.')
        return ConversationHandler.END
    context.user_data['subject'] = update.message.text
    update.message.reply_text('Now, drop the body of the email.')
    return BODY

def get_body(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('Unauthorized user.')
        return ConversationHandler.END
    context.user_data['body'] = update.message.text
    update.message.reply_text(f'How many emails to send? Max {MAX_EMAILS_PER_SESSION}')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('Unauthorized user.')
        return ConversationHandler.END
    try:
        number_of_emails = int(update.message.text)
        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text('Daily limit reached. Adjusting send count.')
            number_of_emails = remaining
        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'Max per session is {MAX_EMAILS_PER_SESSION}. Adjusting count.')
            number_of_emails = MAX_EMAILS_PER_SESSION
        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('Now, set the time delay (seconds) between emails.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('Invalid number. Try again.')
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
            account = random.choice(smtp_accounts)
            if send_email(
                recipient=recipient,
                sender_email=account['email'],
                sender_password=account['password'],
                subject=subject,
                body=body
            ):
                count += 1
                email_counters[user_id] += 1
                if email_counters[user_id] >= MAX_EMAILS_PER_DAY:
                    update.message.reply_text("Daily email limit reached, try again tomorrow.")
                    break
                update.message.reply_text(f"✅ {count} email{'s' if count > 1 else ''} sent. Waiting {time_delay} seconds.")
            time.sleep(time_delay)
        update.message.reply_text("All emails have been sent successfully.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Invalid delay. Try again.')
        return TIME_DELAY

def cancel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('Unauthorized user.')
        return ConversationHandler.END
    update.message.reply_text('Operation aborted.')
    return ConversationHandler.END

# ------------ MAIN FUNCTION -------------
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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
