from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.parse
from dotenv import load_dotenv
import os

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Обработка сообщений с номером и текстом
def handle_message(update, context):
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

# Команда /start
def start(update, context):
    update.message.reply_text("Привет! Отправь мне номер телефона (и по желанию сообщение), и я сделаю ссылку WhatsApp.")

# Запуск бота
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
