import logging
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.schemas.analysis import AnalysisResponse
from backend.app.services.parser import parse_document, DocumentParsingError
from backend.app.services.extractor import extract_resume_info, extract_job_info
from backend.app.services.matcher import match_skills
from backend.app.services.scorer import calculate_compatibility_score
from backend.app.services.explainer import generate_explanation_report
from backend.app.core.database import get_db
from backend.app.models.analysis import AnalysisHistory

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_match(
    resume: UploadFile = File(..., description="Candidate resume in PDF, DOCX, or TXT format"),
    job_description_text: Optional[str] = Form(None, description="Pasted Job Description text"),
    job_description_file: Optional[UploadFile] = File(None, description="Optional uploaded JD file"),
    db: Session = Depends(get_db)
):
    """
    Complete analysis pipeline:
    1. Parse resume and job documents
    2. Extract structured candidate and job information
    3. Perform semantic skill normalization and matching
    4. Compute transparent compatibility scores
    5. Detect critical and nice-to-have missing skills
    6. Generate grounded explanation report
    7. Persist to SQLite history
    """
    logger.info(f"Received analyze request. Resume file: {resume.filename}")

    # 1. Parse Resume Document
    try:
        resume_bytes = await resume.read()
        resume_text = parse_document(resume_bytes, resume.filename or "resume.txt")
    except DocumentParsingError as e:
        logger.warning(f"Resume parsing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error parsing resume: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to parse resume document. Please check the file format.")

    # 2. Parse Job Description
    job_text = ""
    if job_description_text and job_description_text.strip():
        job_text = job_description_text.strip()
    elif job_description_file:
        try:
            jd_bytes = await job_description_file.read()
            job_text = parse_document(jd_bytes, job_description_file.filename or "jd.txt")
        except DocumentParsingError as e:
            raise HTTPException(status_code=400, detail=f"Job description file error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to parse job description file.")
    else:
        raise HTTPException(status_code=400, detail="Please provide a job description (either paste text or upload a file).")

    if len(job_text.strip()) < 30:
        raise HTTPException(status_code=400, detail="Job description text is too short to perform a meaningful analysis.")

    # 3. Information Extraction
    try:
        candidate_info = extract_resume_info(resume_text)
        job_info = extract_job_info(job_text)
    except Exception as e:
        logger.error(f"Error during information extraction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to extract information from documents.")

    # 4. Semantic Matching & Missing Skills
    try:
        matched_skills, missing_skills, partial_matches = match_skills(
            candidate=candidate_info,
            job=job_info,
            raw_resume_text=resume_text,
            raw_job_text=job_text
        )
    except Exception as e:
        logger.error(f"Error during matching: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to run semantic matching engine.")

    # 5. Compatibility Scoring
    try:
        overall_score, rating_label, score_breakdown = calculate_compatibility_score(
            candidate=candidate_info,
            job=job_info,
            matched_skills=matched_skills
        )
    except Exception as e:
        logger.error(f"Error during scoring: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to calculate compatibility score.")

    # 6. Explanation Report
    try:
        explanation = generate_explanation_report(
            candidate=candidate_info,
            job=job_info,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            overall_score=overall_score,
            rating_label=rating_label,
            score_breakdown=score_breakdown
        )
    except Exception as e:
        logger.error(f"Error generating explanation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate explanation report.")

    created_iso = datetime.utcnow().isoformat()

    # 7. Persist to Database
    db_record = None
    try:
        db_record = AnalysisHistory(
            candidate_name=candidate_info.name,
            candidate_email=candidate_info.email,
            job_title=job_info.title,
            overall_score=overall_score,
            rating_label=rating_label,
            score_breakdown=score_breakdown.model_dump(),
            matched_skills=[m.model_dump() for m in matched_skills],
            missing_skills=[m.model_dump() for m in missing_skills],
            explanations=explanation.model_dump(),
            candidate_info=candidate_info.model_dump(),
            job_info=job_info.model_dump()
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        logger.warning(f"Could not persist history to database: {e}")
        db.rollback()

    matched_exact_and_semantic = [m for m in matched_skills if m.match_type != "MISSING"]

    return AnalysisResponse(
        id=db_record.id if db_record else None,
        created_at=created_iso,
        overall_score=overall_score,
        rating_label=rating_label,
        candidate_info=candidate_info,
        job_info=job_info,
        matched_skills=matched_exact_and_semantic,
        missing_skills=missing_skills,
        partial_matches=partial_matches,
        total_matched_count=len(matched_exact_and_semantic),
        total_missing_count=len(missing_skills),
        total_partial_count=len(partial_matches),
        score_breakdown=score_breakdown,
        explanation=explanation
    )
