#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd
import numpy as np
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

class TestFitMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        # Get the data directory - using the root data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
        # Load test data
        cls.data_a = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_1.csv'))
        cls.data_b = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_2.csv'))
        
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
            verbose=True
        )
        
        # Run prepare stage with lower threshold for key detection
        self.llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Log the key/value detection checkpoint for debugging
        prepare_stage_logger = self.llamasee.stages["prepare"]
        key_value_detection = prepare_stage_logger.get_checkpoint("key_value_detection")
        if key_value_detection:
            logger.debug(f"Key/value detection checkpoint: {key_value_detection}")
            
            # Log the detected keys and values
            logger.debug(f"Potential keys: {key_value_detection.get('potential_keys', {})}")
            logger.debug(f"Potential values: {key_value_detection.get('potential_values', {})}")
            logger.debug(f"Valid keys: {key_value_detection.get('valid_keys', [])}")
            logger.debug(f"Valid values: {key_value_detection.get('valid_values', [])}")
    
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
        # Get the key/value detection checkpoint from prepare stage
        prepare_stage_logger = self.llamasee.stages["prepare"]
        key_value_detection = prepare_stage_logger.get_checkpoint("key_value_detection")
        
        # Get the nested data part
        nested_data = key_value_detection["data"]["data"]
        
        # Get validated keys and values
        valid_keys = nested_data.get("valid_keys", [])
        valid_values = nested_data.get("valid_values", [])
        
        # Select some columns as keys and values
        keys = valid_keys[:2]  # First two valid keys
        values = valid_values[:2]  # First two valid values
        
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
        # Get the key/value detection checkpoint from prepare stage
        prepare_stage_logger = self.llamasee.stages["prepare"]
        key_value_detection = prepare_stage_logger.get_checkpoint("key_value_detection")
        
        # Get the nested data part
        nested_data = key_value_detection["data"]["data"]
        
        # Get validated keys and values
        valid_keys = nested_data.get("valid_keys", [])
        valid_values = nested_data.get("valid_values", [])
        
        # Select some columns as keys and values
        keys = valid_keys[:2]  # First two valid keys
        values = valid_values[:2]  # First two valid values
        
        # Create dimensions
        dimensions = {
            'time': [keys[0]],  # First key as time dimension
            'category': [keys[1]]  # Second key as category dimension
        }
        
        # Run fit method with dimensions
        result = self.llamasee.fit(keys=keys, values=values, dimensions=dimensions)
        
        # Check that the method returns self for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that dimensions were set correctly
        self.assertEqual(self.llamasee.dimensions, dimensions)
    
    def test_column_analysis_checkpoint(self):
        """Test that column analysis checkpoint is created"""
        # Run fit method
        self.llamasee.fit()
        
        # Get the stage logger
        stage_logger = self.llamasee.stages["fit"]
        
        # Check that column analysis checkpoint exists
        column_analysis_checkpoint = stage_logger.get_checkpoint("column_analysis")
        self.assertIsNotNone(column_analysis_checkpoint)
        
        # Log the column analysis checkpoint for debugging
        logger.debug(f"Column analysis checkpoint: {column_analysis_checkpoint}")
        
        # Get the data part of the checkpoint
        self.assertIn("data", column_analysis_checkpoint)
        column_analysis = column_analysis_checkpoint["data"]
        
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
        comparison_structure_checkpoint = stage_logger.get_checkpoint("comparison_structure")
        self.assertIsNotNone(comparison_structure_checkpoint)
        
        # Log the comparison structure checkpoint for debugging
        logger.debug(f"Comparison structure checkpoint: {comparison_structure_checkpoint}")
        
        # Get the data part of the checkpoint
        self.assertIn("data", comparison_structure_checkpoint)
        comparison_structure = comparison_structure_checkpoint["data"]
        
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