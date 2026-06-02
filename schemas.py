from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    country: str
    degree: str
    semester: str
    skills: str
    interest: str


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True
class RecommendationRequest(BaseModel):
    country: str
    degree: str
    skills: str
class RoadmapRequest(BaseModel):
    career: str
    missing_skills: list[str]
class ResumeCareerRequest(BaseModel):
    country: str
    degree: str
    skills: list[str]
class AIRoadmapRequest(BaseModel):
    country: str
    degree: str
    career: str
    current_skills: str
    missing_skills: list[str]
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str
class ChatbotRequest(BaseModel):
    message: str
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str