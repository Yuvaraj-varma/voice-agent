# 🚀 Deployment Guide - Voice Agent System

## Quick Deploy Options

### ⭐ Option 1: Vercel + Render (RECOMMENDED)

#### Frontend (Vercel)
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

**Environment Variables in Vercel:**
- `NEXT_PUBLIC_BACKEND_URL` = Your Render backend URL

#### Backend (Render)
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo: `voice-agent`
4. Settings:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `GEMINI_API_KEY`
   - `ELEVENLABS_API_KEY`
   - `DEEPSEEK_API_KEY`
   - `CHROMA_PATH=chroma_db`

**Live URLs:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-app.onrender.com`

---

### ⭐ Option 2: Railway (EASIEST)

1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub repo
4. Select `voice-agent`
5. Railway auto-detects both services
6. Add environment variables in dashboard
7. Done! ✅

**Live URL:** `https://your-app.railway.app`

---

### 🐳 Option 3: Docker Deployment

#### Local Testing
```bash
# Build and run
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

#### Deploy to Any Cloud (AWS, GCP, Azure)
```bash
# Build images
docker build -t voice-agent-backend ./backend
docker build -t voice-agent-frontend ./frontend

# Push to registry
docker tag voice-agent-backend your-registry/voice-agent-backend
docker push your-registry/voice-agent-backend

docker tag voice-agent-frontend your-registry/voice-agent-frontend
docker push your-registry/voice-agent-frontend
```

---

### 🌐 Option 4: Heroku

#### Backend
```bash
cd backend
heroku login
heroku create voice-agent-backend
heroku config:set GEMINI_API_KEY=your_key
heroku config:set ELEVENLABS_API_KEY=your_key
git push heroku main
```

#### Frontend
```bash
cd frontend
heroku create voice-agent-frontend
heroku config:set NEXT_PUBLIC_BACKEND_URL=https://voice-agent-backend.herokuapp.com/api
git push heroku main
```

---

## 📋 Pre-Deployment Checklist

### Backend
- [ ] All API keys in environment variables
- [ ] CORS configured for frontend URL
- [ ] Database/ChromaDB persistent storage
- [ ] Health check endpoint working (`/health`)
- [ ] Rate limiting configured

### Frontend
- [ ] Backend URL in environment variable
- [ ] Build succeeds (`npm run build`)
- [ ] No hardcoded API keys
- [ ] Error boundaries in place

---

## 🔐 Environment Variables

### Backend (.env)
```env
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
DEEPSEEK_API_KEY=your_deepseek_key
CHROMA_PATH=chroma_db
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.com/api
```

---

## 🎯 For Interview Demo

### Best Setup:
1. **Frontend:** Vercel (free, fast, professional domain)
2. **Backend:** Render (free tier, always-on with paid plan)

### Demo URLs to Share:
```
Live App: https://voice-agent.vercel.app
GitHub: https://github.com/Yuvaraj-varma/voice-agent
Documentation: https://github.com/Yuvaraj-varma/voice-agent/blob/main/PROJECT_DOCUMENTATION.md
```

### Interview Talking Points:
✅ "Deployed full-stack AI application with CI/CD"
✅ "Containerized with Docker for scalability"
✅ "Implemented proper environment variable management"
✅ "Set up CORS and security middleware"
✅ "Used cloud services (Vercel/Render/Railway)"

---

## 🚨 Common Issues

### Issue: CORS Error
**Fix:** Update backend `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: API Keys Not Working
**Fix:** Ensure environment variables are set in deployment platform dashboard

### Issue: ChromaDB Not Persisting
**Fix:** Use persistent volume/storage in cloud platform

---

## 📊 Monitoring

### Health Check
```bash
curl https://your-backend.com/health
```

### Logs
- **Vercel:** Dashboard → Logs
- **Render:** Dashboard → Logs
- **Railway:** Dashboard → Deployments → Logs

---

## 💰 Cost Estimate

### Free Tier (Good for Interviews)
- Vercel: Free (hobby plan)
- Render: Free (with sleep after inactivity)
- Railway: $5/month credit

### Production (If Needed)
- Vercel Pro: $20/month
- Render: $7/month (always-on)
- Railway: Pay-as-you-go

---

## 🎓 Next Steps

1. Choose deployment platform
2. Set up environment variables
3. Deploy backend first
4. Update frontend with backend URL
5. Deploy frontend
6. Test all features
7. Share live URL in resume/LinkedIn

**Your project will be live and accessible for interviews! 🚀**
