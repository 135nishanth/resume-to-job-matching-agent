from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CandidateInfo(BaseModel):
    name: str = "Unknown Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: List[str] = Field(default_factory=list)
    work_experience: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_years_experience: float = 0.0
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    cloud_technologies: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


class JobInfo(BaseModel):
    title: str = "Target Position"
    company: Optional[str] = None
    location: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    required_experience_years: float = 0.0
    preferred_experience_years: float = 0.0
    education_requirements: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


class SkillMatch(BaseModel):
    skill: str
    canonical_skill: str
    category: str
    requirement_type: str  # REQUIRED or PREFERRED
    match_type: str        # EXACT MATCH, SEMANTIC MATCH, or MISSING
    similarity_score: float
    candidate_evidence: str
    job_requirement: str


class MissingSkill(BaseModel):
    skill: str
    canonical_skill: str
    category: str
    importance: str        # CRITICAL (Required) or NICE_TO_HAVE (Preferred)
    reason: str
    related_candidate_skills: List[str] = Field(default_factory=list)


class ScoreBreakdownItem(BaseModel):
    category: str
    weight_percentage: float
    earned_score: float
    max_score: float
    commentary: str


class ScoreBreakdown(BaseModel):
    required_skills: ScoreBreakdownItem
    preferred_skills: ScoreBreakdownItem
    experience: ScoreBreakdownItem
    education_certs: ScoreBreakdownItem
    projects: ScoreBreakdownItem


class ExplanationReport(BaseModel):
    overall_summary: str
    strengths: List[str] = Field(default_factory=list)
    critical_missing: List[str] = Field(default_factory=list)
    nice_to_have_missing: List[str] = Field(default_factory=list)
    experience_summary: str
    recommendations: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    id: Optional[int] = None
    created_at: str
    overall_score: float
    rating_label: str
    candidate_info: CandidateInfo
    job_info: JobInfo
    matched_skills: List[SkillMatch] = Field(default_factory=list)
    missing_skills: List[MissingSkill] = Field(default_factory=list)
    partial_matches: List[SkillMatch] = Field(default_factory=list)
    total_matched_count: int = 0
    total_missing_count: int = 0
    total_partial_count: int = 0
    score_breakdown: ScoreBreakdown
    explanation: ExplanationReport


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    version: str


class HistorySummary(BaseModel):
    id: int
    created_at: str
    candidate_name: str
    job_title: str
    overall_score: float
    rating_label: str
    total_matched: int
    total_missing: int
