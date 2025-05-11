import os
import sys
import json
import pandas as pd
import unittest
import logging
from typing import List
from collections import Counter

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

class TestCompareAndInsights(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data using real data files"""
        # Get the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
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
        """Create a fresh LlamaSee instance for each test"""
        self.llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True
        )
        
        # Run prepare and fit stages
        self.llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        self.llamasee.fit()

    def test_compare(self):
        """Test the compare method"""
        # Run the compare method
        result = self.llamasee.compare()
        
        # Check that the method returns the instance for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that comparison results are not empty
        self.assertIsNotNone(self.llamasee._comparison_results)
        self.assertGreater(len(self.llamasee._comparison_results), 0)
        
        # Verify key match statistics
        match_counts = self.llamasee._comparison_results['dataset_key_match'].value_counts()
        self.logger.info(f"Key match statistics: {match_counts.to_dict()}")
        
        # Check that we have all expected match types
        self.assertIn('match', match_counts.index)
        self.assertIn('a-only', match_counts.index)
        self.assertIn('b-only', match_counts.index)
        
        # Check that the sum of all match types equals the total number of rows
        self.assertEqual(match_counts.sum(), len(self.llamasee._comparison_results))
        
        # Check that the key columns are preserved
        key_columns = self.llamasee._comparison_structure['keys']
        for key in key_columns:
            self.assertIn(key, self.llamasee._comparison_results.columns)
        
        # Log the comparison results
        logger.debug(f"Comparison results: {self.llamasee._comparison_results}")

    def test_generate_insights(self):
        """Test the generate_insights method"""
        # Run compare method first
        self.llamasee.compare()
        
        # Run generate_insights method
        insights = self.llamasee.generate_insights()
        
        # Check that insights are generated
        self.assertIsInstance(insights, List)
        self.assertGreater(len(insights), 0)
        
        # Log the generated insights
        for insight in insights:
            logger.debug(f"Generated insight: {insight}")

    def test_comparison_and_insight_statistics(self):
        """Test to analyze and log statistics about comparison results and insights"""
        # Set logging level to INFO for this test
        logger.setLevel(logging.INFO)
        
        # Run compare and generate insights
        self.llamasee.compare()
        insights = self.llamasee.generate_insights()

        # Analyze comparison results
        comparison_results = self.llamasee._comparison_results
        
        # Print and log comparison statistics
        print("\n=== COMPARISON STATISTICS ===")
        logger.info("\n=== COMPARISON STATISTICS ===")
        print(f"Total comparison records: {len(comparison_results)}")
        logger.info(f"Total comparison records: {len(comparison_results)}")
        
        # Verify we have comparison results
        self.assertIsNotNone(comparison_results)
        self.assertGreater(len(comparison_results), 0)
        
        # Print and log column names
        print("\nAvailable columns in comparison results:")
        logger.info("\nAvailable columns in comparison results:")
        columns = list(comparison_results.columns)
        print(f"Columns: {columns}")
        logger.info(f"Columns: {columns}")
        
        # Check if we have the expected difference columns
        has_absolute_diff = 'absolute_difference' in columns
        has_percentage_diff = 'percentage_difference' in columns
        
        print(f"Has absolute difference column: {has_absolute_diff}")
        print(f"Has percentage difference column: {has_percentage_diff}")
        logger.info(f"Has absolute difference column: {has_absolute_diff}")
        logger.info(f"Has percentage difference column: {has_percentage_diff}")
        
        # Analyze absolute differences
        if has_absolute_diff:
            abs_diff_stats = {
                'total_differences': len(comparison_results[comparison_results['absolute_difference'] != 0]),
                'mean_difference': comparison_results['absolute_difference'].mean(),
                'max_difference': comparison_results['absolute_difference'].max(),
                'min_difference': comparison_results['absolute_difference'].min(),
                'std_difference': comparison_results['absolute_difference'].std()
            }
            
            print("\nAbsolute Difference Statistics:")
            logger.info("\nAbsolute Difference Statistics:")
            print(f"  Total non-zero differences: {abs_diff_stats['total_differences']}")
            print(f"  Mean difference: {abs_diff_stats['mean_difference']:.2f}")
            print(f"  Max difference: {abs_diff_stats['max_difference']:.2f}")
            print(f"  Min difference: {abs_diff_stats['min_difference']:.2f}")
            print(f"  Standard deviation: {abs_diff_stats['std_difference']:.2f}")
            
            # Verify statistics
            self.assertGreaterEqual(abs_diff_stats['total_differences'], 0)
            self.assertIsNotNone(abs_diff_stats['mean_difference'])
            self.assertIsNotNone(abs_diff_stats['max_difference'])
            self.assertIsNotNone(abs_diff_stats['min_difference'])
            self.assertIsNotNone(abs_diff_stats['std_difference'])
        
        # Analyze percentage differences
        if has_percentage_diff:
            pct_diff_stats = {
                'total_differences': len(comparison_results[comparison_results['percentage_difference'] != 0]),
                'mean_difference': comparison_results['percentage_difference'].mean(),
                'max_difference': comparison_results['percentage_difference'].max(),
                'min_difference': comparison_results['percentage_difference'].min(),
                'std_difference': comparison_results['percentage_difference'].std()
            }
            
            print("\nPercentage Difference Statistics:")
            logger.info("\nPercentage Difference Statistics:")
            print(f"  Total non-zero differences: {pct_diff_stats['total_differences']}")
            print(f"  Mean difference: {pct_diff_stats['mean_difference']:.2f}%")
            print(f"  Max difference: {pct_diff_stats['max_difference']:.2f}%")
            print(f"  Min difference: {pct_diff_stats['min_difference']:.2f}%")
            print(f"  Standard deviation: {pct_diff_stats['std_difference']:.2f}%")
            
            # Verify statistics
            self.assertGreaterEqual(pct_diff_stats['total_differences'], 0)
            self.assertIsNotNone(pct_diff_stats['mean_difference'])
            self.assertIsNotNone(pct_diff_stats['max_difference'])
            self.assertIsNotNone(pct_diff_stats['min_difference'])
            self.assertIsNotNone(pct_diff_stats['std_difference'])
        
        # Analyze by value columns
        value_stats = {}
        for value in self.llamasee.values:
            # Find the value columns for this value
            value_col_a = None
            value_col_b = None
            
            for col in comparison_results.columns:
                if value in col and '_a' in col:
                    value_col_a = col
                elif value in col and '_b' in col:
                    value_col_b = col
            
            if value_col_a and value_col_b:
                # Calculate direct differences between the value columns
                direct_diff = comparison_results[value_col_a] - comparison_results[value_col_b]
                
                stats = {
                    'total_differences': len(direct_diff[direct_diff != 0]),
                    'mean_difference': direct_diff.mean(),
                    'max_difference': direct_diff.max(),
                    'min_difference': direct_diff.min(),
                    'std_difference': direct_diff.std()
                }
                value_stats[value] = stats
                
                # Print and log statistics for this value
                print(f"\n{value} (direct comparison):")
                logger.info(f"\n{value} (direct comparison):")
                print(f"  Total differences: {stats['total_differences']}")
                print(f"  Mean difference: {stats['mean_difference']:.2f}")
                print(f"  Max difference: {stats['max_difference']:.2f}")
                print(f"  Min difference: {stats['min_difference']:.2f}")
                print(f"  Standard deviation: {stats['std_difference']:.2f}")
                
                # Verify statistics
                self.assertGreaterEqual(stats['total_differences'], 0)
                self.assertIsNotNone(stats['mean_difference'])
                self.assertIsNotNone(stats['max_difference'])
                self.assertIsNotNone(stats['min_difference'])
                self.assertIsNotNone(stats['std_difference'])
            else:
                print(f"Warning: Could not find value columns for: {value}")
                logger.warning(f"Could not find value columns for: {value}")

        # Analyze insights
        print("\n=== INSIGHT STATISTICS ===")
        logger.info("\n=== INSIGHT STATISTICS ===")
        print(f"Total insights generated: {len(insights)}")
        logger.info(f"Total insights generated: {len(insights)}")
        
        # Verify we have insights
        self.assertIsInstance(insights, List)
        self.assertGreater(len(insights), 0)
        
        # Group insights by type
        insight_types = Counter(insight.insight_type for insight in insights)
        print("\nInsights by Type:")
        logger.info("\nInsights by Type:")
        for itype, count in insight_types.items():
            print(f"  {itype}: {count}")
            logger.info(f"  {itype}: {count}")
        
        # Group insights by scope level
        scope_levels = Counter(insight.scope_level for insight in insights)
        print("\nInsights by Scope Level:")
        logger.info("\nInsights by Scope Level:")
        for scope, count in scope_levels.items():
            print(f"  {scope}: {count}")
            logger.info(f"  {scope}: {count}")
        
        # Analyze importance scores
        importance_scores = [insight.importance_score for insight in insights]
        mean_importance = sum(importance_scores)/len(importance_scores)
        max_importance = max(importance_scores)
        min_importance = min(importance_scores)
        
        print("\nImportance Score Statistics:")
        logger.info("\nImportance Score Statistics:")
        print(f"  Mean importance: {mean_importance:.2f}")
        print(f"  Max importance: {max_importance:.2f}")
        print(f"  Min importance: {min_importance:.2f}")
        
        # Verify importance scores
        self.assertGreaterEqual(mean_importance, 0)
        self.assertGreaterEqual(max_importance, 0)
        self.assertGreaterEqual(min_importance, 0)
        
        # Group insights by value column
        value_insights = {}
        for value in self.llamasee.values:
            count = len([i for i in insights if value in i.source_data.get('columns', [])])
            value_insights[value] = count
            print(f"  {value}: {count}")
            logger.info(f"  {value}: {count}")
        
        print("\n=== END STATISTICS ===\n")
        logger.info("\n=== END STATISTICS ===\n")

if __name__ == '__main__':
    unittest.main() 