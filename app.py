import os
from aiogram import Bot, Dispatcher, types
from aiogram import F  # Import F for filters in aiogram v3.x
from aiogram.utils import executor
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне номер телефона (и по желанию сообщение), и я сделаю ссылку WhatsApp.")

@dp.message_handler(lambda message: message.text)
async def handle_message(message: types.Message):
    text = message.text.strip()
    parts = text.split(maxsplit=1)
    if not parts:
        await message.reply("Отправь номер телефона.")
        return

    digits = ''.join(filter(str.isdigit, parts[0]))

    if digits.startswith('7') and len(digits) == 11:
        if len(parts) > 1:
            message_text = urllib.parse.quote(parts[1])
            link = f"https://wa.me/{digits}?text={message_text}"
        else:
            link = f"https://wa.me/{digits}"

        await message.reply(f"Ссылка на WhatsApp:\n{link}")
    else:
        await message.reply("Пожалуйста, отправь номер в формате +7 700 123 4567 или просто цифрами.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
