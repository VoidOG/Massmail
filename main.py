import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '7440411032:AAH7OU28kZNyID37DZsXWeKFGSJxba6yOjU'

# Define authorized users and their passwords
authorized_users = {
    6663845789: '911',      # User ID 1 with Password 1
    6551446148: '911',      # User ID 2 with Password 2
    6698364560: '6969',     # User ID 3 with Password 3
    1110013191: '9999'      # Updated User ID 4 with Password 4
}

# List of sender email configurations (Gmail SMTP server details, email, and password)
senders = [
    {
        "smtp_server": "smtp.gmail.com",  # Gmail SMTP server
        "port": 465,  # SSL port for Gmail
        "sender_email": "imvoid1001@gmail.com",
        "sender_password": "mjmkalzfveddvkmr"
    },
    {
        "smtp_server": "smtp.gmail.com",
        "port": 465,
        "sender_email": "massacres1001@gmail.com",
        "sender_password": "vjkfmjnsiiajkbzh"
    }
]

# Maximum emails allowed per session
MAX_EMAILS_PER_SESSION = 50

# Define stages for the conversation handler
PASSWORD, RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(6)

def send_email(recipient, sender_email, sender_password, smtp_server, port, subject, body):
    """Function to send an email using specified sender credentials."""
    try:
        # Set up the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP SSL session and send the email
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        return True  # Return True if the email is sent successfully

    except Exception as e:
        print(f'Failed to send email from {sender_email} to {recipient}: {e}')
        return False  # Return False if the email fails to send

def start(update: Update, context: CallbackContext):
    """Start the conversation and send a welcome message with a button."""
    keyboard = [
        [InlineKeyboardButton("Developer", url="https://t.me/Cenzeo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "🚀 **Welcome to Mass Mail** 🚀\n\n"
        "The ultimate bulk email tool designed for those who think big. "
        "Here, you wield the power to send emails at scale with precision and control.\n\n"
        "Created by the OG, Cenzo, for those who refuse to settle.\n\n"
        "⚙️ Let’s get to work, soldier. Time to make an impact. ⚙️"
    )

    update.message.reply_text(welcome_message, reply_markup=reply_markup)
    return PASSWORD

def check_password(update: Update, context: CallbackContext):
    """Check if the entered password is correct."""
    user_id = update.message.from_user.id
    entered_password = update.message.text.strip()  # Strip any whitespace from input

    # Debug: Print the user ID and entered password for troubleshooting
    print(f"Debug: User ID: {user_id}, Entered Password: {entered_password}")

    # Check if the user ID and password match an entry in authorized_users
    if authorized_users.get(user_id) == entered_password:
        context.user_data['authenticated'] = True
        update.message.reply_text('🔒 Authentication successful! You’re in, soldier. 🔓\nNow drop that recipient email address and let’s get this mission rolling.')
        return RECIPIENT
    else:
        # If the user ID is found but the password doesn't match, inform about incorrect password
        if user_id in authorized_users:
            update.message.reply_text('🚫 Incorrect password. Try again or hit /cancel to back out.')
        else:
            # If the user ID itself is not recognized, inform the user
            update.message.reply_text('⛔ Access denied. You’re not authorized to use this bot.')
        
        return PASSWORD

def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    context.user_data['recipient'] = update.message.text
    update.message.reply_text('📧 Got it. Now, hit me with the subject of the email.')
    return SUBJECT

def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    context.user_data['subject'] = update.message.text
    update.message.reply_text('📝 Subject locked and loaded. Now, drop the body of the email.')
    return BODY

def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    context.user_data['body'] = update.message.text
    update.message.reply_text('✍️ Body received. How many emails are we firing off today? (Max 50)')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    try:
        number_of_emails = int(update.message.text)
        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'⚠️ You’ve requested {number_of_emails} emails. The max cap is {MAX_EMAILS_PER_SESSION}. Setting to 50.')
            number_of_emails = MAX_EMAILS_PER_SESSION
        
        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('📊 Number of emails locked in. Now, set the time delay (in seconds) between each email.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('❌ Invalid number. Let’s try that again, champ.')
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

        # Send the specified number of emails with a time delay
        count = 0
        for _ in range(number_of_emails):
            # Randomly select a sender from the list
            sender = random.choice(senders)
            if send_email(
                recipient=recipient,
                sender_email=sender['sender_email'],
                sender_password=sender['sender_password'],
                smtp_server=sender['smtp_server'],
                port=sender['port'],
                subject=subject,
                body=body
            ):
                count += 1
                update.message.reply_text(f"✅ {count} email{'s' if count > 1 else ''} sent. Keep going, we’re just getting started.")

            time.sleep(time_delay)

        update.message.reply_text("🎯 Mission accomplished. All emails have been sent. Good work.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('❌ Invalid time delay. Try again, soldier.')
        return TIME_DELAY

def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    update.message.reply_text('❌ Operation aborted. Until next time.')
    return ConversationHandler.END

def main():
    """Start the bot and handle commands."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define the conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, check_password)],
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, get_recipient)],
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            BODY: [MessageHandler(Filters.text & ~Filters.command, get_body)],
            NUMBER_OF_EMAILS: [MessageHandler(Filters.text & ~Filters.command, get_number_of_emails)],
            TIME_DELAY: [MessageHandler(Filters.text & ~Filters.command, get_time_delay)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
