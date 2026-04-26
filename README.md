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

---

## 🎯 Overview

QuantFlow Agent is an intelligent stock market analysis system that combines:

- **Real-time market data** from Yahoo Finance
- **Technical analysis** using Alpha Vantage
- **News aggregation** from EventRegistry
- **SEC filings analysis** using RAG (Retrieval Augmented Generation) with ChromaDB
- **LangGraph orchestration** for complex multi-step analysis
- **Chainlit UI** for a conversational chat interface

Built with LangChain, LangGraph, and GPT-4o-mini, QuantFlow provides professional-grade market intelligence through an intuitive conversational interface.

---

## ✨ Features

- 🔴 **Real-time stock prices** and market data
- 📊 **Key financial metrics** (P/E, EPS, dividend yield, beta, 52-week range)
- 📈 **Technical indicators** (RSI with buy/sell signals)
- 📰 **Latest news** aggregation
- 🔍 **SEC filings search** (10-K, 10-Q deep analysis via RAG)
- 🤖 **AI-powered insights** using GPT-4o-mini
- 🧮 **Financial calculations** and comparisons
- 📉 **Multi-stock comparison** (up to 5 stocks)
- 💡 **Analyst recommendations** and price targets
- 🎯 **Earnings tracking** with beat/miss analysis

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

# Or run CLI mode
uv run python main.py
```

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
│              │  │              │  │                  │
│ • Price      │  │ • Info       │  │ • SEC Filings    │
│ • Metrics    │  │ • Financials │  │ • ChromaDB       │
│ • Technical  │  │ • Earnings   │  │ • Semantic Q&A   │
│ • Compare    │  │ • Analysts   │  │ • 19 Tickers     │
└──────────────┘  └──────────────┘  └──────────────────┘
        ↓                  ↓                   ↓
   Yahoo Finance      Yahoo Finance       ChromaDB (local)
   Alpha Vantage      EventRegistry       + OpenAI Embeddings
```

---

## 🛠️ Tools Overview

QuantFlow Agent provides **11 specialized tools** across 5 categories:

### Market Data Tools (4)

| Tool | Purpose | Data Source |
|------|---------|-------------|
| `get_current_price_yahoo` | Real-time stock prices | Yahoo Finance |
| `get_key_metrics` | P/E, dividend, beta, 52-week range | Yahoo Finance |
| `technical_analysis` | RSI with buy/sell signals | Alpha Vantage |
| `compare_stocks` | Side-by-side comparison (up to 5) | Yahoo Finance |

### Company Analysis Tools (4)

| Tool | Purpose | Data Source |
|------|---------|-------------|
| `get_company_info` | Sector, industry, description | Yahoo Finance |
| `get_financials` | Income, Balance Sheet, Cash Flow | Yahoo Finance |
| `get_earnings_history` | EPS beats/misses, next date | Yahoo Finance |
| `get_analyst_recommendations` | Price targets, ratings | Yahoo Finance |

### News & Sentiment (1)

| Tool | Purpose | Data Source |
|------|---------|-------------|
| `fetch_latest_news` | Breaking news articles | EventRegistry |

### RAG Tools (1)

| Tool | Purpose | Data Source |
|------|---------|-------------|
| `search_sec_filings` | AI-powered SEC filing search | ChromaDB + OpenAI |

### Utility Tools (1)

| Tool | Purpose | Technology |
|------|---------|------------|
| `calculator` | Safe math evaluation | NumExpr |

**📖 For detailed tool documentation, see [TOOLS.md](TOOLS.md)**

---

## 🔧 Installation

### Prerequisites

- Python 3.11+
- `uv` package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

### Setup Steps

1. **Clone the repository:**

```bash
git clone https://github.com/faniyi-akinbobola/QuantFlow-Agent.git
cd QuantFlow-Agent
```

2. **Install dependencies:**

```bash
uv sync
```

3. **Set up environment variables:**

Create a `.env` file in the project root:

```env
# OpenAI (required)
OPENAI_API_KEY=your_openai_api_key

# Alpha Vantage (required for technical analysis)
ALPHAVANTAGE_KEY=your_alphavantage_key

# EventRegistry (required for news)
NEWSAPI_KEY=your_eventregistry_key

# SEC EDGAR identity (required by SEC)
NAME=Your Name or Company
EMAIL=your.email@example.com
```

4. **Ingest SEC filings** (one-time setup):

```bash
uv run python scripts/ingest.py
```

This downloads and ingests 10-K and 10-Q filings for **19 tickers** into a local ChromaDB vector store:

> AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, NFLX, JPM, V, MA, BAC, JNJ, UNH, LLY, WMT, PG, KO, PEP

- **~30,000 document chunks** stored locally
- **Time:** ~20-30 minutes
- **Cost:** ~$0.00 (uses local ChromaDB, no Pinecone needed)

---

## �� Usage

### Chat UI (Chainlit)

```bash
uv run chainlit run ui/ui.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### CLI Mode

```bash
uv run python main.py
```

### Example Queries

**Simple queries:**
- "What's the current price of Apple?"
- "Show me Tesla's financial statements"
- "What's the latest news on Microsoft?"

**Complex investment queries:**
- "Should I invest in AAPL right now? Give me a full analysis."
- "Compare AAPL, MSFT, and GOOGL. Which has the best value?"
- "What are Amazon's main business risks according to their 10-K?"
- "Is NVDA overbought based on technical analysis?"

---

## 🔑 API Keys Required

| Service | Purpose | Cost | Sign Up |
|---------|---------|------|---------|
| **OpenAI** | LLM + Embeddings | Pay-per-use | [platform.openai.com](https://platform.openai.com) |
| **Alpha Vantage** | Technical Analysis | Free (5 calls/min) | [alphavantage.co](https://www.alphavantage.co) |
| **EventRegistry** | News Articles | Free tier (1000/day) | [eventregistry.org](https://eventregistry.org) |

**No API key needed:**
- Yahoo Finance (via `yfinance`)
- ChromaDB (local, no cloud account required)

---

## 📊 Evaluation

The project includes a comprehensive evaluation framework in `evals/`.

```bash
uv run python evals/runners/run_local.py
```

**Latest results (95 test cases across 6 datasets):**

| Metric | Score |
|--------|-------|
| Tool Usage | 93.33% |
| Correctness | 93.33% |
| Reasoning Quality | 86.67% |
| Overall Pass Rate | ~99% |

See `evals/README.md` for full documentation.

---

## 🚀 Roadmap

- [x] Real-time market data tools
- [x] SEC filings RAG search (ChromaDB, 19 tickers, ~30K chunks)
- [x] Technical analysis (RSI)
- [x] News aggregation
- [x] LangGraph agent with multi-tool orchestration
- [x] Chainlit chat UI
- [x] Comprehensive evaluation framework
- [ ] More technical indicators (MACD, Bollinger Bands)
- [ ] Portfolio tracking and management
- [ ] Chart generation and visualization
- [ ] Expand SEC filing coverage to more tickers

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Built With

- [LangChain](https://langchain.com) — LLM application framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Agent orchestration
- [Chainlit](https://chainlit.io) — Chat UI
- [OpenAI](https://openai.com) — GPT-4o-mini and embeddings
- [ChromaDB](https://www.trychroma.com) — Local vector database
- [yfinance](https://github.com/ranaroussi/yfinance) — Yahoo Finance data
- [Alpha Vantage](https://www.alphavantage.co) — Technical indicators
- [EventRegistry](https://eventregistry.org) — News aggregation
- [edgartools](https://github.com/bellingcat/edgartools) — SEC filings

---

**Built with ❤️ for traders, investors, and financial analysts**
