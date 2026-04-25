# QuantFlow Agent Evaluation Framework

A comprehensive evaluation suite for testing the QuantFlow stock market AI agent's performance, accuracy, and reliability.

## 🎯 Overview

This evaluation framework provides:

- **Multiple Datasets**: 85+ test cases across 6 categories
- **LLM Judges**: Automated evaluation using GPT-4o-mini
- **Deterministic Metrics**: Tool usage, retrieval quality, performance metrics
- **Rich Reports**: JSON, Markdown, and HTML outputs
- **CI/CD Integration**: Automated testing with threshold enforcement
- **Comprehensive Coverage**: RAG, tool usage, edge cases, out-of-scope detection

## 📁 Directory Structure

```
evals/
├── configs/              # Configuration files
│   ├── eval_config.yaml     # Main evaluation configuration
│   └── llm_judges.yaml      # LLM judge prompts and settings
├── dataset/              # Test datasets (85+ test cases)
│   ├── rag_queries.json          # RAG retrieval tests (10 cases)
│   ├── investment_analysis.json  # Complex analysis (10 cases)
│   ├── tool_usage_cases.json     # Tool selection tests (25 cases)
│   ├── edge_cases.json           # Edge case handling (20 cases)
│   ├── out_of_scope.json         # Out-of-scope detection (15 cases)
│   └── regression_suite.json     # Core functionality (15 cases)
├── evaluators/           # Evaluation logic
│   ├── correctness.py           # Factual accuracy
│   ├── faithfulness.py          # Hallucination detection
│   ├── reasoning_quality.py     # Logical coherence
│   ├── tool_usage.py            # Tool selection accuracy
│   └── rag/
│       ├── grounding.py         # Context usage
│       └── retrieval_metrics.py # Recall@k, MRR, nDCG
├── metrics/              # Performance metrics
│   ├── cost.py                  # LLM API cost tracking
│   ├── latency.py               # Response time metrics
│   └── usage.py                 # Tool usage patterns
├── utils/                # Utility modules
│   ├── dataset_loader.py        # Load and sample datasets
│   ├── metric_aggregator.py     # Aggregate statistics
│   └── report_generator.py      # Generate reports
├── runners/              # Execution scripts
│   ├── run_local.py             # Local development runs
│   └── run_ci.py                # CI/CD pipeline runs
└── reports/              # Generated reports
    └── README.md                # Report documentation
```

## 🚀 Quick Start

### Run Local Evaluation

```bash
# From project root
python evals/runners/run_local.py
```

This will:
1. Load all enabled datasets
2. Run the agent on each test case
3. Apply evaluators (correctness, faithfulness, tool usage, etc.)
4. Calculate metrics (latency, cost, usage)
5. Generate reports in `evals/reports/`

### Run CI/CD Evaluation

```bash
# Set CI environment variable
export CI=true

# Run with threshold enforcement
python evals/runners/run_ci.py
```

This will:
- Run all evaluations
- Compare results against thresholds
- Exit with code 1 if thresholds are breached
- Exit with code 0 if all checks pass

## 📊 Datasets

### RAG Queries (10 cases)
Tests retrieval quality and context usage from SEC filings.

**Example:**
```json
{
  "question": "What was Apple's revenue in their latest 10-K filing?",
  "expected_behavior": "retrieve_and_answer",
  "relevant_doc_ids": ["AAPL_10K_2024"]
}
```

### Investment Analysis (10 cases)
Tests comprehensive investment analysis capabilities.

**Example:**
```json
{
  "question": "Should I invest in AAPL right now?",
  "expected_tools": ["get_current_price_yahoo", "get_key_metrics", "fetch_latest_news"],
  "required_components": ["current_price", "financial_metrics", "news_sentiment"]
}
```

### Tool Usage Cases (25 cases)
Tests correct tool selection and usage.

**Example:**
```json
{
  "question": "What's the latest news on Apple?",
  "expected_tools": ["fetch_latest_news"],
  "mode": "exact"
}
```

### Edge Cases (20 cases)
Tests error handling and graceful degradation.

**Example:**
```json
{
  "question": "",
  "expected_behavior": "graceful_error",
  "expected_response": "polite_clarification_request"
}
```

### Out of Scope (15 cases)
Tests detection of non-stock-market queries.

**Example:**
```json
{
  "question": "What is Bitcoin?",
  "expected_behavior": "out_of_scope",
  "category": "cryptocurrency"
}
```

### Regression Suite (15 cases)
Tests core functionality stability.

