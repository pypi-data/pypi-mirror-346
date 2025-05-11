"""
Insight Manager module for LlamaSee.

This module provides a high-level interface for generating, storing, and retrieving insights.
It integrates the insight generator with various storage backends.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

from ..core.insight import Insight
from ..generation.insight_generator import InsightGenerator
from ..storage.insight_storage import create_insight_storage

logger = logging.getLogger(__name__)

class InsightManager:
    """
    High-level interface for managing insights in LlamaSee.
    
    This class integrates insight generation with storage backends, providing
    a unified interface for generating, storing, and retrieving insights.
    """
    
    def __init__(
        self,
        insight_config: Optional[Dict[str, Any]] = None,
        storage_type: str = "file",
        storage_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the InsightManager.
        
        Args:
            insight_config: Configuration for insight generation
            storage_type: Type of storage backend to use ("file", "csv", or "sqlite")
            storage_config: Configuration for the storage backend
        """
        self.insight_generator = InsightGenerator(insight_config)
        self.storage = create_insight_storage(storage_type=storage_type, **(storage_config or {}))
        logger.info(f"Initialized InsightManager with {storage_type} storage")
    
    def generate_and_save_insights(
        self,
        comparison_results: Dict[str, Any],
        scope: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        top_n: int = 5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate insights from comparison results and save them to storage.
        
        Args:
            comparison_results: Results from data comparison
            scope: Scope information about the comparison
            context: Additional context for insight generation
            top_n: Number of top insights to generate
            metadata: Additional metadata to store with the insights
            
        Returns:
            str: Identifier for the saved insights
        """
        # Generate insights
        insights = self.insight_generator.generate_insights(
            comparison_results=comparison_results,
            scope=scope,
            context=context,
            top_n=top_n
        )
        
        # Prepare metadata
        batch_metadata = {
            "timestamp": datetime.now().isoformat(),
            "insight_count": len(insights),
            "comparison_id": context.get("comparison_id") if context else None,
            "description": context.get("description") if context else None
        }
        
        if metadata:
            batch_metadata.update(metadata)
        
        # Save insights
        batch_id = self.storage.save_insights(insights, batch_metadata)
        logger.info(f"Saved {len(insights)} insights with batch ID: {batch_id}")
        
        return batch_id
    
    def load_insights(self, batch_id: str) -> List[Insight]:
        """
        Load insights from storage by batch ID.
        
        Args:
            batch_id: Identifier for the batch of insights
            
        Returns:
            List[Insight]: List of loaded insights
        """
        insights = self.storage.load_insights(batch_id)
        logger.info(f"Loaded {len(insights)} insights for batch ID: {batch_id}")
        return insights
    
    def list_saved_insights(self) -> List[Dict[str, Any]]:
        """
        List all saved insight batches with their metadata.
        
        Returns:
            List[Dict[str, Any]]: List of metadata for saved insight batches
        """
        return self.storage.list_saved_insights()
    
    def delete_insights(self, batch_id: str) -> bool:
        """
        Delete insights from storage by batch ID.
        
        Args:
            batch_id: Identifier for the batch of insights to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        success = self.storage.delete_insights(batch_id)
        if success:
            logger.info(f"Deleted insights for batch ID: {batch_id}")
        else:
            logger.warning(f"Failed to delete insights for batch ID: {batch_id}")
        return success
    
    def get_insight_by_id(self, insight_id: str, batch_id: Optional[str] = None) -> Optional[Insight]:
        """
        Get a specific insight by its ID, optionally filtering by batch ID.
        
        Args:
            insight_id: ID of the insight to retrieve
            batch_id: Optional batch ID to filter by
            
        Returns:
            Optional[Insight]: The requested insight, or None if not found
        """
        return self.storage.get_insight_by_id(insight_id, batch_id)
    
    def export_insights_to_csv(
        self,
        batch_id: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Export insights to a CSV file.
        
        Args:
            batch_id: Identifier for the batch of insights to export
            output_path: Optional path for the output CSV file
            
        Returns:
            str: Path to the exported CSV file
        """
        insights = self.load_insights(batch_id)
        
        # Prepare data for CSV export
        data = []
        for insight in insights:
            row = {
                "id": insight.id,
                "description": insight.description,
                "importance_score": insight.importance_score,
                "insight_type": insight.insight_type,
                "scope_level": insight.scope_level,
                "dimensions": ",".join(insight.dimensions),
                "magnitude": insight.magnitude,
                "frequency": insight.frequency,
                "business_impact": insight.business_impact,
                "uniqueness": insight.uniqueness,
                "weighted_score": insight.weighted_score
            }
            data.append(row)
        
        # Create DataFrame and save to CSV
        import pandas as pd
        df = pd.DataFrame(data)
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"insights_export_{batch_id}_{timestamp}.csv"
        
        df.to_csv(output_path, index=False)
        logger.info(f"Exported {len(insights)} insights to: {output_path}")
        
        return output_path 