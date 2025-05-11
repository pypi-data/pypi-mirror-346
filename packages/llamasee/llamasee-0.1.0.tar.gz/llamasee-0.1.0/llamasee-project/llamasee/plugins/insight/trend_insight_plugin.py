"""
Trend insight plugin for LlamaSee.
"""
from typing import Dict, Any, List, Optional
import numpy as np
from scipy import stats
from ...core.insight import Insight
from .base_insight_plugin import BaseInsightPlugin
import logging

class TrendInsightPlugin(BaseInsightPlugin):
    """
    Plugin for generating trend insights.
    
    This plugin specializes in analyzing trends in time series data, including:
    - Linear trends
    - Seasonal patterns
    - Trend changes
    """
    
    def __init__(self):
        """Initialize the plugin."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.insight_types = ['trend']
        self.scope_levels = ['aggregate', 'dimension', 'individual']
        self.insight_type = 'trend'
    
    def generate_insights(
        self,
        comparison_results: Dict[str, Any],
        scope: str,
        context: Optional[Dict[str, Any]] = None,
        top_n: int = 10,
        fact_type: Optional[str] = None,
        time_key: Optional[str] = None
    ) -> List[Insight]:
        """
        Generate trend insights from comparison results.
        
        Args:
            comparison_results: Results from a comparison operation
            scope: The scope level for insights ('aggregate', 'dimension', 'individual')
            context: Optional context information for insight generation
            top_n: Maximum number of insights to return
            fact_type: Optional filter for specific fact types
            time_key: Optional key for time-based analysis
            
        Returns:
            List[Insight]: List of generated insights
        """
        insights = []
        
        # Extract comparison results and scope
        comparison_results = comparison_results.get('comparison_results', {})
        scope = scope
        
        # Generate linear trend insights
        linear_insights = self._generate_linear_trend_insights(comparison_results, scope)
        insights.extend(linear_insights)
        
        # Generate seasonal pattern insights
        seasonal_insights = self._generate_seasonal_insights(comparison_results, scope)
        insights.extend(seasonal_insights)
        
        # Generate trend change insights
        change_insights = self._generate_trend_change_insights(comparison_results, scope)
        insights.extend(change_insights)
        
        return insights
    
    def _generate_linear_trend_insights(self, comparison_results: Dict[str, Any], scope: str) -> List[Insight]:
        """Generate insights about linear trends in the data."""
        insights = []
        
        # Extract time series data
        time_series_data = self._extract_time_series_data(comparison_results)
        if not time_series_data:
            return insights
        
        # Calculate trend statistics
        for metric, values in time_series_data.items():
            if len(values) < 2:
                continue
                
            # Calculate linear regression
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Create trend insight
            insight = Insight(
                insight_type='trend',
                scope_level=scope,
                metric=metric,
                value={
                    'slope': slope,
                    'intercept': intercept,
                    'r_squared': r_value ** 2,
                    'p_value': p_value
                },
                significance=p_value,
                description=f"Linear trend analysis for {metric} shows a {self._get_trend_direction(slope)} trend "
                           f"with {self._get_significance_description(p_value)} significance "
                           f"(R² = {r_value ** 2:.3f})."
            )
            insights.append(insight)
        
        return insights
    
    def _generate_seasonal_insights(self, comparison_results: Dict[str, Any], scope: str) -> List[Insight]:
        """Generate insights about seasonal patterns in the data."""
        insights = []
        
        # Extract time series data
        time_series_data = self._extract_time_series_data(comparison_results)
        if not time_series_data:
            return insights
        
        # Look for seasonal patterns
        for metric, values in time_series_data.items():
            if len(values) < 14:  # Need at least 2 weeks of data
                continue
            
            # Calculate autocorrelation
            acf = np.correlate(values, values, mode='full')[len(values)-1:]
            acf = acf / acf[0]  # Normalize
            
            # Look for peaks in autocorrelation
            peaks = self._find_peaks(acf[1:])  # Skip lag 0
            if peaks:
                # Find the most significant seasonal period
                seasonal_period = peaks[0] + 1  # +1 because we skipped lag 0
                peak_value = acf[seasonal_period]
                
                # Create seasonal insight
                insight = Insight(
                    insight_type='trend',
                    scope_level=scope,
                    metric=metric,
                    value={
                        'seasonal_period': seasonal_period,
                        'autocorrelation': peak_value
                    },
                    significance=1.0 - abs(peak_value),  # Higher correlation = lower p-value
                    description=f"Seasonal pattern detected in {metric} with period {seasonal_period} "
                               f"(autocorrelation = {peak_value:.3f})."
                )
                insights.append(insight)
        
        return insights
    
    def _generate_trend_change_insights(self, comparison_results: Dict[str, Any], scope: str) -> List[Insight]:
        """Generate insights about changes in trends."""
        insights = []
        
        # Extract time series data
        time_series_data = self._extract_time_series_data(comparison_results)
        if not time_series_data:
            return insights
        
        # Analyze trend changes
        for metric, values in time_series_data.items():
            if len(values) < 10:  # Need enough data points
                continue
            
            # Calculate rolling slopes
            window_size = 5
            rolling_slopes = []
            for i in range(len(values) - window_size + 1):
                window = values[i:i+window_size]
                slope, _, _, p_value, _ = stats.linregress(np.arange(window_size), window)
                rolling_slopes.append((i + window_size//2, slope, p_value))
            
            # Find significant trend changes
            for i in range(1, len(rolling_slopes)):
                prev_slope, curr_slope = rolling_slopes[i-1][1], rolling_slopes[i][1]
                if abs(curr_slope - prev_slope) > 0.1 and rolling_slopes[i][2] < 0.05:
                    # Create trend change insight
                    insight = Insight(
                        insight_type='trend',
                        scope_level=scope,
                        metric=metric,
                        value={
                            'position': rolling_slopes[i][0],
                            'old_slope': prev_slope,
                            'new_slope': curr_slope,
                            'change': curr_slope - prev_slope
                        },
                        significance=rolling_slopes[i][2],
                        description=f"Significant trend change detected in {metric} at position {rolling_slopes[i][0]}: "
                                   f"slope changed from {prev_slope:.3f} to {curr_slope:.3f}."
                    )
                    insights.append(insight)
        
        return insights
    
    def _extract_time_series_data(self, comparison_results: Dict[str, Any]) -> Dict[str, List[float]]:
        """Extract time series data from comparison results."""
        time_series_data = {}
        
        # Extract metrics from comparison results
        for metric in ['forecast_value_p50', 'forecast_value_p10', 'forecast_value_p90']:
            if metric in comparison_results:
                values = [float(x) for x in comparison_results[metric] if x is not None]
                if values:
                    time_series_data[metric] = values
        
        return time_series_data
    
    def _find_peaks(self, arr: np.ndarray, threshold: float = 0.1) -> List[int]:
        """Find peaks in an array that are above the threshold."""
        peaks = []
        for i in range(1, len(arr)-1):
            if arr[i] > threshold and arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                peaks.append(i)
        return sorted(peaks, key=lambda x: arr[x], reverse=True)
    
    def _get_trend_direction(self, slope: float) -> str:
        """Get a human-readable description of the trend direction."""
        if slope > 0:
            return "upward"
        elif slope < 0:
            return "downward"
        else:
            return "flat"
    
    def _get_significance_description(self, p_value: float) -> str:
        """Get a human-readable description of the statistical significance."""
        if p_value < 0.01:
            return "high"
        elif p_value < 0.05:
            return "moderate"
        else:
            return "low"
