# Episteme

**Episteme** is a self-directed learning engine for decomposing complex tasks into prerequisite concepts and tracking personal mastery over time. It bridges the gap between what you want to do and what you need to know—starting from a local Python + SQLite base and scaling toward agentic, LLM-augmented knowledge workflows.

---

## 🧠 Core Philosophy

Every ambitious goal is a graph of dependencies. Episteme makes these visible, traceable, and actionable.

> 🎯 Task: "Build a transformer-based dialogue agent"  
> 🧩 Prereqs: ["cross-attention", "causal masking", "token embeddings", "beam search", ...]

By mapping and reviewing the underlying concepts, you move from surface-level learning to durable, transferable understanding.

---

## 🔧 Features

- 🔍 **Task decomposition** into prerequisite concepts
- ✅ **Track what you know, don’t know, and learn**
- 🪵 **Log learning moments, confusions, and insights**
- 🔁 **Concept reuse** across tasks
- 💾 **Lightweight + local**: Python + SQLite
- 🤖 *(Planned)*: Local LLM integration for automated concept generation
- 🌐 *(Planned)*: LangGraph agent orchestration

---

## 🚀 Quickstart

```bash
git clone https://github.com/your-username/episteme.git
cd episteme
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python episteme.py

## TODO

- [ ] Set up SQLite schema
- [x] Write README.md
- [ ] Build CLI for task + concept tracking
- [ ] Integrate LLM for prerequisite decomposition
- [ ] Create reflection logger
