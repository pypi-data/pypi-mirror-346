"""
Schema analysis and management for LlamaSee.

This module provides functionality for automatically detecting and classifying
columns in datasets as keys, values, or dimensions.
"""

from .schema_analysis import (
    ColumnType,
    ColumnInfo,
    SchemaAnalyzer
)
from .key_enricher import KeyEnricher

__all__ = [
    'ColumnType',
    'ColumnInfo',
    'SchemaAnalyzer',
    'KeyEnricher'
] 