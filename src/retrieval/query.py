import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def search_jobs(
    resume_text: str,
    encoder: SentenceTransformer,
    index,
    jobs_df: pd.DataFrame,
    top_k: int = 5,
) -> pd.DataFrame:
    top_k = max(1, min(top_k, len(jobs_df)))
    vector = encoder.encode([resume_text], normalize_embeddings=True)
    scores, indices = index.search(np.asarray(vector, dtype="float32"), top_k)
    results = jobs_df.iloc[indices[0]].copy()
    results["score"] = scores[0]
    return results


def search_jobs_by_vector(
    query_vector: np.ndarray,
    index,
    jobs_df: pd.DataFrame,
    top_k: int = 5,
) -> pd.DataFrame:
    top_k = max(1, min(top_k, len(jobs_df)))
    scores, indices = index.search(np.asarray(query_vector, dtype="float32"), top_k)
    results = jobs_df.iloc[indices[0]].copy()
    results["score"] = scores[0]
    return results
