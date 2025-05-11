import unittest
import pandas as pd
import numpy as np
import json
import os
from llamasee.llamasee import LlamaSee
from llamasee.insight_config import InsightConfig
from llamasee.core.insight import Insight

class TestLlamaSeeCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Get the project root directory
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        data_dir = os.path.join(project_root, 'data')
        
        # Load test data
        cls.data_a = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_1.csv'))
        cls.data_b = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_2.csv'))
        
        # Load metadata
        with open(os.path.join(data_dir, 'ForecastControl_run_1.json'), 'r') as f:
            cls.metadata_a = json.load(f)
        with open(os.path.join(data_dir, 'ForecastControl_run_2.json'), 'r') as f:
            cls.metadata_b = json.load(f)
            
        # Load context
        with open(os.path.join(data_dir, 'context.json'), 'r') as f:
            cls.context = json.load(f)
            
    def setUp(self):
        # Create a fresh LlamaSee instance for each test
        self.llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True
        )
        
    def test_initialization(self):
        """Test proper initialization of LlamaSee instance"""
        self.assertIsNotNone(self.llamasee)
        self.assertEqual(self.llamasee.metadata_a, self.metadata_a)
        self.assertTrue(isinstance(self.llamasee.data_a, pd.DataFrame))
        self.assertEqual(self.llamasee.metadata_b, self.metadata_b)
        self.assertTrue(isinstance(self.llamasee.data_b, pd.DataFrame))
        self.assertEqual(self.llamasee.context, self.context)
        
    def test_set_dimensions(self):
        """Test setting dimensions and aggregation levels"""
        dimensions = ['sku', 'store_id']
        agg_levels = {'sku': 'product', 'store_id': 'region'}
        
        self.llamasee.set_dimensions(dimensions, agg_levels)
        
        self.assertEqual(self.llamasee.dimensions, set(dimensions))
        self.assertEqual(self.llamasee.aggregation_levels, agg_levels)
        
    def test_set_comparison_structure(self):
        """Test setting comparison structure with keys and values"""
        keys = ['sku', 'store_id', 'forecast_date']
        values = ['forecast_value_p50', 'forecast_value_p10', 'forecast_value_p90']
        
        self.llamasee.set_comparison_structure(keys, values)
        
        self.assertEqual(self.llamasee.keys, keys)
        self.assertEqual(self.llamasee.values, values)
        self.assertEqual(self.llamasee.dimensions, set(keys))
        
    def test_detect_potential_keys(self):
        """Test detection of potential key columns"""
        potential_keys = self.llamasee.detect_potential_keys(threshold=0.95)
        
        # Check that the expected key columns are detected
        self.assertIn('sku', potential_keys)
        self.assertIn('store_id', potential_keys)
        self.assertIn('forecast_date', potential_keys)
        
        # Check that value columns are not detected as keys
        self.assertNotIn('forecast_value_p50', potential_keys)
        self.assertNotIn('forecast_value_p10', potential_keys)
        self.assertNotIn('forecast_value_p90', potential_keys)
        
    def test_detect_potential_values(self):
        """Test detection of potential value columns"""
        potential_values = self.llamasee.detect_potential_values()
        
        # Check that the expected value columns are detected
        self.assertIn('forecast_value_p50', potential_values)
        self.assertIn('forecast_value_p10', potential_values)
        self.assertIn('forecast_value_p90', potential_values)
        
        # Check that key columns are not detected as values
        self.assertNotIn('sku', potential_values)
        self.assertNotIn('store_id', potential_values)
        self.assertNotIn('forecast_date', potential_values)
        
    def test_compare_datasets(self):
        """Test comparison of datasets"""
        # Set up comparison structure
        self.llamasee.set_comparison_structure(
            keys=['sku', 'store_id', 'forecast_date'],
            values=['forecast_value_p50']
        )
        
        # Run comparison
        comparison_results = self.llamasee.compare_datasets()
        
        # Check that comparison results are generated
        self.assertIsNotNone(comparison_results)
        self.assertTrue(isinstance(comparison_results, pd.DataFrame))
        
        # Check that comparison results contain expected columns
        expected_columns = ['sku', 'store_id', 'forecast_date', 
                          'forecast_value_p50_a', 'forecast_value_p50_b',
                          'absolute_difference', 'percentage_difference']
        for col in expected_columns:
            self.assertIn(col, comparison_results.columns)
            
    def test_generate_insights(self):
        """Test insight generation"""
        # Set up comparison structure and run comparison
        self.llamasee.set_comparison_structure(
            keys=['sku', 'store_id', 'forecast_date'],
            values=['forecast_value_p50']
        )
        self.llamasee.compare_datasets()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Check that insights are generated
        self.assertIsNotNone(insights)
        self.assertTrue(isinstance(insights, list))
        self.assertTrue(all(isinstance(insight, Insight) for insight in insights))
        
        # Check that insights have required attributes
        for insight in insights:
            self.assertIsNotNone(insight.id)
            self.assertIsNotNone(insight.description)
            self.assertIsNotNone(insight.importance_score)
            self.assertIsNotNone(insight.source_data)
            self.assertIsNotNone(insight.trace)
            
            # Check source data structure
            self.assertIn('column', insight.source_data)
            self.assertIn('statistics', insight.source_data)
            self.assertIn('comparison_results', insight.source_data)
            
            # Check statistics
            stats = insight.source_data['statistics']
            self.assertIn('mean_diff', stats)
            self.assertIn('max_diff', stats)
            self.assertIn('min_diff', stats)
            self.assertIn('std_diff', stats)
            self.assertIn('pct_changed', stats)
            
            # Check trace information
            self.assertIn('columns', insight.trace)
            self.assertIn('data_indices', insight.trace)
            
            # Check LLM enhancements if available
            if self.llamasee.llm_enhancer:
                self.assertIsNotNone(insight.llm_tags)
                self.assertIsNotNone(insight.llm_annotation)
            
    def test_filter_insights(self):
        """Test insight filtering"""
        # Generate insights first
        self.llamasee.set_comparison_structure(
            keys=['sku', 'store_id', 'forecast_date'],
            values=['forecast_value_p50']
        )
        self.llamasee.compare_datasets()
        all_insights = self.llamasee.generate_insights()
        
        # Test filtering by importance score
        filtered_insights = self.llamasee.filter_insights(min_importance=0.5)
        self.assertTrue(all(insight.importance_score >= 0.5 for insight in filtered_insights))
        
        # Test filtering by dimension
        dimension_insights = self.llamasee.filter_insights(dimensions=['sku'])
        self.assertTrue(all('sku' in insight.trace['columns'] for insight in dimension_insights))
        
        # Test filtering with both criteria
        combined_filtered = self.llamasee.filter_insights(min_importance=0.5, dimensions=['sku'])
        self.assertTrue(all(insight.importance_score >= 0.5 for insight in combined_filtered))
        self.assertTrue(all('sku' in insight.trace['columns'] for insight in combined_filtered))
        
        # Test filtering with no criteria (should return all insights)
        all_filtered = self.llamasee.filter_insights()
        self.assertEqual(len(all_filtered), len(all_insights))
        
    def test_export_results(self):
        """Test exporting results"""
        # Generate results first
        self.llamasee.set_comparison_structure(
            keys=['sku', 'store_id', 'forecast_date'],
            values=['forecast_value_p50']
        )
        self.llamasee.compare_datasets()
        self.llamasee.generate_insights()
        
        # Test CSV export
        csv_path = 'test_results.csv'
        self.llamasee.export_results(csv_path, format='csv')
        csv_data = pd.read_csv(csv_path)
        self.assertTrue(csv_data.shape[0] > 0)
        self.assertIn('id', csv_data.columns)
        self.assertIn('description', csv_data.columns)
        self.assertIn('importance_score', csv_data.columns)
        
        # Test JSON export
        json_path = 'test_results.json'
        self.llamasee.export_results(json_path, format='json')
        with open(json_path, 'r') as f:
            results = json.load(f)
        self.assertIn('metadata', results)
        self.assertIn('comparison_results', results)
        self.assertIn('insights', results)
        
        # Verify insight structure in JSON
        for insight in results['insights']:
            self.assertIn('id', insight)
            self.assertIn('description', insight)
            self.assertIn('importance_score', insight)
            self.assertIn('source_data', insight)
            self.assertIn('trace', insight)
        
        # Test text export
        text_path = 'test_results.txt'
        self.llamasee.export_results(text_path, format='text')
        with open(text_path, 'r') as f:
            text_content = f.read()
        self.assertIn('LlamaSee Insights Report', text_content)
        self.assertIn('Generated on:', text_content)
        self.assertIn('Total insights:', text_content)
        
        # Clean up test files
        for file_path in [csv_path, json_path, text_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
        
if __name__ == '__main__':
    unittest.main() 