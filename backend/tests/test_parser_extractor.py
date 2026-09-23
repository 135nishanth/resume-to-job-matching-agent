import pytest
from backend.app.services.parser import parse_document, DocumentParsingError
from backend.app.services.extractor import extract_resume_info, extract_job_info


def test_parse_plain_text():
    sample_txt = "John Doe\nSoftware Engineer\nSkills: Python, Docker\nExperience: 5 years"
    parsed = parse_document(sample_txt.encode("utf-8"), "resume.txt")
    assert "John Doe" in parsed
    assert "Python" in parsed


def test_parse_empty_document_raises_error():
    with pytest.raises(DocumentParsingError):
        parse_document(b"", "empty.txt")


def test_extract_resume_no_hallucination():
    sample_text = """
    Jane Smith
    Email: jane.smith@example.com
    Phone: (555) 123-4567

    SUMMARY
    Senior Frontend Engineer with 4 years experience in React and TypeScript.

    EDUCATION
    Bachelor of Science in Computer Science, MIT 2020

    SKILLS
    React, TypeScript, CSS, Git
    """
    candidate = extract_resume_info(sample_text)
    assert candidate.name == "Jane Smith"
    assert candidate.email == "jane.smith@example.com"
    assert candidate.phone == "(555) 123-4567"
    assert "React" in candidate.technical_skills
    assert "TypeScript" in candidate.technical_skills
    assert candidate.estimated_years_experience >= 4.0

    # Ensure no hallucination of skills not mentioned
    assert "Kubernetes" not in candidate.technical_skills
    assert "Rust" not in candidate.technical_skills


def test_extract_job_sections():
    sample_jd = """
    Job Title: Full Stack Developer
    Company: TechCorp

    REQUIRED SKILLS
    - Python
    - FastAPI
    - PostgreSQL

    PREFERRED SKILLS
    - Docker
    - Kubernetes
    """
    job = extract_job_info(sample_jd)
    assert job.title == "Full Stack Developer"
    assert "Python" in job.required_skills
    assert "FastAPI" in job.required_skills
    assert "PostgreSQL" in job.required_skills
    assert "Docker" in job.preferred_skills
    assert "Kubernetes" in job.preferred_skills
