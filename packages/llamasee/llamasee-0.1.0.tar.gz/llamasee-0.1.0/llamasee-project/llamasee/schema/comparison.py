"""
Canonical data comparison model for LlamaSee.

This module defines the standard intermediate format for comparison results,
ensuring consistent data representation across different comparison plugins
and insight generators.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import pandas as pd
import numpy as np
import logging

@dataclass
class ComparisonResultRow:
    """
    Represents a single row of comparison results in the canonical format.
    
    This is the fundamental unit of comparison in LlamaSee, representing
    the difference between two values for a given key and dimension.
    
    Time-related fields:
    - time_key: The primary time-related key (e.g., date, period)
      - granularity: The granularity of the time key (e.g., day, week, month)
      - metadata: Additional time-related metadata (e.g., fiscal period, season)
    """
    # Key information (combination of all key columns from prepare and fit stages)
    key: Dict[str, Any] = field(default_factory=dict)
    
    # Time-related fields
    time_key: Optional[str] = None
    time_key_info: Dict[str, Any] = field(default_factory=lambda: {
        "granularity": None,
        "metadata": {}
    })
    
    # Dimension information (enriched keys) - initially empty, can be enriched later
    dimension: Dict[str, Any] = field(default_factory=dict)
    
    # Fact type (value column name)
    fact_type: str = "value"
    
    # Values being compared
    value_a: Optional[float] = None
    value_b: Optional[float] = None
    
    # Difference metrics
    diff: Optional[float] = None
    percent_change: Optional[float] = None
    
    # Traceability and metadata
    trace_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate differences if not provided and handle time-related fields."""
        # Handle fact_type specific values
        if self.fact_type:
            # Check if fact_type specific values exist in key
            if f"{self.fact_type}_a" in self.key:
                self.value_a = self.key.pop(f"{self.fact_type}_a")
            if f"{self.fact_type}_b" in self.key:
                self.value_b = self.key.pop(f"{self.fact_type}_b")
            if f"{self.fact_type}_diff" in self.key:
                self.diff = self.key.pop(f"{self.fact_type}_diff")
            if f"{self.fact_type}_pct_diff" in self.key:
                self.percent_change = self.key.pop(f"{self.fact_type}_pct_diff")
        
        # Calculate differences if not provided
        if self.value_a is not None and self.value_b is not None:
            # Calculate difference metrics
            if self.diff is None:
                self.diff = self.value_b - self.value_a
            if self.percent_change is None and self.value_a != 0:
                self.percent_change = (self.diff / abs(self.value_a)) * 100
        
        # Move any dim_* keys from key to dimension
        dim_keys = {k: v for k, v in self.key.items() if k.startswith('dim_')}
        for k, v in dim_keys.items():
            # Remove from key
            del self.key[k]
            # Add to dimension with the dim_ prefix removed
            self.dimension[k[4:]] = v
        
        # Add match_status dimension if not present
        if 'match_status' not in self.dimension:
            if pd.isna(self.value_a) and pd.isna(self.value_b):
                self.dimension['match_status'] = 'missing_in_both'
            elif pd.isna(self.value_a):
                self.dimension['match_status'] = 'missing_in_a'
            elif pd.isna(self.value_b):
                self.dimension['match_status'] = 'missing_in_b'
            else:
                self.dimension['match_status'] = 'present_in_both'
                
        # Handle time-related fields
        self._process_time_fields()
            
    def detect_time_key_granularity(self, key_name: str) -> Optional[str]:
        """
        Detect the granularity of a time key based on its value.
        
        Args:
            key_name: The name of the time key to analyze
            
        Returns:
            The detected granularity (e.g., 'hour', 'day', 'week', 'month', 'year')
            or None if granularity cannot be determined
        """
        if key_name not in self.key:
            return None
            
        time_value = self.key[key_name]
        if time_value is None:
            return None
            
        try:
            # Convert to pandas timestamp for standardization
            ts = pd.to_datetime(time_value)
            
            # Infer granularity based on the timestamp format and value
            if ts.hour != 0 or ts.minute != 0:
                return 'hour'
            elif ts.day != 1:
                return 'day'
            elif ts.month != 1:
                return 'month'
            else:
                return 'year'
        except (ValueError, TypeError):
            # If conversion fails, try to infer granularity from the key name
            for pattern in ['hour', 'day', 'week', 'month', 'year']:
                if pattern in key_name.lower():
                    return pattern
                    
            return None
    
    def set_time_key_granularity(self, key_name: str, granularity: Optional[str] = None) -> None:
        """
        Set the granularity for a time key.
        
        Args:
            key_name: The name of the time key
            granularity: Optional granularity to set. If None, will attempt to detect it.
        """
        if key_name not in self.key:
            return
            
        # Set the time key
        self.time_key = key_name
        
        # If granularity is not provided, try to detect it
        if granularity is None:
            granularity = self.detect_time_key_granularity(key_name)
            
        # Set the granularity
        if granularity:
            self.time_key_info["granularity"] = granularity
            
        # Add time-related metadata
        time_value = self.key[key_name]
        if time_value is not None:
            try:
                # Convert to pandas timestamp for standardization
                ts = pd.to_datetime(time_value)
                
                # Store the standardized datetime value
                self.key[key_name] = ts
                
                # Add time-related metadata
                self.time_key_info["metadata"].update({
                    'year': ts.year,
                    'month': ts.month,
                    'quarter': (ts.month - 1) // 3 + 1,
                    'is_weekend': ts.weekday() >= 5 if self.time_key_info["granularity"] in ['day', 'hour'] else None,
                    'day_of_week': ts.weekday() if self.time_key_info["granularity"] in ['day', 'hour'] else None,
                    'week_of_year': ts.isocalendar()[1] if self.time_key_info["granularity"] in ['day', 'hour'] else None
                })
            except (ValueError, TypeError):
                # If conversion fails, just store the original value
                pass
            
    def _process_time_fields(self) -> None:
        """Process and validate time-related fields from keys."""
        # Common time-related column patterns
        time_patterns = ['date', 'period', 'time', 'year', 'month', 'week', 'day']
        
        # Look for time-related keys
        time_keys = [k for k in self.key.keys() if any(pattern in k.lower() for pattern in time_patterns)]
        
        if time_keys:
            # Use the first time key found as the primary time key
            primary_time_key = time_keys[0]
            self.set_time_key_granularity(primary_time_key)
            
            # Store any additional time-related keys as metadata
            for key in time_keys[1:]:
                self.time_key_info["metadata"][key] = self.key[key]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the row to a dictionary for DataFrame conversion."""
        # Start with the base dictionary
        result = {
            "key": self.key,
            "time_key": self.time_key,
            "time_key_info": self.time_key_info,
            "dimension": self.dimension,
            "fact_type": self.fact_type,
            "trace_id": self.trace_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
        
        # Add fact_type specific columns if fact_type is provided
        if self.fact_type:
            result[f"{self.fact_type}_a"] = self.value_a
            result[f"{self.fact_type}_b"] = self.value_b
            result[f"{self.fact_type}_diff"] = self.diff
            result[f"{self.fact_type}_pct_diff"] = self.percent_change
        
        # Add generic columns
        result["value_a"] = self.value_a
        result["value_b"] = self.value_b
        result["diff"] = self.diff
        result["percent_change"] = self.percent_change
        
        # Add flattened key and dimension values
        for k, v in self.key.items():
            result[k] = v
        for k, v in self.dimension.items():
            result[f"dim_{k}"] = v
        
        return result
        
    def enrich_dimensions(self, dimension_mappings: Dict[str, Dict[str, Any]]) -> None:
        """
        Enrich the dimension field with additional dimensional information based on mappings.
        
        This method can be called at runtime to add dimensional information to the row
        without modifying the original data. The dimension field will be populated with
        enriched key values based on the provided mappings.
        
        Args:
            dimension_mappings: Dictionary mapping key names to enrichment configurations
                Each configuration should include:
                - key_column: The original key column to enrich
                - enriched_key: The name of the enriched dimension
                - default_value: Value to use for unmapped keys (defaults to "Unknown")
                - mappings: Dictionary mapping original key values to enriched values
        """
        for key_name, config in dimension_mappings.items():
            # Skip if the key doesn't exist in this row
            if key_name not in self.key:
                continue
                
            # Get the original key value
            original_value = self.key[key_name]
            
            # Get the enriched key name and mappings
            enriched_key = config.get("enriched_key", f"dim_{key_name}")
            mappings = config.get("mappings", {})
            default_value = config.get("default_value", "Unknown")
            
            # Apply the mapping or use default value
            enriched_value = mappings.get(original_value, default_value)
            
            # Add to dimension dictionary
            self.dimension[enriched_key] = enriched_value

@dataclass
class ComparisonResult:
    """
    Represents the complete result of a comparison operation.
    
    This class contains the comparison results in both DataFrame and row format,
    along with metadata about the comparison operation.
    
    Time-series analysis capabilities:
    - trend_detection: Analyze trends in the data over time
    - anomaly_detection: Identify anomalies in time-series data
    - seasonality_analysis: Detect seasonal patterns in the data
    """
    # Core comparison data
    df: pd.DataFrame
    rows: List[ComparisonResultRow]
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate and process the comparison result."""
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("df must be a pandas DataFrame")
        if not isinstance(self.rows, list):
            raise ValueError("rows must be a list")
        if not all(isinstance(row, ComparisonResultRow) for row in self.rows):
            raise ValueError("all rows must be ComparisonResultRow instances")
            
        # Ensure DataFrame has required columns
        required_columns = {'value_a', 'value_b', 'diff', 'percent_change'}
        missing_columns = required_columns - set(self.df.columns)
        if missing_columns:
            # Try to find columns with fact_type prefix
            fact_types = {row.fact_type for row in self.rows if row.fact_type}
            if fact_types:
                self.metadata['fact_types'] = list(fact_types)
                for fact_type in fact_types:
                    # Add fact_type specific columns if they exist
                    if f"{fact_type}_a" in self.df.columns and f"{fact_type}_b" in self.df.columns:
                        self.df[f"{fact_type}_diff"] = self.df[f"{fact_type}_b"] - self.df[f"{fact_type}_a"]
                        self.df[f"{fact_type}_pct_diff"] = (self.df[f"{fact_type}_b"] / self.df[f"{fact_type}_a"] - 1) * 100
            else:
                # Add generic columns
                self.df['value_a'] = None
                self.df['value_b'] = None
                self.df['diff'] = None
                self.df['percent_change'] = None
        
        # Ensure DataFrame has time-related columns if present in rows
        if any(row.time_key for row in self.rows):
            if 'time_key' not in self.df.columns:
                self.df['time_key'] = None
            if 'time_key_info' not in self.df.columns:
                self.df['time_key_info'] = None
    
    def set_time_key_granularity(self, key_name: str, granularity: Optional[str] = None) -> None:
        """
        Set the granularity for a time key across all rows.
        
        Args:
            key_name: The name of the time key
            granularity: Optional granularity to set. If None, will attempt to detect it.
        """
        for row in self.rows:
            row.set_time_key_granularity(key_name, granularity)
            
        # Update DataFrame if needed
        if 'time_key' in self.df.columns and 'time_key_info' in self.df.columns:
            # Update time_key column
            self.df['time_key'] = [row.time_key for row in self.rows]
            
            # Update time_key_info column
            self.df['time_key_info'] = [row.time_key_info for row in self.rows]
    
    def detect_time_key_granularity(self, key_name: str) -> Optional[str]:
        """
        Detect the most common granularity for a time key across all rows.
        
        Args:
            key_name: The name of the time key to analyze
            
        Returns:
            The most common granularity or None if granularity cannot be determined
        """
        # Get all granularities from rows that have this time key
        granularities = []
        for row in self.rows:
            if row.time_key == key_name and row.time_key_info["granularity"]:
                granularities.append(row.time_key_info["granularity"])
                
        if not granularities:
            return None
            
        # Return the most common granularity
        from collections import Counter
        return Counter(granularities).most_common(1)[0][0]
    
    def analyze_time_series(self, 
                          value_column: str = 'value_b',
                          time_column: str = 'time_key',
                          granularity: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform time-series analysis on the comparison results.
        
        Args:
            value_column: The column to analyze (default: 'value_b')
            time_column: The time column to use (default: 'time_key')
            granularity: Optional granularity override (default: use detected granularity)
            
        Returns:
            Dictionary containing analysis results:
            - trends: Trend analysis results
            - anomalies: Detected anomalies
            - seasonality: Seasonal patterns
            - statistics: Summary statistics
        """
        if time_column not in self.df.columns:
            raise ValueError(f"Time column '{time_column}' not found in DataFrame")
            
        # Get the time series data
        time_series = self.df[[time_column, value_column]].copy()
        time_series = time_series.dropna()
        
        if len(time_series) < 2:
            return {
                'error': 'Insufficient data points for time series analysis',
                'trends': None,
                'anomalies': None,
                'seasonality': None,
                'statistics': None
            }
            
        # Convert time column to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(time_series[time_column]):
            time_series[time_column] = pd.to_datetime(time_series[time_column])
            
        # Sort by time
        time_series = time_series.sort_values(time_column)
        
        # Determine granularity
        if granularity is None:
            # Use the most common granularity from the data
            granularity = self.detect_time_key_granularity(time_column)
            if granularity is None:
                granularity = 'day'  # Default granularity
        
        # Resample data based on granularity
        resampled = time_series.set_index(time_column).resample(granularity)[value_column].agg(['mean', 'std', 'count'])
        
        # Calculate basic statistics
        stats = {
            'mean': resampled['mean'].mean(),
            'std': resampled['std'].mean(),
            'min': resampled['mean'].min(),
            'max': resampled['mean'].max(),
            'range': resampled['mean'].max() - resampled['mean'].min(),
            'granularity': granularity
        }
        
        # Detect trends using linear regression
        x = np.arange(len(resampled))
        y = resampled['mean'].values
        slope, intercept = np.polyfit(x, y, 1)
        trend = {
            'slope': slope,
            'direction': 'increasing' if slope > 0 else 'decreasing',
            'strength': abs(slope) / stats['std'] if stats['std'] > 0 else 0
        }
        
        # Detect anomalies using z-score method
        z_scores = np.abs((resampled['mean'] - stats['mean']) / stats['std'])
        anomalies = resampled[z_scores > 3].index.tolist()
        
        # Detect seasonality
        seasonality = {}
        if len(resampled) >= 4:  # Need at least 4 points for seasonality
            # Calculate autocorrelation
            acf = pd.Series(resampled['mean']).autocorr(lag=1)
            seasonality['autocorrelation'] = acf
            seasonality['has_seasonality'] = abs(acf) > 0.3
            
            # If we have enough data, try to detect the season length
            if len(resampled) >= 12:
                # Calculate autocorrelation for different lags
                acf_lags = [pd.Series(resampled['mean']).autocorr(lag=i) for i in range(1, 13)]
                max_acf_lag = np.argmax(np.abs(acf_lags)) + 1
                seasonality['suggested_period'] = max_acf_lag
        
        return {
            'trends': trend,
            'anomalies': anomalies,
            'seasonality': seasonality,
            'statistics': stats
        }
    
    def get_time_aggregates(self,
                          value_column: str = 'value_b',
                          time_column: str = 'time_key',
                          group_by: List[str] = None) -> pd.DataFrame:
        """
        Get aggregated values grouped by time and optional dimensions.
        
        Args:
            value_column: The column to aggregate (default: 'value_b')
            time_column: The time column to use (default: 'time_key')
            group_by: Additional columns to group by (default: None)
            
        Returns:
            DataFrame with aggregated values
        """
        if time_column not in self.df.columns:
            raise ValueError(f"Time column '{time_column}' not found in DataFrame")
            
        # Prepare grouping columns
        group_cols = [time_column]
        if group_by:
            group_cols.extend(group_by)
            
        # Perform aggregation
        agg_df = self.df.groupby(group_cols)[value_column].agg([
            'count',
            'mean',
            'std',
            'min',
            'max',
            'sum'
        ]).reset_index()
        
        return agg_df
    
    @classmethod
    def from_dataframe(cls, df_a: pd.DataFrame, df_b: pd.DataFrame, keys: List[str], values: List[str], time_keys: Optional[List[str]] = None) -> 'ComparisonResult':
        """
        Create a ComparisonResult from two dataframes.
        
        Args:
            df_a: First dataframe
            df_b: Second dataframe
            keys: List of key columns
            values: List of value columns (fact types)
            time_keys: Optional list of time key columns
            
        Returns:
            ComparisonResult: The comparison result
        """
        # Merge dataframes on keys
        merged_df = pd.merge(df_a, df_b, on=keys, how='outer', suffixes=('_a', '_b'))
        
        # Create rows
        rows = []
        for _, row in merged_df.iterrows():
            # Create key dictionary
            key = {k: row[k] for k in keys}
            
            # Create dimension dictionary from dim_* columns
            dimension = {}
            for col in row.index:
                if col.startswith('dim_'):
                    dimension[col[4:]] = row[col]
            
            # Add time keys to key dictionary
            if time_keys:
                for time_key in time_keys:
                    key[time_key] = row.get(time_key)
            
            # Create rows for each value/fact_type
            for value in values:
                # Get values
                value_a = row.get(f"{value}_a")
                value_b = row.get(f"{value}_b")
                
                # Calculate diff and percent_change
                diff = None
                percent_change = None
                if pd.notna(value_a) and pd.notna(value_b):
                    diff = value_b - value_a
                    if value_a != 0:
                        percent_change = (value_b / value_a - 1) * 100
                
                # Create ComparisonResultRow
                comparison_row = ComparisonResultRow(
                    key=key.copy(),  # Make a copy to avoid shared references
                    dimension=dimension.copy(),
                    fact_type=value,
                    value_a=value_a,
                    value_b=value_b,
                    diff=diff,
                    percent_change=percent_change,
                    time_key=key.get('time_key'),
                    time_key_info={},
                    timestamp=datetime.now()
                )
                
                # Set time key granularity if time keys exist
                if time_keys:
                    for time_key in time_keys:
                        comparison_row.set_time_key_granularity(time_key)
                
                rows.append(comparison_row)
        
        # Create metadata
        metadata = {
            'keys': keys,
            'fact_types': values,  # Store values as fact_types
            'time_keys': time_keys or []
        }
        
        # Create DataFrame with all columns
        df = pd.DataFrame([row.to_dict() for row in rows])
        
        return cls(df=df, rows=rows, metadata=metadata)
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert comparison results to a pandas DataFrame.
        
        Returns:
            DataFrame containing comparison results with both generic and fact_type specific columns
        """
        # Convert rows to dictionaries
        row_dicts = [row.to_dict() for row in self.rows]
        
        # Create DataFrame
        df = pd.DataFrame(row_dicts)
        
        # Get fact types from metadata
        fact_types = self.metadata.get('fact_types', [])
        
        # Ensure all fact_type specific columns exist
        for fact_type in fact_types:
            if fact_type:
                # Add fact_type specific columns if they don't exist
                for suffix in ['_a', '_b', '_diff', '_pct_diff']:
                    col = f"{fact_type}{suffix}"
                    if col not in df.columns:
                        df[col] = None
        
        # Ensure generic columns exist
        generic_cols = ['value_a', 'value_b', 'diff', 'percent_change']
        for col in generic_cols:
            if col not in df.columns:
                df[col] = None
        
        return df
    
    def slice_by_dimension(self, dim_key: str, dim_value: Any) -> 'ComparisonResult':
        """
        Filter results to a specific dimension value.
        
        Args:
            dim_key: Dimension key to filter by
            dim_value: Dimension value to filter by
            
        Returns:
            New ComparisonResult with filtered rows
        """
        # Use the new filter method for backward compatibility
        return self.filter(dimension_filters={dim_key: dim_value})
    
    def filter(self, 
               key_filters: Optional[Dict[str, Any]] = None,
               dimension_filters: Optional[Dict[str, Any]] = None) -> 'ComparisonResult':
        """
        Filter results by keys and/or dimensions with support for various filter types.
        
        Args:
            key_filters: Dictionary of key filters {key_name: filter_value}
                        Filter values can be:
                        - Exact value
                        - List of values (any match)
                        - Range tuple (min, max) for numeric values
                        - Callable function for custom filtering
            dimension_filters: Dictionary of dimension filters {dimension: filter_value}
                             Same filter value types as key_filters
            
        Returns:
            New ComparisonResult with filtered rows
        """
        filtered_rows = self.rows
        
        # Apply key filters if specified
        if key_filters:
            for key, filter_value in key_filters.items():
                filtered_rows = self._apply_filter(filtered_rows, key, filter_value, is_dimension=False)
        
        # Apply dimension filters if specified
        if dimension_filters:
            for dim, filter_value in dimension_filters.items():
                filtered_rows = self._apply_filter(filtered_rows, dim, filter_value, is_dimension=True)
        
        return ComparisonResult(df=self.df, rows=filtered_rows, metadata=self.metadata)
    
    def _apply_filter(self, rows: List['ComparisonResultRow'], field: str, 
                     filter_value: Any, is_dimension: bool = True) -> List['ComparisonResultRow']:
        """
        Apply a filter to a list of rows based on the filter value type.
        
        Args:
            rows: List of rows to filter
            field: Field name to filter by (key or dimension)
            filter_value: Filter value (exact, list, range, or callable)
            is_dimension: Whether the field is a dimension (True) or key (False)
            
        Returns:
            Filtered list of rows
        """
        # Handle different filter value types
        if callable(filter_value):
            # Custom filter function
            return [row for row in rows if filter_value(
                row.dimension.get(field) if is_dimension else row.key.get(field)
            )]
        
        elif isinstance(filter_value, (list, tuple)) and len(filter_value) == 2 and all(isinstance(x, (int, float)) for x in filter_value):
            # Range filter (min, max)
            min_val, max_val = filter_value
            return [row for row in rows if self._is_in_range(
                row.dimension.get(field) if is_dimension else row.key.get(field),
                min_val, max_val
            )]
        
        elif isinstance(filter_value, (list, tuple)):
            # List of values (any match)
            return [row for row in rows if (
                row.dimension.get(field) if is_dimension else row.key.get(field)
            ) in filter_value]
        
        else:
            # Exact value match
            return [row for row in rows if (
                row.dimension.get(field) if is_dimension else row.key.get(field)
            ) == filter_value]
    
    def _is_in_range(self, value: Any, min_val: Union[int, float], max_val: Union[int, float]) -> bool:
        """
        Check if a value is within a numeric range.
        
        Args:
            value: Value to check
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            
        Returns:
            True if value is within range, False otherwise
        """
        if value is None:
            return False
        
        try:
            numeric_value = float(value)
            return min_val <= numeric_value <= max_val
        except (ValueError, TypeError):
            return False
    
    def resolve_filter_rule(self, field: str, filter_rule: Any, is_dimension: bool = True) -> List[Any]:
        """
        Resolve a filter rule into a concrete list of values.
        
        This method is useful for debugging and for creating more complex filters.
        
        Args:
            field: Field name to resolve (key or dimension)
            filter_rule: Filter rule to resolve
            is_dimension: Whether the field is a dimension (True) or key (False)
            
        Returns:
            List of values that match the filter rule
        """
        # Get all unique values for the field
        if is_dimension:
            all_values = {row.dimension.get(field) for row in self.rows if field in row.dimension}
        else:
            all_values = {row.key.get(field) for row in self.rows if field in row.key}
        
        # Remove None values
        all_values = {v for v in all_values if v is not None}
        
        # Handle different filter rule types
        if callable(filter_rule):
            # Custom filter function
            return [v for v in all_values if filter_rule(v)]
        
        elif isinstance(filter_rule, (list, tuple)) and len(filter_rule) == 2 and all(isinstance(x, (int, float)) for x in filter_rule):
            # Range filter (min, max)
            min_val, max_val = filter_rule
            return [v for v in all_values if self._is_in_range(v, min_val, max_val)]
        
        elif isinstance(filter_rule, (list, tuple)):
            # List of values (any match)
            return [v for v in all_values if v in filter_rule]
        
        else:
            # Exact value match
            return [v for v in all_values if v == filter_rule]
    
    def filter_by_fact_type(self, fact_type: str) -> 'ComparisonResult':
        """
        Filter results to a specific fact type.
        
        Args:
            fact_type: Fact type to filter by
            
        Returns:
            New ComparisonResult with filtered rows and filtered DataFrame
        """
        # Filter rows
        filtered_rows = [r for r in self.rows if r.fact_type == fact_type]
        
        # Filter DataFrame
        filtered_df = None
        if 'fact_type' in self.df.columns:
            # If fact_type column exists, filter directly
            filtered_df = self.df[self.df['fact_type'] == fact_type]
        else:
            # If fact_type column doesn't exist, try to filter based on fact_type specific columns
            fact_type_cols = [col for col in self.df.columns if col.startswith(fact_type + '_')]
            if fact_type_cols:
                # Keep fact_type specific columns and non-fact-type columns
                all_fact_types = self.metadata.get('fact_types', [])
                non_fact_type_cols = [col for col in self.df.columns if not any(col.startswith(ft + '_') for ft in all_fact_types)]
                filtered_df = self.df[fact_type_cols + non_fact_type_cols].copy()
                
                # Rename fact_type specific columns to generic names
                rename_map = {
                    f"{fact_type}_a": "value_a",
                    f"{fact_type}_b": "value_b",
                    f"{fact_type}_diff": "diff",
                    f"{fact_type}_pct_diff": "percent_change"
                }
                filtered_df = filtered_df.rename(columns=rename_map)
                
                # Add fact_type column
                filtered_df['fact_type'] = fact_type
            else:
                # If no fact_type specific columns, keep the original DataFrame
                filtered_df = self.df.copy()
                filtered_df['fact_type'] = fact_type
        
        # Update metadata
        metadata = self.metadata.copy()
        metadata['current_fact_type'] = fact_type
        
        return ComparisonResult(df=filtered_df, rows=filtered_rows, metadata=metadata)
    
    def group_aggregate_by_dimension(self, by: str, metric: str = "diff", agg: str = "sum") -> pd.DataFrame:
        """
        Group and aggregate results by a dimension.
        
        Args:
            by: Dimension key to group by
            metric: Metric to aggregate (default: "diff")
            agg: Aggregation function (default: "sum")
            
        Returns:
            DataFrame with aggregated results
        """
        df = self.to_dataframe()
        if by not in df.columns:
            df[by] = df["dimension"].apply(lambda d: d.get(by))
        return df.groupby(by)[metric].agg(agg).reset_index()
    
    def summarize_by_fact_type(self) -> pd.DataFrame:
        """
        Generate summary statistics by fact type.
        
        Returns:
            DataFrame with summary statistics by fact type
        """
        df = self.to_dataframe()
        return df.groupby("fact_type")["diff"].agg(["mean", "std", "count"]).reset_index()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Calculate summary statistics for the comparison results.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.rows:
            return {}
        
        diffs = [row.diff for row in self.rows if row.diff is not None]
        percent_changes = [row.percent_change for row in self.rows if row.percent_change is not None]
        
        return {
            "total_comparisons": len(self.rows),
            "mean_diff": np.mean(diffs) if diffs else None,
            "median_diff": np.median(diffs) if diffs else None,
            "mean_percent_change": np.mean(percent_changes) if percent_changes else None,
            "median_percent_change": np.median(percent_changes) if percent_changes else None,
            "max_diff": max(diffs) if diffs else None,
            "min_diff": min(diffs) if diffs else None
        }
    
    def get_dimension_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate statistics by dimension.
        
        Returns:
            Dictionary mapping dimensions to their statistics
        """
        if not self.rows:
            return {}
        
        # Group rows by dimension
        dimension_groups = {}
        for row in self.rows:
            for dim_key, dim_value in row.dimension.items():
                if dim_key not in dimension_groups:
                    dimension_groups[dim_key] = {}
                if dim_value not in dimension_groups[dim_key]:
                    dimension_groups[dim_key][dim_value] = []
                dimension_groups[dim_key][dim_value].append(row)
        
        # Calculate stats for each dimension
        stats = {}
        for dim_key, dim_values in dimension_groups.items():
            stats[dim_key] = {}
            for dim_value, rows in dim_values.items():
                diffs = [row.diff for row in rows if row.diff is not None]
                percent_changes = [row.percent_change for row in rows if row.percent_change is not None]
                
                stats[dim_key][dim_value] = {
                    "total_comparisons": len(rows),
                    "mean_diff": np.mean(diffs) if diffs else None,
                    "median_diff": np.median(diffs) if diffs else None,
                    "mean_percent_change": np.mean(percent_changes) if percent_changes else None,
                    "median_percent_change": np.median(percent_changes) if percent_changes else None,
                    "max_diff": max(diffs) if diffs else None,
                    "min_diff": min(diffs) if diffs else None
                }
        
        return stats
        
    def enrich_dimensions(self, dimension_mappings: Dict[str, Dict[str, Any]]) -> None:
        """
        Enrich all rows with dimensional information based on mapping files.
        
        This method applies the dimension mappings to all rows in the comparison result,
        populating the dimension field with enriched key values.
        
        Args:
            dimension_mappings: Dictionary mapping key names to enrichment configurations
                Each configuration should include:
                - key_column: The original key column to enrich
                - enriched_key: The name of the enriched dimension
                - default_value: Value to use for unmapped keys (defaults to "Unknown")
                - mappings: Dictionary mapping original key values to enriched values
        """
        for row in self.rows:
            row.enrich_dimensions(dimension_mappings)
            
        # Update metadata to include dimension enrichment information
        if "dimension_enrichment" not in self.metadata:
            self.metadata["dimension_enrichment"] = {}
            
        self.metadata["dimension_enrichment"].update({
            "timestamp": datetime.now(),
            "mappings": dimension_mappings
        })

    def analyze_dimension(self, 
                         fact_type: Optional[str] = None,
                         dimension_filters: Optional[Dict[str, Any]] = None,
                         key_filters: Optional[Dict[str, Any]] = None,
                         group_by: Optional[str] = None,
                         metric: str = "diff",
                         agg: str = "sum",
                         aggregate_first: bool = False) -> pd.DataFrame:
        """
        Perform dimensional analysis on comparison results with filtering and aggregation.
        
        Args:
            fact_type: Optional fact type to filter by (e.g., "forecast_value_p50")
            dimension_filters: Optional dictionary of dimension filters {dimension: value}
                             Filter values can be:
                             - Exact value
                             - List of values (any match)
                             - Range tuple (min, max) for numeric values
                             - Callable function for custom filtering
            key_filters: Optional dictionary of key filters {key: value}
                        Same filter value types as dimension_filters
            group_by: Optional dimension to group by (e.g., "match_status")
            metric: Metric to calculate (default: "diff")
            agg: Aggregation function (default: "sum")
            aggregate_first: If True, aggregate raw values first, then calculate metric.
                           If False, calculate metric for each row, then aggregate.
            
        Returns:
            DataFrame with analysis results, including count information
        """
        # Start with all rows
        filtered_result = self
        
        # Apply fact type filter if specified
        if fact_type:
            filtered_result = filtered_result.filter_by_fact_type(fact_type)
        
        # Apply dimension and key filters if specified
        if dimension_filters or key_filters:
            filtered_result = filtered_result.filter(
                key_filters=key_filters,
                dimension_filters=dimension_filters
            )
        
        # If grouping is specified, aggregate by the dimension
        if group_by:
            if aggregate_first:
                # Convert to DataFrame for easier manipulation
                df = filtered_result.to_dataframe()
                
                # Extract the grouping dimension
                if group_by not in df.columns:
                    df[group_by] = df["dimension"].apply(lambda d: d.get(group_by))
                
                # Group by the dimension
                grouped = df.groupby(group_by)
                
                # Create result DataFrame with the group_by column
                result_df = pd.DataFrame({group_by: grouped.groups.keys()})
                
                # Add count column to track the number of rows in each group
                result_df["count"] = result_df[group_by].apply(lambda x: len(grouped.get_group(x)))
                
                # Handle each match_status separately to avoid NaN issues
                for status in result_df[group_by]:
                    # Filter rows for this status
                    status_df = df[df[group_by] == status]
                    
                    # Skip if no rows for this status
                    if len(status_df) == 0:
                        continue
                    
                    # For missing_in_a, value_a is NaN, so diff is -value_b
                    if status == 'missing_in_a':
                        if metric == "diff":
                            result_df.loc[result_df[group_by] == status, "diff"] = -status_df["value_b"].sum()
                        elif metric == "percent_change":
                            result_df.loc[result_df[group_by] == status, "percent_change"] = -100  # 100% decrease
                    
                    # For missing_in_b, value_b is NaN, so diff is value_a
                    elif status == 'missing_in_b':
                        if metric == "diff":
                            result_df.loc[result_df[group_by] == status, "diff"] = status_df["value_a"].sum()
                        elif metric == "percent_change":
                            result_df.loc[result_df[group_by] == status, "percent_change"] = 100  # 100% increase
                    
                    # For missing_in_both, both values are NaN, so diff is 0
                    elif status == 'missing_in_both':
                        if metric == "diff":
                            result_df.loc[result_df[group_by] == status, "diff"] = 0
                        elif metric == "percent_change":
                            result_df.loc[result_df[group_by] == status, "percent_change"] = 0
                    
                    # For present_in_both, calculate normally
                    elif status == 'present_in_both':
                        # Filter out rows with NaN values
                        valid_df = status_df.dropna(subset=["value_a", "value_b"])
                        
                        if len(valid_df) > 0:
                            # Aggregate value_a and value_b separately
                            agg_a = valid_df["value_a"].agg(agg)
                            agg_b = valid_df["value_b"].agg(agg)
                            
                            # Calculate metrics based on aggregated values
                            if metric == "diff":
                                result_df.loc[result_df[group_by] == status, "diff"] = agg_b - agg_a
                            elif metric == "percent_change":
                                # Handle division by zero
                                if agg_a != 0:
                                    result_df.loc[result_df[group_by] == status, "percent_change"] = (agg_b / agg_a - 1) * 100
                                else:
                                    result_df.loc[result_df[group_by] == status, "percent_change"] = np.inf if agg_b > 0 else 0
                
                return result_df
            else:
                # Original approach: calculate metric for each row, then aggregate
                df = filtered_result.to_dataframe()
                
                # Extract the grouping dimension
                if group_by not in df.columns:
                    df[group_by] = df["dimension"].apply(lambda d: d.get(group_by))
                
                # Group by the dimension
                grouped = df.groupby(group_by)
                
                # Create result DataFrame with the group_by column and count
                result_df = pd.DataFrame({group_by: grouped.groups.keys()})
                result_df["count"] = result_df[group_by].apply(lambda x: len(grouped.get_group(x)))
                
                # Add the metric column
                result_df[metric] = grouped[metric].agg(agg)
                
                return result_df
        
        # If no grouping, return summary statistics
        if aggregate_first:
            # Calculate aggregated metrics
            df = filtered_result.to_dataframe()
            
            # Filter out rows with NaN values
            valid_df = df.dropna(subset=["value_a", "value_b"])
            
            # Create result with count information
            result = {"count": len(valid_df)}
            
            if len(valid_df) > 0:
                agg_a = valid_df["value_a"].agg(agg)
                agg_b = valid_df["value_b"].agg(agg)
                
                if metric == "diff":
                    result["diff"] = agg_b - agg_a
                elif metric == "percent_change":
                    result["percent_change"] = (agg_b / agg_a - 1) * 100 if agg_a != 0 else np.inf
                else:
                    result[metric] = valid_df[metric].agg(agg)
            else:
                # If no valid rows, return empty result with count
                result.update({"diff": 0, "percent_change": 0})
                
            return pd.DataFrame([result])
        else:
            # Original approach with count added
            stats = filtered_result.get_summary_stats()
            stats["count"] = len(filtered_result.rows)
            return pd.DataFrame([stats]) 