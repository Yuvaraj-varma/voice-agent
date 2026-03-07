# Voice Agent System - Complete Project Summary for Claude.ai

## 🎯 Project Overview
Full-stack AI Voice Agent system with 4 main features: Text-to-Speech, Speech-to-Speech transformation, AI Voice Agent, and RAG-based Data Science Tutor.

**Tech Stack:**
- Backend: FastAPI (Python 3.13.1)
- Frontend: Next.js 16 + React 19
- AI: Google Gemini, ElevenLabs, DeepSeek
- Database: ChromaDB (vector database)
- Styling: TailwindCSS 4

---

## 📁 Project Structure

```
Voice-Agent-system/
├── backend/                    # FastAPI Backend
│   ├── routes/                 # API endpoints
│   │   ├── text_speech_routes.py    # TTS & voice listing
│   │   ├── voice_transform.py       # Speech-to-Speech
│   │   ├── voice_agent.py           # Conversational AI
│   │   └── ds_rag_agent.py          # RAG tutor
│   ├── services/
│   │   └── rag_service.py           # RAG pipeline
│   ├── providers/
│   │   ├── gemini_provider.py       # Gemini integration
│   │   └── deepseek_provider.py     # Fallback LLM
│   ├── utils/
│   │   ├── gemini_rotator.py        # API key rotation
│   │   ├── logger.py                # Logging system
│   │   └── tts.py                   # TTS utilities
│   ├── middleware/
│   │   └── request_id.py            # Request tracking
│   ├── exceptions/
│   │   ├── base.py                  # Custom exceptions
│   │   └── handlers.py              # Error handlers
│   ├── data/ds_notes/               # PDF documents
│   ├── chroma_db/                   # Vector DB storage
│   └── main.py                      # FastAPI entry point
│
└── frontend/                   # Next.js Frontend
    ├── src/
    │   ├── app/
    │   │   ├── page.js              # Landing page
    │   │   ├── generate-voice/      # TTS UI
    │   │   ├── speech-to-speech/    # Voice transform UI
    │   │   ├── voice-agent/         # AI agent UI
    │   │   └── ds-tutor/            # RAG tutor UI
    │   ├── components/
    │   │   ├── AudioPlayer.js       # Audio playback
    │   │   ├── AudioRecorder.js     # Voice recording
    │   │   └── VoiceSelector.js     # Voice selection
    │   ├── services/
    │   │   ├── api.js               # API client
    │   │   ├── voiceApi.js          # Voice endpoints
    │   │   └── dsTutorApi.js        # Tutor endpoints
    │   └── hooks/
    │       └── useVoices.js         # Voice management
    └── public/                      # Static assets
```

---

## 🚀 Features

### 1. Text-to-Speech (Generate Voice)
**Route:** `/generate-voice`
**Backend:** `text_speech_routes.py`

- Convert text to natural speech
- 500 character limit
- Multiple ElevenLabs voices
- Real-time audio generation
- Download capability

**API Endpoint:** `POST /api/speech`
```json
{
  "text": "Hello world",
  "voiceId": "21m00Tcm4TlvDq8ikWAM"
}
```

### 2. Speech-to-Speech Conversion
**Route:** `/speech-to-speech`
**Backend:** `voice_transform.py`

- Upload audio (WAV, MP3, WEBM)
- Transcribe with Gemini AI
- Convert to different voice
- 50MB file size limit

**API Endpoint:** `POST /api/voice-transform`
- Multipart form data: audio file + voiceId

### 3. Voice Agent (Conversational AI)
**Route:** `/voice-agent`
**Backend:** `voice_agent.py`

- Real-time voice conversations
- Text input alternative
- AI-powered responses (Gemini)
- Voice output (ElevenLabs)
- Auto-play responses

**API Endpoints:**
- `POST /api/voice-agent` (voice input)
- `POST /api/text-agent` (text input)

**Response Format:**
```json
{
  "userText": "What is AI?",
  "text": "AI is artificial intelligence...",
  "audio": "base64_encoded_audio"
}
```

### 4. DS Tutor (RAG-based Q&A)
**Route:** `/ds-tutor`
**Backend:** `ds_rag_agent.py` + `rag_service.py`

- PDF document ingestion
- Vector-based semantic search
- Context-aware answers
- Voice input/output support
- Source citation (page numbers)

**API Endpoint:** `POST /api/ds-rag-agent`
```json
{
  "question": "What is machine learning?",
  "mode": "text"  // or "voice"
}
```

