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

class TestKeyDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        # Create test data with known key and value columns
        cls.data_a = pd.DataFrame({
            'id': range(100),
            'sku': [f'SKU{i}' for i in range(100)],
            'store_id': [f'STORE{i%10}' for i in range(100)],
            'date': pd.date_range(start='2024-01-01', periods=100),
            'value': np.random.rand(100) * 100,
            'quantity': np.random.randint(1, 100, 100),
            'price': np.random.rand(100) * 10
        })
        
        cls.data_b = pd.DataFrame({
            'id': range(100),
            'sku': [f'SKU{i}' for i in range(100)],
            'store_id': [f'STORE{i%10}' for i in range(100)],
            'date': pd.date_range(start='2024-01-01', periods=100),
            'value': np.random.rand(100) * 100,
            'quantity': np.random.randint(1, 100, 100),
            'price': np.random.rand(100) * 10
        })
        
        # Create metadata
        cls.metadata_a = {"name": "Dataset A", "description": "Test dataset A"}
        cls.metadata_b = {"name": "Dataset B", "description": "Test dataset B"}
        cls.context = {"description": "Test context"}
    
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
        """Test detection of potential key columns"""
        # Test with default threshold
        potential_keys = self.llamasee.detect_potential_keys(threshold=0.95)
        logger.debug(f"Potential keys with threshold 0.95: {potential_keys}")
        
        # Test with lower threshold
        potential_keys_low = self.llamasee.detect_potential_keys(threshold=0.5)
        logger.debug(f"Potential keys with threshold 0.5: {potential_keys_low}")
        
        # Test with very low threshold
        potential_keys_very_low = self.llamasee.detect_potential_keys(threshold=0.1)
        logger.debug(f"Potential keys with threshold 0.1: {potential_keys_very_low}")
        
        # Check that key columns are detected
        self.assertIn('id', potential_keys)
        self.assertIn('sku', potential_keys)
        self.assertIn('store_id', potential_keys)
        self.assertIn('date', potential_keys)
        
        # Check that value columns are not detected as keys with high threshold
        self.assertNotIn('value', potential_keys)
        self.assertNotIn('quantity', potential_keys)
        self.assertNotIn('price', potential_keys)
        
        # Check that value columns might be detected as keys with very low threshold
        self.assertIn('value', potential_keys_very_low)
        self.assertIn('quantity', potential_keys_very_low)
        self.assertIn('price', potential_keys_very_low)
    
    def test_detect_potential_values(self):
        """Test detection of potential value columns"""
        # Test with default parameters
        potential_values = self.llamasee.detect_potential_values()
        logger.debug(f"Potential values: {potential_values}")
        
        # Test with exclude_keys=False
        potential_values_with_keys = self.llamasee.detect_potential_values(exclude_keys=False)
        logger.debug(f"Potential values (including keys): {potential_values_with_keys}")
        
        # Check that value columns are detected
        self.assertIn('value', potential_values)
        self.assertIn('quantity', potential_values)
        self.assertIn('price', potential_values)
        
        # Check that key columns are not detected as values by default
        self.assertNotIn('id', potential_values)
        self.assertNotIn('sku', potential_values)
        self.assertNotIn('store_id', potential_values)
        self.assertNotIn('date', potential_values)
        
        # Check that key columns are detected as values when exclude_keys=False
        self.assertIn('id', potential_values_with_keys)
        self.assertIn('sku', potential_values_with_keys)
        self.assertIn('store_id', potential_values_with_keys)
        self.assertIn('date', potential_values_with_keys)
    
    def test_key_value_detection_in_prepare(self):
        """Test key/value detection in prepare method"""
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
        
        # Check that the checkpoint has the expected keys
        self.assertIn("potential_keys_a", key_value_detection)
        self.assertIn("potential_keys_b", key_value_detection)
        self.assertIn("potential_values_a", key_value_detection)
        self.assertIn("potential_values_b", key_value_detection)
        
        # Check that the expected keys are detected
        self.assertIn("id", key_value_detection["potential_keys_a"])
        self.assertIn("sku", key_value_detection["potential_keys_a"])
        self.assertIn("store_id", key_value_detection["potential_keys_a"])
        self.assertIn("date", key_value_detection["potential_keys_a"])
        
        # Check that the expected values are detected
        self.assertIn("value", key_value_detection["potential_values_a"])
        self.assertIn("quantity", key_value_detection["potential_values_a"])
        self.assertIn("price", key_value_detection["potential_values_a"])

if __name__ == '__main__':
    unittest.main() 