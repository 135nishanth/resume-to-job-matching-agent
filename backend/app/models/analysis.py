from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from backend.app.core.database import Base


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    candidate_name = Column(String(255), default="Unknown Candidate")
    candidate_email = Column(String(255), nullable=True)
    job_title = Column(String(255), default="Job Match")
    overall_score = Column(Float, nullable=False)
    rating_label = Column(String(100), default="Match Score")
    
    # Store complete payload data
    score_breakdown = Column(JSON, nullable=False)
    matched_skills = Column(JSON, nullable=False)
    missing_skills = Column(JSON, nullable=False)
    explanations = Column(JSON, nullable=False)
    candidate_info = Column(JSON, nullable=False)
    job_info = Column(JSON, nullable=False)
