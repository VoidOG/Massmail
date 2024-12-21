import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
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
            "```𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝗉𝖾𝗋𝗆𝗂𝗍𝗍𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍!!\n"
            "𝖯𝗎𝗒 𝗆𝖾𝗆𝖻𝗾𝗅....<<you can insert the next text here for full length>>```",
            parse_mode="MarkdownV2"
        )
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Cenzeo"),
         InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    image_url = "https://i.ibb.co/bg228Qh/file-250.jpg"
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
    update.message.reply_text('📧 ɢᴏᴛ ɪᴛ. ɴᴏᴡ, ʜɪᴛ ᴍᴇ ᴡɪᴛʜ ᴛʜᴇ sᴜʙᴊᴇᴄᴛ ᴏғ ᴛʜᴇ ᴇᴍᴀɪʟ.')
    return SUBJECT


def get_subject(update: Update, context: CallbackContext):
    """Store the subject and ask for the body."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    context.user_data['subject'] = update.message.text
    update.message.reply_text('📝 sᴜʙᴊᴇᴄᴛ ʟᴏᴄᴋᴇᴅ ᴀɴᴅ ʟᴏᴀᴅᴇᴅ. ɴᴏᴡ, ᴅʀᴏᴘ ᴛʜᴇ ʙᴏᴅʏ ᴏғ ᴛʜᴇ ᴇᴍᴀɪʟ.')
    return BODY


def get_body(update: Update, context: CallbackContext):
    """Store the body and ask for the number of emails."""
    user_id = update.message.from_user.id
    if user_id not in authorized_users:
        update.message.reply_text('❌ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀ.')
        return ConversationHandler.END

    context.user_data['body'] = update.message.text
    update.message.reply_text(f'✍️ ʙᴏᴅʏ ʀᴇᴄᴇɪᴠᴇᴅ. ʜᴏᴡ ᴍᴀɴʏ ᴇᴍᴀɪʟs ᴀʀᴇ ᴡᴇ ғɪʀɪɴɢ ᴏғғ ᴛᴏᴅᴀʏ? (ᴍᴀx {MAX_EMAILS_PER_SESSION})')
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
            update.message.reply_text(f'⚠️ ᴅᴀɪʟʏ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ. ʏᴏᴜ ᴄᴀɴ sᴇɴᴅ ᴜᴘ ᴛᴏ {remaining} ᴍᴏʀᴇ ᴇᴍᴀɪʟs ᴛᴏᴅᴀʏ.')
            number_of_emails = remaining

        if number_of_emails > MAX_EMAILS_PER_SESSION:
            update.message.reply_text(f'⚠️ ʏᴏᴜ’ve ʀᴇǫᴜᴇsᴛᴇᴅ {number_of_emails} ᴇᴍᴀɪʟs. ᴛʜᴇ ᴍᴀx ᴄᴀᴘ ᴘᴇʀ sᴇssɪᴏɴ ɪs {MAX_EMAILS_PER_SESSION}. sᴇᴛᴛɪɴɪɴɢ ᴛᴏ 50.')
            number_of_emails = MAX_EMAILS_PER_SESSION

        context.user_data['number_of_emails'] = number_of_emails
        update.message.reply_text('📊 ɴᴜᴍʙᴇʀ ᴏғ ᴇᴍᴀɪʟs ʟᴏᴄᴋᴇᴅ ɪɴ. ɴᴏᴡ, sᴇᴛ ᴛʜᴇ ᴛɪᴍᴇ ᴅᴇʟᴀʏ (ɪɴ sᴇᴄᴏɴᴅs) ʙᴇᴛᴡᴇᴇɴ ᴇᴀᴄʜ ᴇᴍᴀɪʟ.')
        return TIME_DELAY
    except ValueError:
        update.message.reply_text('❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ. ʟᴇᴛ’s ᴛʀʏ ᴛʜᴀᴛ ᴀɢᴀɪɴ, ᴄʜᴀᴍᴘ.')
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

        update.message.reply_text("🎯 ᴍɪssɪᴏɴ ᴀᴄᴄᴏᴍᴘʟɪsʜᴇᴅ. ᴀʟʟ ᴇᴍᴀɪʟs ʜᴀᴠᴇ ʙᴇᴇɴ sᴇɴᴛ. ɢᴏᴏᴅ ᴡᴏʀᴋ.")
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

    update.message.reply_text('❌ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴀʙᴏʀᴛᴇᴅ. ᴜɴᴛɪʟ ɴᴇxᴛ ᴛɪᴍᴇ.')
    return ConversationHandler.END


def buy(update: Update, context: CallbackContext):
    """Send a message with text and two inline buttons using MarkdownV2 formatting."""
    keyboard = [
        [InlineKeyboardButton("Contact Developer", url="https://t.me/Cenzeo"),
         InlineKeyboardButton("Join Channel", url="https://t.me/themassacres")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # MarkdownV2 formatted text
    message = (
        "```"
        "To access the premium features of the bot, you need to buy a membership. "
        "💡  Here's how you can proceed:\n\n"
        "1. Contact the developer for payment details\n"
        "2. Join our channel for updates\n\n"
        "💰 Membership starts at 250 INR for 1 month! 💰"
        "```"
    )

    update.message.reply_text(message, reply_markup=reply_markup, parse_mode="MarkdownV2")


def main():
    """Start the bot and handle commands."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

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
    
    buy_handler = CommandHandler('buy', buy)
    dispatcher.add_handler(buy_handler)

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
