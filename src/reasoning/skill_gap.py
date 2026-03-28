from src.reasoning.skill_cleanup import clean_skill_list


def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


def compute_skill_gap(resume_skills: list[str], job_skills: list[str]) -> list[str]:
    resume_set = {normalize_skill(skill) for skill in clean_skill_list(resume_skills)}
    job_set = {normalize_skill(skill) for skill in clean_skill_list(job_skills)}
    return sorted(job_set - resume_set)
