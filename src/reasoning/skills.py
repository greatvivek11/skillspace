from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config.settings import DATA_DIR
from src.data.normalize import normalize_text
from src.reasoning.skill_cleanup import clean_skill_list


def load_skill_catalog(path: Path | None = None) -> pd.DataFrame:
    csv_path = path or (DATA_DIR / "skills_seed.csv")
    return pd.read_csv(csv_path)


def extract_skills(text: str, skill_catalog: pd.DataFrame) -> list[str]:
    normalized_text = normalize_text(text).lower()
    matches: list[str] = []

    for _, row in skill_catalog.iterrows():
        canonical = str(row["skill"]).strip().lower()
        aliases = [item.strip().lower() for item in str(row["aliases"]).split("|") if item.strip()]
        terms = [canonical, *aliases]
        if any(term and term in normalized_text for term in terms):
            matches.append(canonical)

    return clean_skill_list(sorted(set(matches)))
