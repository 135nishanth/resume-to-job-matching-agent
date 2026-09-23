from typing import List
from backend.app.schemas.analysis import (
    CandidateInfo,
    JobInfo,
    SkillMatch,
    MissingSkill,
    ScoreBreakdown,
    ExplanationReport
)


def generate_explanation_report(
    candidate: CandidateInfo,
    job: JobInfo,
    matched_skills: List[SkillMatch],
    missing_skills: List[MissingSkill],
    overall_score: float,
    rating_label: str,
    score_breakdown: ScoreBreakdown
) -> ExplanationReport:
    """
    Generate an explainable, objective narrative breakdown strictly grounded in
    extracted resume data and job requirements.
    """
    # 1. Overall Summary
    summary = (
        f"Candidate {candidate.name} earned an overall compatibility score of {overall_score:.0f}/100 "
        f"({rating_label}) for the position of '{job.title}'. "
        f"The candidate meets key core competencies with {score_breakdown.required_skills.earned_score:.1f}/"
        f"{score_breakdown.required_skills.max_score:.1f} points in required technical requirements."
    )

    # 2. Key Strengths (Only substantiated by extracted matches)
    strengths: List[str] = []
    exact_matches = [m for m in matched_skills if m.match_type == "EXACT MATCH"]
    semantic_matches = [m for m in matched_skills if m.match_type == "SEMANTIC MATCH"]

    for m in exact_matches[:5]:
        if m.candidate_evidence and "No direct" not in m.candidate_evidence:
            strengths.append(f"Strong direct proficiency in {m.skill}: \"{m.candidate_evidence[:90]}\"")
        else:
            strengths.append(f"Verified match for required skill '{m.skill}'.")

    for m in semantic_matches[:3]:
        strengths.append(
            f"Demonstrated semantic alignment with {m.skill} (Similarity: {int(m.similarity_score * 100)}%): "
            f"\"{m.candidate_evidence[:80]}\""
        )

    # 3. Critical Missing vs Nice-to-Have Missing
    critical_missing = [m.skill for m in missing_skills if m.importance == "CRITICAL"]
    nice_to_have = [m.skill for m in missing_skills if m.importance == "NICE_TO_HAVE"]

    # 4. Experience Summary
    cand_yrs = candidate.estimated_years_experience
    req_yrs = job.required_experience_years
    if req_yrs > 0:
        if cand_yrs >= req_yrs:
            exp_text = (
                f"Candidate demonstrates approximately {cand_yrs:.1f} years of relevant professional experience, "
                f"meeting or exceeding the required {req_yrs:.1f} years."
            )
        else:
            exp_text = (
                f"Candidate demonstrates approximately {cand_yrs:.1f} years of relevant experience, "
                f"which is below the target requirement of {req_yrs:.1f} years."
            )
    else:
        exp_text = f"Candidate profile indicates approximately {cand_yrs:.1f} years of accumulated experience."

    # 5. Actionable Recommendations
    recommendations: List[str] = []
    if critical_missing:
        recommendations.append(
            f"Prioritize probing candidate's practical exposure to core missing requirements: {', '.join(critical_missing[:3])}."
        )
    if semantic_matches:
        rec_skills = [m.skill for m in semantic_matches[:2]]
        recommendations.append(
            f"Verify hands-on depth during technical interview for semantically related skills: {', '.join(rec_skills)}."
        )
    if candidate.projects:
        recommendations.append(
            f"Review portfolio project '{candidate.projects[0][:60]}' to evaluate architecture design patterns."
        )
    if not recommendations:
        recommendations.append("Candidate demonstrates strong all-around qualifications; recommend advancing to interview.")

    return ExplanationReport(
        overall_summary=summary,
        strengths=strengths,
        critical_missing=critical_missing,
        nice_to_have_missing=nice_to_have,
        experience_summary=exp_text,
        recommendations=recommendations
    )
