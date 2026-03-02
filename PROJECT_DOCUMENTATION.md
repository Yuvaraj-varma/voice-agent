# Voice Agent System - Complete Project Documentation

## 🎯 Project Overview
A full-stack AI Voice Agent system that enables real-time voice interactions, text-to-speech conversion, speech-to-speech transformation, and an intelligent RAG-based Data Science tutor. Built with modern technologies for production-ready AI voice applications.

---

## 🏗️ Architecture

### Tech Stack
**Backend:**
- FastAPI (Python web framework)
- Google Gemini AI (LLM & Speech-to-Text)
- ElevenLabs (Text-to-Speech)
- ChromaDB (Vector database)
- LangChain (RAG framework)
- HuggingFace Embeddings (sentence-transformers)

**Frontend:**
- Next.js 16 (React framework)
- TailwindCSS 4 (Styling)
- Axios (HTTP client)
- React Three Fiber (3D graphics)

---

## 📁 Project Structure

```
Voice-Agent-system/
├── backend/
│   ├── routes/              # API endpoints
│   │   ├── text_speech_routes.py      # TTS & voice listing
│   │   ├── voice_transform.py         # Speech-to-Speech
│   │   ├── voice_agent.py             # Conversational agent
│   │   └── ds_rag_agent.py            # RAG-based tutor
│   ├── services/
│   │   └── rag_service.py             # RAG pipeline
│   ├── providers/
│   │   ├── gemini_provider.py         # Gemini integration
│   │   └── deepseek_provider.py       # DeepSeek fallback
│   ├── utils/
│   │   ├── gemini_rotator.py          # API key rotation
│   │   ├── logger.py                  # Logging system
│   │   └── tts.py                     # TTS utilities
│   ├── middleware/
│   │   └── request_id.py              # Request tracking
│   ├── exceptions/
│   │   ├── base.py                    # Custom exceptions
│   │   └── handlers.py                # Error handlers
│   ├── chroma_db/                     # Vector database storage
│   ├── data/ds_notes/                 # PDF documents
│   └── main.py                        # FastAPI app entry
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── generate-voice/        # Text-to-Speech UI
    │   │   ├── speech-to-speech/      # Voice transformation UI
    │   │   ├── voice-agent/           # Conversational agent UI
    │   │   ├── ds-tutor/              # RAG tutor UI
    │   │   └── page.js                # Landing page
    │   ├── components/
    │   │   ├── AudioPlayer.js         # Audio playback
    │   │   ├── AudioRecorder.js       # Voice recording
    │   │   ├── VoiceSelector.js       # Voice selection
    │   │   └── ErrorBoundary.js       # Error handling
    │   ├── services/
    │   │   ├── api.js                 # API client
    │   │   ├── voiceApi.js            # Voice endpoints
    │   │   └── dsTutorApi.js          # Tutor endpoints
    │   └── hooks/
    │       └── useVoices.js           # Voice management hook
    └── package.json
```

---

## 🚀 Features Implemented

### 1. **Text-to-Speech (Generate Voice)** 🗣️
**Route:** `/generate-voice`
**Backend:** `text_speech_routes.py`

**Features:**
- Convert text input to natural speech
- 500 character limit
- Multiple voice selection (ElevenLabs voices)
- Real-time audio generation
- Download generated audio

**Technical Flow:**
1. User enters text in frontend
2. POST request to `/api/speech` with text + voiceId
3. Backend calls ElevenLabs API
4. Returns audio stream (MP3)
5. Frontend plays audio with AudioPlayer component

---

### 2. **Speech-to-Speech Conversion** 💬
**Route:** `/speech-to-speech`
**Backend:** `voice_transform.py`

**Features:**
- Upload audio file (WAV, MP3, WEBM)
- Transcribe using Gemini AI
- Convert to different voice using ElevenLabs
- 50MB file size limit

**Technical Flow:**
1. User uploads audio file
2. POST to `/api/voice-transform` with file + voiceId
3. Gemini transcribes audio to text
4. ElevenLabs converts text to new voice
5. Returns transformed audio

---

### 3. **Voice Agent (Conversational AI)** 🎙️
**Route:** `/voice-agent`
**Backend:** `voice_agent.py`

**Features:**
- Real-time voice conversations
- Text input alternative
- AI-powered responses (Gemini)
- Voice output (ElevenLabs)
- Auto-play responses

**Technical Flow:**
1. User speaks or types question
2. Voice: POST to `/api/voice-agent` → Gemini transcribes
3. Text: POST to `/api/text-agent` → Direct processing
4. Gemini generates AI response
5. ElevenLabs synthesizes speech
6. Returns JSON: `{userText, text, audio}`
7. Frontend auto-plays audio response

**Architecture:**
- `BaseVoiceAgent` (Abstract class)
- `GeminiVoiceAgent` (Implementation)
- `VoiceAgentOrchestrator` (Request handler)
- Dependency injection pattern

---

### 4. **DS Tutor (RAG-based Q&A)** 📚
**Route:** `/ds-tutor`
**Backend:** `ds_rag_agent.py` + `rag_service.py`

**Features:**
- PDF document ingestion
- Vector-based semantic search
- Context-aware answers
- Voice input/output support
- Source citation (page numbers)

**Technical Flow:**
1. **Ingestion:** PDF → Text chunks → Embeddings → ChromaDB
2. **Query:** User question → Embedding → Similarity search
3. **Retrieval:** Top 3 relevant chunks
4. **Generation:** Gemini/DeepSeek generates answer from context
5. **Response:** Text + Audio + Sources

**RAG Pipeline:**
```python
# Embeddings
HuggingFaceEmbeddings("all-MiniLM-L6-v2")

# Vector Store
ChromaDB (persistent storage)

# Retrieval
similarity_search(question, k=3)

# Generation
Gemini (primary) → DeepSeek (fallback)
```

