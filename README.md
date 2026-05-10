# 🎙️ Voice AI Agent System

> A full-stack AI-powered voice application built with FastAPI, Next.js, Google Gemini, and ElevenLabs — featuring Text-to-Speech, Speech-to-Speech, a conversational Voice Agent, and a RAG-based Invoice Assistant.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔊 **Text to Speech** | Convert any text to natural-sounding audio using ElevenLabs |
| 🎤 **Speech to Speech** | Record your voice → AI processes → responds with voice |
| 🤖 **Voice Agent** | Conversational AI agent powered by Google Gemini + LangChain + DuckDuckGo web search |
| 📄 **Invoice Assistant** | Upload invoice PDFs → ask questions → AI answers using RAG pipeline |

---

## 🛠️ Tech Stack

**Backend**
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) FastAPI
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) Python 3.10+
- Google Gemini AI (`gemini-2.0-flash`, `gemini-2.5-flash-lite`) — primary LLM
- ElevenLabs API + gTTS (voice synthesis with fallback)
- LangChain + LangChain Google GenAI (AI agent framework)
- Pinecone (cloud vector DB) with session-based namespace isolation
- Google Gemini Embeddings (`gemini-embedding-001`)
- DuckDuckGo Search (`ddgs`) — real-time web search tool
- SlowAPI (rate limiting)
- httpx (async HTTP client)

**Frontend**
- ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js) Next.js 16 + React 19
- TailwindCSS 4
- Lucide React (icons)
- Fetch API (HTTP client)
- MediaRecorder API (real-time audio recording/playback)

**Infrastructure**
- Docker + docker-compose
- Vercel (frontend deployment)
- Render (backend deployment)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│         Next.js + TailwindCSS                │
│   (Audio recording, playback, chat UI)       │
└─────────────────┬───────────────────────────┘
                  │ REST API
┌─────────────────▼───────────────────────────┐
│                 Backend                      │
│              FastAPI                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
│  │   TTS    │ │  Voice   │ │  Invoice    │  │
│  │ Service  │ │  Agent   │ │  Assistant  │  │
│  │          │ │ (Gemini  │ │  (LangChain │  │
│  │          │ │+LangChain│ │  +Pinecone) │  │
│  └──────────┘ └──────────┘ └─────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- API Keys: Google Gemini, ElevenLabs, Pinecone

### 1. Clone the repo
```bash
git clone https://github.com/Yuvaraj-varma/voice-agent.git
cd voice-agent
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
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
VOICE_AGENT_GEMINI_API_KEY=your_voice_agent_key
RAG_GEMINI_API_KEY=your_rag_gemini_key

# Voice Synthesis Keys
ELEVENLABS_API_KEY=your_elevenlabs_key
DS_TUTOR_ELEVENLABS_API_KEY=your_ds_tutor_key

# Vector Database
PINECONE_API_KEY=your_pinecone_key

# Optional Fallback
DEEPSEEK_API_KEY=your_deepseek_key
```

---

## 📌 Key Implementation Highlights

- **RAG Pipeline** — Ingests invoice PDFs → chunks text → generates vector embeddings (Gemini Embeddings) → stores in Pinecone with session-based namespace isolation → semantic search → feeds context to Gemini
- **Session Isolation** — Each user gets a unique session ID via `crypto.randomUUID()` stored in `localStorage` — data isolated per user in Pinecone namespaces without login
- **AI Agent** — LangChain `AgentExecutor` + `create_tool_calling_agent` with DuckDuckGo web search tool for real-time information
- **Dual TTS System** — ElevenLabs for premium voices + gTTS as free fallback
- **Dedicated API Keys** — Separate Gemini keys for Voice Agent and Invoice Assistant to prevent rate limit conflicts
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
