# 🛠️ Tools Reference Guide

Complete documentation for all QuantFlow Agent tools.

## 📋 Table of Contents

- [Overview](#overview)
- [Market Data Tools](#market-data-tools)
- [Company Analysis Tools](#company-analysis-tools)
- [News & Sentiment](#news--sentiment)
- [RAG Tools (SEC Filings)](#rag-tools-sec-filings)
- [Utility Tools](#utility-tools)
- [Tool Summary Table](#tool-summary-table)

---

## 🎯 Overview

QuantFlow Agent provides 11 specialized tools across 5 categories:

| Category              | Tools   | Data Sources                 |
| --------------------- | ------- | ---------------------------- |
| **Market Data**       | 4 tools | Yahoo Finance, Alpha Vantage |
| **Company Analysis**  | 4 tools | Yahoo Finance                |
| **News & Sentiment**  | 1 tool  | EventRegistry                |
| **RAG (SEC Filings)** | 1 tool  | Pinecone + OpenAI            |
| **Utilities**         | 1 tool  | NumExpr                      |

---

## 📊 Market Data Tools

### 1. `get_current_price_yahoo(ticker: str)`

**Purpose:** Get real-time stock price and daily statistics

**Data Source:** Yahoo Finance (free, near real-time)

**Parameters:**

- `ticker` (str): Stock ticker symbol (e.g., "AAPL", "TSLA")

**Returns:**

- Current price
- Open, High, Low prices
- Daily change ($ and %)
- Previous close

**Example Usage:**

```python
from tools import get_current_price_yahoo

result = get_current_price_yahoo("AAPL")
print(result)
```

**Example Output:**

```
AAPL Current Price: $175.23
Change: $4.23 (+2.47%)
Previous Close: $170.00
```

**Use Cases:**

- Quick price checks
- Daily performance monitoring
- Portfolio valuation
- Entry/exit timing

**Limitations:**

- No intraday historical data
- Limited to major exchanges

---

### 2. `get_key_metrics(ticker: str)`

**Purpose:** Get real-time valuation and financial metrics

**Data Source:** Yahoo Finance

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- Current Price
- Market Cap
- P/E Ratio (TTM & Forward)
- EPS (Trailing 12 months)
- Dividend Yield
- Beta (volatility)
- 52-Week High/Low
- Distance from 52-week range (%)

**Example Usage:**

```python
from tools import get_key_metrics

result = get_key_metrics("MSFT")
print(result)
```

**Example Output:**

```
Key Metrics for MSFT:

Current Price: $420.55
Market Cap: $3,125,234,500,000

Valuation Metrics:
  P/E Ratio (TTM): 35.20
  Forward P/E: 32.10
  EPS (TTM): $11.95

Dividend & Risk:
  Dividend Yield: 0.75%
  Beta: 0.89

52-Week Range:
  High: $450.00
  Low: $320.00
  Current vs High: -6.54%
  Current vs Low: +31.42%
```

**Metrics Explained:**

- **P/E Ratio:** Price-to-Earnings ratio (lower = cheaper relative to earnings)
- **Forward P/E:** Expected P/E based on analyst estimates
- **Beta:** Volatility vs market (1.0 = market average, >1 = more volatile)
- **Dividend Yield:** Annual dividend as % of stock price

**Use Cases:**

- Stock valuation analysis
- Comparing valuations across stocks
- Risk assessment (beta)
- Income investing (dividend yield)

---

### 3. `technical_analysis(ticker: str)`

**Purpose:** Get RSI (Relative Strength Index) with buy/sell signals

**Data Source:** Alpha Vantage

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- Current RSI value (14-day)
- Signal interpretation (Overbought/Oversold/Neutral)
- Recent trend (last 3 days)
- Date of calculation

**Example Usage:**

```python
from tools import technical_analysis

result = technical_analysis("TSLA")
print(result)
```

**Example Output:**

```
Technical Analysis for TSLA:

RSI (14-day): 72.34
Signal: 📈 OVERBOUGHT - Potential sell signal
Date: 2024-04-17

Recent Trend:
  2024-04-17: 72.34
  2024-04-16: 68.21
  2024-04-15: 65.89
```

**Signal Interpretation:**

- **RSI > 70:** Overbought (potential sell signal)
- **RSI < 30:** Oversold (potential buy signal)
- **RSI 30-70:** Neutral (no strong signal)

**Use Cases:**

- Momentum trading
- Entry/exit timing
- Identifying overbought/oversold conditions
- Trend confirmation

**Limitations:**

- Free tier: 5 calls/minute limit
- 15-minute data delay on free tier
- RSI is a lagging indicator

---

### 4. `compare_stocks(tickers: str)`

**Purpose:** Side-by-side comparison of multiple stocks

**Data Source:** Yahoo Finance

**Parameters:**

- `tickers` (str): Comma-separated ticker symbols (e.g., "AAPL,MSFT,GOOGL")
- Maximum: 5 stocks
- Minimum: 2 stocks

**Returns:**

- Price comparison
- P/E Ratio comparison
- Forward P/E comparison
- EPS comparison
- Market Cap comparison
- Dividend Yield comparison
- Beta comparison
- Key insights (lowest P/E, highest dividend, largest company)

**Example Usage:**

```python
from tools import compare_stocks

result = compare_stocks("AAPL,MSFT,GOOGL")
print(result)
```

**Example Output:**

```
Stock Comparison: AAPL, MSFT, GOOGL

Metric                        AAPL          MSFT         GOOGL
================================================================
Price                      $175.23       $420.55       $140.25
P/E Ratio (TTM)              28.45         35.20         25.30
Forward P/E                  26.80         32.10         23.50
EPS (TTM)                    $6.16         $11.95        $5.54
Market Cap               $2,750.5B     $3,125.2B     $1,780.8B
Dividend Yield               0.52%         0.75%         0.00%
Beta                          1.29          0.89          1.05

================================================================

Key Insights:
• Lowest P/E: GOOGL (25.30) - Potentially undervalued
• Highest Dividend: MSFT (0.75%) - Best for income
• Largest Company: MSFT ($3,125.2B market cap)
```

**Use Cases:**

- Sector comparison
- Portfolio diversification analysis
- Finding best value stocks
- Income investing comparison

**Tips:**

- Compare stocks in same sector for best insights
- Lower P/E doesn't always mean better value
- Consider growth vs value investing style

---

## 🏢 Company Analysis Tools

### 5. `get_company_info(ticker: str)`

**Purpose:** Get company overview and profile

**Data Source:** Yahoo Finance

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- Company name
- Sector
- Industry
- Number of employees
- Headquarters location
- Website
- Business description (500 chars summary)

**Example Usage:**

```python
from tools import get_company_info

result = get_company_info("AAPL")
print(result)
```

**Example Output:**

```
Company Information for AAPL:

Name: Apple Inc.
Sector: Technology
Industry: Consumer Electronics
Employees: 161,000
Headquarters: Cupertino, CA USA
Website: https://www.apple.com

Business Description:
Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, Mac, iPad, and wearables, home, and accessories. Apple also sells various related services. The company serves consumers, small and mid-sized businesses, education, enterprise, and government customers...
```

**Use Cases:**

- Quick company overview
- Sector/industry identification
- Company size assessment
- Research starting point

**Note:**

- Faster than RAG search for basic info
- Use `search_sec_filings()` for detailed business strategy

---

### 6. `get_financials(ticker: str)`

**Purpose:** Get financial statements (Income, Balance Sheet, Cash Flow)

**Data Source:** Yahoo Finance

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- **Income Statement:** Revenue, Gross Profit, Operating Income, Net Income
- **Balance Sheet:** Total Assets, Liabilities, Equity, Cash
- **Cash Flow:** Operating, Investing, Financing, Free Cash Flow

**Example Usage:**

```python
from tools import get_financials

result = get_financials("AMZN")
print(result)
```

**Example Output:**

```
Financial Statements for AMZN:

=== Income Statement (Most Recent Year) ===
Total Revenue: $574,785,000,000
Gross Profit: $270,456,000,000
Operating Income: $36,852,000,000
Net Income: $30,425,000,000

=== Balance Sheet (Most Recent) ===
Total Assets: $527,854,000,000
Total Liabilities: $358,744,000,000
Stockholder Equity: $169,110,000,000
Cash: $73,387,000,000

=== Cash Flow (Most Recent) ===
Operating Cash Flow: $84,946,000,000
Investing Cash Flow: -$47,679,000,000
Financing Cash Flow: -$25,651,000,000
Free Cash Flow: $37,267,000,000
```

**Key Metrics Explained:**

- **Free Cash Flow:** Operating Cash Flow - Capital Expenditures (cash available for growth/dividends)
- **Gross Profit:** Revenue - Cost of Goods Sold
- **Operating Income:** Profit from core business operations
- **Net Income:** Bottom-line profit after all expenses

**Use Cases:**

- Financial health assessment
- Profitability analysis
- Cash generation analysis
- Debt load evaluation

**Limitations:**

- Quarterly/annual data (not real-time)
- Most recent filing only
- For historical trends, use `search_sec_filings()`

---

### 7. `get_earnings_history(ticker: str)`

**Purpose:** Get earnings history with beat/miss analysis

**Data Source:** Yahoo Finance

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- Last 4 quarters of earnings
- EPS Estimate vs Actual
- Earnings surprises ($ and %)
- Beat/Miss/Met indicators
- Next earnings date
- Expected EPS

**Example Usage:**

```python
from tools import get_earnings_history

result = get_earnings_history("NVDA")
print(result)
```

**Example Output:**

```
Earnings History for NVDA:

Recent Earnings (Last 4 Quarters):
------------------------------------------------------------

Date: 2024-02-01
  EPS Estimate: $2.10
  EPS Actual:   $2.18
  Surprise:     +$0.08 (+3.8%) ✅ BEAT

Date: 2023-11-02
  EPS Estimate: $1.39
  EPS Actual:   $1.46
  Surprise:     +$0.07 (+5.0%) ✅ BEAT

Date: 2023-08-03
  EPS Estimate: $1.19
  EPS Actual:   $1.26
  Surprise:     +$0.07 (+5.9%) ✅ BEAT

Date: 2023-05-04
  EPS Estimate: $1.43
  EPS Actual:   $1.52
  Surprise:     +$0.09 (+6.3%) ✅ BEAT

============================================================

📅 Next Earnings Date: 2024-05-02
   Expected EPS: $1.50
```

**Understanding Earnings:**

- **Beat:** Company exceeded analyst expectations (usually bullish)
- **Miss:** Company fell short of expectations (usually bearish)
- **Met:** Company matched expectations exactly

**Use Cases:**

- Track earnings consistency
- Identify earnings surprises
- Plan for earnings volatility
- Assess company guidance accuracy

**Trading Implications:**

- Stock often moves 5-15% on earnings day
- Consistent beats may indicate strong management
- Consistent misses may indicate guidance issues

---

### 8. `get_analyst_recommendations(ticker: str)`

**Purpose:** Get analyst ratings and price targets

**Data Source:** Yahoo Finance

**Parameters:**

- `ticker` (str): Stock ticker symbol

**Returns:**

- Price targets (High, Mean, Low)
- Current price
- Potential upside/downside (%)
- Consensus recommendation (Strong Buy/Buy/Hold/Sell/Strong Sell)
- Number of analysts covering the stock
- Recent upgrades/downgrades (last 5 changes)
- Firm names and rating changes

**Example Usage:**

```python
from tools import get_analyst_recommendations

result = get_analyst_recommendations("TSLA")
print(result)
```

**Example Output:**

```
Analyst Recommendations for TSLA:

Price Targets:
  High:    $350.00
  Mean:    $245.50
  Low:     $180.00
  Current: $220.23

📈 Upside: 11.5%

Consensus Recommendation: BUY
Number of Analysts: 52

Recent Rating Changes (Last 5):
------------------------------------------------------------

2024-04-15 | Morgan Stanley
  Hold → Buy (upgrade)

2024-04-10 | Goldman Sachs
  Rating: Buy (main)

2024-04-05 | JP Morgan
  Buy → Strong Buy (upgrade)

2024-03-28 | Barclays
  Rating: Overweight (main)

2024-03-20 | Wedbush
  Hold → Buy (upgrade)
```

**Rating Definitions:**

- **Strong Buy:** Analysts very bullish, expect significant upside
- **Buy:** Analysts bullish, expect moderate upside
- **Hold:** Neutral, own if you have it, but don't rush to buy
- **Sell:** Analysts bearish, expect downside
- **Strong Sell:** Analysts very bearish, expect significant downside

**Use Cases:**

- Gauge Wall Street sentiment
- Identify potential upside/downside
- Track analyst sentiment changes
- Contrarian investing (fade the consensus)

**Important Notes:**

- Analyst targets are often wrong
- Use as one data point among many
- Upgrades/downgrades can move stock prices short-term
- More analysts = more institutional interest

---

## 📰 News & Sentiment

### 9. `fetch_latest_news(ticker: str, max_items: int = 5)`

**Purpose:** Get latest news articles for a stock

**Data Source:** EventRegistry

**Parameters:**

- `ticker` (str): Stock ticker symbol or company name
- `max_items` (int, optional): Number of articles (default: 5, max: 100)

**Returns:**

- Article title
- Source (publication)
- Publication date
- Summary (300 chars)
- Article URL

**Example Usage:**

```python
from tools import fetch_latest_news

result = fetch_latest_news("AAPL", max_items=3)
print(result)
```

**Example Output:**

```
Latest News for AAPL:

1. Apple Announces New AI Features in iOS 18
   Source: TechCrunch | Date: 2024-04-17
   Apple unveiled major AI enhancements coming to iOS 18, including improved Siri capabilities and on-device machine learning features that prioritize user privacy while delivering powerful new functionality...
   URL: https://techcrunch.com/2024/04/17/apple-ai-ios18

2. Apple Stock Reaches All-Time High Amid Strong iPhone Sales
   Source: Bloomberg | Date: 2024-04-16
   Apple Inc. shares hit a new record as iPhone 15 sales exceeded analyst expectations in the March quarter, driven by strong demand in China and emerging markets where the company has been aggressively expanding...
   URL: https://bloomberg.com/2024/04/16/apple-stock-ath

3. Analysts Upgrade Apple on Services Revenue Growth
   Source: CNBC | Date: 2024-04-15
   Multiple Wall Street firms raised their price targets for Apple citing accelerating growth in the company's services segment, which now accounts for 25% of total revenue and maintains higher margins than hardware...
   URL: https://cnbc.com/2024/04/15/apple-services-upgrade
```

**Use Cases:**

- Track breaking news
- Monitor company announcements
- Sentiment analysis
- Event-driven trading
- Research catalysts

**Tips:**

- News can move stock prices instantly
- Cross-reference with price action
- Look for recurring themes
- Major news usually appears in multiple sources

**Limitations:**

- Free tier: 1000 API calls/day
- May miss very recent news (5-10 min delay)
- Quality varies by source

---

## 🔍 RAG Tools (SEC Filings)

### 10. `search_sec_filings(query: str, ticker: str = None)`

**Purpose:** Search SEC filings (10-K, 10-Q) using AI-powered semantic search

**Data Source:** Pinecone Vector Database with OpenAI Embeddings

**Technology Stack:**

- **Vector Database:** Pinecone
- **Embeddings:** OpenAI text-embedding-3-large (3072 dimensions)
- **Search Algorithm:** MMR (Maximal Marginal Relevance)
- **Chunking:** RecursiveCharacterTextSplitter (1000 chars, 200 overlap)

**Filings Stored:**

- 3 × 10-K filings (annual reports)
- 2 × 10-Q filings (quarterly reports)
- For tickers: **AAPL, TSLA, MSFT, AMZN**

**Parameters:**

- `query` (str): Question or topic to search for
- `ticker` (str, optional): Filter results by specific ticker

**Returns:**

- Top 5 relevant chunks from SEC filings
- For each result:
  - Ticker symbol
  - Filing type (10-K or 10-Q)
  - Filing date
  - Content excerpt (500 chars)
  - Chunk metadata

**Example Usage:**

```python
from tools import search_sec_filings

# Search all tickers
result = search_sec_filings("What are the main risk factors?")

# Search specific ticker
result = search_sec_filings("What are the main risk factors?", ticker="AAPL")
print(result)
```

**Example Output:**

```
SEC Filing Results for: What are the main risk factors?

--- Result 1 ---
Ticker: AAPL
Filing: 10-K
Date: 2024-01-15

Content:
Risk Factors: The Company faces intense competition in the markets where it operates. The Company's business, financial condition, and results of operations could be materially adversely affected by these and other risks. Competition has been particularly intense in the smartphone, personal computer, and tablet markets. The Company expects competition to continue to intensify as competitors introduce new products and services...

--- Result 2 ---
Ticker: AAPL
Filing: 10-K
Date: 2024-01-15

Content:
Our business is subject to risks associated with international operations. A significant portion of our revenue is generated outside the United States. International operations are subject to various risks including currency fluctuations, political instability, trade restrictions, and compliance with foreign regulations. Changes in the economic or political conditions in countries where we operate could adversely impact our business...

--- Result 3 ---
Ticker: AAPL
Filing: 10-Q
Date: 2024-07-10

Content:
Changes in currency exchange rates could adversely affect our financial results. We are exposed to foreign currency risk as a significant portion of our sales, expenses, and assets are denominated in currencies other than the U.S. dollar. Strengthening of the dollar relative to other currencies can negatively impact reported revenues and earnings when translated to dollars...
```

**How It Works:**

1. **Ingestion Phase** (one-time):

   ```
   SEC EDGAR → Download filings → Chunk documents → Create embeddings → Store in Pinecone
   ```

2. **Retrieval Phase** (runtime):

   ```
   User query → Embed query → Vector search → MMR ranking → Return top 5 chunks
   ```

3. **MMR (Maximal Marginal Relevance):**
   - Balances relevance with diversity
   - Avoids returning 5 similar chunks
   - λ = 0.7 (70% relevance, 30% diversity)

**Use Cases:**

- Deep company research
- Risk factor analysis
- Business strategy insights
- Competitive landscape research
- Management discussion analysis
- Financial metrics context
- Historical performance context

**Example Queries:**

- "What are the company's main revenue sources?"
- "What risks does the company face?"
- "How does the company describe its competitive advantages?"
- "What is the company's growth strategy?"
- "What are the company's key financial metrics?"
- "What does management say about recent performance?"

**Advantages Over Traditional Search:**

- ✅ Semantic understanding (understands intent, not just keywords)
- ✅ Finds relevant info even with different wording
- ✅ Returns diverse results (MMR)
- ✅ Works across multiple filings simultaneously

**Limitations:**

- ❌ Only covers AAPL, TSLA, MSFT, AMZN
- ❌ Limited to 3 × 10-K + 2 × 10-Q per ticker
- ❌ Not real-time (filings updated quarterly/annually)
- ❌ Requires OpenAI API calls (cost per query)

**Tips:**

- Be specific in your queries
- Use natural language questions
- Filter by ticker for focused results
- Compare across companies by omitting ticker filter

---

## 🧮 Utility Tools

### 11. `calculator(expression: str)`

**Purpose:** Evaluate mathematical expressions safely

**Technology:** NumExpr (safe mathematical expression evaluation)

**Parameters:**

- `expression` (str): Mathematical expression to evaluate

**Supported Operations:**

- **Basic Arithmetic:** `+`, `-`, `*`, `/`, `**` (power), `%` (modulo)
- **Parentheses:** `(`, `)`
- **Functions:** `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `abs`

**Example Usage:**

```python
from tools import calculator

# Basic calculation
result = calculator("(175.23 * 100) / 28.45")
print(result)

# P/E ratio calculation
result = calculator("175.23 / 6.16")
print(result)

# Percentage change
result = calculator("((175.23 - 170.00) / 170.00) * 100")
print(result)
```

**Example Output:**

```
(175.23 * 100) / 28.45 = 616.0281688

175.23 / 6.16 = 28.4480519481

((175.23 - 170.00) / 170.00) * 100 = 3.076470588
```

**Common Financial Calculations:**

1. **P/E Ratio:**

   ```python
   calculator("stock_price / eps")
   # Example: calculator("175.23 / 6.16")
   ```

2. **Percentage Change:**

   ```python
   calculator("((new_price - old_price) / old_price) * 100")
   # Example: calculator("((175 - 170) / 170) * 100")
   ```

3. **Market Cap:**

   ```python
   calculator("stock_price * shares_outstanding")
   # Example: calculator("175.23 * 15730000000")
   ```

4. **Dividend Yield:**

   ```python
   calculator("(annual_dividend / stock_price) * 100")
   # Example: calculator("(0.96 / 175.23) * 100")
   ```

5. **Return on Investment:**
   ```python
   calculator("((current_value - initial_value) / initial_value) * 100")
   ```

**Use Cases:**

- Financial ratio calculations
- Portfolio value calculations
- Percentage changes
- Quick math during analysis
- Custom metric calculations

**Safety Features:**

- ✅ No code execution (safe evaluation)
- ✅ No file system access
- ✅ No network access
- ✅ Only mathematical operations

**Limitations:**

- ❌ Cannot access variables or state
- ❌ Cannot define custom functions
- ❌ Limited to single expression evaluation

---

## 📊 Tool Summary Table

### Quick Reference

| Tool                          | Category | Data Source       | Cost      | Real-time?     | Rate Limit  |
| ----------------------------- | -------- | ----------------- | --------- | -------------- | ----------- |
| `get_current_price_yahoo`     | Market   | Yahoo Finance     | Free      | Near real-time | None        |
| `get_key_metrics`             | Market   | Yahoo Finance     | Free      | Real-time      | None        |
| `technical_analysis`          | Market   | Alpha Vantage     | Free      | 15-min delay   | 5 calls/min |
| `compare_stocks`              | Market   | Yahoo Finance     | Free      | Real-time      | None        |
| `get_company_info`            | Company  | Yahoo Finance     | Free      | Daily updates  | None        |
| `get_financials`              | Company  | Yahoo Finance     | Free      | Quarterly      | None        |
| `get_earnings_history`        | Company  | Yahoo Finance     | Free      | Real-time      | None        |
| `get_analyst_recommendations` | Company  | Yahoo Finance     | Free      | Real-time      | None        |
| `fetch_latest_news`           | News     | EventRegistry     | Free tier | Real-time      | 1000/day    |
| `search_sec_filings`          | RAG      | Pinecone + OpenAI | Paid      | Offline        | Unlimited   |
| `calculator`                  | Utility  | NumExpr           | Free      | Instant        | None        |

### By Use Case

**Day Trading:**

- `get_current_price_yahoo` - Live prices
- `technical_analysis` - RSI signals
- `fetch_latest_news` - Breaking news

**Fundamental Analysis:**

- `get_key_metrics` - Valuation metrics
- `get_financials` - Financial statements
- `get_analyst_recommendations` - Price targets
- `search_sec_filings` - Deep dive research

**Portfolio Management:**

- `compare_stocks` - Multi-stock comparison
- `get_key_metrics` - Risk assessment (beta)
- `get_earnings_history` - Track performance

**Research:**

- `get_company_info` - Company overview
- `search_sec_filings` - Detailed analysis
- `get_analyst_recommendations` - Wall Street view
- `fetch_latest_news` - Current events

### By Data Freshness

**Real-time (< 1 minute):**

- `get_current_price_yahoo`
- `get_key_metrics`
- `get_earnings_history`
- `get_analyst_recommendations`
- `fetch_latest_news`

**Near real-time (15 minutes):**

- `technical_analysis` (Alpha Vantage free tier)

**Updated Daily:**

- `get_company_info`

**Updated Quarterly/Annually:**

- `get_financials`
- `search_sec_filings` (10-K, 10-Q)

---

## 🔑 Required API Keys

### OpenAI

- **Purpose:** LLM reasoning + embeddings for RAG
- **Cost:** Pay-per-use (GPT-4: ~$0.01-0.03 per 1K tokens, Embeddings: ~$0.0001 per 1K tokens)
- **Get key:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Pinecone

- **Purpose:** Vector database for SEC filings
- **Cost:** Free tier (1 index, 5M vectors), Paid starts at $70/month
- **Get key:** [app.pinecone.io](https://app.pinecone.io)

### Alpha Vantage

- **Purpose:** Technical analysis indicators
- **Cost:** Free (5 API calls/minute, 500/day), Premium starts at $50/month
- **Get key:** [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

### EventRegistry

- **Purpose:** News articles aggregation
- **Cost:** Free tier (1000 calls/day), Paid starts at $99/month
- **Get key:** [eventregistry.org](https://eventregistry.org)

### Yahoo Finance (yfinance)

- **Purpose:** Market data, company info, financials
- **Cost:** Free (no API key required)
- **Package:** `yfinance` Python library

---

## 🚀 Best Practices

### Tool Selection

1. **For quick price checks:** Use `get_current_price_yahoo`
2. **For valuation analysis:** Use `get_key_metrics` + `get_financials`
3. **For deep research:** Use `search_sec_filings` + `get_company_info`
4. **For timing trades:** Use `technical_analysis` + `fetch_latest_news`
5. **For comparing options:** Use `compare_stocks`

### Performance Tips

1. **Batch requests:** If analyzing multiple stocks, use `compare_stocks` instead of multiple individual calls
2. **Cache results:** Market data tools return real-time data, consider caching for 1-5 minutes
3. **Filter RAG searches:** Always use `ticker` parameter when searching for specific company
4. **Monitor rate limits:** Alpha Vantage has 5 calls/min limit on free tier

### Error Handling

All tools return error messages as strings when issues occur:

- Invalid tickers
- API rate limits
- Network errors
- No data available

Example error outputs:

```
"Error: Invalid ticker 'XYZ'"
"Error: API rate limit reached. Try again later."
"No earnings data available for PRIVATE-CO"
```

---

## 📧 Support

For issues, questions, or feature requests:

- **GitHub Issues:** [github.com/faniyi-akinbobola/QuantFlow-Agent/issues](https://github.com/faniyi-akinbobola/QuantFlow-Agent/issues)
- **Email:** your.email@example.com

---

**Last Updated:** April 17, 2026  
**Version:** 1.0.0
