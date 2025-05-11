"""
Test the insight configuration system with sample data.

This script tests the insight configuration system using real sample data
from the data directory.
"""

import unittest
import pandas as pd
import json
import os
import sys

# Add the parent directory to the path so we can import the llamasee package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from llamasee.llamasee import LlamaSee
from llamasee.insight_config import InsightConfig

class TestInsightConfigWithSampleData(unittest.TestCase):
    def setUp(self):
        """Set up test data from the sample files."""
        # Get the path to the data directory
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
        
        # Load the sample data
        self.data_a = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_1.csv'))
        self.data_b = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_2.csv'))
        
        # Load the metadata
        with open(os.path.join(data_dir, 'ForecastControl_run_1.json'), 'r') as f:
            self.metadata_a = json.load(f)
        
        with open(os.path.join(data_dir, 'ForecastControl_run_2.json'), 'r') as f:
            self.metadata_b = json.load(f)
        
        # Load the context
        with open(os.path.join(data_dir, 'context.json'), 'r') as f:
            self.context = json.load(f)
    
    def test_default_configuration_with_sample_data(self):
        """Test that the default configuration works correctly with sample data."""
        # Create LlamaSee instance with default configuration
        llamasee = LlamaSee(
            self.metadata_a, self.data_a,
            self.metadata_b, self.data_b,
            context=self.context
        )
        
        # Auto-detect comparison structure
        llamasee.auto_detect_comparison_structure()
        
        # Run comparison
        llamasee.compare()
        
        # Generate insights
        insights = llamasee.generate_insights(top_n=5)
        
        # Check that insights were generated
        self.assertTrue(len(insights) > 0)
        
        # Check that insights have the expected fields
        for insight in insights:
            self.assertIsNotNone(insight.insight_type)
            self.assertIsNotNone(insight.scope_level)
            self.assertIsNotNone(insight.magnitude)
            self.assertIsNotNone(insight.frequency)
            self.assertIsNotNone(insight.business_impact)
            self.assertIsNotNone(insight.uniqueness)
            self.assertIsNotNone(insight.weighted_score)
            
            # Print insight details for inspection
            print(f"\nInsight: {insight.description}")
            print(f"Type: {insight.insight_type}, Scope: {insight.scope_level}")
            print(f"Magnitude: {insight.magnitude:.2f}, Frequency: {insight.frequency:.2f}")
            print(f"Business Impact: {insight.business_impact:.2f}, Uniqueness: {insight.uniqueness:.2f}")
            print(f"Weighted Score: {insight.weighted_score:.2f}")
    
    def test_custom_configuration_with_sample_data(self):
        """Test that custom configuration works correctly with sample data."""
        # Create custom configuration
        custom_weights = {
            'magnitude': 0.4,
            'frequency': 0.1,
            'business_impact': 0.3,
            'uniqueness': 0.2
        }
        
        custom_type_adjustments = {
            'anomaly': {
                'magnitude': 0.2,
                'frequency': -0.1,
                'business_impact': 0.1,
                'uniqueness': 0.0
            }
        }
        
        custom_config = InsightConfig(
            weights=custom_weights,
            type_adjustments=custom_type_adjustments
        )
        
        # Create LlamaSee instance with custom configuration
        llamasee = LlamaSee(
            self.metadata_a, self.data_a,
            self.metadata_b, self.data_b,
            context=self.context,
            insight_config=custom_config
        )
        
        # Auto-detect comparison structure
        llamasee.auto_detect_comparison_structure()
        
        # Run comparison
        llamasee.compare()
        
        # Generate insights
        insights = llamasee.generate_insights(top_n=5)
        
        # Check that insights were generated
        self.assertTrue(len(insights) > 0)
        
        # Check that insights have the expected fields
        for insight in insights:
            self.assertIsNotNone(insight.insight_type)
            self.assertIsNotNone(insight.scope_level)
            self.assertIsNotNone(insight.magnitude)
            self.assertIsNotNone(insight.frequency)
            self.assertIsNotNone(insight.business_impact)
            self.assertIsNotNone(insight.uniqueness)
            self.assertIsNotNone(insight.weighted_score)
            
            # Print insight details for inspection
            print(f"\nInsight: {insight.description}")
            print(f"Type: {insight.insight_type}, Scope: {insight.scope_level}")
            print(f"Magnitude: {insight.magnitude:.2f}, Frequency: {insight.frequency:.2f}")
            print(f"Business Impact: {insight.business_impact:.2f}, Uniqueness: {insight.uniqueness:.2f}")
            print(f"Weighted Score: {insight.weighted_score:.2f}")
    
    def test_compare_default_and_custom_configurations(self):
        """Compare insights generated with default and custom configurations."""
        # Create LlamaSee instance with default configuration
        llamasee_default = LlamaSee(
            self.metadata_a, self.data_a,
            self.metadata_b, self.data_b,
            context=self.context
        )
        
        # Create custom configuration
        custom_weights = {
            'magnitude': 0.4,
            'frequency': 0.1,
            'business_impact': 0.3,
            'uniqueness': 0.2
        }
        
        custom_type_adjustments = {
            'anomaly': {
                'magnitude': 0.2,
                'frequency': -0.1,
                'business_impact': 0.1,
                'uniqueness': 0.0
            }
        }
        
        custom_config = InsightConfig(
            weights=custom_weights,
            type_adjustments=custom_type_adjustments
        )
        
        # Create LlamaSee instance with custom configuration
        llamasee_custom = LlamaSee(
            self.metadata_a, self.data_a,
            self.metadata_b, self.data_b,
            context=self.context,
            insight_config=custom_config
        )
        
        # Auto-detect comparison structure for both
        llamasee_default.auto_detect_comparison_structure()
        llamasee_custom.auto_detect_comparison_structure()
        
        # Run comparison for both
        llamasee_default.compare()
        llamasee_custom.compare()
        
        # Generate insights for both
        insights_default = llamasee_default.generate_insights(top_n=5)
        insights_custom = llamasee_custom.generate_insights(top_n=5)
        
        # Check that insights were generated for both
        self.assertTrue(len(insights_default) > 0)
        self.assertTrue(len(insights_custom) > 0)
        
        # Print comparison
        print("\n=== Default Configuration Insights ===")
        for i, insight in enumerate(insights_default, 1):
            print(f"{i}. {insight.description} (Score: {insight.weighted_score:.2f})")
        
        print("\n=== Custom Configuration Insights ===")
        for i, insight in enumerate(insights_custom, 1):
            print(f"{i}. {insight.description} (Score: {insight.weighted_score:.2f})")
        
        # Check if the insights are different
        default_descriptions = [insight.description for insight in insights_default]
        custom_descriptions = [insight.description for insight in insights_custom]
        
        # The insights might be the same but in a different order, or they might be different
        # We'll just check that we got insights from both configurations
        self.assertTrue(len(default_descriptions) > 0)
        self.assertTrue(len(custom_descriptions) > 0)

if __name__ == '__main__':
    unittest.main() 