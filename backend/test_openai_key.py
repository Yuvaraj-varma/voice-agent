"""
Test OpenAI API key and find best model for RAG
Run: python test_openai_key.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
print(f"Key found: {key[:20]}...")

try:
    from openai import OpenAI
except ImportError:
    print("\n❌ openai package not installed. Run: pip install openai")
    exit(1)

client = OpenAI(api_key=key)

# --------------------------------------------------
# Step 1: Check key is valid
# --------------------------------------------------
print("\n--- Step 1: Checking API key ---")
try:
    models = client.models.list()
    print("✅ API key is VALID")
except Exception as e:
    print(f"❌ API key INVALID: {e}")
    exit(1)

# --------------------------------------------------
# Step 2: Test RAG models
# --------------------------------------------------
RAG_MODELS = [
    ("gpt-4o-mini",        "⭐ Best for RAG — fast, cheap, smart"),
    ("gpt-4o",             "💪 Most powerful — higher cost"),
    ("gpt-3.5-turbo",      "💰 Cheapest — less accurate"),
]

print("\n--- Step 2: Testing RAG models ---")
print("Sending: 'What is an invoice?' to each model\n")

results = []
for model, label in RAG_MODELS:
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an invoice assistant. Answer briefly."},
                {"role": "user",   "content": "What is an invoice? Answer in one sentence."},
            ],
            max_tokens=60,
        )
        reply = res.choices[0].message.content.strip()
        print(f"✅ {model} ({label})")
        print(f"   Reply: {reply}\n")
        results.append((model, True))
    except Exception as e:
        print(f"❌ {model} — {e}\n")
        results.append((model, False))

# --------------------------------------------------
# Step 3: Test embedding model (needed for RAG)
# --------------------------------------------------
print("--- Step 3: Testing embedding model (for Pinecone) ---")
try:
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input="Invoice total amount due",
    )
    dim = len(emb.data[0].embedding)
    print(f"✅ text-embedding-3-small works — dimension: {dim}")
    print("   ⭐ Use this for RAG embeddings (1536 dim, cheap)")
except Exception as e:
    print(f"❌ Embedding failed: {e}")

# --------------------------------------------------
# Summary
# --------------------------------------------------
print("\n" + "=" * 50)
print("RECOMMENDATION FOR YOUR INVOICE RAG SYSTEM:")
print("=" * 50)
print("LLM Model  : gpt-4o-mini  (fast + accurate + cheap)")
print("Embeddings : text-embedding-3-small  (1536 dim)")
print("Pinecone   : set dimension=1536 for OpenAI embeddings")
