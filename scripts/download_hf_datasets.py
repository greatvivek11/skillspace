from __future__ import annotations

import argparse
from pathlib import Path
import sys

from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import RAW_DATA_DIR
from src.data.hf_sources import HF_SOURCES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download public HF datasets for SkillSpace.")
    parser.add_argument(
        "--source",
        choices=["jobs", "resumes", "all"],
        default="all",
        help="Which configured source to download.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Optional row limit per dataset to keep local experiments lightweight.",
    )
    return parser.parse_args()


def download_source(source_key: str, limit: int) -> None:
    source = HF_SOURCES[source_key]
    dataset_name = str(source["dataset_name"])
    split = str(source["split"])
    dataset = load_dataset(dataset_name, split=split)
    if limit > 0:
        dataset = dataset.select(range(min(limit, len(dataset))))

    output_dir = RAW_DATA_DIR / source_key
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "raw.parquet"
    dataset.to_parquet(str(output_path))
    print(f"Downloaded {source_key} dataset to {output_path}")


def main() -> None:
    args = parse_args()
    targets = HF_SOURCES.keys() if args.source == "all" else [args.source]
    for source_key in targets:
        download_source(source_key, args.limit)


if __name__ == "__main__":
    main()
