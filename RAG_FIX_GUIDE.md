# RAG Service Fix - Complete Guide

## ✅ CHANGES MADE

### 1. Fixed `rag_service.py`
- ✅ Added `HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")`
- ✅ Pass `embedding_function` to Chroma()
- ✅ Auto-rebuild from PDFs if loading fails
- ✅ Added `_build_vectorstore()` method with:
  - PyPDFDirectoryLoader
  - RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200)
  - Chroma.from_documents()

### 2. Fixed `requirements.txt`
- ✅ Added `sentence-transformers`
- ✅ Added `pypdf`
- ✅ Added `langchain-text-splitters`

### 3. Updated `.gitignore`
- ✅ Added `chroma_db/` to prevent committing vector DB

---

## 🔧 HOW TO REMOVE chroma_db FROM GIT

Run these commands in your backend directory:

```bash
# Remove from git tracking (keeps local files)
git rm -r --cached chroma_db/

# Commit the removal
git add .gitignore
git commit -m "Remove chroma_db from git tracking"

# Push to remote
git push origin main
```

---

## 🚀 DEPLOY TO RENDER

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Fix RAG service: add embeddings and auto-rebuild"
   git push origin main
   ```

2. **Render will auto-deploy** and:
   - Install new dependencies
   - Build ChromaDB from PDFs on first startup
   - Save to `chroma_db/` directory (ephemeral storage)

3. **Verify on Render:**
   - Check logs for: "Vector store built and saved"
   - Test DS Tutor endpoint

---

## 📝 WHAT HAPPENS NOW

### On Render Startup:
1. Loads HuggingFace embeddings
2. Tries to load existing ChromaDB
3. **If fails** → Auto-builds from `data/ds_notes/*.pdf`
4. Saves to `chroma_db/` (ephemeral, regenerated on restart)

### Environment Variables (already set):
- `PDF_PATH=data/ds_notes`
- `CHROMA_PATH=chroma_db`

---

## ⚠️ IMPORTANT NOTES

1. **Ephemeral Storage:** Render's free tier has ephemeral storage, so ChromaDB rebuilds on each restart (this is fine, takes ~10 seconds)

2. **First Deploy:** Will take longer as it downloads sentence-transformers model (~80MB)

3. **PDFs:** Make sure `data/ds_notes/DS_Basics.pdf` is committed to git

---

## 🧪 TEST LOCALLY (Optional)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Check logs for:
- "Loading HuggingFace embeddings..."
- "Vector store built and saved to: ..."

---

## ✨ DONE!

Your RAG service will now:
- ✅ Load embeddings correctly
- ✅ Auto-rebuild if ChromaDB is missing/corrupted
- ✅ Work on Render without committing chroma_db
