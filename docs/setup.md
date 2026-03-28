# SkillSpace Setup Notes

## Phase 1 Model Choice

Use a compact encoder-only embedding model:

- `sentence-transformers/all-MiniLM-L6-v2`

Why this model:

- strong semantic search baseline
- small enough for local development and HF Spaces CPU hosting
- easy to fine-tune later for resume-to-job retrieval

## Dataset Strategy

Phase 1 uses two layers of data:

1. tiny hand-authored sample data for local pipeline development
2. public Hugging Face datasets for larger experiments

Configured public sources:

- jobs: `NxtGenIntern/job_titles_and_descriptions`
- resumes: `datasetmaster/resumes`

These are treated as input sources, not as the final project dataset contract.
We normalize them into SkillSpace-owned canonical parquet files under `artifacts/processed/`.

## Local Workflow

1. Install dependencies from `requirements.txt`
2. Run `python3 scripts/preprocess_sample_data.py`
3. Optionally run `python3 scripts/download_hf_datasets.py --source all --limit 1000`
4. Run `python3 scripts/preprocess_hf_data.py --source all`
5. Run `python3 scripts/embed_jobs.py --input artifacts/processed/jobs_hf_v1.parquet --prefix jobs_hf_v1`
6. Run `python3 scripts/build_index.py --input artifacts/embeddings/jobs_hf_v1.npy --output artifacts/index/jobs_hf_v1.faiss`
7. Run `SKILLSPACE_HF_LOCAL_ONLY=1 python3 -m src.ui.app`

If the HF processed dataset and prebuilt index artifacts exist, the app will automatically prefer `hf` mode by default.

## Cross-Machine Plan

Use the same repo structure on macOS and Windows.

- MacBook: development, preprocessing, small test runs
- Windows desktop: larger embedding runs and later fine-tuning

Keep these out of git:

- raw datasets
- embedding matrices
- FAISS indexes
- model checkpoints

## Hugging Face Authentication

You do not need a token for public model and dataset downloads.

You will want a token later for:

- pushing the fine-tuned model to your own HF model repo
- pushing a cleaned dataset to your own HF dataset repo
- managing a private Space or private artifacts

## Hugging Face Space Layout

Recommended repo split for publishing:

1. Space repo
   - `app.py`
   - `src/`
   - lightweight runtime artifacts or startup download logic
   - `requirements-space.txt`
2. Model repo
   - fine-tuned sentence-transformer checkpoint
3. Dataset repo
   - cleaned, documented dataset slices for SkillSpace

For a first deployment, keep the Space simple:

- use prebuilt FAISS artifacts
- avoid training code in the Space runtime
- keep the app on CPU
- use `requirements-space.txt` instead of the broader local dev requirements when possible
