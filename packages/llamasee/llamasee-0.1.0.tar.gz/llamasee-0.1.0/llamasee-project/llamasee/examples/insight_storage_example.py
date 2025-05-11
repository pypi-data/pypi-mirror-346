#!/usr/bin/env python
"""
Example script demonstrating how to use the LlamaSee insight storage system.

This script shows how to:
1. Generate insights from comparison results
2. Save insights to different storage backends
3. Load and retrieve insights
4. Export insights to CSV
"""

import os
import json
import logging
from pathlib import Path

from llamasee.integration.insight_manager import InsightManager
from llamasee.core.insight import Insight

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_comparison_results():
    """Create sample comparison results for demonstration."""
    return {
        "sales": {
            "summary": {
                "mean_percentage_diff": 15.7,
                "mean_absolute_diff": 1250.0,
                "max_percentage_diff": 45.2,
                "min_percentage_diff": -12.3
            },
            "trends": {
                "trend_similarity": 0.85,
                "trend_direction": "similar"
            },
            "anomalies": {
                "total_anomalies": 8,
                "anomalies": {
                    "store_123_product_456": {
                        "difference": {
                            "percentage_diff": 35.7
                        },
                        "key_components": {
                            "store_id": "123",
                            "product_id": "456"
                        },
                        "reason": "Unusual spike in sales"
                    }
                }
            },
            "dimension_insights": {
                "region": {
                    "significant_values": {
                        "north": {
                            "mean_percentage_diff": 25.3,
                            "raw_percentage_diff": 22.1,
                            "diff_sum_positive": 1500.0,
                            "diff_sum_negative": -300.0,
                            "net_diff": 1200.0,
                            "raw_sum_a": 5000.0,
                            "raw_sum_b": 6100.0
                        }
                    }
                }
            }
        },
        "key_differences": {
            "max_diff_dimension": "region",
            "max_diff_value": 15,
            "dimension_differences": {
                "region": 15,
                "product_category": 8,
                "store_type": 3
            }
        }
    }

def create_sample_scope():
    """Create sample scope information for demonstration."""
    return {
        "overlap_percentage": 85.0,
        "common_columns": ["id", "date", "store_id", "product_id", "sales", "region"],
        "unique_to_a": ["customer_id", "loyalty_score"],
        "unique_to_b": ["inventory_level", "promotion_flag"],
        "key_overlap": {
            "overlap_percentage": 90.0,
            "common_keys": ["store_id", "product_id"],
            "unique_to_a": ["store_id", "product_id", "date_2023"],
            "unique_to_b": ["store_id", "product_id", "date_2024"]
        },
        "overlap": {
            "region": {
                "overlap_percentage": 95.0,
                "common_values": ["north", "south", "east", "west"],
                "unique_to_a": ["central"],
                "unique_to_b": []
            }
        }
    }

def main():
    """Run the example."""
    logger.info("Starting insight storage example")
    
    # Create sample data
    comparison_results = create_sample_comparison_results()
    scope = create_sample_scope()
    context = {
        "comparison_id": "sample_comparison_001",
        "description": "Sales data comparison between 2023 and 2024"
    }
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Example 1: File-based storage
    logger.info("\n=== Example 1: File-based storage ===")
    file_storage_manager = InsightManager(storage_type="file", storage_config={"storage_dir": "output/file_storage"})
    
    file_identifier = file_storage_manager.generate_and_save_insights(
        comparison_results=comparison_results,
        scope=scope,
        context=context,
        top_n=5
    )
    
    logger.info(f"Saved insights to file with identifier: {file_identifier}")
    
    # Load and display insights
    file_insights = file_storage_manager.load_insights(file_identifier)
    logger.info(f"Loaded {len(file_insights)} insights from file storage")
    
    for i, insight in enumerate(file_insights, 1):
        logger.info(f"Insight {i}: {insight.description} (Score: {insight.weighted_score:.2f})")
    
    # Example 2: CSV-based storage
    logger.info("\n=== Example 2: CSV-based storage ===")
    csv_storage_manager = InsightManager(storage_type="csv", storage_config={"storage_dir": "output/csv_storage"})
    
    csv_identifier = csv_storage_manager.generate_and_save_insights(
        comparison_results=comparison_results,
        scope=scope,
        context=context,
        top_n=5
    )
    
    logger.info(f"Saved insights to CSV with identifier: {csv_identifier}")
    
    # Export to CSV
    export_path = csv_storage_manager.export_insights_to_csv(csv_identifier, "output/exported_insights.csv")
    logger.info(f"Exported insights to: {export_path}")
    
    # Example 3: SQLite-based storage
    logger.info("\n=== Example 3: SQLite-based storage ===")
    sqlite_storage_manager = InsightManager(storage_type="sqlite", storage_config={"db_path": "output/insights.db"})
    
    sqlite_identifier = sqlite_storage_manager.generate_and_save_insights(
        comparison_results=comparison_results,
        scope=scope,
        context=context,
        top_n=5
    )
    
    logger.info(f"Saved insights to SQLite with identifier: {sqlite_identifier}")
    
    # List saved insights
    saved_insights = sqlite_storage_manager.list_saved_insights()
    logger.info(f"Found {len(saved_insights)} saved insight sets in SQLite storage")
    
    for i, batch in enumerate(saved_insights, 1):
        logger.info(f"Batch {i}: {batch.get('batch_id', 'unknown')} - {batch.get('insight_count', 0)} insights")
    
    # Example 4: Get insight by ID
    logger.info("\n=== Example 4: Get insight by ID ===")
    if file_insights:
        insight_id = file_insights[0].id
        insight = file_storage_manager.get_insight_by_id(insight_id)
        
        if insight:
            logger.info(f"Found insight by ID: {insight.description}")
        else:
            logger.warning(f"Insight with ID {insight_id} not found")
    
    logger.info("\nInsight storage example completed successfully")

if __name__ == "__main__":
    main() 