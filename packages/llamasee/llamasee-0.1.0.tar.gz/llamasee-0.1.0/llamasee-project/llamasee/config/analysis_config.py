"""
Configuration for data analysis components.

This module provides configuration classes for data analysis components,
including comparison methods, statistical tests, and visualization options.
"""

from typing import Dict, Any, List, Optional, Union
import numpy as np

class AnalysisConfig:
    """
    Configuration class for data analysis components.
    
    This class provides configuration options for data analysis components,
    including comparison methods, statistical tests, and visualization options.
    """
    
    def __init__(self, 
                 comparison_methods: Dict[str, bool] = None,
                 statistical_tests: Dict[str, Dict[str, Any]] = None,
                 visualization_options: Dict[str, Any] = None,
                 threshold_values: Dict[str, float] = None,
                 **kwargs):
        """
        Initialize the analysis configuration.
        
        Args:
            comparison_methods: Methods to use for data comparison
            statistical_tests: Statistical tests to use
            visualization_options: Options for data visualization
            threshold_values: Threshold values for various metrics
            **kwargs: Additional configuration options
        """
        self.comparison_methods = comparison_methods or self._get_default_comparison_methods()
        self.statistical_tests = statistical_tests or self._get_default_statistical_tests()
        self.visualization_options = visualization_options or self._get_default_visualization_options()
        self.threshold_values = threshold_values or self._get_default_threshold_values()
        
        # Store additional configuration options
        self.options = kwargs
    
    def _get_default_comparison_methods(self) -> Dict[str, bool]:
        """
        Get the default comparison methods.
        
        Returns:
            Dictionary of comparison methods
        """
        return {
            "basic_stats": True,
            "distribution": True,
            "correlation": True,
            "trend": True,
            "anomaly": True,
            "difference": True
        }
    
    def _get_default_statistical_tests(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the default statistical tests.
        
        Returns:
            Dictionary of statistical tests
        """
        return {
            "ttest": {
                "enabled": True,
                "alpha": 0.05,
                "equal_var": False
            },
            "mann_whitney": {
                "enabled": True,
                "alpha": 0.05
            },
            "ks_test": {
                "enabled": True,
                "alpha": 0.05
            },
            "chi_square": {
                "enabled": True,
                "alpha": 0.05
            },
            "anova": {
                "enabled": True,
                "alpha": 0.05
            }
        }
    
    def _get_default_visualization_options(self) -> Dict[str, Any]:
        """
        Get the default visualization options.
        
        Returns:
            Dictionary of visualization options
        """
        return {
            "histogram": {
                "enabled": True,
                "bins": "auto",
                "density": False
            },
            "boxplot": {
                "enabled": True,
                "showfliers": True
            },
            "scatter": {
                "enabled": True,
                "alpha": 0.5
            },
            "line": {
                "enabled": True,
                "markers": True
            },
            "bar": {
                "enabled": True,
                "stacked": False
            }
        }
    
    def _get_default_threshold_values(self) -> Dict[str, float]:
        """
        Get the default threshold values.
        
        Returns:
            Dictionary of threshold values
        """
        return {
            "correlation_threshold": 0.7,
            "difference_threshold": 0.1,
            "anomaly_threshold": 2.0,
            "trend_threshold": 0.05,
            "significance_threshold": 0.05
        }
    
    def get_comparison_methods(self) -> Dict[str, bool]:
        """
        Get the comparison methods.
        
        Returns:
            Dictionary of comparison methods
        """
        return self.comparison_methods
    
    def is_comparison_method_enabled(self, method: str) -> bool:
        """
        Check if a comparison method is enabled.
        
        Args:
            method: The comparison method
            
        Returns:
            True if the method is enabled
        """
        return self.comparison_methods.get(method, False)
    
    def get_statistical_tests(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the statistical tests.
        
        Returns:
            Dictionary of statistical tests
        """
        return self.statistical_tests
    
    def is_statistical_test_enabled(self, test: str) -> bool:
        """
        Check if a statistical test is enabled.
        
        Args:
            test: The statistical test
            
        Returns:
            True if the test is enabled
        """
        return self.statistical_tests.get(test, {}).get("enabled", False)
    
    def get_statistical_test_params(self, test: str) -> Dict[str, Any]:
        """
        Get the parameters for a statistical test.
        
        Args:
            test: The statistical test
            
        Returns:
            Dictionary of test parameters
        """
        return self.statistical_tests.get(test, {})
    
    def get_visualization_options(self) -> Dict[str, Any]:
        """
        Get the visualization options.
        
        Returns:
            Dictionary of visualization options
        """
        return self.visualization_options
    
    def is_visualization_enabled(self, viz_type: str) -> bool:
        """
        Check if a visualization type is enabled.
        
        Args:
            viz_type: The visualization type
            
        Returns:
            True if the visualization is enabled
        """
        return self.visualization_options.get(viz_type, {}).get("enabled", False)
    
    def get_visualization_params(self, viz_type: str) -> Dict[str, Any]:
        """
        Get the parameters for a visualization type.
        
        Args:
            viz_type: The visualization type
            
        Returns:
            Dictionary of visualization parameters
        """
        return self.visualization_options.get(viz_type, {})
    
    def get_threshold_values(self) -> Dict[str, float]:
        """
        Get the threshold values.
        
        Returns:
            Dictionary of threshold values
        """
        return self.threshold_values
    
    def get_threshold(self, threshold_name: str) -> float:
        """
        Get a threshold value.
        
        Args:
            threshold_name: The threshold name
            
        Returns:
            Threshold value
        """
        return self.threshold_values.get(threshold_name, 0.0)
    
    def get_option(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration option.
        
        Args:
            key: The option key
            default: Default value if the option is not set
            
        Returns:
            The option value
        """
        return self.options.get(key, default)

# Default configuration instance
default_config = AnalysisConfig() 