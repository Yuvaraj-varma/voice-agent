# 📦 Project Requirements & Dependencies

## Backend Requirements (Python 3.13)

### Core Framework
```
fastapi==0.128.1          # Web framework
uvicorn[standard]==0.40.0 # ASGI server
python-dotenv==1.2.1      # Environment variables
httpx==0.28.1             # HTTP client
pydantic==2.12.5          # Data validation
slowapi==0.1.9            # Rate limiting
```

### AI/ML Services
```
google-generativeai==0.8.6  # Gemini API (STT, LLM)
sentence-transformers==2.7.0 # Text embeddings
torch==2.5.1+cpu            # PyTorch (CPU only)
```

### Vector Database
```
chromadb==1.4.1           # Vector database
```

### LangChain (RAG)
```
langchain-core==1.2.9
langchain-community==0.4.1
langchain-chroma==0.1.4
langchain-huggingface==0.1.2
```

### Other Dependencies
```
numpy>=1.24.0,<2.0.0      # Numerical computing
```

### Total Backend Packages: 150+ (including dependencies)

---

## Frontend Requirements (Node.js)

### Core Framework
```
next@16.0.1               # React framework
react@19.2.0              # UI library
react-dom@19.2.0          # React DOM
```

### Styling
```
tailwindcss@4.1.16        # CSS framework
@tailwindcss/postcss@4.1.16
```

### HTTP Client
```
axios@1.13.5              # API requests
```

### UI Components
```
lucide-react@0.548.0      # Icons
```

### 3D Graphics (Optional)
```
three@0.181.1             # 3D library
@react-three/fiber@9.4.0  # React Three.js
@react-three/drei@10.7.7  # Three.js helpers
```

### Total Frontend Packages: 12 direct dependencies

---

## Installation Commands

### Backend Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

---

## System Requirements

### Minimum
- **Python:** 3.13+
- **Node.js:** 18.0+
- **RAM:** 4GB
- **Storage:** 2GB free space

### Recommended
- **Python:** 3.13
- **Node.js:** 20.0+
- **RAM:** 8GB
- **Storage:** 5GB free space

---

## API Keys Required

### Essential
```
GEMINI_API_KEY          # Google Gemini (Free tier available)
ELEVENLABS_API_KEY      # ElevenLabs TTS (Free tier: 10k chars/month)
```

### Optional
```
DEEPSEEK_API_KEY        # Alternative LLM
HUGGINGFACE_API_KEY     # HuggingFace models
OPENAI_API_KEY          # OpenAI (if using GPT)
```

---

## Development Tools

### Backend
```bash
# Run server
uvicorn main:app --reload

# Test endpoints
python test_endpoints.py

# Check packages
pip list
```

### Frontend
```bash
# Development server
npm run dev

# Production build
npm run build

# Start production
npm start

# Check packages
npm list --depth=0
```

---

## Package Sizes

### Backend
- **Total Size:** ~2.5GB (with PyTorch CPU)
- **Without PyTorch:** ~500MB
- **Core packages:** ~200MB

### Frontend
- **node_modules:** ~800MB
- **Build output:** ~50MB

---

## Key Features by Package

### Backend
| Package | Feature |
|---------|---------|
| FastAPI | REST API endpoints |
| Gemini | Speech-to-Text, LLM responses |
| ElevenLabs | Text-to-Speech (via API) |
| ChromaDB | Vector storage for RAG |
| LangChain | RAG pipeline |
| Sentence Transformers | Text embeddings |

### Frontend
| Package | Feature |
|---------|---------|
| Next.js | Server-side rendering, routing |
| React | UI components |
| TailwindCSS | Styling |
| Axios | API calls |
| Lucide | Icons |

---

## Deployment Requirements

### Render (Backend)
```
Runtime: Python 3.13
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
Memory: 512MB minimum (Free tier)
```

### Vercel (Frontend)
```
Framework: Next.js
Build: npm run build
Output: .next/
Node: 18.x or higher
```

---

## Quick Check Commands

### Verify Backend Installation
```bash
cd backend
.venv\Scripts\activate
python -c "import fastapi, uvicorn, google.generativeai, httpx, chromadb; print('✅ All imports OK')"
```

### Verify Frontend Installation
```bash
cd frontend
npm run build
# Should complete without errors
```

### Test Everything
```bash
# Backend
cd backend
.venv\Scripts\activate
python test_endpoints.py

# Frontend
cd frontend
npm run dev
# Open http://localhost:3000
```

---

## Troubleshooting

### Backend Issues
```bash
# Reinstall packages
pip install -r requirements.txt --force-reinstall

# Clear cache
pip cache purge

# Check Python version
python --version  # Should be 3.13+
```

### Frontend Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next

# Check Node version
node --version  # Should be 18+
```

---

## Summary

**Backend:** 150+ Python packages (~2.5GB)
**Frontend:** 12 direct packages (~800MB)
**Total Project Size:** ~3.5GB
**API Keys:** 2 required (Gemini, ElevenLabs)
**Development Time:** 15 min setup
