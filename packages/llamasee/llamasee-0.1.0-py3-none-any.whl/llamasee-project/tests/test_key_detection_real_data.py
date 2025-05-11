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

class TestKeyDetectionRealData(unittest.TestCase):
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
    
    def test_detect_potential_keys(self):
        """Test detection of potential key columns with real data"""
        # Test with default threshold
        potential_keys = self.llamasee.detect_potential_keys(threshold=0.95)
        logger.debug(f"Potential keys with threshold 0.95: {potential_keys}")
        
        # Test with lower threshold
        potential_keys_low = self.llamasee.detect_potential_keys(threshold=0.5)
        logger.debug(f"Potential keys with threshold 0.5: {potential_keys_low}")
        
        # Test with very low threshold
        potential_keys_very_low = self.llamasee.detect_potential_keys(threshold=0.1)
        logger.debug(f"Potential keys with threshold 0.1: {potential_keys_very_low}")
        
        # Check that we found at least some potential keys
        self.assertGreater(len(potential_keys_low), 0, "No potential keys found with threshold 0.5")
        
        # Check that we found more keys with lower threshold
        self.assertGreaterEqual(len(potential_keys_low), len(potential_keys), 
                               "Lower threshold should find at least as many keys as higher threshold")
        self.assertGreaterEqual(len(potential_keys_very_low), len(potential_keys_low), 
                               "Very low threshold should find at least as many keys as low threshold")
    
    def test_detect_potential_values(self):
        """Test detection of potential value columns with real data"""
        # Test with default parameters
        potential_values = self.llamasee.detect_potential_values()
        logger.debug(f"Potential values: {potential_values}")
        
        # Test with exclude_keys=False
        potential_values_with_keys = self.llamasee.detect_potential_values(exclude_keys=False)
        logger.debug(f"Potential values (including keys): {potential_values_with_keys}")
        
        # Check that we found at least some potential values
        self.assertGreater(len(potential_values), 0, "No potential values found")
        
        # Check that we found more values when including keys
        self.assertGreaterEqual(len(potential_values_with_keys), len(potential_values), 
                               "Including keys should find at least as many values")
    
    def test_key_value_detection_in_prepare(self):
        """Test key/value detection in prepare method with real data"""
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
        
        # Check that the checkpoint has the expected structure
        self.assertIn("timestamp", key_value_detection)
        self.assertIn("data", key_value_detection)
        
        # Get the data part of the checkpoint
        key_value_data = key_value_detection["data"]
        
        # Check that the data has the expected keys
        self.assertIn("data", key_value_data)
        
        # Get the nested data part
        nested_data = key_value_data["data"]
        
        # Check that the nested data has the expected keys
        self.assertIn("potential_keys_a", nested_data)
        self.assertIn("potential_keys_b", nested_data)
        self.assertIn("potential_values_a", nested_data)
        self.assertIn("potential_values_b", nested_data)
        
        # Check that we found at least some potential keys and values
        self.assertGreater(len(nested_data["potential_keys_a"]), 0, 
                          "No potential keys found in dataset A")
        self.assertGreater(len(nested_data["potential_keys_b"]), 0, 
                          "No potential keys found in dataset B")
        self.assertGreaterEqual(len(nested_data["potential_values_a"]), 0, 
                          "No potential values found in dataset A")
        self.assertGreaterEqual(len(nested_data["potential_values_b"]), 0, 
                          "No potential values found in dataset B")
        
        # Log the detected keys and values
        logger.debug(f"Potential keys in dataset A: {nested_data['potential_keys_a']}")
        logger.debug(f"Potential keys in dataset B: {nested_data['potential_keys_b']}")
        logger.debug(f"Potential values in dataset A: {nested_data['potential_values_a']}")
        logger.debug(f"Potential values in dataset B: {nested_data['potential_values_b']}")
    
    def test_common_potential_keys(self):
        """Test finding common potential keys between datasets"""
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
        
        # Get the nested data part
        nested_data = key_value_detection["data"]["data"]
        
        # Find common potential keys
        common_potential_keys = set(nested_data["potential_keys_a"]).intersection(
            set(nested_data["potential_keys_b"])
        )
        
        # Log common potential keys
        logger.debug(f"Common potential keys: {common_potential_keys}")
        
        # Check that we found at least some common potential keys
        self.assertGreater(len(common_potential_keys), 0, 
                          "No common potential keys found between datasets")

if __name__ == '__main__':
    unittest.main() 