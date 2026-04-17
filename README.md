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
- [Documentation](#documentation)

---

## 🎯 Overview

QuantFlow Agent is an intelligent stock market analysis system that combines:

- **Real-time market data** from Yahoo Finance
- **Technical analysis** using Alpha Vantage
- **News aggregation** from EventRegistry
- **SEC filings analysis** using RAG (Retrieval Augmented Generation)
- **LangGraph orchestration** for complex multi-step analysis

Built with LangChain, LangGraph, and GPT-4, QuantFlow provides professional-grade market intelligence through an intuitive conversational interface.

---

## ✨ Features

- 🔴 **Real-time stock prices** and market data
- 📊 **Financial statements** (Income, Balance Sheet, Cash Flow)
- 📈 **Technical indicators** (RSI with buy/sell signals)
- 📰 **Latest news** aggregation and sentiment
- 🔍 **SEC filings search** (10-K, 10-Q deep analysis)
- 🤖 **AI-powered insights** using GPT-4
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

# Set up environment variables (see API Keys section)
cp .env.example .env
# Edit .env with your API keys

# Ingest SEC filings (one-time setup)
python scripts/ingest.py

# Run the agent
python main.py
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User Interface                         │
│              (Natural Language Queries)                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              LangGraph Agent (GPT-4o)                   │
│  • Understands user questions                           │
│  • Routes to appropriate tools                          │
│  • Synthesizes multi-source data                        │
│  • Generates comprehensive insights                     │
└─────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                  ↓                   ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ Market Tools │  │ Company Tools│  │   RAG Tools      │
│              │  │              │  │                  │
│ • Price      │  │ • Info       │  │ • SEC Filings    │
│ • Metrics    │  │ • Financials │  │ • Vector Search  │
│ • Technical  │  │ • Earnings   │  │ • Semantic Q&A   │
│ • Compare    │  │ • Analysts   │  │ • Deep Research  │
└──────────────┘  └──────────────┘  └──────────────────┘
        ↓                  ↓                   ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ Yahoo Finance│  │ Yahoo Finance│  │ Pinecone Vector  │
│ (Real-time)  │  │ (Fundamentals│  │ Database         │
└──────────────┘  └──────────────┘  │ + OpenAI         │
                                     │ Embeddings       │
┌──────────────┐  ┌──────────────┐  └──────────────────┘
│ Alpha Vantage│  │ EventRegistry│
│ (Technical)  │  │ (News)       │
└──────────────┘  └──────────────┘
```

---

## 🛠️ Tools Overview

QuantFlow Agent provides **11 specialized tools** across 5 categories:

### Market Data Tools (4)

| Tool                      | Purpose                            | Data Source   |
| ------------------------- | ---------------------------------- | ------------- |
| `get_current_price_yahoo` | Real-time stock prices             | Yahoo Finance |
| `get_key_metrics`         | P/E, dividend, beta, 52-week range | Yahoo Finance |
| `technical_analysis`      | RSI with buy/sell signals          | Alpha Vantage |
| `compare_stocks`          | Side-by-side comparison (up to 5)  | Yahoo Finance |

### Company Analysis Tools (4)

| Tool                          | Purpose                          | Data Source   |
| ----------------------------- | -------------------------------- | ------------- |
| `get_company_info`            | Sector, industry, description    | Yahoo Finance |
| `get_financials`              | Income, Balance Sheet, Cash Flow | Yahoo Finance |
| `get_earnings_history`        | EPS beats/misses, next date      | Yahoo Finance |
| `get_analyst_recommendations` | Price targets, ratings           | Yahoo Finance |

### News & Sentiment (1)

| Tool                | Purpose                | Data Source   |
| ------------------- | ---------------------- | ------------- |
| `fetch_latest_news` | Breaking news articles | EventRegistry |

### RAG Tools (1)

| Tool                 | Purpose                      | Data Source       |
| -------------------- | ---------------------------- | ----------------- |
| `search_sec_filings` | AI-powered SEC filing search | Pinecone + OpenAI |

### Utility Tools (1)

| Tool         | Purpose              | Technology |
| ------------ | -------------------- | ---------- |
| `calculator` | Safe math evaluation | NumExpr    |

**📖 For detailed tool documentation, see [TOOLS.md](TOOLS.md)**

---

## 🔧 Installation

### Prerequisites

- Python 3.12+
- `uv` package manager

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

# Pinecone (required for RAG)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=finagent

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
python scripts/ingest.py
```

This will:

- Download 10-K and 10-Q filings for AAPL, TSLA, MSFT, AMZN
- Chunk documents into searchable segments
- Create embeddings using OpenAI
- Store in Pinecone vector database
- **Time:** ~10-15 minutes
- **Cost:** ~$0.50-1.00 in OpenAI embedding costs

---

## 📚 Usage

### Command Line

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the agent
python main.py
```

### Using Individual Tools

```python
from tools import (
    get_current_price_yahoo,
    get_key_metrics,
    search_sec_filings,
    compare_stocks,
)

# Get current price
price = get_current_price_yahoo("AAPL")
print(price)

# Get valuation metrics
metrics = get_key_metrics("MSFT")
print(metrics)

# Compare stocks
comparison = compare_stocks("AAPL,MSFT,GOOGL")
print(comparison)

# Search SEC filings
risks = search_sec_filings("What are the risk factors?", ticker="AAPL")
print(risks)
```

### Using the Agent (Coming Soon)

```python
from graph.builder import create_agent

agent = create_agent()

# Ask a complex question
response = agent.invoke({
    "messages": ["Compare Apple and Microsoft. Which is a better investment?"]
})

print(response["messages"][-1].content)
```

The agent will:

1. Call `get_key_metrics("AAPL")` and `get_key_metrics("MSFT")`
2. Call `get_analyst_recommendations()` for both
3. Call `search_sec_filings()` for strategic insights
4. Synthesize all data into a comprehensive recommendation

### Example Queries

**Simple queries:**

- "What's the current price of Apple?"
- "Show me Tesla's financial statements"
- "What's the latest news on Microsoft?"

**Complex queries:**

- "Compare AAPL, MSFT, and GOOGL. Which has the best value?"
- "What are Amazon's main business risks according to their 10-K?"
- "Is NVDA overbought based on technical analysis?"
- "Show me Apple's earnings history and analyst recommendations"

---

## 🔑 API Keys Required

| Service           | Purpose            | Cost                                | Sign Up                                            |
| ----------------- | ------------------ | ----------------------------------- | -------------------------------------------------- |
| **OpenAI**        | LLM + Embeddings   | Pay-per-use (~$0.01-0.03/1K tokens) | [platform.openai.com](https://platform.openai.com) |
| **Pinecone**      | Vector Database    | Free tier (1 index, 5M vectors)     | [pinecone.io](https://pinecone.io)                 |
| **Alpha Vantage** | Technical Analysis | Free (5 calls/min, 500/day)         | [alphavantage.co](https://www.alphavantage.co)     |
| **EventRegistry** | News Articles      | Free tier (1000 calls/day)          | [eventregistry.org](https://eventregistry.org)     |

**No API key needed:**

- Yahoo Finance (via `yfinance` library)

### Cost Estimate

**Initial setup:**

- SEC filings ingestion: ~$0.50-1.00 (one-time)

**Per query:**

- With RAG: ~$0.01-0.05 (OpenAI API + embeddings)
- Without RAG: ~$0.005-0.02 (OpenAI API only)

**Monthly (100 queries):**

- Estimated: $2-5

---

## 📖 Documentation

- **[TOOLS.md](TOOLS.md)** - Comprehensive tool reference with examples
- **[Architecture](#architecture)** - System design overview
- **[API Keys](#api-keys-required)** - Required services and costs

---

## 📊 Tool Summary

| Category             | Tools   | Free?                                     | Real-time?             |
| -------------------- | ------- | ----------------------------------------- | ---------------------- |
| **Market Data**      | 4 tools | ✅ Yes (except Alpha Vantage rate limits) | ✅ Yes                 |
| **Company Analysis** | 4 tools | ✅ Yes                                    | ✅ Yes                 |
| **News**             | 1 tool  | ⚠️ Free tier (1000/day)                   | ✅ Yes                 |
| **RAG**              | 1 tool  | ❌ Paid (OpenAI)                          | ❌ No (offline search) |
| **Utilities**        | 1 tool  | ✅ Yes                                    | ✅ Yes                 |

---

## 🚀 Roadmap

- [x] Real-time market data tools
- [x] SEC filings RAG search
- [x] Technical analysis (RSI)
- [x] News aggregation
- [ ] Complete LangGraph agent implementation
- [ ] Web UI (Streamlit/Gradio)
- [ ] More technical indicators (MACD, Bollinger Bands, Moving Averages)
- [ ] Portfolio tracking and management
- [ ] Backtesting capabilities
- [ ] Chart generation and visualization
- [ ] Options data and analysis
- [ ] Real-time alerts and notifications
- [ ] Expand SEC filing coverage to more tickers

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Author:** Akinbobola Faniyi  
**GitHub:** [@faniyi-akinbobola](https://github.com/faniyi-akinbobola)  
**Project:** [QuantFlow-Agent](https://github.com/faniyi-akinbobola/QuantFlow-Agent)

---

## ⭐ Acknowledgments

Built with:

- [LangChain](https://langchain.com) - LLM application framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent orchestration
- [OpenAI](https://openai.com) - GPT-4 and embeddings
- [Pinecone](https://pinecone.io) - Vector database
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance data
- [Alpha Vantage](https://www.alphavantage.co) - Technical indicators
- [EventRegistry](https://eventregistry.org) - News aggregation
- [edgartools](https://github.com/bellingcat/edgartools) - SEC filings

---

**Built with ❤️ for traders, investors, and financial analysts**
