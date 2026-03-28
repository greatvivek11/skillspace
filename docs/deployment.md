# SkillSpace Deployment Notes

## Goal

Publish SkillSpace as a shareable Hugging Face Space backed by:

- a public Gradio app
- a public model repo for the embedding model or fine-tuned checkpoint
- a public dataset repo for cleaned SkillSpace data artifacts

## Suggested Publishing Structure

### 1. Space Repo

Include:

- `app.py`
- `src/`
- `requirements-space.txt`
- small demo-safe artifacts or startup download hooks

Use this for:

- UI
- online resume inference
- loading prebuilt job index artifacts

### 2. Model Repo

Include:

- baseline or fine-tuned sentence-transformer model
- model card
- evaluation snapshot

### 3. Dataset Repo

Include:

- cleaned job and resume parquet files or representative subsets
- schema description
- provenance and license notes

## Runtime Defaults

The app now behaves like this:

- if HF processed data and prebuilt index artifacts exist, default to `hf` mode
- otherwise default to `sample` mode
- if `SKILLSPACE_RUNTIME_MODE` is set, that explicit value wins

## Recommended Space Startup

For the first public version:

1. commit the app code
2. use `requirements-space.txt`
3. include or download the prebuilt FAISS index and job id mapping
4. keep inference encoder-only and CPU-friendly

## Pre-Publish Checklist

- verify `python3 -m src.ui.app` works locally
- verify `SKILLSPACE_HF_LOCAL_ONLY=1` works from cache
- verify `hf` mode reports `prebuilt artifact`
- capture one evaluation snapshot from `scripts/evaluate_retrieval.py`
- add screenshots and an app link to your website/resume after publishing
