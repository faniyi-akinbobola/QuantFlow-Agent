import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pinecone import Pinecone
from utils.loader import load_env_var

api_key = load_env_var("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

print("Current Pinecone Indexes:")
print("-" * 60)

indexes = pc.list_indexes()

if not indexes:
    print("✅ No indexes found - deletion successful!")
else:
    for idx in indexes:
        print(f"📊 Index: {idx.name}")
        print(f"   Dimension: {idx.dimension}")
        print(f"   Metric: {idx.metric}")
        print(f"   Status: {idx.status}")
        print()

print("-" * 60)