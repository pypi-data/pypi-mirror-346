"""
Configuration for insight categorization and scoring.

This module provides default configurations for insight categorization,
including weights, thresholds, and normalization factors.
"""

from typing import Dict, Any, List

# Default insight type weights
DEFAULT_WEIGHTS = {
    'magnitude': 0.3,
    'frequency': 0.2,
    'business_impact': 0.3,
    'uniqueness': 0.2
}

# Type-specific weight adjustments
TYPE_WEIGHT_ADJUSTMENTS = {
    'anomaly': {
        'magnitude': 0.1,
        'frequency': -0.1,
        'business_impact': 0.0,
        'uniqueness': 0.0
    },
    'trend': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.1,
        'uniqueness': -0.1
    },
    'difference': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.0,
        'uniqueness': 0.0
    },
    'scope': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.0,
        'uniqueness': 0.0
    },
    'distribution': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.0,
        'uniqueness': 0.0
    },
    'other': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.0,
        'uniqueness': 0.0
    }
}

# Scope-specific weight adjustments
SCOPE_WEIGHT_ADJUSTMENTS = {
    'global': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.1,
        'uniqueness': -0.1
    },
    'dimension': {
        'magnitude': 0.0,
        'frequency': 0.0,
        'business_impact': 0.0,
        'uniqueness': 0.0
    },
    'individual': {
        'magnitude': 0.0,
        'frequency': -0.1,
        'business_impact': 0.0,
        'uniqueness': 0.1
    }
}

# Normalization factors for different metrics
NORMALIZATION_FACTORS = {
    'percentage_diff': 100.0,  # 100% difference is considered maximum
    'total_comparisons': 1000.0,  # 1000 comparisons is considered maximum
    'anomalies': 100.0,  # 100 anomalies is considered maximum
    'trend_similarity': 1.0,  # 1.0 similarity is considered maximum
}

# Default business impact for different factors
BUSINESS_IMPACT_DEFAULTS = {
    'key_metrics': 0.8,  # Default impact for insights related to key metrics
    'percentage_diff': 50.0,  # 50% difference is considered high impact
    'anomalies': 50.0,  # 50 anomalies is considered high impact
}

# Key metrics that are considered important for business impact
KEY_METRICS = [
    'sales',
    'revenue',
    'profit',
    'cost',
    'customer',
    'user',
    'conversion',
    'retention'
]

# Insight type detection patterns
INSIGHT_TYPE_PATTERNS = {
    'difference': ['difference', 'percentage_diff', 'absolute_diff', 'ratio'],
    'trend': ['trend', 'trend_direction', 'trend_similarity', 'increasing', 'decreasing'],
    'anomaly': ['anomaly', 'anomalies', 'outlier', 'unexpected'],
    'scope': ['scope', 'overlap', 'missing', 'coverage'],
    'distribution': ['distribution', 'skewness', 'variance', 'spread'],
}

# Default significance threshold for dimension insights
DEFAULT_SIGNIFICANCE_THRESHOLD = 5.0  # 5% difference is considered significant

