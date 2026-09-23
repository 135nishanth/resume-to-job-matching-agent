import re
from typing import List, Tuple, Dict, Any, Optional
from backend.app.schemas.analysis import CandidateInfo, JobInfo, SkillMatch, MissingSkill
from backend.app.services.skill_normalizer import (
    normalize_skill,
    get_related_skills,
    are_skills_related
)
from backend.app.services.embeddings import embedding_service
from backend.app.core.config import settings


def find_best_evidence_sentence(keyword: str, text: str, fallback_snippets: List[str]) -> str:
    """
    Search for a sentence in text containing the keyword or semantically most similar sentence.
    """
    # 1. Direct keyword mention in text lines
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 15]
    for line in lines:
        if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", line.lower()):
            clean = re.sub(r"^[-*•\s\d\.\)]+", "", line).strip()
            return clean

    # 2. Check fallback snippet list
    for snip in fallback_snippets:
        if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", snip.lower()):
            return snip

    # 3. If semantic model loaded, find sentence with highest similarity
    if lines and embedding_service.is_loaded:
        similarities = embedding_service.compute_similarity_matrix([keyword], lines[:30])[0]
        best_idx = int(similarities.argmax())
        if similarities[best_idx] > 0.50:
            return re.sub(r"^[-*•\s\d\.\)]+", "", lines[best_idx]).strip()

    return f"Demonstrated background related to {keyword}"


def find_job_requirement_sentence(skill: str, job_text: str, fallback_requirements: List[str]) -> str:
    """Find the specific sentence in the JD mentioning this skill."""
    lines = [l.strip() for l in job_text.split("\n") if len(l.strip()) > 10]
    for line in lines:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", line.lower()):
            clean = re.sub(r"^[-*•\s\d\.\)]+", "", line).strip()
            return clean

    for snip in fallback_requirements:
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", snip.lower()):
            return snip

    return f"Requirement for {skill} in target role"


def match_skills(
    candidate: CandidateInfo,
    job: JobInfo,
    raw_resume_text: str,
    raw_job_text: str
) -> Tuple[List[SkillMatch], List[MissingSkill], List[SkillMatch]]:
    """
    Perform semantic matching between candidate skills & experience and job requirements.
    Distinguishes:
      - EXACT MATCH
      - SEMANTIC MATCH
      - MISSING
    Separates missing into Critical (Required) and Nice-to-Have (Preferred).
    """
    all_matched_skills: List[SkillMatch] = []
    missing_skills: List[MissingSkill] = []
    partial_matches: List[SkillMatch] = []

    # Prepare candidate textual evidence corpus
    candidate_skills_set = set(s.lower() for s in candidate.technical_skills)
    candidate_skills_list = candidate.technical_skills
    exp_bullets = [item.get("description", "") for item in candidate.work_experience if isinstance(item, dict)]
    proj_bullets = candidate.projects
    all_candidate_statements = candidate_skills_list + exp_bullets + proj_bullets

    # Process Required Skills
    for skill_name in job.required_skills:
        canonical_name, category = normalize_skill(skill_name)
        match_record, is_missing = evaluate_single_skill_match(
            skill_name=skill_name,
            canonical_name=canonical_name,
            category=category,
            requirement_type="REQUIRED",
            candidate_skills_set=candidate_skills_set,
            candidate_skills_list=candidate_skills_list,
            all_candidate_statements=all_candidate_statements,
            raw_resume_text=raw_resume_text,
            raw_job_text=raw_job_text,
            job_requirements=job.responsibilities
        )
        all_matched_skills.append(match_record)

        if is_missing:
            # Detect related candidate skills for missing required skill
            related = [
                cs for cs in candidate.technical_skills 
                if are_skills_related(canonical_name, cs) or cs in get_related_skills(canonical_name)
            ]
            missing_skills.append(MissingSkill(
                skill=skill_name,
                canonical_skill=canonical_name,
                category=category,
                importance="CRITICAL",
                reason=f"Required qualification '{skill_name}' was not detected in candidate profile.",
                related_candidate_skills=related[:3]
            ))
        elif match_record.match_type == "SEMANTIC MATCH":
            partial_matches.append(match_record)

    # Process Preferred Skills
    for skill_name in job.preferred_skills:
        canonical_name, category = normalize_skill(skill_name)
        match_record, is_missing = evaluate_single_skill_match(
            skill_name=skill_name,
            canonical_name=canonical_name,
            category=category,
            requirement_type="PREFERRED",
            candidate_skills_set=candidate_skills_set,
            candidate_skills_list=candidate_skills_list,
            all_candidate_statements=all_candidate_statements,
            raw_resume_text=raw_resume_text,
            raw_job_text=raw_job_text,
            job_requirements=job.responsibilities
        )
        all_matched_skills.append(match_record)

        if is_missing:
            related = [
                cs for cs in candidate.technical_skills 
                if are_skills_related(canonical_name, cs) or cs in get_related_skills(canonical_name)
            ]
            missing_skills.append(MissingSkill(
                skill=skill_name,
                canonical_skill=canonical_name,
                category=category,
                importance="NICE_TO_HAVE",
                reason=f"Preferred qualification '{skill_name}' not explicitly evidenced.",
                related_candidate_skills=related[:3]
            ))
        elif match_record.match_type == "SEMANTIC MATCH":
            partial_matches.append(match_record)

    return all_matched_skills, missing_skills, partial_matches


