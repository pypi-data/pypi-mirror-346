"""
Basic insight plugin for LlamaSee.

This plugin generates basic insights from comparison results, focusing on
key differences, value differences, and dimension analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
import logging
import uuid
from ...core.insight import Insight
from ...schema.comparison import ComparisonResultRow
from .base_insight_plugin import BaseInsightPlugin as InsightPlugin
from ...utils.trace import TraceManager

class BasicInsightPlugin(InsightPlugin):
    """
    Basic insight plugin that generates insights from comparison results.
    """
    
    def __init__(self):
        """Initialize the plugin."""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self.name = "BasicInsightPlugin"
        self.version = "1.0.0"
        self.insight_type = "standard"
        self.trace_manager = TraceManager()
        self.insight_types = ['standard']
        self.scope_levels = ['aggregate', 'dimension', 'individual']
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Configuration dictionary for the plugin
        """
        self.config = config
        self.logger.info(f"Initialized {self.name} with configuration")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate the configuration for this plugin.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if configuration is valid
        """
        # No specific validation needed for this plugin
        return True
    
    def get_name(self) -> str:
        """
        Get the name of the plugin.
        
        Returns:
            Plugin name
        """
        return self.name
    
    def get_description(self) -> str:
        """
        Get the description of the plugin.
        
        Returns:
            Plugin description
        """
        return "Generates basic insights from comparison results, focusing on key differences, value differences, and dimension analysis."
    
    def get_version(self) -> str:
        """
        Get the version of the plugin.
        
        Returns:
            Plugin version
        """
        return self.version
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get the capabilities of the plugin.
        
        Returns:
            Dictionary of plugin capabilities
        """
        return {
            "insight_types": self.get_insight_types(),
            "insight_categories": self.get_insight_categories(),
            "scoring_factors": self.get_scoring_factors()
        }
    
    def generate_insights(
        self, 
        comparison_results: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate insights from comparison results.
        
        Args:
            comparison_results: Results from a comparison operation
            context: Optional context information
            limit: Optional limit on the number of insights to return
            
        Returns:
            List of generated insights
        """
        self.logger.info(f"Generating insights with {self.name}")
        
        insights = []
        
        # Generate key difference insights
        if "key_differences" in comparison_results:
            key_insights = self._generate_key_difference_insights(comparison_results["key_differences"])
            insights.extend(key_insights)
        
        # Generate value difference insights
        if "value_differences" in comparison_results:
            value_insights = self._generate_value_difference_insights(comparison_results["value_differences"])
            insights.extend(value_insights)
        
        # Generate dimension analysis insights
        if "dimension_analysis" in comparison_results:
            dimension_insights = self._generate_dimension_insights(comparison_results["dimension_analysis"])
            insights.extend(dimension_insights)
        
        # Generate summary insights
        if "summary" in comparison_results:
            summary_insights = self._generate_summary_insights(comparison_results["summary"])
            insights.extend(summary_insights)
        
        # Score insights
        scored_insights = self.score_insights(insights)
        
        # Sort by score (descending)
        scored_insights.sort(key=lambda x: x["score"], reverse=True)
        
        # Apply limit if provided
        if limit is not None:
            scored_insights = scored_insights[:limit]
        
        return scored_insights
    
    def enhance_insights(
        self, 
        insights: List[Dict[str, Any]], 
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Enhance existing insights with additional information.
        
        Args:
            insights: List of insights to enhance
            context: Optional context information
            
        Returns:
            List of enhanced insights
        """
        self.logger.info(f"Enhancing insights with {self.name}")
        
        enhanced_insights = []
        
        for insight in insights:
            # Create a copy of the insight
            enhanced_insight = insight.copy()
            
            # Add business impact if not present
            if "business_impact" not in enhanced_insight:
                enhanced_insight["business_impact"] = self._calculate_business_impact(insight)
            
            # Add recommendations if not present
            if "recommendations" not in enhanced_insight:
                enhanced_insight["recommendations"] = self._generate_recommendations(insight)
            
            # Add traceability if not present
            if "traceability" not in enhanced_insight:
                enhanced_insight["traceability"] = self._generate_traceability(insight)
            
            enhanced_insights.append(enhanced_insight)
        
        return enhanced_insights
    
    def categorize_insights(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Categorize insights by type and scope.
        
        Args:
            insights: List of insights to categorize
            
        Returns:
            List of categorized insights
        """
        self.logger.info(f"Categorizing insights with {self.name}")
        
        categorized_insights = []
        
        for insight in insights:
            # Create a copy of the insight
            categorized_insight = insight.copy()
            
            # Determine insight type
            if "type" not in categorized_insight:
                categorized_insight["type"] = self._determine_insight_type(insight)
            
            # Determine insight scope
            if "scope" not in categorized_insight:
                categorized_insight["scope"] = self._determine_insight_scope(insight)
            
            # Determine insight category
            if "category" not in categorized_insight:
                categorized_insight["category"] = self._determine_insight_category(insight)
            
            categorized_insights.append(categorized_insight)
        
        return categorized_insights
    
    def score_insights(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score insights based on multiple factors.
        
        Args:
            insights: List of insights to score
            
        Returns:
            List of scored insights
        """
        self.logger.info(f"Scoring insights with {self.name}")
        
        scored_insights = []
        
        for insight in insights:
            # Create a copy of the insight
            scored_insight = insight.copy()
            
            # Calculate score based on multiple factors
            score = self._calculate_insight_score(insight)
            
            # Add score to insight
            scored_insight["score"] = score
            
            scored_insights.append(scored_insight)
        
        return scored_insights
    
    def _generate_key_difference_insights(self, key_differences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from key differences.
        
        Args:
            key_differences: Dictionary of key differences
            
        Returns:
            List of key difference insights
        """
        insights = []
        
        for key, differences in key_differences.items():
            # Skip if there's an error
            if "error" in differences:
                continue
            
            # Check for keys only in dataset A
            if differences["count_only_in_a"] > 0:
                insights.append({
                    "type": "key_difference",
                    "category": "missing_data",
                    "scope": "individual",
                    "title": f"Keys only in dataset A: {key}",
                    "description": f"Found {differences['count_only_in_a']} keys in dataset A that are not in dataset B for column '{key}'",
                    "details": {
                        "key": key,
                        "count": differences["count_only_in_a"],
                        "values": differences["only_in_a"]
                    },
                    "severity": "medium" if differences["count_only_in_a"] < 10 else "high"
                })
            
            # Check for keys only in dataset B
            if differences["count_only_in_b"] > 0:
                insights.append({
                    "type": "key_difference",
                    "category": "new_data",
                    "scope": "individual",
                    "title": f"Keys only in dataset B: {key}",
                    "description": f"Found {differences['count_only_in_b']} keys in dataset B that are not in dataset A for column '{key}'",
                    "details": {
                        "key": key,
                        "count": differences["count_only_in_b"],
                        "values": differences["only_in_b"]
                    },
                    "severity": "medium" if differences["count_only_in_b"] < 10 else "high"
                })
        
        return insights
    
    def _generate_value_difference_insights(self, value_differences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from value differences.
        
        Args:
            value_differences: Dictionary of value differences
            
        Returns:
            List of value difference insights
        """
        insights = []
        
        for value, value_results in value_differences.items():
            # Skip if there's an error
            if "error" in value_results:
                continue
            
            # Process each key's results
            for key, key_results in value_results.items():
                # Skip if no results
                if not key_results:
                    continue
                
                # Count significant differences
                significant_count = sum(1 for r in key_results if "is_significant" in r and r["is_significant"])
                
                if significant_count > 0:
                    # Find the largest difference
                    largest_diff = max(key_results, key=lambda x: abs(x.get("pct_diff", 0)))
                    
                    insights.append({
                        "type": "value_difference",
                        "category": "anomaly",
                        "scope": "individual",
                        "title": f"Significant value differences for {value}",
                        "description": f"Found {significant_count} significant differences in values for column '{value}' when comparing by '{key}'",
                        "details": {
                            "value": value,
                            "key": key,
                            "count": significant_count,
                            "largest_difference": {
                                "key_value": largest_diff["key_value"],
                                "value_a": largest_diff["value_a"],
                                "value_b": largest_diff["value_b"],
                                "pct_diff": largest_diff["pct_diff"]
                            }
                        },
                        "severity": "medium" if significant_count < 5 else "high"
                    })
        
        return insights
    
    def _generate_dimension_insights(self, dimension_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from dimension analysis.
        
        Args:
            dimension_analysis: Dictionary of dimension analysis results
            
        Returns:
            List of dimension insights
        """
        insights = []
        
        for dimension, results in dimension_analysis.items():
            # Skip if there's an error
            if "error" in results:
                continue
            
            # Check for dimension value differences
            unique_values_a = set(results["unique_values"]["a"])
            unique_values_b = set(results["unique_values"]["b"])
            
            only_in_a = unique_values_a - unique_values_b
            only_in_b = unique_values_b - unique_values_a
            
            if only_in_a:
                insights.append({
                    "type": "dimension_difference",
                    "category": "missing_data",
                    "scope": "dimension",
                    "title": f"Dimension values only in dataset A: {dimension}",
                    "description": f"Found {len(only_in_a)} dimension values in dataset A that are not in dataset B for dimension '{dimension}'",
                    "details": {
                        "dimension": dimension,
                        "count": len(only_in_a),
                        "values": list(only_in_a)
                    },
                    "severity": "medium" if len(only_in_a) < 5 else "high"
                })
            
            if only_in_b:
                insights.append({
                    "type": "dimension_difference",
                    "category": "new_data",
                    "scope": "dimension",
                    "title": f"Dimension values only in dataset B: {dimension}",
                    "description": f"Found {len(only_in_b)} dimension values in dataset B that are not in dataset A for dimension '{dimension}'",
                    "details": {
                        "dimension": dimension,
                        "count": len(only_in_b),
                        "values": list(only_in_b)
                    },
                    "severity": "medium" if len(only_in_b) < 5 else "high"
                })
            
            # Check for value differences by dimension
            for value, value_results in results["value_differences"].items():
                # Skip if no results
                if not value_results:
                    continue
                
                # Count significant differences
                significant_count = sum(1 for r in value_results if "is_significant" in r and r["is_significant"])
                
                if significant_count > 0:
                    # Find the largest difference
                    largest_diff = max(value_results, key=lambda x: abs(x.get("pct_diff", 0)))
                    
                    insights.append({
                        "type": "dimension_value_difference",
                        "category": "anomaly",
                        "scope": "dimension",
                        "title": f"Significant value differences by {dimension}",
                        "description": f"Found {significant_count} significant differences in values for column '{value}' when analyzing by dimension '{dimension}'",
                        "details": {
                            "dimension": dimension,
                            "value": value,
                            "count": significant_count,
                            "largest_difference": {
                                "dimension_value": largest_diff["dimension_value"],
                                "value_a": largest_diff["value_a"],
                                "value_b": largest_diff["value_b"],
                                "pct_diff": largest_diff["pct_diff"]
                            }
                        },
                        "severity": "medium" if significant_count < 5 else "high"
                    })
        
        return insights
    
    def _generate_summary_insights(self, summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate insights from summary information.
        
        Args:
            summary: Dictionary of summary information
            
        Returns:
            List of summary insights
        """
        insights = []
        
        # Check for key differences
        if summary["key_differences_count"] > 0:
            insights.append({
                "type": "summary",
                "category": "difference",
                "scope": "global",
                "title": "Key differences detected",
                "description": f"Found differences in {summary['key_differences_count']} out of {summary['total_keys']} keys",
                "details": {
                    "key_differences_count": summary["key_differences_count"],
                    "total_keys": summary["total_keys"]
                },
                "severity": "medium" if summary["key_differences_count"] < summary["total_keys"] / 2 else "high"
            })
        
        # Check for value differences
        if summary["value_differences_count"] > 0:
            insights.append({
                "type": "summary",
                "category": "difference",
                "scope": "global",
                "title": "Value differences detected",
                "description": f"Found differences in {summary['value_differences_count']} out of {summary['total_values']} values",
                "details": {
                    "value_differences_count": summary["value_differences_count"],
                    "total_values": summary["total_values"]
                },
                "severity": "medium" if summary["value_differences_count"] < summary["total_values"] / 2 else "high"
            })
        
        # Check for significant differences
        if summary["significant_differences"]:
            insights.append({
                "type": "summary",
                "category": "anomaly",
                "scope": "global",
                "title": "Significant differences detected",
                "description": f"Found {len(summary['significant_differences'])} significant differences in values",
                "details": {
                    "significant_differences_count": len(summary["significant_differences"]),
                    "significant_differences": summary["significant_differences"]
                },
                "severity": "high"
            })
        
        return insights
    
    def _calculate_business_impact(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate the business impact of an insight.
        
        Args:
            insight: Insight to calculate business impact for
            
        Returns:
            Dictionary of business impact information
        """
        # Default impact
        impact = {
            "level": "low",
            "description": "No significant business impact identified",
            "affected_areas": []
        }
        
        # Determine impact based on insight type and severity
        if insight["type"] == "key_difference":
            if insight["severity"] == "high":
                impact["level"] = "high"
                impact["description"] = "Missing or new keys may indicate data quality issues or schema changes"
                impact["affected_areas"] = ["data_quality", "schema"]
            elif insight["severity"] == "medium":
                impact["level"] = "medium"
                impact["description"] = "Some missing or new keys may require attention"
                impact["affected_areas"] = ["data_quality"]
        
        elif insight["type"] == "value_difference":
            if insight["severity"] == "high":
                impact["level"] = "high"
                impact["description"] = "Large value differences may indicate data anomalies or errors"
                impact["affected_areas"] = ["data_quality", "accuracy"]
            elif insight["severity"] == "medium":
                impact["level"] = "medium"
                impact["description"] = "Some value differences may require investigation"
                impact["affected_areas"] = ["data_quality"]
        
        elif insight["type"] == "dimension_difference":
            if insight["severity"] == "high":
                impact["level"] = "high"
                impact["description"] = "Missing or new dimension values may affect analysis and reporting"
                impact["affected_areas"] = ["analysis", "reporting"]
            elif insight["severity"] == "medium":
                impact["level"] = "medium"
                impact["description"] = "Some dimension differences may affect specific analyses"
                impact["affected_areas"] = ["analysis"]
        
        elif insight["type"] == "dimension_value_difference":
            if insight["severity"] == "high":
                impact["level"] = "high"
                impact["description"] = "Large differences in dimension values may indicate systemic issues"
                impact["affected_areas"] = ["data_quality", "analysis"]
            elif insight["severity"] == "medium":
                impact["level"] = "medium"
                impact["description"] = "Some dimension value differences may require attention"
                impact["affected_areas"] = ["data_quality"]
        
        elif insight["type"] == "summary":
            if insight["severity"] == "high":
                impact["level"] = "high"
                impact["description"] = "Multiple significant differences detected across the dataset"
                impact["affected_areas"] = ["data_quality", "accuracy", "analysis"]
            elif insight["severity"] == "medium":
                impact["level"] = "medium"
                impact["description"] = "Some differences detected that may require attention"
                impact["affected_areas"] = ["data_quality"]
        
        return impact
    
    def _generate_recommendations(self, insight: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations for an insight.
        
        Args:
            insight: Insight to generate recommendations for
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Generate recommendations based on insight type and severity
        if insight["type"] == "key_difference":
            if insight["severity"] == "high":
                recommendations.append("Investigate the cause of missing or new keys")
                recommendations.append("Update data validation rules to catch these issues")
                recommendations.append("Consider adding automated tests for key consistency")
            elif insight["severity"] == "medium":
                recommendations.append("Review the missing or new keys to ensure they are expected")
                recommendations.append("Document any intentional changes to the key structure")
        
        elif insight["type"] == "value_difference":
            if insight["severity"] == "high":
                recommendations.append("Investigate the cause of large value differences")
                recommendations.append("Check for data processing or transformation issues")
                recommendations.append("Verify the accuracy of the data sources")
            elif insight["severity"] == "medium":
                recommendations.append("Review the value differences to ensure they are expected")
                recommendations.append("Document any intentional changes to the values")
        
        elif insight["type"] == "dimension_difference":
            if insight["severity"] == "high":
                recommendations.append("Investigate the cause of missing or new dimension values")
                recommendations.append("Update dimension hierarchies if needed")
                recommendations.append("Ensure consistent dimension handling across systems")
            elif insight["severity"] == "medium":
                recommendations.append("Review the dimension differences to ensure they are expected")
                recommendations.append("Document any intentional changes to the dimensions")
        
        elif insight["type"] == "dimension_value_difference":
            if insight["severity"] == "high":
                recommendations.append("Investigate the cause of large dimension value differences")
                recommendations.append("Check for dimension aggregation or rollup issues")
                recommendations.append("Verify the consistency of dimension hierarchies")
            elif insight["severity"] == "medium":
                recommendations.append("Review the dimension value differences to ensure they are expected")
                recommendations.append("Document any intentional changes to the dimension values")
        
        elif insight["type"] == "summary":
            if insight["severity"] == "high":
                recommendations.append("Conduct a comprehensive review of the data quality")
                recommendations.append("Implement additional data validation checks")
                recommendations.append("Consider setting up automated data quality monitoring")
            elif insight["severity"] == "medium":
                recommendations.append("Review the differences to ensure they are expected")
                recommendations.append("Document any intentional changes to the data")
        
        return recommendations
    
    def _generate_traceability(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate traceability information for an insight.
        
        Args:
            insight: Insight to generate traceability for
            
        Returns:
            Dictionary of traceability information
        """
        # Create a trace object
        trace = self.trace_manager.create_trace()
        
        # Add data points based on insight type
        if insight["type"] == "key_difference":
            if "details" in insight and "key" in insight["details"]:
                trace = self.trace_manager.add_dataset_trace(
                    trace,
                    "dataset_a",
                    columns=[insight["details"]["key"]]
                )
                trace = self.trace_manager.add_dataset_trace(
                    trace,
                    "dataset_b",
                    columns=[insight["details"]["key"]]
                )
        
        elif insight["type"] == "value_difference":
            if "details" in insight:
                if "value" in insight["details"]:
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_a",
                        columns=[insight["details"]["value"]]
                    )
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_b",
                        columns=[insight["details"]["value"]]
                    )
                if "key" in insight["details"]:
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_a",
                        columns=[insight["details"]["key"]]
                    )
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_b",
                        columns=[insight["details"]["key"]]
                    )
        
        elif insight["type"] == "dimension_difference":
            if "details" in insight and "dimension" in insight["details"]:
                trace = self.trace_manager.add_dimension_trace(
                    trace,
                    insight["details"]["dimension"],
                    "all"
                )
        
        elif insight["type"] == "dimension_value_difference":
            if "details" in insight:
                if "dimension" in insight["details"]:
                    trace = self.trace_manager.add_dimension_trace(
                        trace,
                        insight["details"]["dimension"],
                        "all"
                    )
                if "value" in insight["details"]:
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_a",
                        columns=[insight["details"]["value"]]
                    )
                    trace = self.trace_manager.add_dataset_trace(
                        trace,
                        "dataset_b",
                        columns=[insight["details"]["value"]]
                    )
        
        elif insight["type"] == "summary":
            if "details" in insight:
                if "key_differences_count" in insight["details"]:
                    trace = self.trace_manager.add_comparison_trace(
                        trace,
                        "key_differences_count",
                        insight["details"]["key_differences_count"]
                    )
                if "value_differences_count" in insight["details"]:
                    trace = self.trace_manager.add_comparison_trace(
                        trace,
                        "value_differences_count",
                        insight["details"]["value_differences_count"]
                    )
        
        return trace
    
    def _determine_insight_type(self, insight: Dict[str, Any]) -> str:
        """
        Determine the type of an insight.
        
        Args:
            insight: Insight to determine type for
            
        Returns:
            Insight type
        """
        # Use the type if already set
        if "type" in insight:
            return insight["type"]
        
        # Determine type based on content
        if "key_differences" in insight.get("details", {}):
            return "key_difference"
        elif "value_differences" in insight.get("details", {}):
            return "value_difference"
        elif "dimension" in insight.get("details", {}):
            return "dimension_difference"
        else:
            return "summary"
    
    def _determine_insight_scope(self, insight: Dict[str, Any]) -> str:
        """
        Determine the scope of an insight.
        
        Args:
            insight: Insight to determine scope for
            
        Returns:
            Insight scope
        """
        # Use the scope if already set
        if "scope" in insight:
            return insight["scope"]
        
        # Determine scope based on content
        if "key" in insight.get("details", {}):
            return "individual"
        elif "dimension" in insight.get("details", {}):
            return "dimension"
        else:
            return "global"
    
    def _determine_insight_category(self, insight: Dict[str, Any]) -> str:
        """
        Determine the category of an insight.
        
        Args:
            insight: Insight to determine category for
            
        Returns:
            Insight category
        """
        # Use the category if already set
        if "category" in insight:
            return insight["category"]
        
        # Determine category based on content
        if "is_significant" in insight.get("details", {}):
            return "anomaly"
        elif "only_in_a" in insight.get("details", {}) or "only_in_b" in insight.get("details", {}):
            return "missing_data"
        else:
            return "difference"
    
    def _calculate_insight_score(self, insight: Dict[str, Any]) -> float:
        """
        Calculate a score for an insight.
        
        Args:
            insight: Insight to calculate score for
            
        Returns:
            Insight score (0.0 to 1.0)
        """
        # Base score
        score = 0.5
        
        # Adjust score based on severity
        if insight.get("severity") == "high":
            score += 0.3
        elif insight.get("severity") == "medium":
            score += 0.1
        
        # Adjust score based on scope
        if insight.get("scope") == "global":
            score += 0.1
        elif insight.get("scope") == "dimension":
            score += 0.05
        
        # Adjust score based on type
        if insight.get("type") == "summary":
            score += 0.1
        elif insight.get("type") == "dimension_difference":
            score += 0.05
        
        # Adjust score based on business impact
        if "business_impact" in insight:
            if insight["business_impact"].get("level") == "high":
                score += 0.2
            elif insight["business_impact"].get("level") == "medium":
                score += 0.1
        
        # Ensure score is between 0.0 and 1.0
        return max(0.0, min(1.0, score))
    
    def get_insight_types(self) -> List[str]:
        """
        Get the types of insights supported by this plugin.
        
        Returns:
            List of supported insight types
        """
        return ["key_difference", "value_difference", "dimension_difference", "dimension_value_difference", "summary"]
    
    def get_insight_categories(self) -> List[str]:
        """
        Get the categories of insights supported by this plugin.
        
        Returns:
            List of supported insight categories
        """
        return ["missing_data", "new_data", "anomaly", "difference"]
    
    def get_scoring_factors(self) -> List[str]:
        """
        Get the factors used for scoring insights by this plugin.
        
        Returns:
            List of scoring factors
        """
        return ["severity", "scope", "type", "business_impact"] 