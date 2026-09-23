import pytest
from backend.app.services.embeddings import embedding_service
from backend.app.services.matcher import match_skills
from backend.app.schemas.analysis import CandidateInfo, JobInfo
from backend.app.services.skill_normalizer import normalize_skill, are_skills_related


def test_embedding_service_singleton_and_similarity():
    assert embedding_service is not None
    # Semantic sentence similarity for domain tasks
    sim_rest = embedding_service.compute_similarity(
        "RESTful API development with Python", 
        "Building REST APIs in Python"
    )
    assert sim_rest > 0.75

    sim_ml = embedding_service.compute_similarity(
        "Trained deep learning machine learning models", 
        "Machine learning predictive models"
    )
    assert sim_ml > 0.60

    # Unrelated terms should have significantly lower similarity
    sim_unrelated = embedding_service.compute_similarity(
        "PostgreSQL relational database schema design", 
        "Graphic design with Photoshop and typography"
    )
    assert sim_unrelated < 0.40


def test_semantic_relationship_examples():
    # User specified examples:
    # 1. "React.js" and "React"
    canon1, _ = normalize_skill("React.js")
    canon2, _ = normalize_skill("React")
    assert canon1 == canon2 == "React"

    # 2. "RESTful API development" and "REST API"
    canon_rest1, _ = normalize_skill("RESTful API development")
    canon_rest2, _ = normalize_skill("REST API")
    assert canon_rest1 == canon_rest2 == "REST API"

    # 3. "Machine Learning" and "ML"
    canon_ml1, _ = normalize_skill("Machine Learning")
    canon_ml2, _ = normalize_skill("ML")
    assert canon_ml1 == canon_ml2 == "Machine Learning"

    # 4. "PostgreSQL" and "relational database experience"
    canon_pg, _ = normalize_skill("PostgreSQL")
    canon_rdb, _ = normalize_skill("relational database experience")
    assert are_skills_related(canon_pg, canon_rdb)


def test_matcher_distinguishes_exact_semantic_missing():
    candidate = CandidateInfo(
        name="Test Dev",
        technical_skills=["Python", "FastAPI", "PostgreSQL"],
        work_experience=[
            {"description": "Developed backend microservices using FastAPI and relational databases."}
        ],
        projects=["Created machine learning classification model using PyTorch."],
        estimated_years_experience=3.0
    )

    job = JobInfo(
        title="Backend Developer",
        required_skills=["Python", "Docker"],
        preferred_skills=["Machine Learning"],
        required_experience_years=2.0
    )

    resume_text = "Experienced in Python and PostgreSQL. Built microservices with FastAPI."
    job_text = "Requires Python and Docker. Preferred: Machine Learning."

    matched, missing, partial = match_skills(candidate, job, resume_text, job_text)

    match_dict = {m.skill: m for m in matched}
    missing_names = [m.skill for m in missing]

    # Python is an EXACT MATCH
    assert match_dict["Python"].match_type == "EXACT MATCH"
    assert match_dict["Python"].similarity_score >= 0.88

    # Docker is MISSING
    assert "Docker" in missing_names
    assert any(m.skill == "Docker" and m.importance == "CRITICAL" for m in missing)

    # Machine Learning matches semantically via projects
    assert match_dict["Machine Learning"].match_type in ["EXACT MATCH", "SEMANTIC MATCH"]
    assert match_dict["Machine Learning"].similarity_score >= 0.50
