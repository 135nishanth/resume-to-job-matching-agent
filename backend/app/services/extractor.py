import re
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from backend.app.schemas.analysis import CandidateInfo, JobInfo
from backend.app.services.skill_normalizer import (
    SKILL_TAXONOMY,
    normalize_skill,
    clean_skill_string
)


# Section header detection regex patterns
RESUME_SECTIONS = {
    "summary": r"(?:summary|objective|professional\s+summary|profile|about\s+me)",
    "skills": r"(?:skills|technical\s+skills|skills\s+&\s+technologies|core\s+competencies|technologies|proficiencies)",
    "experience": r"(?:work\s+experience|professional\s+experience|experience|employment\s+history|career\s+history)",
    "education": r"(?:education|academic\s+background|academic\s+history|qualifications)",
    "projects": r"(?:projects|personal\s+projects|key\s+projects|notable\s+projects)",
    "certifications": r"(?:certifications|certificates|licenses|credentials)"
}

JD_SECTIONS = {
    "required": r"(?:required\s+skills|required\s+qualifications|basic\s+qualifications|minimum\s+qualifications|requirements|what\s+you\s+need|must\s+have)",
    "preferred": r"(?:preferred\s+skills|preferred\s+qualifications|bonus\s+points|nice\s+to\s+have|desired\s+qualifications|what\s+gives\s+you\s+an\s+edge|bonus)",
    "responsibilities": r"(?:responsibilities|duties|what\s+you'll\s+do|role\s+overview|key\s+responsibilities)",
    "about": r"(?:about\s+the\s+role|about\s+us|company\s+overview|summary)"
}


def extract_email(text: str) -> Optional[str]:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else None


