import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_roadmap(
    country,
    degree,
    career,
    current_skills,
    missing_skills
):
    prompt = f"""
You are a professional AI Career Advisor.

Country: {country}
Degree: {degree}
Target Career: {career}
Current Skills: {current_skills}
Missing Skills: {missing_skills}

Generate a detailed 12-month roadmap.
Include monthly learning plan, certifications, projects, GitHub tasks,
LinkedIn tasks, internship strategy, job strategy, and freelancing strategy.

IMPORTANT:
- Do NOT use Markdown.
- Do NOT use #, ##, ### headings.
- Do NOT use **bold** formatting.
- Do NOT use bullet symbols like *, -, •.
- Use proper English.
- Use numbered sections instead.
- Format the roadmap for a professional web application.
- Write clear paragraphs.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text