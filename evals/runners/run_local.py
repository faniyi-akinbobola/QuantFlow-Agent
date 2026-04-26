"""
Local Evaluation Runner
Runs evaluations locally for development and testing
"""

import sys
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, List
import yaml

# Add parent directory to path to import from evals
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evals.utils.dataset_loader import DatasetLoader
from evals.utils.metric_aggregator import MetricAggregator
from evals.utils.report_generator import ReportGenerator
from evals.evaluators.correctness import correctness_evaluator_llm
from evals.evaluators.faithfulness import faithfulness_evaluator_llm
from evals.evaluators.reasoning_quality import reasoning_quality_evaluator_llm
from evals.evaluators.tool_usage import tool_usage_evaluator
from evals.evaluators.rag.grounding import grounding_evaluator_llm
from evals.evaluators.rag.retrieval_metrics import retrieval_evaluator
from evals.metrics.cost import calculate_llm_cost, aggregate_costs
from evals.metrics.latency import aggregate_latencies
from evals.metrics.usage import avg_tools_per_query, overuse_rate, tool_usage_distribution

from graph.graph import workflow
from graph.state import AgentState
from langgraph.checkpoint.memory import MemorySaver


class LocalEvaluationRunner:
    """Run evaluations locally."""
    
    def __init__(self, config_path: str = "evals/configs/eval_config.yaml"):
        """
        Initialize evaluation runner.
        
        Args:
            config_path: Path to evaluation configuration file
        """
        self.config = self._load_config(config_path)
        self.dataset_loader = DatasetLoader()
        self.metric_aggregator = MetricAggregator()
        self.report_generator = ReportGenerator(
            output_dir=self.config.get("reporting", {}).get("output_dir", "evals/reports")
        )
        self.results = []
        self.failures = []
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    async def run_agent(self, question: str, thread_id: str = "eval") -> Dict[str, Any]:
        """
        Run the agent on a single question.
        
        Args:
            question: Question to ask the agent
            thread_id: Thread ID for conversation
            
        Returns:
            Dictionary with answer, tools used, and metadata
        """
        start_time = time.time()
        
        try:
            # Use fresh in-memory checkpointer per eval run to avoid stale state
            checkpointer = MemorySaver()
            
            # Compile graph with checkpointer
            app = workflow.compile(checkpointer=checkpointer)
            
            # Run the agent with recursion limit to prevent infinite loops
            config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 25
            }
            input_state = {"messages": [("user", question)]}
            
            result = await app.ainvoke(input_state, config)
            
            # Extract information
            messages = result["messages"]
            last_message = messages[-1]
            
            # Get answer
            answer = last_message.content if hasattr(last_message, 'content') else str(last_message)
            
            # Extract tools used
            tools_used = []
            for msg in messages:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tools_used.append(tool_call.get('name', 'unknown'))
            
            latency = time.time() - start_time
            
            return {
                "answer": answer,
                "tools_used": tools_used,
                "latency": latency,
                "success": True,
                "messages": messages
            }
            
        except Exception as e:
            latency = time.time() - start_time
            return {
                "answer": f"Error: {str(e)}",
                "tools_used": [],
                "latency": latency,
                "success": False,
                "error": str(e)
            }
    
    async def evaluate_dataset(self, dataset_name: str) -> Dict[str, Any]:
        """
        Evaluate a single dataset.
        
        Args:
            dataset_name: Name of the dataset to evaluate
            
        Returns:
            Evaluation results for the dataset
        """
        print(f"\n📊 Evaluating dataset: {dataset_name}")
        
        # Load dataset
        dataset = self.dataset_loader.load_dataset(dataset_name)
        print(f"  Loaded {len(dataset)} test cases")
        
        # Run agent on each example
        results = []
        for i, example in enumerate(dataset):
            print(f"  Progress: {i+1}/{len(dataset)}", end='\r')
            
            question = example.get("question", "")
            thread_id = f"eval_{dataset_name}_{i}"
            
            # Run agent
            agent_result = await self.run_agent(question, thread_id)
            
            # Combine with example
            result = {
                **example,
                **agent_result
            }
            results.append(result)
        
        print(f"  ✅ Completed {len(results)} evaluations")
        
        # Run evaluators
        dataset_config = self.config.get("datasets", {}).get(dataset_name, {})
        evaluator_scores = await self._run_evaluators(dataset_name, results, dataset)
        
        # Calculate metrics
        passed = sum(1 for r in results if r.get("success", False))
        total = len(results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "dataset_name": dataset_name,
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": pass_rate,
            "results": results,
            "evaluator_scores": evaluator_scores
        }
    
    async def _run_evaluators(
        self, 
        dataset_name: str, 
        results: List[Dict[str, Any]], 
        dataset: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Run all applicable evaluators on results."""
        evaluator_scores = {}
        evaluator_config = self.config.get("evaluators", {})
        
        # Tool Usage Evaluator
        if "tool_usage" in evaluator_config and evaluator_config["tool_usage"].get("enabled"):
            if dataset_name in evaluator_config["tool_usage"].get("applicable_to", []):
                score = tool_usage_evaluator(results, dataset)
                evaluator_scores["tool_usage"] = score
                print(f"    Tool Usage: {score:.2f}%")
        
        # Correctness Evaluator
        if "correctness" in evaluator_config and evaluator_config["correctness"].get("enabled"):
            if dataset_name in evaluator_config["correctness"].get("applicable_to", []):
                examples = [
                    {
                        "question": r.get("question", ""),
                        "output": r.get("answer", ""),
                        "reference": r.get("reference", "")
                    }
                    for r in results
                ]
                score = correctness_evaluator_llm(examples)
                evaluator_scores["correctness"] = score
                print(f"    Correctness: {score:.2f}%")
        
        # Faithfulness Evaluator
        if "faithfulness" in evaluator_config and evaluator_config["faithfulness"].get("enabled"):
            if dataset_name in evaluator_config["faithfulness"].get("applicable_to", []):
                examples = [
                    {
                        "question": r.get("question", ""),
                        "answer": r.get("answer", ""),
                        "context": r.get("context", "")
                    }
                    for r in results if r.get("context")
                ]
                if examples:
                    score = faithfulness_evaluator_llm(examples)
                    evaluator_scores["faithfulness"] = score
                    print(f"    Faithfulness: {score:.2f}%")
        
        # Reasoning Quality Evaluator
        if "reasoning_quality" in evaluator_config and evaluator_config["reasoning_quality"].get("enabled"):
            if dataset_name in evaluator_config["reasoning_quality"].get("applicable_to", []):
                examples = [
                    {
                        "question": r.get("question", ""),
                        "answer": r.get("answer", "")
                    }
                    for r in results
                ]
                score = reasoning_quality_evaluator_llm(examples)
                evaluator_scores["reasoning_quality"] = score
                print(f"    Reasoning Quality: {score:.2f}%")
        
        return evaluator_scores
    
    async def run_all_evaluations(self) -> Dict[str, Any]:
        """
        Run all enabled evaluations.
        
        Returns:
            Complete evaluation results
        """
        print("🚀 Starting QuantFlow Agent Evaluation")
        print(f"Project: {self.config.get('project_name', 'Unknown')}")
        print(f"Version: {self.config.get('version', 'Unknown')}\n")
        
        start_time = time.time()
        
        # Get enabled datasets
        datasets_config = self.config.get("datasets", {})
        enabled_datasets = [
            name for name, config in datasets_config.items()
            if config.get("enabled", True)
        ]
        
        print(f"📋 Enabled datasets: {', '.join(enabled_datasets)}\n")
        
        # Run evaluations
        dataset_results = {}
        for dataset_name in enabled_datasets:
            try:
                result = await self.evaluate_dataset(dataset_name)
                dataset_results[dataset_name] = result
                
                # Track failures
                for r in result["results"]:
                    if not r.get("success", False):
                        self.failures.append({
                            "dataset": dataset_name,
                            "id": r.get("id", "unknown"),
                            "question": r.get("question", ""),
                            "reason": r.get("error", "Unknown error")
                        })
                
            except Exception as e:
                print(f"  ❌ Error evaluating {dataset_name}: {e}")
                continue
        
        # Aggregate metrics
        all_results = []
        for dataset_result in dataset_results.values():
            all_results.extend(dataset_result["results"])
        
        # Calculate overall metrics
        total_tests = sum(r["total"] for r in dataset_results.values())
        total_passed = sum(r["passed"] for r in dataset_results.values())
        overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # Latency metrics
        latency_stats = aggregate_latencies(all_results)
        
        # Usage metrics
        usage_stats = {
            "avg_tools_per_query": avg_tools_per_query(all_results),
            "overuse_rate": overuse_rate(all_results),
            "tool_distribution": tool_usage_distribution(all_results)
        }
        
        total_duration = time.time() - start_time
        
        # Compile final results
        final_results = {
            "summary": {
                "total_tests": total_tests,
                "passed": total_passed,
                "failed": total_tests - total_passed,
                "pass_rate": overall_pass_rate,
                "duration": total_duration,
                "total_cost": 0.0  # Would need to track actual API costs
            },
            "datasets": dataset_results,
            "metrics": {
                "latency": latency_stats,
                "usage": usage_stats
            },
            "failures": self.failures,
            "config": self.config
        }
        
        return final_results
    
    async def run_and_report(self):
        """Run evaluations and generate reports."""
        # Run evaluations
        results = await self.run_all_evaluations()
        
        # Generate reports
        print("\n📝 Generating reports...")
        report_formats = self.config.get("reporting", {}).get("format", ["json", "markdown"])
        generated_files = self.report_generator.generate_report(
            results,
            formats=report_formats,
            include_failures=self.config.get("reporting", {}).get("include_failures", True),
            include_examples=self.config.get("reporting", {}).get("include_examples", True)
        )
        
        print("\n✅ Evaluation Complete!")
        print(f"Pass Rate: {results['summary']['pass_rate']:.2f}%")
        print(f"Duration: {results['summary']['duration']:.2f}s")
        print(f"\nReports generated:")
        for format_type, file_path in generated_files.items():
            print(f"  - {format_type}: {file_path}")


async def main():
    """Main entry point for local evaluation."""
    runner = LocalEvaluationRunner()
    await runner.run_and_report()


if __name__ == "__main__":
    asyncio.run(main())
