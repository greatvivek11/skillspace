# SkillSpace Phase 1 Implementation Plan (3–4 Week MVP)

## Phase 1 Status Checklist

### Completed

- ✅ Working public Hugging Face Space deployed
- ✅ Public dataset repo created and populated
- ✅ Compact pretrained embedding baseline selected and implemented
- ✅ Job corpus preprocessing pipeline implemented
- ✅ Resume corpus preprocessing pipeline implemented
- ✅ FAISS retrieval pipeline implemented
- ✅ Deterministic skill extraction and skill-gap reasoning implemented
- ✅ Gradio app implemented with HR-facing demo flow
- ✅ Retrieval metrics script implemented with Recall@K and MRR
- ✅ Local and Space deployment paths documented

### Partially Complete / Optional Polish

- ✅ Resume input via pasted text
- ✅ Resume input via uploaded `.txt` file
- ✅ Export results as JSON
- ⬜ Debug/latency panel for interactive inspection
- ⬜ `docs/phase-1-results.md` metrics write-up

### Deferred To Phase 2

- ⬜ Custom tokenizer
- ⬜ From-scratch dual-encoder training
- ⬜ Neural reranker
- ⬜ Larger-scale fine-tuning on expanded curated data
- ⬜ Richer recruiter workflow features beyond matching + skill gaps

## 1) Phase 1 Goal

Ship a portfolio-ready vertical slice that works end-to-end:

1. Ingest resume text
2. Retrieve relevant jobs semantically
3. Show skill-gap insights with deterministic logic
4. Deploy a usable demo on Hugging Face Spaces

Primary success criteria:

- Working app URL (public or unlisted)
- Measurable retrieval metrics (Recall@K / MRR)
- Clean architecture and reproducible runbook

---

## 2) Scope Boundaries (Must-Have vs Defer)

### Must-Have (Phase 1)

- Pretrained embedding model baseline (no from-scratch pretraining)
- Job corpus preprocessing + FAISS index
- Resume → embedding → top-K job retrieval
- Simple skill extraction + gap computation
- Gradio UI with explainable outputs
- HF deployment with pinned dependencies

### Defer to Phase 2

- Custom tokenizer
- Full synthetic data curriculum
- From-scratch dual-encoder pretraining
- Neural reranker
- Advanced archetype manifold / trajectory simulation

---

## 3) Recommended Repository Layout

Create this structure first:

```text
skillspace/
  docs/
  src/
    config/
    data/
    embeddings/
    retrieval/
    reasoning/
    evaluation/
    ui/
  scripts/
  artifacts/
    sample_data/
  .env.example
  requirements.txt
  README.md
```

Conventions:

- Keep large artifacts out of git (`.gitignore`)
- Store only sample slices in `artifacts/sample_data/`
- Use YAML/JSON configs instead of hardcoding constants

---

## 4) Tooling and Environment Setup

## 4.1 Python environment

Recommended: Python 3.11.

Steps:

1. Create virtual environment
2. Install requirements
3. Verify torch/faiss/gradio imports

`requirements.txt` baseline:

- torch
- sentence-transformers
- faiss-cpu (or faiss-gpu on desktop)
- pandas
- numpy
- scikit-learn
- rapidfuzz
- gradio
- pydantic
- python-dotenv
- huggingface_hub

## 4.2 Device strategy

- Local dev/inference: CPU or Mac GPU where supported
- Bulk embedding/index build: desktop GPU box
- Deployment target: HF Spaces CPU runtime

---

## 5) Data Plan (Practical MVP)

## 5.1 Data sources

Use open datasets with clear licenses:

- Job postings dataset (primary)
- Resume/profile text dataset (secondary)

Start small:

- Jobs: 5k–20k rows
- Resumes/profiles: 500–3k rows for evaluation and demo examples

## 5.2 Data schema

Define canonical job fields:

- `job_id`
- `title`
- `description`
- `skills_raw`
- `domain`
- `location` (optional)

Define canonical resume fields:

- `resume_id`
- `raw_text`
- `skills_raw` (if available)
- `target_domain` (optional)

## 5.3 Preprocessing pipeline

Implement deterministic pipeline:

1. Normalize whitespace and punctuation
2. Remove boilerplate artifacts
3. Merge title + description into retrieval text field
4. Deduplicate near-duplicate jobs (fuzzy threshold)
5. Persist processed parquet/csv with version tag

Output contracts:

- `artifacts/processed/jobs_v1.parquet`
- `artifacts/processed/resumes_v1.parquet`

---

## 6) Embedding Baseline Implementation

## 6.1 Model selection

Choose one compact sentence embedding model from HF (well-known, widely used).

Selection criteria:

- Good semantic retrieval quality
- Fast CPU inference
- Stable community usage

## 6.2 Embedding scripts

Create scripts:

1. `scripts/embed_jobs.py`
2. `scripts/embed_resumes.py`

Implementation details:

- Batch encoding
- L2 normalization
- Save `.npy` vectors + id mapping JSON
- Log throughput and runtime

