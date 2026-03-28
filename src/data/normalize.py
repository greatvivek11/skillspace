from __future__ import annotations

from typing import Iterable

import pandas as pd


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\n", " ").split())


def split_pipe_skills(value: object) -> list[str]:
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [item.strip() for item in text.split("|") if item.strip()]


def coalesce_text(row: pd.Series, candidates: Iterable[str]) -> str:
    for key in candidates:
        if key in row and pd.notna(row[key]):
            text = normalize_text(row[key])
            if text:
                return text
    return ""


def coalesce_skills(row: pd.Series, candidates: Iterable[str]) -> list[str]:
    for key in candidates:
        if key in row and pd.notna(row[key]):
            value = row[key]
            if isinstance(value, list):
                return [normalize_text(item) for item in value if normalize_text(item)]
            if isinstance(value, str):
                text = value.strip()
                if not text:
                    continue
                if "|" in text:
                    return split_pipe_skills(text)
                if "," in text:
                    return [item.strip() for item in text.split(",") if item.strip()]
                return [text]
    return []


def safe_slug(prefix: str, index: int) -> str:
    return f"{prefix}_{index:05d}"