def evaluate_single_skill_match(
    skill_name: str,
    canonical_name: str,
    category: str,
    requirement_type: str,
    candidate_skills_set: set,
    candidate_skills_list: List[str],
    all_candidate_statements: List[str],
    raw_resume_text: str,
    raw_job_text: str,
    job_requirements: List[str]
) -> Tuple[SkillMatch, bool]:
    """Evaluate whether a skill is EXACT MATCH, SEMANTIC MATCH, or MISSING."""
    job_sentence = find_job_requirement_sentence(skill_name, raw_job_text, job_requirements)

    # 1. Check exact match via canonical or direct text in resume
    is_exact = False
    if canonical_name.lower() in candidate_skills_set or skill_name.lower() in candidate_skills_set:
        is_exact = True
    elif re.search(r"\b" + re.escape(skill_name.lower()) + r"\b", raw_resume_text.lower()):
        is_exact = True

    if is_exact:
        evidence = find_best_evidence_sentence(skill_name, raw_resume_text, all_candidate_statements)
        return SkillMatch(
            skill=skill_name,
            canonical_skill=canonical_name,
            category=category,
            requirement_type=requirement_type,
            match_type="EXACT MATCH",
            similarity_score=1.0,
            candidate_evidence=evidence,
            job_requirement=job_sentence
        ), False

    # 2. Check semantic similarity against candidate statements & skills
    best_similarity = 0.0
    best_evidence = ""

    if all_candidate_statements and embedding_service.is_loaded:
        sim_scores = embedding_service.compute_similarity_matrix([skill_name], all_candidate_statements)[0]
        best_idx = int(sim_scores.argmax())
        best_similarity = float(sim_scores[best_idx])
        best_evidence = all_candidate_statements[best_idx]

    # Evaluate against thresholds
    if best_similarity >= settings.EXACT_MATCH_THRESHOLD:
        return SkillMatch(
            skill=skill_name,
            canonical_skill=canonical_name,
            category=category,
            requirement_type=requirement_type,
            match_type="EXACT MATCH",
            similarity_score=round(best_similarity, 3),
            candidate_evidence=best_evidence,
            job_requirement=job_sentence
        ), False
    elif best_similarity >= settings.SEMANTIC_MATCH_THRESHOLD:
        return SkillMatch(
            skill=skill_name,
            canonical_skill=canonical_name,
            category=category,
            requirement_type=requirement_type,
            match_type="SEMANTIC MATCH",
            similarity_score=round(best_similarity, 3),
            candidate_evidence=best_evidence,
            job_requirement=job_sentence
        ), False
    else:
        # Check domain ontology cluster for partial credit
        for c_skill in candidate_skills_list:
            c_canon, _ = normalize_skill(c_skill)
            if are_skills_related(canonical_name, c_canon) or are_skills_related(canonical_name, c_skill):
                best_similarity = max(best_similarity, 0.75)
                best_evidence = f"Possesses related skill: {c_skill}"
                return SkillMatch(
                    skill=skill_name,
                    canonical_skill=canonical_name,
                    category=category,
                    requirement_type=requirement_type,
                    match_type="SEMANTIC MATCH",
                    similarity_score=best_similarity,
                    candidate_evidence=best_evidence,
                    job_requirement=job_sentence
                ), False

        return SkillMatch(
            skill=skill_name,
            canonical_skill=canonical_name,
            category=category,
            requirement_type=requirement_type,
            match_type="MISSING",
            similarity_score=round(best_similarity, 3),
            candidate_evidence="No direct or semantic evidence found in resume.",
            job_requirement=job_sentence
        ), True
