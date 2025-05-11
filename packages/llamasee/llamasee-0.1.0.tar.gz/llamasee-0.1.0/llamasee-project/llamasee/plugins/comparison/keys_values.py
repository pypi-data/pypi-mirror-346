"""
Keys and Values comparison plugin for LlamaSee.

This plugin compares datasets by identifying key columns and value columns,
then comparing the values for matching keys.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
import logging
from .base import ComparisonPlugin

class KeysValuesComparisonPlugin(ComparisonPlugin):
    """
    Comparison plugin that compares datasets by keys and values.
    """
    
    def __init__(self):
        """Initialize the plugin."""
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.name = "KeysValuesComparisonPlugin"
        self.version = "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Configuration dictionary for the plugin
        """
        self.config = config
        self.logger.info(f"Initialized {self.name} with configuration")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for this plugin.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        # No specific validation needed for this plugin
        return True
    
    def get_name(self) -> str:
        """
        Get the name of the plugin.
        
        Returns:
            Plugin name
        """
        return self.name
    
    def get_description(self) -> str:
        """
        Get the description of the plugin.
        
        Returns:
            Plugin description
        """
        return "Compares datasets by identifying key columns and value columns, then comparing the values for matching keys."
    
    def get_version(self) -> str:
        """
        Get the version of the plugin.
        
        Returns:
            Plugin version
        """
        return self.version
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of the plugin.
        
        Returns:
            Dictionary of plugin capabilities
        """
        return {
            "comparison_types": self.get_comparison_types(),
            "comparison_metrics": self.get_comparison_metrics(),
            "supported_data_types": self.get_supported_data_types(),
            "supported_dimensions": self.get_supported_dimensions(),
            "supported_aggregations": self.get_supported_aggregations()
        }
    
    def compare(
        self, 
        data_a: pd.DataFrame, 
        data_b: pd.DataFrame, 
        keys: Optional[List[str]] = None,
        values: Optional[List[str]] = None,
        dimensions: Optional[List[str]] = None,
        aggregation_levels: Optional[Dict[str, str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compare two datasets and identify differences.
        
        Args:
            data_a: First dataset to compare
            data_b: Second dataset to compare
            keys: Optional list of key columns to use for comparison
            values: Optional list of value columns to compare
            dimensions: Optional list of dimensions to analyze
            aggregation_levels: Optional dictionary of dimension to aggregation level
            context: Optional context information for the comparison
            
        Returns:
            Dictionary containing comparison results
        """
        self.logger.info(f"Comparing datasets with {self.name}")
        
        # If keys and values are not provided, try to detect them
        if not keys or not values:
            detected_keys, detected_values = self._detect_keys_and_values(data_a, data_b)
            keys = keys or detected_keys
            values = values or detected_values
        
        # Ensure we have keys and values
        if not keys or not values:
            self.logger.warning("No keys or values provided for comparison")
            return {"error": "No keys or values provided for comparison"}
        
        # Compare by keys and values
        results = self._compare_by_keys_and_values(data_a, data_b, keys, values)
        
        # If dimensions are provided, analyze by dimensions
        if dimensions:
            dimension_results = self._analyze_by_dimensions(data_a, data_b, keys, values, dimensions, aggregation_levels)
            results["dimension_analysis"] = dimension_results
        
        return results
    
    def _detect_keys_and_values(self, data_a: pd.DataFrame, data_b: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """
        Detect potential keys and values in the datasets.
        
        Args:
            data_a: First dataset
            data_b: Second dataset
            
        Returns:
            Tuple of (keys, values)
        """
        # Simple detection based on cardinality
        all_columns = set(data_a.columns) & set(data_b.columns)
        
        keys = []
        values = []
        
        for col in all_columns:
            # Check if column exists in both datasets
            if col not in data_a.columns or col not in data_b.columns:
                continue
            
            # Calculate cardinality (number of unique values)
            cardinality_a = data_a[col].nunique()
            cardinality_b = data_b[col].nunique()
            
            # Calculate total rows
            total_rows_a = len(data_a)
            total_rows_b = len(data_b)
            
            # Calculate cardinality ratio
            ratio_a = cardinality_a / total_rows_a if total_rows_a > 0 else 0
            ratio_b = cardinality_b / total_rows_b if total_rows_b > 0 else 0
            
            # If cardinality ratio is high, consider it a key
            if ratio_a > 0.8 or ratio_b > 0.8:
                keys.append(col)
            else:
                # Check if it's a numeric column
                if pd.api.types.is_numeric_dtype(data_a[col]) and pd.api.types.is_numeric_dtype(data_b[col]):
                    values.append(col)
                else:
                    # For non-numeric columns, check if they have a reasonable number of unique values
                    if cardinality_a < 20 and cardinality_b < 20:
                        values.append(col)
        
        return keys, values
    
    def _compare_by_keys_and_values(
        self, 
        data_a: pd.DataFrame, 
        data_b: pd.DataFrame, 
        keys: List[str], 
        values: List[str]
    ) -> Dict[str, Any]:
        """
        Compare datasets by keys and values.
        
        Args:
            data_a: First dataset
            data_b: Second dataset
            keys: List of key columns
            values: List of value columns
            
        Returns:
            Dictionary of comparison results
        """
        results = {
            "keys": keys,
            "values": values,
            "key_differences": {},
            "value_differences": {},
            "summary": {}
        }
        
        # Check for key differences
        for key in keys:
            if key not in data_a.columns or key not in data_b.columns:
                results["key_differences"][key] = {
                    "error": f"Key '{key}' not found in both datasets"
                }
                continue
            
            # Get unique values for this key in both datasets
            unique_a = set(data_a[key].unique())
            unique_b = set(data_b[key].unique())
            
            # Find differences
            only_in_a = unique_a - unique_b
            only_in_b = unique_b - unique_a
            common = unique_a & unique_b
            
            results["key_differences"][key] = {
                "only_in_a": list(only_in_a),
                "only_in_b": list(only_in_b),
                "common": list(common),
                "count_only_in_a": len(only_in_a),
                "count_only_in_b": len(only_in_b),
                "count_common": len(common)
            }
        
        # Compare values for common keys
        for value in values:
            if value not in data_a.columns or value not in data_b.columns:
                results["value_differences"][value] = {
                    "error": f"Value '{value}' not found in both datasets"
                }
                continue
            
            # Get common keys
            common_keys = {}
            for key in keys:
                if key in data_a.columns and key in data_b.columns:
                    common_keys[key] = list(set(data_a[key].unique()) & set(data_b[key].unique()))
            
            # Compare values for each key
            value_results = {}
            for key, key_values in common_keys.items():
                key_results = []
                
                for key_value in key_values:
                    # Get rows with this key value
                    rows_a = data_a[data_a[key] == key_value]
                    rows_b = data_b[data_b[key] == key_value]
                    
                    # Skip if no rows found
                    if len(rows_a) == 0 or len(rows_b) == 0:
                        continue
                    
                    # Get values
                    value_a = rows_a[value].iloc[0]
                    value_b = rows_b[value].iloc[0]
                    
                    # Skip if both values are NaN
                    if pd.isna(value_a) and pd.isna(value_b):
                        continue
                    
                    # Calculate difference
                    if pd.api.types.is_numeric_dtype(data_a[value]) and pd.api.types.is_numeric_dtype(data_b[value]):
                        # For numeric values, calculate absolute and percentage difference
                        if not pd.isna(value_a) and not pd.isna(value_b):
                            abs_diff = value_b - value_a
                            pct_diff = (abs_diff / value_a) * 100 if value_a != 0 else float('inf')
                            
                            key_results.append({
                                "key_value": key_value,
                                "value_a": value_a,
                                "value_b": value_b,
                                "abs_diff": abs_diff,
                                "pct_diff": pct_diff,
                                "is_significant": abs(pct_diff) > 10  # 10% threshold
                            })
                    else:
                        # For non-numeric values, just check if they're different
                        if value_a != value_b:
                            key_results.append({
                                "key_value": key_value,
                                "value_a": value_a,
                                "value_b": value_b,
                                "is_different": True
                            })
                
                value_results[key] = key_results
            
            results["value_differences"][value] = value_results
        
        # Generate summary
        summary = {
            "total_keys": len(keys),
            "total_values": len(values),
            "key_differences_count": sum(1 for k, v in results["key_differences"].items() if "error" not in v and (v["count_only_in_a"] > 0 or v["count_only_in_b"] > 0)),
            "value_differences_count": sum(1 for v, vr in results["value_differences"].items() if "error" not in vr and any(len(kr) > 0 for kr in vr.values())),
            "significant_differences": []
        }
        
        # Find significant differences
        for value, value_results in results["value_differences"].items():
            if "error" in value_results:
                continue
                
            for key, key_results in value_results.items():
                for result in key_results:
                    if "is_significant" in result and result["is_significant"]:
                        summary["significant_differences"].append({
                            "key": key,
                            "key_value": result["key_value"],
                            "value": value,
                            "value_a": result["value_a"],
                            "value_b": result["value_b"],
                            "pct_diff": result["pct_diff"]
                        })
        
        results["summary"] = summary
        
        return results
    
    def _analyze_by_dimensions(
        self, 
        data_a: pd.DataFrame, 
        data_b: pd.DataFrame, 
        keys: List[str], 
        values: List[str],
        dimensions: List[str],
        aggregation_levels: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze differences by dimensions.
        
        Args:
            data_a: First dataset
            data_b: Second dataset
            keys: List of key columns
            values: List of value columns
            dimensions: List of dimensions to analyze
            aggregation_levels: Optional dictionary of dimension to aggregation level
            
        Returns:
            Dictionary of dimension analysis results
        """
        results = {}
        
        for dimension in dimensions:
            if dimension not in data_a.columns or dimension not in data_b.columns:
                results[dimension] = {
                    "error": f"Dimension '{dimension}' not found in both datasets"
                }
                continue
            
            # Get aggregation level for this dimension
            agg_level = aggregation_levels.get(dimension) if aggregation_levels else None
            
            # Analyze by dimension
            dimension_results = self._analyze_dimension(
                data_a, data_b, keys, values, dimension, agg_level
            )
            
            results[dimension] = dimension_results
        
        return results
    
    def _analyze_dimension(
        self, 
        data_a: pd.DataFrame, 
        data_b: pd.DataFrame, 
        keys: List[str], 
        values: List[str],
        dimension: str,
        aggregation_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a specific dimension.
        
        Args:
            data_a: First dataset
            data_b: Second dataset
            keys: List of key columns
            values: List of value columns
            dimension: Dimension to analyze
            aggregation_level: Optional aggregation level
            
        Returns:
            Dictionary of dimension analysis results
        """
        results = {
            "dimension": dimension,
            "aggregation_level": aggregation_level,
            "unique_values": {
                "a": list(data_a[dimension].unique()),
                "b": list(data_b[dimension].unique())
            },
            "value_differences": {}
        }
        
        # Get unique values for this dimension
        unique_values_a = data_a[dimension].unique()
        unique_values_b = data_b[dimension].unique()
        
        # Find common values
        common_values = list(set(unique_values_a) & set(unique_values_b))
        
        # Analyze each value
        for value in values:
            if value not in data_a.columns or value not in data_b.columns:
                results["value_differences"][value] = {
                    "error": f"Value '{value}' not found in both datasets"
                }
                continue
            
            # Skip if not numeric
            if not pd.api.types.is_numeric_dtype(data_a[value]) or not pd.api.types.is_numeric_dtype(data_b[value]):
                continue
            
            # Analyze by dimension value
            value_results = []
            
            for dim_value in common_values:
                # Get rows with this dimension value
                rows_a = data_a[data_a[dimension] == dim_value]
                rows_b = data_b[data_b[dimension] == dim_value]
                
                # Skip if no rows found
                if len(rows_a) == 0 or len(rows_b) == 0:
                    continue
                
                # Aggregate if needed
                if aggregation_level:
                    if aggregation_level == "sum":
                        value_a = rows_a[value].sum()
                        value_b = rows_b[value].sum()
                    elif aggregation_level == "mean":
                        value_a = rows_a[value].mean()
                        value_b = rows_b[value].mean()
                    elif aggregation_level == "median":
                        value_a = rows_a[value].median()
                        value_b = rows_b[value].median()
                    elif aggregation_level == "min":
                        value_a = rows_a[value].min()
                        value_b = rows_b[value].min()
                    elif aggregation_level == "max":
                        value_a = rows_a[value].max()
                        value_b = rows_b[value].max()
                    else:
                        # Default to mean
                        value_a = rows_a[value].mean()
                        value_b = rows_b[value].mean()
                else:
                    # Default to mean
                    value_a = rows_a[value].mean()
                    value_b = rows_b[value].mean()
                
                # Skip if both values are NaN
                if pd.isna(value_a) and pd.isna(value_b):
                    continue
                
                # Calculate difference
                if not pd.isna(value_a) and not pd.isna(value_b):
                    abs_diff = value_b - value_a
                    pct_diff = (abs_diff / value_a) * 100 if value_a != 0 else float('inf')
                    
                    value_results.append({
                        "dimension_value": dim_value,
                        "value_a": value_a,
                        "value_b": value_b,
                        "abs_diff": abs_diff,
                        "pct_diff": pct_diff,
                        "is_significant": abs(pct_diff) > 10  # 10% threshold
                    })
            
            results["value_differences"][value] = value_results
        
        return results
    
    def get_comparison_types(self) -> List[str]:
        """
        Get the types of comparisons supported by this plugin.
        
        Returns:
            List of supported comparison types
        """
        return ["keys_values", "dimension"]
    
    def get_comparison_metrics(self) -> List[str]:
        """
        Get the metrics used for comparison by this plugin.
        
        Returns:
            List of comparison metrics
        """
        return ["absolute_difference", "percentage_difference", "key_differences", "value_differences"]
    
    def get_supported_data_types(self) -> List[str]:
        """
        Get the data types supported by this plugin.
        
        Returns:
            List of supported data types
        """
        return ["numeric", "categorical", "datetime"]
    
    def get_supported_dimensions(self) -> List[str]:
        """
        Get the dimensions supported by this plugin.
        
        Returns:
            List of supported dimensions
        """
        return ["time", "location", "product", "category", "metric"]
    
    def get_supported_aggregations(self) -> Dict[str, List[str]]:
        """
        Get the aggregation methods supported by this plugin.
        
        Returns:
            Dictionary mapping dimensions to supported aggregation methods
        """
        return {
            "time": ["sum", "mean", "median", "min", "max"],
            "location": ["sum", "mean", "median", "min", "max"],
            "product": ["sum", "mean", "median", "min", "max"],
            "category": ["sum", "mean", "median", "min", "max"],
            "metric": ["sum", "mean", "median", "min", "max"]
        } 