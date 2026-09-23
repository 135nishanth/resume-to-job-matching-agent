import pytest
from backend.app.schemas.analysis import CandidateInfo, JobInfo, SkillMatch
from backend.app.services.scorer import calculate_compatibility_score, get_rating_label
from backend.app.core.config import settings


def test_scorer_bounds_and_weights():
    candidate = CandidateInfo(
        name="Alice",
        estimated_years_experience=5.0,
        education=["BS Computer Science"],
        certifications=["AWS Certified"],
        projects=["Built full stack ecommerce app with React and FastAPI"]
    )

    job = JobInfo(
        title="Senior Python Engineer",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["AWS"],
        required_experience_years=4.0
    )

    # 100% match case
    perfect_matches = [
        SkillMatch(
            skill="Python",
            canonical_skill="Python",
            category="Languages",
            requirement_type="REQUIRED",
            match_type="EXACT MATCH",
            similarity_score=1.0,
            candidate_evidence="6 years Python",
            job_requirement="Strong Python"
        ),
        SkillMatch(
            skill="FastAPI",
            canonical_skill="FastAPI",
            category="Frameworks",
            requirement_type="REQUIRED",
            match_type="EXACT MATCH",
            similarity_score=1.0,
            candidate_evidence="FastAPI production services",
            job_requirement="FastAPI experience"
        ),
        SkillMatch(
            skill="AWS",
            canonical_skill="AWS",
            category="Cloud & DevOps",
            requirement_type="PREFERRED",
            match_type="EXACT MATCH",
            similarity_score=1.0,
            candidate_evidence="AWS certified",
            job_requirement="AWS preferred"
        )
    ]

    score, label, breakdown = calculate_compatibility_score(candidate, job, perfect_matches)
    assert 0.0 <= score <= 100.0
    assert score >= 90.0
    assert label == "Exceptional Alignment"
    assert breakdown.required_skills.earned_score == 50.0
    assert breakdown.preferred_skills.earned_score == 15.0


def test_scorer_penalizes_missing_required():
    candidate = CandidateInfo(
        name="Bob",
        estimated_years_experience=1.0,
        education=[],
        certifications=[]
    )

    job = JobInfo(
        title="Senior Architect",
        required_skills=["Kubernetes", "Distributed Systems", "C++"],
        preferred_skills=["AWS"],
        required_experience_years=8.0
    )

    # All required missing
    missing_matches = [
        SkillMatch(
            skill="Kubernetes",
            canonical_skill="Kubernetes",
            category="Cloud & DevOps",
            requirement_type="REQUIRED",
            match_type="MISSING",
            similarity_score=0.1,
            candidate_evidence="None",
            job_requirement="Kubernetes required"
        ),
        SkillMatch(
            skill="Distributed Systems",
            canonical_skill="Distributed Systems",
            category="Architecture",
            requirement_type="REQUIRED",
            match_type="MISSING",
            similarity_score=0.1,
            candidate_evidence="None",
            job_requirement="Distributed systems"
        ),
        SkillMatch(
            skill="C++",
            canonical_skill="C++",
            category="Languages",
            requirement_type="REQUIRED",
            match_type="MISSING",
            similarity_score=0.0,
            candidate_evidence="None",
            job_requirement="C++"
        )
    ]

    score, label, breakdown = calculate_compatibility_score(candidate, job, missing_matches)
    assert 0.0 <= score <= 100.0
    assert score < 40.0
    assert breakdown.required_skills.earned_score == 0.0
