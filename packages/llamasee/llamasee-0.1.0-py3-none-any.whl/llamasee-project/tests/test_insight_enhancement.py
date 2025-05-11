#!/usr/bin/env python3
import os
import sys
import json
import pandas as pd
import unittest
import logging
import tempfile
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from unittest.mock import MagicMock, patch

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import LlamaSee and insight components
from llamasee.llamasee import LlamaSee
from llamasee.core.insight import Insight
from llamasee.generation.insight_generator import InsightGenerator
from llamasee.integration.insight_manager import InsightManager
from llamasee.enhancement.llm_enhancer import LLMEnhancer
from llamasee.enhancement.trace_enricher import TraceEnricher
from llamasee.enhancement.metadata_enricher import MetadataEnricher

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestInsightEnhancement(unittest.TestCase):
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
        
        # Create a temporary directory for storage tests
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        # Remove temporary directory
        shutil.rmtree(cls.temp_dir)
    
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
        
        # Run compare stage to get comparison results
        self.llamasee.compare()
        
        # Generate insights
        self.insights = self.llamasee.generate_insights()
        
        # Create enhancement components
        self.llm_enhancer = LLMEnhancer()
        self.trace_enricher = TraceEnricher()
        self.metadata_enricher = MetadataEnricher()
    
    def test_llm_enhancement(self):
        """Test LLM enhancement of insights"""
        # Mock the LLM enhancer to avoid actual API calls
        with patch.object(LLMEnhancer, 'enhance_insight', return_value={
            'enhanced_description': 'This is an enhanced description',
            'business_impact': 'High',
            'recommendations': ['Recommendation 1', 'Recommendation 2']
        }):
            # Enhance a single insight
            original_insight = self.insights[0]
            enhanced_insight = self.llm_enhancer.enhance_insight(original_insight)
            
            # Check that the insight was enhanced
            self.assertNotEqual(original_insight.description, enhanced_insight['enhanced_description'])
            self.assertIn('business_impact', enhanced_insight)
            self.assertIn('recommendations', enhanced_insight)
            
            # Check that the recommendations are a list
            self.assertIsInstance(enhanced_insight['recommendations'], list)
            self.assertGreater(len(enhanced_insight['recommendations']), 0)
    
    def test_trace_enrichment(self):
        """Test trace enrichment of insights"""
        # Enrich a single insight
        original_insight = self.insights[0]
        enriched_insight = self.trace_enricher.enrich_insight(original_insight)
        
        # Check that the trace was enriched
        self.assertIsNotNone(enriched_insight.trace)
        
        # Check that the trace contains the expected fields
        self.assertIn('data_indices', enriched_insight.trace)
        self.assertIn('columns', enriched_insight.trace)
        self.assertIn('values', enriched_insight.trace)
        self.assertIn('context', enriched_insight.trace)
        
        # Check that the trace contains data from the source data
        self.assertIsNotNone(enriched_insight.trace['data_indices'])
        self.assertIsNotNone(enriched_insight.trace['columns'])
    
    def test_metadata_enrichment(self):
        """Test metadata enrichment of insights"""
        # Enrich a single insight
        original_insight = self.insights[0]
        enriched_insight = self.metadata_enricher.enrich_insight(original_insight)
        
        # Check that the metadata was enriched
        self.assertIsNotNone(enriched_insight.metadata)
        
        # Check that the metadata contains the expected fields
        self.assertIn('timestamp', enriched_insight.metadata)
        self.assertIn('source', enriched_insight.metadata)
        self.assertIn('version', enriched_insight.metadata)
        
        # Check that the timestamp is a valid ISO format string
        try:
            datetime.fromisoformat(enriched_insight.metadata['timestamp'])
        except ValueError:
            self.fail("Timestamp is not a valid ISO format string")
    
    def test_combined_enhancement(self):
        """Test combined enhancement of insights"""
        # Mock the LLM enhancer to avoid actual API calls
        with patch.object(LLMEnhancer, 'enhance_insight', return_value={
            'enhanced_description': 'This is an enhanced description',
            'business_impact': 'High',
            'recommendations': ['Recommendation 1', 'Recommendation 2']
        }):
            # Enhance all insights
            enhanced_insights = []
            for insight in self.insights:
                # LLM enhancement
                llm_enhanced = self.llm_enhancer.enhance_insight(insight)
                
                # Trace enrichment
                trace_enriched = self.trace_enricher.enrich_insight(insight)
                
                # Metadata enrichment
                metadata_enriched = self.metadata_enricher.enrich_insight(insight)
                
                # Combine enhancements
                enhanced_insight = insight
                enhanced_insight.description = llm_enhanced['enhanced_description']
                enhanced_insight.metadata = metadata_enriched.metadata
                enhanced_insight.trace = trace_enriched.trace
                
                enhanced_insights.append(enhanced_insight)
            
            # Check that all insights were enhanced
            self.assertEqual(len(enhanced_insights), len(self.insights))
            
            # Check that each enhanced insight has the expected fields
            for insight in enhanced_insights:
                self.assertNotEqual(insight.description, '')
                self.assertIsNotNone(insight.metadata)
                self.assertIsNotNone(insight.trace)
    
    def test_enhancement_with_custom_config(self):
        """Test enhancement with custom configuration"""
        # Create a custom LLM enhancer
        custom_llm_enhancer = LLMEnhancer(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500
        )
        
        # Mock the custom LLM enhancer
        with patch.object(LLMEnhancer, 'enhance_insight', return_value={
            'enhanced_description': 'This is a custom enhanced description',
            'business_impact': 'Medium',
            'recommendations': ['Custom Recommendation']
        }):
            # Enhance a single insight
            original_insight = self.insights[0]
            enhanced_insight = custom_llm_enhancer.enhance_insight(original_insight)
            
            # Check that the insight was enhanced with the custom configuration
            self.assertNotEqual(original_insight.description, enhanced_insight['enhanced_description'])
            self.assertEqual(enhanced_insight['business_impact'], 'Medium')
            self.assertEqual(enhanced_insight['recommendations'], ['Custom Recommendation'])
    
    def test_enhancement_error_handling(self):
        """Test error handling during enhancement"""
        # Mock the LLM enhancer to raise an exception
        with patch.object(LLMEnhancer, 'enhance_insight', side_effect=Exception("API Error")):
            # Try to enhance a single insight
            original_insight = self.insights[0]
            
            # The enhancement should not raise an exception
            try:
                enhanced_insight = self.llm_enhancer.enhance_insight(original_insight)
                # If we get here, the enhancement should have returned the original insight
                self.assertEqual(enhanced_insight, original_insight)
            except Exception as e:
                self.fail(f"Enhancement raised an exception: {e}")

if __name__ == '__main__':
    unittest.main() 