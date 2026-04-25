#!/usr/bin/env python3
"""Check what's in the Chroma vector database."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.chroma_vector_store import load_vectorstore
from rag.embeddings import get_embeddings
from collections import Counter

vs = load_vectorstore(get_embeddings())

# Get count
total_count = vs._collection.count()
print(f'Total documents: {total_count}')

# Sample metadata to check tickers
sample = vs._collection.get(limit=1000, include=['metadatas'])

tickers = {m.get('ticker') for m in sample['metadatas'] if m.get('ticker')}
print(f'Tickers found in sample: {sorted(tickers)}')

ticker_counts = Counter(m.get('ticker') for m in sample['metadatas'] if m.get('ticker'))
print('\nSample documents per ticker (first 1000 docs):')
for ticker, count in sorted(ticker_counts.items()):
    print(f'  {ticker}: {count}')
