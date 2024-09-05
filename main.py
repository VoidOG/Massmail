import smtplib
import ssl
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler
from datetime import datetime, timedelta

# Email credentials and configuration
senders = [
    {"sender_email": "imvoid1001@gmail.com", "password": "mjmkalzfveddvkmr"},
    {"sender_email": "massacres1001@gmail.com", "password": "vjkfmjnsiiajkbzh"}
]

# Constants
MAX_EMAILS_PER_SENDER = 80
TELEGRAM_BOT_TOKEN = "7440411032:AAH7OU28kZNyID37DZsXWeKFGSJxba6yOjU"  # Replace with your bot token
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Authorized users (only user IDs)
authorized_users = [6663845789, 6698364560, 1110013191, 6551446148]

# States for conversation handler
RECIPIENT_TYPE, RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(6)

# Initialize global variables to track email statistics
email_stats = {sender['sender_email']: 0 for sender in senders}  # Emails sent today
weekly_email_stats = {sender['sender_email']: 0 for sender in senders}  # Emails sent this week
overall_email_stats = {sender['sender_email']: 0 for sender in senders}  # Total emails sent

# Function to track email statistics
def track_email_stats(sender_email):
    email_stats[sender_email] += 1
    weekly_email_stats[sender_email] += 1
    overall_email_stats[sender_email] += 1