def extract_name(text: str) -> str:
    """Extract candidate name from the top portion of the resume text."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return "Unknown Candidate"
    
    # Typically name is on line 1 or 2
    for line in lines[:4]:
        # Filter out lines that look like emails, urls, or section headers
        if "@" in line or "http" in line or "/" in line:
            continue
        cleaned = re.sub(r"^(resume|curriculum vitae|cv)\s*[-:]?\s*", "", line, flags=re.IGNORECASE).strip()
        words = cleaned.split()
        if 1 <= len(words) <= 4 and all(w[0].isupper() or w in ["de", "van", "von", "Jr.", "III"] for w in words if w):
            return cleaned
            
    return lines[0][:40]


def extract_sections(text: str, section_patterns: Dict[str, str]) -> Dict[str, str]:
    """Segment document text into sections based on recognized headers."""
    lines = text.split("\n")
    current_section = "header"
    sections: Dict[str, List[str]] = {"header": []}
    
    # Compile pattern list
    patterns = [(sec, re.compile(rf"^\s*(?:[\#\*\-]+\s*)?{pat}[:\s]*$", re.IGNORECASE)) 
                for sec, pat in section_patterns.items()]

    for line in lines:
        matched_section = None
        for sec, regex in patterns:
            if regex.match(line.strip()):
                matched_section = sec
                break
        
        if matched_section:
            current_section = matched_section
            if current_section not in sections:
                sections[current_section] = []
        else:
            if current_section not in sections:
                sections[current_section] = []
            sections[current_section].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_years_of_experience(text: str) -> float:
    """
    Estimate total years of experience from explicit mentions (e.g. '6+ years')
    or from date ranges (e.g. 2019 - Present, 2015 - 2018).
    """
    # 1. Check explicit mentions like '6+ years of experience' or '5 years experience'
    explicit = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:-\s*\d+\s*)?years?(?:\s+of)?(?:\s+experience)?", text, re.IGNORECASE)
    if explicit:
        years = [float(y) for y in explicit]
        # Return reasonable max (not outlier like year 2024)
        valid_years = [y for y in years if 0.5 <= y <= 40]
        if valid_years:
            return max(valid_years)

    # 2. Extract year spans like '2018 - 2022', '2020 - Present'
    current_year = datetime.now().year
    year_ranges = re.findall(r"\b(20\d\d|19\d\d)\s*(?:–|-|to)\s*(20\d\d|present|current)\b", text, re.IGNORECASE)
    total_span = 0.0
    seen_years = set()
    for start, end in year_ranges:
        start_y = int(start)
        end_y = current_year if end.lower() in ["present", "current"] else int(end)
        if start_y <= end_y <= current_year + 1 and (end_y - start_y) <= 30:
            for y in range(start_y, end_y):
                seen_years.add(y)
    
    if seen_years:
        total_span = float(len(seen_years))
        return total_span

    return 1.0


def extract_skills_from_text(text: str) -> List[Tuple[str, str, str]]:
    """
    Extract technical and domain skills by matching taxonomy canonicals and aliases.
    Returns list of (canonical_skill, original_mention, category).
    """
    extracted = {}
    lower_text = text.lower()

    for canonical, (category, aliases) in SKILL_TAXONOMY.items():
        all_terms = [canonical] + aliases
        for term in all_terms:
            pattern = rf"\b{re.escape(term.lower())}\b"
            match = re.search(pattern, lower_text)
            if match:
                if canonical not in extracted:
                    extracted[canonical] = (canonical, term, category)
                break

    return list(extracted.values())


def extract_bullet_points(section_text: str) -> List[str]:
    """Extract individual bullet points or meaningful lines."""
    bullets = []
    lines = section_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Strip bullet prefixes
        cleaned = re.sub(r"^[-*•\d\.\)\s]+", "", line).strip()
        if len(cleaned) > 10:
            bullets.append(cleaned)
    return bullets


def extract_resume_info(text: str) -> CandidateInfo:
    """Parse resume text into structured CandidateInfo without hallucination."""
    sections = extract_sections(text, RESUME_SECTIONS)
    
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    
    # Location detection
    loc_match = re.search(r"([A-Z][a-zA-Z\s]+,\s*[A-Z]{2}(?:\s+\d{5})?)", text)
    location = loc_match.group(1).strip() if loc_match else None

    # Education extraction
    edu_text = sections.get("education", "")
    education_lines = []
    for line in edu_text.split("\n"):
        line = line.strip()
        if any(deg in line.lower() for deg in ["bachelor", "master", "ph.d", "b.s", "m.s", "degree", "university", "college"]):
            education_lines.append(line)
    if not education_lines and edu_text:
        education_lines = [l.strip() for l in edu_text.split("\n") if len(l.strip()) > 10]

    # Experience extraction
    exp_text = sections.get("experience", "")
    years_exp = extract_years_of_experience(exp_text or text)
    exp_bullets = extract_bullet_points(exp_text)
    
    # Construct work experience items
    work_items = []
    for bullet in exp_bullets[:8]:
        work_items.append({"description": bullet})

    # Projects extraction
    proj_text = sections.get("projects", "")
    projects = extract_bullet_points(proj_text)

    # Certifications extraction
    cert_text = sections.get("certifications", "")
    certifications = extract_bullet_points(cert_text)

    # Skills extraction across skills section and full text
    skills_source = sections.get("skills", "") + "\n" + exp_text + "\n" + proj_text + "\n" + text
    extracted_skills = extract_skills_from_text(skills_source)

    # Categorize skills
    prog_langs = []
    frameworks = []
    databases = []
    cloud = []
    tools = []
    soft_skills = []
    all_tech = []

    for canon, orig, cat in extracted_skills:
        if cat == "Languages":
            prog_langs.append(canon)
            all_tech.append(canon)
        elif cat == "Frameworks":
            frameworks.append(canon)
            all_tech.append(canon)
        elif cat == "Databases":
            databases.append(canon)
            all_tech.append(canon)
        elif cat == "Cloud & DevOps":
            cloud.append(canon)
            all_tech.append(canon)
        elif cat in ["Tools", "AI & ML"]:
            tools.append(canon)
            all_tech.append(canon)
        elif cat == "Soft Skills":
            soft_skills.append(canon)
        else:
            all_tech.append(canon)

    return CandidateInfo(
        name=name,
        email=email,
        phone=phone,
        location=location,
        education=education_lines,
        work_experience=work_items,
        estimated_years_experience=years_exp,
        technical_skills=sorted(list(set(all_tech))),
        soft_skills=sorted(list(set(soft_skills))),
        certifications=certifications,
        projects=projects,
        programming_languages=sorted(list(set(prog_langs))),
        frameworks=sorted(list(set(frameworks))),
        databases=sorted(list(set(databases))),
        cloud_technologies=sorted(list(set(cloud))),
        tools=sorted(list(set(tools)))
    )


def extract_job_info(text: str) -> JobInfo:
    """Parse job description text into structured JobInfo."""
    sections = extract_sections(text, JD_SECTIONS)
    
    # Title extraction
    title = "Target Position"
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    title_match = re.search(r"(?:job\s+title|role|position)[:\s]+([^\n]+)", text, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    elif lines:
        for line in lines[:3]:
            if any(term in line.lower() for term in ["engineer", "developer", "architect", "lead", "scientist", "manager"]):
                title = line.strip("#-* ")
                break

    # Company extraction
    company = None
    comp_match = re.search(r"(?:company|organization|at\s+)([A-Z][a-zA-Z0-9\s]+)", text)
    if comp_match:
        company = comp_match.group(1).strip()

    # Experience extraction
    req_exp = extract_years_of_experience(sections.get("required", "") or text)

    # Responsibilities
    resp_text = sections.get("responsibilities", "")
    responsibilities = extract_bullet_points(resp_text)

    # Required Skills
    req_text = sections.get("required", "")
    if not req_text:
        # Fallback to general text if no explicit required section
        req_text = text
    req_skills_tuples = extract_skills_from_text(req_text)
    required_skills = sorted(list(set(c for c, _, _ in req_skills_tuples)))

    # Preferred Skills
    pref_text = sections.get("preferred", "")
    pref_skills_tuples = extract_skills_from_text(pref_text)
    preferred_skills = sorted(list(set(c for c, _, _ in pref_skills_tuples if c not in required_skills)))

    # If preferred section had nothing but required has skills, ensure reasonable split
    if not preferred_skills and len(required_skills) > 6:
        # Keep top skills required, move lower to preferred
        split_point = int(len(required_skills) * 0.7)
        preferred_skills = required_skills[split_point:]
        required_skills = required_skills[:split_point]

    # Education requirements
    edu_reqs = []
    for line in text.split("\n"):
        line_clean = line.strip().lower()
        if any(term in line_clean for term in ["bachelor", "master", "ph.d", "degree in computer science"]):
            edu_reqs.append(line.strip())

    return JobInfo(
        title=title,
        company=company,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        required_experience_years=req_exp,
        preferred_experience_years=max(req_exp, req_exp + 1),
        education_requirements=edu_reqs[:3],
        responsibilities=responsibilities[:6],
        technologies=required_skills + preferred_skills
    )
