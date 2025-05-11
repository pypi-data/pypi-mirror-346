#!/usr/bin/env python3
"""
Tests for the insight storage functionality.
"""

import os
import sys
import unittest
import logging
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from llamasee.core.insight import Insight
from llamasee.storage.insight_storage import InsightStorage, CSVInsightStorage, SQLiteInsightStorage

# Configure logging
logger = logging.getLogger(__name__)

class TestInsightStorage(unittest.TestCase):
    """Test cases for insight storage functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Use the specified storage directory
        self.storage_dir = Path("/Users/gpt2s/Desktop/Projects/LlamaSee/LlamaSee/llamasee-project/llamaseeStorage")
        
        # Create a test results directory
        self.test_results_dir = Path("/Users/gpt2s/Desktop/Projects/LlamaSee/LlamaSee/llamasee-project/test-results")
        os.makedirs(self.test_results_dir, exist_ok=True)
        
        # Create a mock database backend
        self.db_backend = MagicMock(spec=SQLiteInsightStorage)
        
        # Create a file backend
        self.file_backend = CSVInsightStorage(storage_dir=self.storage_dir)
        
        # Create an insight storage with both backends
        self.insight_storage = InsightStorage(
            file_backend=self.file_backend,
            database_backend=self.db_backend
        )
        
        # Create sample insights
        self.sample_insights = self.create_sample_insights()
    
    def tearDown(self):
        """Clean up the test environment."""
        # Clean up any test files created during the tests
        for file in self.storage_dir.glob("insights_*.csv"):
            try:
                file.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete test file {file}: {str(e)}")
        
        for file in self.storage_dir.glob("metadata_*.json"):
            try:
                file.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete test file {file}: {str(e)}")
    
    def create_sample_insights(self):
        """Create sample insights for testing."""
        # Create a statistical insight
        statistical_insight = Insight(
            id="statistical_insight",
            description="Statistical insight",
            importance_score=0.8,
            source_data={"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]}
        )
        statistical_insight.insight_type = "data_science"
        statistical_insight.insight_subtype = "statistical"
        statistical_insight.scope_level = "aggregate"
        statistical_insight.scope_details = {"dimension": "time"}
        statistical_insight.trace_data = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Create a trend insight
        trend_insight = Insight(
            id="trend_insight",
            description="Trend insight",
            importance_score=0.7,
            source_data={"dataset_a": [0], "dataset_b": [0]}
        )
        trend_insight.insight_type = "data_science"
        trend_insight.insight_subtype = "trend"
        trend_insight.scope_level = "dimension"
        trend_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-08"}
        trend_insight.trace_data = {
            "data_indices": {"dataset_a": [0], "dataset_b": [0]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Create an anomaly insight
        anomaly_insight = Insight(
            id="anomaly_insight",
            description="Anomaly insight",
            importance_score=0.9,
            source_data={"dataset_a": [2], "dataset_b": [2]}
        )
        anomaly_insight.insight_type = "data_science"
        anomaly_insight.insight_subtype = "anomaly"
        anomaly_insight.scope_level = "individual"
        anomaly_insight.scope_details = {"dimension": "time", "dimension_value": "2025-03-10"}
        anomaly_insight.trace_data = {
            "data_indices": {"dataset_a": [2], "dataset_b": [2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-10"}
        }
        
        return [statistical_insight, trend_insight, anomaly_insight]
    
    def test_save_insights_file_backend(self):
        """Test saving insights using the file backend."""
        # Save the insights
        self.file_backend.save_insights(self.sample_insights)
        
        # Get the list of saved insights
        saved_insights_list = self.file_backend.list_saved_insights()
        
        # Verify that at least one insight file was saved
        self.assertGreater(len(saved_insights_list), 0)
        
        # Get the filepath from the first saved insight
        filepath = saved_insights_list[0]["filepath"]
        
        # Verify that the insights are stored in the file backend
        stored_insights = self.file_backend.load_insights(filepath)
        
        # Verify that the correct number of insights are stored
        self.assertEqual(len(stored_insights), 3)
        
        # Verify that each insight is stored correctly
        for insight in stored_insights:
            self.assertIn(insight.id, ["statistical_insight", "trend_insight", "anomaly_insight"])
            
            if insight.id == "statistical_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "statistical")
                self.assertEqual(insight.scope_level, "aggregate")
            elif insight.id == "trend_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "trend")
                self.assertEqual(insight.scope_level, "dimension")
            elif insight.id == "anomaly_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "anomaly")
                self.assertEqual(insight.scope_level, "individual")
    
    def test_save_insights_database_backend(self):
        """Test saving insights using the database backend."""
        # Set up the database backend to return the sample insights
        self.db_backend.save_insights.return_value = "test_batch_id"
        self.db_backend.load_insights.return_value = self.sample_insights
        
        # Save the insights
        batch_id = self.db_backend.save_insights(self.sample_insights)
        
        # Verify that the insights are stored in the database backend
        stored_insights = self.db_backend.load_insights(batch_id)
        
        # Verify that the correct number of insights are stored
        self.assertEqual(len(stored_insights), 3)
        
        # Verify that each insight is stored correctly
        for insight in stored_insights:
            self.assertIn(insight.id, ["statistical_insight", "trend_insight", "anomaly_insight"])
            
            if insight.id == "statistical_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "statistical")
                self.assertEqual(insight.scope_level, "aggregate")
            elif insight.id == "trend_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "trend")
                self.assertEqual(insight.scope_level, "dimension")
            elif insight.id == "anomaly_insight":
                self.assertEqual(insight.insight_type, "data_science")
                self.assertEqual(insight.insight_subtype, "anomaly")
                self.assertEqual(insight.scope_level, "individual")
    
    def test_get_insights_by_type(self):
        """Test getting insights by type."""
        # Save the insights
        self.file_backend.save_insights(self.sample_insights)
        
        # Get the list of saved insights
        saved_insights_list = self.file_backend.list_saved_insights()
        
        # Verify that at least one insight file was saved
        self.assertGreater(len(saved_insights_list), 0)
        
        # Get the filepath from the first saved insight
        filepath = saved_insights_list[0]["filepath"]
        
        # Get insights by type
        all_insights = self.file_backend.load_insights(filepath)
        data_science_insights = [insight for insight in all_insights if insight.insight_type == "data_science"]
        
        # Verify that the correct number of insights are returned
        self.assertEqual(len(data_science_insights), 3)
        
        # Verify that each insight has the correct type
        for insight in data_science_insights:
            self.assertEqual(insight.insight_type, "data_science")
    
    def test_get_insights_by_scope(self):
        """Test getting insights by scope."""
        # Save the insights
        self.file_backend.save_insights(self.sample_insights)
        
        # Get the list of saved insights
        saved_insights_list = self.file_backend.list_saved_insights()
        
        # Verify that at least one insight file was saved
        self.assertGreater(len(saved_insights_list), 0)
        
        # Get the filepath from the first saved insight
        filepath = saved_insights_list[0]["filepath"]
        
        # Get insights by scope
        all_insights = self.file_backend.load_insights(filepath)
        aggregate_insights = [insight for insight in all_insights if insight.scope_level == "aggregate"]
        dimension_insights = [insight for insight in all_insights if insight.scope_level == "dimension"]
        individual_insights = [insight for insight in all_insights if insight.scope_level == "individual"]
        
        # Verify that the correct number of insights are returned
        self.assertEqual(len(aggregate_insights), 1)
        self.assertEqual(len(dimension_insights), 1)
        self.assertEqual(len(individual_insights), 1)
        
        # Verify that each insight has the correct scope
        self.assertEqual(aggregate_insights[0].scope_level, "aggregate")
        self.assertEqual(dimension_insights[0].scope_level, "dimension")
        self.assertEqual(individual_insights[0].scope_level, "individual")
    
    def test_get_insights_by_traceability(self):
        """Test getting insights by traceability"""
        # Save insights with different traceability
        time_insight = Insight(
            id="time_insight",
            description="Time-based insight",
            importance_score=0.8,
            source_data={"value": 100}
        )
        time_insight.trace = {
            "dimension_context": ["time", "date"],
            "data_indices": {"dataset_a": [1, 2, 3], "dataset_b": [1, 2, 3]},
            "column_references": {"dataset_a": ["date"], "dataset_b": ["date"]}
        }
        
        product_insight = Insight(
            id="product_insight",
            description="Product-based insight",
            importance_score=0.7,
            source_data={"value": 200}
        )
        product_insight.trace = {
            "dimension_context": ["product", "category"],
            "data_indices": {"dataset_a": [4, 5, 6], "dataset_b": [4, 5, 6]},
            "column_references": {"dataset_a": ["product_id"], "dataset_b": ["product_id"]}
        }
        
        # Save insights
        self.file_backend.save_insights([time_insight, product_insight])
        
        # Get all insights
        all_insights = self.file_backend.load_insights(self.file_backend.list_saved_insights()[0]["filepath"])
        
        # Filter insights by traceability
        time_insights = [insight for insight in all_insights if "time" in insight.trace["dimension_context"]]
        product_insights = [insight for insight in all_insights if "product" in insight.trace["dimension_context"]]
        
        # Verify results
        self.assertEqual(len(time_insights), 1)
        self.assertEqual(len(product_insights), 1)
        self.assertEqual(time_insights[0].id, "time_insight")
        self.assertEqual(product_insights[0].id, "product_insight")
    
    def test_update_insight(self):
        """Test updating an insight."""
        # Save the insights
        self.file_backend.save_insights(self.sample_insights)
        
        # Update the statistical insight
        updated_insight = Insight(
            id="statistical_insight",
            description="Updated statistical insight",
            importance_score=0.9,
            source_data={"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]}
        )
        updated_insight.insight_type = "data_science"
        updated_insight.insight_subtype = "statistical"
        updated_insight.scope_level = "aggregate"
        updated_insight.scope_details = {"dimension": "time"}
        updated_insight.trace_data = {
            "data_indices": {"dataset_a": [0, 1, 2], "dataset_b": [0, 1, 2]},
            "column_references": {"dataset_a": ["forecast_value_p50"], "dataset_b": ["forecast_value_p50"]},
            "dimension_context": {"time": "2025-03-08"}
        }
        
        # Update the insight by saving a new batch with the updated insight
        updated_insights = [updated_insight] + [insight for insight in self.sample_insights if insight.id != "statistical_insight"]
        self.file_backend.save_insights(updated_insights)
        
        # Get the list of saved insights
        saved_insights_list = self.file_backend.list_saved_insights()
        
        # Verify that at least one insight file was saved
        self.assertGreater(len(saved_insights_list), 0)
        
        # Get the filepath from the first saved insight
        filepath = saved_insights_list[0]["filepath"]
        
        # Get the updated insight
        stored_insights = self.file_backend.load_insights(filepath)
        
        # Find the updated insight
        updated_stored_insight = next(
            (insight for insight in stored_insights if insight.id == "statistical_insight"),
            None
        )
        
        # Verify that the insight is updated correctly
        self.assertIsNotNone(updated_stored_insight)
        self.assertEqual(updated_stored_insight.description, "Updated statistical insight")
        self.assertEqual(updated_stored_insight.importance_score, 0.9)
    
    def test_delete_insight(self):
        """Test deleting an insight."""
        # Save the insights
        self.file_backend.save_insights(self.sample_insights)
        
        # Delete the statistical insight by saving a new batch without it
        remaining_insights = [insight for insight in self.sample_insights if insight.id != "statistical_insight"]
        self.file_backend.save_insights(remaining_insights)
        
        # Get the list of saved insights
        saved_insights_list = self.file_backend.list_saved_insights()
        
        # Verify that at least one insight file was saved
        self.assertGreater(len(saved_insights_list), 0)
        
        # Get the filepath from the first saved insight
        filepath = saved_insights_list[0]["filepath"]
        
        # Get the remaining insights
        stored_insights = self.file_backend.load_insights(filepath)
        
        # Verify that the insight is deleted
        self.assertEqual(len(stored_insights), 2)
        
        # Verify that the deleted insight is not in the stored insights
        deleted_insight = next(
            (insight for insight in stored_insights if insight.id == "statistical_insight"),
            None
        )
        self.assertIsNone(deleted_insight)
    
    def test_insight_serialization(self):
        """Test insight serialization."""
        # Create a sample insight
        insight = self.sample_insights[0]
        
        # Serialize the insight
        serialized_insight = insight.to_dict()
        
        # Verify that the insight is serialized correctly
        self.assertEqual(serialized_insight["id"], insight.id)
        self.assertEqual(serialized_insight["description"], insight.description)
        self.assertEqual(serialized_insight["importance_score"], insight.importance_score)
        self.assertEqual(serialized_insight["insight_type"], insight.insight_type)
        self.assertEqual(serialized_insight["insight_subtype"], insight.insight_subtype)
        self.assertEqual(serialized_insight["scope_level"], insight.scope_level)
        self.assertEqual(serialized_insight["scope_details"], insight.scope_details)
        self.assertEqual(serialized_insight["trace"], insight.trace)
        
        # Deserialize the insight
        deserialized_insight = Insight.from_dict(serialized_insight)
        
        # Verify that the insight is deserialized correctly
        self.assertEqual(deserialized_insight.id, insight.id)
        self.assertEqual(deserialized_insight.description, insight.description)
        self.assertEqual(deserialized_insight.importance_score, insight.importance_score)
        self.assertEqual(deserialized_insight.insight_type, insight.insight_type)
        self.assertEqual(deserialized_insight.insight_subtype, insight.insight_subtype)
        self.assertEqual(deserialized_insight.scope_level, insight.scope_level)
        self.assertEqual(deserialized_insight.scope_details, insight.scope_details)
        self.assertEqual(deserialized_insight.trace, insight.trace)

if __name__ == "__main__":
    unittest.main() 