"""
Data quality analysis for LlamaSee.

This module provides functionality for analyzing data quality in datasets,
including checks for missing values, data type inconsistencies, duplicates,
outliers, and comparison issues between datasets.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import logging


class DataQualityAnalyzer:
    """
    Analyzes data quality in datasets and provides detailed reports.
    
    This class performs comprehensive data quality checks on datasets,
    including checks for missing values, data type inconsistencies,
    duplicate records, outliers, key cardinality issues, and comparison
    issues between datasets.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the data quality analyzer.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def check_data_quality(self, data_a: pd.DataFrame, data_b: pd.DataFrame, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive data quality checks on both datasets.
        
        Args:
            data_a: First DataFrame to check
            data_b: Second DataFrame to check
            keys: Optional list of key columns to focus quality checks on
            
        Returns:
            Dictionary containing overall quality score and detailed issues
        """
        self.logger.debug("Starting comprehensive data quality check")
        self.logger.debug(f"Dataset A: {data_a.shape[0]} rows, {data_a.shape[1]} columns")
        self.logger.debug(f"Dataset B: {data_b.shape[0]} rows, {data_b.shape[1]} columns")
        if keys:
            self.logger.debug(f"Focusing quality checks on key columns: {keys}")
        
        # Check individual dataset quality
        quality_a = self._check_single_dataset_quality(data_a, "A", keys)
        quality_b = self._check_single_dataset_quality(data_b, "B", keys)
        
        self.logger.debug(f"Dataset A quality score: {quality_a['quality_score']:.2f}")
        self.logger.debug(f"Dataset B quality score: {quality_b['quality_score']:.2f}")
        
        # Check comparison quality
        comparison_quality = self._check_comparison_quality(data_a, data_b, keys)
        
        self.logger.debug(f"Comparison quality score: {comparison_quality['quality_score']:.2f}")
        
        # Calculate overall quality score
        overall_score = (quality_a['quality_score'] + quality_b['quality_score'] + comparison_quality['quality_score']) / 3
        
        self.logger.debug(f"Overall quality score: {overall_score:.2f}")
        
        # Compile all issues
        all_issues = []
        
        # Add dataset A issues
        for issue in quality_a['issues']:
            issue['dataset'] = 'A'
            all_issues.append(issue)
        
        # Add dataset B issues
        for issue in quality_b['issues']:
            issue['dataset'] = 'B'
            all_issues.append(issue)
        
        # Add comparison issues
        for issue in comparison_quality['issues']:
            issue['dataset'] = 'comparison'
            all_issues.append(issue)
        
        self.logger.debug(f"Total issues found: {len(all_issues)}")
        
        return {
            'overall_quality_score': overall_score,
            'dataset_a_quality': quality_a,
            'dataset_b_quality': quality_b,
            'comparison_quality': comparison_quality,
            'issues': all_issues
        }
    
    def _check_single_dataset_quality(self, data: pd.DataFrame, dataset_name: str, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Check quality of a single dataset.
        
        Args:
            data: DataFrame to check
            dataset_name: Name of the dataset for logging
            keys: Optional list of key columns to focus quality checks on
            
        Returns:
            Dictionary containing quality score and issues
        """
        self.logger.debug(f"Checking quality for dataset {dataset_name}")
        self.logger.debug(f"Shape: {data.shape[0]} rows, {data.shape[1]} columns")
        if keys:
            self.logger.debug(f"Focusing on key columns: {keys}")
        
        issues = []
        quality_score = 1.0  # Start with perfect score
        
        # Check for missing values
        missing_values = data.isnull().sum()
        missing_columns = missing_values[missing_values > 0]
        
        # If keys are specified, prioritize checking those columns
        if keys:
            key_missing = missing_columns[missing_columns.index.isin(keys)]
            if not key_missing.empty:
                self.logger.debug(f"Found missing values in key columns: {list(key_missing.index)}")
                issues.append({
                    'type': 'missing_values',
                    'severity': 'high',
                    'affected_columns': list(key_missing.index),
                    'description': f"Found {key_missing.sum()} missing values in key columns",
                    'recommendation': "Key columns should not contain missing values"
                })
                quality_score *= 0.7  # Severe penalty for missing values in key columns
            
            # Check non-key columns
            non_key_missing = missing_columns[~missing_columns.index.isin(keys)]
            if not non_key_missing.empty:
                self.logger.debug(f"Found missing values in non-key columns: {list(non_key_missing.index)}")
                issues.append({
                    'type': 'missing_values',
                    'severity': 'medium' if non_key_missing.sum() > len(data) * 0.1 else 'low',
                    'affected_columns': list(non_key_missing.index),
                    'description': f"Found {non_key_missing.sum()} missing values across {len(non_key_missing)} non-key columns",
                    'recommendation': "Consider imputing missing values or removing rows with missing values"
                })
                quality_score *= 0.9  # Moderate penalty for missing values in non-key columns
        else:
            # Check all columns if no keys specified
            if not missing_columns.empty:
                self.logger.debug(f"Found missing values in columns: {list(missing_columns.index)}")
                issues.append({
                    'type': 'missing_values',
                    'severity': 'high' if missing_columns.sum() > len(data) * 0.1 else 'medium',
                    'affected_columns': list(missing_columns.index),
                    'description': f"Found {missing_columns.sum()} missing values across {len(missing_columns)} columns",
                    'recommendation': "Consider imputing missing values or removing rows with missing values"
                })
                quality_score *= 0.8  # Penalize for missing values
        
        # Check for duplicates
        duplicates = data.duplicated().sum()
        if duplicates > 0:
            self.logger.debug(f"Found {duplicates} duplicate rows")
            issues.append({
                'type': 'duplicates',
                'severity': 'medium' if duplicates < len(data) * 0.1 else 'high',
                'affected_columns': list(data.columns),
                'description': f"Found {duplicates} duplicate rows",
                'recommendation': "Consider removing duplicate rows"
            })
            quality_score *= 0.9  # Penalize for duplicates
        
        # Check for outliers in numeric columns
        numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_columns:
            # Skip key columns if specified
            if keys and col in keys:
                continue
                
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
            if len(outliers) > 0:
                self.logger.debug(f"Found {len(outliers)} outliers in column {col}")
                issues.append({
                    'type': 'outliers',
                    'severity': 'medium' if len(outliers) < len(data) * 0.05 else 'high',
                    'affected_columns': [col],
                    'description': f"Found {len(outliers)} outliers in column {col}",
                    'recommendation': "Consider investigating and handling outliers"
                })
                quality_score *= 0.95  # Small penalty for outliers
        
        # Check data types
        for col in data.columns:
            # Skip key columns if specified
            if keys and col in keys:
                continue
                
            if data[col].dtype == 'object':
                # Check for mixed types in string columns
                unique_types = data[col].apply(type).unique()
                if len(unique_types) > 1:
                    self.logger.debug(f"Found mixed types in column {col}: {unique_types}")
                    issues.append({
                        'type': 'mixed_types',
                        'severity': 'high',
                        'affected_columns': [col],
                        'description': f"Column {col} contains mixed data types: {unique_types}",
                        'recommendation': "Standardize data types in this column"
                    })
                    quality_score *= 0.7  # Significant penalty for mixed types
        
        self.logger.debug(f"Dataset {dataset_name} quality score: {quality_score:.2f}")
        self.logger.debug(f"Found {len(issues)} issues in dataset {dataset_name}")
        
        return {
            'quality_score': quality_score,
            'issues': issues,
            'statistics': {
                'row_count': len(data),
                'column_count': len(data.columns),
                'missing_value_count': data.isnull().sum().sum(),
                'duplicate_row_count': duplicates
            }
        }
    
    def _check_comparison_quality(self, data_a: pd.DataFrame, data_b: pd.DataFrame, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Check quality of comparison between two datasets.
        
        Args:
            data_a: First DataFrame
            data_b: Second DataFrame
            keys: Optional list of key columns to focus quality checks on
            
        Returns:
            Dictionary containing comparison quality score and issues
        """
        self.logger.debug("Checking comparison quality between datasets")
        self.logger.debug(f"Dataset A shape: {data_a.shape}, Dataset B shape: {data_b.shape}")
        if keys:
            self.logger.debug(f"Focusing comparison quality checks on key columns: {keys}")
        
        issues = []
        quality_score = 1.0  # Start with perfect score
        
        # Check for column mismatches
        cols_a = set(data_a.columns)
        cols_b = set(data_b.columns)
        missing_in_b = cols_a - cols_b
        missing_in_a = cols_b - cols_a
        
        # Log detailed column information
        self.logger.debug(f"Dataset A columns: {sorted(list(cols_a))}")
        self.logger.debug(f"Dataset B columns: {sorted(list(cols_b))}")
        if missing_in_b:
            self.logger.debug(f"Columns present in A but missing in B: {sorted(list(missing_in_b))}")
        if missing_in_a:
            self.logger.debug(f"Columns present in B but missing in A: {sorted(list(missing_in_a))}")
        
        # If keys are specified, prioritize checking those columns
        if keys:
            key_missing_in_b = missing_in_b.intersection(set(keys))
            key_missing_in_a = missing_in_a.intersection(set(keys))
            
            if key_missing_in_b or key_missing_in_a:
                self.logger.debug(f"Key column mismatches - Missing in B: {key_missing_in_b}, Missing in A: {key_missing_in_a}")
                self.logger.debug(f"Key columns in A: {sorted(list(set(keys).intersection(cols_a)))}")
                self.logger.debug(f"Key columns in B: {sorted(list(set(keys).intersection(cols_b)))}")
                issues.append({
                    'type': 'key_column_mismatch',
                    'severity': 'high',
                    'affected_columns': {
                        'missing_in_b': list(key_missing_in_b),
                        'missing_in_a': list(key_missing_in_a)
                    },
                    'description': "Datasets have different key columns",
                    'recommendation': "Align key columns between datasets"
                })
                quality_score *= 0.6  # Severe penalty for key column mismatches
            
            # Check non-key columns
            non_key_missing_in_b = missing_in_b - set(keys)
            non_key_missing_in_a = missing_in_a - set(keys)
            
            if non_key_missing_in_b or non_key_missing_in_a:
                self.logger.debug(f"Non-key column mismatches - Missing in B: {non_key_missing_in_b}, Missing in A: {non_key_missing_in_a}")
                issues.append({
                    'type': 'column_mismatch',
                    'severity': 'medium',
                    'affected_columns': {
                        'missing_in_b': list(non_key_missing_in_b),
                        'missing_in_a': list(non_key_missing_in_a)
                    },
                    'description': "Datasets have different non-key columns",
                    'recommendation': "Align column sets between datasets"
                })
                quality_score *= 0.8  # Moderate penalty for non-key column mismatches
        else:
            # Check all columns if no keys specified
            if missing_in_b or missing_in_a:
                self.logger.debug(f"Column mismatches - Missing in B: {missing_in_b}, Missing in A: {missing_in_a}")
                issues.append({
                    'type': 'column_mismatch',
                    'severity': 'high',
                    'affected_columns': {
                        'missing_in_b': list(missing_in_b),
                        'missing_in_a': list(missing_in_a)
                    },
                    'description': "Datasets have different columns",
                    'recommendation': "Align column sets between datasets"
                })
                quality_score *= 0.7  # Significant penalty for column mismatches
        
        # Check for type mismatches in common columns
        common_cols = cols_a.intersection(cols_b)
        
        # If keys are specified, prioritize checking those columns
        if keys:
            key_common_cols = common_cols.intersection(set(keys))
            for col in key_common_cols:
                if data_a[col].dtype != data_b[col].dtype:
                    self.logger.debug(f"Type mismatch in key column {col}: {data_a[col].dtype} vs {data_b[col].dtype}")
                    issues.append({
                        'type': 'key_type_mismatch',
                        'severity': 'high',
                        'affected_columns': [col],
                        'description': f"Key column {col} has different types: {data_a[col].dtype} vs {data_b[col].dtype}",
                        'recommendation': "Standardize data types for key columns between datasets"
                    })
                    quality_score *= 0.7  # Severe penalty for key type mismatches
            
            # Check non-key columns
            non_key_common_cols = common_cols - set(keys)
            for col in non_key_common_cols:
                if data_a[col].dtype != data_b[col].dtype:
                    self.logger.debug(f"Type mismatch in non-key column {col}: {data_a[col].dtype} vs {data_b[col].dtype}")
                    issues.append({
                        'type': 'type_mismatch',
                        'severity': 'medium',
                        'affected_columns': [col],
                        'description': f"Column {col} has different types: {data_a[col].dtype} vs {data_b[col].dtype}",
                        'recommendation': "Standardize data types between datasets"
                    })
                    quality_score *= 0.9  # Moderate penalty for non-key type mismatches
        else:
            # Check all columns if no keys specified
            for col in common_cols:
                if data_a[col].dtype != data_b[col].dtype:
                    self.logger.debug(f"Type mismatch in column {col}: {data_a[col].dtype} vs {data_b[col].dtype}")
                    issues.append({
                        'type': 'type_mismatch',
                        'severity': 'high',
                        'affected_columns': [col],
                        'description': f"Column {col} has different types: {data_a[col].dtype} vs {data_b[col].dtype}",
                        'recommendation': "Standardize data types between datasets"
                    })
                    quality_score *= 0.8  # Penalty for type mismatches
        
        # Check for value range mismatches in numeric columns
        numeric_cols = data_a.select_dtypes(include=['int64', 'float64']).columns
        numeric_cols = numeric_cols.intersection(data_b.select_dtypes(include=['int64', 'float64']).columns)
        
        # If keys are specified, prioritize checking those columns
        if keys:
            key_numeric_cols = numeric_cols.intersection(set(keys))
            for col in key_numeric_cols:
                min_a, max_a = data_a[col].min(), data_a[col].max()
                min_b, max_b = data_b[col].min(), data_b[col].max()
                
                if abs(min_a - min_b) > 0.05 * (max_a - min_a) or abs(max_a - max_b) > 0.05 * (max_a - min_a):
                    self.logger.debug(f"Value range mismatch in key column {col}")
                    self.logger.debug(f"Dataset A range: [{min_a}, {max_a}], Dataset B range: [{min_b}, {max_b}]")
                    issues.append({
                        'type': 'key_value_range_mismatch',
                        'severity': 'high',
                        'affected_columns': [col],
                        'description': f"Key column {col} has significantly different value ranges between datasets",
                        'recommendation': "Investigate and align value ranges for key columns"
                    })
                    quality_score *= 0.7  # Severe penalty for key value range mismatches
            
            # Check non-key columns
            non_key_numeric_cols = numeric_cols - set(keys)
            for col in non_key_numeric_cols:
                min_a, max_a = data_a[col].min(), data_a[col].max()
                min_b, max_b = data_b[col].min(), data_b[col].max()
                
                if abs(min_a - min_b) > 0.1 * (max_a - min_a) or abs(max_a - max_b) > 0.1 * (max_a - min_a):
                    self.logger.debug(f"Value range mismatch in non-key column {col}")
                    self.logger.debug(f"Dataset A range: [{min_a}, {max_a}], Dataset B range: [{min_b}, {max_b}]")
                    issues.append({
                        'type': 'value_range_mismatch',
                        'severity': 'medium',
                        'affected_columns': [col],
                        'description': f"Column {col} has significantly different value ranges between datasets",
                        'recommendation': "Investigate and align value ranges if appropriate"
                    })
                    quality_score *= 0.9  # Small penalty for non-key value range mismatches
        else:
            # Check all columns if no keys specified
            for col in numeric_cols:
                min_a, max_a = data_a[col].min(), data_a[col].max()
                min_b, max_b = data_b[col].min(), data_b[col].max()
                
                if abs(min_a - min_b) > 0.1 * (max_a - min_a) or abs(max_a - max_b) > 0.1 * (max_a - min_a):
                    self.logger.debug(f"Value range mismatch in column {col}")
                    self.logger.debug(f"Dataset A range: [{min_a}, {max_a}], Dataset B range: [{min_b}, {max_b}]")
                    issues.append({
                        'type': 'value_range_mismatch',
                        'severity': 'medium',
                        'affected_columns': [col],
                        'description': f"Column {col} has significantly different value ranges between datasets",
                        'recommendation': "Investigate and align value ranges if appropriate"
                    })
                    quality_score *= 0.9  # Small penalty for value range mismatches
        
        self.logger.debug(f"Comparison quality score: {quality_score:.2f}")
        self.logger.debug(f"Found {len(issues)} comparison issues")
        
        return {
            'quality_score': quality_score,
            'issues': issues,
            'statistics': {
                'common_columns': len(common_cols),
                'missing_columns': len(missing_in_a.union(missing_in_b)),
                'type_mismatches': sum(1 for col in common_cols if data_a[col].dtype != data_b[col].dtype)
            }
        } 