from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from roadmap import generate_roadmap
from schemas import RoadmapRequest
import os
import shutil
from fastapi import UploadFile, File
from resume_analyzer import analyze_resume
from resume_recommender import recommend_from_resume
from schemas import ResumeCareerRequest
from ai_roadmap import generate_ai_roadmap
from schemas import AIRoadmapRequest
from fastapi import HTTPException

from schemas import UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token

from database import Base, engine, get_db
from models import Student, User
from schemas import StudentCreate, StudentResponse
from schemas import StudentCreate, StudentResponse, RecommendationRequest
from recommendation import recommend_careers
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerAI Roadmap Advisor",
    description="AI-powered career roadmap system for students",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "CareerAI Backend is Running Successfully"
    }


@app.post("/students/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name,
        country=student.country,
        degree=student.degree,
        semester=student.semester,
        skills=student.skills,
        interest=student.interest
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/students/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students
@app.post("/recommend-careers/")
def recommend_career(data: RecommendationRequest):
    recommendations = recommend_careers(
        student_country=data.country,
        student_degree=data.degree,
        student_skills=data.skills
    )

    return {
        "country": data.country,
        "degree": data.degree,
        "current_skills": data.skills,
        "top_recommendations": recommendations
    }
@app.post("/generate-roadmap/")
def create_roadmap(data: RoadmapRequest):

    roadmap = generate_roadmap(
        data.career,
        data.missing_skills
    )

    return {
        "career": data.career,
        "roadmap": roadmap
    }
@app.post("/analyze-resume/")
def upload_resume(file: UploadFile = File(...)):
    upload_folder = "uploaded_resumes"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_resume(file_path)

    return {
        "filename": file.filename,
        "analysis": result
    }
@app.post("/resume-career-analysis/")
def resume_career_analysis(data: ResumeCareerRequest):

    recommendations = recommend_from_resume(
        data.country,
        data.degree,
        data.skills
    )

    return {
        "country": data.country,
        "degree": data.degree,
        "recommendations": recommendations
    }
@app.post("/generate-ai-roadmap/")
def create_ai_roadmap(data: AIRoadmapRequest):

    roadmap = generate_ai_roadmap(
        country=data.country,
        degree=data.degree,
        career=data.career,
        current_skills=data.current_skills,
        missing_skills=data.missing_skills
    )

    return {
        "career": data.career,
        "ai_roadmap": roadmap
    }
@app.post("/register/")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }
@app.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }