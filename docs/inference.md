# SkillSpace Inference & Retrieval System Design

## Overview

SkillSpace deploys a production‑realistic semantic retrieval stack built around a dual‑encoder transformer and a lightweight neural reranker. The system emphasizes low‑latency inference, scalable vector search, and modular deployment on HuggingFace.

---

## Embedding Architecture

- Encoder: Dual‑Encoder Transformer (8L, 512H)
- Projection Head: Learnable projection to 384‑dim embeddings
- Normalization: L2‑normalized vectors for cosine similarity

Rationale:
- Smaller index footprint
- Improved retrieval generalization
- Stable ANN performance

---

## Vector Index System

SkillSpace uses a hybrid FAISS configuration:

- IVF (Inverted File Index) for coarse partitioning
- HNSW for fast approximate nearest neighbor search

Benefits:
- Sub‑linear retrieval latency
- Scalable to 100k–1M job embeddings
- Production‑realistic infra signal

---

## Retrieval Pipeline

### Stage 1 — ANN Retrieval
- Encode resume → 384‑dim embedding
- Query FAISS index
- Retrieve top‑K candidates (e.g., K=50)

### Stage 2 — Neural Reranking
- Tiny cross‑encoder transformer scores top‑K pairs
- Produces final ranked list (e.g., top‑10)

This dual‑stage design balances recall and precision.

---

## Embedding Lifecycle Strategy

- Job embeddings computed **offline** and indexed
- Resume embeddings computed **online** per query
- Index refreshed via periodic batch updates

Advantages:
- Low query latency
- Deterministic retrieval behavior
- Clear separation of training vs serving concerns

---

## Neural Reranker Design

- Architecture: Tiny cross‑encoder transformer (4L, 256H)
- Input: [CLS] resume_text [SEP] job_text
- Output: relevance score

Purpose:
- Fine‑grained semantic disambiguation
- Improved ranking precision in adjacent skill domains

---

## Inference Batching Strategy

Dynamic micro‑batch scheduler:

- Aggregates concurrent requests
- Adapts batch size to latency budget
- Supports CPU‑only inference on HF Spaces

Optimizations:
- Mixed precision where available
- Token truncation heuristics

---

## HuggingFace Deployment Topology

SkillSpace uses multi‑artifact deployment:

- Encoder model → HF Model Hub
- Reranker model → HF Model Hub
- Vector index → Space persistent storage
- UI + inference runtime → HF Space

This modular design mirrors production ML systems.

---

## Latency Optimization Philosophy

Multi‑level optimizations:

- ANN index tuning (nlist, efSearch)
- Embedding cache for repeat queries
- Projection dimension reduction
- Section‑aware token truncation

Target latency:
- < 500 ms median retrieval on CPU runtime

---

## Inference Data Flow

```mermaid
flowchart LR

User[User Resume]
UI[Gradio UI]
Encoder[Dual Encoder]
Index[FAISS Index]
Candidates[Top‑K Jobs]
Reranker[Cross Encoder]
Results[Ranked Output]

User --> UI
UI --> Encoder
Encoder --> Index
Index --> Candidates
Candidates --> Reranker
Reranker --> Results
Results --> UI
```

---

## Design Philosophy

SkillSpace treats retrieval as:

> a modular semantic reasoning pipeline rather than a monolithic search function.

This enables realistic ML system design while remaining deployable on constrained free‑tier infrastructure.