# Start command
def start(update: Update, context: CallbackContext):
    """Sends a welcome message with buttons linking to the developer and channel."""
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        welcome_message = (
            f"👾 **Welcome to Mass Mail Bot** 👾\n\n"
            "🚀 The ultimate tool for sending mass emails securely and efficiently.\n"
            "💼 Developed by Cenzo (@Cenzeo) for smooth operations.\n\n"
            "🔥 Click below to connect with the Developer and stay updated on our Channel!"
        )
        keyboard = [
            [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Cenzeo")],
            [InlineKeyboardButton("📢 Channel", url="https://t.me/themassacres")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_photo(
            "https://telegra.ph/file/0b4853eb7a9d860f3e73b.jpg",
            caption=welcome_message,
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text("⚠️ You are not authorized to use this bot. Contact the developer for access.")

# Help command
def help_command(update: Update, context: CallbackContext):
    """Displays help information about the bot's usage."""
    help_message = (
        "📚 **Help Menu** 📚\n\n"
        "Welcome to the Mass Mail Bot! Here's a guide on how to use the bot:\n\n"
        "1. **/start** - Start the bot and receive a welcome message with links to the Developer and our Channel.\n\n"
        "2. **/help** - Displays this help message with detailed instructions on how to use the bot.\n\n"
        "3. **Initiates the email sending process. You will be guided through:**\n"
        "   - Choosing whether to send to a single or multiple recipients.\n"
        "   - Providing the recipient's email address(es).\n"
        "   - Entering the subject and body of the email.\n"
        "   - Specifying the number of emails to send and the time delay between them.\n\n"
        "4. **/cancel** - Use this command at any time to cancel the current operation.\n\n"
        "⚠️ **Important Notes:**\n"
        "- Ensure you follow the instructions step-by-step to successfully send emails.\n"
        "- Stay within the email limits to avoid issues.\n"
        "- Contact the bot administrator for any issues or further assistance.\n\n"
        "If you need more help or encounter any issues, feel free to reach out to the Developer."
    )
    update.message.reply_text(help_message)

# Stats command
def stats_command(update: Update, context: CallbackContext):
    """Prompt the user to enter the passcode to view stats."""
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        keyboard = [
            [InlineKeyboardButton("📅 Today", callback_data='stats_today')],
            [InlineKeyboardButton("📆 Weekly", callback_data='stats_weekly')],
            [InlineKeyboardButton("📊 Overall", callback_data='stats_overall')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('📊 Select the stats timeframe:', reply_markup=reply_markup)
    else:
        update.message.reply_text("⚠️ You are not authorized to access this command.")

def show_stats(update: Update, context: CallbackContext):
    """Display the selected stats based on user input."""
    query = update.callback_query
    query.answer()  # Acknowledge the callback

    if query.data == 'stats_today':
        stats_message = generate_stats_message(email_stats, "📅 Today's Email Stats")
    elif query.data == 'stats_weekly':
        stats_message = generate_stats_message(weekly_email_stats, "📆 Weekly Email Stats")
    elif query.data == 'stats_overall':
        stats_message = generate_stats_message(overall_email_stats, "📊 Overall Email Stats")
    
    query.edit_message_text(stats_message)

def generate_stats_message(stats, title):
    """Generates a stats message for the given stats dictionary."""
    total_possible_emails = MAX_EMAILS_PER_SENDER * len(senders)
    total_sent = sum(stats.values())
    remaining_emails = total_possible_emails - total_sent

    stats_message = (
        f"{title}\n\n"
        f"📬 **Total Emails Allowed:** {total_possible_emails}\n"
        f"📤 **Total Emails Sent:** {total_sent}\n"
        f"📝 **Remaining Emails:** {remaining_emails}\n\n"
        "🕵️‍♂️ **User Activity:**\n"
    )

    for sender, count in stats.items():
        stats_message += f"🧑‍💼 Sender: {sender}, 📧 Emails Sent: {count}\n"

    return stats_message

# Handling email sending flow
def select_recipient_type(update: Update, context: CallbackContext):
    """Ask the user if they want to send to a single or multiple recipients."""
    keyboard = [
        [InlineKeyboardButton("Single Recipient", callback_data='single')],
        [InlineKeyboardButton("Multiple Recipients", callback_data='multiple')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Would you like to send to a single recipient or multiple recipients?", reply_markup=reply_markup)
    return RECIPIENT_TYPE

def get_recipient(update: Update, context: CallbackContext):
    """Get the recipient(s) address(es)."""
    query = update.callback_query
    context.user_data['recipient_type'] = query.data
    query.edit_message_text("Please send the recipient email address(es).")
    return RECIPIENT

def get_subject(update: Update, context: CallbackContext):
    """Get the email subject."""
    context.user_data['recipients'] = update.message.text.strip()
    update.message.reply_text("Please send the email subject.")
    return SUBJECT

def get_body(update: Update, context: CallbackContext):
    """Get the email body."""
    context.user_data['subject'] = update.message.text.strip()
    update.message.reply_text("Please send the email body.")
    return BODY

def get_number_of_emails(update: Update, context: CallbackContext):
    """Get the number of emails to send."""
    context.user_data['body'] = update.message.text.strip()
    update.message.reply_text("How many emails would you like to send?")
    return NUMBER_OF_EMAILS

def get_time_delay(update: Update, context: CallbackContext):
    """Get the time delay between sending emails."""
    try:
        context.user_data['number_of_emails'] = int(update.message.text.strip())
        update.message.reply_text("Please enter the time delay between sending emails (in seconds).")
        return TIME_DELAY
    except ValueError:
        update.message.reply_text("Invalid number of emails. Please try again.")
        return NUMBER_OF_EMAILS

def send_emails(update: Update, context: CallbackContext):
    """Send the emails as per user input."""
    try:
        time_delay = int(update.message.text.strip())
        number_of_emails = context.user_data['number_of_emails']
        subject = context.user_data['subject']
        body = context.user_data['body']
        recipients = context.user_data['recipients'].split(',') if context.user_data['recipient_type'] == 'multiple' else [context.user_data['recipients']]

        if len(recipients) == 0:
            update.message.reply_text("No recipients provided. Operation cancelled.")
            return ConversationHandler.END
        
        if number_of_emails > MAX_EMAILS_PER_SENDER:
            update.message.reply_text(f"Cannot send more than {MAX_EMAILS_PER_SENDER} emails per session. Operation cancelled.")
            return ConversationHandler.END

        sender_index = 0
        emails_sent = 0
        
        for recipient in recipients:
            if emails_sent >= number_of_emails:
                break
            
            sender = senders[sender_index]
            try:
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context()) as server:
                    server.login(sender['sender_email'], sender['password'])
                    message = f"Subject: {subject}\n\n{body}"
                    server.sendmail(sender['sender_email'], recipient.strip(), message)
                    track_email_stats(sender['sender_email'])
                    
                    update.message.reply_text(f"📧 Email sent to {recipient.strip()}!")
                    emails_sent += 1
                    time.sleep(time_delay)  # Wait before sending the next email

                    # Move to the next sender if current sender reaches limit
                    if email_stats[sender['sender_email']] >= MAX_EMAILS_PER_SENDER:
                        sender_index = (sender_index + 1) % len(senders)
                        email_stats[senders[sender_index]['sender_email']] = 0  # Reset count for next sender

                update.message.reply_text(f"👾 All emails sent successfully!")
            except Exception as e:
                update.message.reply_text(f"❌ Failed to send email to {recipient.strip()}. Error: {e}")
    
    except ValueError:
        update.message.reply_text("❌ Invalid time delay. Please try again.")
    
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    """Handle the cancellation of the conversation."""
    update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

def main():
    """Start the bot and set up handlers."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('stats', stats_command))

    # Callback query handler for stats
    dp.add_handler(CallbackQueryHandler(show_stats, pattern='^stats_'))

    # Conversation handler for email sending
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('sendemail', select_recipient_type)],
        states={
            RECIPIENT_TYPE: [CallbackQueryHandler(get_recipient)],
            RECIPIENT: [MessageHandler(Filters.text & ~Filters.command, get_subject)],
            SUBJECT: [MessageHandler(Filters.text & ~Filters.command, get_body)],
            BODY: [MessageHandler(Filters.text & ~Filters.command, get_number_of_emails)],
            NUMBER_OF_EMAILS: [MessageHandler(Filters.text & ~Filters.command, get_time_delay)],
            TIME_DELAY: [MessageHandler(Filters.text & ~Filters.command, send_emails)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    # Error handler
    dp.add_error_handler(lambda update, context: print(f"Update {update} caused error {context.error}"))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
