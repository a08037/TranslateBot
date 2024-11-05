import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile, ContentType
from aiogram.filters import Command
from gtts import gTTS
from deep_translator import GoogleTranslator

API_TOKEN = '8061783060:AAGC9tkI3BFMmBKVYBxqeKwu_PurgOZmJ2I'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Убедитесь, что папка img существует
if not os.path.exists('img'):
    os.makedirs('img')

# Обработчик для команды /start
async def start_handler(message: types.Message):
    await message.answer("Hello!")

# Обработчик для сохранения всех отправленных пользователем фото
async def handle_photo(message: types.Message):
    # Выбираем фото наибольшего размера
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = f"img/{photo.file_id}.jpg"

    # Скачиваем файл
    await bot.download_file(file_info.file_path, destination=file_path)
    await message.reply("Фото сохранено!")


# Команда для отправки голосового сообщения
async def send_voice_message(message: types.Message):
    tts = gTTS("Привет! Это тестовое аудиосообщение.", lang='ru')
    tts.save("sample.mp3")
    audio = FSInputFile("sample.mp3")
    await message.answer_audio(audio)
    os.remove("sample.mp3")

# Обработчик для перевода текста на английский язык
async def translate_text(message: types.Message):
    translated = GoogleTranslator(source='auto', target='en').translate(message.text)
    await message.reply(f"Перевод: {translated}")


async def main():
    # Регистрируем обработчики
    dp.message.register(start_handler, Command("start"))
    dp.message.register(handle_photo, F.content_type == ContentType.PHOTO)
    dp.message.register(send_voice_message, Command("voice"))
    dp.message.register(translate_text, F.content_type == ContentType.TEXT)

    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
