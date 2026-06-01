from recommendation import recommend_careers


def recommend_from_resume(country, degree, extracted_skills):

    skills_string = ",".join(extracted_skills)

    recommendations = recommend_careers(
        country,
        degree,
        skills_string
    )

    return recommendations