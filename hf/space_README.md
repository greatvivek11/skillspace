---
title: SkillSpace Demo
emoji: 💼
colorFrom: blue
colorTo: green
sdk: gradio
python_version: "3.10"
app_file: app.py
suggested_hardware: cpu-basic
disable_embedding: false
---

# SkillSpace Demo

SkillSpace is a semantic resume-to-job matching demo built with:

- sentence-transformer embeddings
- FAISS retrieval
- deterministic skill-gap reasoning
- Gradio UI

## Runtime

This Space prefers prebuilt HF artifacts when they are available:

- processed jobs parquet
- FAISS index
- job id mapping

If those artifacts are missing, the app can still fall back to sample-mode behavior.

## Project Links

- Dataset repo: `greatvivek11/skillspace-data`
- Model repo: `greatvivek11/skillspace-encoder`
