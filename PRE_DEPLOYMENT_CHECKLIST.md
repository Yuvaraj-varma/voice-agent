# ✅ Pre-Deployment Checklist

## Before You Deploy - MUST DO

### 1. ⚠️ CRITICAL: Remove Sensitive Data from Git
```bash
# Check if .env is in .gitignore
git check-ignore backend/.env
git check-ignore frontend/.env.local

# If they show up in git status, remove them:
git rm --cached backend/.env
git rm --cached frontend/.env.local
git commit -m "Remove sensitive files"
```

### 2. 🔐 Verify API Keys Are NOT in Code
```bash
# Search for hardcoded keys
cd backend
findstr /s /i "sk-" *.py
findstr /s /i "AIza" *.py

# Should return NOTHING or only from .env file
```

### 3. ✅ Test Locally First
```bash
# Backend
cd backend
..\.venv\Scripts\activate
uvicorn main:app --reload

# Test: http://127.0.0.1:8000/health
# Test: http://127.0.0.1:8000/api/voices

# Frontend
cd frontend
npm run dev

# Test: http://localhost:3000
```

### 4. 📝 Update CORS for Production
**File:** `backend/main.py`

Current (Development):
```python
allow_origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://*.onrender.com",
]
```

After deployment, update to your exact URLs:
```python
allow_origins=[
    "https://your-app.vercel.app",  # Your actual Vercel URL
]
```

### 5. 🔍 Check Requirements.txt
```bash
cd backend
type requirements.txt
```

Verify all packages are listed with versions.

### 6. 📦 Test Frontend Build
```bash
cd frontend
npm run build

# Should complete without errors
```

### 7. 🗂️ Verify File Structure
```
Voice-Agent-system/
├── backend/
│   ├── main.py ✅
│   ├── requirements.txt ✅
│   ├── runtime.txt ✅
│   ├── .env (NOT in git) ✅
│   └── routes/ ✅
└── frontend/
    ├── package.json ✅
    ├── next.config.mjs ✅
    ├── .env.local (NOT in git) ✅
    └── src/ ✅
```

### 8. 🔑 Prepare Environment Variables

**Backend (Render):**
```
GEMINI_API_KEY=AIzaSyCgpl42UqqfuvoHJoaPhTNf31ub8JY7AZE
ELEVENLABS_API_KEY=44ee3de05b108f6dfef88c5b698f8594134d7407abbd006470415bc68df44431
DEEPSEEK_API_KEY=sk-ffae1f71c2ed46da9a47c361df72d412
CHROMA_PATH=chroma_db
```

**Frontend (Vercel):**
```
NEXT_PUBLIC_BACKEND_URL=https://your-backend.onrender.com/api
```

### 9. 📊 Test All Features Work
- [ ] Generate Voice (Text-to-Speech)
- [ ] Speech-to-Speech (Voice Transform)
- [ ] Voice Agent (Conversational AI)
- [ ] DS Tutor (RAG Q&A)

### 10. 🚀 Git Status Check
```bash
git status
# Should show: "nothing to commit, working tree clean"

git log --oneline -1
# Should show your latest commit
```

---

## ⚠️ IMPORTANT WARNINGS

### DO NOT Deploy If:
- ❌ `.env` files are tracked in git
- ❌ API keys are hardcoded in source files
- ❌ Local tests are failing
- ❌ `npm run build` fails
- ❌ Backend health check fails

### MUST DO Before Deploy:
- ✅ All tests pass locally
- ✅ No sensitive data in git
- ✅ CORS configured correctly
- ✅ Environment variables ready
- ✅ Latest code pushed to GitHub

---

## 🎯 Deployment Order

1. **Push to GitHub** (if not done)
   ```bash
   git push origin main
   ```

2. **Deploy Backend First** (Render)
   - Get backend URL
   - Test: `https://your-backend.onrender.com/health`

3. **Deploy Frontend** (Vercel)
   - Use backend URL in environment variable
   - Test: `https://your-frontend.vercel.app`

4. **Update CORS** (if needed)
   - Add exact frontend URL to backend CORS
   - Redeploy backend

---

## 📋 Quick Pre-Deploy Commands

```bash
# 1. Check git status
git status

# 2. Verify .env is ignored
git check-ignore backend/.env

# 3. Test backend
cd backend && ..\.venv\Scripts\activate && python test_endpoints.py

# 4. Test frontend build
cd frontend && npm run build

# 5. Push to GitHub
git push origin main
```

---

## ✅ Ready to Deploy?

If all checks pass:
1. Follow `DEPLOYMENT_CHECKLIST.md` for step-by-step deployment
2. Start with backend (Render)
3. Then deploy frontend (Vercel)

**Estimated Time:** 15-20 minutes

---

## 🆘 Need Help?

- Backend issues: Check Render logs
- Frontend issues: Check Vercel logs
- CORS errors: Update `main.py` with exact URLs
- API key errors: Verify environment variables in dashboard
