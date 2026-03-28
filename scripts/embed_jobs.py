from pathlib import Path
import argparse
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import DEFAULT_EMBEDDING_MODEL, EMBEDDINGS_DIR, PROCESSED_DIR
from src.data.io import read_table, write_json
from src.embeddings.encoder import encode_texts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Embed processed SkillSpace job records.")
    parser.add_argument(
        "--input",
        default=str(PROCESSED_DIR / "jobs_v1.parquet"),
        help="Processed jobs parquet path.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="Sentence transformer model name.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for embedding generation.",
    )
    parser.add_argument(
        "--prefix",
        default="jobs_v1",
        help="Artifact output prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    jobs_df = read_table(Path(args.input))
    if "retrieval_text" not in jobs_df.columns:
        jobs_df["retrieval_text"] = jobs_df["title"].fillna("") + ". " + jobs_df["description"].fillna("")

    texts = jobs_df["retrieval_text"].fillna("").tolist()
    vectors = encode_texts(texts, model_name=args.model, batch_size=args.batch_size)

    vectors_path = EMBEDDINGS_DIR / f"{args.prefix}.npy"
    ids_path = EMBEDDINGS_DIR / f"{args.prefix}_ids.json"
    meta_path = EMBEDDINGS_DIR / f"{args.prefix}_meta.json"

    np.save(vectors_path, np.asarray(vectors, dtype="float32"))
    write_json(jobs_df["job_id"].tolist(), ids_path)
    write_json({"model": args.model, "rows": len(jobs_df)}, meta_path)
    print(f"Wrote embeddings to {vectors_path}")
    print(f"Wrote id mapping to {ids_path}")


if __name__ == "__main__":
    main()
