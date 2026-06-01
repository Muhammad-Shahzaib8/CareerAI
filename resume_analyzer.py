from pypdf import PdfReader


KNOWN_SKILLS = [
    "python", "java", "javascript", "html", "css", "sql",
    "machine learning", "deep learning", "data analysis",
    "statistics", "react", "django", "fastapi", "flask",
    "aws", "docker", "linux", "git", "github",
    "cybersecurity", "networking", "tensorflow", "pandas",
    "numpy", "scikit-learn", "power bi", "excel"
]


def extract_text_from_pdf(file_path: str):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text.lower()


def extract_skills_from_text(text: str):
    found_skills = []

    for skill in KNOWN_SKILLS:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills


def analyze_resume(file_path: str):
    text = extract_text_from_pdf(file_path)
    skills = extract_skills_from_text(text)

    return {
        "extracted_skills": skills,
        "total_skills_found": len(skills)
    }