from pathlib import Path
import argparse
import sys

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import EMBEDDINGS_DIR, INDEX_DIR
from src.retrieval.index import build_index, save_index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a FAISS index from job embeddings.")
    parser.add_argument(
        "--input",
        default=str(EMBEDDINGS_DIR / "jobs_v1.npy"),
        help="Input embeddings .npy path.",
    )
    parser.add_argument(
        "--output",
        default=str(INDEX_DIR / "jobs_v1.faiss"),
        help="Output FAISS index path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    embeddings_path = Path(args.input)
    vectors = np.load(embeddings_path)
    index = build_index(vectors)
    save_index(index, Path(args.output))
    print(f"FAISS index created at {args.output}")


if __name__ == "__main__":
    main()
