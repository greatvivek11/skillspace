from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import DATA_DIR, PROCESSED_DIR
from src.data.normalize import normalize_text, split_pipe_skills
from src.data.io import write_parquet


def preprocess_jobs(path: Path) -> pd.DataFrame:
    jobs = pd.read_csv(path)
    jobs["description"] = jobs["description"].map(normalize_text)
    jobs["skills_raw"] = jobs["skills_raw"].map(split_pipe_skills)
    jobs["retrieval_text"] = jobs["title"] + ". " + jobs["description"]
    return jobs


def preprocess_resumes(path: Path) -> pd.DataFrame:
    resumes = pd.read_csv(path)
    resumes["raw_text"] = resumes["raw_text"].map(normalize_text)
    resumes["skills_raw"] = resumes["skills_raw"].map(split_pipe_skills)
    return resumes


def main() -> None:
    jobs = preprocess_jobs(DATA_DIR / "jobs_sample.csv")
    resumes = preprocess_resumes(DATA_DIR / "resumes_sample.csv")

    write_parquet(jobs, PROCESSED_DIR / "jobs_v1.parquet")
    write_parquet(resumes, PROCESSED_DIR / "resumes_v1.parquet")

    print(f"Wrote {len(jobs)} jobs to {PROCESSED_DIR / 'jobs_v1.parquet'}")
    print(f"Wrote {len(resumes)} resumes to {PROCESSED_DIR / 'resumes_v1.parquet'}")


if __name__ == "__main__":
    main()
