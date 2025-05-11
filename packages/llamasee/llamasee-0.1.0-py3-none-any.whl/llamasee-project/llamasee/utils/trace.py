"""
Trace functionality for LlamaSee.
"""
import json
from typing import Dict, Any, List, Optional, Union
import pandas as pd
from ..core.insight import Insight
import logging

class TraceManager:
    """
    Manages trace functionality for insights.
    
    This class provides methods for creating and managing traces that link
    insights to their source data.
    """
    
    @staticmethod
    def create_trace(data_indices=None, columns=None, values=None, context=None):
        """
        Create a trace object with the given information.
        
        Args:
            data_indices: Row indices in the original datasets
            columns: Column names
            values: Key-value pairs
            context: Additional context
            
        Returns:
            Dict: Trace object
        """
        trace = {
            'data_indices': data_indices or [],
            'columns': columns or [],
            'values': values or {},
            'context': context or {},
            'dataset_a': {
                'indices': [],
                'columns': [],
                'values': {}
            },
            'dataset_b': {
                'indices': [],
                'columns': [],
                'values': {}
            },
            'dimension_context': {},
            'comparison_context': {}
        }
        
        return trace
    
    @staticmethod
    def add_dataset_trace(trace, dataset, indices=None, columns=None, values=None):
        """
        Add dataset-specific trace information.
        
        Args:
            trace: Trace object
            dataset: Dataset identifier ('dataset_a' or 'dataset_b')
            indices: Row indices
            columns: Column names
            values: Key-value pairs
            
        Returns:
            Dict: Updated trace object
        """
        if dataset not in ['dataset_a', 'dataset_b']:
            logging.warning(f"Invalid dataset identifier: {dataset}")
            return trace
        
        if indices:
            trace[dataset]['indices'] = indices
        if columns:
            trace[dataset]['columns'] = columns
        if values:
            trace[dataset]['values'] = values
        
        return trace
    
    @staticmethod
    def add_dimension_trace(trace, dimension_id, dimension_value):
        """
        Add dimension-specific trace information.
        
        Args:
            trace: Trace object
            dimension_id: Dimension identifier
            dimension_value: Dimension value
            
        Returns:
            Dict: Updated trace object
        """
        trace['dimension_context'][dimension_id] = dimension_value
        return trace
    
    @staticmethod
    def add_comparison_trace(trace, comparison_type, comparison_value):
        """
        Add comparison-specific trace information.
        
        Args:
            trace: Trace object
            comparison_type: Comparison type
            comparison_value: Comparison value
            
        Returns:
            Dict: Updated trace object
        """
        trace['comparison_context'][comparison_type] = comparison_value
        return trace
    
    @staticmethod
    def get_highlight_data(insight, dataset_a=None, dataset_b=None):
        """
        Get data to highlight based on the trace.
        
        Args:
            insight: The insight with trace
            dataset_a: Dataset A to highlight
            dataset_b: Dataset B to highlight
            
        Returns:
            Dict[str, Any]: Data to highlight
        """
        if not insight.trace:
            return {}
        
        result = {
            'dataset_a': {},
            'dataset_b': {}
        }
        
        # Process dataset A
        if dataset_a is not None and 'dataset_a' in insight.trace:
            dataset_a_trace = insight.trace['dataset_a']
            indices = dataset_a_trace.get('indices', [])
            columns = dataset_a_trace.get('columns', [])
            
            if indices and columns:
                highlight_data = dataset_a.iloc[indices][columns].to_dict(orient='records')
                result['dataset_a'] = {
                    'indices': indices,
                    'columns': columns,
                    'data': highlight_data,
                    'values': dataset_a_trace.get('values', {})
                }
        
        # Process dataset B
        if dataset_b is not None and 'dataset_b' in insight.trace:
            dataset_b_trace = insight.trace['dataset_b']
            indices = dataset_b_trace.get('indices', [])
            columns = dataset_b_trace.get('columns', [])
            
            if indices and columns:
                highlight_data = dataset_b.iloc[indices][columns].to_dict(orient='records')
                result['dataset_b'] = {
                    'indices': indices,
                    'columns': columns,
                    'data': highlight_data,
                    'values': dataset_b_trace.get('values', {})
                }
        
        # Add dimension and comparison context
        result['dimension_context'] = insight.trace.get('dimension_context', {})
        result['comparison_context'] = insight.trace.get('comparison_context', {})
        
        return result
    
    @staticmethod
    def format_trace_for_llm(insight):
        """
        Format trace data for LLM consumption.
        
        Args:
            insight: The insight with trace
            
        Returns:
            str: Formatted trace data
        """
        if not insight.trace:
            return "No trace data available."
        
        trace_data = {
            'columns': insight.trace.get('columns', []),
            'values': insight.trace.get('values', {}),
            'context': insight.trace.get('context', {}),
            'dataset_a': insight.trace.get('dataset_a', {}),
            'dataset_b': insight.trace.get('dataset_b', {}),
            'dimension_context': insight.trace.get('dimension_context', {}),
            'comparison_context': insight.trace.get('comparison_context', {})
        }
        
        return json.dumps(trace_data, indent=2)
    
    @staticmethod
    def get_trace_summary(insight):
        """
        Get a summary of the trace.
        
        Args:
            insight: The insight with trace
            
        Returns:
            str: Trace summary
        """
        if not insight.trace:
            return "No trace data available."
        
        summary = []
        
        # General trace information
        columns = insight.trace.get('columns', [])
        values = insight.trace.get('values', {})
        context = insight.trace.get('context', {})
        
        if columns:
            summary.append(f"Columns: {', '.join(columns)}")
        
        if values:
            summary.append("Values:")
            for key, value in values.items():
                summary.append(f"  - {key}: {value}")
        
        if context:
            summary.append("Context:")
            for key, value in context.items():
                summary.append(f"  - {key}: {value}")
        
        # Dataset-specific information
        for dataset in ['dataset_a', 'dataset_b']:
            dataset_trace = insight.trace.get(dataset, {})
            if dataset_trace:
                dataset_name = "Dataset A" if dataset == 'dataset_a' else "Dataset B"
                summary.append(f"{dataset_name}:")
                
                indices = dataset_trace.get('indices', [])
                if indices:
                    summary.append(f"  - Indices: {indices}")
                
                columns = dataset_trace.get('columns', [])
                if columns:
                    summary.append(f"  - Columns: {', '.join(columns)}")
                
                values = dataset_trace.get('values', {})
                if values:
                    summary.append("  - Values:")
                    for key, value in values.items():
                        summary.append(f"    - {key}: {value}")
        
        # Dimension context
        dimension_context = insight.trace.get('dimension_context', {})
        if dimension_context:
            summary.append("Dimension Context:")
            for dimension_id, dimension_value in dimension_context.items():
                summary.append(f"  - {dimension_id}: {dimension_value}")
        
        # Comparison context
        comparison_context = insight.trace.get('comparison_context', {})
        if comparison_context:
            summary.append("Comparison Context:")
            for comparison_type, comparison_value in comparison_context.items():
                summary.append(f"  - {comparison_type}: {comparison_value}")
        
        return "\n".join(summary) 