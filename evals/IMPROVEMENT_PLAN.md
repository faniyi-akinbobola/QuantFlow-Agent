# Evaluation Results - Improvement Plan

## Executive Summary

**Current Status:** 98.95% pass rate (94/95 tests passed)  
**Evaluation Date:** April 25, 2026

---

## 🔴 Critical Issues

### 1. RAG Retrieval - 50% Correctness Score

**Root Cause:**  
The vector database only contains **2 tickers** (AAPL and TSLA) out of 10+ required tickers.

```
Total documents: 51,438
Indexed tickers: AAPL (51,431 docs), TSLA (7 docs)
Missing tickers: MSFT, GOOGL, AMZN, NVDA, META, NFLX, INTC, AMD
```

**Failed Queries:**
- ❌ `rag_003`: Tesla's operating expenses (low data volume - only 7 docs)
- ❌ `rag_009`: Intel's capital expenditure (ticker not indexed)
- ❌ `rag_010`: AMD's competitive positioning (ticker not indexed)

**Impact:**  
- 50% of RAG queries fail or return incomplete data
- Users get "No relevant SEC filings found" errors
- Defeats the purpose of having SEC filing analysis

**Solution:**

#### Option A: Complete Ingestion (Recommended)
```bash
# Ingest all required tickers
cd /Users/akinbobola/Works/stock_agent

# Add missing tickers to ingestion script
TICKERS=("MSFT" "GOOGL" "AMZN" "NVDA" "META" "NFLX" "INTC" "AMD")

for ticker in "${TICKERS[@]}"; do
    echo "Ingesting $ticker..."
    uv run python scripts/ingest.py --ticker $ticker --forms 10-K,10-Q
done
```

#### Option B: Improve Chunk Size & Retrieval
Current settings:
- `chunk_size`: 1000 characters
- `chunk_overlap`: 200 characters  
- `top_k`: 5 results

Recommended improvements:
```python
# rag/chunking.py
chunk_size = 1500  # Increase for more context
chunk_overlap = 300  # More overlap for continuity

# tools/rag/retrieval_tool.py
top_k = 8  # Return more results
```

#### Option C: Add Metadata Filtering
Improve search by adding date filters:
```python
# In retrieval_tool.py - add date filtering
from datetime import datetime, timedelta

recent_date = datetime.now() - timedelta(days=365)

results = vectorstore.similarity_search(
    query,
    k=top_k,
    filter={
        "ticker": ticker.upper(),
        "date": {"$gte": recent_date.strftime("%Y-%m-%d")}
    }
)
```

**Priority:** 🔴 **CRITICAL** - Blocks 50% of RAG functionality

**Estimated Effort:** 
- Option A: 2-4 hours (ingestion time)
- Option B: 30 minutes
- Option C: 1 hour

---

### 2. Tool Orchestration - 10% Tool Usage Score

**Root Cause:**  
Agent uses too few tools for investment analysis. Only averaging **2.6 tools per query** when comprehensive analysis requires **4-6 tools**.

**Example Failure:**
```
Query: "Should I invest in AAPL right now? Provide comprehensive analysis."
Expected tools: get_company_info, get_key_metrics, get_analyst_recommendations, 
               get_earnings_history, fetch_latest_news, technical_analysis
Actual tools used: Sometimes only 1-2 tools
```

**Tool Distribution Analysis:**
```
Tool                          Usage Count
get_analyst_recommendations   36/95 (38%)
get_key_metrics              32/95 (34%)
fetch_latest_news            29/95 (31%)
technical_analysis           28/95 (29%)
get_current_price_yahoo      20/95 (21%)
get_financials               19/95 (20%)
get_earnings_history         18/95 (19%)
search_sec_filings           25/95 (26%)
```

**Impact:**
- Incomplete investment analysis
- Users miss critical data points
- Poor decision-making support

**Solution:**

#### Fix 1: Improve Agent Prompts
```python
# llm/prompt.py - Add explicit tool usage guidance

SYSTEM_PROMPT = """
You are QuantFlow, an expert stock market analyst...

**COMPREHENSIVE ANALYSIS REQUIREMENTS:**

For investment questions like "Should I invest in [TICKER]?", you MUST:
1. ✅ Get current price and key metrics (get_key_metrics)
2. ✅ Check analyst recommendations (get_analyst_recommendations)
3. ✅ Review recent earnings (get_earnings_history)
4. ✅ Fetch latest news (fetch_latest_news)
5. ✅ Perform technical analysis (technical_analysis)
6. ✅ Get company info (get_company_info)

For comparison questions, you MUST:
1. ✅ Use compare_stocks tool first
2. ✅ Then get detailed metrics for each ticker

**NEVER provide investment analysis with fewer than 4 tools.**
"""
```

#### Fix 2: Add Tool Planning Node
Create a new node in the graph that plans which tools to use:

```python
# graph/nodes.py

def plan_tools_node(state: AgentState) -> AgentState:
    """Plan which tools are needed based on query type."""
    
    query = state["messages"][-1].content.lower()
    required_tools = []
    
    # Investment analysis
    if any(word in query for word in ["invest", "buy", "analysis", "should i"]):
        required_tools = [
            "get_company_info",
            "get_key_metrics", 
            "get_analyst_recommendations",
            "get_earnings_history",
            "fetch_latest_news",
            "technical_analysis"
        ]
    
    # Comparison
    elif "compare" in query or " vs " in query or " versus " in query:
        required_tools = ["compare_stocks", "get_key_metrics"]
    
    # Add to state
    state["required_tools"] = required_tools
    state["tools_used"] = []
    
    return state
```

