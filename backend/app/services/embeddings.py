import logging
from typing import List, Union
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Singleton service for generating dense text embeddings and computing
    cosine similarity metrics using SentenceTransformers.
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        try:
            logger.info(f"Loading SentenceTransformer model: {settings.EMBEDDING_MODEL_NAME}")
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            logger.info("SentenceTransformer model successfully loaded.")
        except Exception as e:
            logger.error(f"Error loading SentenceTransformer: {e}")
            self._model = None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding vector for a single string."""
        if not text or not text.strip():
            return np.zeros((384,), dtype=np.float32)
        if self._model is None:
            self._initialize_model()
        
        vec = self._model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return vec

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Batch generate embeddings for a list of strings."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)
        if self._model is None:
            self._initialize_model()
            
        embeddings = self._model.encode(
            texts, 
            batch_size=32, 
            convert_to_numpy=True, 
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two text strings."""
        if not text1.strip() or not text2.strip():
            return 0.0
        v1 = self.get_embedding(text1).reshape(1, -1)
        v2 = self.get_embedding(text2).reshape(1, -1)
        sim = float(cosine_similarity(v1, v2)[0][0])
        return max(0.0, min(1.0, sim))

    def compute_similarity_matrix(self, texts1: List[str], texts2: List[str]) -> np.ndarray:
        """
        Compute pairwise cosine similarity matrix between two text lists.
        Output shape: (len(texts1), len(texts2))
        """
        if not texts1 or not texts2:
            return np.zeros((len(texts1), len(texts2)))
        e1 = self.get_embeddings(texts1)
        e2 = self.get_embeddings(texts2)
        sim_matrix = cosine_similarity(e1, e2)
        return np.clip(sim_matrix, 0.0, 1.0)


# Global instance
embedding_service = EmbeddingService()