class InsightConfig:
    """
    Configuration class for insight categorization and scoring.
    
    This class provides methods to access and customize insight categorization settings.
    """
    
    def __init__(self, 
                 weights: Dict[str, float] = None,
                 type_adjustments: Dict[str, Dict[str, float]] = None,
                 scope_adjustments: Dict[str, Dict[str, float]] = None,
                 normalization_factors: Dict[str, float] = None,
                 business_impact_defaults: Dict[str, float] = None,
                 insight_type_patterns: Dict[str, List[str]] = None,
                 key_metrics: List[str] = None,
                 significance_threshold: float = None):
        """
        Initialize the insight configuration.
        
        Args:
            weights: Default weights for different factors
            type_adjustments: Weight adjustments for different insight types
            scope_adjustments: Weight adjustments for different scope levels
            normalization_factors: Factors for normalizing different metrics
            business_impact_defaults: Default business impact values
            insight_type_patterns: Patterns for detecting insight types
            key_metrics: List of key metrics for business impact calculation
            significance_threshold: Threshold for determining significant differences in dimension insights
        """
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.type_adjustments = type_adjustments or TYPE_WEIGHT_ADJUSTMENTS.copy()
        self.scope_adjustments = scope_adjustments or SCOPE_WEIGHT_ADJUSTMENTS.copy()
        self.normalization_factors = normalization_factors or NORMALIZATION_FACTORS.copy()
        self.business_impact_defaults = business_impact_defaults or BUSINESS_IMPACT_DEFAULTS.copy()
        self.insight_type_patterns = insight_type_patterns or INSIGHT_TYPE_PATTERNS.copy()
        self.key_metrics = key_metrics or KEY_METRICS.copy()
        self.significance_threshold = significance_threshold or DEFAULT_SIGNIFICANCE_THRESHOLD
    
    def get_weights(self, insight_type: str = None, scope_level: str = None) -> Dict[str, float]:
        """
        Get the weights for different factors, adjusted for insight type and scope.
        
        Args:
            insight_type: The type of insight
            scope_level: The scope level of the insight
            
        Returns:
            Dictionary of weights for different factors
        """
        # Start with default weights
        weights = self.weights.copy()
        
        # Apply type-specific adjustments
        if insight_type and insight_type in self.type_adjustments:
            for factor, adjustment in self.type_adjustments[insight_type].items():
                weights[factor] = weights.get(factor, 0.0) + adjustment
        
        # Apply scope-specific adjustments
        if scope_level and scope_level in self.scope_adjustments:
            for factor, adjustment in self.scope_adjustments[scope_level].items():
                weights[factor] = weights.get(factor, 0.0) + adjustment
        
        return weights
    
    def normalize_value(self, value: float, metric: str) -> float:
        """
        Normalize a value based on the appropriate normalization factor.
        
        Args:
            value: The value to normalize
            metric: The metric type (e.g., 'percentage_diff', 'total_comparisons')
            
        Returns:
            Normalized value between 0 and 1
        """
        if metric in self.normalization_factors:
            factor = self.normalization_factors[metric]
            return min(1.0, abs(value) / factor)
        return 0.5  # Default normalization
    
    def get_business_impact_default(self, factor: str) -> float:
        """
        Get the default business impact for a specific factor.
        
        Args:
            factor: The factor to get the default for
            
        Returns:
            Default business impact value
        """
        return self.business_impact_defaults.get(factor, 0.5)
    
    def get_key_metrics(self) -> List[str]:
        """
        Get the list of key metrics for business impact calculation.
        
        Returns:
            List of key metrics
        """
        return self.key_metrics
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        return {
            "weights": self.weights,
            "type_adjustments": self.type_adjustments,
            "scope_adjustments": self.scope_adjustments,
            "normalization_factors": self.normalization_factors,
            "business_impact_defaults": self.business_impact_defaults,
            "insight_type_patterns": self.insight_type_patterns,
            "key_metrics": self.key_metrics,
            "significance_threshold": self.significance_threshold
        }
    
    def detect_insight_type(self, source_data: Dict[str, Any]) -> str:
        """
        Detect the type of insight based on source data.
        
        Args:
            source_data: The source data for the insight
            
        Returns:
            str: The detected insight type
        """
        # Get type from source data
        data_type = source_data.get('type', '')
        
        # Map source data types to insight types
        type_mapping = {
            'scope': 'scope',
            'key_overlap': 'scope',
            'dimension_overlap': 'scope',
            'value_difference': 'difference',
            'extreme_difference': 'difference',
            'ratio_difference': 'difference',
            'trend_similarity': 'trend',
            'opposite_trends': 'trend',
            'multiple_anomalies': 'anomaly',
            'specific_anomaly': 'anomaly',
            'key_difference': 'distribution',
            'dimension_specific': 'distribution'
        }
        
        return type_mapping.get(data_type, 'other')

# Default configuration instance
default_config = InsightConfig() 