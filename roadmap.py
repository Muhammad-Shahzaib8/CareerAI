def generate_roadmap(career, missing_skills):

    roadmap = []

    month = 1

    for skill in missing_skills:

        roadmap.append({
            "month": month,
            "focus_skill": skill,
            "goal": f"Learn {skill}"
        })

        month += 1

    roadmap.append({
        "month": month,
        "focus_skill": "Projects",
        "goal": f"Build portfolio projects for {career}"
    })

    roadmap.append({
        "month": month + 1,
        "focus_skill": "Interview Preparation",
        "goal": "Prepare for internships and jobs"
    })

    return roadmap