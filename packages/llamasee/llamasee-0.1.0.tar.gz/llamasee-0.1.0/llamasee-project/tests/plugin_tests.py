#!/usr/bin/env python3
"""
Tests for the plugin discovery and filtering functionality.
"""

import os
import sys
import unittest
import logging
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from llamasee.plugins.manager import PluginManager
from llamasee.plugins.insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin

# Configure logging
logger = logging.getLogger(__name__)

class TestPluginDiscovery(unittest.TestCase):
    """Test cases for plugin discovery functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary plugin directory for testing
        self.plugin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_plugins")
        os.makedirs(self.plugin_dir, exist_ok=True)
        
        # Create a mock plugin manager
        self.plugin_manager = PluginManager(plugin_dir=self.plugin_dir)
        
        # Create mock plugins
        self.create_mock_plugins()
    
    def tearDown(self):
        """Clean up the test environment."""
        # Remove the temporary plugin directory
        import shutil
        if os.path.exists(self.plugin_dir):
            shutil.rmtree(self.plugin_dir)
    
    def create_mock_plugins(self):
        """Create mock plugins for testing."""
        # Create a data science plugin
        data_science_plugin_path = os.path.join(self.plugin_dir, "data_science_plugin.py")
        with open(data_science_plugin_path, "w") as f:
            f.write("""
from llamasee.plugins.insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin

class DataSciencePlugin(InsightPlugin):
    def generate_insights(self, comparison_results, context=None):
        return []
    
    def enhance_insights(self, insights, context=None):
        return insights
    
    def categorize_insights(self, insights):
        return insights
    
    def score_insights(self, insights):
        return insights
    
    def get_insight_types(self):
        return ["data_science"]
    
    def get_insight_categories(self):
        return ["statistical", "trend", "anomaly"]
    
    def get_scoring_factors(self):
        return ["importance", "uniqueness", "business_impact"]
""")
        
        # Create a data structure plugin
        data_structure_plugin_path = os.path.join(self.plugin_dir, "data_structure_plugin.py")
        with open(data_structure_plugin_path, "w") as f:
            f.write("""
from llamasee.plugins.insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin

class DataStructurePlugin(InsightPlugin):
    def generate_insights(self, comparison_results, context=None):
        return []
    
    def enhance_insights(self, insights, context=None):
        return insights
    
    def categorize_insights(self, insights):
        return insights
    
    def score_insights(self, insights):
        return insights
    
    def get_insight_types(self):
        return ["data_structure"]
    
    def get_insight_categories(self):
        return ["column", "key", "schema"]
    
    def get_scoring_factors(self):
        return ["importance", "uniqueness", "business_impact"]
""")
        
        # Create a context plugin
        context_plugin_path = os.path.join(self.plugin_dir, "context_plugin.py")
        with open(context_plugin_path, "w") as f:
            f.write("""
from llamasee.plugins.insight.base_insight_plugin import BaseInsightPlugin as InsightPlugin

class ContextPlugin(InsightPlugin):
    def generate_insights(self, comparison_results, context=None):
        return []
    
    def enhance_insights(self, insights, context=None):
        return insights
    
    def categorize_insights(self, insights):
        return insights
    
    def score_insights(self, insights):
        return insights
    
    def get_insight_types(self):
        return ["context"]
    
    def get_insight_categories(self):
        return ["dataset", "forecast", "summary"]
    
    def get_scoring_factors(self):
        return ["importance", "uniqueness", "business_impact"]
