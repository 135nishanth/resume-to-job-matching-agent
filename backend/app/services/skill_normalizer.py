import re
from typing import Dict, List, Optional, Tuple, Set


# Canonical skill -> (category, list of aliases/synonyms/variations)
SKILL_TAXONOMY: Dict[str, Tuple[str, List[str]]] = {
    # Programming Languages
    "Python": ("Languages", ["python", "python3", "python 3", "python programming", "core python"]),
    "JavaScript": ("Languages", ["javascript", "js", "ecmascript", "es6", "es6+", "vanilla javascript"]),
    "TypeScript": ("Languages", ["typescript", "ts"]),
    "Go": ("Languages", ["go", "golang", "go language"]),
    "Java": ("Languages", ["java", "core java", "java 8", "java 11", "java 17"]),
    "C++": ("Languages", ["c++", "cpp", "c plus plus"]),
    "C#": ("Languages", ["c#", "csharp", "c sharp", ".net c#"]),
    "Rust": ("Languages", ["rust", "rustlang"]),
    "Ruby": ("Languages", ["ruby", "ruby programming"]),
    "PHP": ("Languages", ["php", "php7", "php8"]),
    "Swift": ("Languages", ["swift", "swiftlang"]),
    "Kotlin": ("Languages", ["kotlin"]),
    "SQL": ("Languages", ["sql", "structured query language", "ansi sql"]),
    "R": ("Languages", ["r", "r programming", "r language"]),
    "Bash": ("Languages", ["bash", "shell", "shell scripting", "bash scripting", "zsh", "sh"]),

    # Frameworks & Libraries
    "React": ("Frameworks", ["react", "react.js", "reactjs", "react js", "react 18", "react 19"]),
    "Next.js": ("Frameworks", ["next.js", "nextjs", "next js", "next"]),
    "Vue.js": ("Frameworks", ["vue", "vue.js", "vuejs", "vue 3"]),
    "Angular": ("Frameworks", ["angular", "angularjs", "angular 2+"]),
    "Node.js": ("Frameworks", ["node", "node.js", "nodejs", "node js"]),
    "Express.js": ("Frameworks", ["express", "express.js", "expressjs"]),
    "FastAPI": ("Frameworks", ["fastapi", "fast-api", "fast api"]),
    "Flask": ("Frameworks", ["flask", "flask-restful"]),
    "Django": ("Frameworks", ["django", "django rest framework", "drf"]),
    "Spring Boot": ("Frameworks", ["spring boot", "springboot", "spring framework", "spring"]),
    "ASP.NET": ("Frameworks", ["asp.net", "asp.net core", ".net core", "dotnet core", ".net"]),
    "Ruby on Rails": ("Frameworks", ["ruby on rails", "rails", "ror"]),
    "Tailwind CSS": ("Frameworks", ["tailwind", "tailwind css", "tailwindcss", "tailwind-css"]),
    "Redux": ("Frameworks", ["redux", "redux toolkit", "rtk"]),
    "GraphQL": ("Frameworks", ["graphql", "apollo graphql", "graphql api"]),
    "REST API": ("Frameworks", [
        "rest api", "restful api", "rest apis", "restful apis", 
        "restful api development", "restful web services", "rest architecture", "rest"
    ]),
    "gRPC": ("Frameworks", ["grpc", "google rpc", "protobuf"]),
    "Recharts": ("Frameworks", ["recharts", "recharts library"]),
    "D3.js": ("Frameworks", ["d3", "d3.js", "d3js"]),

    # Databases
    "PostgreSQL": ("Databases", [
        "postgresql", "postgres", "pgsql", "postgres database", "psql"
    ]),
    "Relational Database": ("Databases", [
        "relational database", "rdbms", "relational databases", "sql database", 
        "relational database experience", "sql db"
    ]),
    "MySQL": ("Databases", ["mysql", "my sql", "mariadb"]),
    "SQLite": ("Databases", ["sqlite", "sqlite3"]),
    "MongoDB": ("Databases", ["mongodb", "mongo", "nosql mongodb"]),
    "Redis": ("Databases", ["redis", "redis cache", "redis key-value"]),
    "Elasticsearch": ("Databases", ["elasticsearch", "elastic search", "elk stack", "opensearch"]),
    "Cassandra": ("Databases", ["cassandra", "apache cassandra"]),
    "DynamoDB": ("Databases", ["dynamodb", "aws dynamodb"]),
    "Snowflake": ("Databases", ["snowflake", "snowflake data warehouse"]),
    "BigQuery": ("Databases", ["bigquery", "google bigquery", "gcp bigquery"]),

    # Cloud & DevOps
    "AWS": ("Cloud & DevOps", [
        "aws", "amazon web services", "amazon aws", "aws cloud", "aws ec2", "aws s3"
    ]),
    "Google Cloud Platform": ("Cloud & DevOps", [
        "google cloud platform", "gcp", "google cloud", "google cloud services"
    ]),
    "Azure": ("Cloud & DevOps", ["azure", "microsoft azure", "azure cloud"]),
    "Docker": ("Cloud & DevOps", ["docker", "docker containerization", "containerization", "docker containers"]),
    "Kubernetes": ("Cloud & DevOps", ["kubernetes", "k8s", "kube", "k8s orchestration"]),
    "Terraform": ("Cloud & DevOps", ["terraform", "hashicorp terraform", "iac terraform"]),
    "CI/CD": ("Cloud & DevOps", [
        "ci/cd", "ci cd", "continuous integration", "continuous deployment", 
        "github actions", "gitlab ci", "jenkins", "circleci"
    ]),
    "Linux": ("Cloud & DevOps", ["linux", "unix", "ubuntu", "debian", "centos", "redhat"]),
    "Microservices": ("Cloud & DevOps", [
        "microservices", "microservice architecture", "distributed systems", "service-oriented architecture"
    ]),

    # AI & Machine Learning
    "Machine Learning": ("AI & ML", [
        "machine learning", "ml", "machine-learning", "statistical learning", "predictive modeling"
    ]),
    "Deep Learning": ("AI & ML", ["deep learning", "dl", "neural networks", "deep neural networks"]),
    "Natural Language Processing": ("AI & ML", [
        "natural language processing", "nlp", "text mining", "text analytics"
    ]),
    "Large Language Models": ("AI & ML", [
        "large language models", "llm", "llms", "generative ai", "genai", "prompt engineering"
    ]),
    "PyTorch": ("AI & ML", ["pytorch", "torch", "py-torch"]),
    "TensorFlow": ("AI & ML", ["tensorflow", "tf", "keras"]),
    "Scikit-learn": ("AI & ML", ["scikit-learn", "sklearn", "scikit learn"]),
    "Hugging Face": ("AI & ML", ["hugging face", "huggingface", "transformers", "hugging face transformers"]),
    "Sentence Transformers": ("AI & ML", [
        "sentence transformers", "sentence-transformers", "vector embeddings", 
        "text embeddings", "semantic embeddings"
    ]),
    "Vector Database": ("AI & ML", [
        "vector database", "vector search", "vector db", "pinecone", "chroma", "weaviate", "qdrant", "pgvector"
    ]),
    "LangChain": ("AI & ML", ["langchain", "llamaindex", "llama-index"]),
    "Pandas": ("AI & ML", ["pandas", "dataframe"]),
    "NumPy": ("AI & ML", ["numpy", "scientific computing"]),
    "MLOps": ("AI & ML", ["mlops", "mlflow", "weights & biases", "wandb", "model monitoring"]),

    # Tools & Testing
    "Git": ("Tools", ["git", "version control", "github", "gitlab", "bitbucket"]),
    "Pytest": ("Tools", ["pytest", "unittest", "python testing", "automated testing"]),
    "Jest": ("Tools", ["jest", "vitest", "mocha", "chai", "frontend testing"]),
    "JIRA": ("Tools", ["jira", "confluence", "scrum tools"]),
    "Figma": ("Tools", ["figma", "ui design", "wireframing"]),

    # Soft Skills
    "Leadership": ("Soft Skills", ["leadership", "team leadership", "mentorship", "mentoring engineers"]),
    "Communication": ("Soft Skills", ["communication", "written communication", "verbal communication", "presentation skills"]),
    "Agile Methodology": ("Soft Skills", ["agile", "scrum", "kanban", "sprint planning", "agile development"]),
    "Problem Solving": ("Soft Skills", ["problem solving", "analytical thinking", "critical thinking", "troubleshooting"]),
    "Collaboration": ("Soft Skills", ["collaboration", "cross-functional collaboration", "team player", "teamwork"])
}

