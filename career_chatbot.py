import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def get_career_chatbot_response(user_email: str, message: str):

    prompt = f"""
You are CareerAI, a professional AI career advisor.

User Email: {user_email}

Student Question:
{message}

Give a practical, detailed, and student-friendly answer.

Focus on:
- Career roadmap
- Skills
- Projects
- Certifications
- Internships
- GitHub
- LinkedIn
- Freelancing
- Remote jobs

Do not give generic advice.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini Error:", e)

        return "CareerAI AI service is temporarily unavailable. Please try again later."
