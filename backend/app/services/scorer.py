from typing import List, Dict, Any, Tuple
from backend.app.schemas.analysis import (
    CandidateInfo,
    JobInfo,
    SkillMatch,
    ScoreBreakdown,
    ScoreBreakdownItem
)
from backend.app.services.embeddings import embedding_service
from backend.app.core.config import settings


def get_rating_label(overall_score: float) -> str:
    """Return qualitative rating badge for overall score."""
    if overall_score >= 88.0:
        return "Exceptional Alignment"
    elif overall_score >= 75.0:
        return "Strong Semantic Alignment"
    elif overall_score >= 60.0:
        return "Moderate Alignment"
    elif overall_score >= 45.0:
        return "Partial Alignment"
    else:
        return "Low Alignment"


def calculate_compatibility_score(
    candidate: CandidateInfo,
    job: JobInfo,
    matched_skills: List[SkillMatch]
) -> Tuple[float, str, ScoreBreakdown]:
    """
    Computes transparent weighted compatibility score strictly between 0 and 100.
    Weights:
      - Required Skills: 50%
      - Preferred Skills: 15%
      - Experience: 20%
      - Education/Certifications: 5%
      - Projects Semantic Relevance: 10%
    """
    # 1. Required Skills Score (50 max)
    req_matches = [m for m in matched_skills if m.requirement_type == "REQUIRED"]
    max_req_score = settings.WEIGHT_REQUIRED_SKILLS * 100.0  # 50.0

    if not req_matches:
        earned_req = max_req_score
        req_comment = "No specific required skills specified in job description."
    else:
        scores = []
        for m in req_matches:
            if m.match_type == "EXACT MATCH":
                scores.append(1.0)
            elif m.match_type == "SEMANTIC MATCH":
                scores.append(m.similarity_score)
            else:
                scores.append(0.0)
        
        avg_req = sum(scores) / len(scores)
        earned_req = round(avg_req * max_req_score, 1)
        exact_count = sum(1 for m in req_matches if m.match_type == "EXACT MATCH")
        semantic_count = sum(1 for m in req_matches if m.match_type == "SEMANTIC MATCH")
        missing_count = sum(1 for m in req_matches if m.match_type == "MISSING")
        req_comment = (
            f"Matched {exact_count + semantic_count}/{len(req_matches)} required skills "
            f"({exact_count} exact, {semantic_count} semantic). {missing_count} critical missing."
        )

    # 2. Preferred Skills Score (15 max)
    pref_matches = [m for m in matched_skills if m.requirement_type == "PREFERRED"]
    max_pref_score = settings.WEIGHT_PREFERRED_SKILLS * 100.0  # 15.0

    if not pref_matches:
        earned_pref = max_pref_score
        pref_comment = "No preferred skills explicitly listed; full points awarded."
    else:
        scores = []
        for m in pref_matches:
            if m.match_type == "EXACT MATCH":
                scores.append(1.0)
            elif m.match_type == "SEMANTIC MATCH":
                scores.append(m.similarity_score)
            else:
                scores.append(0.0)
        
        avg_pref = sum(scores) / len(scores)
        earned_pref = round(avg_pref * max_pref_score, 1)
        matched_pref = sum(1 for m in pref_matches if m.match_type in ["EXACT MATCH", "SEMANTIC MATCH"])
        pref_comment = f"Demonstrated {matched_pref}/{len(pref_matches)} preferred or bonus qualifications."

    # 3. Experience Score (20 max)
    max_exp_score = settings.WEIGHT_EXPERIENCE * 100.0  # 20.0
    cand_years = candidate.estimated_years_experience
    req_years = job.required_experience_years

    if req_years <= 0:
        earned_exp = max_exp_score
        exp_comment = f"Candidate has ~{cand_years:.1f} years experience. Meets role expectations."
    else:
        ratio = min(1.2, cand_years / req_years)
        earned_exp = round(min(1.0, ratio) * max_exp_score, 1)
        if cand_years >= req_years:
            exp_comment = f"Candidate demonstrates ~{cand_years:.1f} yrs experience, meeting or exceeding required {req_years:.1f} yrs."
        else:
            exp_comment = f"Candidate has ~{cand_years:.1f} yrs experience vs {req_years:.1f} yrs required."

    # 4. Education & Certifications (5 max)
    max_edu_score = settings.WEIGHT_EDUCATION * 100.0  # 5.0
    edu_pts = 0.0
    has_degree = len(candidate.education) > 0
    has_certs = len(candidate.certifications) > 0
    
    if has_degree:
        edu_pts += 3.5
    if has_certs:
        edu_pts += 1.5
    if not has_degree and not has_certs and not job.education_requirements:
        edu_pts = max_edu_score

    earned_edu = min(max_edu_score, edu_pts)
    edu_comment = f"{len(candidate.education)} degree(s) and {len(candidate.certifications)} certification(s) verified."

    # 5. Semantic Relevance of Projects (10 max)
    max_proj_score = settings.WEIGHT_PROJECTS * 100.0  # 10.0
    if not candidate.projects:
        earned_proj = 5.0
        proj_comment = "No specific standalone projects section detected; moderate baseline score applied."
    elif embedding_service.is_loaded and job.responsibilities:
        # Compute semantic alignment of projects to job responsibilities
        proj_sims = embedding_service.compute_similarity_matrix(candidate.projects, job.responsibilities)
        avg_proj_sim = float(proj_sims.mean()) if proj_sims.size > 0 else 0.5
        # Scale to max_proj_score
        proj_factor = min(1.0, max(0.4, avg_proj_sim * 1.3))
        earned_proj = round(proj_factor * max_proj_score, 1)
        proj_comment = f"Candidate's {len(candidate.projects)} project(s) show strong domain relevance to role responsibilities."
    else:
        earned_proj = 8.0
        proj_comment = f"Extracted {len(candidate.projects)} relevant technical project(s)."

    # Final Overall Score
    total_raw = earned_req + earned_pref + earned_exp + earned_edu + earned_proj
    overall_score = round(max(0.0, min(100.0, total_raw)), 1)
    rating_label = get_rating_label(overall_score)

    breakdown = ScoreBreakdown(
        required_skills=ScoreBreakdownItem(
            category="Required Skills",
            weight_percentage=settings.WEIGHT_REQUIRED_SKILLS * 100,
            earned_score=earned_req,
            max_score=max_req_score,
            commentary=req_comment
        ),
        preferred_skills=ScoreBreakdownItem(
            category="Preferred Skills",
            weight_percentage=settings.WEIGHT_PREFERRED_SKILLS * 100,
            earned_score=earned_pref,
            max_score=max_pref_score,
            commentary=pref_comment
        ),
        experience=ScoreBreakdownItem(
            category="Experience Match",
            weight_percentage=settings.WEIGHT_EXPERIENCE * 100,
            earned_score=earned_exp,
            max_score=max_exp_score,
            commentary=exp_comment
        ),
        education_certs=ScoreBreakdownItem(
            category="Education & Certifications",
            weight_percentage=settings.WEIGHT_EDUCATION * 100,
            earned_score=earned_edu,
            max_score=max_edu_score,
            commentary=edu_comment
        ),
        projects=ScoreBreakdownItem(
            category="Projects & Domain Alignment",
            weight_percentage=settings.WEIGHT_PROJECTS * 100,
            earned_score=earned_proj,
            max_score=max_proj_score,
            commentary=proj_comment
        )
    )

    return overall_score, rating_label, breakdown
