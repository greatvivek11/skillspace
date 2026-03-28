# SkillSpace Phase 2 Implementation Plan (Research Expansion)

## 1) Phase 2 Goal

Upgrade Phase 1 MVP into a research-grade semantic career intelligence system while preserving production usability.

Primary outcomes:

- Better retrieval quality via domain-tuned representation learning
- More robust skill reasoning through ontology and harder supervision
- Stronger explainability and benchmarking

---

## 2) Phase 2 Scope

## In Scope

- Domain-adaptive or contrastive fine-tuning (and optional from-scratch experiments)
- Ontology build-out and graph-aware supervision
- Synthetic data generation for coverage gaps
- Neural reranker integration
- Expanded evaluation suite + ablation studies

## Out of Scope (unless extra time)

- Large-scale distributed training cluster ops
- Multi-region production infrastructure

---

## 3) Workstreams

Run five parallel workstreams with shared weekly sync:

1. Data + Ontology
2. Modeling + Training
3. Retrieval + Reranking
4. Product Reasoning + Explainability
5. MLOps + Deployment

Each workstream must publish:

- weekly changelog
- metric deltas
- risk blockers

---

## 4) Data & Ontology Expansion

## 4.1 Ontology v2

Build ontology artifacts:

- canonical skills list
- synonym graph
- parent-child taxonomy
- cross-domain adjacency links

Pipeline steps:

1. Seed from public taxonomies and curated tech lists
2. Mine candidate skills from corpus (TF-IDF + embedding neighbors)
3. Human-in-the-loop consolidation
4. Version ontology (`ontology_v2`)

## 4.2 Synthetic data generation

Generate targeted synthetic samples for underrepresented archetypes.

Constraints:

- clearly label synthetic vs real
- preserve realistic skill co-occurrence
- avoid template leakage into evaluation

Artifacts:

- `artifacts/synthetic/resumes_v2.parquet`
- `artifacts/synthetic/jobs_v2.parquet`

## 4.3 Curriculum datasets

Create staged training sets:

- easy (coarse domain alignment)
- medium (adjacent domain disambiguation)
- hard (fine-grained role differentiation)

---

## 5) Modeling and Training Upgrades

## 5.1 Model roadmap

Order of experiments:

1. **Phase 2A (recommended):** contrastive fine-tune pretrained encoder
2. **Phase 2B:** dual-encoder architecture refinements (pooling/loss/temperature)
3. **Phase 2C (optional):** limited from-scratch training experiments

## 5.2 Training system

Implement modular trainer features:

- config-driven runs
- mixed precision
- gradient accumulation
- checkpoint lifecycle
- deterministic seeds

## 5.3 Losses and sampling

Experiment matrix:

- InfoNCE baseline
- hard-negative mining
- margin-based variants
- curriculum-aware temperature schedule

## 5.4 Experiment tracking

Track in W&B (or equivalent):

- retrieval metrics by domain
- embedding geometry diagnostics
- calibration and confidence curves
- run configs + artifact lineage

---

## 6) Retrieval and Reranking v2

## 6.1 ANN index optimization

Benchmark:

- FlatIP vs IVF vs HNSW
- latency/recall tradeoff at target corpus sizes

## 6.2 Neural reranker

Add cross-encoder reranker pipeline:

1. Retrieve top-K via ANN
2. Score candidates with reranker
3. Re-rank top results

Measure gains:

- MRR uplift
- nDCG uplift
- latency impact

## 6.3 Caching strategy

- cache frequent query embeddings
- cache top-K retrieval results for demo traffic
- add cache invalidation when index version changes

---

## 7) Product Intelligence v2

## 7.1 Skill-gap reasoning v2

Enhance with ontology-aware weighting:

- prerequisite-aware penalties
- adjacent-skill boosts
- role-priority profiles

## 7.2 Explanations

Upgrade explanation templates:

- why matched
- why not top-1
- what to learn next (short horizon / long horizon)

## 7.3 Visualization

Add:

- embedding neighborhood map
- confidence bands
- before/after skill acquisition simulation

---

## 8) Evaluation & Research Rigor

## 8.1 Benchmark design

Maintain three benchmark tracks:

1. Retrieval relevance
2. Skill-gap quality
3. User interpretability

## 8.2 Ablation plan

Minimum ablations:

- without ontology features
- without synthetic data
- without reranker
- baseline vs tuned encoder

## 8.3 Statistical discipline

- fixed random seeds
- confidence intervals where feasible
- report mean over multiple runs for key experiments

---

## 9) Hugging Face Integration for Phase 2

## 9.1 Artifact separation strategy

Use separate HF repos:

- `skillspace-encoder-*`
- `skillspace-reranker-*`
- `skillspace-datasets-*` (if sharing permissible subsets)
- `skillspace-demo-space`

## 9.2 Versioning conventions

Adopt explicit tags:

- model: `v2.0.0`, `v2.1.0`
- index: `index_v2_*`
- ontology: `ontology_v2_*`

Expose selected version in app UI footer for traceability.

## 9.3 Space deployment topology

Space startup should:

1. Read desired artifact versions from config
2. Pull encoder/reranker/index from HF Hub
3. Warm up models
4. Expose health endpoint/check

## 9.4 Secrets and governance

Store only in Space Secrets:

- `HF_TOKEN`
- optional analytics keys

Never commit `.env` or tokens.

## 9.5 CI/CD suggestion

Automate:

- lint + tests on PR
- optional nightly eval
- promote artifacts to "stable" tag only when metric gates pass

---

## 10) AI-Agent Execution Plan (Detailed)

Agent task graph:

1. **Planner Agent**
   - finalize milestone breakdown
   - assign owners and dependencies
2. **Data Agent**
   - ontology v2 build scripts
   - synthetic generation + QA checks
3. **Training Agent**
   - experiment configs
   - training run orchestration
4. **Retrieval Agent**
   - ANN benchmark harness
   - reranker integration
5. **Product Agent**
   - reasoning logic + explanation templates
6. **Deployment Agent**
   - HF artifact publishing and Space updates
7. **Evaluation Agent**
   - benchmark execution + report generation

Handoff artifact for every agent:

- command list
- expected outputs
- verification checklist
- rollback notes

---

## 11) Milestone Timeline (Example: 6–8 Weeks)

### Milestone A (Week 1–2)

- Ontology v2 baseline
- contrastive fine-tune baseline
- benchmark harness finalized

### Milestone B (Week 3–4)

- hard-negative curriculum
- ANN optimization experiments
- first reranker integration

### Milestone C (Week 5–6)

- explanation + reasoning v2
- ablation suite complete
- deployment hardening on HF Spaces

### Buffer (Week 7–8)

- from-scratch pilot experiments (optional)
- polish, writeup, demo narrative

---

## 12) Risks and Mitigations

- **Data noise increases with scale** → enforce schema checks, dedupe, and quality sampling.
- **Reranker latency regression** → cap K, distill reranker, batch inference.
- **Experiment sprawl** → strict run naming, metric gates, weekly pruning.
- **Reproducibility drift** → immutable configs and artifact version pinning.

---

## 13) Phase 2 Exit Criteria

- [ ] Tuned system beats Phase 1 baseline on agreed metrics
- [ ] Reranker improves ranking quality with acceptable latency
- [ ] Ontology-aware skill-gap outputs show measurable consistency gains
- [ ] Full experiment report and ablations documented
- [ ] HF deployment supports versioned artifact switching

---

## 14) Deliverables

1. Research report with ablations and conclusions
2. Versioned models/indexes/ontology artifacts on HF
3. Improved public demo with explainability
4. Clear roadmap for Phase 3 (if pursued)
