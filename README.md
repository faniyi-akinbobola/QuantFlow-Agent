# QuantFlow Agent 🚀

AI-powered stock market analysis agent with real-time data, SEC filings analysis, and comprehensive financial tools.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Tools Overview](#tools-overview)
- [Installation](#installation)
- [Usage](#usage)
- [API Keys Required](#api-keys-required)
- [Evaluation](#evaluation)
- [Deployment](#deployment)

---

## 🎯 Overview

QuantFlow Agent is an intelligent stock market analysis system that combines:

- **Real-time market data** from Yahoo Finance
- **Technical analysis** using Alpha Vantage
- **News aggregation** from EventRegistry
- **SEC filings analysis** via RAG (ChromaDB, 19 tickers, ~30K chunks)
- **LangGraph orchestration** for complex multi-step reasoning
- **Chainlit UI** for a conversational chat interface
- **LangSmith tracing** for observability

Built with LangChain, LangGraph, and GPT-4o-mini.

---

## ✨ Features

- 🔴 **Real-time stock prices** and market data
- 📊 **Key financial metrics** — P/E, EPS, dividend yield, beta, 52-week range
- 📈 **Technical indicators** — RSI with buy/sell signals
- 📰 **Latest news** aggregation
- 🔍 **SEC filings search** — 10-K and 10-Q deep analysis via RAG
- 🤖 **AI-powered insights** using GPT-4o-mini
- 🧮 **Financial calculations** and multi-stock comparisons
- 💡 **Analyst recommendations** and price targets
- 🎯 **Earnings tracking** with beat/miss history

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/faniyi-akinbobola/QuantFlow-Agent.git
cd QuantFlow-Agent

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Ingest SEC filings into ChromaDB (one-time setup, ~20-30 min)
uv run python scripts/ingest.py

# Run the chat UI
uv run chainlit run ui/ui.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Chainlit Chat UI                       │
│              (Natural Language Queries)                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│         LangGraph Agent (GPT-4o-mini)                   │
│  • Routes to appropriate tools                          │
│  • Synthesizes multi-source data                        │
│  • Generates comprehensive insights                     │
│  • Recursion-protected (limit: 25 steps)                │
└─────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                  ↓                   ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ Market Tools │  │ Company Tools│  │   RAG Tools      │
│ • Price      │  │ • Info       │  │ • SEC Filings    │
│ • Metrics    │  │ • Financials │  │ • ChromaDB local │
│ • Technical  │  │ • Earnings   │  │ • 19 Tickers     │
│ • Compare    │  │ • Analysts   │  │ • ~30K chunks    │
└──────────────┘  └──────────────┘  └──────────────────┘
        ↓                  ↓                   ↓
   Yahoo Finance      Yahoo Finance       ChromaDB (local)
   Alpha Vantage      EventRegistry       + OpenAI Embeddings
```

---

## 🛠️ Tools Overview

QuantFlow Agent provides **11 specialized tools** across 5 categories:

### Market Data (4)

| Tool | Purpose | Source |
|------|---------|--------|
| `get_current_price_yahoo` | Real-time stock prices | Yahoo Finance |
| `get_key_metrics` | P/E, dividend, beta, 52-week range | Yahoo Finance |
| `technical_analysis` | RSI with buy/sell signals | Alpha Vantage |
| `compare_stocks` | Side-by-side comparison (up to 5) | Yahoo Finance |

### Company Analysis (4)

| Tool | Purpose | Source |
|------|---------|--------|
| `get_company_info` | Sector, industry, description | Yahoo Finance |
| `get_financials` | Income, Balance Sheet, Cash Flow | Yahoo Finance |
| `get_earnings_history` | EPS beats/misses, next date | Yahoo Finance |
| `get_analyst_recommendations` | Price targets, ratings | Yahoo Finance |

### News (1)

| Tool | Purpose | Source |
|------|---------|--------|
| `fetch_latest_news` | Breaking news articles | EventRegistry |

### RAG (1)

| Tool | Purpose | Source |
|------|---------|--------|
| `search_sec_filings` | AI-powered SEC filing search | ChromaDB + OpenAI |

### Utilities (1)

| Tool | Purpose | Technology |
|------|---------|------------|
| `calculator` | Safe math evaluation | NumExpr |

**📖 See [TOOLS.md](TOOLS.md) for full documentation.**

---

## 🔧 Installation

### Prerequisites

- Python **3.11+**
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Steps

```bash
# 1. Clone
git clone https://github.com/faniyi-akinbobola/QuantFlow-Agent.git
cd QuantFlow-Agent

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Fill in your API keys

# 4. Ingest SEC filings (one-time, ~20-30 min)
uv run python scripts/ingest.py
```

The ingest script downloads 10-K and 10-Q filings for these 19 tickers and stores them in a local ChromaDB vector database:

> AAPL · MSFT · GOOGL · AMZN · META · NVDA · TSLA · NFLX · JPM · V · MA · BAC · JNJ · UNH · LLY · WMT · PG · KO · PEP

---

## 📚 Usage

### Chat UI

```bash
uv run chainlit run ui/ui.py
```

### CLI Mode

```bash
uv run python main.py
```

### Example Queries

```
"What's the current price of Apple?"
"Show me Tesla's financial statements"
"Should I invest in AAPL right now? Give me a full analysis."
"Compare AAPL, MSFT, and GOOGL — which has the best value?"
"What are Amazon's main business risks from their latest 10-K?"
"Is NVDA overbought based on technical analysis?"
```

---

## 🔑 API Keys Required

| Service | Purpose | Cost |
|---------|---------|------|
| **OpenAI** | LLM (GPT-4o-mini) + embeddings | Pay-per-use |
| **Alpha Vantage** | RSI / technical analysis | Free (5 req/min) |
| **EventRegistry** | News articles | Free tier (1000/day) |

**No key needed:** Yahoo Finance (`yfinance`) · ChromaDB (runs fully local)

Create a `.env` from the provided template:

```bash
cp .env.example .env
```

---

## 📊 Evaluation

A comprehensive evaluation framework lives in `evals/` — 6 datasets, 95 test cases.

```bash
uv run python evals/runners/run_local.py
```

**Latest results:**

| Metric | Score |
|--------|-------|
| Tool Usage | 93.33% |
| Correctness | 93.33% |
| Reasoning Quality | 86.67% |
| Overall Pass Rate | ~99% |

See [`evals/README.md`](evals/README.md) for details.

---

## 🚢 Deployment

See the [Docker section](#docker) below for bundled deployment, or use Render / Railway.

### Docker

```bash
# Build image (ChromaDB is bundled inside)
docker build -t quantflow-agent .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=... \
  -e ALPHAVANTAGE_KEY=... \
  -e NEWSAPI_KEY=... \
  -e NAME="Your Name" \
  -e EMAIL=your@email.com \
  -e LANGCHAIN_API_KEY=... \
  quantflow-agent
```

Open [http://localhost:8000](http://localhost:8000).

### Render / Railway

1. Push your code (including the built `data/chroma_db/`) to GitHub
2. Create a **Web Service** pointing to your repo
3. Set **Start Command:** `chainlit run ui/ui.py --host 0.0.0.0 --port 8000`
4. Add all environment variables from `.env.example`
5. Deploy

> **Note:** `data/chroma_db/` is gitignored by default. For deployment you either build a Docker image (recommended) or temporarily allow the `data/` directory in `.gitignore` when pushing to your deployment branch.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

MIT License

---

## ⭐ Built With

[LangChain](https://langchain.com) · [LangGraph](https://langchain-ai.github.io/langgraph/) · [Chainlit](https://chainlit.io) · [OpenAI](https://openai.com) · [ChromaDB](https://www.trychroma.com) · [yfinance](https://github.com/ranaroussi/yfinance) · [Alpha Vantage](https://www.alphavantage.co) · [EventRegistry](https://eventregistry.org) · [edgartools](https://github.com/bellingcat/edgartools)

---

**Built with ❤️ for traders, investors, and financial analysts**
