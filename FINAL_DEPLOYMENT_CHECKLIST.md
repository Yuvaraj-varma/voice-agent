# ✅ Deployment Checklist

## 📦 Backend Status

### ✅ Files Ready
- [x] `rag_service.py` - Updated to use Pinecone (lightweight)
- [x] `requirements.txt` - Removed heavy deps (ChromaDB, torch)
- [x] `upload_to_pinecone.py` - Script to upload PDFs
- [x] `main.py` - FastAPI app with RAG service
- [x] `Dockerfile` - Docker config
- [x] `.env` - Has PINECONE_API_KEY

### ⚠️ Before Deploying Backend

1. **Install Pinecone client**
   ```bash
   pip install pinecone-client==5.0.0
   pip install pypdf langchain-community langchain-text-splitters
   ```

2. **Upload PDFs to Pinecone (ONE TIME)**
   ```bash
   python upload_to_pinecone.py
   ```
   This will:
   - Create index "ds-tutor" in Pinecone
   - Upload all PDF chunks from `data/ds_notes/`
   - Takes ~2-5 minutes

3. **Test locally**
   ```bash
   uvicorn main:app --reload
   # Visit http://localhost:8000/health
   # Should show: {"status": "ok", "vector_db": true}
   ```

### 🚀 Deploy Backend to Render

1. Push code to GitHub
2. Go to https://render.com → New Web Service
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance**: Free
4. Environment Variables:
   ```
   GEMINI_API_KEY=AIzaSyCgpl42UqqfuvoHJoaPhTNf31ub8JY7AZE
   PINECONE_API_KEY=pcsk_oPWbS_BsaTGBjWVJSm1bzWAktwZp2vHC3khiTTrnL3qyvGDAuVKbRG8XvU16TkrL33vzg
   DEEPSEEK_API_KEY=sk-ffae1f71c2ed46da9a47c361df72d412
   ```
5. Deploy!

---

## 🎨 Frontend Status

### ✅ Files Ready
- [x] `package.json` - Next.js dependencies
- [x] `.env.local` - Backend URL (needs update after deploy)
- [x] All components in `src/`

### 🚀 Deploy Frontend to Vercel

1. Push code to GitHub
2. Go to https://vercel.com → New Project
3. Import your repo
4. Settings:
   - **Framework**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Environment Variables:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-backend.onrender.com
   ```
   (Replace with your Render backend URL)
6. Deploy!

---

## 📊 Memory Comparison

| Component | Before | After |
|---|---|---|
| Backend RAM | 512MB+ | ~150MB |
| Startup Time | 2-3 min | 10-20 sec |
| Disk Storage | Required | Zero |
| Vector DB | ChromaDB (local) | Pinecone (cloud) |

---

## 🔍 Testing After Deployment

### Backend Health Check
```bash
curl https://your-backend.onrender.com/health
# Expected: {"status": "ok", "vector_db": true}
```

### Frontend Test
1. Visit your Vercel URL
2. Try "RAG Data Science Tutor" feature
3. Ask: "What is machine learning?"
4. Should get answer from your PDF

---

## ⚠️ Common Issues

**"Pinecone index not found"**
- Run `upload_to_pinecone.py` locally first

**"vector_db": false**
- Check PINECONE_API_KEY in Render env vars
- Check Pinecone dashboard for index "ds-tutor"

**Frontend can't connect to backend**
- Update NEXT_PUBLIC_BACKEND_URL in Vercel
- Check CORS settings in `main.py`

---

## 📝 Next Steps

1. ✅ Run `pip install pinecone-client pypdf langchain-community langchain-text-splitters`
2. ✅ Run `python upload_to_pinecone.py`
3. ✅ Test locally: `uvicorn main:app --reload`
4. ✅ Deploy backend to Render
5. ✅ Deploy frontend to Vercel
6. ✅ Update frontend env with backend URL
7. ✅ Test live deployment

**You're ready to deploy! 🚀**
