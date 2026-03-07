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
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python
- Google Gemini AI (primary LLM) + DeepSeek (fallback)
- ElevenLabs API (voice synthesis)
- LangChain + ChromaDB (RAG pipeline)
- HuggingFace Embeddings

**Frontend**
- ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js) Next.js + TailwindCSS
- MediaRecorder API (real-time audio recording/playback)

**Infrastructure**
- Docker + docker-compose
- PostgreSQL + MongoDB

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
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
DEEPSEEK_API_KEY=your_deepseek_key  # optional fallback
```

---

## 📌 Key Implementation Highlights

- **RAG Pipeline** — Ingests PDFs → chunks text → generates vector embeddings → semantic search → feeds context to Gemini to reduce hallucinations
- **Multi-provider LLM** — Gemini as primary, DeepSeek as automatic fallback with API key rotation for rate limit handling
- **Production Features** — Rate limiting (SlowAPI), CORS middleware, custom exception handling, structured logging with request ID tracking, response caching

---

## 👨‍💻 Author

**Gollapothu Yuvaraj**  
Python Developer | AI & Data Science Enthusiast  
📧 gyuvrajvarma@gmail.com  
🔗 [GitHub](https://github.com/Yuvaraj-varma)

---

## 📄 License

This project is licensed under the MIT License.
