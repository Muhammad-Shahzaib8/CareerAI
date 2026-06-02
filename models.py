from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    skills = Column(String, nullable=False)
    interest = Column(String, nullable=False)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
class SavedRoadmap(Base):
    __tablename__ = "saved_roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    career = Column(String, nullable=False)
    current_skills = Column(String, nullable=False)
    missing_skills = Column(String, nullable=False)
    roadmap_text = Column(String, nullable=False)
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)