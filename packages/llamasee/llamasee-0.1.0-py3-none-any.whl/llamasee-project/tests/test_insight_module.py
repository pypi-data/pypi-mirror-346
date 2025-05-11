#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd
import unittest
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from unittest.mock import MagicMock, patch
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import LlamaSee and insight components
from llamasee.llamasee import LlamaSee
from llamasee.core.insight import Insight
from llamasee.generation.insight_generator import InsightGenerator
from llamasee.integration.insight_manager import InsightManager
from llamasee.insight_config import InsightConfig, default_config
from llamasee.schema.key_enricher import KeyEnricher

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestInsightModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data using real data files"""
        # Get the data directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        
        # Load test data
        cls.data_a = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_1_cleaned.csv'))
        cls.data_b = pd.read_csv(os.path.join(data_dir, 'ForecastResults_run_2_cleaned.csv'))
        
        # Convert forecast_date to datetime
        cls.data_a['forecast_date'] = pd.to_datetime(cls.data_a['forecast_date'])
        cls.data_b['forecast_date'] = pd.to_datetime(cls.data_b['forecast_date'])
        
        # Log the data size
        logger.info(f"Loaded data_a with {len(cls.data_a)} rows")
        logger.info(f"Loaded data_b with {len(cls.data_b)} rows")
        
        # Load metadata
        with open(os.path.join(data_dir, 'ForecastControl_run_1.json'), 'r') as f:
            cls.metadata_a = json.load(f)
        with open(os.path.join(data_dir, 'ForecastControl_run_2.json'), 'r') as f:
            cls.metadata_b = json.load(f)
            
        # Load context
        with open(os.path.join(data_dir, 'context.json'), 'r') as f:
            cls.context = json.load(f)
        
        # Create a directory for test results
        cls.test_results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test-results')
        os.makedirs(cls.test_results_dir, exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        # No need to remove the test results directory as we want to keep the results
        pass
    
    def setUp(self):
        """Set up test data and LlamaSee instance."""
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # Create LlamaSee instance
        self.llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True, 
            log_level="DEBUG"
        )
        
        # Set logger level to DEBUG for insight generator
        logging.getLogger('llamasee.generation.insight_generator').setLevel(logging.DEBUG)
        
        # Run prepare and fit stages
        self.llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        self.llamasee.fit()
        
        # Note: analyze_scope is now called internally by generate_insights
        # No need to call it explicitly here
    
    def verify_comparison_stage(self):
        """Verify that the comparison stage has completed successfully"""
        # Run compare stage if not already run
        if not hasattr(self.llamasee, '_comparison_results') or self.llamasee._comparison_results is None:
            self.llamasee.compare()
        
        # Get the compare stage logger
        compare_stage_logger = self.llamasee.stages.get("compare")
        self.assertIsNotNone(compare_stage_logger, "Compare stage logger not found")
        
        # Check that the stage has completed
        stage_status = self.llamasee.stage_manager.get_stage_status("compare")
        self.assertEqual(stage_status, "completed", f"Compare stage not completed. Status: {stage_status}")
        
        # Get the output checkpoint
        output_checkpoint = compare_stage_logger.get_checkpoint("output")
        self.assertIsNotNone(output_checkpoint, "Compare stage output checkpoint not found")
        
        # Check that the stage completed successfully
        self.assertTrue(output_checkpoint.get("success", False), "Compare stage did not complete successfully")
        
        # Log high-level information about comparison results
        if hasattr(self.llamasee, '_comparison_results') and self.llamasee._comparison_results is not None:
            if isinstance(self.llamasee._comparison_results, pd.DataFrame):
                logger.info(f"Comparison results: {len(self.llamasee._comparison_results)} records")
                logger.info(f"Comparison columns: {list(self.llamasee._comparison_results.columns)}")
            else:
                logger.info(f"Comparison results: {len(self.llamasee._comparison_results)} items")
                for key, value in self.llamasee._comparison_results.items():
                    if isinstance(value, dict) and 'summary' in value:
                        logger.info(f"  {key}: {value['summary']}")
        else:
            logger.warning("No comparison results available")
            self.fail("No comparison results available")
    
    def test_export_comparison_datasets(self):
        """Test exporting comparison datasets with time key granularity detection."""
        # Create LlamaSee instance
        llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True,
            log_level="DEBUG"
        )
        
        # Run prepare stage
        llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Run fit stage without key enrichment
        llamasee.fit()
        
        # Run compare stage
        result = llamasee.compare()
        
        # Export comparison results before enrichment
        before_enrichment_path = os.path.join(self.test_results_dir, "comparison_before_enrichment.csv")
        if isinstance(llamasee._comparison_results, pd.DataFrame):
            llamasee._comparison_results.to_csv(before_enrichment_path, index=False)
            logger.info(f"Exported comparison results before enrichment to {before_enrichment_path}")
            logger.info(f"Columns in before enrichment: {list(llamasee._comparison_results.columns)}")
        else:
            logger.warning("Comparison results before enrichment are not a DataFrame, cannot export to CSV")
        
        # Check time key granularity in first few rows
        if isinstance(llamasee._comparison_results, pd.DataFrame):
            # Check if time_key and time_key_info columns exist
            self.assertIn('time_key', llamasee._comparison_results.columns)
            self.assertIn('time_key_info', llamasee._comparison_results.columns)
            
            # Check the first few rows
            for _, row in llamasee._comparison_results.head(5).iterrows():
                # Check if time_key column exists, but don't assert it's not None
                # Some rows might not have a time key
                if row['time_key'] is not None:
                    # Only check time_key_info if time_key is not None
                    if row['time_key_info'] is not None:
                        if isinstance(row['time_key_info'], dict):
                            # If it's a dict, check for granularity
                            self.assertIn('granularity', row['time_key_info'])
                            self.assertIsNotNone(row['time_key_info']['granularity'])
                        else:
                            # If it's not a dict, log a warning but don't fail the test
                            logger.warning(f"time_key_info is not a dict: {row['time_key_info']}")
                    else:
                        # If it's None, log a warning but don't fail the test
                        logger.warning("time_key_info is None")
                else:
                    # If time_key is None, log a warning but don't fail the test
                    logger.warning("time_key is None")
        
        # Export results
        output_path = '/Users/gpt2s/Desktop/Projects/LlamaSee/LlamaSee/llamasee-project/llamaseeStorage/debug_output/comparison_before_enrichment.csv'
        if isinstance(llamasee._comparison_results, pd.DataFrame):
            llamasee._comparison_results.to_csv(output_path, index=False)
            logger.info(f"Exported comparison results to {output_path}")
        else:
            logger.warning("Comparison results are not a DataFrame, cannot export to CSV")
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_path))
        
        # Sample key enrichment configuration
        key_enrichment = {
            "store_id": {
                "key_column": "store_id",
                "enriched_key": "region",
                "mappings": {
                    "STORE-13360597": "Southwest",
                    "STORE-16140789": "West",
                    "STORE-16140790": "Northeast",
                    "STORE-16140791": "Southeast",
                    "STORE-16140792": "Midwest"
                }
            }
        }
        
        # Create a new LlamaSee instance for the enriched comparison
        enriched_llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True,
            log_level="DEBUG"
        )
        
        # Run prepare stage
        enriched_llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Run fit stage with key enrichment
        enriched_llamasee.fit(key_enrichment=key_enrichment)
        
        # Run compare stage
        enriched_llamasee.compare()
        
        # Export comparison results after enrichment
        after_enrichment_path = os.path.join(self.test_results_dir, "comparison_after_enrichment.csv")
        if isinstance(enriched_llamasee._comparison_results, pd.DataFrame):
            enriched_llamasee._comparison_results.to_csv(after_enrichment_path, index=False)
            logger.info(f"Exported comparison results after enrichment to {after_enrichment_path}")
            logger.info(f"Columns in after enrichment: {list(enriched_llamasee._comparison_results.columns)}")
        else:
            logger.warning("Comparison results after enrichment are not a DataFrame, cannot export to CSV")
        
        # Export the enriched datasets separately
        enriched_data_a_path = os.path.join(self.test_results_dir, "enriched_dataset_a.csv")
        enriched_data_b_path = os.path.join(self.test_results_dir, "enriched_dataset_b.csv")
        
        enriched_llamasee.data_a.to_csv(enriched_data_a_path, index=False)
        enriched_llamasee.data_b.to_csv(enriched_data_b_path, index=False)
        
        logger.info(f"Exported enriched dataset A to {enriched_data_a_path}")
        logger.info(f"Exported enriched dataset B to {enriched_data_b_path}")
        
        # Verify that the enriched column is in the exported files
        if os.path.exists(after_enrichment_path):
            after_enrichment_df = pd.read_csv(after_enrichment_path)
            enriched_column = "dim_region"
            self.assertIn(enriched_column, after_enrichment_df.columns, 
                         f"Enriched column {enriched_column} not found in exported comparison results")
            
            # Log the first few rows of the enriched comparison results
            logger.info(f"First few rows of enriched comparison results:")
            logger.info(after_enrichment_df.head().to_string())
            
            # Log the count of each region in the enriched comparison results
            if enriched_column in after_enrichment_df.columns:
                region_counts = after_enrichment_df[enriched_column].value_counts()
                logger.info(f"Region counts in enriched comparison results:")
                logger.info(region_counts.to_string())
        
        # Export the key enrichment metadata
        enrichment_metadata_path = os.path.join(self.test_results_dir, "key_enrichment_metadata.json")
        with open(enrichment_metadata_path, 'w') as f:
            json.dump(enriched_llamasee.key_enrichment_metadata, f, indent=2)
        
        logger.info(f"Exported key enrichment metadata to {enrichment_metadata_path}")
        
        # Export the canonical format data
        canonical_results_path = os.path.join(self.test_results_dir, "canonical_comparison_results.json")
        if hasattr(enriched_llamasee, '_canonical_comparison_results'):
            # Convert ComparisonResultRow objects to dictionaries
            canonical_data = {
                'rows': [row.__dict__ for row in enriched_llamasee._canonical_comparison_results.rows],
                'metadata': enriched_llamasee._canonical_comparison_results.metadata
            }
            with open(canonical_results_path, 'w') as f:
                json.dump(canonical_data, f, indent=2, default=str)  # Use str for datetime objects
            logger.info(f"Exported canonical comparison results to {canonical_results_path}")
            
            # Log the first few rows of the canonical results
            logger.info("First few rows of canonical comparison results:")
            for row in enriched_llamasee._canonical_comparison_results.rows[:5]:
                logger.info(f"Row: {row.__dict__}")
        else:
            logger.warning("Canonical comparison results not available")
        
        # Verify that the files exist
        self.assertTrue(os.path.exists(before_enrichment_path), f"Before enrichment file should exist at {before_enrichment_path}")
        self.assertTrue(os.path.exists(after_enrichment_path), f"After enrichment file should exist at {after_enrichment_path}")
        self.assertTrue(os.path.exists(enriched_data_a_path), f"Enriched dataset A file should exist at {enriched_data_a_path}")
        self.assertTrue(os.path.exists(enriched_data_b_path), f"Enriched dataset B file should exist at {enriched_data_b_path}")
        self.assertTrue(os.path.exists(enrichment_metadata_path), f"Enrichment metadata file should exist at {enrichment_metadata_path}")
        
        logger.info("Export comparison datasets test completed successfully")
    
    def test_key_enrichment(self):
        """Test key enrichment functionality"""
        # Create a new LlamaSee instance for this test
        llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True,
            log_level="DEBUG"
        )
        
        # Run prepare stage
        llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Verify that the data has been filtered to the correct date range
        min_date_a = pd.to_datetime(llamasee.data_a['forecast_date'].min())
        max_date_a = pd.to_datetime(llamasee.data_a['forecast_date'].max())
        min_date_b = pd.to_datetime(llamasee.data_b['forecast_date'].min())
        max_date_b = pd.to_datetime(llamasee.data_b['forecast_date'].max())
        
        expected_min_date = pd.to_datetime('2025-04-07')
        expected_max_date = pd.to_datetime('2025-04-13')
        
        self.assertTrue(min_date_a >= expected_min_date, f"Dataset A includes dates before {expected_min_date.date()}")
        self.assertTrue(max_date_a <= expected_max_date, f"Dataset A includes dates after {expected_max_date.date()}")
        self.assertTrue(min_date_b >= expected_min_date, f"Dataset B includes dates before {expected_min_date.date()}")
        self.assertTrue(max_date_b <= expected_max_date, f"Dataset B includes dates after {expected_max_date.date()}")
        
        # Log the date range for debugging
        logger.info(f"Dataset A date range: {min_date_a.date()} to {max_date_a.date()}")
        logger.info(f"Dataset B date range: {min_date_b.date()} to {max_date_b.date()}")
        
        # Create a sample key enrichment configuration
        # Assuming 'store_id' is a key column in the datasets
        key_enrichment = {
            "store_id": {
                "key_column": "store_id",
                "enriched_key": "region",
                "default_value": "Other",
                "mappings": {
                    "STORE-13360597": "Southwest",
                    "STORE-16140789": "West",
                    "STORE-16140790": "Northeast",
                    "STORE-16140791": "Southeast",
                    "STORE-16140792": "Midwest"
                }
            }
        }
        
        # Run fit stage with key enrichment
        llamasee.fit(key_enrichment=key_enrichment)
        
        # Verify that key enrichment was applied
        self.assertTrue(hasattr(llamasee, 'key_enrichment_metadata'), "Key enrichment metadata not found")
        self.assertGreater(len(llamasee.key_enrichment_metadata), 0, "No key enrichments were applied")
        
        # Check that the enriched key column was added to the datasets
        enriched_column = "dim_region"
        self.assertIn(enriched_column, llamasee.data_a.columns, f"Enriched column {enriched_column} not found in dataset A")
        self.assertIn(enriched_column, llamasee.data_b.columns, f"Enriched column {enriched_column} not found in dataset B")
        
        # Check that the enriched key was added to the keys list
        self.assertIn(enriched_column, llamasee.keys, f"Enriched key {enriched_column} not added to keys list")
        
        # Check that the enrichment was applied correctly for a mapped value
        sample_store_id = "STORE-13360597"
        expected_region = "Southwest"
        actual_region = llamasee.data_a.loc[llamasee.data_a['store_id'] == sample_store_id, enriched_column].iloc[0]
        self.assertEqual(actual_region, expected_region, f"Enrichment not applied correctly for store_id {sample_store_id}")
        
        # Check that the default value is used for unmapped values
        unmapped_store_id = "STORE-99999999"
        if unmapped_store_id in llamasee.data_a['store_id'].values:
            actual_region = llamasee.data_a.loc[llamasee.data_a['store_id'] == unmapped_store_id, enriched_column].iloc[0]
            self.assertEqual(actual_region, "Other", f"Default value not applied correctly for store_id {unmapped_store_id}")
        
        # Run compare stage to ensure it works with enriched keys
        llamasee.compare()
        
        # Verify that comparison results include the enriched key
        self.assertIsNotNone(llamasee._comparison_results, "Comparison results not generated")
        
        # Check that the comparison results respect the date filtering
        comparison_df = llamasee._comparison_results.to_dataframe()
        if 'forecast_date' in comparison_df.columns:
            min_date_comp = pd.to_datetime(comparison_df['forecast_date'].min())
            max_date_comp = pd.to_datetime(comparison_df['forecast_date'].max())
            
            self.assertTrue(min_date_comp >= expected_min_date, f"Comparison results include dates before {expected_min_date.date()}")
            self.assertTrue(max_date_comp <= expected_max_date, f"Comparison results include dates after {expected_max_date.date()}")
            
            logger.info(f"Comparison results date range: {min_date_comp.date()} to {max_date_comp.date()}")
        
        # Generate insights to ensure they work with the date-filtered data
        llamasee.generate_insights()
        
        # Verify that insights were generated
        self.assertIsNotNone(llamasee._insights, "Insights not generated")
        self.assertGreater(len(llamasee._insights), 0, "No insights were generated")
        
        # Export results to verify the canonical format
        export_path = os.path.join(self.test_results_dir, "key_enrichment_test_export.json")
        llamasee.export_results(export_path)
        
        # Verify the export file was created
        self.assertTrue(os.path.exists(export_path), f"Export file not created at {export_path}")
        
        # Load the exported data
        with open(export_path, 'r') as f:
            export_data = json.load(f)
        
        # Verify the structure of the exported data
        self.assertIn("canonical_comparison_results", export_data, "Canonical comparison results not found in export")
        self.assertIn("insights", export_data, "Insights not found in export")
        
        # Check that the canonical format includes the enriched key
        canonical_results = export_data["canonical_comparison_results"]
        self.assertIn("keys", canonical_results, "Keys not found in canonical results")
        self.assertIn("dimensions", canonical_results, "Dimensions not found in canonical results")
        
        # Verify that the enriched key is in the dimensions, not the keys
        self.assertIn("region", canonical_results["dimensions"], "Enriched key 'region' not found in dimensions")
        self.assertNotIn("dim_region", canonical_results["keys"], "Enriched key 'dim_region' should not be in keys")
        
        # Log the first row for verification
        if "rows" in canonical_results and len(canonical_results["rows"]) > 0:
            first_row = canonical_results["rows"][0]
            logger.info(f"First row in canonical format: {first_row}")
    
    def test_insight_generation(self):
        """Test basic insight generation with specific parameters"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        logger.info("Generating insights with specific parameters")
        # Generate insights with specific parameters
        insights = self.llamasee.generate_insights(
            scope='aggregate',
            fact_type='forecast_value_p50',
            time_key='forecast_date'
        )
        
        # Log insight counts and categorizations
        logger.info(f"Total insights generated: {len(insights)}")
        
        # Count by insight type
        insight_types = {}
        for insight in insights:
            insight_type = insight.insight_type if insight.insight_type else "uncategorized"
            insight_types[insight_type] = insight_types.get(insight_type, 0) + 1
        logger.info("Insights by type:")
        for insight_type, count in insight_types.items():
            logger.info(f"  {insight_type}: {count}")
        
        # Count by scope level
        scope_levels = {}
        for insight in insights:
            scope_level = insight.scope_level if insight.scope_level else "uncategorized"
            scope_levels[scope_level] = scope_levels.get(scope_level, 0) + 1
        logger.info("Insights by scope level:")
        for scope_level, count in scope_levels.items():
            logger.info(f"  {scope_level}: {count}")
        
        # Check that insights were generated
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        # Check that each insight has required attributes
        for insight in insights:
            self.assertIsInstance(insight, Insight)
            self.assertIsNotNone(insight.id)
            self.assertIsNotNone(insight.description)
            self.assertIsNotNone(insight.importance_score)
            # Verify fact_type and scope
            if hasattr(insight, 'source_data') and isinstance(insight.source_data, dict):
                if 'fact_type' in insight.source_data:
                    self.assertEqual(insight.source_data['fact_type'], 'forecast_value_p50')
                if 'scope' in insight.source_data:
                    self.assertEqual(insight.source_data['scope'], 'aggregate')
            
        # Export dimension results
        export_path = os.path.join(self.test_results_dir, "dimension_results.json")
        export_result = self.llamasee.export_dimension_comparison_results(output_path=export_path, format="json")
        
        # Verify export was successful
        self.assertIn("path", export_result, "Export result should contain path")
        self.assertEqual(export_result["format"], "json", "Export format should be json")
        self.assertTrue(os.path.exists(export_path), f"Export file should exist at {export_path}")
        
        # Log export information
        logger.info(f"Exported dimension results to {export_path}")
    
    def test_insight_types(self):
        """Test that different types of insights are generated"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Check that we have different types of insights
        insight_types = set(insight.insight_type for insight in insights)
        self.assertGreater(len(insight_types), 1)
        
        # Check that each insight type is valid
        valid_types = {'statistical', 'pattern', 'anomaly'}
        for insight_type in insight_types:
            self.assertIn(insight_type, valid_types)
    
    def test_insight_scope_levels(self):
        """Test that insights are generated at different scope levels"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Check that we have insights at different scope levels
        scope_levels = set(insight.scope_level for insight in insights)
        self.assertGreater(len(scope_levels), 1)
        
        # Check that each scope level is valid
        valid_levels = {'column', 'row', 'table'}
        for scope_level in scope_levels:
            self.assertIn(scope_level, valid_levels)
    
    def test_insight_scoring(self):
        """Test that insights are scored correctly"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Check that insights have valid importance scores
        for insight in insights:
            self.assertGreaterEqual(insight.importance_score, 0)
            self.assertLessEqual(insight.importance_score, 1)
        
        # Check that insights are sorted by importance
        sorted_insights = sorted(insights, key=lambda x: x.importance_score, reverse=True)
        self.assertEqual(insights, sorted_insights)
    
    def test_insight_storage(self):
        """Test insight storage and retrieval"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Create insight manager with file storage
        insight_manager = InsightManager(storage_type="file", storage_config={"path": self.test_results_dir})
        
        # Save insights
        batch_id = insight_manager.generate_and_save_insights(
            comparison_results=self.llamasee._comparison_results,
            scope=self.llamasee.analyze_scope(),
            context=self.context
        )
        
        # Check that batch ID was generated
        self.assertIsNotNone(batch_id)
        
        # Load insights
        loaded_insights = insight_manager.load_insights(batch_id)
        
        # Check that loaded insights match original insights
        self.assertEqual(len(loaded_insights), len(insights))
        for original, loaded in zip(insights, loaded_insights):
            self.assertEqual(original.id, loaded.id)
            self.assertEqual(original.description, loaded.description)
            self.assertEqual(original.importance_score, loaded.importance_score)
    
    def test_insight_filtering(self):
        """Test insight filtering"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Filter insights by importance score
        filtered_insights = self.llamasee.filter_insights(min_importance=0.5)
        
        # Check that filtered insights have higher importance scores
        self.assertLessEqual(len(filtered_insights), len(insights))
        for insight in filtered_insights:
            self.assertGreaterEqual(insight.importance_score, 0.5)
        
        # Filter insights by dimension
        dimension_insights = self.llamasee.filter_insights(dimensions=['time'])
        
        # Check that dimension-filtered insights have the correct dimension
        for insight in dimension_insights:
            self.assertIn('time', insight.dimensions)
    
    def test_insight_export(self):
        """Test insight export"""
        # Verify comparison stage
        self.verify_comparison_stage()
        
        # Generate insights
        insights = self.llamasee.generate_insights()
        
        # Export insights to CSV
        export_path = os.path.join(self.test_results_dir, 'insights.csv')
        self.llamasee.export_results(export_path, format='csv')
        
        # Check that export file exists
        self.assertTrue(os.path.exists(export_path))
        
        # Check that exported file contains insights
        exported_df = pd.read_csv(export_path)
        self.assertGreater(len(exported_df), 0)
        self.assertIn('id', exported_df.columns)
        self.assertIn('description', exported_df.columns)
        self.assertIn('importance_score', exported_df.columns)
    
    def test_insight_configuration(self):
        """Test insight generation with custom configuration"""
        # Create custom insight configuration
        insight_config = {
            'min_importance_score': 0.3,
            'max_insights': 10,
            'insight_types': ['statistical', 'pattern'],
            'scope_levels': ['column', 'table']
        }
        
        # Create LlamaSee instance with custom configuration
        llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            insight_config=insight_config,
            verbose=True
        )
        
        # Run stages
        llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        llamasee.fit()
        llamasee.compare()
        
        # Verify comparison stage
        compare_stage_logger = llamasee.stages.get("compare")
        self.assertIsNotNone(compare_stage_logger, "Compare stage logger not found")
        stage_status = llamasee.stage_manager.get_stage_status("compare")
        self.assertEqual(stage_status, "completed", f"Compare stage not completed. Status: {stage_status}")
        
        # Log high-level information about comparison results
        if hasattr(llamasee, '_comparison_results') and llamasee._comparison_results:
            if isinstance(llamasee._comparison_results, pd.DataFrame):
                logger.info(f"Comparison results: {len(llamasee._comparison_results)} records")
                logger.info(f"Comparison columns: {list(llamasee._comparison_results.columns)}")
            else:
                logger.info(f"Comparison results: {len(llamasee._comparison_results)} items")
                for key, value in llamasee._comparison_results.items():
                    if isinstance(value, dict) and 'summary' in value:
                        logger.info(f"  {key}: {value['summary']}")
        else:
            logger.warning("No comparison results available")
            self.fail("No comparison results available")
        
        # Generate insights
        insights = llamasee.generate_insights()
        
        # Check that insights respect configuration
        self.assertLessEqual(len(insights), insight_config['max_insights'])
        for insight in insights:
            self.assertGreaterEqual(insight.importance_score, insight_config['min_importance_score'])
            self.assertIn(insight.insight_type, insight_config['insight_types'])
            self.assertIn(insight.scope_level, insight_config['scope_levels'])
    
    def test_edge_cases(self):
        """Test edge cases for insight generation"""
        # Test with empty datasets
        empty_df = pd.DataFrame()
        empty_llamasee = LlamaSee(
            metadata_a={},
            data_a=empty_df,
            metadata_b={},
            data_b=empty_df,
            context={},
            verbose=True
        )
        
        # Run stages
        empty_llamasee.prepare(
            data_a=empty_df,
            data_b=empty_df,
            metadata_a={},
            metadata_b={},
            context={}
        )
        empty_llamasee.fit()
        empty_llamasee.compare()
        
        # Verify comparison stage
        compare_stage_logger = empty_llamasee.stages.get("compare")
        self.assertIsNotNone(compare_stage_logger, "Compare stage logger not found")
        stage_status = empty_llamasee.stage_manager.get_stage_status("compare")
        self.assertEqual(stage_status, "completed", f"Compare stage not completed. Status: {stage_status}")
        
        # Log high-level information about comparison results
        if hasattr(empty_llamasee, '_comparison_results') and empty_llamasee._comparison_results:
            logger.info(f"Empty dataset comparison results: {empty_llamasee._comparison_results}")
        else:
            logger.warning("No comparison results available for empty dataset")
        
        # Generate insights
        empty_insights = empty_llamasee.generate_insights()
        
        # Check that no insights are generated for empty datasets
        self.assertEqual(len(empty_insights), 0)
        
        # Test with minimal datasets
        minimal_df = pd.DataFrame({
            'key': [1, 2],
            'value': [10, 20]
        })
        minimal_llamasee = LlamaSee(
            metadata_a={},
            data_a=minimal_df,
            metadata_b={},
            data_b=minimal_df,
            context={},
            verbose=True
        )
        
        # Run stages
        minimal_llamasee.prepare(
            data_a=minimal_df,
            data_b=minimal_df,
            metadata_a={},
            metadata_b={},
            context={}
        )
        minimal_llamasee.fit(keys=['key'], values=['value'])
        minimal_llamasee.compare()
        
        # Verify comparison stage
        compare_stage_logger = minimal_llamasee.stages.get("compare")
        self.assertIsNotNone(compare_stage_logger, "Compare stage logger not found")
        stage_status = minimal_llamasee.stage_manager.get_stage_status("compare")
        self.assertEqual(stage_status, "completed", f"Compare stage not completed. Status: {stage_status}")
        
        # Log high-level information about comparison results
        if hasattr(minimal_llamasee, '_comparison_results') and minimal_llamasee._comparison_results:
            if isinstance(minimal_llamasee._comparison_results, pd.DataFrame):
                logger.info(f"Minimal dataset comparison results: {len(minimal_llamasee._comparison_results)} records")
                logger.info(f"Minimal dataset comparison columns: {list(minimal_llamasee._comparison_results.columns)}")
            else:
                logger.info(f"Minimal dataset comparison results: {minimal_llamasee._comparison_results}")
        else:
            logger.warning("No comparison results available for minimal dataset")
            self.fail("No comparison results available for minimal dataset")
        
        # Generate insights
        minimal_insights = minimal_llamasee.generate_insights()
        
        # Check that insights are generated for minimal datasets
        self.assertGreater(len(minimal_insights), 0)
        
        # Test with identical datasets
        identical_llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_a,
            data_b=self.data_a,
            context=self.context,
            verbose=True
        )
        
        # Run stages
        identical_llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_a,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_a,
            context=self.context
        )
        identical_llamasee.fit()
        identical_llamasee.compare()
        
        # Verify comparison stage
        compare_stage_logger = identical_llamasee.stages.get("compare")
        self.assertIsNotNone(compare_stage_logger, "Compare stage logger not found")
        stage_status = identical_llamasee.stage_manager.get_stage_status("compare")
        self.assertEqual(stage_status, "completed", f"Compare stage not completed. Status: {stage_status}")
        
        # Log high-level information about comparison results
        if hasattr(identical_llamasee, '_comparison_results') and identical_llamasee._comparison_results:
            if isinstance(identical_llamasee._comparison_results, pd.DataFrame):
                logger.info(f"Identical dataset comparison results: {len(identical_llamasee._comparison_results)} records")
                logger.info(f"Identical dataset comparison columns: {list(identical_llamasee._comparison_results.columns)}")
            else:
                logger.info(f"Identical dataset comparison results: {len(identical_llamasee._comparison_results)} items")
                for key, value in identical_llamasee._comparison_results.items():
                    if isinstance(value, dict) and 'summary' in value:
                        logger.info(f"  {key}: {value['summary']}")
        else:
            logger.warning("No comparison results available for identical dataset")
            self.fail("No comparison results available for identical dataset")
        
        # Generate insights
        identical_insights = identical_llamasee.generate_insights()
        
        # Check that insights are generated for identical datasets
        self.assertGreater(len(identical_insights), 0)
        
        # Check that insights reflect the datasets are identical
        for insight in identical_insights:
            if insight.insight_type == 'statistical':
                self.assertIn('identical', insight.description.lower())
                self.assertIn('no difference', insight.description.lower())
    
    def test_compare_method(self):
        """Test the compare method and generate output for individual and dimensional comparisons"""
        # Set dimensions for comparison

        
        # Run compare method
        result = self.llamasee.compare()
        
        # Check that the method returns self for chaining
        self.assertEqual(result, self.llamasee)
        
        # Check that comparison results are not empty
        self.assertIsNotNone(self.llamasee._comparison_results)
        
        # Log the comparison results
        logger.info(f"Comparison results type: {type(self.llamasee._comparison_results)}")
        if isinstance(self.llamasee._comparison_results, pd.DataFrame):
            logger.info(f"Comparison results: {len(self.llamasee._comparison_results)} records")
            logger.info(f"Comparison columns: {list(self.llamasee._comparison_results.columns)}")
        else:
            logger.info(f"Comparison results: {len(self.llamasee._comparison_results)} items")
            for key, value in self.llamasee._comparison_results.items():
                if isinstance(value, dict) and 'summary' in value:
                    logger.info(f"  {key}: {value['summary']}")
        
        # Export individual comparison results
        individual_export_path = os.path.join(self.test_results_dir, "individual_comparison_results.json")
        self.llamasee.export_individual_comparison_results(output_path=individual_export_path, format="json")
        
        # Verify individual export was successful
        self.assertTrue(os.path.exists(individual_export_path), f"Individual export file should exist at {individual_export_path}")
        
        # Load and check individual export content
        with open(individual_export_path, 'r') as f:
            individual_export_data = json.load(f)
        
        # Check that individual export contains expected data
        self.assertIsInstance(individual_export_data, dict)  # Changed from list to dict
        self.assertGreater(len(individual_export_data), 0)
        
        # Check that dimension comparison results are not empty
        self.assertIsNotNone(self.llamasee._dimension_comparison_results)
        self.assertGreater(len(self.llamasee._dimension_comparison_results), 0)

    def test_dimensional_analysis(self):
        """Test dimensional analysis with filtering and aggregation"""
        # Create a new LlamaSee instance for this test
        llamasee = LlamaSee(
            metadata_a=self.metadata_a,
            data_a=self.data_a,
            metadata_b=self.metadata_b,
            data_b=self.data_b,
            context=self.context,
            verbose=True,
            log_level="DEBUG"
        )
        
        # Run prepare stage
        llamasee.prepare(
            data_a=self.data_a,
            data_b=self.data_b,
            metadata_a=self.metadata_a,
            metadata_b=self.metadata_b,
            context=self.context
        )
        
        # Create key enrichment configuration
        key_enrichment = {
            "store_id": {
                "key_column": "store_id",
                "enriched_key": "region",
                "default_value": "Unknown",
                "mappings": {
                    "STORE-13360597": "Southwest",
                    "STORE-16140789": "West",
                    "STORE-16140790": "Northeast",
                    "STORE-16140791": "Southeast",
                    "STORE-16140792": "Midwest"
                }
            }
        }
        
        # Run fit stage with key enrichment
        llamasee.fit(key_enrichment=key_enrichment)
        
        # Run compare stage
        llamasee.compare()
        
        # Get the comparison results
        results = llamasee._canonical_comparison_results
        
        # Log detailed comparison statistics
        logger.info("\n=== Detailed Comparison Statistics ===")
        logger.info(f"Total number of comparison rows: {len(results.rows)}")
        
        # Count rows by match status
        match_status_counts = {}
        for row in results.rows:
            status = row.dimension.get('match_status', 'unknown')
            match_status_counts[status] = match_status_counts.get(status, 0) + 1
        
        logger.info("\nMatch Status Distribution:")
        for status, count in match_status_counts.items():
            percentage = (count / len(results.rows)) * 100
            logger.info(f"  {status}: {count} rows ({percentage:.2f}%)")
        
        # Count rows by region
        region_counts = {}
        for row in results.rows:
            region = row.dimension.get("region", "Unknown")
            region_counts[region] = region_counts.get(region, 0) + 1
        
        logger.info("\nRegion Distribution:")
        for region, count in region_counts.items():
            percentage = (count / len(results.rows)) * 100
            logger.info(f"  {region}: {count} rows ({percentage:.2f}%)")
        
        # Analyze value differences by region
        logger.info("\n=== Value Differences by Region ===")
        for region in region_counts.keys():
            region_rows = [row for row in results.rows if row.dimension.get("region") == region]
            if region_rows:
                total_diff = sum(row.diff for row in region_rows if row.diff is not None)
                avg_diff = total_diff / len(region_rows)
                logger.info(f"\nRegion: {region}")
                logger.info(f"  Total rows: {len(region_rows)}")
                logger.info(f"  Average difference: {avg_diff:.2f}")
                logger.info(f"  Total difference: {total_diff:.2f}")
        
        # Analyze by date range
        logger.info("\n=== Date Range Analysis ===")
        date_rows = {}
        for row in results.rows:
            date = row.key.get("forecast_date")
            if date:
                date_rows[date] = date_rows.get(date, 0) + 1
        
        logger.info("\nRows by Date:")
        for date, count in sorted(date_rows.items()):
            logger.info(f"  {date}: {count} rows")
        
        # Analyze match patterns
        logger.info("\n=== Match Pattern Analysis ===")
        for region in region_counts.keys():
            region_rows = [row for row in results.rows if row.dimension.get("region") == region]
            match_count = sum(1 for row in region_rows if row.dimension.get('match_status') == 'present_in_both')
            a_only_count = sum(1 for row in region_rows if row.dimension.get('match_status') == 'missing_in_b')
            b_only_count = sum(1 for row in region_rows if row.dimension.get('match_status') == 'missing_in_a')
            
            logger.info(f"\nRegion: {region}")
            logger.info(f"  Total rows: {len(region_rows)}")
            logger.info(f"  Matches: {match_count} ({match_count/len(region_rows)*100:.2f}%)")
            logger.info(f"  A-only: {a_only_count} ({a_only_count/len(region_rows)*100:.2f}%)")
            logger.info(f"  B-only: {b_only_count} ({b_only_count/len(region_rows)*100:.2f}%)")
        
        # Analyze value distributions
        logger.info("\n=== Value Distribution Analysis ===")
        for region in region_counts.keys():
            region_rows = [row for row in results.rows if row.dimension.get("region") == region]
            if region_rows:
                values_a = [row.value_a for row in region_rows if row.value_a is not None]
                values_b = [row.value_b for row in region_rows if row.value_b is not None]
                
                if values_a and values_b:
                    avg_a = sum(values_a) / len(values_a)
                    avg_b = sum(values_b) / len(values_b)
                    logger.info(f"\nRegion: {region}")
                    logger.info(f"  Average value A: {avg_a:.2f}")
                    logger.info(f"  Average value B: {avg_b:.2f}")
                    logger.info(f"  Difference: {avg_b - avg_a:.2f}")
        
        # Verify the results
        self.assertGreater(len(results.rows), 0, "No comparison results found")
        self.assertGreater(len(region_counts), 0, "No regions found in results")
        self.assertGreater(len(date_rows), 0, "No dates found in results")
        
        # Verify match status distribution
        total_matches = match_status_counts.get("present_in_both", 0)
        total_a_only = match_status_counts.get("missing_in_b", 0)
        total_b_only = match_status_counts.get("missing_in_a", 0)
        self.assertEqual(total_matches + total_a_only + total_b_only, len(results.rows),
                         "Match status counts don't sum to total rows")

    def test_time_series_insights(self):
        """Test time series analysis insights generation."""
        # Use the data already loaded in setUp
        data_a = self.data_a
        data_b = self.data_b
        
        # Create metadata for both datasets
        metadata_a = {
            'name': 'Forecast Run 1',
            'description': 'First forecast run results',
            'date': '2024-03-01'
        }
        
        metadata_b = {
            'name': 'Forecast Run 2',
            'description': 'Second forecast run results',
            'date': '2024-03-02'
        }
        
        # Initialize LlamaSee with the datasets
        llamasee = LlamaSee(metadata_a, data_a, metadata_b, data_b)
        
        # Prepare the data
        llamasee.prepare(
            data_a=data_a,
            data_b=data_b,
            metadata_a=metadata_a,
            metadata_b=metadata_b,
            context=self.context
        )
        
        # Run the fit stage
        llamasee.fit()
        
        # Run the compare stage with time series analysis
        llamasee.compare(
            aggregation_methods={
                'forecast_value_p50': 'mean',
                'forecast_value_p10': 'mean',
                'forecast_value_p90': 'mean'
            },
            post_comparison_enrichment={
                'time_series': {
                    'enabled': True,
                    'trend_detection': True,
                    'anomaly_detection': True
                }
            }
        )
        
        # Get the insights
        insights = llamasee.generate_insights()
        
        # Verify that we have both trend and anomaly insights
        trend_insights = [i for i in insights if i.insight_type == 'trend']
        anomaly_insights = [i for i in insights if i.insight_type == 'anomaly']
        
        assert len(trend_insights) > 0, "No trend insights were generated"
        assert len(anomaly_insights) > 0, "No anomaly insights were generated"
        
        # Verify trend insight properties
        for insight in trend_insights:
            assert insight.scope_level in ['aggregate', 'dimension', 'individual']
            assert insight.metric in ['forecast_value_p50', 'forecast_value_p10', 'forecast_value_p90']
            assert 'slope' in insight.value
            assert 'r_squared' in insight.value
            assert 'p_value' in insight.value
            assert 0 <= insight.significance <= 1
        
        # Verify anomaly insight properties
        for insight in anomaly_insights:
            assert insight.scope_level in ['aggregate', 'dimension', 'individual']
            assert insight.metric in ['forecast_value_p50', 'forecast_value_p10', 'forecast_value_p90']
            assert 'z_score' in insight.value
            assert 0 <= insight.significance <= 1
        
        # Verify that descriptions are informative
        for insight in insights:
            assert len(insight.description) > 0
            assert insight.metric in insight.description
            if insight.insight_type == 'trend':
                assert 'trend' in insight.description.lower()
            else:
                assert 'anomaly' in insight.description.lower()
        
        # Verify that significant insights have high significance scores
        significant_insights = [i for i in insights if i.significance > 0.7]
        assert len(significant_insights) > 0, "No significant insights were found"
        
        # Verify that insights are properly sorted by significance
        sorted_insights = sorted(insights, key=lambda x: x.significance, reverse=True)
        assert insights == sorted_insights, "Insights are not properly sorted by significance"

if __name__ == '__main__':
    unittest.main() 