import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

BOT_TOKEN = 
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
        print(f'Failed to send email from {sender_email} to {recipient}: {e}')
        return False

def start(update: Update, context: CallbackContext):
    """Start the conversation and send a welcome message with buttons and an image."""
    user_id = update.message.from_user.id
    user_list.add(user_id)  # Add the user to the user_list if they interact with the bot

    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("Developer", url="https://t.me/Cenzeo"),
         InlineKeyboardButton("Channel", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://telegra.ph/file/0b4853eb7a9d860f3e73b.jpg"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

    welcome_message = (
        "👾 Welcome to Mass Mail 👾\n\n"
        "The ultimate bulk email tool designed for those who think big.\n\n"
        "Drop your recipient's email ID and watch it bombed!"
    )

    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return RECIPIENT

def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['recipient'] = update.message.text
    update.message.reply_text('📧 Got it. Now, hit me with the subject of the email.')
    return SUBJECT

def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['subject'] = update.message.text
    update.message.reply_text('📝 Subject locked. Now, drop the body of the email.')
    return BODY

def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    context.user_data['body'] = update.message.text
    update.message.reply_text(f'✍️ Body received. How many emails are we firing off today? (Max {MAX_EMAILS_PER_SESSION})')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
        return ConversationHandler.END

    try:
        number_of_emails = int(update.message.text)

        remaining = MAX_EMAILS_PER_DAY - email_counters.get(user_id, 0)
        if number_of_emails > remaining:
            update.message.reply_text(f'⚠️ Daily limit reached. You can send up to {remaining} more emails today.')
            number_of_emails = remaining

        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'⚠️ Max cap is {MAX_EMAILS_PER_SESSION} emails. Setting to {MAX_EMAILS_PER_SESSION}.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('📊 Number of emails locked. Now, set the time delay (in seconds) between each email.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('❌ Invalid number. Try again.')
        return NUMBER_OF_EMAILS

def get_time_delay(update: Update, context: CallbackContext):
    """Store the time delay and start sending the emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ Unauthorized user.')
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
                    update.message.reply_text("⛔ Daily email limit reached. Try again tomorrow.")
                    break

                update.message.reply_text(f"✅ {count} email{'s' if count > 1 else ''} sent. Waiting for {time_delay} seconds.")
                time.sleep(time_delay)

        update.message.reply_text(f"📤 {count} email{'s' if count > 1 else ''} sent successfully!")
        return ConversationHandler.END

    except ValueError:
        update.message.reply_text('❌ Invalid delay. Try again.')
        return TIME_DELAY

def broadcast(update: Update, context: CallbackContext):
    """Broadcast a message to all users who interacted with the bot."""
    user_id = update.message.from_user.id

    if user_id != owner_id:
        update.message.reply_text('❌ Only the bot owner can use this command.')
        return

    update.message.reply_text('📝 Send the message you want to broadcast.')
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
            print(f"Failed to send message to user {user_id}: {e}")

    update.message.reply_text(f'📤 Broadcast sent to {success_count} users.')

def cancel(update: Update, context: CallbackContext):
    """Cancel the current operation."""
    update.message.reply_text('❌ Operation cancelled.')
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
