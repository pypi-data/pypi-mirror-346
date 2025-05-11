"""
Base comparison plugin interface for LlamaSee.

This module defines the base interface that all comparison plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple
import pandas as pd
import logging
from ...plugins.base import BasePlugin

class ComparisonPlugin(BasePlugin):
    """
    Base interface for all LlamaSee comparison plugins.
    
    All comparison plugins must implement this interface to ensure
    consistent interaction with the LlamaSee comparison system.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def get_comparison_types(self) -> List[str]:
        """
        Get the types of comparisons supported by this plugin.
        
        Returns:
            List of supported comparison types
        """
        pass
    
    @abstractmethod
    def get_comparison_metrics(self) -> List[str]:
        """
        Get the metrics used for comparison by this plugin.
        
        Returns:
            List of comparison metrics
        """
        pass
    
    @abstractmethod
    def get_supported_data_types(self) -> List[str]:
        """
        Get the data types supported by this plugin.
        
        Returns:
            List of supported data types
        """
        pass
    
    @abstractmethod
    def get_supported_dimensions(self) -> List[str]:
        """
        Get the dimensions supported by this plugin.
        
        Returns:
            List of supported dimensions
        """
        pass
    
    @abstractmethod
    def get_supported_aggregations(self) -> Dict[str, List[str]]:
        """
        Get the aggregation methods supported by this plugin.
        
        Returns:
            Dictionary mapping dimensions to supported aggregation methods
        """
        pass 