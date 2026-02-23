import os
from openai import OpenAI
from PyPDF2 import PdfReader


# Используем DeepSeek вместо OpenAI
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

if not os.getenv("DEEPSEEK_API_KEY"):
    raise ValueError("DEEPSEEK_API_KEY is missing!")


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def analyze_candidate(pdf_path, answers):

    resume_text = extract_text_from_pdf(pdf_path)

    prompt = f"""
Ты HR-ассистент, оценивающий кандидата на позицию AI Project Manager.

Ответь строго структурированно:

1. Оценка (число от 0 до 100)
2. Сильные стороны (списком)
3. Слабые стороны (списком)
4. Рекомендация по найму (кратко)

Ответ только на русском языке.

Анкета кандидата:
{answers}

Резюме:
{resume_text}
"""

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Ты профессиональный HR-рекрутер."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content