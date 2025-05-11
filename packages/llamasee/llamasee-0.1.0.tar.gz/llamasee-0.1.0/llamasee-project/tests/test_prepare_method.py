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

class TestPrepareMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data using real data files"""
        # Get the data directory
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
    
    def test_prepare_basic(self):
        """Test basic prepare method functionality"""
        # Run prepare stage
        self.llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Get the key/value detection checkpoint
        prepare_stage_logger = self.llamasee.stages["prepare"]
        key_value_detection = prepare_stage_logger.get_checkpoint("key_value_detection")
        
        # Check that the checkpoint exists
        self.assertIsNotNone(key_value_detection)
        
        # Print the key/value detection checkpoint details
        print("\n=== KEY/VALUE DETECTION CHECKPOINT ===")
        print(json.dumps(key_value_detection, indent=2))
        print("=== END KEY/VALUE DETECTION CHECKPOINT ===\n")
        
        # Check that the checkpoint has the expected structure
        self.assertIn("timestamp", key_value_detection)
        self.assertIn("data", key_value_detection)
        
        # Get the data part of the checkpoint
        key_value_data = key_value_detection["data"]
        
        # Print the data structure for debugging
        print("\n=== KEY/VALUE DATA ===")
        print(f"Data type: {type(key_value_data)}")
        print(f"Data keys: {list(key_value_data.keys())}")
        print(f"Full data: {json.dumps(key_value_data, indent=2)}")
        print("=== END KEY/VALUE DATA ===\n")
        
        # Check that the data has the expected structure
        self.assertIn("timestamp", key_value_data)
        self.assertIn("data", key_value_data)
        
        # Get the nested data part
        nested_data = key_value_data["data"]
        
        # Print the nested data structure for debugging
        print("\n=== NESTED DATA ===")
        print(f"Nested data type: {type(nested_data)}")
        print(f"Nested data keys: {list(nested_data.keys())}")
        print(f"Full nested data: {json.dumps(nested_data, indent=2)}")
        print("=== END NESTED DATA ===\n")
        
        # Check that the nested data has the expected keys
        self.assertIn("potential_keys", nested_data)
        self.assertIn("potential_values", nested_data)
        self.assertIn("undecided_columns", nested_data)
        self.assertIn("valid_keys", nested_data)
        self.assertIn("valid_values", nested_data)
        
        # Check that we found at least some potential keys and values
        self.assertGreater(len(nested_data["potential_keys"]), 0, "No potential keys found")
        self.assertGreater(len(nested_data["potential_values"]), 0, "No potential values found")
        
        # Print detected keys and values for debugging
        print("\nDetected keys:", nested_data["potential_keys"])
        print("Detected values:", nested_data["potential_values"])
        if nested_data["undecided_columns"]:
            print("Undecided columns:", nested_data["undecided_columns"])
    
    def test_detect_potential_keys(self):
        """Test detect_potential_keys method directly"""
        # Test with default threshold
        potential_keys_a = self.llamasee.detect_potential_keys(self.data_a)
        potential_keys_b = self.llamasee.detect_potential_keys(self.data_b)
        
        # Log the detected keys
        logger.debug(f"Potential keys in dataset A: {potential_keys_a}")
        logger.debug(f"Potential keys in dataset B: {potential_keys_b}")
        
        # Check that we found at least some potential keys
        self.assertGreater(len(potential_keys_a), 0, "No potential keys found in dataset A")
        self.assertGreater(len(potential_keys_b), 0, "No potential keys found in dataset B")
        
        # Test with lower threshold
        self.llamasee._key_analysis = {}  # Reset key analysis
        potential_keys_a_low = self.llamasee.detect_potential_keys(self.data_a, threshold=0.5)
        potential_keys_b_low = self.llamasee.detect_potential_keys(self.data_b, threshold=0.5)
        
        # Log the detected keys
        logger.debug(f"Potential keys in dataset A with threshold 0.5: {potential_keys_a_low}")
        logger.debug(f"Potential keys in dataset B with threshold 0.5: {potential_keys_b_low}")
        
        # Check that we found at least as many keys with lower threshold
        self.assertGreaterEqual(len(potential_keys_a_low), len(potential_keys_a), 
                               "Lower threshold should find at least as many keys")
        self.assertGreaterEqual(len(potential_keys_b_low), len(potential_keys_b), 
                               "Lower threshold should find at least as many keys")
    
    def test_detect_potential_values(self):
        """Test detect_potential_values method directly"""
        # Test with default parameters
        potential_values_a = self.llamasee.detect_potential_values(self.data_a)
        potential_values_b = self.llamasee.detect_potential_values(self.data_b)
        
        # Log the detected values
        logger.debug(f"Potential values in dataset A: {potential_values_a}")
        logger.debug(f"Potential values in dataset B: {potential_values_b}")
        
        # Check that we found at least some potential values
        self.assertGreater(len(potential_values_a), 0, "No potential values found in dataset A")
        self.assertGreater(len(potential_values_b), 0, "No potential values found in dataset B")
        
        # Test with exclude_keys=False
        self.llamasee._key_analysis = {}  # Reset key analysis
        potential_values_a_with_keys = self.llamasee.detect_potential_values(self.data_a, exclude_keys=False)
        potential_values_b_with_keys = self.llamasee.detect_potential_values(self.data_b, exclude_keys=False)
        
        # Log the detected values
        logger.debug(f"Potential values in dataset A with exclude_keys=False: {potential_values_a_with_keys}")
        logger.debug(f"Potential values in dataset B with exclude_keys=False: {potential_values_b_with_keys}")
        
        # Check that we found at least as many values when including keys
        self.assertGreaterEqual(len(potential_values_a_with_keys), len(potential_values_a), 
                               "Including keys should find at least as many values")
        self.assertGreaterEqual(len(potential_values_b_with_keys), len(potential_values_b), 
                               "Including keys should find at least as many values")

    def test_cardinality_for_specific_columns(self):
        """Test cardinality calculation for specific columns."""
        # Get the data
        data_a = self.data_a
        data_b = self.data_b
        
        # Columns to test
        test_columns = ['sku', 'store_id', 'forecast_date']
        
        print("\n=== CARDINALITY ANALYSIS FOR SPECIFIC COLUMNS ===")
        for column in test_columns:
            # Calculate cardinality for both datasets
            cardinality_a = self.llamasee._calculate_cardinality(data_a, column)
            cardinality_b = self.llamasee._calculate_cardinality(data_b, column)
            
            # Get total and unique counts
            total_a = len(data_a[data_a[column] != 0][column])
            total_b = len(data_b[data_b[column] != 0][column])
            unique_a = len(data_a[data_a[column] != 0][column].unique())
            unique_b = len(data_b[data_b[column] != 0][column].unique())
            
            print(f"\nColumn: {column}")
            print(f"Dataset A - Total non-zero: {total_a}, Unique: {unique_a}, Cardinality: {cardinality_a:.4f}")
            print(f"Dataset B - Total non-zero: {total_b}, Unique: {unique_b}, Cardinality: {cardinality_b:.4f}")
            
            # Check if it would be identified as a key
            is_key_a = self.llamasee._is_potential_key(column, data_a)
            is_key_b = self.llamasee._is_potential_key(column, data_b)
            print(f"Would be identified as key in A: {is_key_a}")
            print(f"Would be identified as key in B: {is_key_b}")
        print("\n=== END CARDINALITY ANALYSIS ===\n")

if __name__ == '__main__':
    unittest.main() 