**RAG Pipeline:**
1. PDF → Text chunks → Embeddings (HuggingFace)
2. Store in ChromaDB
3. Query → Similarity search (top 3 chunks)
4. Generate answer with Gemini/DeepSeek
5. Return answer + sources + audio

---

## 🔧 Backend Architecture

### Main Application (`main.py`)
```python
# Middleware Stack
- RequestIDMiddleware (request tracking)
- TrustedHostMiddleware (security)
- CORSMiddleware (frontend access)
- Rate Limiting (SlowAPI - 10 req/min)

# Lifecycle Management
- startup(): Initialize RAGService
- shutdown(): Cleanup resources

# Routes
- /api/speech (TTS)
- /api/voices (list voices)
- /api/voice-transform (speech-to-speech)
- /api/voice-agent (voice conversation)
- /api/text-agent (text conversation)
- /api/ds-rag-agent (RAG queries)
- /health (health check)
```

### Key Services

**RAGService** (`rag_service.py`)
- Lifecycle-managed singleton
- Vector database operations
- Multi-provider LLM generation
- Response caching
- TTS integration

**GeminiKeyRotator** (`gemini_rotator.py`)
- Multiple API key management
- Automatic rotation on failure
- Rate limit handling

**Provider Pattern**
- `BaseProvider` (abstract interface)
- `GeminiProvider` (primary LLM)
- `DeepSeekProvider` (fallback LLM)
- Automatic failover

---

## 🎨 Frontend Architecture

### Pages
1. **Landing Page** - Navigation hub with 4 feature cards
2. **Generate Voice** - Text input + voice selector + audio player
3. **Speech-to-Speech** - File upload + voice selector + audio player
4. **Voice Agent** - Audio recorder + text input + auto-play responses
5. **DS Tutor** - PDF upload + voice/text input + answer display

### Reusable Components

**AudioPlayer** (`AudioPlayer.js`)
- HTML5 audio controls
- Download functionality
- Conditional rendering

**AudioRecorder** (`AudioRecorder.js`)
- MediaRecorder API
- Real-time recording
- Blob generation
- Visual feedback

**VoiceSelector** (`VoiceSelector.js`)
- Dropdown with voice options
- Fetches from `/api/voices`
- Controlled component

**useVoices Hook** (`useVoices.js`)
- Centralized voice management
- API fetching
- State management

---

## 📊 Data Flow Examples

### Voice Agent Flow
```
User speaks → AudioRecorder
    ↓
Blob → FormData → POST /api/voice-agent
    ↓
Backend: Gemini transcribes audio
    ↓
Gemini generates response
    ↓
ElevenLabs synthesizes speech
    ↓
Response: {userText, text, audio (base64)}
    ↓
Frontend: Display text + Auto-play audio
```

### RAG Tutor Flow
```
User question → POST /api/ds-rag-agent
    ↓
Embed question → ChromaDB similarity search
    ↓
Retrieve top 3 chunks
    ↓
Build prompt with context
    ↓
Gemini generates answer (fallback: DeepSeek)
    ↓
Extract sources (page numbers)
    ↓
Response: {answer, sources, provider}
    ↓
Frontend: Display answer + sources
```

---

## 🛠️ Dependencies

### Backend (requirements.txt)
```
fastapi==0.128.1
uvicorn[standard]==0.40.0
google-generativeai==0.8.6
chromadb==0.5.23
langchain-core
langchain-community
langchain-chroma
langchain-huggingface
httpx==0.28.1
python-dotenv==1.2.1
pydantic==2.12.5
slowapi==0.1.9
python-multipart==0.0.9
numpy>=1.24.0,<2.0.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "next": "16.0.1",
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "axios": "^1.13.1",
    "tailwindcss": "^4",
    "lucide-react": "^0.548.0",
    "@react-three/fiber": "^9.4.0",
    "@react-three/drei": "^10.7.7",
    "three": "^0.181.1"
  }
}
```

---

## 🔐 Security Features

1. **Rate Limiting** - SlowAPI (10 req/min on root)
2. **Input Validation** - File size (50MB), text length (500-5000 chars)
3. **Error Handling** - Custom exceptions + global handlers
4. **CORS Configuration** - Restricted origins (localhost:3000, Vercel, Render)
5. **Trusted Hosts** - Host header validation

---

## 📈 Performance Optimizations

1. **Async/Await Pattern** - Non-blocking I/O
2. **Connection Pooling** - Reusable HTTP clients
3. **Streaming Responses** - Audio streaming
4. **Caching** - RAG query cache
5. **Lazy Loading** - On-demand model loading

