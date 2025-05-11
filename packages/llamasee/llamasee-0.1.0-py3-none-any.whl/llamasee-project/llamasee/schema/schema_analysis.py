"""
Schema analysis for LlamaSee.

This module provides functionality for automatically detecting and classifying
columns in datasets as keys, values, or dimensions. It implements a more robust
and modular approach to schema analysis than the previous implementation.
"""

from typing import Dict, List, Tuple, Any, Optional, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum
import logging

class ColumnType(Enum):
    """Enumeration of column types."""
    KEY = "key"
    VALUE = "value"
    DIMENSION = "dimension"
    UNKNOWN = "unknown"

@dataclass
class ColumnInfo:
    """Information about a column in a dataset."""
    name: str
    dtype: str
    unique_count: int
    null_count: int
    cardinality_ratio: float
    numeric_ratio: float
    column_type: ColumnType
    stats: Dict[str, Any]
    metadata: Dict[str, Any]  # Additional metadata like name patterns, etc.

class SchemaAnalyzer:
    """
    Analyzes and classifies columns in datasets.
    
    This class uses statistical analysis and heuristics to automatically
    identify key columns, value columns, and dimensions in datasets.
    """
    
    def __init__(self, 
                 key_cardinality_threshold: float = 0.2,
                 value_numeric_threshold: float = 0.5,
                 dimension_cardinality_threshold: float = 0.2,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize the schema analyzer.
        
        Args:
            key_cardinality_threshold: Minimum unique ratio for key columns
            value_numeric_threshold: Minimum numeric ratio for value columns
            dimension_cardinality_threshold: Maximum unique ratio for dimension columns
            logger: Optional logger instance
        """
        self.key_cardinality_threshold = key_cardinality_threshold
        self.value_numeric_threshold = value_numeric_threshold
        self.dimension_cardinality_threshold = dimension_cardinality_threshold
        self.logger = logger or logging.getLogger(__name__)
        
        # Common patterns for column classification
        self.key_patterns = ['id', 'key', 'code', 'ref', 'sku', 'name', 'category', 'type', 'region', 'location']
        self.value_patterns = ['value', 'amount', 'price', 'cost', 'revenue', 'sales', 'quantity', 'count', 'p10', 'p50', 'p90']
        self.date_patterns = ['date', 'period', 'time', 'year', 'month', 'week', 'day', 'quarter', 'fiscal']
    
    def analyze_column(self, df: pd.DataFrame, column: str, analyze_non_zero: bool = True) -> ColumnInfo:
        """
        Analyze a single column in a dataset.
        
        Args:
            df: DataFrame containing the column
            column: Name of the column to analyze
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            
        Returns:
            ColumnInfo object with column analysis
        """
        # Get basic column information
        series = df[column]
        dtype = str(series.dtype)
        total_rows = len(df)
        unique_count = series.nunique()
        null_count = series.isnull().sum()
        
        # Calculate ratios
        cardinality_ratio = unique_count / total_rows if total_rows > 0 else 0
        numeric_ratio = pd.to_numeric(series, errors='coerce').notna().mean()
        
        # Check naming patterns
        name_metadata = {
            "is_key_name": any(key_term in column.lower() for key_term in self.key_patterns),
            "is_value_name": any(value_term in column.lower() for value_term in self.value_patterns),
            "is_date_name": any(date_term in column.lower() for date_term in self.date_patterns),
            "is_forecast_value": 'forecast_value' in column.lower()
        }
        
        # Calculate statistics
        stats = {
            "min": series.min() if numeric_ratio > 0 else None,
            "max": series.max() if numeric_ratio > 0 else None,
            "mean": series.mean() if numeric_ratio > 0 else None,
            "median": series.median() if numeric_ratio > 0 else None,
            "std": series.std() if numeric_ratio > 0 else None,
            "most_common": series.value_counts().head(5).to_dict()
        }
        
        # For numeric columns, analyze non-zero values separately if requested
        non_zero_stats = {}
        if analyze_non_zero and numeric_ratio > 0:
            # Count zeros in the column
            zero_count = (series == 0).sum()
            zero_ratio = zero_count / total_rows if total_rows > 0 else 0
            
            # Get non-zero values
            non_zero_values = series[series != 0]
            non_zero_count = len(non_zero_values)
            
            if non_zero_count > 0:
                # Calculate cardinality for non-zero values
                non_zero_unique_count = non_zero_values.nunique()
                non_zero_cardinality_ratio = non_zero_unique_count / non_zero_count
                
                non_zero_stats = {
                    "zero_count": zero_count,
                    "zero_ratio": zero_ratio,
                    "non_zero_count": non_zero_count,
                    "non_zero_unique_count": non_zero_unique_count,
                    "non_zero_cardinality_ratio": non_zero_cardinality_ratio,
                    "non_zero_is_value_like": non_zero_cardinality_ratio > 0.5 or non_zero_unique_count > 50
                }
        
        # Combine all metadata
        metadata = {
            **name_metadata,
            "non_zero_stats": non_zero_stats
        }
        
        # Determine column type
        column_type = self._determine_column_type(
            cardinality_ratio, 
            numeric_ratio, 
            unique_count,
            metadata
        )
        
        return ColumnInfo(
            name=column,
            dtype=dtype,
            unique_count=unique_count,
            null_count=null_count,
            cardinality_ratio=cardinality_ratio,
            numeric_ratio=numeric_ratio,
            column_type=column_type,
            stats=stats,
            metadata=metadata
        )
    
    def _determine_column_type(self, 
                             cardinality_ratio: float, 
                             numeric_ratio: float,
                             unique_count: int,
                             metadata: Dict[str, Any]) -> ColumnType:
        """
        Determine the type of a column based on its characteristics.
        
        Args:
            cardinality_ratio: Ratio of unique values to total values
            numeric_ratio: Ratio of numeric values to total values
            unique_count: Number of unique values
            metadata: Additional metadata about the column
            
        Returns:
            ColumnType enum value
        """
        # Check for date columns first - they should be keys
        if metadata.get("is_date_name", False):
            return ColumnType.KEY
        
        # Check for key columns
        if ((metadata.get("non_zero_stats", {}).get("non_zero_cardinality_ratio", cardinality_ratio) <= self.key_cardinality_threshold or 
            metadata.get("is_key_name", False))):
            return ColumnType.KEY
        
        # Check for value columns
        if ((numeric_ratio >= self.value_numeric_threshold and 
             metadata.get("is_value_name", False)) or
            metadata.get("is_forecast_value", False) or
            (metadata.get("non_zero_stats", {}).get("non_zero_is_value_like", False) and
             numeric_ratio > 0)):
            return ColumnType.VALUE
        
        # Check for dimension columns
        if (cardinality_ratio <= self.dimension_cardinality_threshold and 
            unique_count > 1):
            return ColumnType.DIMENSION
        
        return ColumnType.UNKNOWN
    
    def detect_schema(self, df: pd.DataFrame, analyze_non_zero: bool = True) -> Dict[ColumnType, List[str]]:
        """
        Detect the schema of a dataset.
        
        Args:
            df: DataFrame to analyze
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            
        Returns:
            Dictionary mapping column types to lists of column names
        """
        schema = {
            ColumnType.KEY: [],
            ColumnType.VALUE: [],
            ColumnType.DIMENSION: [],
            ColumnType.UNKNOWN: []
        }
        
        # Analyze each column
        for column in df.columns:
            column_info = self.analyze_column(df, column, analyze_non_zero)
            schema[column_info.column_type].append(column)
            self.logger.debug(f"Column {column} classified as {column_info.column_type.value}")
        
        return schema
    
    def detect_potential_keys(self, df: pd.DataFrame, threshold: float = 0.2) -> List[str]:
        """
        Detect potential key columns based on cardinality and naming patterns.
        
        Args:
            df: DataFrame to analyze
            threshold: Cardinality threshold (0-1) to consider a column as a potential key
            
        Returns:
            List of potential key column names
        """
        # Check if we already have schema analysis for this DataFrame
        df_id = id(df)
        if hasattr(self, '_schema_cache') and df_id in self._schema_cache:
            schema = self._schema_cache[df_id]
        else:
            # Temporarily adjust the threshold
            original_threshold = self.key_cardinality_threshold
            self.key_cardinality_threshold = threshold
            
            # Detect schema
            schema = self.detect_schema(df)
            
            # Cache the schema analysis
            if not hasattr(self, '_schema_cache'):
                self._schema_cache = {}
            self._schema_cache[df_id] = schema
            
            # Restore the original threshold
            self.key_cardinality_threshold = original_threshold
        
        # Return potential keys
        return schema[ColumnType.KEY]
    
    def detect_time_granularity(self, df: pd.DataFrame, time_key: str) -> Optional[str]:
        """
        Detect the granularity of a time key based on its values.
        
        Args:
            df: DataFrame containing the time key
            time_key: Name of the time key column
            
        Returns:
            Detected granularity ('hour', 'day', 'week', 'month', 'year') or None if cannot be determined
        """
        if time_key not in df.columns:
            self.logger.warning(f"Time key {time_key} not found in DataFrame")
            return None
            
        try:
            # Convert to datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(df[time_key]):
                df[time_key] = pd.to_datetime(df[time_key])
            
            # Get sample of non-null values
            sample = df[time_key].dropna().head(100)
            if len(sample) < 2:
                return None
                
            # Calculate time differences
            diffs = sample.diff().dropna()
            if len(diffs) == 0:
                return None
                
            # Get most common difference
            most_common_diff = diffs.mode().iloc[0]
            diff_hours = most_common_diff.total_seconds() / 3600
            
            # Determine granularity
            if diff_hours < 2:
                return 'hour'
            elif diff_hours < 72:  # Changed from 24 to 72 hours
                return 'day'
            elif diff_hours < 168:  # 7 days
                return 'week'
            elif diff_hours < 720:  # 30 days
                return 'month'
            else:
                return 'year'
                
        except Exception as e:
            self.logger.warning(f"Error detecting time granularity for {time_key}: {str(e)}")
            return None

    def validate_time_key(self, df: pd.DataFrame, time_key: str, expected_granularity: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a time key's format and granularity.
        
        Args:
            df: DataFrame containing the time key
            time_key: Name of the time key column
            expected_granularity: Optional expected granularity to validate against
            
        Returns:
            Dictionary containing validation results and metadata
        """
        validation = {
            "is_valid": False,
            "granularity": None,
            "errors": [],
            "metadata": {}
        }
        
        try:
            # Check if column exists
            if time_key not in df.columns:
                validation["errors"].append(f"Time key {time_key} not found in DataFrame")
                return validation
                
            # Convert to datetime
            try:
                df[time_key] = pd.to_datetime(df[time_key])
            except Exception as e:
                validation["errors"].append(f"Could not convert {time_key} to datetime: {str(e)}")
                return validation
                
            # Detect granularity
            detected_granularity = self.detect_time_granularity(df, time_key)
            validation["granularity"] = detected_granularity
            
            # Validate against expected granularity if provided
            if expected_granularity and detected_granularity != expected_granularity:
                validation["errors"].append(
                    f"Detected granularity '{detected_granularity}' does not match expected '{expected_granularity}'"
                )
            
            # Add metadata
            validation["metadata"] = {
                "min_date": df[time_key].min(),
                "max_date": df[time_key].max(),
                "unique_dates": df[time_key].nunique(),
                "null_count": df[time_key].isnull().sum()
            }
            
            validation["is_valid"] = len(validation["errors"]) == 0
            return validation
            
        except Exception as e:
            validation["errors"].append(f"Error validating time key: {str(e)}")
            return validation

    def detect_time_keys(self, df: pd.DataFrame, key_columns: Optional[List[str]] = None) -> List[str]:
        """
        Detect time-related key columns based on naming patterns and data types.
        
        Args:
            df: DataFrame to analyze
            key_columns: Optional list of key columns to check. If None, checks all columns.
            
        Returns:
            List of detected time key column names
        """
        time_keys = []
        columns_to_check = key_columns if key_columns is not None else df.columns
        
        for column in columns_to_check:
            # Check if column name contains date-related terms
            if any(term in column.lower() for term in ['date', 'time', 'day', 'month', 'year', 'period']):
                # Validate the time key
                validation = self.validate_time_key(df, column)
                if validation["is_valid"]:
                    time_keys.append(column)
                    self.logger.debug(f"Detected time key: {column} (granularity: {validation['granularity']})")
                else:
                    self.logger.debug(f"Column {column} has time-related name but failed validation: {validation['errors']}")
            
            # Check if column is already datetime type
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                validation = self.validate_time_key(df, column)
                if validation["is_valid"]:
                    time_keys.append(column)
                    self.logger.debug(f"Detected time key from datetime type: {column} (granularity: {validation['granularity']})")
        
        return time_keys
    
    def convert_time_keys_to_datetime(self, df: pd.DataFrame, time_keys: List[str]) -> Tuple[pd.DataFrame, List[str]]:
        """
        Convert time key columns to datetime format.
        
        Args:
            df: DataFrame containing the time keys
            time_keys: List of time key column names to convert
            
        Returns:
            Tuple containing:
            - DataFrame with converted time key columns
            - Updated list of valid time keys (removing those that failed conversion)
        """
        result_df = df.copy()
        valid_time_keys = []
        
        for column in time_keys:
            if column in result_df.columns:
                try:
                    # Try to convert to datetime
                    result_df[column] = pd.to_datetime(result_df[column])
                    self.logger.debug(f"Converted time key column '{column}' to datetime format")
                    valid_time_keys.append(column)
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Could not convert time key column '{column}' to datetime: {str(e)}")
                    self.logger.warning(f"Column '{column}' will not be used for time-series analysis")
                    # Keep the original column if conversion fails
                    # The column will be removed from the time_keys list
        
        return result_df, valid_time_keys
    
    def detect_potential_values(self, df: pd.DataFrame, exclude_keys: List[str] = None) -> List[str]:
        """
        Detect potential value columns based on data type and naming patterns.
        
        Args:
            df: DataFrame to analyze
            exclude_keys: List of column names to exclude from value detection
            
        Returns:
            List of potential value column names
        """
        # Check if we already have schema analysis for this DataFrame
        df_id = id(df)
        if hasattr(self, '_schema_cache') and df_id in self._schema_cache:
            schema = self._schema_cache[df_id]
        else:
            # Detect schema
            schema = self.detect_schema(df)
            
            # Cache the schema analysis
            if not hasattr(self, '_schema_cache'):
                self._schema_cache = {}
            self._schema_cache[df_id] = schema
        
        # Get potential values, excluding any specified keys
        potential_values = schema[ColumnType.VALUE]
        if exclude_keys:
            potential_values = [col for col in potential_values if col not in exclude_keys]
        
        return potential_values
    
    def suggest_comparison_columns(self, 
                                 df_a: pd.DataFrame, 
                                 df_b: pd.DataFrame,
                                 key_threshold: float = 0.95,
                                 value_threshold: float = 0.1,
                                 analyze_non_zero: bool = True) -> Tuple[List[str], List[str], List[str]]:
        """
        Suggest columns for comparison between two datasets.
        
        Args:
            df_a: First DataFrame
            df_b: Second DataFrame
            key_threshold: Cardinality threshold for key detection
            value_threshold: Cardinality threshold for value detection
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            
        Returns:
            Tuple of (key_columns, value_columns, dimension_columns)
        """
        # Detect potential keys in both datasets
        keys_a = self.detect_potential_keys(df_a, threshold=key_threshold)
        keys_b = self.detect_potential_keys(df_b, threshold=key_threshold)
        
        # Find common keys
        common_keys = list(set(keys_a) & set(keys_b))
        
        # Detect potential values in both datasets
        values_a = self.detect_potential_values(df_a, exclude_keys=common_keys)
        values_b = self.detect_potential_values(df_b, exclude_keys=common_keys)
        
        # Find common values
        common_values = list(set(values_a) & set(values_b))
        
        # Detect dimensions
        dimensions_a = self.detect_schema(df_a)[ColumnType.DIMENSION]
        dimensions_b = self.detect_schema(df_b)[ColumnType.DIMENSION]
        
        # Find common dimensions
        common_dimensions = list(set(dimensions_a) & set(dimensions_b))
        
        return common_keys, common_values, common_dimensions
    
    def auto_detect_comparison_structure(self, 
                                       df_a: pd.DataFrame, 
                                       df_b: pd.DataFrame,
                                       key_threshold: float = 0.95, 
                                       value_threshold: float = 0.1,
                                       analyze_non_zero: bool = True,
                                       exclude_keys_from_values: bool = True) -> Tuple[List[str], List[str], List[str]]:
        """
        Automatically detect keys, values, and time keys for comparison.
        
        Args:
            df_a: First DataFrame
            df_b: Second DataFrame
            key_threshold: Cardinality threshold for key detection
            value_threshold: Cardinality threshold for value detection
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            exclude_keys_from_values: Whether to exclude detected keys from values
            
        Returns:
            Tuple of (detected_keys, detected_values, detected_time_keys)
        """
        self.logger.info("Automatically detecting comparison structure...")
        
        # Detect potential keys
        detected_keys = self.detect_potential_keys(df_a, threshold=key_threshold)
        
        # Detect time keys (only from key columns)
        detected_time_keys = self.detect_time_keys(df_a, key_columns=detected_keys)
        
        # Add time keys to detected keys if not already included
        for time_key in detected_time_keys:
            if time_key not in detected_keys:
                detected_keys.append(time_key)
                self.logger.debug(f"Added time key: {time_key}")
        
        # Detect potential values
        detected_values = self.detect_potential_values(
            df_a, 
            exclude_keys=detected_keys if exclude_keys_from_values else None
        )
        
        self.logger.info(f"Automatically detected {len(detected_keys)} keys, {len(detected_values)} values, and {len(detected_time_keys)} time keys")
        
        return detected_keys, detected_values, detected_time_keys
    
    def validate_comparison_columns(self,
                                  df_a: pd.DataFrame,
                                  df_b: pd.DataFrame,
                                  keys: List[str],
                                  values: List[str],
                                  dimensions: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Validate column selections for comparison.
        
        Args:
            df_a: First DataFrame
            df_b: Second DataFrame
            keys: Selected key columns
            values: Selected value columns
            dimensions: Optional dimension columns
            
        Returns:
            Dictionary of validation errors by column type
        """
        errors = {
            "keys": [],
            "values": [],
            "dimensions": []
        }
        
        # Validate keys
        for key in keys:
            if key not in df_a.columns or key not in df_b.columns:
                errors["keys"].append(f"Key column {key} not found in both datasets")
            elif df_a[key].dtype != df_b[key].dtype:
                errors["keys"].append(f"Key column {key} has mismatched types")
        
        # Validate values
        for value in values:
            if value not in df_a.columns or value not in df_b.columns:
                errors["values"].append(f"Value column {value} not found in both datasets")
            elif not (pd.api.types.is_numeric_dtype(df_a[value]) and 
                     pd.api.types.is_numeric_dtype(df_b[value])):
                errors["values"].append(f"Value column {value} is not numeric in both datasets")
        
        # Validate dimensions
        if dimensions:
            for dim in dimensions:
                if dim not in df_a.columns or dim not in df_b.columns:
                    errors["dimensions"].append(f"Dimension column {dim} not found in both datasets")
                elif df_a[dim].dtype != df_b[dim].dtype:
                    errors["dimensions"].append(f"Dimension column {dim} has mismatched types")
        
        return errors
    
    def define_dimensions(self, df: pd.DataFrame, keys: List[str]) -> Dict[str, Any]:
        """
        Define dimensions based on key columns and their unique values.
        
        Args:
            df: DataFrame containing the data
            keys: List of key columns to use for dimension definition
            
        Returns:
            Dictionary containing dimension definitions
        """
        try:
            if not keys:
                self.logger.warning("No key columns defined. Cannot define dimensions.")
                return {}
                
            dimensions = {}
            for i, key_col in enumerate(keys):
                self.logger.debug(f"Processing key column: {key_col}")
                
                # Find unique values for this key
                unique_values = sorted(df[key_col].unique().tolist())
                self.logger.debug(f"Found {len(unique_values)} unique values for {key_col}")
                
                # Create dimension definition
                dimension_id = f"dim_{i+1}"
                dimensions[dimension_id] = {
                    "key": key_col,
                    "values": unique_values
                }
                
                self.logger.debug(f"Created dimension {dimension_id} for key {key_col}")
                
            return dimensions
            
        except Exception as e:
            self.logger.error(f"Error defining dimensions: {str(e)}")
            raise 