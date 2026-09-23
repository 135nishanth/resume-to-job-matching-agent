import pytest
from backend.app.services.skill_normalizer import (
    normalize_skill,
    get_related_skills,
    are_skills_related
)


def test_normalize_exact_and_aliases():
    # React variants
    skill, cat = normalize_skill("React.js")
    assert skill == "React"
    assert cat == "Frameworks"

    skill, cat = normalize_skill("ReactJS")
    assert skill == "React"

    # Python variants
    skill, cat = normalize_skill("Python programming")
    assert skill == "Python"
    assert cat == "Languages"

    # REST API variants
    skill, cat = normalize_skill("RESTful APIs")
    assert skill == "REST API"

    skill, cat = normalize_skill("RESTful API development")
    assert skill == "REST API"

    # PostgreSQL variants
    skill, cat = normalize_skill("Postgres")
    assert skill == "PostgreSQL"
    assert cat == "Databases"

    # Machine Learning variants
    skill, cat = normalize_skill("ML")
    assert skill == "Machine Learning"
    assert cat == "AI & ML"

    # Kubernetes variants
    skill, cat = normalize_skill("k8s")
    assert skill == "Kubernetes"
    assert cat == "Cloud & DevOps"


def test_related_skills_clustering():
    # PostgreSQL should be in relational cluster with SQL and MySQL
    assert are_skills_related("PostgreSQL", "Relational Database")
    assert are_skills_related("PostgreSQL", "MySQL")
    assert are_skills_related("React", "TypeScript")
    assert are_skills_related("Docker", "Kubernetes")

    # Unrelated skills should not be clustered
    assert not are_skills_related("PostgreSQL", "React")
    assert not are_skills_related("Figma", "Docker")


def test_fallback_normalization():
    skill, cat = normalize_skill("Quantum Computing Engine")
    assert skill == "Quantum Computing Engine"
    assert cat in ["Technical", "Other"]
