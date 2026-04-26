"""
Report Generator Utility
Generates evaluation reports in multiple formats (JSON, HTML, Markdown)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class ReportGenerator:
    """Generate comprehensive evaluation reports."""
    
    def __init__(self, output_dir: str = "evals/reports"):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_report(
        self,
        results: Dict[str, Any],
        formats: List[str] = ["json", "markdown"],
        include_failures: bool = True,
        include_examples: bool = True
    ) -> Dict[str, Path]:
        """
        Generate evaluation report in multiple formats.
        
        Args:
            results: Evaluation results dictionary
            formats: List of output formats ('json', 'markdown', 'html')
            include_failures: Include failed test examples
            include_examples: Include example outputs
            
        Returns:
            Dictionary mapping format to file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_files = {}
        
        for format_type in formats:
            if format_type == "json":
                file_path = self._generate_json(results, timestamp)
            elif format_type == "markdown":
                file_path = self._generate_markdown(results, timestamp, include_failures, include_examples)
            elif format_type == "html":
                file_path = self._generate_html(results, timestamp, include_failures, include_examples)
            else:
                print(f"Unknown format: {format_type}")
                continue
            
            generated_files[format_type] = file_path
        
        return generated_files
    
    def _generate_json(self, results: Dict[str, Any], timestamp: str) -> Path:
        """Generate JSON report."""
        file_path = self.output_dir / f"eval_report_{timestamp}.json"
        
        def json_serializer(obj):
            """Custom JSON serializer for non-serializable objects."""
            # Handle LangChain message objects
            if hasattr(obj, 'content'):
                return str(obj.content)
            # Handle other objects
            return str(obj)
        
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2, default=json_serializer)
        
        print(f"✅ JSON report saved: {file_path}")
        return file_path
    
    def _generate_markdown(
        self, 
        results: Dict[str, Any], 
        timestamp: str,
        include_failures: bool,
        include_examples: bool
    ) -> Path:
        """Generate Markdown report."""
        file_path = self.output_dir / f"eval_report_{timestamp}.md"
        
        md = []
        md.append("# QuantFlow Agent - Evaluation Report\n")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")
        
        # Summary Section
        md.append("## 📊 Summary\n")
        summary = results.get("summary", {})
        md.append(f"- **Total Tests:** {summary.get('total_tests', 0)}")
        md.append(f"- **Passed:** {summary.get('passed', 0)}")
        md.append(f"- **Failed:** {summary.get('failed', 0)}")
        md.append(f"- **Pass Rate:** {summary.get('pass_rate', 0):.2f}%")
        md.append(f"- **Total Duration:** {summary.get('duration', 0):.2f}s")
        md.append(f"- **Total Cost:** ${summary.get('total_cost', 0):.4f}\n")
        
        # Metrics Section
        md.append("## 📈 Metrics\n")
        metrics = results.get("metrics", {})
        
        for metric_name, metric_stats in metrics.items():
            md.append(f"### {metric_name}\n")
            md.append(f"- Mean: {metric_stats.get('mean', 0):.2f}")
            md.append(f"- Median: {metric_stats.get('median', 0):.2f}")
            md.append(f"- Min: {metric_stats.get('min', 0):.2f}")
            md.append(f"- Max: {metric_stats.get('max', 0):.2f}")
            md.append(f"- P95: {metric_stats.get('p95', 0):.2f}\n")
        
        # Dataset Results
        md.append("## 📋 Dataset Results\n")
        datasets = results.get("datasets", {})
        
        for dataset_name, dataset_results in datasets.items():
            md.append(f"### {dataset_name}\n")
            md.append(f"- **Tests:** {dataset_results.get('total', 0)}")
            md.append(f"- **Passed:** {dataset_results.get('passed', 0)}")
            md.append(f"- **Pass Rate:** {dataset_results.get('pass_rate', 0):.2f}%\n")
            
            # Evaluator scores
            evaluator_scores = dataset_results.get("evaluator_scores", {})
            if evaluator_scores:
                md.append("**Evaluator Scores:**\n")
                for evaluator, score in evaluator_scores.items():
                    md.append(f"- {evaluator}: {score:.2f}%")
                md.append("")
        
        # Failures Section
        if include_failures:
            md.append("## ❌ Failures\n")
            failures = results.get("failures", [])
            
            if failures:
                for failure in failures[:10]:  # Limit to first 10
                    md.append(f"### {failure.get('id', 'Unknown')}\n")
                    md.append(f"**Question:** {failure.get('question', 'N/A')}\n")
                    md.append(f"**Reason:** {failure.get('reason', 'N/A')}\n")
                    md.append("---\n")
            else:
                md.append("No failures! 🎉\n")
        
        # Threshold Comparison
        md.append("## 🎯 Threshold Comparison\n")
        threshold_results = results.get("threshold_comparison", {})
        
        for metric, comparison in threshold_results.items():
            status_emoji = "✅" if comparison.get("passed") else "❌"
            md.append(f"- {status_emoji} **{metric}**: {comparison.get('actual', 0):.2f} (threshold: {comparison.get('threshold', 0):.2f})")
        md.append("")
        
        # Write to file
        with open(file_path, 'w') as f:
            f.write('\n'.join(md))
        
        print(f"✅ Markdown report saved: {file_path}")
        return file_path
    
    def _generate_html(
        self, 
        results: Dict[str, Any], 
        timestamp: str,
        include_failures: bool,
        include_examples: bool
    ) -> Path:
        """Generate HTML report."""
        file_path = self.output_dir / f"eval_report_{timestamp}.html"
        
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("<title>QuantFlow Agent - Evaluation Report</title>")
        html.append("<style>")
        html.append(self._get_html_styles())
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        
        html.append("<div class='container'>")
        html.append("<h1>📊 QuantFlow Agent - Evaluation Report</h1>")
        html.append(f"<p class='timestamp'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # Summary Cards
        summary = results.get("summary", {})
        html.append("<div class='summary-cards'>")
        html.append(f"<div class='card'><h3>{summary.get('total_tests', 0)}</h3><p>Total Tests</p></div>")
        html.append(f"<div class='card success'><h3>{summary.get('passed', 0)}</h3><p>Passed</p></div>")
        html.append(f"<div class='card error'><h3>{summary.get('failed', 0)}</h3><p>Failed</p></div>")
        html.append(f"<div class='card'><h3>{summary.get('pass_rate', 0):.1f}%</h3><p>Pass Rate</p></div>")
        html.append("</div>")
        
        # Metrics Table
        html.append("<h2>Metrics</h2>")
        html.append("<table>")
        html.append("<tr><th>Metric</th><th>Mean</th><th>Median</th><th>Min</th><th>Max</th><th>P95</th></tr>")
        
        for metric_name, stats in results.get("metrics", {}).items():
            html.append(f"<tr>")
            html.append(f"<td><strong>{metric_name}</strong></td>")
            html.append(f"<td>{stats.get('mean', 0):.2f}</td>")
            html.append(f"<td>{stats.get('median', 0):.2f}</td>")
            html.append(f"<td>{stats.get('min', 0):.2f}</td>")
            html.append(f"<td>{stats.get('max', 0):.2f}</td>")
            html.append(f"<td>{stats.get('p95', 0):.2f}</td>")
            html.append(f"</tr>")
        
        html.append("</table>")
        
        # Dataset Results
        html.append("<h2>Dataset Results</h2>")
        for dataset_name, dataset_results in results.get("datasets", {}).items():
            pass_rate = dataset_results.get('pass_rate', 0)
            status_class = 'success' if pass_rate >= 80 else 'warning' if pass_rate >= 60 else 'error'
            
            html.append(f"<div class='dataset-card {status_class}'>")
            html.append(f"<h3>{dataset_name}</h3>")
            html.append(f"<p>Pass Rate: <strong>{pass_rate:.1f}%</strong> ({dataset_results.get('passed', 0)}/{dataset_results.get('total', 0)})</p>")
            html.append("</div>")
        
        html.append("</div>")  # Close container
        html.append("</body>")
        html.append("</html>")
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(html))
        
        print(f"✅ HTML report saved: {file_path}")
        return file_path
    
    def _get_html_styles(self) -> str:
        """Get CSS styles for HTML report."""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { color: #333; margin-bottom: 10px; }
        h2 { color: #555; margin-top: 40px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        h3 { color: #666; }
        .timestamp { color: #888; font-size: 14px; }
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        .card h3 { margin: 0; font-size: 36px; color: #333; }
        .card p { margin: 10px 0 0; color: #666; }
        .card.success { border-color: #4caf50; }
        .card.success h3 { color: #4caf50; }
        .card.error { border-color: #f44336; }
        .card.error h3 { color: #f44336; }
        .card.warning { border-color: #ff9800; }
        .card.warning h3 { color: #ff9800; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
            color: #333;
        }
        tr:hover { background: #f9f9f9; }
        .dataset-card {
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
        }
        .dataset-card.success { border-left-color: #4caf50; background: #f1f8f4; }
        .dataset-card.warning { border-left-color: #ff9800; background: #fff8f0; }
        .dataset-card.error { border-left-color: #f44336; background: #fef1f0; }
        """
    
    def generate_comparison_report(
        self,
        results_list: List[Dict[str, Any]],
        labels: List[str]
    ) -> Path:
        """
        Generate a comparison report across multiple evaluation runs.
        
        Args:
            results_list: List of evaluation results
            labels: Labels for each result set
            
        Returns:
            Path to generated comparison report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.output_dir / f"comparison_report_{timestamp}.md"
        
        md = []
        md.append("# Evaluation Comparison Report\n")
        md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append("---\n")
        
        # Summary comparison table
        md.append("## Summary Comparison\n")
        md.append("| Metric | " + " | ".join(labels) + " |")
        md.append("|--------|" + "|".join(["--------"] * len(labels)) + "|")
        
        # Pass rate row
        pass_rates = [f"{r.get('summary', {}).get('pass_rate', 0):.2f}%" for r in results_list]
        md.append("| Pass Rate | " + " | ".join(pass_rates) + " |")
        
        # Cost row
        costs = [f"${r.get('summary', {}).get('total_cost', 0):.4f}" for r in results_list]
        md.append("| Total Cost | " + " | ".join(costs) + " |")
        
        # Duration row
        durations = [f"{r.get('summary', {}).get('duration', 0):.2f}s" for r in results_list]
        md.append("| Duration | " + " | ".join(durations) + " |\n")
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(md))
        
        print(f"✅ Comparison report saved: {file_path}")
        return file_path
