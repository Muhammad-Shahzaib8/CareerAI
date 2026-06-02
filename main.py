from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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
from auth import get_current_user_email
from schemas import ChatbotRequest
from career_chatbot import get_career_chatbot_response
from schemas import ChangePasswordRequest

from schemas import UserRegister, UserLogin
from auth import hash_password, verify_password, create_access_token, get_current_user_email

from database import Base, engine, get_db
from models import Student, User, SavedRoadmap, ChatHistory
from schemas import StudentCreate, StudentResponse
from schemas import StudentCreate, StudentResponse, RecommendationRequest
from recommendation import recommend_careers
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerAI Roadmap Advisor",
    description="AI-powered career roadmap system for students",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
@app.get("/my-profile/")
def my_profile(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }
@app.post("/protected-ai-roadmap/")
def protected_ai_roadmap(
    data: AIRoadmapRequest,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    roadmap = generate_ai_roadmap(
        country=data.country,
        degree=data.degree,
        career=data.career,
        current_skills=data.current_skills,
        missing_skills=data.missing_skills
    )

    saved_roadmap = SavedRoadmap(
        user_email=current_user_email,
        country=data.country,
        degree=data.degree,
        career=data.career,
        current_skills=data.current_skills,
        missing_skills=", ".join(data.missing_skills),
        roadmap_text=roadmap
    )

    db.add(saved_roadmap)
    db.commit()
    db.refresh(saved_roadmap)

    return {
        "message": "AI roadmap generated and saved successfully",
        "roadmap_id": saved_roadmap.id,
        "user": current_user_email,
        "career": data.career,
        "ai_roadmap": roadmap
    }
@app.get("/my-roadmaps/")
def get_my_roadmaps(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    roadmaps = db.query(SavedRoadmap).filter(
        SavedRoadmap.user_email == current_user_email
    ).all()

    return roadmaps
@app.get("/roadmap/{roadmap_id}")
def get_single_roadmap(
    roadmap_id: int,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    roadmap = db.query(SavedRoadmap).filter(
        SavedRoadmap.id == roadmap_id,
        SavedRoadmap.user_email == current_user_email
    ).first()

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found"
        )

    return roadmap
@app.delete("/roadmap/{roadmap_id}")
def delete_roadmap(
    roadmap_id: int,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    roadmap = db.query(SavedRoadmap).filter(
        SavedRoadmap.id == roadmap_id,
        SavedRoadmap.user_email == current_user_email
    ).first()

    if not roadmap:
        raise HTTPException(
            status_code=404,
            detail="Roadmap not found"
        )

    db.delete(roadmap)
    db.commit()

    return {
        "message": "Roadmap deleted successfully"
    }

@app.post("/career-chatbot/")
def career_chatbot(
    data: ChatbotRequest,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    reply = get_career_chatbot_response(
        user_email=current_user_email,
        message=data.message
    )

    new_chat = ChatHistory(
        user_email=current_user_email,
        question=data.message,
        answer=reply
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return {
        "message": "Chat response generated and saved successfully",
        "chat_id": new_chat.id,
        "user": current_user_email,
        "question": data.message,
        "reply": reply
    }
@app.get("/my-chat-history/")
def get_my_chat_history(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    chats = db.query(ChatHistory).filter(
        ChatHistory.user_email == current_user_email
    ).all()

    return chats
@app.delete("/chat/{chat_id}")
def delete_chat(
    chat_id: int,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    chat = db.query(ChatHistory).filter(
        ChatHistory.id == chat_id,
        ChatHistory.user_email == current_user_email
    ).first()

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db.delete(chat)
    db.commit()

    return {
        "message": "Chat deleted successfully"
    }
@app.post("/change-password/")
def change_password(
    data: ChangePasswordRequest,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == current_user_email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(data.old_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )

    user.password = hash_password(data.new_password)

    db.commit()

    return {
        "message": "Password changed successfully"
    }
@app.get("/dashboard-stats/")
def dashboard_stats(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    roadmap_count = db.query(SavedRoadmap).filter(
        SavedRoadmap.user_email == current_user_email
    ).count()

    chat_count = db.query(ChatHistory).filter(
        ChatHistory.user_email == current_user_email
    ).count()

    return {
        "roadmaps": roadmap_count,
        "chats": chat_count
    }