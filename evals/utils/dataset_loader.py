"""
Dataset Loader Utility
Handles loading and preprocessing of evaluation datasets
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional


class DatasetLoader:
    """Load and manage evaluation datasets."""
    
    def __init__(self, base_path: str = "evals/dataset"):
        """
        Initialize dataset loader.
        
        Args:
            base_path: Base directory containing dataset files
        """
        self.base_path = Path(base_path)
        
    def load_dataset(self, dataset_name: str) -> List[Dict[str, Any]]:
        """
        Load a dataset by name.
        
        Args:
            dataset_name: Name of the dataset (e.g., 'rag_queries', 'tool_usage_cases')
            
        Returns:
            List of examples from the dataset
        """
        file_path = self.base_path / f"{dataset_name}.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    def load_multiple_datasets(self, dataset_names: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load multiple datasets.
        
        Args:
            dataset_names: List of dataset names to load
            
        Returns:
            Dictionary mapping dataset names to their data
        """
        datasets = {}
        for name in dataset_names:
            datasets[name] = self.load_dataset(name)
        return datasets
    
    def load_all_datasets(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all available datasets.
        
        Returns:
            Dictionary mapping dataset names to their data
        """
        dataset_files = self.base_path.glob("*.json")
        datasets = {}
        
        for file_path in dataset_files:
            dataset_name = file_path.stem
            datasets[dataset_name] = self.load_dataset(dataset_name)
        
        return datasets
    
    def sample_dataset(
        self, 
        dataset: List[Dict[str, Any]], 
        size: int, 
        strategy: str = "random",
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Sample a subset of the dataset.
        
        Args:
            dataset: Full dataset to sample from
            size: Number of samples to return
            strategy: Sampling strategy ('random', 'stratified', 'balanced')
            seed: Random seed for reproducibility
            
        Returns:
            Sampled subset of the dataset
        """
        if seed is not None:
            random.seed(seed)
        
        if size >= len(dataset):
            return dataset
        
        if strategy == "random":
            return random.sample(dataset, size)
        
        elif strategy == "stratified":
            # Sample proportionally from each category
            return self._stratified_sample(dataset, size)
        
        elif strategy == "balanced":
            # Equal samples from each category
            return self._balanced_sample(dataset, size)
        
        else:
            raise ValueError(f"Unknown sampling strategy: {strategy}")
    
    def _stratified_sample(self, dataset: List[Dict[str, Any]], size: int) -> List[Dict[str, Any]]:
        """Stratified sampling based on category field."""
        # Group by category
        categories = {}
        for item in dataset:
            category = item.get("category", "default")
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Calculate samples per category
        samples = []
        total = len(dataset)
        
        for category, items in categories.items():
            proportion = len(items) / total
            category_size = max(1, int(size * proportion))
            category_samples = random.sample(items, min(category_size, len(items)))
            samples.extend(category_samples)
        
        # If we need more samples, add randomly
        if len(samples) < size:
            remaining = [item for item in dataset if item not in samples]
            additional = random.sample(remaining, min(size - len(samples), len(remaining)))
            samples.extend(additional)
        
        return samples[:size]
    
    def _balanced_sample(self, dataset: List[Dict[str, Any]], size: int) -> List[Dict[str, Any]]:
        """Balanced sampling - equal from each category."""
        # Group by category
        categories = {}
        for item in dataset:
            category = item.get("category", "default")
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Equal samples from each category
        samples = []
        per_category = size // len(categories)
        
        for category, items in categories.items():
            category_samples = random.sample(items, min(per_category, len(items)))
            samples.extend(category_samples)
        
        # Fill remaining if needed
        if len(samples) < size:
            remaining = [item for item in dataset if item not in samples]
            additional = random.sample(remaining, min(size - len(samples), len(remaining)))
            samples.extend(additional)
        
        return samples[:size]
    
    def filter_dataset(
        self, 
        dataset: List[Dict[str, Any]], 
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Filter dataset based on criteria.
        
        Args:
            dataset: Dataset to filter
            filters: Dictionary of field: value pairs to filter by
            
        Returns:
            Filtered dataset
        """
        filtered = dataset
        
        for field, value in filters.items():
            if isinstance(value, list):
                # Filter by multiple values
                filtered = [item for item in filtered if item.get(field) in value]
            else:
                # Filter by single value
                filtered = [item for item in filtered if item.get(field) == value]
        
        return filtered
    
    def get_dataset_stats(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about a dataset.
        
        Args:
            dataset: Dataset to analyze
            
        Returns:
            Dictionary of statistics
        """
        if not dataset:
            return {"total": 0}
        
        stats = {
            "total": len(dataset),
            "fields": set(),
            "categories": {},
        }
        
        for item in dataset:
            # Track all fields
            stats["fields"].update(item.keys())
            
            # Count categories
            category = item.get("category", "uncategorized")
            stats["categories"][category] = stats["categories"].get(category, 0) + 1
        
        stats["fields"] = list(stats["fields"])
        
        return stats
    
    def validate_dataset(self, dataset: List[Dict[str, Any]], required_fields: List[str]) -> bool:
        """
        Validate that dataset has required fields.
        
        Args:
            dataset: Dataset to validate
            required_fields: List of required field names
            
        Returns:
            True if valid, False otherwise
        """
        for item in dataset:
            for field in required_fields:
                if field not in item:
                    print(f"Missing required field '{field}' in item: {item.get('id', 'unknown')}")
                    return False
        
        return True
