"""
Insight generation and categorization components for LlamaSee.
"""
import uuid
import logging
from typing import Dict, Any, List, Optional, Set, Union
import pandas as pd
from ..core.insight import Insight
from ..insight_config import InsightConfig, default_config
from ..utils.trace import TraceManager
from llamasee.plugins.manager import PluginManager
from ..schema.comparison import ComparisonResult, ComparisonResultRow
from datetime import datetime

class InsightGenerator:
    """
    Generates and categorizes insights from comparison results.
    
    This class is responsible for:
    1. Generating insights from different types of analysis
    2. Categorizing insights by type and scope
    3. Calculating importance scores and metrics
    4. Grouping related insights
    """
    
    def __init__(self, insight_config: Optional[InsightConfig] = None, plugin_manager=None):
        """
        Initialize the insight generator.
        
        Args:
            insight_config: Configuration for insight generation
            plugin_manager: Plugin manager for insight plugins
        """
        self.insight_config = insight_config or default_config
        self.plugin_manager = plugin_manager or PluginManager()
        self.logger = logging.getLogger(__name__)
#        self.logger.propagate = True
        self.logger.setLevel(logging.DEBUG)

        self.trace_manager = TraceManager()  
    def _filter_by_fact_type(self, comparison_results: Union[pd.DataFrame, Dict[str, Any], ComparisonResult], fact_type: Optional[str] = None) -> Union[pd.DataFrame, Dict[str, Any], ComparisonResult]:
        """
        Filter comparison results by fact type.
        
        Args:
            comparison_results: Results to filter
            fact_type: Fact type to filter by
            
        Returns:
            Filtered results in the same format as input
        """
        self.logger.info(f"Filtering by fact type: {fact_type}")
        
        if fact_type is None:
            self.logger.info("No fact type provided, returning original results")
            return comparison_results
            
        if isinstance(comparison_results, pd.DataFrame):
            self.logger.info(f"Input is DataFrame with shape {comparison_results.shape}")
            self.logger.info(f"DataFrame columns: {comparison_results.columns.tolist()}")
            
            # If fact_type column exists, filter directly
            if 'fact_type' in comparison_results.columns:
                filtered_df = comparison_results[comparison_results['fact_type'] == fact_type]
                self.logger.info(f"Filtered DataFrame shape: {filtered_df.shape}")
                return filtered_df
            
            # If no fact_type column, try to create ComparisonResult
            try:
                # Create a ComparisonResult from the DataFrame
                rows = []
                for _, row in comparison_results.iterrows():
                    # Extract key information
                    key = {}
                    dimension = {}
                    for col in row.index:
                        if col.startswith('dim_'):
                            dimension[col[4:]] = row[col]
                        elif col not in ['value_a', 'value_b', 'diff', 'percent_change', 'fact_type']:
                            key[col] = row[col]
                    
                    # Create ComparisonResultRow
                    result_row = ComparisonResultRow(
                        key=key,
                        dimension=dimension,
                        fact_type=fact_type,  # Use provided fact_type
                        value_a=row.get('value_a'),
                        value_b=row.get('value_b'),
                        diff=row.get('diff'),
                        percent_change=row.get('percent_change')
                    )
                    rows.append(result_row)
                
                comparison_result = ComparisonResult(rows=rows)
                filtered_result = comparison_result.filter_by_fact_type(fact_type)
                return filtered_result.to_dataframe()
                
            except Exception as e:
                self.logger.warning(f"Failed to create ComparisonResult from DataFrame: {e}")
                # Return original DataFrame if conversion fails
                return comparison_results
        
        elif isinstance(comparison_results, ComparisonResult):
            self.logger.info("Input is ComparisonResult")
            return comparison_results.filter_by_fact_type(fact_type)
            
        elif isinstance(comparison_results, dict):
            self.logger.info("Input is dictionary")
            if 'fact_type' in comparison_results:
                return comparison_results if comparison_results['fact_type'] == fact_type else {}
            return comparison_results
            
        else:
            self.logger.warning(f"Unsupported type for comparison_results: {type(comparison_results)}")
            return comparison_results

    def generate_insights(
        self,
        comparison_results: Union[Dict[str, Any], pd.DataFrame, ComparisonResult],
        scope: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        top_n: int = 5,
        fact_type: Optional[str] = None,
        time_key: Optional[str] = None
    ) -> List[Insight]:
        """
        Generate insights from comparison results.
        
        Args:
            comparison_results: Results from data comparison (can be DataFrame, dict, or ComparisonResult)
            scope: Scope information from analysis
            context: Additional context
            top_n: Number of top insights to return
            fact_type: Optional fact type to filter insights by (e.g., "forecast_value_p50")
            time_key: Optional time key to use for time-based insights
            
        Returns:
            List[Insight]: Generated insights
        """
        self.logger.info("Starting insight generation")
        
        # Check if comparison_results is valid
        if comparison_results is None:
            self.logger.error("No comparison results provided")
            return []
            
        # Log comparison_results type and length
        self.logger.debug(f"comparison_results type: {type(comparison_results)}")
        if isinstance(comparison_results, pd.DataFrame):
            self.logger.debug(f"DataFrame shape: {comparison_results.shape}")
        elif isinstance(comparison_results, dict):
            self.logger.debug(f"Dictionary length: {len(comparison_results)}")
        elif isinstance(comparison_results, ComparisonResult):
            self.logger.debug(f"ComparisonResult with {len(comparison_results.rows)} rows")
        
        # Filter by fact_type if provided
        if fact_type:
            self.logger.info(f"Filtering by fact_type: {fact_type}")
            comparison_results = self._filter_by_fact_type(comparison_results, fact_type)
            self.logger.debug(f"Filtered comparison_results type: {type(comparison_results)}")
            if isinstance(comparison_results, ComparisonResult):
                self.logger.debug(f"Filtered ComparisonResult with {len(comparison_results.rows)} rows")
            elif isinstance(comparison_results, pd.DataFrame):
                self.logger.debug(f"Filtered DataFrame shape: {comparison_results.shape}")
        
        # Convert to ComparisonResult only if needed for plugins
        comparison_result_for_plugins = None
        if not isinstance(comparison_results, ComparisonResult):
            self.logger.info("Converting to ComparisonResult format for plugins")
            if isinstance(comparison_results, pd.DataFrame):
                self.logger.info(f"Converting DataFrame with columns: {comparison_results.columns.tolist()}")
                # Create ComparisonResultRow objects
                rows = []
                for _, row in comparison_results.iterrows():
                    # Create key dictionary
                    key = {}
                    dimension = {}
                    
                    # Process each column
                    for col in row.index:
                        # Skip NaN values
                        if pd.isna(row[col]):
                            continue
                            
                        # Handle dimension columns
                        if col.startswith('dim_'):
                            dimension[col[4:]] = row[col]
                        # Handle special columns
                        elif col in ['value_a', 'value_b', 'diff', 'percent_change', 'fact_type']:
                            continue
                        # Handle time key
                        elif col in ['time_key', 'forecast_date', 'date']:
                            key['time_key'] = row[col]
                        # All other columns go into key
                        else:
                            key[col] = row[col]
                    
                    # Determine value columns based on fact_type
                    value_a = None
                    value_b = None
                    diff_val = None
                    pct_change = None
                    
                    if fact_type:
                        # Try fact_type specific columns first
                        value_a = row.get(f"{fact_type}_a")
                        value_b = row.get(f"{fact_type}_b")
                        diff_val = row.get(f"{fact_type}_diff")
                        pct_change = row.get(f"{fact_type}_pct_diff")
                    
                    # Fallback to generic columns if needed
                    if value_a is None:
                        value_a = row.get('value_a')
                    if value_b is None:
                        value_b = row.get('value_b')
                    if diff_val is None:
                        diff_val = row.get('diff')
                    if pct_change is None:
                        pct_change = row.get('percent_change')
                    
                    # Create ComparisonResultRow
                    comparison_row = ComparisonResultRow(
                        key=key,
                        dimension=dimension,
                        fact_type=fact_type or row.get('fact_type', 'value'),
                        value_a=value_a,
                        value_b=value_b,
                        diff=diff_val,
                        percent_change=pct_change,
                        time_key=key.get('time_key'),
                        time_key_info={},
                        timestamp=datetime.now()
                    )
                    rows.append(comparison_row)
                
                # Create ComparisonResult object
                comparison_result_for_plugins = ComparisonResult(
                    df=comparison_results,
                    rows=rows,
                    metadata={
                        "fact_type": fact_type,
                        "timestamp": datetime.now()
                    }
                )
                self.logger.info(f"Created ComparisonResult with {len(rows)} rows")
            elif isinstance(comparison_results, dict):
                # Create ComparisonResultRow objects
                rows = []
                for row_data in comparison_results.values():
                    if isinstance(row_data, dict):
                        comparison_row = ComparisonResultRow(**row_data)
                        rows.append(comparison_row)
                
                # Create ComparisonResult object
                comparison_result_for_plugins = ComparisonResult(
                    df=pd.DataFrame(comparison_results.values()),
                    rows=rows,
                    metadata={
                        "fact_type": fact_type,
                        "timestamp": datetime.now()
                    }
                )
        else:
            comparison_result_for_plugins = comparison_results
        
        # Get insight plugins
        insight_plugins = self.plugin_manager.get_insight_plugins_by_type("all")
        self.logger.info(f"Found {len(insight_plugins)} insight plugins")
        
        # Generate insights using plugins
        all_insights = []
        for plugin in insight_plugins:
            try:
                self.logger.info(f"Generating insights using plugin: {plugin.__class__.__name__}")
                plugin_insights = plugin.generate_insights(
                    comparison_results=comparison_result_for_plugins,
                    context=context,
                    top_n=top_n,
                    fact_type=fact_type,
                    time_key=time_key
                )
                all_insights.extend(plugin_insights)
                self.logger.info(f"Generated {len(plugin_insights)} insights from {plugin.__class__.__name__}")
            except Exception as e:
                self.logger.error(f"Error generating insights with plugin {plugin.__class__.__name__}: {str(e)}")
        
        # Sort insights by importance score
        all_insights.sort(key=lambda x: x.importance_score, reverse=True)
        
        # Return top N insights
        return all_insights[:top_n]
    
    def _get_plugins(self) -> List[Any]:
        """
        Get insight plugins from the plugin manager.
        
        Returns:
            List of insight plugins
        """
        if not self.plugin_manager:
            return []
        
        plugins = []
        
        # Get plugins by insight type
        for insight_type in ['data_science', 'data_structure', 'context']:
            try:
                type_plugins = self.plugin_manager.get_insight_plugins_by_type(insight_type)
                plugins.extend(type_plugins)
            except Exception as e:
                self.logger.error(f"Error getting plugins for insight type {insight_type}: {str(e)}")
        
        return plugins
    
    def _categorize_insight(self, insight: Insight, all_insights: List[Insight] = None) -> Insight:
        """
        Categorize an insight based on its source data.
        
        Args:
            insight: The insight to categorize
            all_insights: List of all insights for uniqueness calculation
            
        Returns:
            The categorized insight
        """
        source_data = insight.source_data
        
        # Determine insight type using the configuration
        insight.insight_type = self.insight_config.detect_insight_type(source_data)
        
        # Determine scope level
        if 'key_components' in source_data:
            insight.scope_level = 'individual'
            insight.dimensions = list(source_data['key_components'].keys())
        elif any(key in source_data for key in ['dimension', 'dimension_value']) or 'dimension_insights' in source_data:
            insight.scope_level = 'dimension'
            dimension = source_data.get('dimension', '')
            insight.dimensions = [dimension] if dimension else []
        elif source_data.get('type') in ['scope', 'key_overlap', 'key_difference']:
            insight.scope_level = 'aggregate'
            insight.dimensions = []
        else:
            # Default to aggregate scope for value-level insights
            insight.scope_level = 'aggregate'
            insight.dimensions = []
        
        # Calculate importance factors
        insight.magnitude = self._calculate_magnitude(source_data)
        insight.frequency = self._calculate_frequency(source_data)
        insight.business_impact = self._calculate_business_impact(source_data)
        
        # Calculate uniqueness if all_insights is provided
        if all_insights:
            insight.uniqueness = self._calculate_uniqueness(insight, all_insights)
        else:
            insight.uniqueness = 0.5  # Default uniqueness
        
        return insight
    
    def _calculate_magnitude(self, source_data: Dict[str, Any]) -> float:
        """
        Calculate the normalized magnitude of an insight.
        
        Args:
            source_data: The source data for the insight
            
        Returns:
            Normalized magnitude score (0-1)
        """
        # Default magnitude
        magnitude = 0.5
        
        # For difference insights
        if 'percentage_diff' in source_data:
            pct_diff = abs(source_data['percentage_diff'])
            # Normalize percentage difference using configuration
            magnitude = self.insight_config.normalize_value(pct_diff, 'percentage_diff')
        
        # For anomaly insights
        if 'anomalies' in source_data:
            total_anomalies = source_data.get('total_anomalies', 0)
            # Normalize based on number of anomalies using configuration
            magnitude = self.insight_config.normalize_value(total_anomalies, 'anomalies')
        
        # For trend insights
        if 'trend_similarity' in source_data:
            # Higher magnitude for more distinct trends
            magnitude = 1.0 - abs(source_data['trend_similarity'])
        
        return magnitude
    
    def _calculate_frequency(self, source_data: Dict[str, Any]) -> float:
        """
        Calculate the normalized frequency of an insight.
        
        Args:
            source_data: The source data for the insight
            
        Returns:
            Normalized frequency score (0-1)
        """
        # Default frequency
        frequency = 0.5
        
        # For difference insights
        if 'total_comparisons' in source_data:
            total = source_data['total_comparisons']
            # Normalize based on total comparisons using configuration
            frequency = self.insight_config.normalize_value(total, 'total_comparisons')
        
        # For anomaly insights
        if 'anomalies' in source_data and 'total_comparisons' in source_data:
            anomalies = source_data.get('total_anomalies', 0)
            total = source_data['total_comparisons']
            if total > 0:
                # Frequency is the ratio of anomalies to total comparisons
                frequency = min(1.0, anomalies / total)
        
        return frequency
    
    def _calculate_business_impact(self, source_data: Dict[str, Any]) -> float:
        """
        Calculate the normalized business impact of an insight.
        
        Args:
            source_data: The source data for the insight
            
        Returns:
            Normalized business impact score (0-1)
        """
        # Default business impact
        impact = 0.5
        
        # Check if the insight is related to key metrics
        key_metrics = self.insight_config.get_key_metrics()
        columns = source_data.get('columns', [])
        
        # Higher impact if related to key metrics
        if any(metric in columns for metric in key_metrics):
            impact = self.insight_config.get_business_impact_default('key_metrics')
        
        # For difference insights, higher impact for larger differences
        if 'percentage_diff' in source_data:
            pct_diff = abs(source_data['percentage_diff'])
            # Scale impact based on percentage difference using configuration
            impact = max(impact, self.insight_config.normalize_value(pct_diff, 'percentage_diff'))
        
        # For anomaly insights, higher impact for more anomalies
        if 'anomalies' in source_data:
            total_anomalies = source_data.get('total_anomalies', 0)
            # Scale impact based on number of anomalies using configuration
            impact = max(impact, self.insight_config.normalize_value(total_anomalies, 'anomalies'))
        
        return impact
    
    def _calculate_uniqueness(self, insight: Insight, all_insights: List[Insight]) -> float:
        """
        Calculate the normalized uniqueness of an insight.
        
        Args:
            insight: The insight to evaluate
            all_insights: List of all insights
            
        Returns:
            Normalized uniqueness score (0-1)
        """
        # Default uniqueness
        uniqueness = 0.5
        
        # Count similar insights
        similar_count = 0
        for other in all_insights:
            if other.id == insight.id:
                continue
                
            # Check if insights are of the same type
            if other.insight_type == insight.insight_type:
                similar_count += 1
                
            # Check if insights have similar dimensions
            if set(other.dimensions) == set(insight.dimensions):
                similar_count += 1
        
        # Calculate uniqueness based on similar insights
        if similar_count > 0:
            uniqueness = 1.0 / (1.0 + similar_count)
        
        return uniqueness
    
    def _calculate_weighted_score(self, insight: Insight) -> float:
        """
        Calculate a weighted importance score based on multiple factors.
        
        Args:
            insight: The insight to score
            
        Returns:
            Weighted importance score (0-100)
        """
        # Get weights from configuration
        weights = self.insight_config.get_weights(insight.insight_type, insight.scope_level)
        
        # Ensure all factors are between 0 and 1
        magnitude = max(0.0, min(1.0, insight.magnitude))
        frequency = max(0.0, min(1.0, insight.frequency))
        business_impact = max(0.0, min(1.0, insight.business_impact))
        uniqueness = max(0.0, min(1.0, insight.uniqueness))
        
        # Calculate weighted score (0-1)
        score = (
            magnitude * weights['magnitude'] +
            frequency * weights['frequency'] +
            business_impact * weights['business_impact'] +
            uniqueness * weights['uniqueness']
        )
        
        # Normalize to 0-100 range
        score = max(0.0, min(1.0, score)) * 100.0
        
        return score
    
    def group_insights(self, insights: List[Insight]) -> Dict[str, Dict[str, List[Insight]]]:
        """
        Group insights by type and scope.
        
        Args:
            insights: List of insights to group
            
        Returns:
            Dictionary of grouped insights
        """
        grouped = {
            'difference': {'global': [], 'dimension': [], 'individual': []},
            'trend': {'global': [], 'dimension': [], 'individual': []},
            'anomaly': {'global': [], 'dimension': [], 'individual': []},
            'scope': {'global': [], 'dimension': [], 'individual': []},
            'distribution': {'global': [], 'dimension': [], 'individual': []},
            'other': {'global': [], 'dimension': [], 'individual': []}
        }
        
        for insight in insights:
            if insight.insight_type in grouped:
                grouped[insight.insight_type][insight.scope_level].append(insight)
        
        return grouped
    
    def _generate_scope_insights(self, scope: Dict[str, Any]) -> List[Insight]:
        """
        Generate insights from scope analysis.
        
        Args:
            scope: Scope information from analysis
            
        Returns:
            List[Insight]: Generated scope insights
        """
        insights = []
        
        # Insight about column overlap
        if scope['overlap_percentage'] < 100:
            insight_id = str(uuid.uuid4())
            description = f"Only {scope['overlap_percentage']:.1f}% of columns are common between datasets"
            importance_score = 0.8
            
            source_data = {
                'type': 'scope',
                'common_columns': scope['common_columns'],
                'unique_to_a': scope['unique_to_a'],
                'unique_to_b': scope['unique_to_b']
            }
            
            insight = Insight(insight_id, description, importance_score, source_data)
            
            # Populate trace data
            insight.trace_data = {
                'data_indices': [],
                'columns': list(scope['common_columns']) + list(scope['unique_to_a']) + list(scope['unique_to_b']),
                'values': {},
                'context': {'overlap_percentage': scope['overlap_percentage']}
            }
            
            insights.append(insight)
        
        # Insight about key overlap
        if 'key_overlap' in scope and scope['key_overlap'] is not None:
            key_overlap = scope['key_overlap']
            if key_overlap['overlap_percentage'] < 100:
                insight_id = str(uuid.uuid4())
                description = f"Only {key_overlap['overlap_percentage']:.1f}% of key combinations are common between datasets"
                importance_score = 0.9
                
                source_data = {
                    'type': 'key_overlap',
                    'common_keys': key_overlap['common_keys'],
                    'unique_to_a': key_overlap['unique_to_a'],
                    'unique_to_b': key_overlap['unique_to_b']
                }
                
                insight = Insight(insight_id, description, importance_score, source_data)
                
                # Populate trace data
                insight.trace_data = {
                    'data_indices': [],
                    'columns': scope.get('keys', []),
                    'values': {
                        'common_keys': key_overlap['common_keys'],
                        'unique_to_a': key_overlap['unique_to_a'],
                        'unique_to_b': key_overlap['unique_to_b']
                    },
                    'context': {'overlap_percentage': key_overlap['overlap_percentage']}
                }
                
                insights.append(insight)
        
        # Insights about dimension overlap
        for dimension, info in scope.get('overlap', {}).items():
            if info['overlap_percentage'] < 100:
                insight_id = str(uuid.uuid4())
                description = f"Dimension '{dimension}' has {info['overlap_percentage']:.1f}% overlap between datasets"
                importance_score = 0.7
                
                source_data = {
                    'type': 'dimension_overlap',
                    'dimension': dimension,
                    'common_values': info['common_values'],
                    'unique_to_a': info['unique_to_a'],
                    'unique_to_b': info['unique_to_b']
                }
                
                insight = Insight(insight_id, description, importance_score, source_data)
                
                # Populate trace data
                insight.trace_data = {
                    'data_indices': [],
                    'columns': [dimension],
                    'values': {
                        'common_values': info['common_values'],
                        'unique_to_a': info['unique_to_a'],
                        'unique_to_b': info['unique_to_b']
                    },
                    'context': {'overlap_percentage': info['overlap_percentage']}
                }
                
                insights.append(insight)
        
        return insights
    
    def _generate_value_insights(self, comparison_results: Dict[str, Any]) -> List[Insight]:
        """
        Generate insights from value comparisons.
        
        Args:
            comparison_results: Results from data comparison
            
        Returns:
            List[Insight]: Generated value insights
        """
        insights = []
        
        for value, results in comparison_results.items():
            if value == 'key_differences':
                continue
                
            if 'summary' in results:
                summary = results['summary']
                
                # Check for significant mean difference
                if abs(summary['mean_percentage_diff']) > 5.0:
                    insight_id = str(uuid.uuid4())
                    direction = "increased" if summary['mean_percentage_diff'] > 0 else "decreased"
                    description = f"{value} has {direction} by {abs(summary['mean_percentage_diff']):.1f}% on average"
                    importance_score = min(0.9, 0.5 + abs(summary['mean_percentage_diff']) / 100)
                    
                    source_data = {
                        'type': 'value_difference',
                        'value': value,
                        'mean_percentage_diff': summary['mean_percentage_diff'],
                        'mean_absolute_diff': summary['mean_absolute_diff'],
                        'mean_ratio': summary.get('mean_ratio', 0)
                    }
                    
                    insight = Insight(insight_id, description, importance_score, source_data)
                    
                    # Populate trace data
                    insight.trace_data = {
                        'data_indices': [],
                        'columns': [value],
                        'values': {
                            'mean_percentage_diff': summary['mean_percentage_diff'],
                            'mean_absolute_diff': summary['mean_absolute_diff'],
                            'mean_ratio': summary.get('mean_ratio', 0)
                        },
                        'context': {'value': value}
                    }
                    
                    insights.append(insight)
                
                # Check for extreme differences
                if abs(summary['max_percentage_diff']) > 20.0:
                    insight_id = str(uuid.uuid4())
                    direction = "increased" if summary['max_percentage_diff'] > 0 else "decreased"
                    description = f"Maximum {value} difference is {direction} by {abs(summary['max_percentage_diff']):.1f}%"
                    importance_score = min(0.9, 0.5 + abs(summary['max_percentage_diff']) / 100)
                    
                    source_data = {
                        'type': 'extreme_difference',
                        'value': value,
                        'max_percentage_diff': summary['max_percentage_diff']
                    }
                    
                    insight = Insight(insight_id, description, importance_score, source_data)
                    
                    # Populate trace data
                    insight.trace_data = {
                        'data_indices': [],
                        'columns': [value],
                        'values': {
                            'max_percentage_diff': summary['max_percentage_diff']
                        },
                        'context': {'value': value}
                    }
                    
                    insights.append(insight)
                
                # Check for significant ratio differences
                if 'mean_ratio' in summary and abs(summary['mean_ratio'] - 1.0) > 0.05:
                    insight_id = str(uuid.uuid4())
                    direction = "higher" if summary['mean_ratio'] > 1.0 else "lower"
                    description = f"{value} in dataset B is {direction} by a factor of {abs(summary['mean_ratio']):.2f} on average"
                    importance_score = min(0.9, 0.5 + abs(summary['mean_ratio'] - 1.0))
                    
                    source_data = {
                        'type': 'ratio_difference',
                        'value': value,
                        'mean_ratio': summary['mean_ratio']
                    }
                    
                    insight = Insight(insight_id, description, importance_score, source_data)
                    
                    # Populate trace data
                    insight.trace_data = {
                        'data_indices': [],
                        'columns': [value],
                        'values': {
                            'mean_ratio': summary['mean_ratio']
                        },
                        'context': {'value': value}
                    }
                    
                    insights.append(insight)
        
        return insights
    
    def _generate_trend_insights(self, comparison_results: Dict[str, Any]) -> List[Insight]:
        """
        Generate insights from trend analysis.
        
        Args:
            comparison_results: Results from data comparison
            
        Returns:
            List[Insight]: Generated trend insights
        """
        insights = []
        
        for value, results in comparison_results.items():
            if 'trends' in results:
                trend_results = results['trends']
                
                # Check for trend similarity
                if 'trend_similarity' in trend_results and trend_results['trend_similarity'] > 0.8:
                    insight_id = str(uuid.uuid4())
                    description = f"{value} shows similar trends in both datasets (correlation: {trend_results['trend_similarity']:.2f})"
                    importance_score = 0.7
                    
                    source_data = {
                        'type': 'trend_similarity',
                        'value': value,
                        'trend_similarity': trend_results['trend_similarity']
                    }
                    
                    insight = Insight(insight_id, description, importance_score, source_data)
                    
                    # Populate trace data
                    insight.trace_data = {
                        'data_indices': [],
                        'columns': [value],
                        'values': {
                            'trend_similarity': trend_results['trend_similarity']
                        },
                        'context': {'value': value}
                    }
                    
                    insights.append(insight)
                
                # Check for trend direction
                if 'trend_direction' in trend_results:
                    if trend_results['trend_direction'] == 'opposite':
                        insight_id = str(uuid.uuid4())
                        description = f"{value} shows opposite trends in the two datasets"
                        importance_score = 0.8
                        
                        source_data = {
                            'type': 'opposite_trends',
                            'value': value,
                            'trend_direction': trend_results['trend_direction']
                        }
                        
                        insight = Insight(insight_id, description, importance_score, source_data)
                        
                        # Populate trace data
                        insight.trace_data = {
                            'data_indices': [],
                            'columns': [value],
                            'values': {
                                'trend_direction': trend_results['trend_direction']
                            },
                            'context': {'value': value}
                        }
                        
                        insights.append(insight)
        
        return insights
    
    def _generate_anomaly_insights(self, comparison_results: Dict[str, Any]) -> List[Insight]:
        """
        Generate insights from anomaly detection.
        
        Args:
            comparison_results: Results from data comparison
            
        Returns:
            List[Insight]: Generated anomaly insights
        """
        insights = []
        
        for value, results in comparison_results.items():
            if 'anomalies' in results:
                anomaly_results = results['anomalies']
                
                # Check for significant number of anomalies
                if anomaly_results['total_anomalies'] > 10:
                    insight_id = str(uuid.uuid4())
                    description = f"Found {anomaly_results['total_anomalies']} anomalies in {value} comparisons"
                    importance_score = min(0.9, 0.5 + anomaly_results['total_anomalies'] / 100)
                    
                    source_data = {
                        'type': 'multiple_anomalies',
                        'value': value,
                        'total_anomalies': anomaly_results['total_anomalies']
                    }
                    
                    insight = Insight(insight_id, description, importance_score, source_data)
                    
                    # Populate trace data
                    insight.trace_data = {
                        'data_indices': [],
                        'columns': [value],
                        'values': {
                            'total_anomalies': anomaly_results['total_anomalies']
                        },
                        'context': {'value': value}
                    }
                    
                    insights.append(insight)
                
                # Check for specific anomalies with high percentage differences
                for key_str, anomaly in anomaly_results['anomalies'].items():
                    if abs(anomaly['difference']['percentage_diff']) > 30.0:
                        insight_id = str(uuid.uuid4())
                        key_components = anomaly['key_components']
                        key_desc = ", ".join([f"{k}: {v}" for k, v in key_components.items()])
                        
                        direction = "increased" if anomaly['difference']['percentage_diff'] > 0 else "decreased"
                        description = f"Anomaly in {value}: {direction} by {abs(anomaly['difference']['percentage_diff']):.1f}% for {key_desc}"
                        importance_score = min(0.9, 0.5 + abs(anomaly['difference']['percentage_diff']) / 100)
                        
                        source_data = {
                            'type': 'specific_anomaly',
                            'value': value,
                            'key': key_str,
                            'percentage_diff': anomaly['difference']['percentage_diff'],
                            'reason': anomaly['reason']
                        }
                        
                        insight = Insight(insight_id, description, importance_score, source_data)
                        
                        # Populate trace data
                        insight.trace_data = {
                            'data_indices': [],
                            'columns': [value] + list(key_components.keys()),
                            'values': {
                                'key': key_str,
                                'percentage_diff': anomaly['difference']['percentage_diff'],
                                'key_components': key_components
                            },
                            'context': {'value': value}
                        }
                        
                        insights.append(insight)
        
        return insights
    
    def _generate_dimension_specific_insights(self, comparison_results: Dict) -> List[Insight]:
        """
        Generate insights from dimension-specific analysis.
        
        This method follows a structured approach:
        1. Define dimensions with their keys and values
        2. Iterate through all dimension combinations
        3. Generate insights based on aggregated results
        
        Args:
            comparison_results: Dictionary containing comparison results
            
        Returns:
            List[Insight]: List of generated insights
        """
        insights = []
        self.logger.info("Starting dimension-specific insight generation")
        
        # Check if we have dimension insights
        if 'dimension_insights' not in comparison_results:
            self.logger.warning("No dimension insights found in comparison results")
            return insights
            
        # Step 1: Define dimensions
        dimension_definitions = []
        for dimension_name, dimension_data in comparison_results['dimension_insights'].items():
            self.logger.info(f"Processing dimension: {dimension_name}")
            
            # Get all values for this dimension
            dimension_values = list(dimension_data.keys())
            self.logger.info(f"Found {len(dimension_values)} values for dimension {dimension_name}")
            
            # Create dimension definition
            dimension_def = {
                'id': dimension_name,
                'name': dimension_name,
                'values': dimension_values
            }
            dimension_definitions.append(dimension_def)
            
        self.logger.info(f"Created {len(dimension_definitions)} dimension definitions")
        
        # Step 2: Iterate through all dimension combinations
        for dimension_def in dimension_definitions:
            dimension_id = dimension_def['id']
            dimension_name = dimension_def['name']
            dimension_values = dimension_def['values']
            
            self.logger.info(f"Processing dimension {dimension_id} with {len(dimension_values)} values")
            
            # Process each value in the dimension
            for value in dimension_values:
                self.logger.debug(f"Processing value {value} for dimension {dimension_id}")
                
                # Get the data for this dimension value
                value_data = comparison_results['dimension_insights'][dimension_id][value]
                
                # Check if we have metrics data
                if 'metrics' not in value_data:
                    self.logger.debug(f"No metrics data for dimension {dimension_id}, value {value}")
                    continue
                
                metrics = value_data['metrics']
                
                # Step 3: Generate insights based on metrics
                # Process each metric column
                for metric_col, metric_values in metrics.items():
                    # Check if this is a percentage difference column
                    is_percentage = 'percentage_diff' in metric_col.lower()
                    
                    # Get the mean value
                    mean_value = metric_values.get('mean', 0)
                    
                    # Check for significant differences
                    if abs(mean_value) > self.insight_config.significance_threshold:
                        self.logger.info(f"Found significant difference for dimension {dimension_id}, value {value}, metric {metric_col}: {mean_value:.2f}")
                        
                        # Calculate importance score based on magnitude
                        importance_score = min(0.9, 0.5 + abs(mean_value) / 100)
                        
                        # Create insight
                        insight = Insight(
                            id=f"dim_{dimension_id}_{value}_{metric_col}_{len(insights)}",
                            description=f"The {dimension_name} value {value} shows a significant difference of {mean_value:.2f} for {metric_col}",
                            importance_score=importance_score,
                            source_data={
                                'dimension': dimension_id,
                                'dimension_name': dimension_name,
                                'dimension_value': value,
                                'metric': metric_col,
                                'mean_value': mean_value,
                                'metrics': metrics,
                                'dimension_insights': True,
                                'scope_level': 'dimension'
                            }
                        )
                        
                        # Add trace data
                        insight.trace_data = {
                            'dimension': dimension_id,
                            'dimension_name': dimension_name,
                            'value': value,
                            'metric': metric_col,
                            'mean_value': mean_value,
                            'metrics': metrics
                        }
                        
                        insights.append(insight)
                        self.logger.info(f"Created insight for dimension {dimension_id}, value {value}, metric {metric_col}")
                    
                    # Check for large sum differences
                    sum_value = metric_values.get('sum', 0)
                    if abs(sum_value) > 0 and is_percentage and abs(sum_value) > self.insight_config.significance_threshold:
                        self.logger.info(f"Found significant sum difference for dimension {dimension_id}, value {value}, metric {metric_col}: {sum_value:.2f}")
                        
                        # Calculate importance score based on magnitude
                        importance_score = min(0.9, 0.5 + abs(sum_value) / 100)
                        
                        # Create insight
                        insight = Insight(
                            id=f"dim_sum_{dimension_id}_{value}_{metric_col}_{len(insights)}",
                            description=f"The {dimension_name} value {value} shows a significant sum difference of {sum_value:.2f} for {metric_col}",
                            importance_score=importance_score,
                            source_data={
                                'dimension': dimension_id,
                                'dimension_name': dimension_name,
                                'dimension_value': value,
                                'metric': metric_col,
                                'sum_value': sum_value,
                                'metrics': metrics,
                                'dimension_insights': True,
                                'scope_level': 'dimension'
                            }
                        )
                        
                        # Add trace data
                        insight.trace_data = {
                            'dimension': dimension_id,
                            'dimension_name': dimension_name,
                            'value': value,
                            'metric': metric_col,
                            'sum_value': sum_value,
                            'metrics': metrics
                        }
                        
                        insights.append(insight)
                        self.logger.info(f"Created sum difference insight for dimension {dimension_id}, value {value}, metric {metric_col}")
        
        self.logger.info(f"Generated {len(insights)} dimension-specific insights")
        return insights
    
    def _categorize_insights(self, insights: List[Insight]) -> List[Insight]:
        """
        Categorize insights by type and scope.
        
        Args:
            insights: List of insights to categorize
            
        Returns:
            List[Insight]: Categorized insights
        """
        for insight in insights:
            # Determine insight type
            if 'type' in insight.source_data:
                insight.insight_type = insight.source_data['type']
            
            # Determine scope level
            if 'key_components' in insight.source_data:
                insight.scope_level = 'individual'
            elif 'dimension' in insight.source_data or 'dimension_value' in insight.source_data:
                insight.scope_level = 'dimension'
            else:
                insight.scope_level = 'aggregate'
            
            # Calculate uniqueness score
            insight.uniqueness_score = self._calculate_uniqueness(insight)
            
            # Calculate weighted score
            insight.weighted_score = self._calculate_weighted_score(insight)
        
        return insights 