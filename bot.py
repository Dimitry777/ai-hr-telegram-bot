import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from pdf_parser import extract_text_from_pdf
from ai_analyzer import analyze_candidate

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_answers = {}

questions = [
    "Ваше полное имя (ФИО)",
    "Какой у вас опыт управления проектами (в годах) ?",
    "Какой у вас опыт управления AI или ML командами (в годах)?",
    "У вас есть завершенные AI-продукты о которых выможете рассказать?",
    "Опишите ваш опыт с Agile"
]

@dp.message(Command("start"))
async def start(message: Message):
    user_answers[message.from_user.id] = []
    await message.answer("Добро пожаловать в чат с AI PM HR Assistant")
    await message.answer(questions[0])

@dp.message(F.document)
async def handle_messages(message: Message):

    document = message.document

    if document.mime_type != "application/pdf":
        await message.answer("Пожалуйста, отправьте резюме в формате PDF.")
        return

    file_id = document.file_id

    file = await bot.get_file(file_id)
    file_path = file.file_path

    downloaded_file = await bot.download_file(file_path)

    local_pdf_path = f"resume_{message.from_user.id}.pdf"

    with open(local_pdf_path, "wb") as f:
        f.write(downloaded_file.read())

    answers = "\n".join(user_answers[message.from_user.id])

    result = analyze_candidate(local_pdf_path, answers)

    await message.answer(result)

    else:

        user_answers[user_id].append(message.text)

        if len(user_answers[user_id]) < len(questions):
            await message.answer(questions[len(user_answers[user_id])])
        else:
            await message.answer("Загрузите ваше резюме в формате PDF")

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))