from pydantic import BaseModel


class JobRecord(BaseModel):
    job_id: str
    title: str
    description: str
    skills_raw: list[str] = []
    domain: str | None = None
    location: str | None = None


class ResumeRecord(BaseModel):
    resume_id: str
    raw_text: str
    skills_raw: list[str] = []
    target_domain: str | None = None
