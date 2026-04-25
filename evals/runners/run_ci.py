"""
CI/CD Evaluation Runner
Runs evaluations in CI/CD pipelines with strict thresholds and fast-fail options
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, Any
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evals.runners.run_local import LocalEvaluationRunner


class CIEvaluationRunner(LocalEvaluationRunner):
    """Run evaluations in CI/CD environment with threshold enforcement."""
    
    def __init__(self, config_path: str = "evals/configs/eval_config.yaml"):
        """Initialize CI evaluation runner."""
        super().__init__(config_path)
        self.ci_config = self.config.get("ci", {})
        self.threshold_breaches = []
        
    async def run_with_thresholds(self) -> Dict[str, Any]:
        """
        Run evaluations and check against thresholds.
        
        Returns:
            Evaluation results with threshold comparison
        """
        # Run all evaluations
        results = await self.run_all_evaluations()
        
        # Check thresholds
        threshold_results = self._check_thresholds(results)
        results["threshold_comparison"] = threshold_results
        
        # Determine if we should fail CI
        should_fail = self._should_fail_ci(threshold_results)
        results["ci_status"] = "failed" if should_fail else "passed"
        
        return results
    
    def _check_thresholds(self, results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Check results against configured thresholds.
        
        Args:
            results: Evaluation results
            
        Returns:
            Dictionary of threshold comparisons
        """
        threshold_results = {}
        
        # Check evaluator thresholds
        evaluator_config = self.config.get("evaluators", {})
        
        for dataset_name, dataset_result in results.get("datasets", {}).items():
            for evaluator_name, score in dataset_result.get("evaluator_scores", {}).items():
                if evaluator_name in evaluator_config:
                    threshold = evaluator_config[evaluator_name].get("threshold", 0)
                    passed = score >= threshold
                    
                    key = f"{dataset_name}_{evaluator_name}"
                    threshold_results[key] = {
                        "passed": passed,
                        "threshold": threshold,
                        "actual": score,
                        "difference": score - threshold
                    }
                    
                    if not passed:
                        self.threshold_breaches.append({
                            "metric": key,
                            "threshold": threshold,
                            "actual": score,
                            "difference": score - threshold
                        })
        
        # Check latency thresholds
        latency_config = self.config.get("metrics", {}).get("latency", {})
        if latency_config.get("enabled"):
            latency_stats = results.get("metrics", {}).get("latency", {})
            latency_thresholds = latency_config.get("thresholds", {})
            
            for metric, threshold in latency_thresholds.items():
                actual = latency_stats.get(metric, 0)
                passed = actual <= threshold
                
                threshold_results[f"latency_{metric}"] = {
                    "passed": passed,
                    "threshold": threshold,
                    "actual": actual,
                    "difference": actual - threshold
                }
                
                if not passed:
                    self.threshold_breaches.append({
                        "metric": f"latency_{metric}",
                        "threshold": threshold,
                        "actual": actual,
                        "difference": actual - threshold
                    })
        
        # Check usage thresholds
        usage_config = self.config.get("metrics", {}).get("usage", {})
        if usage_config.get("enabled"):
            usage_stats = results.get("metrics", {}).get("usage", {})
            usage_thresholds = usage_config.get("thresholds", {})
            
            for metric, threshold in usage_thresholds.items():
                actual = usage_stats.get(metric, 0)
                passed = actual <= threshold
                
                threshold_results[f"usage_{metric}"] = {
                    "passed": passed,
                    "threshold": threshold,
                    "actual": actual,
                    "difference": actual - threshold
                }
                
                if not passed:
                    self.threshold_breaches.append({
                        "metric": f"usage_{metric}",
                        "threshold": threshold,
                        "actual": actual,
                        "difference": actual - threshold
                    })
        
        return threshold_results
    
    def _should_fail_ci(self, threshold_results: Dict[str, Dict[str, Any]]) -> bool:
        """
        Determine if CI should fail based on threshold breaches.
        
        Args:
            threshold_results: Threshold comparison results
            
        Returns:
            True if CI should fail, False otherwise
        """
        if not self.ci_config.get("fail_on_threshold_breach", True):
            return False
        
        # Check if any thresholds were breached
        return len(self.threshold_breaches) > 0
    
    async def run_and_report(self):
        """Run evaluations, generate reports, and exit with appropriate code."""
        print("🔧 Running CI/CD Evaluation Pipeline")
        print(f"Fail on threshold breach: {self.ci_config.get('fail_on_threshold_breach', True)}")
        print(f"Fast fail: {self.ci_config.get('fail_fast', False)}\n")
        
        # Run evaluations with threshold checking
        results = await self.run_with_thresholds()
        
        # Generate reports
        print("\n📝 Generating reports...")
        report_formats = self.config.get("reporting", {}).get("format", ["json", "markdown"])
        generated_files = self.report_generator.generate_report(
            results,
            formats=report_formats,
            include_failures=True,
            include_examples=self.config.get("reporting", {}).get("include_examples", True)
        )
        
        # Print summary
        print("\n" + "="*60)
        print("CI/CD Evaluation Summary")
        print("="*60)
        print(f"Status: {results['ci_status'].upper()}")
        print(f"Pass Rate: {results['summary']['pass_rate']:.2f}%")
        print(f"Duration: {results['summary']['duration']:.2f}s")
        print(f"Total Tests: {results['summary']['total_tests']}")
        print(f"Passed: {results['summary']['passed']}")
        print(f"Failed: {results['summary']['failed']}")
        
        # Print threshold breaches
        if self.threshold_breaches:
            print(f"\n❌ Threshold Breaches ({len(self.threshold_breaches)}):")
            for breach in self.threshold_breaches:
                print(f"  - {breach['metric']}: {breach['actual']:.2f} (threshold: {breach['threshold']:.2f}, diff: {breach['difference']:.2f})")
        else:
            print("\n✅ All thresholds passed!")
        
        print(f"\n📄 Reports:")
        for format_type, file_path in generated_files.items():
            print(f"  - {format_type}: {file_path}")
        
        print("="*60)
        
        # Exit with appropriate code
        if results["ci_status"] == "failed":
            print("\n❌ CI/CD Pipeline FAILED")
            sys.exit(1)
        else:
            print("\n✅ CI/CD Pipeline PASSED")
            sys.exit(0)


async def main():
    """Main entry point for CI evaluation."""
    # Check if running in CI environment
    is_ci = os.getenv("CI", "false").lower() == "true"
    
    if is_ci:
        print("🤖 Detected CI environment")
    else:
        print("⚠️  Not running in CI environment (set CI=true to enable CI mode)")
    
    runner = CIEvaluationRunner()
    await runner.run_and_report()


if __name__ == "__main__":
    asyncio.run(main())
