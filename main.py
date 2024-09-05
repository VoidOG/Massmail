import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '7440411032:AAH7OU28kZNyID37DZsXWeKFGSJxba6yOjU'

# Define authorized users and their passwords
authorized_users = {
    6663845789: '911',   # User ID 1 with Password 1
    6551446148: '911',   # User ID 2 with Password 2
    6698364560: '6969',  # User ID 3 with Password 3
    6698364560: '1111'   # User ID 4 with Password 4
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
    """Start the conversation and send a welcome message."""
    update.message.reply_text(
        "Welcome to the Bulk Email Sender Bot!\n\n"
        "I'm here to help you send bulk emails easily and efficiently.\n"
        "Developed by Cenzo (@Cenzeo), this bot allows you to send emails using multiple sender accounts.\n"
        "To get started, please enter your password."
    )
    return PASSWORD

def check_password(update: Update, context: CallbackContext):
    """Check if the entered password is correct."""
    user_id = update.message.from_user.id
    entered_password = update.message.text

    if authorized_users.get(user_id) == entered_password:
        context.user_data['authenticated'] = True
        update.message.reply_text('Authentication successful! Please provide the recipient email address.')
        return RECIPIENT
    else:
        update.message.reply_text('Incorrect password. Please try again or /cancel to stop.')
        return PASSWORD

def get_recipient(update: Update, context: CallbackContext):
    """Store the recipient email and ask for the subject."""
    context.user_data['recipient'] = update.message.text
    update.message.reply_text('Got it. Now, please provide the subject of the email.')
    return SUBJECT

def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    context.user_data['subject'] = update.message.text
    update.message.reply_text('Subject noted. Now, please provide the body of the email.')
    return BODY

def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    context.user_data['body'] = update.message.text
    update.message.reply_text('Body received. How many emails would you like to send? (Max 50)')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    try:
        number_of_emails = int(update.message.text)
        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'You have requested {number_of_emails} emails. The maximum allowed per session is {MAX_EMAILS_PER_SESSION}. Setting to 50.')
            number_of_emails = MAX_EMAILS_PER_SESSION
        
        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('Number of emails noted. Please provide the time delay (in seconds) between each email.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('Invalid number of emails. Please provide a valid number.')
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
                update.message.reply_text(f"{count} email{'s' if count > 1 else ''} sent")

            time.sleep(time_delay)

        update.message.reply_text("All emails have been sent.")
        return ConversationHandler.END
    except ValueError:
        update.message.reply_text('Invalid time delay. Please provide a valid number.')
        return TIME_DELAY

def cancel(update: Update, context: CallbackContext):
    """Cancel the conversation."""
    update.message.reply_text('Conversation canceled.')
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
