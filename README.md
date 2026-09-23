# Intelligent Resume-to-Job Matching Agent

> An AI-powered full-stack application that analyzes candidate resumes against job descriptions, extracts skills and experience, understands semantic relationships between qualifications, calculates an explainable compatibility score (0–100), detects missing skills, and provides grounded matching reports.

---

## 🚀 Key Features

* **Multi-Format Document Parsing**: Ingests resumes in **PDF**, **DOCX**, and **TXT** formats, as well as pasted or uploaded Job Descriptions.
* **Semantic Skill Normalization**: Beyond keywords — maps abbreviations, aliases, and related concepts (`"React.js"` → `"React"`, `"RESTful APIs"` → `"REST API"`, `"ML"` → `"Machine Learning"`, `"PostgreSQL"` → relational database).
* **Local Sentence Transformers Embeddings**: Generates dense 384-dimensional embeddings using `all-MiniLM-L6-v2` for genuine cosine similarity matching.
* **Multi-Tiered Classification**:
  - `EXACT MATCH`: Direct canonical or verbatim match.
  - `SEMANTIC MATCH`: High conceptual alignment with candidate evidence quotes.
  - `MISSING`: Categorized into **Critical Missing (Required)** vs. **Nice-to-Have (Preferred)**.
* **Transparent 5-Dimension Scoring Engine**:
  - Required Skills: **50%**
  - Preferred Skills: **15%**
  - Experience Match: **20%**
  - Education & Certifications: **5%**
  - Projects & Domain Relevance: **10%**
* **Explainable AI Reasoning Report**: Objective narrative summary, evidence quotes from the resume, experience evaluation, and actionable recruiter interview recommendations.
* **Modern SaaS Recruitment Dashboard**: Built with React, TypeScript, Tailwind CSS, Recharts, and SQLite history persistence.

---

## 🛠️ Tech Stack

* **Frontend**: React 19, TypeScript, Tailwind CSS v4, Lucide React, Recharts, Vite
* **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy ORM, SQLite
* **AI & NLP**: `sentence-transformers` (`all-MiniLM-L6-v2`), PyTorch, Scikit-learn, NumPy
* **Document Processing**: `pypdf`, `python-docx`
* **Testing**: Pytest (12 automated unit tests across normalization, embeddings, matching, and scoring)

---

## 📂 Project Structure

```
resume-to-job-matching-agent/
├── backend/
│   ├── app/
│   │   ├── api/             # REST endpoints (/analyze, /health, /history, /samples)
│   │   ├── core/            # Configurable weights, thresholds, database setup
│   │   ├── models/          # SQLAlchemy SQLite models
│   │   ├── schemas/         # Typed Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── parser.py            # PDF / DOCX / TXT document parsing
│   │   │   ├── extractor.py         # Entity & experience extraction
│   │   │   ├── skill_normalizer.py  # Canonical taxonomy & aliases
│   │   │   ├── embeddings.py        # SentenceTransformers embeddings singleton
│   │   │   ├── matcher.py           # Exact, semantic, and missing skill matching
│   │   │   ├── scorer.py            # Transparent weighted score calculation
│   │   │   └── explainer.py         # Grounded evidence reasoning engine
│   │   └── main.py          # FastAPI application & CORS
│   ├── tests/               # Pytest suite
│   ├── requirements.txt
│   └── run.py               # Backend startup script
├── frontend/
│   ├── src/
│   │   ├── components/      # ScoreGauge, StatCards, BreakdownChart, MatchTable, etc.
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # Main dashboard
│   │   └── index.css        # Tailwind styling & Google Fonts
│   └── package.json
├── data/
│   ├── sample_resumes/      # Pre-packaged test resumes
│   └── sample_job_descriptions/ # Pre-packaged test JDs
└── README.md
```

---

## 🏁 Getting Started

### 1. Backend Setup

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run backend server
python run.py
```
* Backend API: `http://localhost:8000`
* Interactive API Docs (Swagger): `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
* Dashboard URL: `http://localhost:5173`

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
./backend/venv/bin/pytest -v
```

All 12 unit tests validate:
- Skill normalization & alias resolution (`test_skill_normalizer.py`)
- Sentence Transformers cosine similarity & semantic matching (`test_embeddings_matcher.py`)
- Transparent scoring bounds, weights, and penalty calculations (`test_scorer.py`)
- Document parsing and non-hallucinated extraction (`test_parser_extractor.py`)