# How to Add Multiple Gemini API Keys on Render

## Problem
You're hitting rate limits with only 1 Gemini API key.

## Solution
Add multiple Gemini API keys to rotate automatically.

---

## Step 1: Get More Gemini API Keys

1. Go to https://aistudio.google.com/apikey
2. Create 2-3 more API keys (free tier allows multiple keys)
3. Copy each key

---

## Step 2: Add Keys to Render Environment Variables

Go to your Render dashboard → Your service → Environment

Add these variables:

```
GEMINI_API_KEY_1=your_first_key_here
GEMINI_API_KEY_2=your_second_key_here
GEMINI_API_KEY_3=your_third_key_here
```

**OR keep your existing setup:**
```
GEMINI_API_KEY=your_key_here
```

The code automatically detects both formats!

---

## How It Works

The `GeminiKeyRotator` class:
1. Tries to load `GEMINI_API_KEY_1` through `GEMINI_API_KEY_8`
2. Falls back to `GEMINI_API_KEY` if numbered keys don't exist
3. Rotates keys automatically when rate limit is hit
4. Retries with exponential backoff

---

## What Changed

✅ **Problem 1 Fixed:** Better error logging shows why RAG fails
✅ **Problem 2 Fixed:** Switched to `gemini-1.5-flash-8b` (higher limits)
✅ **Problem 3 Fixed:** Replaced ElevenLabs with gTTS (free, works on servers)

---

## Deploy

```bash
git add .
git commit -m "Fix: Better logging, gemini-1.5-flash-8b, gTTS instead of ElevenLabs"
git push origin main
```

Then add the API keys on Render and redeploy!
