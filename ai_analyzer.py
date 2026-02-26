from PyPDF2 import PdfReader

# AI PM skill keywords
AI_PM_SKILLS = {
    "python": 8,
    "machine learning": 10,
    "deep learning": 10,
    "nlp": 9,
    "data science": 8,
    "ai": 6,
    "llm": 9,
    "openai": 6,
    "tensorflow": 7,
    "pytorch": 7,
    "project management": 8,
    "scrum": 6,
    "agile": 6,
    "jira": 5,
    "product management": 7,
    "stakeholder": 6,
    "sql": 5,
    "api": 5,
    "docker": 4,
    "cloud": 5
}


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.lower()
    return text


def score_candidate(text):

    score = 0
    found_skills = []

    for skill, weight in AI_PM_SKILLS.items():
        if skill in text:
            score += weight
            found_skills.append(skill)

    if score > 100:
        score = 100

    return score, found_skills


def analyze_candidate(pdf_path, answers):

    resume_text = extract_text_from_pdf(pdf_path)
    combined_text = (resume_text + answers).lower()

    score, skills = score_candidate(combined_text)

    if score >= 75:
        recommendation = "Рекомендуется к найму"
    elif score >= 50:
        recommendation = "Рассмотреть после интервью"
    else:
        recommendation = "Не рекомендуется"

    strengths = ", ".join(skills[:5]) if skills else "Недостаточно релевантных AI навыков"

    missing_skills = [
        skill for skill in AI_PM_SKILLS.keys()
        if skill not in skills
    ]

    weaknesses = ", ".join(missing_skills[:5]) if missing_skills else "Нет явных слабых сторон"

    result = f"""
📊 Оценка кандидата: {score}/100

💪 Сильные стороны:
{strengths}

⚠️ Слабые стороны:
{weaknesses}

🧾 Рекомендация:
{recommendation}
"""

    return result