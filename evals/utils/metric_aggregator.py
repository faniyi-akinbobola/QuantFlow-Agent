"""
Metric Aggregator Utility
Aggregates and computes statistics across evaluation metrics
"""

import statistics
from typing import List, Dict, Any, Optional


class MetricAggregator:
    """Aggregate and compute statistics for evaluation metrics."""
    
    def __init__(self):
        """Initialize metric aggregator."""
        self.metrics = {}
        
    def add_metric(self, name: str, value: float, metadata: Optional[Dict] = None):
        """
        Add a single metric value.
        
        Args:
            name: Metric name
            value: Metric value
            metadata: Optional metadata about this metric
        """
        if name not in self.metrics:
            self.metrics[name] = []
        
        entry = {"value": value}
        if metadata:
            entry["metadata"] = metadata
        
        self.metrics[name].append(entry)
    
    def add_metrics(self, metrics: Dict[str, float], metadata: Optional[Dict] = None):
        """
        Add multiple metrics at once.
        
        Args:
            metrics: Dictionary of metric name -> value
            metadata: Optional metadata for all metrics
        """
        for name, value in metrics.items():
            self.add_metric(name, value, metadata)
    
    def get_aggregated_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Get aggregated statistics for all metrics.
        
        Returns:
            Dictionary mapping metric names to their statistics
        """
        aggregated = {}
        
        for metric_name, values in self.metrics.items():
            # Extract just the values
            value_list = [entry["value"] for entry in values]
            
            if not value_list:
                continue
            
            aggregated[metric_name] = self._compute_statistics(value_list)
        
        return aggregated
    
    def _compute_statistics(self, values: List[float]) -> Dict[str, float]:
        """
        Compute comprehensive statistics for a list of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Dictionary of statistics
        """
        if not values:
            return {}
        
        sorted_values = sorted(values)
        
        stats = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "count": len(values),
        }
        
        # Add standard deviation if we have enough values
        if len(values) >= 2:
            stats["std"] = statistics.stdev(values)
        
        # Add percentiles
        stats["p25"] = self._percentile(sorted_values, 25)
        stats["p50"] = self._percentile(sorted_values, 50)
        stats["p75"] = self._percentile(sorted_values, 75)
        stats["p90"] = self._percentile(sorted_values, 90)
        stats["p95"] = self._percentile(sorted_values, 95)
        stats["p99"] = self._percentile(sorted_values, 99)
        
        return stats
    
    def _percentile(self, sorted_data: List[float], percent: float) -> float:
        """
        Calculate percentile from sorted data.
        
        Args:
            sorted_data: Sorted list of numbers
            percent: Percentile to calculate (0-100)
            
        Returns:
            Value at the given percentile
        """
        if not sorted_data:
            return 0.0
        
        k = (len(sorted_data) - 1) * (percent / 100)
        f = int(k)
        c = f + 1
        
        if c >= len(sorted_data):
            return sorted_data[-1]
        
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        
        return d0 + d1
    
    def get_metric_summary(self, metric_name: str) -> Optional[Dict[str, float]]:
        """
        Get summary statistics for a specific metric.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Dictionary of statistics or None if metric not found
        """
        if metric_name not in self.metrics:
            return None
        
        values = [entry["value"] for entry in self.metrics[metric_name]]
        return self._compute_statistics(values)
    
    def compare_to_threshold(self, thresholds: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """
        Compare metrics against thresholds.
        
        Args:
            thresholds: Dictionary of metric_name -> threshold_value
            
        Returns:
            Dictionary with comparison results
        """
        results = {}
        aggregated = self.get_aggregated_metrics()
        
        for metric_name, threshold in thresholds.items():
            if metric_name not in aggregated:
                results[metric_name] = {
                    "status": "missing",
                    "message": f"Metric {metric_name} not found"
                }
                continue
            
            mean_value = aggregated[metric_name]["mean"]
            passed = mean_value >= threshold
            
            results[metric_name] = {
                "status": "passed" if passed else "failed",
                "threshold": threshold,
                "actual": mean_value,
                "difference": mean_value - threshold,
                "passed": passed
            }
        
        return results
    
    def get_pass_rate(self, threshold: float = 0.5) -> float:
        """
        Calculate overall pass rate across all binary metrics.
        
        Args:
            threshold: Value above which a metric is considered passing (0-1)
            
        Returns:
            Overall pass rate as percentage (0-100)
        """
        aggregated = self.get_aggregated_metrics()
        
        if not aggregated:
            return 0.0
        
        total_passed = 0
        total_metrics = 0
        
        for metric_name, stats in aggregated.items():
            total_metrics += 1
            if stats["mean"] >= threshold * 100:  # Convert threshold to percentage
                total_passed += 1
        
        return (total_passed / total_metrics) * 100 if total_metrics > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export all metrics and aggregations as dictionary.
        
        Returns:
            Complete metrics data
        """
        return {
            "raw_metrics": self.metrics,
            "aggregated_metrics": self.get_aggregated_metrics(),
            "overall_pass_rate": self.get_pass_rate()
        }
    
    def reset(self):
        """Clear all stored metrics."""
        self.metrics = {}
    
    def merge(self, other: 'MetricAggregator'):
        """
        Merge metrics from another aggregator.
        
        Args:
            other: Another MetricAggregator instance
        """
        for metric_name, values in other.metrics.items():
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []
            self.metrics[metric_name].extend(values)
