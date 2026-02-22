from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

JOB_DESCRIPTION = """
We are hiring an AI Project Manager.

Must have:
- Experience managing ML teams
- Agile
- AI product delivery
- Stakeholder management
"""

def analyze_candidate(answers, resume_text):

    prompt = f"""
You are an HR AI assistant.

Job:
{JOB_DESCRIPTION}

Candidate Answers:
{answers}

Resume:
{resume_text}

Evaluate candidate.

Return:

Match Score (0-100)
Strengths
Risks
Recommendation
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content