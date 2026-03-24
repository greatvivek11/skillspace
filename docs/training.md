# SkillSpace Training System Design

## Overview

SkillSpace trains a research‑grade tiny dual‑encoder transformer using curriculum contrastive learning. The training system is designed to balance:

- research rigor
- hardware feasibility
- reproducibility
- modern transformer practices

This document specifies the full training stack design.

---

## Model Micro‑Architecture

Final configuration:

- Architecture: Dual‑Encoder Transformer (BERT‑style)
- Layers: 8
- Hidden Size: 512
- Attention Heads: 8
- FFN Dimension: 2048
- Parameters: ~55–65M
- Tokenizer: Skill‑Aware Hybrid BPE (~35k vocab)

This configuration maximizes semantic capacity while remaining trainable on consumer GPUs.

---

## Positional Encoding

SkillSpace uses **Rotary Positional Embeddings (RoPE)**.

Rationale:

- better length generalization
- modern transformer design
- improved embedding stability

---

## Optimizer Strategy

Optimizer:

**AdamW with decoupled scheduling**

Key features:

- weight decay regularization
- decoupled learning rate dynamics
- improved convergence stability

---

## Learning Rate Schedule

Final schedule:

**Warmup + Cosine Decay**

Phases:

1. Linear warmup (0 → peak LR)
2. Cosine decay to minimum LR

Benefits:

- smooth embedding formation
- stable early training
- avoids late‑stage collapse

---

## Contrastive Loss Design

Loss:

**Adaptive Temperature InfoNCE**

Features:

- temperature annealing
- curriculum‑aligned hardness scaling
- improved fine‑grained embedding geometry

---

## Curriculum‑Adaptive Batching

Batch design adapts across training stages:

- Easy phase → larger batches
- Medium phase → moderate batches
- Hard phase → smaller batches

Benefits:

- stable early global structure learning
- precise late‑stage discrimination

---

## Training Curriculum Scheduler

Training progresses through structured stages:

1. Easy semantic separation
2. Medium skill boundary learning
3. Hard micro‑career reasoning

Curriculum is driven by ontology graph distance.

---

## Training Infrastructure

SkillSpace uses a **custom modular trainer framework**.

Capabilities:

- curriculum‑aware data loaders
- multi‑objective training hooks
- checkpoint orchestration
- experiment reproducibility

This provides stronger engineering signal than high‑level frameworks.

---

## Gradient Strategy

- Gradient accumulation for large effective batch sizes
- Mixed precision training (fp16/bf16)
- Gradient clipping for stability

---

## Experiment Tracking

Tracking stack:

- Weights & Biases
- structured JSON logs
- checkpoint metadata

Tracked metrics:

- contrastive loss
- embedding norm statistics
- retrieval proxy metrics
- curriculum stage performance

---

## Checkpointing Strategy

- Stage‑wise checkpoints
- Best retrieval proxy checkpoint
- Final converged checkpoint

This enables analysis of embedding evolution.

---

## Training Philosophy

SkillSpace treats training as:

> structured representation formation rather than generic optimization.

This design enables a small transformer to learn meaningful career semantics under constrained compute budgets.
