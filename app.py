import asyncio
import os
import urllib.parse
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()
TOKEN = "8043279548:AAGh2xyzSkdqUwSO-6fTKvNxQ1choPdwyPg"


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет! Отправь мне <b>номер телефона</b> (и по желанию сообщение), "
        "и я сгенерирую ссылку WhatsApp 📱."
    )

# Обработка текстовых сообщений
@dp.message(F.text)
async def handle_message(message: Message):
    text = message.text.strip()
    parts = text.split(maxsplit=1)

    if not parts:
        await message.answer("❗ Пожалуйста, отправь номер телефона.")
        return

    digits = ''.join(filter(str.isdigit, parts[0]))

    if digits.startswith('7') and len(digits) == 11:
        if len(parts) > 1:
            message_text = urllib.parse.quote(parts[1])
            link = f"https://wa.me/{digits}?text={message_text}"
        else:
            link = f"https://wa.me/{digits}"

        await message.answer(f"✅ Ссылка на WhatsApp:\n{link}")
    else:
        await message.answer("⚠️ Отправь номер в формате +7 700 123 4567 или просто цифрами.")

# Главная функция запуска бота
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