#### Fix 3: Add Tool Validation
```python
# graph/nodes.py - Enhance call_tools node

def call_tools_node(state: AgentState) -> AgentState:
    """Enhanced tool calling with validation."""
    
    # ... existing tool calling logic ...
    
    # Validate tool usage
    required = set(state.get("required_tools", []))
    used = set(state.get("tools_used", []))
    
    missing = required - used
    
    if missing:
        # Force LLM to use missing tools
        reminder = HumanMessage(
            content=f"⚠️ Missing required tools: {', '.join(missing)}. Please use these tools before providing final answer."
        )
        state["messages"].append(reminder)
    
    return state
```

**Priority:** 🟠 **HIGH** - Affects investment analysis quality

**Estimated Effort:** 
- Fix 1: 30 minutes
- Fix 2: 2 hours
- Fix 3: 1 hour

---

### 3. Regression Suite - 53% Correctness Score

**Root Cause:**  
Need to investigate specific failures in regression tests.

**Test Dataset:** `evals/dataset/regression_suite.json`

**Analysis Needed:**
1. Which specific tests are failing?
2. What changed since they last passed?
3. Are failures in tools, LLM reasoning, or RAG?

**Investigation Steps:**

```bash
# 1. Check which regression tests failed
uv run python -c "
import json
with open('evals/reports/eval_report_20260425_222809.json') as f:
    data = json.load(f)
    
regression = data['datasets']['regression_suite']['results']

print('Regression Test Analysis:')
print('=' * 50)

for test in regression:
    test_id = test.get('id', 'unknown')
    question = test.get('question', '')
    
    # Check evaluator scores in messages
    print(f'\n{test_id}: {question[:60]}...')
    print(f'  Tools used: {test.get(\"tools_used\", [])}')
    print(f'  Success: {test.get(\"success\", False)}')
"
```

**Solution:**

1. **Run Detailed Regression Analysis**
```bash
# Create regression analysis script
uv run python evals/runners/run_local.py \
    --dataset regression_suite \
    --verbose \
    --save-failures
```

2. **Fix Individual Regressions**
- Review each failed test case
- Identify if it's a tool issue, prompt issue, or RAG issue
- Apply targeted fixes

3. **Add Regression Prevention**
```python
# Add to CI/CD pipeline
if regression_pass_rate < 85%:
    fail_build("Regression tests below threshold")
```

**Priority:** 🟡 **MEDIUM** - Core functionality working but needs refinement

**Estimated Effort:** 
- Investigation: 1 hour
- Fixes: 2-4 hours per issue

---

## 🟢 Strengths to Maintain

✅ **Edge Cases: 100%** - Excellent error handling  
✅ **Out-of-Scope: 100%** - Perfect query filtering  
✅ **Reasoning Quality: 86-100%** - Strong LLM reasoning  
✅ **Overall Reliability: 98.95%** - Very stable

---

## Implementation Roadmap

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Improve retrieval chunk size and top_k
2. ✅ Update agent prompts with tool requirements
3. ✅ Run regression test analysis

### Phase 2: RAG Data (2-4 hours)
1. ✅ Ingest missing tickers (MSFT, GOOGL, AMZN, NVDA, META, NFLX, INTC, AMD)
2. ✅ Verify ingestion with check_chroma.py
3. ✅ Re-run RAG evaluation

### Phase 3: Tool Orchestration (3-4 hours)
1. ✅ Add tool planning node
2. ✅ Add tool validation
3. ✅ Test with investment analysis dataset

### Phase 4: Regression Fixes (2-4 hours)
1. ✅ Identify specific failures
2. ✅ Apply targeted fixes
3. ✅ Re-run full evaluation

### Phase 5: Validation (30 minutes)
1. ✅ Run complete evaluation suite
2. ✅ Target: >90% on all metrics
3. ✅ Generate final report

---

## Success Criteria

**Target Metrics:**
- RAG Correctness: 50% → **85%+**
- Tool Usage: 10% → **80%+** (investment_analysis)
- Regression Correctness: 53% → **85%+**
- Overall Pass Rate: 98.95% → **99%+**

**Validation:**
```bash
# After improvements, re-run evaluation
uv run python evals/runners/run_local.py

# Expected output:
# RAG Correctness: 85%+
# Tool Usage: 80%+  
# Regression Correctness: 85%+
# Pass Rate: 99%+
```

---

## Next Steps

1. **Choose Priority:** Which issue to tackle first?
   - 🔴 RAG Retrieval (blocking 50% of queries)
   - 🟠 Tool Orchestration (poor analysis quality)
   - 🟡 Regression Fixes (refinement)

2. **Allocate Time:**
   - Quick fixes: 1-2 hours
   - Full improvement: 8-12 hours

3. **Run Evaluation:**
   - After each fix, re-run evaluation
   - Track progress toward targets

---

## Commands Reference

```bash
# Check what's in database
uv run python scripts/check_chroma.py

# Ingest new ticker
uv run python scripts/ingest.py --ticker MSFT --forms 10-K,10-Q

# Run specific dataset
uv run python evals/runners/run_local.py --dataset rag_queries

# Run full evaluation
uv run python evals/runners/run_local.py

# View results
open evals/reports/eval_report_*.html
```

---

## Files to Modify

### RAG Improvements
- ` rag/chunking.py` - Increase chunk size
- `tools/rag/retrieval_tool.py` - Increase top_k, add date filtering
- `scripts/ingest.py` - Ingest missing tickers

### Tool Orchestration
- `llm/prompt.py` - Add tool usage requirements
- `graph/nodes.py` - Add tool planning & validation
- `graph/graph.py` - Integrate new nodes

### Regression Fixes
- `evals/dataset/regression_suite.json` - Review test cases
- Individual tool files - Fix specific issues

---

**Document Generated:** April 25, 2026  
**Evaluation Run:** eval_report_20260425_222809
