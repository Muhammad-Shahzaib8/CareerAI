from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("Gemini_API_Key")
)

def generate_ai_roadmap(
    country,
    degree,
    career,
    current_skills,
    missing_skills
):

    prompt = f"""
You are an expert AI Career Advisor.

Country: {country}
Degree: {degree}
Target Career: {career}

Current Skills:
{current_skills}

Missing Skills:
{missing_skills}

Create a detailed 12-month roadmap.

Include:
- Monthly learning plan
- Certifications
- Projects
- GitHub tasks
- LinkedIn tasks
- Internship strategy
- Job strategy
- Freelancing strategy

Make it practical and professional.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text