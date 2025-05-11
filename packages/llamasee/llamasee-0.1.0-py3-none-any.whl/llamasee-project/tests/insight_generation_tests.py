#!/usr/bin/env python3
"""
Tests for the insight generation functionality.
"""

import os
import sys
import unittest
import logging
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from llamasee.generation.insight_generator import InsightGenerator
from llamasee.plugins.manager import PluginManager
from llamasee.plugins.insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin
from llamasee.generation.insight_generator import Insight

# Configure logging
logger = logging.getLogger(__name__)

class TestInsightGeneration(unittest.TestCase):
    """Test cases for insight generation functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a mock plugin manager
        self.plugin_manager = MagicMock(spec=PluginManager)
        
        # Create mock plugins
        self.data_science_plugin = MagicMock(spec=InsightPlugin)
        self.data_structure_plugin = MagicMock(spec=InsightPlugin)
        self.context_plugin = MagicMock(spec=InsightPlugin)
        
        # Set up plugin return values
        self.data_science_plugin.get_insight_types.return_value = ["data_science"]
        self.data_structure_plugin.get_insight_types.return_value = ["data_structure"]
        self.context_plugin.get_insight_types.return_value = ["context"]
        
        # Add the missing methods to the mock plugins
        self.data_science_plugin.generate_insights = MagicMock()
        self.data_science_plugin.enhance_insight = MagicMock()
        self.data_science_plugin.categorize_insight = MagicMock()
        self.data_science_plugin.score_insight = MagicMock()
        
        self.data_structure_plugin.generate_insights = MagicMock()
        self.data_structure_plugin.enhance_insight = MagicMock()
        self.data_structure_plugin.categorize_insight = MagicMock()
        self.data_structure_plugin.score_insight = MagicMock()
        
        self.context_plugin.generate_insights = MagicMock()
        self.context_plugin.enhance_insight = MagicMock()
        self.context_plugin.categorize_insight = MagicMock()
        self.context_plugin.score_insight = MagicMock()
        
        # Register the plugins with the plugin manager
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_science_plugin]
        
        # Add the get_all_insight_plugins method to the mock
        self.plugin_manager.get_all_insight_plugins = MagicMock(return_value=[
            self.data_science_plugin,
            self.data_structure_plugin,
            self.context_plugin
        ])
        
        # Create a mock insight generator
        self.insight_generator = InsightGenerator(plugin_manager=self.plugin_manager)
        
        # Create sample comparison results
        self.comparison_results = self.create_sample_comparison_results()
        
        # Create sample context data
        self.context_data = self.create_sample_context_data()
    
    def create_sample_comparison_results(self):
        """Create sample comparison results for testing."""
        # Create a sample DataFrame for comparison results
        data = {
            "sku": ["100443204", "100443204", "100443204", "100443204", "100443204"],
            "store_id": ["STORE-13360597", "STORE-13360597", "STORE-13360597", "STORE-13360597", "STORE-13360597"],
            "forecast_date": ["2025-03-08", "2025-03-09", "2025-03-10", "2025-03-11", "2025-03-12"],
            "forecast_period": ["2025-03-08", "2025-03-09", "2025-03-10", "2025-03-11", "2025-03-12"],
            "forecast_value_p50_a": [27356.0, 18400.0, 6159.0, 7564.0, 8797.0],
            "forecast_value_p10_a": [19610.0, 9962.0, 0.0, 0.0, 1169.0],
            "forecast_value_p90_a": [34842.0, 26316.0, 14147.0, 15437.0, 16262.0],
            "forecast_value_p50_b": [27356.0, 18400.0, 6159.0, 7564.0, 8797.0],
            "forecast_value_p10_b": [19610.0, 9962.0, 0.0, 0.0, 1169.0],
            "forecast_value_p90_b": [34842.0, 26316.0, 14147.0, 15437.0, 16262.0],
            "difference_p50": [0.0, 0.0, 0.0, 0.0, 0.0],
            "difference_p10": [0.0, 0.0, 0.0, 0.0, 0.0],
            "difference_p90": [0.0, 0.0, 0.0, 0.0, 0.0],
            "percent_diff_p50": [0.0, 0.0, 0.0, 0.0, 0.0],
            "percent_diff_p10": [0.0, 0.0, 0.0, 0.0, 0.0],
            "percent_diff_p90": [0.0, 0.0, 0.0, 0.0, 0.0]
        }
        
        df = pd.DataFrame(data)
        
        # Create a dictionary with the DataFrame and metadata
        comparison_results = {
            "data": df,
            "metadata": {
                "dimensions": {
                    "time": ["forecast_date"],
                    "product": ["sku"],
                    "location": ["store_id"]
                },
                "value_columns": ["forecast_value_p50", "forecast_value_p10", "forecast_value_p90"],
                "dataset_a": "ForecastResults_run_1",
                "dataset_b": "ForecastResults_run_2"
            }
        }
        
        return comparison_results
    
    def create_sample_context_data(self):
        """Create sample context data for testing."""
        context_data = {
            "objective": "To compare the performance of the two datasets",
            "background": "The two datasets are from the same source, but they are different because they are from different time periods",
            "domain": "The domain of the two datasets is the same, but they are different because they are from different time periods.",
            "key_metrics": ["metric1", "metric2", "metric3"],
            "constraints": ["WE have seen product shortages", "Unexpected weather caused lower foot traffic in some region", "constraint3"]
        }
        
        return context_data
    
    def test_basic_insight_generation(self):
        """Test basic insight generation."""
        # Set up the data science plugin to return a sample insight
        sample_insight = Insight(
            id="test_insight_1",
            description="Test insight",
            importance_score=0.8,
            source_data={"type": "data_science", "value": "test value"}
        )
        
        # Set additional attributes
        sample_insight.insight_type = "data_science"
        sample_insight.insight_subtype = "statistical"
        sample_insight.scope_level = "aggregate"
        sample_insight.scope_details = {"dimension": "time"}
        sample_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        self.data_science_plugin.generate_insights.return_value = [sample_insight]
        
        # Generate insights
        insights = self.insight_generator.generate_insights(self.comparison_results, self.context_data)
        
        # Verify that insights are generated
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0].id, "test_insight_1")
        self.assertEqual(insights[0].insight_type, "data_science")
        self.assertEqual(insights[0].scope_level, "aggregate")
    
    def test_data_science_insight_generation(self):
        """Test data science insight generation."""
        # Set up the data science plugin to return sample insights
        statistical_insight = Insight(
            id="statistical_insight",
            description="Statistical insight",
            importance_score=0.8,
            source_data={"type": "data_science", "value": "statistical value"}
        )
        statistical_insight.insight_type = "data_science"
        statistical_insight.insight_subtype = "statistical"
        statistical_insight.scope_level = "aggregate"
        statistical_insight.scope_details = {"dimension": "time"}
        statistical_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        trend_insight = Insight(
            id="trend_insight",
            description="Trend insight",
            importance_score=0.7,
            source_data={"type": "data_science", "value": "trend value"}
        )
        trend_insight.insight_type = "data_science"
        trend_insight.insight_subtype = "trend"
        trend_insight.scope_level = "dimension"
        trend_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-08"}
        trend_insight.trace = {
            "data_indices": {"dataset_a": [0], "dataset_b": [0]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        anomaly_insight = Insight(
            id="anomaly_insight",
            description="Anomaly insight",
            importance_score=0.9,
            source_data={"type": "data_science", "value": "anomaly value"}
        )
        anomaly_insight.insight_type = "data_science"
        anomaly_insight.insight_subtype = "anomaly"
        anomaly_insight.scope_level = "individual"
        anomaly_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-10"}
        anomaly_insight.trace = {
            "data_indices": {"dataset_a": [2], "dataset_b": [2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-10"}
        }
        
        self.data_science_plugin.generate_insights.return_value = [
            statistical_insight,
            trend_insight,
            anomaly_insight
        ]
        
        # Set up the plugin manager to return only the data science plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_science_plugin]
        
        # Generate insights
        insights = self.insight_generator.generate_insights(self.comparison_results, self.context_data)
        
        # Verify that data science insights are generated
        self.assertEqual(len(insights), 3)
        
        # Verify that each insight type is represented
        insight_types = [insight.insight_subtype for insight in insights]
        self.assertIn("statistical", insight_types)
        self.assertIn("trend", insight_types)
        self.assertIn("anomaly", insight_types)
        
        # Verify that each scope level is represented
        scope_levels = [insight.scope_level for insight in insights]
        self.assertIn("aggregate", scope_levels)
        self.assertIn("dimension", scope_levels)
        self.assertIn("individual", scope_levels)
    
    def test_data_structure_insight_generation(self):
        """Test data structure insight generation."""
        # Set up the data structure plugin to return sample insights
        column_insight = Insight(
            id="column_insight",
            description="Column insight",
            importance_score=0.8,
            source_data={"type": "data_structure", "value": "column value"}
        )
        column_insight.insight_type = "data_structure"
        column_insight.insight_subtype = "column"
        column_insight.scope_level = "aggregate"
        column_insight.scope_details = {"dimension": "time"}
        column_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        key_insight = Insight(
            id="key_insight",
            description="Key insight",
            importance_score=0.7,
            source_data={"type": "data_structure", "value": "key value"}
        )
        key_insight.insight_type = "data_structure"
        key_insight.insight_subtype = "key"
        key_insight.scope_level = "dimension"
        key_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-08"}
        key_insight.trace = {
            "data_indices": {"dataset_a": [0], "dataset_b": [0]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        schema_insight = Insight(
            id="schema_insight",
            description="Schema insight",
            importance_score=0.9,
            source_data={"type": "data_structure", "value": "schema value"}
        )
        schema_insight.insight_type = "data_structure"
        schema_insight.insight_subtype = "schema"
        schema_insight.scope_level = "aggregate"
        schema_insight.scope_details = {"dimension": "time"}
        schema_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        self.data_structure_plugin.generate_insights.return_value = [
            column_insight,
            key_insight,
            schema_insight
        ]
        
        # Set up the plugin manager to return only the data structure plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_structure_plugin]
        
        # Generate insights
        insights = self.insight_generator.generate_insights(self.comparison_results, self.context_data)
        
        # Verify that data structure insights are generated
        self.assertEqual(len(insights), 3)
        
        # Verify that each insight type is represented
        insight_types = [insight.insight_subtype for insight in insights]
        self.assertIn("column", insight_types)
        self.assertIn("key", insight_types)
        self.assertIn("schema", insight_types)
    
    def test_context_insight_generation(self):
        """Test context insight generation."""
        # Set up the context plugin to return sample insights
        business_insight = Insight(
            id="business_insight",
            description="Business insight",
            importance_score=0.85,
            source_data={"type": "context", "value": "business value"}
        )
        business_insight.insight_type = "context"
        business_insight.insight_subtype = "business"
        business_insight.scope_level = "aggregate"
        business_insight.scope_details = {"dimension": "time"}
        business_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        domain_insight = Insight(
            id="domain_insight",
            description="Domain insight",
            importance_score=0.75,
            source_data={"type": "context", "value": "domain value"}
        )
        domain_insight.insight_type = "context"
        domain_insight.insight_subtype = "domain"
        domain_insight.scope_level = "dimension"
        domain_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-08"}
        domain_insight.trace = {
            "data_indices": {"dataset_a": [0], "dataset_b": [0]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        self.context_plugin.generate_insights.return_value = [
            business_insight,
            domain_insight
        ]
        
        # Set up the plugin manager to return only the context plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.context_plugin]
        
        # Generate insights
        insights = self.insight_generator.generate_insights(self.comparison_results, self.context_data)
        
        # Verify that context insights are generated
        self.assertEqual(len(insights), 2)
        
        # Verify that each insight type is represented
        insight_types = [insight.insight_subtype for insight in insights]
        self.assertIn("business", insight_types)
        self.assertIn("domain", insight_types)
    
    def test_insight_enhancement(self):
        """Test insight enhancement."""
        # Create a base insight
        base_insight = Insight(
            id="base_insight",
            description="Base insight",
            importance_score=0.7,
            source_data={"type": "data_science", "value": "base value"}
        )
        base_insight.insight_type = "data_science"
        base_insight.insight_subtype = "statistical"
        base_insight.scope_level = "aggregate"
        base_insight.scope_details = {"dimension": "time"}
        base_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the data science plugin to return the enhanced insight
        enhanced_insight = Insight(
            id="enhanced_insight",
            description="Enhanced insight",
            importance_score=0.85,
            source_data={"type": "data_science", "value": "enhanced value"}
        )
        enhanced_insight.insight_type = "data_science"
        enhanced_insight.insight_subtype = "statistical"
        enhanced_insight.scope_level = "aggregate"
        enhanced_insight.scope_details = {"dimension": "time"}
        enhanced_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the plugin manager to return only the data science plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_science_plugin]
        
        # Set up the data science plugin to return the enhanced insight
        self.data_science_plugin.generate_insights.return_value = [enhanced_insight]
        
        # Generate insights using the insight generator
        insights = self.insight_generator.generate_insights(
            self.comparison_results, 
            {"overlap_percentage": 100, "common_columns": ["forecast_value_p50"]}, 
            self.context_data
        )
        
        # Verify that the insight was enhanced
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0].id, "enhanced_insight")
        self.assertEqual(insights[0].description, "Enhanced insight")
        self.assertEqual(insights[0].importance_score, 0.85)
        self.assertEqual(insights[0].source_data["value"], "enhanced value")
        self.assertEqual(insights[0].insight_type, "data_science")
        self.assertEqual(insights[0].scope_level, "aggregate")
    
    def test_insight_categorization(self):
        """Test insight categorization."""
        # Create a base insight
        base_insight = Insight(
            id="base_insight",
            description="Base insight",
            importance_score=0.7,
            source_data={"type": "data_science", "value": "base value"}
        )
        base_insight.insight_type = "data_science"
        base_insight.insight_subtype = "statistical"
        base_insight.scope_level = "aggregate"
        base_insight.scope_details = {"dimension": "time"}
        base_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the data science plugin to return the categorized insight
        categorized_insight = Insight(
            id="categorized_insight",
            description="Categorized insight",
            importance_score=0.85,
            source_data={"type": "data_science", "value": "categorized value"}
        )
        categorized_insight.insight_type = "data_science"
        categorized_insight.insight_subtype = "statistical"
        categorized_insight.scope_level = "aggregate"
        categorized_insight.scope_details = {"dimension": "time"}
        categorized_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the plugin manager to return only the data science plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_science_plugin]
        
        # Set up the data science plugin to return the categorized insight
        self.data_science_plugin.generate_insights.return_value = [categorized_insight]
        
        # Generate insights using the insight generator
        insights = self.insight_generator.generate_insights(
            self.comparison_results, 
            {"overlap_percentage": 100, "common_columns": ["forecast_value_p50"]}, 
            self.context_data
        )
        
        # Verify that the insight was categorized
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0].id, "categorized_insight")
        self.assertEqual(insights[0].description, "Categorized insight")
        self.assertEqual(insights[0].importance_score, 0.85)
        self.assertEqual(insights[0].source_data["value"], "categorized value")
        self.assertEqual(insights[0].insight_type, "data_science")
        self.assertEqual(insights[0].scope_level, "aggregate")
    
    def test_insight_scoring(self):
        """Test insight scoring."""
        # Create a base insight
        base_insight = Insight(
            id="base_insight",
            description="Base insight",
            importance_score=0.7,
            source_data={"type": "data_science", "value": "base value"}
        )
        base_insight.insight_type = "data_science"
        base_insight.insight_subtype = "statistical"
        base_insight.scope_level = "aggregate"
        base_insight.scope_details = {"dimension": "time"}
        base_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the data science plugin to return the scored insight
        scored_insight = Insight(
            id="scored_insight",
            description="Scored insight",
            importance_score=0.9,
            source_data={"type": "data_science", "value": "scored value"}
        )
        scored_insight.insight_type = "data_science"
        scored_insight.insight_subtype = "statistical"
        scored_insight.scope_level = "aggregate"
        scored_insight.scope_details = {"dimension": "time"}
        scored_insight.trace = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Set up the plugin manager to return only the data science plugin
        self.plugin_manager.get_insight_plugins_by_type.return_value = [self.data_science_plugin]
        
        # Set up the data science plugin to return the scored insight
        self.data_science_plugin.generate_insights.return_value = [scored_insight]
        
        # Generate insights using the insight generator
        insights = self.insight_generator.generate_insights(
            self.comparison_results, 
            {"overlap_percentage": 100, "common_columns": ["forecast_value_p50"]}, 
            self.context_data
        )
        
        # Verify that the insight was scored
        self.assertEqual(len(insights), 1)
        self.assertEqual(insights[0].id, "scored_insight")
        self.assertEqual(insights[0].description, "Scored insight")
        self.assertEqual(insights[0].importance_score, 0.9)
        self.assertEqual(insights[0].source_data["value"], "scored value")
        self.assertEqual(insights[0].insight_type, "data_science")
        self.assertEqual(insights[0].scope_level, "aggregate")
        self.assertTrue(hasattr(insights[0], 'weighted_score'))

if __name__ == "__main__":
    unittest.main() 