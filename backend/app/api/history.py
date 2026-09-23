from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.core.database import get_db
from backend.app.models.analysis import AnalysisHistory
from backend.app.schemas.analysis import HistorySummary, AnalysisResponse

router = APIRouter()


@router.get("/history", response_model=List[HistorySummary])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    records = db.query(AnalysisHistory).order_by(desc(AnalysisHistory.created_at)).limit(limit).all()
    summaries = []
    for r in records:
        matched_cnt = len(r.matched_skills) if isinstance(r.matched_skills, list) else 0
        missing_cnt = len(r.missing_skills) if isinstance(r.missing_skills, list) else 0
        summaries.append(HistorySummary(
            id=r.id,
            created_at=r.created_at.isoformat() if r.created_at else "",
            candidate_name=r.candidate_name,
            job_title=r.job_title,
            overall_score=r.overall_score,
            rating_label=r.rating_label,
            total_matched=matched_cnt,
            total_missing=missing_cnt
        ))
    return summaries


@router.get("/history/{record_id}", response_model=AnalysisResponse)
def get_history_detail(record_id: int, db: Session = Depends(get_db)):
    record = db.query(AnalysisHistory).filter(AnalysisHistory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    matched = record.matched_skills or []
    missing = record.missing_skills or []
    partials = [m for m in matched if m.get("match_type") == "SEMANTIC MATCH"]

    return AnalysisResponse(
        id=record.id,
        created_at=record.created_at.isoformat() if record.created_at else "",
        overall_score=record.overall_score,
        rating_label=record.rating_label,
        candidate_info=record.candidate_info,
        job_info=record.job_info,
        matched_skills=matched,
        missing_skills=missing,
        partial_matches=partials,
        total_matched_count=len(matched),
        total_missing_count=len(missing),
        total_partial_count=len(partials),
        score_breakdown=record.score_breakdown,
        explanation=record.explanations
    )


@router.delete("/history/{record_id}")
def delete_history_detail(record_id: int, db: Session = Depends(get_db)):
    record = db.query(AnalysisHistory).filter(AnalysisHistory.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    db.delete(record)
    db.commit()
    return {"message": "Record successfully deleted"}