**Example:**
```json
{
  "question": "What's AAPL's current stock price?",
  "expected_tools": ["get_current_price_yahoo"],
  "difficulty": "easy"
}
```

## 🧪 Evaluators

### LLM-Based Evaluators

1. **Correctness** (GPT-4o-mini)
   - Evaluates factual accuracy
   - Threshold: 80%

2. **Faithfulness** (GPT-4o-mini)
   - Detects hallucinations
   - Ensures answers are grounded in context
   - Threshold: 90%

3. **Reasoning Quality** (GPT-4o-mini)
   - Assesses logical coherence
   - Threshold: 75%

4. **Grounding** (GPT-4o-mini)
   - Checks if RAG answers use retrieved context
   - Threshold: 85%

### Deterministic Evaluators

1. **Tool Usage**
   - Validates correct tool selection
   - Supports exact match and contains modes
   - Threshold: 85%

2. **Retrieval Metrics**
   - Recall@5, Precision@5, MRR, nDCG
   - Thresholds: 70%, 60%, 75%, 70%

## 📈 Metrics

### Latency Metrics
- Mean, Median, Min, Max
- P50, P95, P99 percentiles
- Thresholds: mean <5s, p95 <10s, p99 <15s

### Cost Metrics
- Per-query cost tracking
- Total budget monitoring
- Model-specific pricing (GPT-4o, GPT-4o-mini, etc.)

### Usage Metrics
- Average tools per query
- Tool usage distribution
- Overuse rate (>3 tools)
- Threshold: <3 tools average, <15% overuse

## ⚙️ Configuration

### eval_config.yaml

Main configuration file:

```yaml
datasets:
  rag_queries:
    enabled: true
    path: "evals/dataset/rag_queries.json"
    sample_size: null  # null = use all

evaluators:
  correctness:
    enabled: true
    threshold: 80
    model: "gpt-4o-mini"
    
metrics:
  latency:
    enabled: true
    thresholds:
      mean: 5.0
      p95: 10.0

ci:
  fail_on_threshold_breach: true
  parallel_execution: true
```

### llm_judges.yaml

LLM judge configurations with prompts:

```yaml
judges:
  correctness:
    model: "gpt-4o-mini"
    temperature: 0
    system_prompt: |
      You are a strict financial accuracy evaluator...
```

## 📝 Reports

### JSON Report
Complete machine-readable results:
```json
{
  "summary": {
    "total_tests": 85,
    "passed": 78,
    "pass_rate": 91.76
  },
  "datasets": {...},
  "metrics": {...}
}
```

### Markdown Report
Human-readable summary with tables and statistics.

### HTML Report
Interactive dashboard with cards and charts.

## 🔧 Development

### Adding New Datasets

1. Create JSON file in `evals/dataset/`
2. Add to `eval_config.yaml`:
```yaml
datasets:
  my_new_dataset:
    path: "evals/dataset/my_new_dataset.json"
    enabled: true
```

### Adding New Evaluators

1. Create evaluator in `evals/evaluators/`
2. Add to `eval_config.yaml`:
```yaml
evaluators:
  my_evaluator:
    enabled: true
    threshold: 80
    applicable_to: ["my_new_dataset"]
```
3. Integrate in `run_local.py`

### Running Specific Datasets

Edit `eval_config.yaml` and set `enabled: false` for unwanted datasets.

## 🎯 Best Practices

1. **Start Small**: Test with small datasets during development
2. **Set Realistic Thresholds**: Based on baseline performance
3. **Monitor Costs**: Track LLM API usage
4. **Version Reports**: Keep historical reports for comparison
5. **CI Integration**: Run on every PR to catch regressions

## 🐛 Troubleshooting

### Evaluations Running Slow
- Enable sampling in config: `sampling.enabled: true`
- Reduce concurrent LLM calls: `advanced.max_concurrent_llm_calls: 3`

### High API Costs
- Use cheaper model: `default_model: "gpt-4o-mini"`
- Enable caching: `cache.enabled: true`

### Threshold Failures
- Review failures in report
- Adjust thresholds if unrealistic
- Improve agent prompts/tools

## 📚 Resources

- [Evaluation Best Practices](https://docs.quantflow.ai/evals)
- [LangSmith Integration](https://docs.quantflow.ai/langsmith)
- [Custom Evaluators Guide](https://docs.quantflow.ai/custom-evals)

## 🤝 Contributing

To add new test cases:

1. Add examples to appropriate dataset JSON
2. Follow existing format
3. Include all required fields
4. Test locally before committing

## 📄 License

Part of the QuantFlow Agent project.
