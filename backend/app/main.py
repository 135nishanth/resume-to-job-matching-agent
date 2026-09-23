import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.analyze import router as analyze_router
from backend.app.api.health import router as health_router
from backend.app.api.history import router as history_router
from backend.app.api.samples import router as samples_router
from backend.app.services.embeddings import embedding_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("resume_matcher")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)

    # Preload embedding model
    logger.info("Pre-warming Sentence Transformers model...")
    _ = embedding_service.is_loaded

    logger.info("Intelligent Resume-to-Job Matching Agent backend is ready!")
    yield
    logger.info("Shutting down backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade AI agent matching resumes against job descriptions beyond keyword matching.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development and local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router, prefix=settings.API_PREFIX, tags=["System"])
app.include_router(analyze_router, prefix=settings.API_PREFIX, tags=["Analysis"])
app.include_router(history_router, prefix=settings.API_PREFIX, tags=["History"])
app.include_router(samples_router, prefix=settings.API_PREFIX, tags=["Samples"])


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "docs_url": "/docs"
    }