# Invert taxonomy into fast lookup: alias_lowercase -> (canonical_name, category)
ALIAS_LOOKUP: Dict[str, Tuple[str, str]] = {}
for canonical, (category, aliases) in SKILL_TAXONOMY.items():
    ALIAS_LOOKUP[canonical.lower()] = (canonical, category)
    for alias in aliases:
        ALIAS_LOOKUP[alias.lower()] = (canonical, category)

# Semantic relatedness clusters (for partial match / related skills detection)
RELATED_CLUSTERS: List[Set[str]] = [
    {"PostgreSQL", "Relational Database", "MySQL", "SQLite", "SQL"},
    {"React", "Next.js", "JavaScript", "TypeScript"},
    {"FastAPI", "Flask", "Django", "Python", "REST API"},
    {"AWS", "Google Cloud Platform", "Azure", "Cloud & DevOps"},
    {"Docker", "Kubernetes", "CI/CD"},
    {"Machine Learning", "Deep Learning", "Natural Language Processing", "Large Language Models", "PyTorch", "TensorFlow", "Scikit-learn"},
    {"Sentence Transformers", "Vector Database", "Large Language Models", "Natural Language Processing"},
    {"Tailwind CSS", "React", "Next.js", "D3.js", "Recharts"}
]


def clean_skill_string(s: str) -> str:
    """Strip punctuation and normalize string for comparison."""
    s = s.strip()
    s = re.sub(r"^[\-\*•\d\.\)\s]+", "", s)  # strip leading bullets/numbers
    s = re.sub(r"[\s,;]+$", "", s)           # strip trailing punctuation
    return s.strip()


