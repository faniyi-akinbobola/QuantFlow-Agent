#!/usr/bin/env python3
"""Quick check of all tickers in database."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.chroma_vector_store import load_vectorstore
from rag.embeddings import get_embeddings

vs = load_vectorstore(get_embeddings())
total = vs._collection.count()

print(f"Total documents: {total:,}\n")

# Check each expected ticker
expected_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX",
    "JPM", "V", "MA", "BAC",
    "JNJ", "UNH", "LLY",
    "WMT", "PG", "KO", "PEP"
]

print("Checking tickers:")
found_tickers = []
for ticker in expected_tickers:
    results = vs._collection.get(
        where={"ticker": ticker},
        limit=1,
        include=['metadatas']
    )
    count = len(results['ids'])
    if count > 0:
        found_tickers.append(ticker)
        print(f"  ✅ {ticker}: Present")
    else:
        print(f"  ❌ {ticker}: Missing")

print(f"\n✅ Found {len(found_tickers)}/{len(expected_tickers)} tickers")
print(f"Tickers: {', '.join(sorted(found_tickers))}")
