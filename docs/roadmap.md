# SkillSpace Execution Roadmap

## Overview

This roadmap defines the research‑grade yet product‑realistic execution strategy for building SkillSpace within a constrained 2–3 week development window.

The execution philosophy balances:

- structured deep learning research
- clean engineering practices
- incremental product validation
- continuous deployment mindset

---

## Execution Principles

- Vertical slice development over isolated subsystems
- Curriculum milestone training instead of monolithic runs
- Hypothesis‑driven experimentation
- Progressive UI intelligence integration
- Continuous deployment and evaluation

---

## Repository Architecture Strategy

SkillSpace follows a **research‑production hybrid structure**:

```
skillspace/
  docs/
  src/
    data/
    ontology/
    tokenization/
    models/
    training/
    retrieval/
    product/
    ui/
  experiments/
  scripts/
  notebooks/
```

This enables:

- reproducible research
- modular engineering
- scalable experimentation

---

## Development Strategy — Vertical Slice Iteration

Instead of building subsystems in isolation:

1. Minimal dataset + tiny model → working retrieval
2. Improved embeddings → validated ranking
3. Product reasoning → UI intelligence
4. Full curriculum training → final deployment

---

## Training Milestone Strategy

Training progresses via structured milestones:

### Milestone 1
- Small dataset
- Easy curriculum
- Validate embedding topology

### Milestone 2
- Medium curriculum
- Improved ontology integration
- Retrieval evaluation

### Milestone 3
- Full curriculum
- Cross‑encoder reranking
- Final embedding convergence

---

## Experimentation Philosophy

All experiments follow hypothesis‑driven design:

- What representation property is being improved?
- How does retrieval performance change?
- Does ontology signal improve clustering?

Tracked via:

- W&B experiment dashboards
- structured experiment notes

---

## UI Development Strategy

UI evolves alongside model capability:

### Stage 1
- Basic retrieval demo

### Stage 2
- Embedding visualization

### Stage 3
- Skill gap reasoning

### Stage 4
- Interactive career exploration

---

## Deployment Strategy

Continuous deployment pipeline:

- Baseline encoder deployed early
- Retrieval index integrated mid‑phase
- Reranker + reasoning deployed final

Ensures:

- early validation
- realistic ML lifecycle signal

---

## Evaluation Roadmap

Evaluation embedded into milestones:

- Retrieval recall@K
- Embedding clustering quality
- Skill prediction proxy metrics
- UX interpretability validation

---

## Time Allocation Plan (2–3 Weeks)

### Week 1
- Data pipeline + ontology
- Tokenizer training
- Baseline encoder training

### Week 2
- Curriculum training
- Retrieval infra
- Initial UI

### Week 3 (optional buffer)
- Reranker
- Product intelligence layer
- Optimization + polish

---

## Final Objective

SkillSpace execution aims to demonstrate:

> end‑to‑end ML system thinking from data design to AI product deployment.

The roadmap ensures disciplined progress while maintaining research‑level depth and product realism.
