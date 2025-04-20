import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import urllib.parse

# Загружаем переменные окружения из .env файла
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Функция для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(maxsplit=1)

    if not parts:
        await update.message.reply_text("Отправь номер телефона.")
        return

    digits = ''.join(filter(str.isdigit, parts[0]))

    if digits.startswith('7') and len(digits) == 11:
        if len(parts) > 1:
            message_text = urllib.parse.quote(parts[1])
            link = f"https://wa.me/{digits}?text={message_text}"
        else:
            link = f"https://wa.me/{digits}"

        await update.message.reply_text(f"Ссылка на WhatsApp:\n{link}")
    else:
        await update.message.reply_text("Пожалуйста, отправь номер в формате +7 700 123 4567 или просто цифрами.")

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне номер телефона (и по желанию сообщение), и я сделаю ссылку WhatsApp.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
