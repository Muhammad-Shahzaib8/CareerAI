from career_data import career_dataset


def clean_skills(skills_text: str):
    return [skill.strip().lower() for skill in skills_text.split(",")]


def calculate_match(student_country, student_degree, student_skills, career):
    score = 0

    if career["country"].lower() == student_country.lower():
        score += 25

    if career["degree"].lower() == student_degree.lower():
        score += 25

    user_skills = set(clean_skills(student_skills))
    required_skills = set(skill.lower() for skill in career["required_skills"])

    matched_skills = user_skills.intersection(required_skills)
    missing_skills = required_skills - user_skills

    skill_score = (len(matched_skills) / len(required_skills)) * 30
    score += skill_score

    score += career["growth_score"] * 0.1
    score += career["salary_score"] * 0.1

    return {
        "career": career["career"],
        "match_score": round(score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "growth_score": career["growth_score"],
        "salary_score": career["salary_score"]
    }


def recommend_careers(student_country, student_degree, student_skills):
    results = []

    for career in career_dataset:
        result = calculate_match(
            student_country,
            student_degree,
            student_skills,
            career
        )
        results.append(result)

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    return results[:3]