# SkillSpace Phase 1 Roadmap (Lean Semantic Matcher)

## 🎯 Goal

Ship a **working ML product** in 3–4 weeks that demonstrates:

- contrastive learning
- semantic embeddings
- job retrieval
- basic skill gap insights

NOT full system complexity.

---

## 🧠 Scope (Strictly Limited)

### Included
- Dual Encoder Transformer (small)
- Basic skill-aware tokenization
- Flat skill list (no DAG)
- Contrastive training (single stage)
- FAISS Flat index
- Simple Gradio UI
- Basic skill gap (set difference)

### Excluded (Phase 2+)
- curriculum learning
- synthetic data generation
- hierarchical ontology
- reranker
- advanced UI interactions

---

## 🏗️ Model Spec

- Layers: 4–6
- Hidden: 256–384
- Heads: 4–6
- Embedding dim: 256

Loss: InfoNCE
Optimizer: AdamW

---

## 📊 Data Strategy

### Resume Data
- Kaggle resume dataset (~10k)

### Job Data
- Kaggle job descriptions (~20k–50k)

### Skills
- curated list (~1k skills)

---

## ⚙️ Pipeline

1. Clean resumes + jobs
2. Extract skills (dictionary match)
3. Build (resume, job) pairs via skill overlap
4. Train dual encoder
5. Encode jobs → FAISS index
6. Query with resume → retrieve jobs

---

## 🖥️ UI (Gradio)

Inputs:
- resume upload / text

Outputs:
- top 5 jobs
- similarity score
- detected skills
- missing skills

---

## 📅 Execution Plan

### Week 1
- Data cleaning
- Skill extraction
- Tokenizer setup

### Week 2
- Model training (small scale)
- Evaluate embeddings

### Week 3
- FAISS retrieval
- Gradio UI

### Week 4 (buffer)
- polish + deploy on HF

---

## 🚀 Success Criteria

- coherent job matches
- reasonable skill gap output
- working UI demo
- hosted on HuggingFace

---

## 🔮 Future Work (Phase 2+)

- curriculum learning
- hierarchical ontology
- reranker
- product intelligence layer

---

## 🧠 Philosophy

Phase 1 is about:

> shipping a real system, not proving theoretical completeness.

Keep it simple. Ship it.
