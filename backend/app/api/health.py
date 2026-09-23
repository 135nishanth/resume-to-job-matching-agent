from fastapi import APIRouter
from backend.app.schemas.analysis import HealthResponse
from backend.app.services.embeddings import embedding_service
from backend.app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="healthy",
        model_loaded=embedding_service.is_loaded,
        model_name=settings.EMBEDDING_MODEL_NAME,
        version=settings.VERSION
    )
