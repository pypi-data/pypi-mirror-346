"""
Key enrichment functionality for LlamaSee.

This module provides functionality for enriching keys with additional dimensional information.
It supports mapping-based enrichments where a key value maps to an enriched value.
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime


class KeyEnricher:
    """
    Enriches keys in datasets with additional dimensional information.
    
    This class takes a dataset and applies key enrichments based on mapping configurations.
    It maintains metadata about the enrichments applied for traceability.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the KeyEnricher.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.enrichment_metadata = {}
    
    def enrich_keys(self, dataset: pd.DataFrame, enrichment_configs: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Apply key enrichments to the dataset.
        
        Args:
            dataset: DataFrame to enrich
            enrichment_configs: List of enrichment configurations
            
        Returns:
            Enriched DataFrame with new enriched columns added (original data is preserved)
        """
        self.logger.info(f"Starting key enrichment with {len(enrichment_configs)} configurations")
        
        # Create a copy of the dataset to avoid modifying the original
        enriched_dataset = dataset.copy()
        
        # Apply each enrichment configuration
        for config in enrichment_configs:
            try:
                # Apply enrichment and get a new DataFrame with the enriched column
                enriched_dataset = self._apply_single_enrichment(enriched_dataset, config)
            except Exception as e:
                self.logger.error(f"Error applying enrichment: {str(e)}")
                # Continue with other enrichments even if one fails
        
        self.logger.info(f"Completed key enrichment. Applied {len(self.enrichment_metadata)} enrichments")
        return enriched_dataset
    
    def _apply_single_enrichment(self, dataset: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply a single key enrichment to the dataset.
        
        Args:
            dataset: DataFrame to enrich
            config: Enrichment configuration
            
        Returns:
            DataFrame with the enrichment applied
        """
        # Extract configuration parameters
        key_column = config.get("key_column")
        enriched_key = config.get("enriched_key")
        mappings = config.get("mappings", {})
        default_value = config.get("default_value", "Unknown")
        
        # Validate configuration
        if not key_column or not enriched_key or not mappings:
            raise ValueError(f"Invalid enrichment configuration: {config}")
        
        # Check if the key column exists in the dataset
        if key_column not in dataset.columns:
            self.logger.warning(f"Key column '{key_column}' not found in dataset. Skipping enrichment.")
            return dataset
        
        # Create the enriched key column
        enriched_column_name = f"dim_{enriched_key}"
        
        # Apply the mapping
        self.logger.debug(f"Applying enrichment: {key_column} -> {enriched_column_name}")
        self.logger.debug(f"Mappings: {mappings}")
        
        # Create a mapping function that returns a default value if key not found
        def map_value(value):
            # Convert to string for lookup
            str_value = str(value)
            mapped_value = mappings.get(str_value, default_value)
            self.logger.debug(f"Mapping {str_value} -> {mapped_value}")
            return mapped_value
        
        # Create a new DataFrame with the enriched column added
        enriched_dataset = dataset.copy()
        
        # Create the enriched column without modifying the original key column
        enriched_dataset[enriched_column_name] = enriched_dataset[key_column].apply(map_value)
        
        # Log the unique values in the enriched column
        unique_values = enriched_dataset[enriched_column_name].unique()
        self.logger.debug(f"Unique values in {enriched_column_name}: {unique_values}")
        
        # Store metadata about the enrichment
        self.enrichment_metadata[enriched_column_name] = {
            "original_key": key_column,
            "enriched_key": enriched_key,
            "enrichment_type": "mapping",
            "parameters": {
                "mappings": mappings,
                "default_value": default_value
            },
            "applied_at": datetime.now().isoformat()
        }
        
        self.logger.debug(f"Successfully applied enrichment: {key_column} -> {enriched_column_name}")
        return enriched_dataset
    
    def get_enrichment_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Get metadata about applied enrichments.
        
        Returns:
            Dictionary containing metadata about each enrichment
        """
        return self.enrichment_metadata
    
    @staticmethod
    def load_enrichment_config(file_path: str) -> Dict[str, Any]:
        """
        Load an enrichment configuration from a file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dictionary containing the enrichment configuration
        """
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_enrichment_config(config: Dict[str, Any], file_path: str) -> None:
        """
        Save an enrichment configuration to a file.
        
        Args:
            config: Enrichment configuration
            file_path: Path to save the configuration to
        """
        with open(file_path, 'w') as f:
            json.dump(config, f, indent=2) 