**Provider Pattern:**
- `BaseProvider` interface
- `GeminiProvider` (primary)
- `DeepSeekProvider` (fallback)
- Automatic failover

---

## 🔧 Backend Architecture

### Main Application (`main.py`)
```python
# Middleware Stack
- RequestIDMiddleware (request tracking)
- TrustedHostMiddleware (security)
- CORSMiddleware (frontend access)
- Rate Limiting (SlowAPI)

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

**Logger** (`logger.py`)
- Structured logging
- Request ID tracking
- Error context capture

---

## 🎨 Frontend Architecture

### Page Structure
1. **Landing Page** (`page.js`)
   - Navigation hub
   - 4 feature cards
   - Gradient design

2. **Generate Voice** (`generate-voice/page.js`)
   - Text input with character counter
   - Voice selector dropdown
   - Audio player with download

3. **Speech-to-Speech** (`speech-to-speech/page.js`)
   - File upload
   - Voice selector
   - Audio player

4. **Voice Agent** (`voice-agent/page.js`)
   - Audio recorder component
   - Text input form
   - Real-time transcription display
   - Auto-play responses

5. **DS Tutor** (`ds-tutor/page.js`)
   - PDF upload
   - Voice/text input
   - Answer display with sources
   - Audio playback

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

## 🔐 Security Features

1. **Rate Limiting**
   - SlowAPI integration
   - 10 requests/minute on root
   - Per-endpoint limits

2. **Input Validation**
   - File size limits (50MB)
   - File type validation
   - Text length limits (500-5000 chars)

3. **Error Handling**
   - Custom exception classes
   - Global exception handlers
   - Structured error responses

4. **CORS Configuration**
   - Restricted origins (localhost:3000)
   - Credential support
   - Method/header whitelisting

5. **Trusted Hosts**
   - Localhost only
   - Host header validation

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

## 🛠️ Key Technologies & Libraries

### Backend Dependencies
```
fastapi==0.128.1          # Web framework
uvicorn==0.40.0           # ASGI server
google-generativeai==0.8.6 # Gemini AI
langchain==1.2.9          # RAG framework
chromadb==1.4.1           # Vector database
sentence-transformers==5.2.2 # Embeddings
httpx==0.28.1             # Async HTTP
slowapi==0.1.9            # Rate limiting
pydantic==2.12.5          # Data validation
python-dotenv==1.2.1      # Environment variables
```

### Frontend Dependencies
```
next==16.0.1              # React framework
react==19.2.0             # UI library
axios==1.13.1             # HTTP client
tailwindcss==4            # Styling
lucide-react==0.548.0     # Icons
@react-three/fiber==9.4.0 # 3D graphics
```

---

## 🌟 Advanced Features

### 1. **Multi-Provider LLM System**
- Primary: Gemini (fast, reliable)
- Fallback: DeepSeek (backup)
- Automatic failover
- Latency tracking

### 2. **API Key Rotation**
- Multiple Gemini keys
- Automatic rotation on failure
- Rate limit handling
- Health tracking

### 3. **Response Caching**
- In-memory cache for RAG queries
- Reduces API calls
- Faster responses

### 4. **Lifecycle Management**
- Startup initialization
- Resource cleanup on shutdown
- Connection pooling

### 5. **Structured Logging**
- Request ID tracking
- Performance metrics
- Error context
- Log levels (INFO, WARNING, ERROR)

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

## 📈 Performance Optimizations

1. **Async/Await Pattern**
   - Non-blocking I/O
   - Concurrent request handling
   - httpx.AsyncClient

2. **Connection Pooling**
   - Reusable HTTP clients
   - Reduced latency

3. **Streaming Responses**
   - Audio streaming
   - Memory efficient

4. **Caching**
   - RAG query cache
   - Voice list cache

5. **Lazy Loading**
   - On-demand model loading
   - Resource optimization

---

## 🔄 Error Handling Strategy

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

// Error boundaries
<ErrorBoundary>
  <Component />
</ErrorBoundary>
```

---

## 🚦 Development Workflow

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Configure .env with API keys
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
```env
# Backend (.env)
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
CHROMA_PATH=chroma_db

# Frontend (.env.local)
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api
```

---

## 🎓 Learning Outcomes

This project demonstrates:
1. **Full-stack AI integration** (Gemini, ElevenLabs)
2. **RAG implementation** (LangChain, ChromaDB)
3. **Real-time audio processing** (MediaRecorder, WebAudio)
4. **Modern Python patterns** (async, dependency injection, providers)
5. **Production-ready architecture** (middleware, logging, error handling)
6. **React best practices** (hooks, components, state management)
7. **API design** (RESTful, streaming, multipart)
8. **Vector databases** (embeddings, similarity search)

---

## 📝 Code Quality Features

1. **Type Hints** (Python)
   - Pydantic models
   - Type annotations
   - Runtime validation

2. **Component Reusability** (React)
   - Custom hooks
   - Shared components
   - Service layer abstraction

3. **Separation of Concerns**
   - Routes → Services → Providers
   - Components → Services → API

4. **Configuration Management**
   - Environment variables
   - Centralized config
   - API base URLs

5. **Documentation**
   - Inline comments
   - Docstrings
   - README files

---

## 🎉 Project Highlights

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

## 🔮 Future Enhancements

- WebSocket support for real-time streaming
- Multi-language support
- User authentication
- Conversation history
- Voice cloning
- Custom voice training
- Mobile app (React Native)
- Docker containerization
- CI/CD pipeline
- Unit/integration tests

---

**Built with ❤️ using FastAPI, Next.js, Gemini AI, and ElevenLabs**
