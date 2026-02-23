import os
from openai import OpenAI
from PyPDF2 import PdfReader

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing!")

client = OpenAI(api_key=api_key)


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def analyze_candidate(pdf_path, answers):

    resume_text = extract_text_from_pdf(pdf_path)

    prompt = f"""
Ты HR-ассистент, оценивающий кандидата на позицию AI Project Manager.

Candidate answers:
{answers}

Resume:
{resume_text}

Ответь на русском языке и предоставь:

1. Оценку от 0 до 100
2. Сильные стороны кандидата
3. Слабые стороны
4. Рекомендацию по найму
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional HR recruiter."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content