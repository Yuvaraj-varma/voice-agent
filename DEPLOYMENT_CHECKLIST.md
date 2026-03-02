# 🚀 Deployment Checklist - Vercel + Render

## ✅ Before You Start

### 1. **Accounts Needed** (Create These First)
- [ ] Vercel account: https://vercel.com/signup (Sign in with GitHub)
- [ ] Render account: https://render.com/register (Sign in with GitHub)

### 2. **API Keys Ready** (You'll need these)
- [ ] GEMINI_API_KEY
- [ ] ELEVENLABS_API_KEY
- [ ] DEEPSEEK_API_KEY (optional)

### 3. **Code Updated**
- [x] Backend CORS allows Vercel domains ✅
- [x] TrustedHost allows all hosts ✅

---

## 📝 Deployment Steps

### **PART 1: Deploy Backend to Render** (Do This First!)

#### Step 1: Go to Render
1. Visit: https://dashboard.render.com
2. Click "New +" → "Web Service"

#### Step 2: Connect GitHub
1. Click "Connect account" → Select GitHub
2. Find and select: `voice-agent` repository
3. Click "Connect"

#### Step 3: Configure Service
```
Name: voice-agent-backend
Region: Choose closest to you
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Step 4: Add Environment Variables
Click "Advanced" → "Add Environment Variable":
```
GEMINI_API_KEY = your_gemini_key_here
ELEVENLABS_API_KEY = your_elevenlabs_key_here
DEEPSEEK_API_KEY = your_deepseek_key_here
CHROMA_PATH = chroma_db
```

#### Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Copy your backend URL: `https://voice-agent-backend-xxxx.onrender.com`

---

### **PART 2: Deploy Frontend to Vercel**

#### Step 1: Install Vercel CLI
```powershell
npm install -g vercel
```

#### Step 2: Login to Vercel
```powershell
vercel login
```
(Opens browser, sign in with GitHub)

#### Step 3: Deploy Frontend
```powershell
cd C:\Users\Yuvaraj\Voice-Agent-system\frontend
vercel
```

#### Step 4: Answer Questions
```
? Set up and deploy "frontend"? Y
? Which scope? (Your account)
? Link to existing project? N
? What's your project's name? voice-agent
? In which directory is your code located? ./
? Want to override settings? N
```

#### Step 5: Add Environment Variable
```powershell
vercel env add NEXT_PUBLIC_BACKEND_URL
```
Enter: `https://your-backend-url.onrender.com/api`

#### Step 6: Deploy to Production
```powershell
vercel --prod
```

---

## 🎯 After Deployment

### Test Your Live App
1. **Frontend URL:** `https://voice-agent-xxxx.vercel.app`
2. **Backend URL:** `https://voice-agent-backend-xxxx.onrender.com`

### Test Endpoints
```bash
# Health check
curl https://your-backend.onrender.com/health

# Test frontend
Open: https://your-frontend.vercel.app
```

---

## 🔧 Troubleshooting

### Issue: CORS Error
**Fix:** Update backend CORS in `main.py` with your exact Vercel URL:
```python
allow_origins=["https://voice-agent-xxxx.vercel.app"]
```

### Issue: Backend Not Starting
**Check:** Render logs in dashboard
**Common Fix:** Ensure all environment variables are set

### Issue: Frontend Can't Connect
**Fix:** Check `NEXT_PUBLIC_BACKEND_URL` in Vercel dashboard

---

## 📊 What You'll Get

### Live URLs
- **App:** `https://voice-agent.vercel.app`
- **API:** `https://voice-agent-backend.onrender.com`
- **GitHub:** `https://github.com/Yuvaraj-varma/voice-agent`

### For Resume/LinkedIn
```
🚀 Deployed full-stack AI Voice Agent
- Frontend: Next.js on Vercel
- Backend: FastAPI on Render
- Features: TTS, Speech-to-Speech, Voice Agent, RAG Tutor
- Live Demo: https://voice-agent.vercel.app
```

---

## 💰 Cost
- **Vercel:** FREE (Hobby plan)
- **Render:** FREE (with sleep after 15 min inactivity)
- **Upgrade:** $7/month for always-on backend

---

## ⏱️ Time Estimate
- Backend deployment: 10 minutes
- Frontend deployment: 5 minutes
- **Total: 15 minutes** ⚡

---

**Ready to deploy? Start with PART 1 (Backend on Render)!** 🚀
