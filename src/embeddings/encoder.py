import os

from sentence_transformers import SentenceTransformer

from src.config.settings import DEFAULT_EMBEDDING_MODEL


def load_encoder(model_name: str = DEFAULT_EMBEDDING_MODEL) -> SentenceTransformer:
    local_only = os.getenv("SKILLSPACE_HF_LOCAL_ONLY", "0").strip() == "1"
    try:
        return SentenceTransformer(model_name, local_files_only=local_only)
    except TypeError:
        return SentenceTransformer(model_name)


def encode_texts(
    texts: list[str],
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 32,
):
    encoder = load_encoder(model_name)
    vectors = encoder.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True,
    )
    return vectors
