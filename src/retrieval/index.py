from pathlib import Path

import faiss
import numpy as np


def build_index(vectors: np.ndarray) -> faiss.IndexFlatIP:
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index


def save_index(index: faiss.IndexFlatIP, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(path))


def load_index(path: Path) -> faiss.Index:
    return faiss.read_index(str(path))
