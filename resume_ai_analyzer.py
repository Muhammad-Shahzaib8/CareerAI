import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def analyze_resume_with_ai(country, education, experience, extracted_skills):
    skills_text = ", ".join(extracted_skills)
    education_text = ", ".join(education) if education else "Not clearly found in resume"
    experience_text = ", ".join(experience) if experience else "No clear experience found"

    prompt = f"""
You are CareerAI, a professional AI career advisor for a real public career platform.

Country:
{country}

Education detected from resume:
{education_text}

Experience or projects detected from resume:
{experience_text}

Skills detected from resume:
{skills_text}

Analyze this resume professionally.

Important rules:
Do not use markdown.
Do not use # symbols.
Do not use asterisks.
Use clean professional English.
Suggest realistic entry-level and junior-level jobs first.
Mention higher designation growth paths separately.
Do not assume only one career path.

Provide these sections:

1. Resume Profile Summary
2. Detected Education
3. Detected Skills
4. Detected Experience Or Projects
5. Best Realistic Job Suggestions
6. Job Chances In The Given Country
7. Future Scope For The Next 3 To 5 Years
8. Missing Skills To Become More Employable
9. Skills Needed For Promotion Or Higher Designation
10. Recommended Certifications
11. Recommended Projects
12. Suggested 3-Month Action Plan
13. Final Career Recommendation

Be practical, realistic, and market-focused.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("Resume AI Analysis Error:", e)
        return "AI resume career analysis is temporarily unavailable. Please try again later."