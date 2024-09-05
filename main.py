import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = "7440411032:AAH7OU28kZNyID37DZsXWeKFGSJxba6yOjU"

# List of sender email configurations (SMTP server details, email, and password)
senders = [
    {
        "smtp_server": "smtp.gmail.com",  # Update with the actual SMTP server
        "port": 465,  # SSL port
        "sender_email": "massacres1001@gmail.com",
        "sender_password": "vjkfmjnsiiajkbzh"
    },
    {
        "smtp_server": "smtp.gmail.com",
        "port": 465,
        "sender_email": "imvoid1001@gmail.com",
        "sender_password": "mjmkalzfveddvkmr"
    },
    # Add more sender configurations as needed
]

# Define stages for the conversation handler
RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(5)

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
    """Start the conversation."""
    update.message.reply_text('Welcome! Let\'s start sending emails. Please provide the recipient email address.')
    return RECIPIENT

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
    update.message.reply_text('Body received. How many emails would you like to send?')
    return NUMBER_OF_EMAILS

def get_number_of_emails(update: Update, context: CallbackContext):
    """Store the number of emails and ask for the time delay."""
    try:
        context.user_data['number_of_emails'] = int(update.message.text)
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
