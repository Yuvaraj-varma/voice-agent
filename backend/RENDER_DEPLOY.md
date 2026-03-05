# Render Deployment Guide

## Environment Variables to Set in Render

Go to your Render service → Environment → Add the following:

```bash
# ElevenLabs (Get new key from: https://elevenlabs.io/app/settings/api-keys)
ELEVENLABS_API_KEY=your_new_elevenlabs_key_here

# Gemini (Get from: https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your_new_gemini_key_here

# Optional: Additional Gemini keys for rotation
GEMINI_API_KEY_1=your_gemini_key_1
GEMINI_API_KEY_2=your_gemini_key_2

# DeepSeek (Optional)
DEEPSEEK_API_KEY=your_deepseek_key

# ChromaDB path (default is fine)
CHROMA_PATH=chroma_db
```

## Important Notes

1. **Your current API keys are INVALID** - You need to generate new ones:
   - ElevenLabs: https://elevenlabs.io/app/settings/api-keys
   - Gemini: https://aistudio.google.com/app/apikey

2. **ChromaDB won't work on Render** unless you:
   - Upload the `chroma_db/` folder to persistent storage
   - OR disable RAG features for now

3. **After setting env vars**, click "Manual Deploy" to redeploy

## Testing After Deployment

```bash
# Test health
curl https://voice-agent-jdiv.onrender.com/health

# Test TTS (after fixing API key)
curl -X POST https://voice-agent-jdiv.onrender.com/api/speech \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=hello&voiceId=21m00Tcm4TlvDq8ikWAM"

# Test voices
curl https://voice-agent-jdiv.onrender.com/api/voices
```

## Quick Fix Checklist

- [ ] Get new ElevenLabs API key
- [ ] Get new Gemini API key  
- [ ] Add keys to Render environment variables
- [ ] Redeploy service
- [ ] Test endpoints
