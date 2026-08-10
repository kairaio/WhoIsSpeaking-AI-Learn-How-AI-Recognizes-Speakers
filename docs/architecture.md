# 🏗️ WhoIsSpeaking AI — Architecture

WhoIsSpeaking AI is an educational project for learning how AI can distinguish between consenting, enrolled speakers using voice embeddings.

---

## 🎙️ System Flow

```mermaid
flowchart TD
    A["🎙️ Human Speaks"] --> B["📤 Audio Upload"]
    B --> C["⚡ FastAPI"]
    C --> D["🔊 Audio Processing"]

    D --> E["🧬 ECAPA-TDNN Speaker Encoder"]
    E --> F["📐 Speaker Embedding"]

    F --> G["🔍 Cosine Similarity"]
    H[("🔐 Enrolled Speaker Profiles")] --> G

    G --> I{"Score ≥ Threshold?"}

    I -->|Yes| J["👤 Known Speaker"]
    I -->|No| K["❓ Unknown Speaker"]

    J --> L["🧠 Speaker Context"]
    J --> M["💾 Speaker Memory"]

    L --> N["🤖 Identity-Aware Assistant"]
    M --> N
```

---

## 🧬 Voice Enrollment

Before the system can recognize a speaker, the speaker must voluntarily enroll voice samples.

```mermaid
flowchart LR
    A["🎙️ Sample 1"] --> D["🔊 Audio Processing"]
    B["🎙️ Sample 2"] --> D
    C["🎙️ Sample 3"] --> D

    D --> E["🧬 Speaker Encoder"]
    E --> F["📐 Embeddings"]
    F --> G["➗ Average + Normalize"]
    G --> H[("🔐 Speaker Profile")]
```

Example:

```text
Kaira voice samples
        ↓
Audio Processing
        ↓
ECAPA-TDNN
        ↓
Speaker Embeddings
        ↓
Average + Normalize
        ↓
Kaira.npy
```

The raw uploaded audio is temporary.

The educational MVP keeps the derived speaker embedding profile instead.

---

## 🔍 Speaker Identification

When a new voice sample arrives:

```mermaid
flowchart TD
    A["🎙️ New Voice"] --> B["🧬 New Embedding"]

    B --> C["Compare with Kaira"]
    B --> D["Compare with Jensen"]
    B --> E["Compare with Other Profiles"]

    C --> F["📊 Similarity Scores"]
    D --> F
    E --> F

    F --> G["🏆 Best Candidate"]
    G --> H{"Above Threshold?"}

    H -->|Yes| I["✅ Known Speaker"]
    H -->|No| J["❓ Unknown"]
```

The system compares embeddings using cosine similarity.

The profile with the highest similarity score becomes the best candidate.

A threshold is then used to decide whether the candidate should be accepted or returned as `Unknown`.

---

## 🧠 Identity-Aware Context

Speaker recognition can be connected to separate context and memory.

```mermaid
flowchart TD
    A["🎙️ Voice"] --> B["🔍 Speaker Recognition"]

    B --> C["👩 Kaira"]
    B --> D["👨 Jensen"]
    B --> E["❓ Unknown"]

    C --> F["🧠 Kaira Context"]
    C --> G["💾 Kaira Memory"]

    D --> H["🧠 Jensen Context"]
    D --> I["💾 Jensen Memory"]

    E --> J["Guest Context"]

    F --> K["🤖 AI Assistant"]
    G --> K

    H --> K
    I --> K

    J --> K
```

This demonstrates how one AI assistant could maintain different contexts for different enrolled speakers.

---

## 🗂️ Main Components

| Component | Purpose |
|---|---|
| `FastAPI` | Provides the HTTP API |
| `SpeechBrain` | Speaker-recognition model interface |
| `ECAPA-TDNN` | Creates speaker embeddings |
| `Torchaudio` | Loads and processes audio |
| `NumPy` | Stores and compares embeddings |
| `Speaker Enrollment` | Creates speaker profiles |
| `Identification` | Finds the closest enrolled speaker |
| `Context` | Loads speaker-specific context |
| `Memory` | Stores separate notes per speaker |

---

## 🔐 Privacy Model

```mermaid
flowchart LR
    A["🎙️ Uploaded Audio"] --> B["Temporary File"]
    B --> C["🧬 Extract Embedding"]
    C --> D[("🔐 Speaker Profile")]
    B --> E["🗑️ Delete Temporary Audio"]
```

Voice can be biometric information.

This project is therefore designed around:

- informed consent;
- voluntary speaker enrollment;
- temporary raw audio processing;
- local derived speaker profiles;
- explicit `Unknown` results;
- profile deletion;
- no covert identification.

---

## ⚠️ Educational Scope

WhoIsSpeaking AI is intended for:

**Education · Learning · Research · Experimentation**

It is **not** designed as a high-security authentication system.

Similarity thresholds must be calibrated using real samples and the actual recording environment.

---

## 🚀 Future Architecture

```mermaid
flowchart LR
    A["🎙️ Voice"] --> B["👤 Speaker Recognition"]
    A --> C["📝 Speech-to-Text"]

    B --> D["🧠 Personal Context"]
    B --> E["💾 Personal Memory"]

    C --> F["🤖 LLM"]
    D --> F
    E --> F

    F --> G["💬 Response"]
    G --> H["🔊 Text-to-Speech"]
```

Future learning modules can explore:

- real-time microphone streaming;
- speech-to-text;
- multilingual transcription;
- LLM integration;
- text-to-speech;
- multiple speakers;
- better threshold calibration;
- encrypted speaker profiles.

---

## 🎯 Core Idea

> Most AI understands **what** was said.

WhoIsSpeaking AI explores how an AI system can also learn:

> **Who is speaking?**

---

**One AI. Multiple enrolled speakers. Different context.**