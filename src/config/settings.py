from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
DATA_DIR = ARTIFACTS_DIR / "sample_data"
RAW_DATA_DIR = ARTIFACTS_DIR / "raw"
PROCESSED_DIR = ARTIFACTS_DIR / "processed"
EMBEDDINGS_DIR = ARTIFACTS_DIR / "embeddings"
INDEX_DIR = ARTIFACTS_DIR / "index"

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
HF_JOBS_PREFIX = "jobs_hf_v1"
