#!/usr/bin/env python3
"""Analyze regression test failures from the evaluation report."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from collections import defaultdict

# Load the evaluation report
report_path = Path("evals/reports/eval_report_20260425_222809.json")

with open(report_path) as f:
    data = json.load(f)

regression = data['datasets']['regression_suite']
results = regression['results']

print("=" * 80)
print("REGRESSION TEST ANALYSIS")
print("=" * 80)
print(f"\nOverall: {regression['passed']}/{regression['total']} passed ({regression['pass_rate']:.1f}%)")
print(f"Correctness Score: {regression['evaluator_scores'].get('correctness', 'N/A')}%")
print(f"Tool Usage Score: {regression['evaluator_scores'].get('tool_usage', 'N/A')}%")
print(f"Reasoning Quality Score: {regression['evaluator_scores'].get('reasoning_quality', 'N/A')}%")

# Analyze each test
print("\n" + "=" * 80)
print("DETAILED TEST RESULTS")
print("=" * 80)

failures = []
successes = []

for test in results:
    test_id = test.get('id', 'unknown')
    question = test.get('question', '')
    success = test.get('success', False)
    tools_used = test.get('tools_used', [])
    answer = test.get('answer', '')
    
    # Get expected from dataset
    expected_tools = test.get('expected_tools', [])
    expected_contains = test.get('expected_answer_contains', [])
    
    # Check if tools match
    tools_match = set(expected_tools).issubset(set(tools_used)) if expected_tools else True
    
    # Check if answer contains expected content
    answer_match = all(
        keyword.lower() in answer.lower() 
        for keyword in expected_contains
    ) if expected_contains else True
    
    result = {
        'id': test_id,
        'question': question,
        'success': success,
        'tools_used': tools_used,
        'expected_tools': expected_tools,
        'tools_match': tools_match,
        'expected_contains': expected_contains,  # Added this
        'answer_match': answer_match,
        'answer_preview': answer[:150] + '...' if len(answer) > 150 else answer
    }
    
    if not success or not tools_match or not answer_match:
        failures.append(result)
    else:
        successes.append(result)

# Print failures
if failures:
    print(f"\n❌ FAILURES ({len(failures)} tests):\n")
    for i, test in enumerate(failures, 1):
        print(f"{i}. {test['id']}: {test['question']}")
        print(f"   Expected tools: {test['expected_tools']}")
        print(f"   Used tools: {test['tools_used']}")
        print(f"   Tools match: {'✅' if test['tools_match'] else '❌'}")
        print(f"   Expected in answer: {test['expected_contains']}")
        print(f"   Answer match: {'✅' if test['answer_match'] else '❌'}")
        print(f"   Answer: {test['answer_preview']}")
        print()
else:
    print("\n✅ No failures detected!")

# Summary by issue type
print("\n" + "=" * 80)
print("FAILURE CATEGORIES")
print("=" * 80)

tool_issues = [f for f in failures if not f['tools_match']]
answer_issues = [f for f in failures if not f['answer_match']]

print(f"\nTool Selection Issues: {len(tool_issues)}")
for test in tool_issues:
    print(f"  - {test['id']}: Expected {test['expected_tools']}, got {test['tools_used']}")

print(f"\nAnswer Content Issues: {len(answer_issues)}")
for test in answer_issues:
    print(f"  - {test['id']}: Missing keywords {test['expected_contains']}")

# Tool usage distribution
print("\n" + "=" * 80)
print("TOOL USAGE DISTRIBUTION")
print("=" * 80)

tool_counts = defaultdict(int)
for test in results:
    for tool in test.get('tools_used', []):
        tool_counts[tool] += 1

for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {tool}: {count}")

print("\n" + "=" * 80)
