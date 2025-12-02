"""
Setup script for Pinecone Vector Database
Indexes vehicle knowledge base using local embeddings (Sentence Transformers)
"""
import os
import json
import time
from typing import List, Dict
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "autoxloo-vehicles")

if not PINECONE_API_KEY:
    print("❌ Error: PINECONE_API_KEY not found in .env file")
    print("Please get a free key from https://pinecone.io and add it to .env")
    exit(1)

def load_knowledge_base() -> List[Dict]:
    """Load vehicle knowledge base"""
    try:
        with open('../data/vehicle_knowledge_base.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: Knowledge base not found. Run build_knowledge_base.py first.")
        exit(1)

def create_embeddings(kb: List[Dict]):
    """Generate embeddings for knowledge base entries"""
    print("\nLoading embedding model (all-MiniLM-L6-v2)...")
    # Use a small, fast, high-quality model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Generating embeddings for {len(kb)} vehicles...")
    
    vectors = []
    for i, entry in enumerate(kb):
        # Create rich text representation for embedding
        text = f"{entry['year']} {entry['make']} {entry['model']}. "
        text += f"{entry['overview']} "
        
        # Add key specs
        if 'powertrain' in entry:
            pt = entry['powertrain']
            text += f"Engine: {pt.get('engine', '')}. "
            text += f"HP: {pt.get('horsepower', '')}. "
        
        # Add features
        if 'features' in entry:
            feats = entry['features']
            text += f"Safety: {', '.join(feats.get('safety', []))}. "
            text += f"Tech: {', '.join(feats.get('technology', []))}. "
        
        # Generate embedding
        embedding = model.encode(text).tolist()
        
        # Create vector record
        vector = {
            "id": f"{entry['make']}_{entry['model']}_{entry['year']}".replace(" ", "_").lower(),
            "values": embedding,
            "metadata": {
                "make": entry['make'],
                "model": entry['model'],
                "year": entry['year'],
                "text": text[:1000]  # Store text for context (limit size)
            }
        }
        vectors.append(vector)
        
        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(kb)}")
            
    return vectors

def setup_pinecone(vectors: List[Dict]):
    """Setup Pinecone index and upload vectors"""
    print(f"\nConnecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists
    existing_indexes = [i.name for i in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,  # Dimension for all-MiniLM-L6-v2
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(1)
    else:
        print(f"Index '{INDEX_NAME}' already exists.")
    
    # Get index
    index = pc.Index(INDEX_NAME)
    
    # Upsert vectors in batches
    print(f"Upserting {len(vectors)} vectors...")
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"  Uploaded batch {i//batch_size + 1}")
        
    print("\n✅ Pinecone setup complete!")
    print(f"Index: {INDEX_NAME}")
    print(f"Vectors: {len(vectors)}")

if __name__ == "__main__":
    print("=" * 60)
    print("AutoXloo AI - Pinecone Setup")
    print("=" * 60)
    
    kb = load_knowledge_base()
    vectors = create_embeddings(kb)
    setup_pinecone(vectors)
