# CareerAI - AI Career Roadmap Advisor

CareerAI is an AI-powered career recommendation and roadmap generation system for students. It analyzes a student's country, degree, skills, resume, and career interests to suggest suitable career paths, missing skills, and a personalized AI-generated roadmap.

## Features

- User registration and login
- Password hashing
- JWT authentication
- Student profile management
- Career recommendation engine
- Skill gap analysis
- PDF resume upload
- Resume skill extraction
- AI-powered roadmap generation using Gemini API
- Country and degree-based career guidance

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- JWT Authentication
- Google Gemini API
- PyPDF
- GitHub

## Project Structure


CareerAI/
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── recommendation.py
├── career_data.py
├── roadmap.py
├── ai_roadmap.py
├── resume_analyzer.py
├── resume_recommender.py
├── requirements.txt
└── README.md


 ## Installation


git clone https://github.com/Muhammad-Shahzaib8/CareerAI.git
cd CareerAI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
## Environment Variables
Create a .env file:
GEMINI_API_KEY=your_gemini_api_key_here
Run Project
uvicorn main:app --reload
Open:
http://127.0.0.1:8000/docs

## Main APIs

Method	Endpoint	Description
POST	/register/	Register user
POST	/login/	Login user
POST	/students/	Create student profile
GET	/students/	Get students
POST	/recommend-careers/	Recommend careers
POST	/generate-roadmap/	Generate basic roadmap
POST	/analyze-resume/	Upload and analyze resume
POST	/generate-ai-roadmap/	Generate AI roadmap

## Future Enhancements

React/Next.js frontend
Admin dashboard
Live job trend analysis
LinkedIn profile analyzer
GitHub profile analyzer
Saved roadmaps
Payment/subscription system
Deployment on cloud


## Author

Muhammad Shahzaib
AI Career Roadmap Recommendation System
