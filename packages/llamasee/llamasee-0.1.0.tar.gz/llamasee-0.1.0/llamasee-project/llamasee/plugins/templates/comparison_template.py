"""
Comparison plugin template for LlamaSee.

This module provides a template for creating new comparison plugins.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from ..comparison.base import ComparisonPlugin

class ComparisonPluginTemplate(ComparisonPlugin):
    """
    Template for creating new comparison plugins.
    
    To create a new comparison plugin:
    1. Copy this template to a new file
    2. Rename the class to your plugin name
    3. Implement all required methods
    4. Add your comparison-specific functionality
    """
    
    def __init__(self):
        """Initialize the comparison plugin."""
        super().__init__()
        self.name = "ComparisonPluginTemplate"
        self.description = "Template for creating new comparison plugins"
        self.version = "0.1.0"
        self.config = {}
        self.enabled = False
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Configuration dictionary for the plugin
        """
        self.config = config
        self.enabled = True
    
    def compare(self, dataset1: pd.DataFrame, dataset2: pd.DataFrame, keys: List[str], values: List[str], dimensions: Optional[List[str]] = None, aggregation_level: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Compare two datasets and identify differences.
        
        Args:
            dataset1: First dataset to compare
            dataset2: Second dataset to compare
            keys: List of key columns to match records
            values: List of value columns to compare
            dimensions: Optional list of dimension columns for analysis
            aggregation_level: Optional aggregation level for analysis
            context: Optional context information for comparison
            
        Returns:
            Dictionary containing comparison results
        """
        try:
            # Validate inputs
            if not all(key in dataset1.columns for key in keys):
                raise ValueError(f"Missing key columns in dataset1: {[key for key in keys if key not in dataset1.columns]}")
            if not all(key in dataset2.columns for key in keys):
                raise ValueError(f"Missing key columns in dataset2: {[key for key in keys if key not in dataset2.columns]}")
            if not all(value in dataset1.columns for value in values):
                raise ValueError(f"Missing value columns in dataset1: {[value for value in values if value not in dataset1.columns]}")
            if not all(value in dataset2.columns for value in values):
                raise ValueError(f"Missing value columns in dataset2: {[value for value in values if value not in dataset2.columns]}")
            if dimensions and not all(dim in dataset1.columns for dim in dimensions):
                raise ValueError(f"Missing dimension columns in dataset1: {[dim for dim in dimensions if dim not in dataset1.columns]}")
            if dimensions and not all(dim in dataset2.columns for dim in dimensions):
                raise ValueError(f"Missing dimension columns in dataset2: {[dim for dim in dimensions if dim not in dataset2.columns]}")
            
            # Perform comparison
            results = {
                "key_differences": self._compare_keys(dataset1, dataset2, keys),
                "value_differences": self._compare_values(dataset1, dataset2, keys, values)
            }
            
            # Add dimension analysis if requested
            if dimensions:
                results["dimension_analysis"] = self._analyze_dimensions(dataset1, dataset2, keys, values, dimensions, aggregation_level)
            
            # Add metadata
            results["metadata"] = {
                "dataset1_rows": len(dataset1),
                "dataset2_rows": len(dataset2),
                "keys": keys,
                "values": values,
                "dimensions": dimensions,
                "aggregation_level": aggregation_level,
                "context": context
            }
            
            return results
        
        except Exception as e:
            return {
                "error": str(e),
                "metadata": {
                    "dataset1_rows": len(dataset1),
                    "dataset2_rows": len(dataset2),
                    "keys": keys,
                    "values": values,
                    "dimensions": dimensions,
                    "aggregation_level": aggregation_level,
                    "context": context
                }
            }
    
    def _compare_keys(self, dataset1: pd.DataFrame, dataset2: pd.DataFrame, keys: List[str]) -> Dict[str, Any]:
        """
        Compare key columns between datasets.
        
        Args:
            dataset1: First dataset
            dataset2: Second dataset
            keys: List of key columns
            
        Returns:
            Dictionary containing key comparison results
        """
        # Get unique keys from both datasets
        keys1 = set(map(tuple, dataset1[keys].values))
        keys2 = set(map(tuple, dataset2[keys].values))
        
        return {
            "only_in_dataset1": list(keys1 - keys2),
            "only_in_dataset2": list(keys2 - keys1),
            "common_keys": list(keys1 & keys2)
        }
    
    def _compare_values(self, dataset1: pd.DataFrame, dataset2: pd.DataFrame, keys: List[str], values: List[str]) -> Dict[str, Any]:
        """
        Compare value columns between datasets.
        
        Args:
            dataset1: First dataset
            dataset2: Second dataset
            keys: List of key columns
            values: List of value columns
            
        Returns:
            Dictionary containing value comparison results
        """
        # Merge datasets on keys
        merged = pd.merge(dataset1, dataset2, on=keys, suffixes=('_1', '_2'))
        
        differences = {}
        for value in values:
            value1 = f"{value}_1"
            value2 = f"{value}_2"
            
            # Calculate differences
            differences[value] = {
                "mean_difference": (merged[value2] - merged[value1]).mean(),
                "std_difference": (merged[value2] - merged[value1]).std(),
                "min_difference": (merged[value2] - merged[value1]).min(),
                "max_difference": (merged[value2] - merged[value1]).max(),
                "total_difference": (merged[value2] - merged[value1]).sum()
            }
        
        return differences
    
    def _analyze_dimensions(self, dataset1: pd.DataFrame, dataset2: pd.DataFrame, keys: List[str], values: List[str], dimensions: List[str], aggregation_level: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze differences by dimensions.
        
        Args:
            dataset1: First dataset
            dataset2: Second dataset
            keys: List of key columns
            values: List of value columns
            dimensions: List of dimension columns
            aggregation_level: Optional aggregation level
            
        Returns:
            Dictionary containing dimension analysis results
        """
        # Merge datasets on keys
        merged = pd.merge(dataset1, dataset2, on=keys, suffixes=('_1', '_2'))
        
        analysis = {}
        for dimension in dimensions:
            dimension_analysis = {}
            
            # Group by dimension
            grouped = merged.groupby(dimension)
            
            for value in values:
                value1 = f"{value}_1"
                value2 = f"{value}_2"
                
                # Calculate statistics by dimension
                dimension_analysis[value] = {
                    "mean_difference": grouped.apply(lambda x: (x[value2] - x[value1]).mean()).to_dict(),
                    "total_difference": grouped.apply(lambda x: (x[value2] - x[value1]).sum()).to_dict()
                }
            
            analysis[dimension] = dimension_analysis
        
        return analysis
    
    def get_comparison_types(self) -> List[str]:
        """
        Get supported comparison types.
        
        Returns:
            List of supported comparison types
        """
        return ["key_comparison", "value_comparison", "dimension_analysis"]
    
    def get_comparison_metrics(self) -> List[str]:
        """
        Get supported comparison metrics.
        
        Returns:
            List of supported comparison metrics
        """
        return ["mean_difference", "std_difference", "min_difference", "max_difference", "total_difference"]
    
    def get_supported_data_types(self) -> List[str]:
        """
        Get supported data types.
        
        Returns:
            List of supported data types
        """
        return ["numeric", "categorical", "temporal"]
    
    def get_supported_dimensions(self) -> List[str]:
        """
        Get supported dimensions.
        
        Returns:
            List of supported dimensions
        """
        return ["time", "location", "product", "category", "metric"]
    
    def get_supported_aggregations(self) -> Dict[str, List[str]]:
        """
        Get supported aggregation methods for each dimension.
        
        Returns:
            Dictionary mapping dimensions to supported aggregation methods
        """
        return {
            "time": ["day", "week", "month", "quarter", "year"],
            "location": ["city", "state", "country", "region"],
            "product": ["category", "subcategory", "brand"],
            "category": ["level1", "level2", "level3"],
            "metric": ["sum", "mean", "median", "min", "max"]
        } 