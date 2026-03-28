from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import PROCESSED_DIR, RAW_DATA_DIR
from src.data.hf_sources import HF_SOURCES
from src.data.io import read_table, write_parquet
from src.data.normalize import coalesce_skills, coalesce_text, normalize_text, safe_slug
from src.reasoning.skill_cleanup import clean_skill_list


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize downloaded HF datasets into SkillSpace schema.")
    parser.add_argument(
        "--source",
        choices=["jobs", "resumes", "all"],
        default="all",
        help="Which configured source to preprocess.",
    )
    return parser.parse_args()


def normalize_jobs(df: pd.DataFrame, field_map: dict[str, list[str]]) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for idx, row in df.iterrows():
        title = coalesce_text(row, field_map["title"])
        description = coalesce_text(row, field_map["description"])
        if not title and not description:
            continue
        record = {
            "job_id": coalesce_text(row, field_map["job_id"]) or safe_slug("job", idx),
            "title": title,
            "description": description,
            "skills_raw": clean_skill_list(coalesce_skills(row, field_map["skills_raw"])),
            "domain": coalesce_text(row, field_map["domain"]) or None,
            "location": coalesce_text(row, field_map["location"]) or None,
        }
        record["retrieval_text"] = normalize_text(f"{record['title']}. {record['description']}")
        records.append(record)
    return pd.DataFrame(records)


def flatten_resume_text(row: pd.Series) -> str:
    parts: list[str] = []

    personal_info = row.get("personal_info")
    if isinstance(personal_info, dict):
        summary = normalize_text(personal_info.get("summary"))
        if summary and summary.lower() != "unknown":
            parts.append(summary)

    experience = row.get("experience")
    if experience is not None:
        for item in list(experience):
            if isinstance(item, dict):
                title = normalize_text(item.get("title"))
                if title and title.lower() != "unknown":
                    parts.append(title)
                responsibilities = item.get("responsibilities")
                if responsibilities is not None:
                    parts.extend(
                        normalize_text(resp)
                        for resp in list(responsibilities)
                        if normalize_text(resp) and normalize_text(resp).lower() != "unknown"
                    )

    projects = row.get("projects")
    if projects is not None:
        for item in list(projects):
            if isinstance(item, dict):
                description = normalize_text(item.get("description"))
                if description and description.lower() != "unknown":
                    parts.append(description)

    return " ".join(parts).strip()


def flatten_resume_skills(row: pd.Series) -> list[str]:
    extracted: list[str] = []
    skills = row.get("skills")
    if not isinstance(skills, dict):
        return extracted

    technical = skills.get("technical")
    if isinstance(technical, dict):
        for value in technical.values():
            if value is None:
                continue
            for item in list(value):
                if isinstance(item, dict):
                    name = normalize_text(item.get("name"))
                    if name and name.lower() != "unknown":
                        extracted.append(name)
                else:
                    name = normalize_text(item)
                    if name and name.lower() != "unknown":
                        extracted.append(name)

    languages = skills.get("languages")
    if languages is not None:
        for item in list(languages):
            if isinstance(item, dict):
                name = normalize_text(item.get("name"))
                if name and name.lower() != "unknown":
                    extracted.append(name)

    return sorted(set(extracted))


def normalize_resumes(df: pd.DataFrame, field_map: dict[str, list[str]]) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    for idx, row in df.iterrows():
        raw_text = coalesce_text(row, field_map["raw_text"]) or flatten_resume_text(row)
        if not raw_text:
            continue
        skills = clean_skill_list(coalesce_skills(row, field_map["skills_raw"]) or flatten_resume_skills(row))
        records.append(
            {
                "resume_id": coalesce_text(row, field_map["resume_id"]) or safe_slug("resume", idx),
                "raw_text": raw_text,
                "skills_raw": skills,
                "target_domain": coalesce_text(row, field_map["target_domain"]) or None,
            }
        )
    return pd.DataFrame(records)


def preprocess_source(source_key: str) -> None:
    source = HF_SOURCES[source_key]
    raw_path = RAW_DATA_DIR / source_key / "raw.parquet"
    df = read_table(raw_path)
    field_map = source["field_map"]
    if source["canonical_type"] == "jobs":
        processed = normalize_jobs(df, field_map)
        output_path = PROCESSED_DIR / "jobs_hf_v1.parquet"
    else:
        processed = normalize_resumes(df, field_map)
        output_path = PROCESSED_DIR / "resumes_hf_v1.parquet"

    write_parquet(processed, output_path)
    print(f"Wrote {len(processed)} rows to {output_path}")


def main() -> None:
    args = parse_args()
    targets = HF_SOURCES.keys() if args.source == "all" else [args.source]
    for source_key in targets:
        preprocess_source(source_key)


if __name__ == "__main__":
    main()
