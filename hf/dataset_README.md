---
pretty_name: SkillSpace Data
language:
- en
license: mit
task_categories:
- text-retrieval
- text-classification
tags:
- resumes
- jobs
- semantic-search
- retrieval
- careers
size_categories:
- n<1K
---

# SkillSpace Data

This dataset repo stores the cleaned Phase 1 artifacts used by SkillSpace.

## Contents

- `processed/jobs_hf_v1.parquet`
- `processed/resumes_hf_v1.parquet`
- `sample_data/skills_seed.csv`
- `sample_data/jobs_sample.csv`
- `sample_data/resumes_sample.csv`

## Purpose

These artifacts support:

- semantic resume-to-job retrieval
- deterministic skill-gap reasoning
- Gradio demo evaluation and iteration

## Provenance

The cleaned artifacts were derived locally from public Hugging Face source datasets and normalized into a project-owned schema for Phase 1 development.

## Notes

- This is an evolving project dataset, not a final benchmark release.
- Future versions may expand rows, improve normalization, and add evaluation splits.
