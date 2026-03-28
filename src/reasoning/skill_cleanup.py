from __future__ import annotations

import re


NOISE_TOKENS = {
    "unknown",
    "n/a",
    "na",
    "none",
    "null",
}

SKILL_REPLACEMENTS = {
    "web frameworks django": "django",
    "web frameworks flask": "flask",
    "web frameworks django flask": "django, flask",
    "data analysis scripting": "data analysis",
    "project management tools": "project management",
}


def clean_skill_text(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[\[\]\{\}]", " ", text)
    text = re.sub(r"[()/]+", " ", text)
    text = re.sub(r"[^a-z0-9+.#&,\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" ,.-")
    text = SKILL_REPLACEMENTS.get(text, text)
    return text.strip(" ,.-")


def split_skill_string(value: str) -> list[str]:
    text = value.replace("|", ",")
    parts = re.split(r",|;|\band\b", text)
    cleaned = []
    for part in parts:
        item = clean_skill_text(part)
        if item and item not in NOISE_TOKENS and len(item) > 1:
            cleaned.append(item)
    return cleaned


def clean_skill_list(skills: list[str]) -> list[str]:
    cleaned: list[str] = []
    for skill in skills:
        cleaned.extend(split_skill_string(skill))
    seen: set[str] = set()
    deduped: list[str] = []
    for skill in cleaned:
        if skill not in seen:
            seen.add(skill)
            deduped.append(skill)
    return deduped
