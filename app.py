from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # Храним токен в .env

# Функция для обработки сообщений
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    parts = text.split(maxsplit=1)
    if not parts:
        update.message.reply_text("Отправь номер телефона.")
        return

    digits = ''.join(filter(str.isdigit, parts[0]))

    if digits.startswith('7') and len(digits) == 11:
        if len(parts) > 1:
            message_text = urllib.parse.quote(parts[1])
            link = f"https://wa.me/{digits}?text={message_text}"
        else:
            link = f"https://wa.me/{digits}"

        update.message.reply_text(f"Ссылка на WhatsApp:\n{link}")
    else:
        update.message.reply_text("Пожалуйста, отправь номер в формате +7 700 123 4567 или просто цифрами.")

# Стартовая команда
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Отправь мне номер телефона (и по желанию сообщение), и я сделаю ссылку WhatsApp.")

# Основная функция
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
