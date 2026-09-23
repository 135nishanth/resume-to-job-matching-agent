import os
from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

SAMPLES_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data"))


@router.get("/samples")
def get_samples() -> Dict[str, List[Dict[str, str]]]:
    """Returns available sample profiles for instant demo loading."""
    resumes_dir = os.path.join(SAMPLES_BASE_DIR, "sample_resumes")
    jds_dir = os.path.join(SAMPLES_BASE_DIR, "sample_job_descriptions")

    resumes = []
    if os.path.exists(resumes_dir):
        for f in sorted(os.listdir(resumes_dir)):
            if f.endswith(".txt"):
                path = os.path.join(resumes_dir, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                title = f.replace(".txt", "").replace("_", " ").title()
                resumes.append({
                    "id": f,
                    "title": title,
                    "filename": f,
                    "content": content
                })

    job_descriptions = []
    if os.path.exists(jds_dir):
        for f in sorted(os.listdir(jds_dir)):
            if f.endswith(".txt"):
                path = os.path.join(jds_dir, f)
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                title = f.replace(".txt", "").replace("_", " ").title()
                job_descriptions.append({
                    "id": f,
                    "title": title,
                    "filename": f,
                    "content": content
                })

    return {
        "resumes": resumes,
        "job_descriptions": job_descriptions
    }