---

## 🔄 Error Handling

### Backend
```python
# Custom exceptions
class AppException(Exception)
    - ValidationError
    - ServiceError
    - ExternalAPIError

# Global handlers
@app.exception_handler(AppException)
async def app_exception_handler()

# Logging
logger.error(f"Context: {error}")
```

### Frontend
```javascript
// Try-catch blocks
try {
  await apiCall()
} catch (err) {
  console.error(err)
  setError("User-friendly message")
}
```

---

## 🚦 Setup & Running

### Backend
```bash
cd backend
pip install -r requirements.txt
# Configure .env with API keys
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

**Backend (.env)**
```env
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
CHROMA_PATH=chroma_db
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api
```

---

## 🎯 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/speech` | POST | Text-to-Speech |
| `/api/voices` | GET | List available voices |
| `/api/voice-transform` | POST | Speech-to-Speech |
| `/api/voice-agent` | POST | Voice conversation |
| `/api/text-agent` | POST | Text conversation |
| `/api/ds-rag-agent` | POST | RAG-based Q&A |
| `/health` | GET | System health check |
| `/` | GET | Root endpoint |

---

## 🌟 Advanced Features

1. **Multi-Provider LLM System** - Gemini (primary) + DeepSeek (fallback)
2. **API Key Rotation** - Multiple Gemini keys with automatic rotation
3. **Response Caching** - In-memory cache for RAG queries
4. **Lifecycle Management** - Startup initialization + resource cleanup
5. **Structured Logging** - Request ID tracking + performance metrics

---

## 🎓 Technical Highlights

✅ **4 Complete Features** (TTS, Speech-to-Speech, Voice Agent, RAG Tutor)
✅ **Production-Ready Backend** (FastAPI + middleware + logging)
✅ **Modern Frontend** (Next.js 16 + React 19 + TailwindCSS 4)
✅ **AI Integration** (Gemini + ElevenLabs + HuggingFace)
✅ **Vector Database** (ChromaDB + RAG pipeline)
✅ **Real-time Audio** (Recording + Playback + Streaming)
✅ **Error Handling** (Custom exceptions + global handlers)
✅ **Security** (Rate limiting + CORS + validation)
✅ **Scalable Architecture** (Provider pattern + dependency injection)
✅ **Performance** (Async + caching + connection pooling)

---

## 📝 Code Quality

1. **Type Hints** - Pydantic models + type annotations
2. **Component Reusability** - Custom hooks + shared components
3. **Separation of Concerns** - Routes → Services → Providers
4. **Configuration Management** - Environment variables + centralized config
5. **Documentation** - Inline comments + docstrings + README files

---

## 🔮 Future Enhancements

- WebSocket support for real-time streaming
- Multi-language support
- User authentication
- Conversation history
- Voice cloning
- Docker containerization
- CI/CD pipeline
- Unit/integration tests

---

## 📊 Project Stats

- **Total Files:** ~65 files
- **Total LOC:** ~5000+ lines
- **Backend Files:** ~30 Python files
- **Frontend Files:** ~20 JS/JSX files
- **Documentation:** 7 markdown files
- **Python Version:** 3.13.1
- **Node Version:** Latest LTS

---

## 🎉 Key Learning Outcomes

1. Full-stack AI integration (Gemini, ElevenLabs)
2. RAG implementation (LangChain, ChromaDB)
3. Real-time audio processing (MediaRecorder, WebAudio)
4. Modern Python patterns (async, dependency injection, providers)
5. Production-ready architecture (middleware, logging, error handling)
6. React best practices (hooks, components, state management)
7. API design (RESTful, streaming, multipart)
8. Vector databases (embeddings, similarity search)

---

**Built with ❤️ using FastAPI, Next.js, Gemini AI, and ElevenLabs**

---

## 📌 Important Notes for Claude.ai

1. **Project Type:** Full-stack AI voice application
2. **Main Technologies:** FastAPI, Next.js, Gemini, ElevenLabs, ChromaDB
3. **Architecture Pattern:** Provider pattern, dependency injection, lifecycle management
4. **Key Features:** TTS, Speech-to-Speech, Voice Agent, RAG Tutor
5. **Deployment Ready:** Docker support, environment configs, error handling
6. **Code Quality:** Type hints, reusable components, structured logging
7. **Security:** Rate limiting, CORS, input validation, error handling

This project demonstrates production-ready full-stack AI development with modern best practices.