""")
    
    def test_plugin_discovery(self):
        """Test that plugins are correctly discovered."""
        # Discover plugins
        discovered_plugins = self.plugin_manager.discover_plugins()
        
        # Verify that all plugin types are discovered
        self.assertIn("insight", discovered_plugins)
        self.assertEqual(len(discovered_plugins["insight"]), 3)
        
        # Verify that the plugin names are correct
        plugin_names = [os.path.basename(p).replace(".py", "") for p in discovered_plugins["insight"]]
        self.assertIn("data_science_plugin", plugin_names)
        self.assertIn("data_structure_plugin", plugin_names)
        self.assertIn("context_plugin", plugin_names)

class TestPluginFiltering(unittest.TestCase):
    """Test cases for plugin filtering functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a mock plugin manager
        self.plugin_manager = PluginManager()
        
        # Create mock plugins
        self.data_science_plugin = MagicMock(spec=InsightPlugin)
        self.data_science_plugin.get_insight_types.return_value = ["data_science"]
        self.data_science_plugin.get_insight_categories.return_value = ["statistical", "trend", "anomaly"]
        
        self.data_structure_plugin = MagicMock(spec=InsightPlugin)
        self.data_structure_plugin.get_insight_types.return_value = ["data_structure"]
        self.data_structure_plugin.get_insight_categories.return_value = ["column", "key", "schema"]
        
        self.context_plugin = MagicMock(spec=InsightPlugin)
        self.context_plugin.get_insight_types.return_value = ["context"]
        self.context_plugin.get_insight_categories.return_value = ["dataset", "forecast", "summary"]
        
        # Register the plugins with the plugin manager
        self.plugin_manager.registry.register_plugin("data_science_plugin", self.data_science_plugin)
        self.plugin_manager.registry.register_plugin("data_structure_plugin", self.data_structure_plugin)
        self.plugin_manager.registry.register_plugin("context_plugin", self.context_plugin)
    
    def test_filter_by_type(self):
        """Test filtering plugins by insight type."""
        # Filter plugins by data science type
        data_science_plugins = self.plugin_manager.get_insight_plugins_by_type("data_science")
        
        # Verify that only data science plugins are returned
        self.assertEqual(len(data_science_plugins), 1)
        self.assertEqual(data_science_plugins[0], self.data_science_plugin)
        
        # Filter plugins by data structure type
        data_structure_plugins = self.plugin_manager.get_insight_plugins_by_type("data_structure")
        
        # Verify that only data structure plugins are returned
        self.assertEqual(len(data_structure_plugins), 1)
        self.assertEqual(data_structure_plugins[0], self.data_structure_plugin)
        
        # Filter plugins by context type
        context_plugins = self.plugin_manager.get_insight_plugins_by_type("context")
        
        # Verify that only context plugins are returned
        self.assertEqual(len(context_plugins), 1)
        self.assertEqual(context_plugins[0], self.context_plugin)
    
    def test_filter_by_scope(self):
        """Test filtering plugins by scope level."""
        # Set up scope levels for the plugins
        self.data_science_plugin.get_scope_levels.return_value = ["aggregate", "dimension"]
        self.data_structure_plugin.get_scope_levels.return_value = ["dimension", "individual"]
        self.context_plugin.get_scope_levels.return_value = ["aggregate"]
        
        # Filter plugins by aggregate scope
        aggregate_plugins = self.plugin_manager.get_insight_plugins_by_scope("aggregate")
        
        # Verify that only plugins with aggregate scope are returned
        self.assertEqual(len(aggregate_plugins), 2)
        self.assertIn(self.data_science_plugin, aggregate_plugins)
        self.assertIn(self.context_plugin, aggregate_plugins)
        
        # Filter plugins by dimension scope
        dimension_plugins = self.plugin_manager.get_insight_plugins_by_scope("dimension")
        
        # Verify that only plugins with dimension scope are returned
        self.assertEqual(len(dimension_plugins), 2)
        self.assertIn(self.data_science_plugin, dimension_plugins)
        self.assertIn(self.data_structure_plugin, dimension_plugins)
        
        # Filter plugins by individual scope
        individual_plugins = self.plugin_manager.get_insight_plugins_by_scope("individual")
        
        # Verify that only plugins with individual scope are returned
        self.assertEqual(len(individual_plugins), 1)
        self.assertEqual(individual_plugins[0], self.data_structure_plugin)
    
    def test_filter_by_traceability(self):
        """Test filtering plugins by traceability requirements."""
        # Set up traceability capabilities for the plugins
        self.data_science_plugin.get_traceability_capabilities.return_value = {
            "data_indices": True,
            "column_references": True,
            "dimension_context": False
        }
        self.data_structure_plugin.get_traceability_capabilities.return_value = {
            "data_indices": False,
            "column_references": True,
            "dimension_context": True
        }
        self.context_plugin.get_traceability_capabilities.return_value = {
            "data_indices": False,
            "column_references": False,
            "dimension_context": True
        }
        
        # Filter plugins by data indices traceability
        data_indices_plugins = self.plugin_manager.get_insight_plugins_by_traceability({"data_indices": True})
        
        # Verify that only plugins with data indices traceability are returned
        self.assertEqual(len(data_indices_plugins), 1)
        self.assertEqual(data_indices_plugins[0], self.data_science_plugin)
        
        # Filter plugins by column references traceability
        column_references_plugins = self.plugin_manager.get_insight_plugins_by_traceability({"column_references": True})
        
        # Verify that only plugins with column references traceability are returned
        self.assertEqual(len(column_references_plugins), 2)
        self.assertIn(self.data_science_plugin, column_references_plugins)
        self.assertIn(self.data_structure_plugin, column_references_plugins)
        
        # Filter plugins by dimension context traceability
        dimension_context_plugins = self.plugin_manager.get_insight_plugins_by_traceability({"dimension_context": True})
        
        # Verify that only plugins with dimension context traceability are returned
        self.assertEqual(len(dimension_context_plugins), 2)
        self.assertIn(self.data_structure_plugin, dimension_context_plugins)
        self.assertIn(self.context_plugin, dimension_context_plugins)

if __name__ == "__main__":
    unittest.main() 