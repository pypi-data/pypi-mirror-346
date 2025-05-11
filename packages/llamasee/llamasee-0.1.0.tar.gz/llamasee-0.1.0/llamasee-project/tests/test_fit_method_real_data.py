#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd
import unittest
import logging
from typing import Dict, Any, List, Optional

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import LlamaSee
from llamasee.llamasee import LlamaSee

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestFitMethodRealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data using real data files"""
        # Get the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
        # Load test data
        cls.data_a = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_1_cleaned.csv'))
        cls.data_b = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_2_cleaned.csv'))
        
        # Log data info
        logger.debug(f"Data A columns: {list(cls.data_a.columns)}")
        logger.debug(f"Data B columns: {list(cls.data_b.columns)}")
        
        # Load metadata
        with open(os.path.join(data_dir, 'ForecastControl_run_1.json'), 'r') as f:
            cls.metadata_a = json.load(f)
        with open(os.path.join(data_dir, 'ForecastControl_run_2.json'), 'r') as f:
            cls.metadata_b = json.load(f)
            
        # Load context
        with open(os.path.join(data_dir, 'context.json'), 'r') as f:
            cls.context = json.load(f)
    
    def setUp(self):
        """Create a fresh LlamaSee instance for each test"""
        self.llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True,
            log_level="DEBUG"
        )
        
        # Run prepare stage
        self.llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
    
    def test_fit_with_no_parameters(self):
        """Test fit method with no parameters (auto-detection)"""
        # Run fit method
        result = self.llamasee.fit()
        
        # Check that the method returns self for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that keys and values were detected
        self.assertIsNotNone(self.llamasee.keys)
        self.assertIsNotNone(self.llamasee.values)
        
        # Check that keys and values are lists
        self.assertIsInstance(self.llamasee.keys, list)
        self.assertIsInstance(self.llamasee.values, list)
        
        # Check that keys and values are not empty
        self.assertGreater(len(self.llamasee.keys), 0)
        self.assertGreater(len(self.llamasee.values), 0)
        
        # Check that all keys exist in both datasets
        for key in self.llamasee.keys:
            self.assertIn(key, self.llamasee.data_a.columns)
            self.assertIn(key, self.llamasee.data_b.columns)
        
        # Check that all values exist in both datasets
        for value in self.llamasee.values:
            self.assertIn(value, self.llamasee.data_a.columns)
            self.assertIn(value, self.llamasee.data_b.columns)
        
        # Log the detected keys and values
        logger.debug(f"Detected keys: {self.llamasee.keys}")
        logger.debug(f"Detected values: {self.llamasee.values}")
    
    def test_fit_with_provided_keys_and_values(self):
        """Test fit method with provided keys and values"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys and values
        keys = common_columns[:2]  # First two columns as keys
        values = common_columns[2:4]  # Next two columns as values
        
        # Run fit method with provided keys and values
        result = self.llamasee.fit(keys=keys, values=values)
        
        # Check that the method returns self for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that keys and values were set correctly
        self.assertEqual(self.llamasee.keys, keys)
        self.assertEqual(self.llamasee.values, values)
    
    def test_fit_with_missing_keys(self):
        """Test fit method with keys that don't exist in both datasets"""
        # Create keys that don't exist in both datasets
        keys = ['non_existent_key_1', 'non_existent_key_2']
        
        # Run fit method with non-existent keys
        with self.assertRaises(ValueError):
            self.llamasee.fit(keys=keys)
    
    def test_fit_with_missing_values(self):
        """Test fit method with values that don't exist in both datasets"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys
        keys = common_columns[:2]  # First two columns as keys
        
        # Create values that don't exist in both datasets
        values = ['non_existent_value_1', 'non_existent_value_2']
        
        # Run fit method with non-existent values
        with self.assertRaises(ValueError):
            self.llamasee.fit(keys=keys, values=values)
    
    def test_fit_with_partial_keys(self):
        """Test fit method with some keys that exist and some that don't"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Create a mix of existing and non-existing keys
        keys = [common_columns[0], 'non_existent_key']
        
        # Run fit method with mixed keys
        with self.assertRaises(ValueError):
            self.llamasee.fit(keys=keys)
    
    def test_fit_with_dimensions(self):
        """Test fit method with dimensions"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys and values
        keys = common_columns[:2]  # First two columns as keys
        values = common_columns[2:4]  # Next two columns as values
        
        # Create dimensions
        dimensions = {
            'time': [common_columns[0]],  # First column as time dimension
            'category': [common_columns[1]]  # Second column as category dimension
        }
        
        # Run fit method with dimensions
        result = self.llamasee.fit(keys=keys, values=values, dimensions=dimensions)
        
        # Check that the method returns self for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that dimensions were set correctly
        self.assertEqual(self.llamasee.dimensions, dimensions)

    def test_dataset_narrowing(self):
        """Test that datasets are narrowed to include only overlapping key combinations"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys and values
        keys = common_columns[:2]  # First two columns as keys
        values = common_columns[2:4]  # Next two columns as values
        
        # Store original dataset sizes
        original_size_a = len(self.data_a)
        original_size_b = len(self.data_b)
        
        # Run fit method
        self.llamasee.fit(keys=keys, values=values)
        
        # Check that datasets were narrowed
        self.assertLessEqual(len(self.llamasee.data_a), original_size_a)
        self.assertLessEqual(len(self.llamasee.data_b), original_size_b)
        
        # Check that original datasets are preserved
        self.assertIsNotNone(self.llamasee._data_a_original)
        self.assertIsNotNone(self.llamasee._data_b_original)
        self.assertEqual(len(self.llamasee._data_a_original), original_size_a)
        self.assertEqual(len(self.llamasee._data_b_original), original_size_b)
        
        # Check that narrowed datasets only contain rows with matching key combinations
        key_combinations_a = self.llamasee.data_a[keys].drop_duplicates()
        key_combinations_b = self.llamasee.data_b[keys].drop_duplicates()
        
        # Convert to string representation for comparison
        keys_a_str = key_combinations_a.apply(lambda row: '_'.join(row.astype(str)), axis=1)
        keys_b_str = key_combinations_b.apply(lambda row: '_'.join(row.astype(str)), axis=1)
        
        # Check that all key combinations in narrowed datasets match
        self.assertEqual(set(keys_a_str), set(keys_b_str))

    def test_overlap_metadata(self):
        """Test that overlap metadata is correctly created and stored"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys and values
        keys = common_columns[:2]  # First two columns as keys
        values = common_columns[2:4]  # Next two columns as values
        
        # Run fit method
        self.llamasee.fit(keys=keys, values=values)
        
        # Check that overlap metadata exists
        self.assertIsNotNone(self.llamasee._overlap_meta)
        
        # Check required metadata fields
        required_fields = [
            "original_counts",
            "overlap_count",
            "removed_counts",
            "overlap_percentage",
            "keys",
            "timestamp"
        ]
        for field in required_fields:
            self.assertIn(field, self.llamasee._overlap_meta)
        
        # Check that counts are consistent
        meta = self.llamasee._overlap_meta
        self.assertEqual(
            meta["original_counts"]["dataset_a"] - meta["removed_counts"]["dataset_a"],
            meta["overlap_count"]
        )
        self.assertEqual(
            meta["original_counts"]["dataset_b"] - meta["removed_counts"]["dataset_b"],
            meta["overlap_count"]
        )
        
        # Check that percentages are calculated correctly
        if meta["original_counts"]["dataset_a"] > 0:
            expected_percentage_a = (meta["overlap_count"] / meta["original_counts"]["dataset_a"]) * 100
            self.assertAlmostEqual(meta["overlap_percentage"]["dataset_a"], expected_percentage_a)
        
        if meta["original_counts"]["dataset_b"] > 0:
            expected_percentage_b = (meta["overlap_count"] / meta["original_counts"]["dataset_b"]) * 100
            self.assertAlmostEqual(meta["overlap_percentage"]["dataset_b"], expected_percentage_b)

    def test_export_fit_results(self):
        """Test exporting fit results in different formats"""
        # Get some columns from the datasets
        common_columns = list(set(self.data_a.columns).intersection(set(self.data_b.columns)))
        
        # Select some columns as keys and values
        keys = common_columns[:2]  # First two columns as keys
        values = common_columns[2:4]  # Next two columns as values
        
        # Run fit method
        self.llamasee.fit(keys=keys, values=values)
        
        # Test JSON export
        json_result = self.llamasee.export_fit_results(format='json')
        self.assertIn('path', json_result)
        self.assertEqual(json_result['format'], 'json')
        
        # Verify JSON file exists and contains expected data
        with open(json_result['path'], 'r') as f:
            json_data = json.load(f)
            self.assertIn('comparison_structure', json_data)
            self.assertIn('overlap_meta', json_data)
            self.assertIn('timestamp', json_data)
        
        # Test CSV export
        csv_result = self.llamasee.export_fit_results(format='csv')
        self.assertIn('path', csv_result)
        self.assertEqual(csv_result['format'], 'csv')
        
        # Verify CSV file exists
        self.assertTrue(os.path.exists(csv_result['path']))
        
        # Test text export
        text_result = self.llamasee.export_fit_results(format='text')
        self.assertIn('path', text_result)
        self.assertEqual(text_result['format'], 'text')
        
        # Verify text file exists and contains expected content
        with open(text_result['path'], 'r') as f:
            text_content = f.read()
            self.assertIn('=== FIT RESULTS ===', text_content)
            self.assertIn('Comparison Structure:', text_content)
            self.assertIn('Overlap Meta:', text_content)
        
        # Clean up exported files
        for result in [json_result, csv_result, text_result]:
            if 'path' in result and os.path.exists(result['path']):
                os.remove(result['path'])

    def test_column_analysis_checkpoint(self):
        """Test that column analysis checkpoint is created"""
        # Run fit method
        self.llamasee.fit()
        
        # Get the stage logger
        stage_logger = self.llamasee.stages["fit"]
        
        # Check that column analysis checkpoint exists
        column_analysis = stage_logger.get_checkpoint("column_analysis")
        self.assertIsNotNone(column_analysis)
        
        # Check that column analysis contains expected keys
        self.assertIn("common_columns", column_analysis)
        self.assertIn("unique_to_a", column_analysis)
        self.assertIn("unique_to_b", column_analysis)
        
        # Check that common_columns is not empty
        self.assertGreater(len(column_analysis["common_columns"]), 0)
    
    def test_comparison_structure_checkpoint(self):
        """Test that comparison structure checkpoint is created"""
        # Run fit method
        self.llamasee.fit()
        
        # Get the stage logger
        stage_logger = self.llamasee.stages["fit"]
        
        # Check that comparison structure checkpoint exists
        comparison_structure = stage_logger.get_checkpoint("comparison_structure")
        self.assertIsNotNone(comparison_structure)
        
        # Check that comparison structure contains expected keys
        self.assertIn("keys", comparison_structure)
        self.assertIn("values", comparison_structure)
        self.assertIn("dimensions", comparison_structure)
        self.assertIn("column_analysis", comparison_structure)
        
        # Check that keys and values match the instance attributes
        self.assertEqual(comparison_structure["keys"], self.llamasee.keys)
        self.assertEqual(comparison_structure["values"], self.llamasee.values)
        self.assertEqual(comparison_structure["dimensions"], self.llamasee.dimensions)

if __name__ == '__main__':
    unittest.main() 