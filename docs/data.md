# SkillSpace Data Intelligence Design

## Overview

SkillSpace is built on a **hybrid real + synthetic data intelligence pipeline** designed to train a dual‑encoder transformer for semantic career reasoning.

The goal is not simply to train on resumes and jobs, but to **engineer structured learning signals** that allow the model to learn:

- career topology
- skill semantics
- job‑resume compatibility
- fine‑grained professional similarity

This document describes the full data design philosophy, pipeline architecture, and training signal construction.

---

## Data Design Principles

SkillSpace follows these core principles:

- Representation learning over classification
- Semantic structure over raw scale
- Controlled curriculum over random supervision
- Ontology‑guided supervision over noisy labels
- Hybrid real + synthetic signal engineering

---

## Data Sources

### Real Resume Data

Sources:
- Kaggle resume datasets
- Resume NER datasets

Target scale:
- ~25k resumes

Purpose:
- real language distribution
- authentic career narratives

---

### Real Job Data

Sources:
- Kaggle job posting datasets
- HuggingFace job datasets
- curated open job corpora

Target scale:
- ~80k job descriptions

Required fields:
- title
- description
- skills
- domain

---

### Synthetic Data Layer

Synthetic data is used to provide:

- curriculum signal control
- balanced archetype coverage
- stable training convergence

Target scale:
- ~40k synthetic resumes
- ~40k synthetic jobs

---

## Skill Ontology

SkillSpace uses a **hierarchical DAG skill ontology**.

### Hierarchy Levels

Level 0 — Meta Domains
- software_engineering
- artificial_intelligence
- data_science
- cloud
- infrastructure
- analytics

Level 1 — Subdomains
- machine_learning
- devops
- backend
- frontend
- computer_vision
- nlp

Level 2 — Skill Families
- transformers
- distributed_systems
- model_deployment

Level 3 — Concrete Skills
- pytorch
- docker
- kubernetes
- react
- aws

Target size:
- 4000–6000 concrete skills

---

## Ontology Construction Pipeline

### Phase 1 — Curated Backbone

Sources:
- ESCO
- O*NET
- curated tech skill lists

Provides semantic skeleton.

### Phase 2 — Data‑Mined Expansion

Methods:
- TF‑IDF phrase mining
- rule‑based skill extraction
- embedding clustering

### Phase 3 — Graph Consolidation

Operations:
- synonym merging
- normalization
- multi‑parent assignment
- noise pruning

Final artifacts:

```
ontology/
   skills_graph.json
   skill_list.txt
   normalization_map.json
```

---

## Skill‑Aware Tokenization

Tokenizer consists of:

- domain BPE (30k tokens)
- skill tokens (3k–6k)

Skill tokens are appended during preprocessing:

Example:

```
Worked on backend systems using Python and Docker.
<SKILL_python> <SKILL_docker>
```

Benefits:

- semantic grounding
- faster convergence
- explainability

---

## Resume Representation

SkillSpace uses **hybrid hierarchical encoding**.

Sections encoded independently:

- summary
- experience
- skills
- projects
- education

Section embeddings aggregated via learned pooling.

Skill tokens injected at section level.

---

## Synthetic Resume Generator

Hybrid structured generator:

Components:
- archetype sampling
- career trajectory simulation
- skill distribution modeling
- templated narrative variation

Supports:
- tech careers
- adjacent technical roles

---

## Contrastive Curriculum Training

Training progresses in stages:

### Stage 1 — Easy
- positives: same archetype
- negatives: distant domains

### Stage 2 — Medium
- positives: skill overlap
- negatives: adjacent domains

### Stage 3 — Hard
- positives: fine skill match
- negatives: near‑skill competitors

Negative sampling guided by ontology graph distance.

---

## Pair Generation Engine

Each training batch contains:

- N resume embeddings
- N positive job embeddings
- N curriculum‑sampled negatives

Loss:
- InfoNCE contrastive loss

---

## Dataset Versioning Strategy

Curriculum datasets stored as snapshots:

- dataset_easy
- dataset_medium
- dataset_hard

Ensures reproducibility and structured training progression.

---

## Evaluation Dataset Design

SkillSpace defines benchmark suites:

- retrieval benchmark
- clustering benchmark
- skill prediction benchmark

Evaluation is stratified by career archetype.

---

## Data Folder Structure

```
data/
   raw/
   processed/
   synthetic/
   ontology/
   curriculum/
   evaluation/
```

---

## Design Philosophy

SkillSpace treats data as:

> engineered learning signal rather than passive dataset.

This enables training a small transformer to learn meaningful semantic career representations within limited compute constraints.
