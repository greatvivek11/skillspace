from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import DEFAULT_EMBEDDING_MODEL, PROCESSED_DIR
from src.data.io import read_table
from src.embeddings.encoder import load_encoder
from src.reasoning.skill_cleanup import clean_skill_list
from src.retrieval.index import build_index
from src.retrieval.query import search_jobs_by_vector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate resume-to-job retrieval with Recall@K and MRR.")
    parser.add_argument("--jobs", default=str(PROCESSED_DIR / "jobs_hf_v1.parquet"))
    parser.add_argument("--resumes", default=str(PROCESSED_DIR / "resumes_hf_v1.parquet"))
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--min-shared-skills", type=int, default=1)
    return parser.parse_args()


def recall_at_k(ranks: list[int | None], k: int) -> float:
    hits = sum(1 for rank in ranks if rank is not None and rank <= k)
    return hits / len(ranks) if ranks else 0.0


def mean_reciprocal_rank(ranks: list[int | None]) -> float:
    scores = [(1.0 / rank) if rank else 0.0 for rank in ranks]
    return sum(scores) / len(scores) if scores else 0.0


def main() -> None:
    args = parse_args()
    jobs_df = read_table(Path(args.jobs))
    resumes_df = read_table(Path(args.resumes)).head(args.limit).copy()

    if "retrieval_text" not in jobs_df.columns:
        jobs_df["retrieval_text"] = jobs_df["title"].fillna("") + ". " + jobs_df["description"].fillna("")

    encoder = load_encoder(DEFAULT_EMBEDDING_MODEL)
    job_vectors = encoder.encode(
        jobs_df["retrieval_text"].fillna("").tolist(),
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    index = build_index(job_vectors)

    ranks: list[int | None] = []
    evaluated = 0

    for _, resume in resumes_df.iterrows():
        raw_resume_skills = resume.get("skills_raw", [])
        if hasattr(raw_resume_skills, "tolist"):
            raw_resume_skills = raw_resume_skills.tolist()
        elif not isinstance(raw_resume_skills, list):
            raw_resume_skills = [raw_resume_skills] if raw_resume_skills else []

        resume_skills = set(clean_skill_list(list(raw_resume_skills)))
        if not resume_skills:
            continue
        evaluated += 1
        query_vector = encoder.encode(
            [str(resume.get("raw_text", ""))],
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        results = search_jobs_by_vector(query_vector, index, jobs_df, top_k=args.top_k)
        rank = None
        for idx, row in enumerate(results.itertuples(index=False), start=1):
            job_skills = getattr(row, "skills_raw", [])
            if hasattr(job_skills, "tolist"):
                job_skills = job_skills.tolist()
            elif not isinstance(job_skills, list):
                job_skills = [job_skills] if job_skills else []
            overlap = resume_skills.intersection(clean_skill_list(list(job_skills)))
            if len(overlap) >= args.min_shared_skills:
                rank = idx
                break
        ranks.append(rank)

    metrics = {
        "evaluated_resumes": evaluated,
        f"recall@{args.top_k}": round(recall_at_k(ranks, args.top_k), 4),
        "mrr": round(mean_reciprocal_rank(ranks), 4),
        "relevance_rule": f"at least {args.min_shared_skills} shared skill(s)",
    }
    print(metrics)


if __name__ == "__main__":
    main()
