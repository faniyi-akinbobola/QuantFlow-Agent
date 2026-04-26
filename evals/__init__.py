"""
QuantFlow Agent Evaluation Framework

A comprehensive evaluation suite for testing stock market AI agent performance.

Usage:
    # Run local evaluation
    python evals/runners/run_local.py
    
    # Run CI/CD evaluation
    python evals/runners/run_ci.py

Components:
    - datasets: Test cases for different scenarios
    - evaluators: LLM-based and deterministic evaluators
    - metrics: Cost, latency, and usage metrics
    - utils: Dataset loading, metric aggregation, report generation
    - runners: Local and CI/CD execution
"""

__version__ = "1.0.0"
__author__ = "QuantFlow Team"

from .utils.dataset_loader import DatasetLoader
from .utils.metric_aggregator import MetricAggregator
from .utils.report_generator import ReportGenerator

__all__ = [
    "DatasetLoader",
    "MetricAggregator",
    "ReportGenerator",
]
