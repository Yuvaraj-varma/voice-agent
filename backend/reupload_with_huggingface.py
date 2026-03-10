"""
Re-upload PDFs to Pinecone with HuggingFace embeddings (384 dimensions)
Run this ONCE to fix the dimension mismatch
"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time

load_dotenv()

# Initialize HuggingFace embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "ds-tutor"

# Delete old index
if index_name in pc.list_indexes().names():
    print(f"Deleting old index: {index_name}")
    pc.delete_index(index_name)
    time.sleep(5)

# Create new index with 384 dimensions (HuggingFace)
pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
)
print(f"Created index: {index_name}")

index = pc.Index(index_name)
time.sleep(5)

# Load PDFs
loader = PyPDFDirectoryLoader("data/ds_notes")
documents = loader.load()
print(f"Loaded {len(documents)} pages")

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")

# Upload to Pinecone with HuggingFace embeddings
for i, doc in enumerate(chunks):
    embedding = model.encode(doc.page_content).tolist()
    
    index.upsert(vectors=[{
        "id": f"chunk_{i}",
        "values": embedding,
        "metadata": {
            "text": doc.page_content,
            "page": doc.metadata.get("page", 0)
        }
    }])
    
    if (i + 1) % 10 == 0:
        print(f"Uploaded {i + 1}/{len(chunks)} chunks")

print(f"✅ Done! Uploaded {len(chunks)} chunks to Pinecone")
print(f"Index stats: {index.describe_index_stats()}")
