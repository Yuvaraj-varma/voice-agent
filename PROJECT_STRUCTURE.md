# Voice Agent System - Project Structure

```
Voice-Agent-system/
│
├── backend/                          # FastAPI Backend
│   ├── routes/                       # API Routes
│   │   ├── __init__.py
│   │   ├── text_speech_routes.py    # TTS & Voice endpoints
│   │   ├── voice_transform.py       # Speech-to-Speech
│   │   ├── voice_agent.py           # AI Voice Agent
│   │   └── ds_rag_agent.py          # RAG Tutor
│   │
│   ├── services/                     # Business Logic
│   │   ├── __init__.py
│   │   └── rag_service.py           # RAG Service
│   │
│   ├── providers/                    # AI Providers
│   │   ├── __init__.py
│   │   ├── base_provider.py
│   │   ├── gemini_provider.py
│   │   └── deepseek_provider.py
│   │
│   ├── utils/                        # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── tts.py
│   │   ├── validators.py
│   │   └── gemini_rotator.py
│   │
│   ├── middleware/                   # Middleware
│   │   └── request_id.py
│   │
│   ├── exceptions/                   # Error Handling
│   │   ├── base.py
│   │   └── handlers.py
│   │
│   ├── data/                         # Data Files
│   │   └── ds_notes/
│   │       └── DS_Basics.pdf
│   │
│   ├── chroma_db/                    # Vector Database (gitignored)
│   │   └── chroma.sqlite3
│   │
│   ├── main.py                       # FastAPI App Entry
│   ├── requirements.txt              # Python Dependencies
│   ├── runtime.txt                   # Python Version
│   ├── Dockerfile                    # Docker Config
│   ├── .env                          # Environment Variables (gitignored)
│   ├── .gitignore
│   └── app.log                       # Logs (gitignored)
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── page.js              # Home Page
│   │   │   ├── layout.js            # Root Layout
│   │   │   ├── globals.css          # Global Styles
│   │   │   ├── loading.js           # Loading Component
│   │   │   ├── error.js             # Error Component
│   │   │   │
│   │   │   ├── generate-voice/      # TTS Page
│   │   │   │   └── page.js
│   │   │   │
│   │   │   ├── speech-to-speech/    # Voice Transform Page
│   │   │   │   └── page.js
│   │   │   │
│   │   │   ├── voice-agent/         # AI Agent Page
│   │   │   │   └── page.js
│   │   │   │
│   │   │   └── ds-tutor/            # RAG Tutor Page
│   │   │       └── page.js
│   │   │
│   │   ├── components/               # React Components
│   │   │   ├── AudioPlayer.js
│   │   │   ├── AudioRecorder.js
│   │   │   ├── VoiceSelector.js
│   │   │   ├── ErrorBoundary.js
│   │   │   └── Loading.js
│   │   │
│   │   ├── services/                 # API Services
│   │   │   ├── api.js
│   │   │   ├── voiceApi.js
│   │   │   └── dsTutorApi.js
│   │   │
│   │   ├── hooks/                    # Custom Hooks
│   │   │   └── useVoices.js
│   │   │
│   │   └── config/                   # Configuration
│   │       └── api.js
│   │
│   ├── public/                       # Static Assets
│   │   ├── talking-face.png
│   │   ├── robot.png
│   │   └── *.svg
│   │
│   ├── .next/                        # Next.js Build (gitignored)
│   ├── node_modules/                 # Dependencies (gitignored)
│   ├── package.json                  # NPM Dependencies
│   ├── package-lock.json
│   ├── next.config.mjs               # Next.js Config
│   ├── jsconfig.json                 # JS Config
│   ├── postcss.config.mjs            # PostCSS Config
│   ├── Dockerfile                    # Docker Config
│   ├── .env.local                    # Environment Variables (gitignored)
│   ├── .gitignore
│   └── README.md
│
├── .venv/                            # Python Virtual Environment (gitignored)
│
├── .gitignore                        # Root Gitignore
├── docker-compose.yml                # Docker Compose
├── README.md                         # Project README
├── LICENSE                           # MIT License
│
├── DEPLOYMENT.md                     # Deployment Guide
├── DEPLOYMENT_CHECKLIST.md           # Deployment Steps
├── PRE_DEPLOYMENT_CHECKLIST.md       # Pre-Deploy Checks
├── PROJECT_DOCUMENTATION.md          # Full Documentation
├── SYSTEM_STATUS.md                  # System Status
├── ERROR_FIXES_SUMMARY.md            # Error Fixes
├── IMPROVEMENTS.md                   # Improvements Log
│
├── test_endpoints.py                 # Backend Test Script
└── .git/                             # Git Repository

```

## Key Files

### Backend
- **main.py** - FastAPI application entry point
- **requirements.txt** - Python dependencies (25 packages)
- **runtime.txt** - Python 3.13.1
- **.env** - API keys (ELEVENLABS, GEMINI, DEEPSEEK)

### Frontend
- **package.json** - Node dependencies (12 packages)
- **next.config.mjs** - Next.js configuration
- **.env.local** - Backend URL configuration

### Configuration
- **docker-compose.yml** - Multi-container setup
- **Dockerfile** (backend & frontend) - Container configs

## Dependencies

### Backend (Python)
```
fastapi==0.128.1
uvicorn==0.40.0
google-generativeai==0.8.6
torch==2.5.1
sentence-transformers==2.7.0
chromadb==1.4.1
langchain-core==1.2.9
langchain-community==0.4.1
langchain-chroma==1.1.0
langchain-huggingface==1.2.0
httpx==0.28.1
python-dotenv==1.2.1
pydantic==2.12.5
slowapi==0.1.9
numpy>=1.24.0,<2.0.0
```

### Frontend (Node)
```
next@16.0.1
react@19.2.0
react-dom@19.2.0
tailwindcss@4.1.16
axios@1.13.5
lucide-react@0.548.0
@react-three/fiber@9.4.0
@react-three/drei@10.7.7
three@0.181.1
```

## Total Files
- Backend: ~30 Python files
- Frontend: ~20 JS/JSX files
- Config: ~15 files
- Documentation: 7 markdown files
- Total LOC: ~5000+ lines

## Git Status
- Branch: main
- Remote: https://github.com/Yuvaraj-varma/voice-agent.git
- Last Commit: "Fix: Add langchain-chroma and clean .env file"
- Status: Clean (ready to push)
