from __future__ import annotations

HF_SOURCES: dict[str, dict[str, object]] = {
    "jobs": {
        "dataset_name": "NxtGenIntern/job_titles_and_descriptions",
        "split": "train",
        "canonical_type": "jobs",
        "field_map": {
            "job_id": ["job_id", "id"],
            "title": ["job_title", "title", "role", "Job Title"],
            "description": ["job_description", "description", "Job Description"],
            "skills_raw": ["skills", "required_skills", "Skills"],
            "domain": ["category", "domain"],
            "location": ["location"],
        },
    },
    "resumes": {
        "dataset_name": "datasetmaster/resumes",
        "split": "train",
        "canonical_type": "resumes",
        "field_map": {
            "resume_id": ["resume_id", "id"],
            "raw_text": ["Resume_test", "resume_text", "text", "resume"],
            "skills_raw": ["skills", "Skills"],
            "target_domain": ["Category", "category", "target_domain"],
        },
    },
}
