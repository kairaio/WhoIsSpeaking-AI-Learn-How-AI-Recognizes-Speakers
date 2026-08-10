🎙️ WhoIsSpeaking AI

<p align="center">
  <b>Learn how AI recognizes who is speaking.</b>
</p>

<p align="center">
  An open-source educational project exploring speaker embeddings,
  voice enrollment, speaker verification, speech recognition,
  and identity-aware AI.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue">
  <img src="https://img.shields.io/badge/FastAPI-API-green">
  <img src="https://img.shields.io/badge/AI-Speaker%20Recognition-purple">
  <img src="https://img.shields.io/badge/License-MIT-yellow">
  <img src="https://img.shields.io/badge/Project-Educational-orange">
</p>

---

## ✨ What is WhoIsSpeaking AI?

Most AI assistants understand **what you say**.

WhoIsSpeaking AI explores something different:

> **Can an AI understand who is speaking and automatically switch context?**

The project teaches how speaker recognition works by building a
consent-based voice AI system from scratch.

---

## 🧠 How It Works

```mermaid
flowchart TD

    A["🎙️ Human Speaks"]
    B["🔊 Audio Input"]
    C["🧬 Speaker Embedding"]
    D["🔍 Voice Comparison"]
    E{"Speaker?"}

    F["👩 Kaira"]
    G["👨 Jensen"]
    H["❓ Unknown"]

    I["📝 Speech-to-Text"]
    J["🧠 Personal Context"]
    K["🤖 AI / LLM"]
    L["🔊 AI Response"]

    A --> B
    B --> C
    C --> D
    D --> E

    E --> F
    E --> G
    E --> H

    F --> I
    G --> I

    I --> J
    J --> K
    K --> L