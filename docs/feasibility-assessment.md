# SkillSpace Feasibility Assessment (3–4 Week Portfolio Sprint)

## Executive Summary

The core idea is strong for a portfolio project: semantic resume–job matching with explainable skill-gap insights is practical, demo-friendly, and showcases end-to-end ML thinking.

However, the current plan is **over-scoped** for 3–4 weeks if you train custom transformers from scratch plus ontology building plus reranking plus rich UI.

Recommended framing for the sprint:

- Build a **vertical slice** that is clearly useful and explainable.
- Defer "research depth" items (large synthetic pipeline, custom trainer complexity, multi-stage curriculum hardening) to post-v1.

## Feasibility Verdict

**Yes, worth trying** if you scope tightly.

- Keep the learning objective (understand concepts and flow).
- Use coding assistants to move faster, but preserve ownership by writing design notes and experiment logs.
- Ship one clean, measurable baseline first.

## Scope Risk in Current Design

Current docs include several high-complexity components:

- from-scratch transformer training
- hybrid real + synthetic data generation at scale
- ontology engineering and graph-aware curriculum
- dual-stage retrieval + neural reranking
- interactive product intelligence UI

This is excellent long-term architecture, but too wide for a short sprint unless aggressively reduced.

## Recommended 3–4 Week MVP Plan

### Week 1

- Curate a small clean dataset (2k–10k jobs + 1k–3k resumes or resume-like profiles)
- Use a compact pretrained sentence embedding model as baseline
- Build FAISS index and retrieval evaluation (Recall@K)

### Week 2

- Add skill extraction and a simple deterministic skill-gap reasoner
- Build first Gradio UI (upload text + top matches + gap list)
- Add experiment tracking and reproducibility notes

### Week 3

- Optional: lightweight contrastive fine-tune (not from-scratch pretraining)
- Improve ranking quality and explanations
- Add portfolio polish (architecture diagram, metrics table, short demo video)

### Week 4 (buffer)

- CPU optimization for deployment
- Error handling / UX improvements
- Final documentation and postmortem

## Hardware Fit

Your hardware is suitable for this scoped approach:

- MacBook Pro M4 Pro 24GB: development, preprocessing, small inference tests
- Desktop (RTX 5070 Ti class + Ryzen 7 + 48GB RAM): fine-tuning, embedding generation, FAISS experiments

For true from-scratch transformer pretraining, time—not raw hardware—is the main bottleneck in a 3–4 week window.

## Repo Size Expectations

With practical controls, repository size can stay manageable:

- Keep raw datasets **out** of git
- Version only small samples and metadata
- Store large artifacts in external storage (HF Hub, cloud bucket, local ignored paths)
- Commit configs, scripts, evaluation results, and model cards

Typical footprint for a clean portfolio repo can remain modest (docs + code + configs + small eval artifacts), while large datasets/checkpoints live outside git.

## What Makes This Portfolio-Strong

- Clear problem statement and why semantic retrieval beats keyword rules
- Measurable evaluation (Recall@K / MRR style metrics)
- Interpretable outputs (skill gaps + rationale)
- Honest tradeoff discussion: baseline vs fine-tuned vs from-scratch ambitions

## Suggested Scope Cuts (If Needed)

Cut first:

1. custom tokenizer training
2. synthetic data generation at large scale
3. cross-encoder reranker
4. complex archetype manifold features

Keep first:

1. embedding retrieval pipeline
2. basic skill-gap explanation
3. simple, polished UI
4. reproducible experiments and metrics

## Decision

Proceed with the project.

But treat "from-scratch deep research system" as **Phase 2**. For this 3–4 week sprint, ship a focused MVP that demonstrates ML system competence end-to-end.
