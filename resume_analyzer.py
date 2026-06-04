import re
from pypdf import PdfReader


KNOWN_SKILLS = [
    "python", "java", "javascript", "html", "css", "sql",
    "machine learning", "deep learning", "data analysis",
    "statistics", "react", "django", "fastapi", "flask",
    "aws", "docker", "linux", "git", "github",
    "cybersecurity", "networking", "tensorflow", "pandas",
    "numpy", "scikit-learn", "power bi", "excel",
    "communication", "leadership", "teamwork",
    "problem solving", "project management",
    "autocad", "matlab", "solidworks",
    "accounting", "finance", "marketing",
    "research", "content writing"
]

DEGREE_KEYWORDS = [
    "bs computer science", "bachelor of computer science",
    "bs information technology", "bachelor of information technology",
    "bs software engineering", "bachelor of software engineering",
    "bs data science", "bachelor of data science",
    "bs artificial intelligence", "bachelor of artificial intelligence",
    "bba", "bachelor of business administration",
    "mba", "master of business administration",
    "bs accounting", "bs finance", "bachelor of commerce", "b.com",
    "mbbs", "doctor of medicine", "pharm d", "pharmacy",
    "bs nursing", "dpt", "doctor of physical therapy",
    "bs electrical engineering", "bs mechanical engineering",
    "bs civil engineering", "bs industrial engineering",
    "bachelor of engineering",
    "ba english", "bs english", "bs psychology",
    "bs education", "b.ed", "m.ed"
]

EXPERIENCE_KEYWORDS = [
    "internship", "intern", "experience", "worked as",
    "freelance", "freelancer", "project", "projects",
    "volunteer", "assistant", "trainee", "developed",
    "created", "built", "managed", "designed"
]


def extract_text_from_pdf(file_path: str):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text.lower()


def clean_text(text: str):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills_from_text(text: str):
    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill.title())

    return list(dict.fromkeys(found_skills))


def extract_education_from_text(text: str):
    found_degrees = []

    for degree in DEGREE_KEYWORDS:
        pattern = r"\b" + re.escape(degree) + r"\b"
        if re.search(pattern, text):
            found_degrees.append(degree.title())

    if found_degrees:
        return list(dict.fromkeys(found_degrees))

    education_patterns = [
        r"\b(?:bs|bsc|b\.sc|bachelor|masters|ms|msc|m\.sc|mba|bba|mbbs|pharm d|dpt)\b.{0,80}",
        r"\b(?:computer science|information technology|software engineering|data science|engineering|finance|accounting|medical|pharmacy|nursing)\b.{0,80}"
    ]

    matches = []

    for pattern in education_patterns:
        results = re.findall(pattern, text)
        for result in results:
            matches.append(result.strip().title())

    return list(dict.fromkeys(matches))[:5]


def extract_experience_from_text(text: str):
    experience_lines = []
    sentences = re.split(r"[.\n]", text)

    for sentence in sentences:
        sentence = sentence.strip()

        if any(keyword in sentence for keyword in EXPERIENCE_KEYWORDS):
            if 20 <= len(sentence) <= 250:
                experience_lines.append(sentence.title())

    return list(dict.fromkeys(experience_lines))[:8]


def analyze_resume(file_path: str):
    text = extract_text_from_pdf(file_path)
    text = clean_text(text)

    skills = extract_skills_from_text(text)
    education = extract_education_from_text(text)
    experience = extract_experience_from_text(text)

    return {
        "extracted_skills": skills,
        "education": education,
        "experience": experience,
        "total_skills_found": len(skills)
    }