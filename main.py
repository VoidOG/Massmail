# © Cenzo @Cenzeo
# meet me on telegram 
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
TELEGRAM_BOT_TOKEN = "6795292888:AAGPvq5pOqoGIHXUpLrRv2EKytK_0gAIli4"  # Replace with your bot token
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Authorized users with passwords
authorized_users = {
    6663845789: "911",
    6698364560: "6969",
    1110013191: "1111",
    6551446148: "911"
}

# States for conversation handler
PASSWORD, RECIPIENT_TYPE, RECIPIENT, SUBJECT, BODY, NUMBER_OF_EMAILS, TIME_DELAY = range(7)

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
        "💬 Use the following commands to navigate the bot:\n\n"
        "/start - Start the bot and display the welcome message\n"
        "/help - Display this help message\n"
        "/stats - View global email sending statistics (requires passcode)\n\n"
        "⚙️ To use this bot, you will be guided step-by-step through sending emails.\n"
        "Stay within the email limits and enjoy safe mass mailing!"
    )
    update.message.reply_text(help_message)

# Password check for /stats command
def stats_command(update: Update, context: CallbackContext):
    """Prompt the user to enter the passcode to view stats."""
    user_id = update.message.from_user.id
    if user_id in authorized_users:
        update.message.reply_text('🔑 Enter the passcode to access global email stats.')
        context.user_data['awaiting_stats_password'] = True
        return PASSWORD
    else:
        update.message.reply_text("⚠️ You are not authorized to access this command.")
        return ConversationHandler.END

def display_stats(update: Update, context: CallbackContext):
    """Displays the stats after verifying the passcode."""
    user_id = update.message.from_user.id
    entered_password = update.message.text.strip()
    if user_id in authorized_users and entered_password == authorized_users[user_id]:
        # Create inline keyboard with options to view stats for Today, Weekly, and Overall
        keyboard = [
            [InlineKeyboardButton("📅 Today", callback_data='stats_today')],
            [InlineKeyboardButton("📆 Weekly", callback_data='stats_weekly')],
            [InlineKeyboardButton("📊 Overall", callback_data='stats_overall')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('📊 Select the stats timeframe:', reply_markup=reply_markup)
    else:
        update.message.reply_text('🚫 Incorrect passcode. Access denied.')
    return ConversationHandler.END

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

# Define other command handlers (get_recipient, get_subject, get_body, etc.)
# These would guide the user through entering the details of their email

def main():
    """Main function to set up the bot handlers and start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define the conversation handler for sending emails
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, display_stats)],
            RECIPIENT_TYPE: [CallbackQueryHandler(select_recipient_type)],
            # Define other states to handle email sending inputs
        },
        fallbacks=[CommandHandler('cancel', lambda update, context: update.message.reply_text('Operation cancelled.'))],
    )

    # Add command handlers
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('stats', stats_command))
    dispatcher.add_handler(CallbackQueryHandler(show_stats, pattern='^stats_'))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
