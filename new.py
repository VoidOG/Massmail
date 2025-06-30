from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
import smtplib
import ssl
import asyncio
from email.message import EmailMessage
import socks
import socket

# === SOCKS5 Proxy Setup ===
socks.set_default_proxy(socks.SOCKS5, "192.252.210.233", 4145)
socket.socket = socks.socksocket

EMAIL, SUBJECT, BODY, COUNT, DELAY = range(5)

ADMIN_USERS = [6663845789]
LOG_GROUP_ID = -1002854086015

# Use your Gmail addresses and actual App Passwords
GMAIL_ACCOUNTS = [
    {"email": "massacres1001@gmail.com", "app_password": "nibhswtstoftyogk"},
    {"email": "sugarplum9911@gmail.com", "app_password": "tkwheocuqqbogzfc"},
]

def is_admin(user_id: int):
    return user_id in ADMIN_USERS

async def start_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You are not authorized to use this bot.")
        return ConversationHandler.END
    await update.message.reply_text("📧 Enter recipient email address:")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["recipient"] = update.message.text
    await update.message.reply_text("✉️ Enter email subject:")
    return SUBJECT

async def get_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["subject"] = update.message.text
    await update.message.reply_text("📝 Enter email body:")
    return BODY

async def get_body(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["body"] = update.message.text
    await update.message.reply_text("🔁 How many times to send the email?")
    return COUNT

async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["count"] = int(update.message.text)
        await update.message.reply_text("⏱️ Time delay (in seconds) between each email?")
        return DELAY
    except:
        await update.message.reply_text("❗ Please enter a valid number.")
        return COUNT

async def get_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["delay"] = int(update.message.text)
    except:
        await update.message.reply_text("❗ Please enter a valid number.")
        return DELAY

    recipient = context.user_data["recipient"]
    subject = context.user_data["subject"]
    body = context.user_data["body"]
    count = context.user_data["count"]
    delay = context.user_data["delay"]

    await update.message.reply_text(f"📨 Starting to send {count} emails to {recipient}...")

    success = 0

    for i in range(count):
        account = GMAIL_ACCOUNTS[i % len(GMAIL_ACCOUNTS)]
        msg = EmailMessage()
        msg["From"] = account["email"]
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            context_ssl = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context_ssl)
                server.login(account["email"], account["app_password"])
                server.send_message(msg)
            success += 1
            await update.message.reply_text(f"✅ Email {i+1}/{count} sent from {account['email']}")
        except Exception as e:
            await update.message.reply_text(f"❌ Email {i+1}/{count} failed — {e}")
            await context.bot.send_message(LOG_GROUP_ID, f"❌ Failed to send email {i+1}: {e}")

        await asyncio.sleep(delay)

    await update.message.reply_text(f"📬 Mailing complete.\n\n✅ Sent: {success}/{count}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Mailing cancelled.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token("6795292888:AAHTxIAjbpJxXZrlBv_6C_F3LhsTSyOQqGA").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("mail", start_mail)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subject)],
            BODY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_body)],
            COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
            DELAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_delay)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    app.run_polling()
