import pandas as pd
import numpy as np
import uuid
from typing import Dict, Any, List, Optional, Set, Tuple, Union, final
import logging
import json
import csv
import traceback
from datetime import datetime
from .dimension import DimensionConfig
from .data_loader import DataLoader
from .insight_config import InsightConfig, default_config
from .core.insight import Insight
from .llm.enhancer import LLMInsightEnhancer
from .utils.trace import TraceManager
from .analysis.metadata import MetadataAnalyzer
from .utils.logger import get_logger
from .utils.stage_logger import StageLogger, StageManager
from .llm.adapters.factory import LLMAdapterFactory
from .generation.insight_generator import InsightGenerator
import os
from llamasee.schema.comparison import ComparisonResult, ComparisonResultRow
from .export import ExporterFactory
from .schema import SchemaAnalyzer, ColumnType
from .storage import InsightStorage
from .analysis.data_quality import DataQualityAnalyzer
from .schema.key_enricher import KeyEnricher

class LlamaSee:
    """
    Main class for LlamaSee data comparison and insight generation.
    """
    def __init__(self, metadata_a: Dict[str, Any], data_a: Any,
                 metadata_b: Dict[str, Any], data_b: Any,
                 context: Optional[Dict[str, Any]] = None,
                 verbose: bool = False,
                 insight_config: Optional[Dict[str, Any]] = None,
                 llm_enhancer: Optional[Any] = None,
                 log_level: str = "INFO"):
        """Initialize LlamaSee with two datasets and their metadata."""
        self.metadata_a = metadata_a
        self.data_a = data_a
        self.metadata_b = metadata_b
        self.data_b = data_b
        self.context = context or {}
        self.verbose = verbose
        self.insight_config = insight_config or InsightConfig()
        self.llm_enhancer = llm_enhancer
                # Set up logging
        self.logger = get_logger("llamasee.llamasee")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Initialize components
        self.trace_manager = TraceManager()
        self.metadata_analyzer = MetadataAnalyzer()
        self.schema_analyzer = SchemaAnalyzer(logger=self.logger)
        self.insight_storage = InsightStorage()
        self.data_quality_analyzer = DataQualityAnalyzer(logger=self.logger)
        
        # Initialize plugin manager
        from .plugins.manager import PluginManager
        self.plugin_manager = PluginManager()
        
        # Initialize comparison structure
        self.keys = []
        self.values = []
        self._dimensions = set()  # Renamed to _dimensions to indicate it's deprecated
        self.aggregation_levels = {}
        
        # Initialize analysis results
        self._key_analysis = {}
        self._value_analysis = {}
        self._dimension_analysis = {}
        self._comparison_results = None
        self._insights = []
        
        # Initialize stage tracking
        self._current_stage = None
        self._stage_status = {}
        
        
        # Initialize stage manager
        self.stage_manager = StageManager()
        
        # Register stages
        self.stages = {
            "prepare": StageLogger("prepare"),
            "fit": StageLogger("fit"),
            "compare": StageLogger("compare"),
            "generate_insights": StageLogger("generate_insights"),
            "export_results": StageLogger("export_results")
        }
        
        for stage_name, stage_logger in self.stages.items():
            self.stage_manager.register_stage(stage_name, stage_logger)
  
    @property
    def dimensions(self):
        """
        DEPRECATED: The dimensions attribute is deprecated and will be removed in a future version.
        Please use enriched keys instead.
        
        Returns:
            The dimensions set.
        """
        import warnings
        warnings.warn(
            "The 'dimensions' attribute is deprecated and will be removed in a future version. "
            "Please use enriched keys instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._dimensions
        
    @dimensions.setter
    def dimensions(self, value):
        """
        DEPRECATED: The dimensions attribute is deprecated and will be removed in a future version.
        Please use enriched keys instead.
        
        Args:
            value: The value to set.
        """
        import warnings
        warnings.warn(
            "The 'dimensions' attribute is deprecated and will be removed in a future version. "
            "Please use enriched keys instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._dimensions = value
    
    def auto_detect_comparison_structure(self, 
                                       key_threshold: float = 0.95, 
                                       value_threshold: float = 0.1,
                                       analyze_non_zero: bool = True,
                                       exclude_keys_from_values: bool = True) -> Tuple[List[str], List[str]]:
        """
        Automatically detect keys and values for comparison.
        
        Args:
            key_threshold: Cardinality threshold for key detection
            value_threshold: Cardinality threshold for value detection
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            exclude_keys_from_values: Whether to exclude detected keys from values
            
        Returns:
            Tuple of (detected_keys, detected_values)
        """
        try:
            detected_keys, detected_values = self.schema_analyzer.auto_detect_comparison_structure(
                self.data_a,
                self.data_b,
                key_threshold=key_threshold,
                value_threshold=value_threshold,
                analyze_non_zero=analyze_non_zero,
                exclude_keys_from_values=exclude_keys_from_values
            )
            
            # Store the detected structure
            self._key_analysis["detected_keys"] = detected_keys
            self._value_analysis["detected_values"] = detected_values
            
            return detected_keys, detected_values
        except Exception as e:
            self.logger.error(f"Error auto-detecting comparison structure: {str(e)}")
            raise
    
    def validate_comparison_columns(self,
                                  keys: List[str],
                                  values: List[str],
                                  dimensions: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Validate column selections for comparison.
        
        Args:
            keys: Selected key columns
            values: Selected value columns
            dimensions: Optional dimension columns
            
        Returns:
            Dictionary of validation errors by column type
        """
        try:
            errors = self.schema_analyzer.validate_comparison_columns(
                self.data_a,
                self.data_b,
                keys=keys,
                values=values,
                dimensions=dimensions
            )
            return errors
        except Exception as e:
            self.logger.error(f"Error validating comparison columns: {str(e)}")
            raise
    
    def suggest_comparison_columns(self,
                                 key_threshold: float = 0.95,
                                 value_threshold: float = 0.1,
                                 analyze_non_zero: bool = True) -> Tuple[List[str], List[str], List[str]]:
        """
        Suggest columns for comparison between the two datasets.
        
        Args:
            key_threshold: Cardinality threshold for key detection
            value_threshold: Cardinality threshold for value detection
            analyze_non_zero: Whether to analyze non-zero values separately for numeric columns
            
        Returns:
            Tuple of (key_columns, value_columns, dimension_columns)
        """
        try:
            keys, values, dimensions = self.schema_analyzer.suggest_comparison_columns(
                self.data_a,
                self.data_b,
                key_threshold=key_threshold,
                value_threshold=value_threshold,
                analyze_non_zero=analyze_non_zero
            )
            return keys, values, dimensions
        except Exception as e:
            self.logger.error(f"Error suggesting comparison columns: {str(e)}")
            raise

    def set_dimensions(self, dimensions: Union[List[str], Dict[str, List[str]]]) -> None:
        """
        Set dimensions for comparison.
        
        Args:
            dimensions: Either a list of dimension keys or a dictionary mapping dimension IDs to lists of dimension keys.
                       If a list is provided, each key will be treated as a single-level dimension.
                       If a dictionary is provided, each key represents a dimension ID and its value is a list of keys
                       that form the hierarchical levels of that dimension.
        """
        self.logger.info("Setting dimensions for comparison")
        
        if isinstance(dimensions, list):
            # Convert list format to dictionary format
            self._dimensions = {f"dim_{dim}": [dim] for dim in dimensions}
        else:
            # Use dictionary format directly
            self._dimensions = dimensions
        
        # Initialize aggregation levels for each dimension
        self.aggregation_levels = {}
        for dim_id, dim_keys in self._dimensions.items():
            self.aggregation_levels[dim_id] = {
                'keys': dim_keys,
                'current_level': 0,  # Start at the most granular level
                'max_level': len(dim_keys) - 1  # The most aggregated level
            }
        
        self.logger.info(f"Set {len(self._dimensions)} dimensions:")
        for dim_id, dim_keys in self._dimensions.items():
            self.logger.info(f"  - {dim_id}: {dim_keys}")
        self.logger.info("Aggregation levels initialized:")
        for dim_id, levels in self.aggregation_levels.items():
            self.logger.info(f"  - {dim_id}: {levels}")
    
    def set_comparison_structure(self, keys: List[str], values: List[str]):
        """Set the comparison structure with keys and values."""
        self.keys = keys
        self.values = values
        self._dimensions = set(keys)
        self.logger.debug(f"Set comparison structure - Keys: {keys}, Values: {values}")
    
    def get_column_analysis(self, column: str) -> Dict[str, Any]:
        """
        Get detailed analysis for a specific column.
        
        Args:
            column: The column name to analyze
            
        Returns:
            Dict containing detailed analysis for the column
        """
        # Ensure we have the analysis data
        if not hasattr(self, '_key_analysis'):
            self.detect_potential_keys()
        
        if not hasattr(self, '_value_analysis'):
            self.detect_potential_values()
        
        # Combine key and value analysis
        key_analysis = self._key_analysis.get(column, {})
        value_analysis = self._value_analysis.get(column, {})
        
        # Merge the analyses
        analysis = {**key_analysis, **value_analysis}
        
        # Add a summary of what type of column this is
        if analysis.get('is_potential_key', False):
            analysis['column_type'] = 'key'
        elif analysis.get('is_potential_value', False):
            analysis['column_type'] = 'value'
        else:
            analysis['column_type'] = 'unknown'
        
        return analysis
    
    def get_all_columns_analysis(self) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed analysis for all columns.
        
        Returns:
            Dict mapping column names to their analysis
        """
        # Ensure we have the analysis data
        if not hasattr(self, '_key_analysis'):
            self.detect_potential_keys()
        
        if not hasattr(self, '_value_analysis'):
            self.detect_potential_values()
        
        # Combine all analyses
        all_columns = set(list(self._key_analysis.keys()) + list(self._value_analysis.keys()))
        
        result = {}
        for column in all_columns:
            result[column] = self.get_column_analysis(column)
        
        return result
    
    def auto_detect_comparison_structure(self, key_threshold: float = 0.95, exclude_keys_from_values: bool = True):
        """
        Automatically detect keys and values for comparison.
        
        Args:
            key_threshold: Cardinality threshold for key detection
            exclude_keys_from_values: Whether to exclude detected keys from values
        """
        self.logger.info("Automatically detecting comparison structure...")
        
        # Detect potential keys
        detected_keys = self.detect_potential_keys(threshold=key_threshold)
        
        # If we have date/period columns, add them to keys
        date_columns = [col for col in self.data_a.columns if 'date' in col.lower() or 'period' in col.lower()]
        for date_col in date_columns:
            if date_col not in detected_keys:
                detected_keys.append(date_col)
                self.logger.debug(f"Added date column to keys: {date_col}")
        
        # Detect potential values
        detected_values = self.detect_potential_values(exclude_keys=exclude_keys_from_values)
        
        # Set the comparison structure
        if detected_keys and detected_values:
            self.set_comparison_structure(keys=detected_keys, values=detected_values)
            self.logger.info(f"Automatically detected {len(detected_keys)} keys and {len(detected_values)} values")
        else:
            self.logger.warning("Could not automatically detect keys and values. Please set them manually.")
    
    def analyze_scope(self) -> Dict[str, Any]:
        """
        Analyze the overlap between datasets and define the scope of comparison.
        
        This method analyzes the overlap between datasets, including column overlap,
        key overlap, and dimension overlap. It creates a scope dictionary that can be
        used for insight generation.
        
        Returns:
            Dict containing scope information including overlap percentages and unique elements.
        """
        # Check if fit stage is completed
        if not self.stage_manager.can_run_stage("compare"):
            raise ValueError("Fit stage must be completed before analyze_scope")
        
        # Get stage logger
        stage_logger = self.stages["compare"]
        
        # Start stage if not already started
        if self.stage_manager.get_stage_status("compare") == "not_started":
            stage_logger.start_stage({
                "keys": self.keys,
                "values": self.values,
                "dimensions": self._dimensions
            })
        
        # Set stage status
        self.stage_manager.set_stage_status("compare", "in_progress")
        
        try:
            self.logger.info("Analyzing data scope and overlap...")
            
            # Analyze column overlap
            columns_a = set(self.data_a.columns)
            columns_b = set(self.data_b.columns)
            common_columns = list(columns_a.intersection(columns_b))
            unique_to_a = list(columns_a - columns_b)
            unique_to_b = list(columns_b - columns_a)
            
            self.scope = {
                'common_columns': common_columns,
                'unique_to_a': unique_to_a,
                'unique_to_b': unique_to_b,
                'overlap_percentage': len(common_columns) / max(len(columns_a), len(columns_b)) * 100,
                'key_overlap': {
                    'common_keys': 0,
                    'unique_to_a': 0,
                    'unique_to_b': 0,
                    'overlap_percentage': 0.0
                },
                'dimension_overlap': {}
            }
            
            # Analyze key overlap if keys are defined
            if self.keys:
                self._analyze_key_overlap()
            
            # Analyze dimension overlap
            dimension_overlap = {}
           
            # If no dimensions are defined, create dimensions from keys
            if not self._dimensions and self.keys:
                self._dimensions = self.schema_analyzer.define_dimensions(self.data_a, self.keys)
            
            self.logger.debug(f"Dimensions in analyze_scope: {self._dimensions}")
            self.logger.debug(f"Dimensions type: {type(self._dimensions)}")
            
            if self._dimensions:
                # Process each dimension
                if isinstance(self._dimensions, dict):
                    for dimension_name, dimension_keys in self._dimensions.items():
                        self.logger.debug(f"Analyzing dimension: {dimension_name} with keys: {dimension_keys}")
                        # Check if all keys in the dimension exist in both datasets
                        if all(key in self.data_a.columns and key in self.data_b.columns for key in dimension_keys):
                            overlap_info = {}
                            for key in dimension_keys:
                                overlap_info[key] = self._analyze_dimension_overlap(key)
                            dimension_overlap[dimension_name] = overlap_info
                else:
                    self.logger.warning(f"Dimensions is not a dictionary: {type(self._dimensions)}")
            
            self.scope['dimension_overlap'] = dimension_overlap
            
            # Create scope checkpoint
            stage_logger.create_checkpoint("scope_analysis", self.scope)
            
            # Log the scope analysis results
            self.logger.info(f"Scope analysis complete. Found {self.scope['key_overlap']['common_keys']} common keys.")
            
            return self.scope
            
        except Exception as e:
            # Log error and set stage status
            stage_logger.log_error(f"Error analyzing scope: {str(e)}")
            self.stage_manager.set_stage_status("compare", "failed")
            raise e
    
    def _analyze_key_overlap(self):
        """Analyze overlap of key combinations between datasets"""
        self.logger.info("Analyzing key overlap...")
        
        # Create key combinations
        keys_a = self.data_a[self.keys].drop_duplicates()
        keys_b = self.data_b[self.keys].drop_duplicates()
        
        # Convert to string representation for comparison
        keys_a_str = keys_a.apply(lambda row: '_'.join(row.astype(str)), axis=1)
        keys_b_str = keys_b.apply(lambda row: '_'.join(row.astype(str)), axis=1)
        
        # Find common and unique keys
        common_keys = set(keys_a_str).intersection(set(keys_b_str))
        unique_to_a = set(keys_a_str) - set(keys_b_str)
        unique_to_b = set(keys_b_str) - set(keys_a_str)
        
        # Calculate overlap percentage
        total_keys = len(common_keys) + len(unique_to_a) + len(unique_to_b)
        overlap_percentage = len(common_keys) / total_keys * 100 if total_keys > 0 else 0
        
        # Store results
        self.scope['key_overlap'] = {
            'common_keys': len(common_keys),
            'unique_to_a': len(unique_to_a),
            'unique_to_b': len(unique_to_b),
            'overlap_percentage': overlap_percentage
        }
        
        if self.verbose:
            self.logger.debug(f"Key overlap: {len(common_keys)} common, {len(unique_to_a)} unique to A, {len(unique_to_b)} unique to B")
            self.logger.debug(f"Key overlap percentage: {overlap_percentage:.2f}%")
    
    def _analyze_dimension_overlap(self, dimension: str) -> Dict[str, Any]:
        """
        Analyze overlap for a specific dimension.
        
        Args:
            dimension: The dimension name to analyze
            
        Returns:
            Dict containing overlap information for the dimension
        """
        values_a = set(self.data_a[dimension].unique())
        values_b = set(self.data_b[dimension].unique())
        
        common_values = list(values_a.intersection(values_b))
        unique_to_a = list(values_a - values_b)
        unique_to_b = list(values_b - values_a)
        
        overlap_percentage = len(common_values) / max(len(values_a), len(values_b)) * 100 if values_a or values_b else 0
        
        return {
            'common_values': common_values,
            'unique_to_a': unique_to_a,
            'unique_to_b': unique_to_b,
            'overlap_percentage': overlap_percentage,
            'total_a': len(values_a),
            'total_b': len(values_b),
            'total_common': len(common_values)
        }


    def prepare(self, data_a: pd.DataFrame, data_b: pd.DataFrame, 
                metadata_a: Optional[Dict] = None, metadata_b: Optional[Dict] = None, 
                context: Optional[Dict] = None) -> 'LlamaSee':
        """
        Prepare the datasets for comparison.
        
        Args:
            data_a: First dataset
            data_b: Second dataset
            metadata_a: Optional metadata for dataset A
            metadata_b: Optional metadata for dataset B
            context: Optional context information
            
        Returns:
            Self for method chaining
        """
        self.logger.info("Starting prepare stage")
        
        # Store the datasets
        self.data_a = data_a.copy()
        self.data_b = data_b.copy()
        
        # Store metadata and context
        self.metadata_a = metadata_a or {}
        self.metadata_b = metadata_b or {}
        self.context = context or {}
        
        # Initialize stage checkpoints
        self._prepare_checkpoint = {}
        
        # Detect potential keys and values directly using schema_analyzer
        try:
            detected_keys = self.schema_analyzer.detect_potential_keys(self.data_a)
            detected_values = self.schema_analyzer.detect_potential_values(
                self.data_a,
                exclude_keys=detected_keys
            )
            
            # Detect time keys using the existing method
            detected_time_keys = self.schema_analyzer.detect_time_keys(self.data_a, key_columns=detected_keys)
            
            self.logger.info(f"Detected {len(detected_time_keys)} potential time keys: {detected_time_keys}")
            
            # Convert time keys to datetime format
            self.data_a, valid_time_keys_a = self.schema_analyzer.convert_time_keys_to_datetime(
                self.data_a, detected_time_keys
            )
            self.data_b, valid_time_keys_b = self.schema_analyzer.convert_time_keys_to_datetime(
                self.data_b, detected_time_keys
            )
            
            # Only use time keys that were successfully converted in both datasets
            valid_time_keys = list(set(valid_time_keys_a) & set(valid_time_keys_b))
            
            # Store the detected keys, values, and time keys in the checkpoint
            self._prepare_checkpoint['valid_keys'] = detected_keys
            self._prepare_checkpoint['valid_values'] = detected_values
            self._prepare_checkpoint['potential_time_keys'] = detected_time_keys
            self._prepare_checkpoint['valid_time_keys'] = valid_time_keys
            self._prepare_checkpoint['time_key_conversion'] = {
                'successful_a': valid_time_keys_a,
                'successful_b': valid_time_keys_b,
                'failed_a': list(set(detected_time_keys) - set(valid_time_keys_a)),
                'failed_b': list(set(detected_time_keys) - set(valid_time_keys_b))
            }
            
            # Also store in the analysis attributes for backward compatibility
            self._key_analysis = {
                "detected_keys": detected_keys,
                "time_keys": valid_time_keys
            }
            self._value_analysis = {
                "detected_values": detected_values
            }
            
            self.logger.info(f"Detected {len(detected_keys)} potential keys, {len(detected_values)} potential values")
            self.logger.info(f"Successfully converted {len(valid_time_keys)} time keys to datetime format")
            self.logger.debug(f"Detected keys: {detected_keys}")
            self.logger.debug(f"Detected values: {detected_values}")
            self.logger.debug(f"Valid time keys: {valid_time_keys}")
            self.logger.debug(f"Time key conversion results: {self._prepare_checkpoint['time_key_conversion']}")
        except Exception as e:
            self.logger.error(f"Error during key/value detection: {str(e)}")
            raise
        
        # Mark prepare stage as completed
        self._prepare_checkpoint['status'] = 'completed'
        
        return self
    
    def _analyze_columns(self) -> Dict[str, Any]:
        """
        Analyze columns in both datasets to identify common columns and their properties.
        
        Returns:
            Dict containing column analysis information
        """
        # Get columns from both datasets
        columns_a = set(self.data_a.columns)
        columns_b = set(self.data_b.columns)
        
        # Find common columns
        common_columns = list(columns_a.intersection(columns_b))
        
        # Find unique columns
        unique_to_a = list(columns_a - columns_b)
        unique_to_b = list(columns_b - columns_a)
        
        # Analyze data types for common columns
        data_types = {}
        for col in common_columns:
            data_types[col] = {
                'data_a': str(self.data_a[col].dtype),
                'data_b': str(self.data_b[col].dtype)
            }
        
        # Create analysis result
        analysis = {
            'common_columns': common_columns,
            'unique_to_a': unique_to_a,
            'unique_to_b': unique_to_b,
            'data_types': data_types
        }
        
        return analysis

    def fit(self, keys: Optional[List[str]] = None, values: Optional[List[str]] = None, 
            dimensions: Optional[Dict[str, List[str]]] = None,
            key_enrichment: Optional[Dict[str, Dict[str, Any]]] = None,
            time_keys: Optional[List[str]] = None,
            time_key_granularity: Optional[Dict[str, str]] = None) -> 'LlamaSee':
        """
        Prepare datasets for analysis by identifying and validating keys and values.
        
        Args:
            keys: Optional list of keys to use for comparison
            values: Optional list of values to compare
            dimensions: Optional dictionary of dimensions to analyze
            key_enrichment: Optional dictionary of key enrichment configurations
            time_keys: Optional list of time keys to use for time-series analysis
            time_key_granularity: Optional dictionary mapping time keys to their granularity
            
        Returns:
            LlamaSee instance for method chaining
        """
        self.logger.info("Starting fit stage")
        
        # Check if prepare stage is completed
        if not hasattr(self, '_prepare_checkpoint') or not self._prepare_checkpoint:
            self.logger.error("Prepare stage not completed. Please run prepare() first.")
            return self
        
        # Perform data quality check before proceeding with fit stage
        self.logger.info("Performing data quality check before fit stage")
        
        # Log dataset shapes for debugging
        self.logger.debug(f"Dataset A shape: {self.data_a.shape}, columns: {list(self.data_a.columns)}")
        self.logger.debug(f"Dataset B shape: {self.data_b.shape}, columns: {list(self.data_b.columns)}")
        
        quality_report = self.check_data_quality(self.data_a, self.data_b, keys)
        
        # Log quality issues if any
        if quality_report['overall_quality_score'] < 0.8:
            self.logger.warning(f"Data quality issues detected. Overall quality score: {quality_report['overall_quality_score']:.2f}")
            
            # Log dataset A issues
            for issue in quality_report['dataset_a'].get('issues', []):
                self.logger.warning(f"Dataset A issue: {issue['type']} - {issue.get('details', 'No details provided')}")
                
            # Log dataset B issues
            for issue in quality_report['dataset_b'].get('issues', []):
                self.logger.warning(f"Dataset B issue: {issue['type']} - {issue.get('details', 'No details provided')}")
                
            # Log comparison issues
            for issue in quality_report.get('comparison_issues', []):
                if isinstance(issue, dict):
                    details = issue.get('details', 'No details provided')
                    if isinstance(details, dict):
                        # Format dictionary details as a string
                        details_str = ', '.join([f"{k}: {v}" for k, v in details.items()])
                        self.logger.warning(f"Comparison issue: {issue.get('type', 'unknown')} - {details_str}")
                    else:
                        self.logger.warning(f"Comparison issue: {issue.get('type', 'unknown')} - {details}")
                else:
                    self.logger.warning(f"Comparison issue: {str(issue)}")
        else:
            self.logger.info(f"Data quality check passed. Overall quality score: {quality_report['overall_quality_score']:.2f}")
        
        # Extract valid keys, values, and time keys from prepare stage
        valid_keys = self._prepare_checkpoint.get('valid_keys', [])
        valid_values = self._prepare_checkpoint.get('valid_values', [])
        detected_time_keys = self._prepare_checkpoint.get('valid_time_keys', [])
        
        self.logger.debug(f"Extracted valid keys: {valid_keys}")
        self.logger.debug(f"Extracted valid values: {valid_values}")
        self.logger.debug(f"Detected time keys: {detected_time_keys}")
        
        # Set keys and values
        if keys is not None:
            # Validate that all specified keys exist in both datasets
            for key in keys:
                if key not in self.data_a.columns or key not in self.data_b.columns:
                    self.logger.warning(f"Key '{key}' not found in both datasets. Skipping.")
                    continue
            self.keys = keys
        else:
            self.keys = valid_keys
        
        if values is not None:
            # Validate that all specified values exist in both datasets
            for value in values:
                if value not in self.data_a.columns or value not in self.data_b.columns:
                    self.logger.warning(f"Value '{value}' not found in both datasets. Skipping.")
                    continue
            self.values = values
        else:
            self.values = valid_values
        
        # Set time keys
        if time_keys is not None:
            # Validate that all specified time keys exist in both datasets
            for time_key in time_keys:
                if time_key not in self.data_a.columns or time_key not in self.data_b.columns:
                    self.logger.warning(f"Time key '{time_key}' not found in both datasets. Skipping.")
                    continue
            self.time_keys = time_keys
        else:
            self.time_keys = detected_time_keys
        
        # Convert time keys to datetime format if needed
        if time_keys:
            self.logger.info(f"Converting {len(time_keys)} time keys to datetime format")
            
            # Skip conversion since it's already done in the prepare stage
            # Just detect granularity for the time keys
            for time_key in time_keys:
                # Determine which DataFrame to use
                df_to_use = self.data_a if time_key in self.data_a.columns else self.data_b
                granularity = self.schema_analyzer.detect_time_granularity(
                    df_to_use, time_key
                )
                if granularity:
                    self.time_key_granularity = {time_key: granularity}
            
            self.logger.info(f"Time key granularity: {self.time_key_granularity}")
        
        # Set dimensions if provided
        if dimensions is not None:
            self.set_dimensions(dimensions)
        
        # Apply key enrichment if provided
        if key_enrichment is not None:
            self.logger.info("Applying key enrichment")
            
            # Create an instance of KeyEnricher
            key_enricher = KeyEnricher(logger=self.logger)
            
            # Convert the key_enrichment dictionary to a list of configurations
            enrichment_configs = []
            for key, config in key_enrichment.items():
                if isinstance(config, dict) and "key_column" in config and "enriched_key" in config:
                    enrichment_configs.append(config)
                else:
                    self.logger.warning(f"Invalid key enrichment configuration for key '{key}'. Skipping.")
            
            # Apply enrichments to both datasets
            if enrichment_configs:
                # Create enriched datasets with new columns added (original data is preserved)
                self.data_a = key_enricher.enrich_keys(self.data_a, enrichment_configs)
                self.data_b = key_enricher.enrich_keys(self.data_b, enrichment_configs)
                
                # Store the enrichment metadata
                self.key_enrichment_metadata = key_enricher.get_enrichment_metadata()
                
                # Add enriched keys to the keys list
                enriched_keys = list(self.key_enrichment_metadata.keys())
                self.keys.extend(enriched_keys)
                
                self.logger.info(f"Applied {len(enriched_keys)} key enrichments")
                self.logger.debug(f"Enriched keys: {enriched_keys}")
        
        # Store time key granularity if provided
        self.time_key_granularity = time_key_granularity or {}
        
        # Create comparison structure checkpoint
        self._comparison_structure_checkpoint = {
            'keys': self.keys,
            'values': self.values,
            'time_keys': self.time_keys,
            'time_key_granularity': self.time_key_granularity,
            'enriched_keys': list(self.key_enrichment_metadata.keys()) if hasattr(self, 'key_enrichment_metadata') else []
        }
        
        # Set the comparison structure for the _generate_comparison_results method
        self._comparison_structure = {
            'key_columns': self.keys,
            'value_columns_a': self.values,
            'value_columns_b': self.values,
            'time_keys': self.time_keys,
            'time_key_granularity': self.time_key_granularity,
            'enriched_keys': list(self.key_enrichment_metadata.keys()) if hasattr(self, 'key_enrichment_metadata') else []
        }
        
        # Store the datasets for comparison
        self._data_a = self.data_a
        self._data_b = self.data_b
        
        # Complete the fit stage
        self.stage_manager.complete_stage("fit", {
            "keys": self.keys,
            "values": self.values,
            "time_keys": self.time_keys,
            "time_key_granularity": self.time_key_granularity,
            "enriched_keys": list(self.key_enrichment_metadata.keys()) if hasattr(self, 'key_enrichment_metadata') else []
        })
        
        self.logger.info("Fit stage completed")
        return self
    
    def export_fit_results(self, path: Optional[str] = None, format: str = 'json') -> Dict[str, Any]:
        """
        Export fit results to a file.
        
        Args:
            path: Path to export the fit results to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        try:
            # Get the exporter
            exporter = ExporterFactory.get_exporter('fit_results', self)
            if not exporter:
                self.logger.error("Fit results exporter not found")
                return {"error": "Fit results exporter not found"}
            
            # Export the fit results
            return exporter.export(path, format)
            
        except Exception as e:
            self.logger.error(f"Error exporting fit results: {str(e)}")
            return {"error": str(e)}

    def compare(self, aggregation_methods: Optional[Dict[str, str]] = None,
                post_comparison_enrichment: Optional[Dict[str, Dict[str, Any]]] = None) -> 'LlamaSee':
        """
        Compare datasets using the configured keys and values.
        
        Args:
            aggregation_methods: Optional dictionary mapping value columns to aggregation methods
            post_comparison_enrichment: Optional dictionary of key enrichment configurations to apply after comparison
            
        Returns:
            LlamaSee instance for method chaining
        """
        self.logger.info("Starting compare stage")
        
        # Check if fit stage is completed
        if not self.stage_manager.is_stage_completed("fit"):
            self.logger.error("Fit stage not completed. Please run fit() first.")
            return self
        
        # Set aggregation methods if provided
        if aggregation_methods is not None:
            self.aggregation_levels = aggregation_methods
        
        # Generate comparison results
        self._comparison_results = self._generate_comparison_results()
        
        # Apply post-comparison enrichment if provided
        if post_comparison_enrichment is not None:
            self.logger.info("Applying post-comparison enrichment")
            self._apply_post_comparison_enrichment(post_comparison_enrichment)
        
        # Complete the compare stage
        self.stage_manager.complete_stage("compare", {
            "comparison_results_shape": self._comparison_results.shape if isinstance(self._comparison_results, pd.DataFrame) else None,
            "aggregation_methods": self.aggregation_levels,
            "post_comparison_enrichment_applied": post_comparison_enrichment is not None
        })
        
        self.logger.info("Compare stage completed")
        return self
    
    def _prepare_dimension_insights(self, comparison_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare dimension insights from comparison results.
        
        Args:
            comparison_dict: Dictionary containing comparison results
            
        Returns:
            Dictionary containing dimension insights
        """
        self.logger.debug("Starting dimension insight preparation")
        
        # Check if we have dimension insights
        if 'dimension_insights' not in comparison_dict:
            self.logger.debug("No dimension insights found in comparison dictionary")
            return comparison_dict
            
        # Log the dimensions we're processing
        dimensions = list(comparison_dict['dimension_insights'].keys())
        self.logger.debug(f"Processing {len(dimensions)} dimensions: {dimensions}")
        
        # Process each dimension
        for dimension_name, dimension_data in comparison_dict['dimension_insights'].items():
            self.logger.debug(f"Processing dimension: {dimension_name} with {len(dimension_data)} values")
            
            # Process each value in the dimension
            for value, value_data in dimension_data.items():
                #self.logger.debug(f"Processing value: {value} for dimension {dimension_name}")
                
                # Check if we have metrics data
                if 'metrics' not in value_data:
                    self.logger.debug(f"No metrics data for dimension {dimension_name}, value {value}")
                    continue
                    
                # Get the metrics
                metrics = value_data['metrics']
                #self.logger.debug(f"Found metrics for {len(metrics)} values in dimension {dimension_name}, value {value}")
                
                # Calculate averages for metrics in multi-key dimensions
                #for metric_name, metric_data in metrics.items():
                #    if 'mean_percentage_diff' in metric_data:
                #        self.logger.debug(f"Metric {metric_name} for dimension {dimension_name}, value {value}: mean_percentage_diff = {metric_data['mean_percentage_diff']:.2f}%")
        
        # Log summary of dimension insights
        total_values = sum(len(dim_data) for dim_data in comparison_dict['dimension_insights'].values())
        self.logger.debug(f"Dimension insight preparation complete. Processed {len(dimensions)} dimensions with {total_values} total values")
        
        return comparison_dict

    def export_individual_results(self, path: str, format: str = 'json') -> Dict[str, Any]:
        """
        Export individual comparison results to a file.
        
        Args:
            path: Path to export the individual comparison results to.
            format: Format to export in ('json', 'csv').
            
        Returns:
            Dictionary containing export information.
        """
        try:
            # Get the exporter
            self.logger.debug(f"Exporting individual comparison results at path: {path} in format: {format}")
            exporter = ExporterFactory.get_exporter('individual_comparison_results', self)
            if not exporter:
                self.logger.error("Individual comparison results exporter not found")
                return {"error": "Individual comparison results exporter not found"}
            
            # Export the results
            result = exporter.export(path, format)
            self.logger.debug(f"Exported individual comparison results at path: {result['path']} in format: {result['format']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error exporting individual results: {str(e)}")
            raise

    @final
    def generate_insights(self, comparison_results: Optional[Union[Dict[str, Any], pd.DataFrame, ComparisonResult]] = None,
                         scope: Optional[Dict[str, Any]] = None,
                         context: Optional[Dict[str, Any]] = None,
                         top_n: int = 5,
                         insight_types: Optional[List[str]] = None,
                         scope_levels: Optional[List[str]] = None,
                         significance_threshold: float = 0.05,
                         min_insight_score: float = 0.5,
                         fact_type: Optional[str] = None,
                         time_key: Optional[str] = None) -> List[Insight]:
        """
        Generate insights from comparison results.
        
        Args:
            comparison_results: Results from data comparison (can be DataFrame, dict, or ComparisonResult)
            scope: Scope information from analysis
            context: Additional context
            top_n: Number of top insights to return
            insight_types: Types of insights to generate
            scope_levels: Scope levels to include
            significance_threshold: Threshold for significance
            min_insight_score: Minimum insight score
            fact_type: Optional fact type to filter insights by (e.g., "forecast_value_p50")
            time_key: Optional time key to use for time-based insights
            
        Returns:
            List[Insight]: Generated insights
        """
        # Check if comparison results are available
        if comparison_results is None:
            comparison_results = self._comparison_results
            
        # Check if comparison results are empty
        if comparison_results is None or (isinstance(comparison_results, pd.DataFrame) and comparison_results.empty):
            self.logger.warning("No comparison results available.")
            return []
            
        # Check if scope is available
        if scope is None:
            scope = self.analyze_scope()
            
        # Check if context is available
        if context is None:
            context = self.context
            
        # Log the start of insight generation
        self.logger.info("Starting insight generation")
        
        # Convert input to canonical ComparisonResult if needed
        if not isinstance(comparison_results, ComparisonResult):
            self.logger.info("Converting input to canonical ComparisonResult format")
            if isinstance(comparison_results, pd.DataFrame):
                # Create ComparisonResultRow objects
                rows = []
                for _, row in comparison_results.iterrows():
                    # Create key dictionary from non-value columns
                    key_dict = {col: row[col] for col in row.index if not col.endswith(('_a', '_b', '_diff', '_pct_diff'))}
                    
                    # Create ComparisonResultRow
                    comparison_row = ComparisonResultRow(
                        key=key_dict,
                        fact_type=fact_type or "value",
                        value_a=row.get(f"{fact_type}_a") if fact_type else None,
                        value_b=row.get(f"{fact_type}_b") if fact_type else None,
                        diff=row.get(f"{fact_type}_diff") if fact_type else None,
                        percent_change=row.get(f"{fact_type}_pct_diff") if fact_type else None,
                        time_key=row.get('time_key'),
                        time_key_info=row.get('time_key_info', {}),
                        timestamp=datetime.now()
                    )
                    rows.append(comparison_row)
                
                # Create ComparisonResult object
                comparison_results = ComparisonResult(
                    df=comparison_results,
                    rows=rows,
                    metadata={
                        "fact_type": fact_type,
                        "timestamp": datetime.now()
                    }
                )
                self.logger.debug(f"Converted DataFrame to ComparisonResult with {len(rows)} rows")
            else:
                # Create ComparisonResult from dictionary
                comparison_results = ComparisonResult(
                    df=pd.DataFrame(comparison_results.values()),
                    rows=[ComparisonResultRow(**row) for row in comparison_results.values()],
                    metadata={
                        "timestamp": datetime.now(),
                        "source": "dict_conversion"
                    }
                )
                self.logger.debug(f"Converted dictionary to ComparisonResult with {len(comparison_results.rows)} rows")
        
        # Initialize insight generator
        insight_generator = InsightGenerator(
            insight_config=self.insight_config,
            plugin_manager=self.plugin_manager
        )
        
        # Generate insights using canonical format
        insights = insight_generator.generate_insights(
            comparison_results=comparison_results,
            scope=scope,
            context=context,
            top_n=top_n,
            fact_type=fact_type
        )
        
        # Store insights
        self._insights = insights
        
        # Log the number of insights generated
        self.logger.info(f"Generated {len(insights)} insights")
        
        return insights
    
    def export_results(self, path: str, format: str = 'csv') -> Dict[str, Any]:
        """
        Export comparison results to a file.
        
        Args:
            path: Path to export the results to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        try:
            # Get the stage logger
            stage_logger = self.stage_manager.get_stage("export_results")
            
            # Start the export stage
            stage_logger.start_stage({
                "path": path,
                "format": format
            })
            self.stage_manager.set_stage_status("export_results", "in_progress")
            
            # Get the exporter
            exporter = ExporterFactory.get_exporter('results', self)
            if not exporter:
                self.logger.error("Results exporter not found")
                self.stage_manager.fail_stage("export_results", {"error": "Results exporter not found"})
                stage_logger.log_error("Results exporter not found")
                return {"error": "Results exporter not found"}
            
            # Export the results
            result = exporter.export(path, format)
            
            # End the stage
            if "error" in result:
                self.stage_manager.fail_stage("export_results", {"error": result["error"]})
                stage_logger.log_error(result["error"])
            else:
                self.stage_manager.complete_stage("export_results", result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error exporting results: {str(e)}")
            self.stage_manager.fail_stage("export_results", {"error": str(e)})
            stage_logger.log_error(e, {"traceback": traceback.format_exc()})
            raise
    

    def run(self, data_a: Union[pd.DataFrame, str], 
            data_b: Union[pd.DataFrame, str],
            keys: Optional[List[str]] = None,
            values: Optional[List[str]] = None,
            metadata_a: Optional[Dict[str, Any]] = None,
            metadata_b: Optional[Dict[str, Any]] = None,
            context: Optional[Dict[str, Any]] = None,
            dimensions: Optional[Dict[str, Any]] = None,
            export_path: Optional[str] = None,
            export_format: str = 'csv') -> 'LlamaSee':
        """
        Execute the full LlamaSee lifecycle.
        
        Args:
            data_a: First dataset (DataFrame or path to file)
            data_b: Second dataset (DataFrame or path to file)
            keys: Optional list of key columns
            values: Optional list of value columns
            metadata_a: Optional metadata for first dataset
            metadata_b: Optional metadata for second dataset
            context: Optional context dictionary
            dimensions: Optional dimension configuration
            export_path: Optional path to export results
            export_format: Format to export results in ('csv', 'json', 'dict')
            
        Returns:
            Self for method chaining
        """
        # Run prepare stage
        self.prepare(data_a, data_b, metadata_a, metadata_b, context)
        
        # Run fit stage
        self.fit(keys, values, dimensions)
        
        # Run compare stage
        self.compare()
        
        # Run generate_insights stage
        self.generate_insights()
        
        # Run export_results stage if path is provided
        if export_path:
            self.export_results(export_path, export_format)
        
        return self
    
    def get_stage_summary(self) -> Dict[str, Any]:
        """Get summary of all stages."""
        return self.stage_manager.get_summary()
    
    def filter_insights(self, min_importance: float = 0.0, dimensions: Optional[List[str]] = None) -> List[Insight]:
        """
        Filter insights based on importance and dimensions.
        
        Args:
            min_importance: Minimum importance score (0-1)
            dimensions: Optional list of dimensions to filter by
            
        Returns:
            List of filtered insights
        """
        filtered = []
        
        for insight in self._insights:
            # Check importance score
            if insight.weighted_score < min_importance:
                continue
                
            # Check dimensions if specified
            if dimensions:
                insight_dims = set(insight.dimensions) if insight.dimensions else set()
                if not insight_dims.intersection(dimensions):
                    continue
                    
            filtered.append(insight)
            
        return filtered

    def compare_datasets(self) -> pd.DataFrame:
        """
        Compare the two datasets based on the set keys and values.
        
        Returns:
            DataFrame containing the comparison results with differences
        """
        self.logger.info("Comparing datasets...")
        
        # Check if comparison structure is set
        if not self.keys or not self.values:
            raise ValueError("Comparison structure not set. Call set_comparison_structure first.")
        
        # Get stage logger
        stage_logger = self.stages["compare"]
        
        # Start stage
        stage_logger.start_stage({
            "keys": self.keys,
            "values": self.values,
            "dimensions": self._dimensions
        })
        
        # Set stage status
        self.stage_manager.set_stage_status("compare", "in_progress")
        
        try:
            # Create copies of the dataframes with renamed columns to avoid conflicts
            df_a = self.data_a.copy()
            df_b = self.data_b.copy()
            
            # Rename value columns to indicate which dataset they come from
            for value in self.values:
                if value in df_a.columns:
                    df_a = df_a.rename(columns={value: f"{value}_a"})
                if value in df_b.columns:
                    df_b = df_b.rename(columns={value: f"{value}_b"})
            
            # Merge the datasets on the key columns
            merged_df = pd.merge(df_a, df_b, on=self.keys, how='outer', suffixes=('_a', '_b'))
            
            # Calculate differences for each value column
            for value in self.values:
                value_a = f"{value}_a"
                value_b = f"{value}_b"
                
                # Calculate absolute difference with value-specific column name
                merged_df[f'{value}_absolute_diff'] = merged_df[value_b] - merged_df[value_a]
                
                # Calculate percentage difference with value-specific column name (avoid division by zero)
                merged_df[f'{value}_percentage_diff'] = np.where(
                    merged_df[value_a] != 0,
                    (merged_df[value_b] - merged_df[value_a]) / merged_df[value_a] * 100,
                    np.inf  # Use infinity for division by zero
                )
                
                # Calculate ratio for additional insight
                merged_df[f'{value}_ratio'] = np.where(
                    merged_df[value_a] != 0,
                    merged_df[value_b] / merged_df[value_a],
                    np.inf
                )
            
            # Store the comparison results
            self._comparison_results = merged_df
            
            # Create comparison results checkpoint
            comparison_results = {
                "row_count": len(merged_df),
                "column_count": len(merged_df.columns),
                "columns": list(merged_df.columns),
                "value_columns": {
                    value: {
                        "original_a": f"{value}_a",
                        "original_b": f"{value}_b",
                        "absolute_diff": f"{value}_absolute_diff",
                        "percentage_diff": f"{value}_percentage_diff",
                        "ratio": f"{value}_ratio"
                    } for value in self.values
                }
            }
            stage_logger.create_checkpoint("comparison_results", comparison_results)
            
            # End stage
            self.stage_manager.complete_stage("compare", {
                "row_count": len(merged_df),
                "column_count": len(merged_df.columns),
                "value_columns": list(comparison_results["value_columns"].keys())
            })
            
            # Set stage status
            self.stage_manager.set_stage_status("compare", "completed")
            
            return merged_df
            
        except Exception as e:
            # Log error and set stage status
            stage_logger.log_error(str(e))
            self.stage_manager.set_stage_status("compare", "failed")
            raise 

    def _generate_comparison_results(self) -> pd.DataFrame:
        """
        Generate comparison results between two datasets.
        
        This method creates a DataFrame that contains:
        1. All key columns from both datasets
        2. A dataset_key_match column indicating which dataset each key exists in
        3. Value columns from both datasets with appropriate suffixes
        4. Difference calculations for matching rows
        5. Time-related metadata and analysis
        
        Returns:
            DataFrame containing the comparison results
        """
        try:
            # Check if comparison structure is set
            if not hasattr(self, '_comparison_structure') or not self._comparison_structure:
                self.logger.error("Comparison structure not set. Please run fit() first.")
                return pd.DataFrame()
            
            # Get the datasets
            data_a = self._data_a
            data_b = self._data_b
            
            # Get key columns and time keys from comparison structure
            key_columns = self._comparison_structure.get('key_columns', [])
            value_columns_a = self._comparison_structure.get('value_columns_a', [])
            value_columns_b = self._comparison_structure.get('value_columns_b', [])
            time_keys = self._comparison_structure.get('time_keys', [])
            time_key_granularity = {}  # Initialize as empty dict
            
            # Debug: Log the comparison structure
            self.logger.debug(f"Comparison structure: {self._comparison_structure}")
            self.logger.debug(f"Key columns: {key_columns}")
            self.logger.debug(f"Value columns A: {value_columns_a}")
            self.logger.debug(f"Value columns B: {value_columns_b}")
            self.logger.debug(f"Time keys: {time_keys}")
            
            # Check if data_a and data_b are tuples and extract DataFrames if needed
            if isinstance(data_a, tuple):
                self.logger.debug(f"data_a is a tuple with {len(data_a)} elements")
                # Assuming the DataFrame is the first element in the tuple
                data_a = data_a[0]
                
            if isinstance(data_b, tuple):
                self.logger.debug(f"data_b is a tuple with {len(data_b)} elements")
                # Assuming the DataFrame is the first element in the tuple
                data_b = data_b[0]
            
            # Debug: Check if key columns exist in dataframes
            self.logger.debug(f"Data A columns: {list(data_a.columns)}")
            self.logger.debug(f"Data B columns: {list(data_b.columns)}")
            
            # Check if all key columns exist in both dataframes
            missing_in_a = [col for col in key_columns if col not in data_a.columns]
            missing_in_b = [col for col in key_columns if col not in data_b.columns]
            
            if missing_in_a:
                self.logger.error(f"Key columns missing in dataset A: {missing_in_a}")
                raise ValueError(f"Key columns missing in dataset A: {missing_in_a}")
                
            if missing_in_b:
                self.logger.error(f"Key columns missing in dataset B: {missing_in_b}")
                raise ValueError(f"Key columns missing in dataset B: {missing_in_b}")
            
            self.logger.info(f"Generating comparison results using {len(key_columns)} key columns")
            
            # Create a DataFrame with all unique keys from both datasets
            keys_a = data_a[key_columns].drop_duplicates()
            keys_b = data_b[key_columns].drop_duplicates()
            
            self.logger.info(f"Dataset A has {len(keys_a)} unique key combinations")
            self.logger.info(f"Dataset B has {len(keys_b)} unique key combinations")
            
            # Create a DataFrame with all unique keys
            all_keys = pd.concat([keys_a, keys_b]).drop_duplicates()
            self.logger.info(f"Total unique key combinations: {len(all_keys)}")
            
            # Debug: Log the key columns in all_keys
            self.logger.debug(f"Key columns in all_keys: {list(all_keys.columns)}")
            
            # Create a column to indicate which dataset each key exists in
            all_keys['dataset_key_match'] = 'neither'
            
            # Create a unique identifier for each key combination
            all_keys['key_id'] = all_keys[key_columns].astype(str).apply(lambda x: '_'.join(x), axis=1)
            keys_a['key_id'] = keys_a[key_columns].astype(str).apply(lambda x: '_'.join(x), axis=1)
            keys_b['key_id'] = keys_b[key_columns].astype(str).apply(lambda x: '_'.join(x), axis=1)
            
            # Mark keys that exist in dataset A
            all_keys.loc[all_keys['key_id'].isin(keys_a['key_id']), 'dataset_key_match'] = 'a-only'
            
            # Mark keys that exist in dataset B
            all_keys.loc[all_keys['key_id'].isin(keys_b['key_id']), 'dataset_key_match'] = 'b-only'
            
            # Mark keys that exist in both datasets
            all_keys.loc[all_keys['key_id'].isin(keys_a['key_id']) & all_keys['key_id'].isin(keys_b['key_id']), 'dataset_key_match'] = 'match'
            
            # Drop the temporary key_id column
            all_keys = all_keys.drop('key_id', axis=1)
            
            # Debug: Log the dataset_key_match distribution
            match_counts = all_keys['dataset_key_match'].value_counts()
            self.logger.debug(f"Dataset key match distribution: {match_counts.to_dict()}")
            
            # Initialize comparison_results with all_keys (which includes original key columns)
            comparison_results = all_keys.copy()
            
            # Merge value columns from dataset A
            if value_columns_a:
                self.logger.info(f"Merging {len(value_columns_a)} value columns from dataset A")
                comparison_results = pd.merge(
                    comparison_results,
                    data_a[key_columns + value_columns_a],
                    on=key_columns,
                    how='left'
                )
                
                # Rename value columns from dataset A
                for col in value_columns_a:
                    if col in comparison_results.columns:
                        comparison_results.rename(columns={col: f"{col}_a"}, inplace=True)
            
            # Merge value columns from dataset B
            if value_columns_b:
                self.logger.info(f"Merging {len(value_columns_b)} value columns from dataset B")
                comparison_results = pd.merge(
                    comparison_results,
                    data_b[key_columns + value_columns_b],
                    on=key_columns,
                    how='left'
                )
                
                # Rename value columns from dataset B
                for col in value_columns_b:
                    if col in comparison_results.columns:
                        comparison_results.rename(columns={col: f"{col}_b"}, inplace=True)
            
            # Calculate differences for matching rows
            matching_rows = comparison_results['dataset_key_match'] == 'match'
            self.logger.info(f"Calculating differences for {matching_rows.sum()} matching rows")
            
            for col_a, col_b in zip(value_columns_a, value_columns_b):
                col_a_suffix = f"{col_a}_a"
                col_b_suffix = f"{col_b}_b"
                
                if col_a_suffix in comparison_results.columns and col_b_suffix in comparison_results.columns:
                    # Calculate absolute difference
                    diff_col = f"{col_a}_diff"
                    comparison_results.loc[matching_rows, diff_col] = (
                        comparison_results.loc[matching_rows, col_a_suffix] - 
                        comparison_results.loc[matching_rows, col_b_suffix]
                    )
                    
                    # Calculate percentage difference
                    pct_diff_col = f"{col_a}_pct_diff"
                    comparison_results.loc[matching_rows, pct_diff_col] = np.where(
                        comparison_results.loc[matching_rows, col_b_suffix] != 0,
                        (comparison_results.loc[matching_rows, col_a_suffix] - 
                         comparison_results.loc[matching_rows, col_b_suffix]) / 
                        comparison_results.loc[matching_rows, col_b_suffix] * 100,
                        np.inf  # Use infinity for division by zero
                    )
            
            # Get time keys and their granularity
            time_keys = self._comparison_structure.get('time_keys', [])
            time_key_granularity = {}  # Initialize as empty dict
            
            # Convert time keys to datetime format if needed
            if time_keys:
                self.logger.info(f"Converting {len(time_keys)} time keys to datetime format")
                
                # Skip conversion since it's already done in the prepare stage
                # Just detect granularity for the time keys
                for time_key in time_keys:
                    # Determine which DataFrame to use
                    df_to_use = data_a if time_key in data_a.columns else data_b
                    granularity = self.schema_analyzer.detect_time_granularity(
                        df_to_use, time_key
                    )
                    if granularity:
                        time_key_granularity[time_key] = granularity
                
                self.logger.info(f"Time key granularity: {time_key_granularity}")
            
            # Create a ComparisonResult object for canonical format
            from llamasee.schema.comparison import ComparisonResult, ComparisonResultRow
            from datetime import datetime
            
            # Create a list of ComparisonResultRow objects
            comparison_rows = []
            
            # Process each row in the comparison results
            for _, row in comparison_results.iterrows():
                # Extract key values
                key_dict = {k: row[k] for k in key_columns}
                
                # Process each value column
                for value in value_columns_a:
                    value_a = row.get(f"{value}_a")
                    value_b = row.get(f"{value}_b")
                    abs_diff = row.get(f"{value}_diff")
                    pct_diff = row.get(f"{value}_pct_diff")
                    
                    # Create base comparison row
                    comp_row = ComparisonResultRow(
                        key=key_dict,
                        value_a=value_a,
                        value_b=value_b,
                        diff=abs_diff,
                        percent_change=pct_diff,
                        fact_type=value,
                        timestamp=datetime.now()
                    )
                    
                    # Set time key and granularity if available
                    for time_key in time_keys:
                        if time_key in key_dict:
                            comp_row.set_time_key_granularity(
                                time_key,
                                time_key_granularity.get(time_key)
                            )
                    
                    # Add to results
                    comparison_rows.append(comp_row)
                    
                    # If enriched keys are available, create dimensional comparisons
                    if hasattr(self, 'key_enrichment_metadata') and self.key_enrichment_metadata:
                        for enriched_key, metadata in self.key_enrichment_metadata.items():
                            if enriched_key in row:
                                # Create a dimensional comparison row
                                dim_row = ComparisonResultRow(
                                    key=key_dict,
                                    value_a=value_a,
                                    value_b=value_b,
                                    diff=abs_diff,
                                    percent_change=pct_diff,
                                    fact_type=value,
                                    dimension={metadata.get("enriched_key", enriched_key): str(row[enriched_key])},
                                    timestamp=datetime.now()
                                )
                                
                                # Set time key and granularity for dimensional row
                                for time_key in time_keys:
                                    if time_key in key_dict:
                                        dim_row.set_time_key_granularity(
                                            time_key,
                                            time_key_granularity.get(time_key)
                                        )
                                
                                comparison_rows.append(dim_row)
            
            # Create the ComparisonResult object
            comparison_result = ComparisonResult(
                df=comparison_results,
                rows=comparison_rows,
                metadata={
                    "dataset_a_rows": len(data_a),
                    "dataset_b_rows": len(data_b),
                    "keys": key_columns,
                    "values": value_columns_a,
                    "time_keys": time_keys,
                    "time_key_granularity": time_key_granularity,
                    "enriched_keys": list(self.key_enrichment_metadata.keys()) if hasattr(self, 'key_enrichment_metadata') else [],
                    "timestamp": datetime.now()
                }
            )
            
            # Add time_key and time_key_info columns to the DataFrame
            if time_keys:
                # Use the first time key as the primary time key
                primary_time_key = time_keys[0]
                comparison_results['time_key'] = primary_time_key
                
                # Create time_key_info column with granularity information
                comparison_results['time_key_info'] = comparison_results.apply(
                    lambda row: {
                        "granularity": time_key_granularity.get(primary_time_key),
                        "metadata": {}
                    },
                    axis=1
                )
            
            # Store both the DataFrame and canonical format
            self._comparison_results = comparison_results
            self._canonical_comparison_results = comparison_result
            
            self.logger.info("Created comparison checkpoints")
            
            return comparison_results
            
        except Exception as e:
            self.logger.error(f"Error generating comparison results: {str(e)}")
            return pd.DataFrame()

    def check_data_quality(self, data_a: Optional[pd.DataFrame] = None, 
                          data_b: Optional[pd.DataFrame] = None,
                          keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive data quality checks on both datasets.
        
        This method delegates to the DataQualityAnalyzer to analyze both datasets
        for common data quality issues including missing values, data type inconsistencies,
        duplicate records, outliers, key cardinality issues, and comparison issues.
        
        Args:
            data_a: First DataFrame to check
            data_b: Second DataFrame to check
            keys: List of key columns to check for cardinality issues
            
        Returns:
            Dictionary containing detailed data quality report
        """
        return self.data_quality_analyzer.check_data_quality(data_a, data_b, keys)

    def _apply_post_comparison_enrichment(self, enrichment_configs: Dict[str, Dict[str, Any]]) -> None:
        """
        Apply key enrichment to the comparison results after they have been generated.
        
        Args:
            enrichment_configs: Dictionary of key enrichment configurations
        """
        try:
            # Check if we have comparison results
            if self._comparison_results is None or not isinstance(self._comparison_results, pd.DataFrame):
                self.logger.error("No comparison results available for post-comparison enrichment")
                return
            
            # Create an instance of KeyEnricher
            key_enricher = KeyEnricher(logger=self.logger)
            
            # Convert the enrichment_configs dictionary to a list of configurations
            config_list = []
            for key, config in enrichment_configs.items():
                if isinstance(config, dict) and "key_column" in config and "enriched_key" in config:
                    config_list.append(config)
                else:
                    self.logger.warning(f"Invalid key enrichment configuration for key '{key}'. Skipping.")
            
            # Apply enrichments to the comparison results
            if config_list:
                # Create a copy of the comparison results to avoid modifying the original
                enriched_results = self._comparison_results.copy()
                
                # Apply each enrichment configuration
                for config in config_list:
                    key_column = config.get("key_column")
                    enriched_key = config.get("enriched_key")
                    mappings = config.get("mappings", {})
                    
                    # Check if the key column exists in the comparison results
                    if key_column not in enriched_results.columns:
                        self.logger.warning(f"Key column '{key_column}' not found in comparison results. Skipping enrichment.")
                        continue
                    
                    # Create the enriched key column
                    enriched_column_name = f"dim_{enriched_key}"
                    
                    # Apply the mapping
                    self.logger.debug(f"Applying post-comparison enrichment: {key_column} -> {enriched_column_name}")
                    
                    # Create a mapping function that preserves original data types
                    def map_value(value):
                        # Convert to string for lookup only, but return the original value if not found
                        str_value = str(value)
                        return mappings.get(str_value, value)
                    
                    # Create the enriched column
                    enriched_results[enriched_column_name] = enriched_results[key_column].apply(map_value)
                    
                    # Store metadata about the enrichment
                    if not hasattr(self, 'post_comparison_enrichment_metadata'):
                        self.post_comparison_enrichment_metadata = {}
                    
                    self.post_comparison_enrichment_metadata[enriched_column_name] = {
                        "original_key": key_column,
                        "enriched_key": enriched_key,
                        "enrichment_type": "mapping",
                        "parameters": {
                            "mappings": mappings
                        },
                        "applied_at": datetime.now().isoformat()
                    }
                
                # Update the comparison results with the enriched version
                self._comparison_results = enriched_results
                
                # Log the applied enrichments
                self.logger.info(f"Applied {len(config_list)} post-comparison enrichments")
                self.logger.debug(f"Post-comparison enriched columns: {list(self.post_comparison_enrichment_metadata.keys())}")
            
        except Exception as e:
            self.logger.error(f"Error applying post-comparison enrichment: {str(e)}")
            # Continue with the original comparison results