def normalize_skill(raw_skill: str) -> Tuple[str, str]:
    """
    Normalizes a raw skill string into a canonical skill name and category.
    Returns: (canonical_name, category)
    Example:
      'React.js' -> ('React', 'Frameworks')
      'Postgres' -> ('PostgreSQL', 'Databases')
      'RESTful APIs' -> ('REST API', 'Frameworks')
      'ML' -> ('Machine Learning', 'AI & ML')
    """
    cleaned = clean_skill_string(raw_skill)
    lower = cleaned.lower()

    # 1. Direct alias lookup
    if lower in ALIAS_LOOKUP:
        return ALIAS_LOOKUP[lower]

    # 2. Check prefix/suffix patterns (e.g., "experience in React", "knowledge of Python")
    patterns = [
        r"^(?:strong\s+|proficient\s+in\s+|knowledge\s+of\s+|experience\s+with\s+|hands-on\s+|deep\s+understanding\s+of\s+)(.+)$",
        r"^(.+?)\s+(?:programming|development|framework|library|database|technology|cloud|services)$"
    ]
    for pattern in patterns:
        match = re.match(pattern, lower)
        if match:
            candidate = match.group(1).strip()
            if candidate in ALIAS_LOOKUP:
                return ALIAS_LOOKUP[candidate]

    # 3. Check substring matches for prominent canonical skills
    for canonical, (category, aliases) in SKILL_TAXONOMY.items():
        if canonical.lower() == lower:
            return canonical, category
        for alias in aliases:
            # Word boundary match
            if re.search(r"\b" + re.escape(alias) + r"\b", lower):
                return canonical, category

    # 4. Fallback: Title case cleaned string with 'Technical' or 'Other' category
    title_cased = cleaned.title() if len(cleaned) > 3 else cleaned.upper()
    return title_cased, "Technical"


def get_related_skills(canonical_skill: str) -> List[str]:
    """Return known related skills from defined domain clusters."""
    related = set()
    for cluster in RELATED_CLUSTERS:
        if canonical_skill in cluster:
            related.update(cluster - {canonical_skill})
    return sorted(list(related))


def are_skills_related(skill_a: str, skill_b: str) -> bool:
    """Check if two skills belong to the same domain cluster."""
    for cluster in RELATED_CLUSTERS:
        if skill_a in cluster and skill_b in cluster:
            return True
    return False