Artifacts:

- `artifacts/embeddings/jobs_v1.npy`
- `artifacts/embeddings/jobs_ids_v1.json`

---

## 7) Retrieval Layer (FAISS)

## 7.1 Index type

Phase 1 default: `IndexFlatIP` with normalized vectors (simple + reliable).

Optional later in Phase 1:

- IVF or HNSW if scale/latency needs tuning

## 7.2 Index build

Script: `scripts/build_index.py`

Steps:

1. Load job embeddings
2. Build FAISS index
3. Add embeddings in `job_id` order
4. Persist index to disk

Artifacts:

- `artifacts/index/jobs_v1.faiss`

## 7.3 Query flow

Module: `src/retrieval/query.py`

Steps:

1. Encode resume text
2. Search top-K (e.g., 20 or 50)
3. Join IDs back to metadata
4. Return scored candidates

---

## 8) Skill-Gap Reasoning (Deterministic v1)

## 8.1 Skill dictionary

Start with curated skills list (CSV/JSON):

- normalized skill token
- aliases/synonyms
- optional category

## 8.2 Extraction

Use rule-based matching with normalization:

1. Lowercase + normalize
2. Alias-to-canonical mapping
3. Deduplicate skills

## 8.3 Gap algorithm

For each candidate job:

- `missing = job_skills - resume_skills`
- Rank by simple priority rules:
  - frequency
  - category weight
  - co-occurrence heuristics

Return:

- top missing skills
- confidence explanation string

---

## 9) Evaluation Plan

## 9.1 Offline retrieval metrics

Implement `scripts/eval_retrieval.py`:

- Recall@5, Recall@10
- MRR@10
- nDCG@10 (optional)

Use a small labeled/heuristic benchmark split.

## 9.2 Product quality checks

Track:

- latency p50/p95
- obvious bad matches rate (manual sample audit)
- explanation consistency

Record results in `docs/phase-1-results.md`.

---

## 10) Gradio App Implementation

Create `src/ui/app.py` with sections:

1. Resume input (paste text/upload text file)
2. Top matches table
3. Skill-gap panel
4. Debug panel (scores/latency toggle)

UX requirements:

- deterministic output ordering
- clear error messages
- loading indicators
- export results as JSON

---

## 11) Hugging Face Integration (Step-by-Step)

## 11.1 HF account and access

1. Create/login to Hugging Face account
2. Generate an access token with write permission
3. Store token locally (`HF_TOKEN`) in `.env` (never commit)

## 11.2 Create repositories

Create:

- Model repo (if publishing tuned artifacts)
- Space repo (Gradio app)

## 11.3 Prepare Space files

At Space root, include:

- `app.py` (entrypoint)
- `requirements.txt`
- optional `README.md`
- any lightweight assets

If your project keeps `src/ui/app.py`, provide thin root `app.py` wrapper import.

## 11.4 Add HF secrets

In Space settings, add:

- `HF_TOKEN` (if needed for private pulls)
- any app config secrets

Do not hardcode secrets in code.

## 11.5 Runtime and hardware

- Start with CPU Basic
- Keep model/index sizes modest for cold start
- Load artifacts lazily on app start

## 11.6 Deploy flow

1. Push Space code
2. Confirm build succeeds
3. Open app logs and run smoke query
4. Validate latency + output formatting

## 11.7 Artifact strategy for Spaces

- Keep large files out of git when possible
- For moderate files, use HF Hub downloads at startup
- Cache downloaded artifacts in Space storage path

---

## 12) AI-Agent Execution Runbook

Give agents this ordered checklist:

1. Create project skeleton and config files
2. Implement data preprocessing + schema validation
3. Implement embedding scripts and save artifacts
4. Build FAISS index and query module
5. Add deterministic skill-gap engine
6. Add evaluation scripts and baseline report
7. Build Gradio UI and local smoke tests
8. Integrate HF Space packaging
9. Deploy and run final acceptance checks
10. Write final docs + architecture notes

Definition of done for each step:

- code exists
- command runs cleanly
- artifacts produced in expected paths
- brief markdown note added to docs

---

## 13) Acceptance Checklist (Phase 1)

You are done with Phase 1 when all are true:

- [ ] `python app.py` launches locally
- [ ] Retrieval returns sensible top-K results
- [ ] Skill gaps are shown with deterministic rationale
- [ ] Offline metrics file exists and is reproducible
- [ ] HF Space builds and serves the app
- [ ] README has setup + run + deploy instructions

---

## 14) Common Failure Modes and Fixes

- **Embeddings mismatch dimensions** → lock single embedding model and validate vector shape before indexing.
- **Slow startup on Spaces** → reduce artifact size, lazy-load index/model.
- **Noisy skill extraction** → tighten aliases and word-boundary rules.
- **Unstable eval** → freeze benchmark split and random seeds.

---

## 15) Deliverables

1. Running demo (HF Space URL)
2. Reproducible baseline metrics
3. Architecture + tradeoff documentation
4. Clear Phase 2 backlog
