# 🎙️ Voice AI Agent System

> A full-stack AI-powered voice application built with FastAPI, Next.js, Google Gemini, and ElevenLabs — featuring Text-to-Speech, Speech-to-Speech, a conversational Voice Agent, and a RAG-based AI tutor.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔊 **Text to Speech** | Convert any text to natural-sounding audio using ElevenLabs |
| 🎤 **Speech to Speech** | Record your voice → AI processes → responds with voice |
| 🤖 **Voice Agent** | Real-time conversational AI agent powered by Google Gemini |
| 📚 **RAG Data Science Tutor** | Upload PDFs → ask questions → AI answers from your documents |

---

## 🛠️ Tech Stack

**Backend**
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) FastAPI + WebSockets
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python 3.10+
- Google Gemini AI (primary LLM) + DeepSeek (fallback)
- ElevenLabs API + gTTS (voice synthesis)
- LangChain + Pinecone (cloud vector DB)
- Sentence Transformers (embeddings)
- SlowAPI (rate limiting)
- httpx (async HTTP client)

**Frontend**
- ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js) Next.js 16 + React 19
- TailwindCSS 4
- Three.js + React Three Fiber (3D graphics)
- Lucide React (icons)
- Axios (HTTP client)
- MediaRecorder API (real-time audio recording/playback)

**Infrastructure**
- Docker + docker-compose
- ChromaDB (local vector storage)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│         Next.js + TailwindCSS                │
│   (Audio recording, playback, chat UI)       │
└─────────────────┬───────────────────────────┘
                  │ REST API / WebSockets
┌─────────────────▼───────────────────────────┐
│                 Backend                      │
│              FastAPI                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │   TTS    │ │  Voice   │ │  RAG Tutor  │  │
│  │ Service  │ │  Agent   │ │  (LangChain │  │
│  │          │ │ (Gemini) │ │  +ChromaDB) │  │
│  └──────────┘ └──────────┘ └─────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys: Google Gemini, ElevenLabs

### 1. Clone the repo
```bash
git clone https://github.com/Yuvaraj-varma/voice-agent.git
cd voice-agent
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Run with Docker (recommended)
```bash
docker-compose up --build
```

---

## 🔑 Environment Variables

```env
# Primary AI Keys
GEMINI_API_KEY=your_gemini_key
VOICE_AGENT_GEMINI_API_KEY=your_voice_agent_key  # dedicated for voice agent

# Voice Synthesis Keys
ELEVENLABS_API_KEY=your_elevenlabs_key
DS_TUTOR_ELEVENLABS_API_KEY=your_ds_tutor_key  # dedicated for DS tutor

# Optional Fallback
DEEPSEEK_API_KEY=your_deepseek_key

# Vector Database (if using Pinecone cloud)
PINECONE_API_KEY=your_pinecone_key  # optional
```

---

## 📌 Key Implementation Highlights

- **RAG Pipeline** — Ingests PDFs → chunks text → generates vector embeddings (Sentence Transformers) → stores in Pinecone/ChromaDB → semantic search → feeds context to Gemini to reduce hallucinations
- **Multi-provider LLM** — Gemini as primary, DeepSeek as automatic fallback with API key rotation for rate limit handling
- **Dual TTS System** — ElevenLabs for premium voices + gTTS as free fallback option
- **Dedicated API Keys** — Separate keys for Voice Agent and DS Tutor to prevent rate limit conflicts
- **Production Features** — Rate limiting (SlowAPI), CORS middleware, custom exception handling, structured logging with request ID tracking, response caching
- **3D UI Elements** — Three.js integration for enhanced visual experience

---

## 👨‍💻 Author

**Gollapothu Yuvaraj**  
Python Developer | AI & Data Science Enthusiast  
📧 gyuvrajvarma@gmail.com  
🔗 [GitHub](https://github.com/Yuvaraj-varma)

---

## 📄 License

This project is licensed under the MIT License.
