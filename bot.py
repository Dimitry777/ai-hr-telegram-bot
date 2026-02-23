import logging
import os
from email_sender import send_email
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from ai_analyzer import analyze_candidate

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

questions = [
    "Ваше полное имя (ФИО)",
    "Сколько у вас лет опыта в управлении проектами?",
    "Сколько у вас лет опыта в IT?",
    "У вас есть опыт управления AI или ML командами?",
    "У вас есть завершенные AI-продукты о которых выможете рассказать?",
    "Работали ли вы по методологии Agile?"
]

user_answers = {}
current_question = {}


@dp.message(CommandStart())
async def start_handler(message: Message):
    user_answers[message.from_user.id] = []
    current_question[message.from_user.id] = 0

    await message.answer(
        "Добро пожаловать в чат с AI PM HR Assistant. Пожалуйста, ответьте на несколько вопросов перед отправкой резюме."
    )

    await message.answer(questions[0])


@dp.message(F.text)
async def handle_answers(message: Message):
    user_id = message.from_user.id

    if user_id not in user_answers:
        return

    user_answers[user_id].append(message.text)
    current_question[user_id] += 1

    if current_question[user_id] < len(questions):
        await message.answer(questions[current_question[user_id]])
    else:
        await message.answer("Спасибо! Теперь отправьте ваше резюме в формате PDF.")


@dp.message(F.document)
async def handle_pdf(message: Message):
    user_id = message.from_user.id

    if user_id not in user_answers:
        await message.answer("Сначала ответьте на вопросы с помощью команды /start.")
        return

    document = message.document

    if document.mime_type != "application/pdf":
        await message.answer("Пожалуйста, отправьте резюме в формате PDF.")
        return

    await message.answer("Получил ваше резюме. Анализирую...")

    file = await bot.get_file(document.file_id)
    file_path = file.file_path

    downloaded_file = await bot.download_file(file_path)

    local_pdf_path = f"resume_{user_id}.pdf"

    with open(local_pdf_path, "wb") as f:
        f.write(downloaded_file.read())

    answers = "\n".join(user_answers[user_id])

    result = analyze_candidate(local_pdf_path, answers)

    await message.answer(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))