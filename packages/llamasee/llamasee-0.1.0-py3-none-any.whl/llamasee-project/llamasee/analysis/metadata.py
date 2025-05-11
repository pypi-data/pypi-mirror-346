"""
Metadata analysis functionality for LlamaSee.
"""
import json
import logging
from typing import Dict, Any, List, Optional, Union
import pandas as pd
from ..core.insight import Insight
from ..llm.enhancer import LLMInsightEnhancer

class MetadataAnalyzer:
    """
    Analyzes metadata from control files.
    
    This class provides methods for analyzing differences in metadata
    between two datasets and generating insights about those differences.
    """
    
    def __init__(self, llm_enhancer: Optional[LLMInsightEnhancer] = None):
        """
        Initialize the metadata analyzer.
        
        Args:
            llm_enhancer: Optional LLM enhancer for generating insights
        """
        self.llm_enhancer = llm_enhancer
        self.logger = logging.getLogger(__name__)
    
    def analyze_metadata_differences(self, metadata_a: Dict[str, Any], 
                                   metadata_b: Dict[str, Any], 
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze differences between two metadata dictionaries.
        
        Args:
            metadata_a: Metadata from dataset A
            metadata_b: Metadata from dataset B
            context: Additional context
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        # Find differences in metadata
        differences = self._find_differences(metadata_a, metadata_b)
        
        # If LLM enhancer is available, use it to analyze the differences
        if self.llm_enhancer and self.llm_enhancer.api_key:
            return self._analyze_with_llm(differences, metadata_a, metadata_b, context)
        
        # Otherwise, return a basic analysis
        return {
            'differences': differences,
            'summary': self._generate_basic_summary(differences)
        }
    
    def _find_differences(self, metadata_a: Dict[str, Any], 
                         metadata_b: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find differences between two metadata dictionaries.
        
        Args:
            metadata_a: Metadata from dataset A
            metadata_b: Metadata from dataset B
            
        Returns:
            List[Dict[str, Any]]: List of differences
        """
        differences = []
        
        # Get all keys from both dictionaries
        all_keys = set(metadata_a.keys()) | set(metadata_b.keys())
        
        for key in all_keys:
            # Check if key exists in both dictionaries
            if key in metadata_a and key in metadata_b:
                # Check if values are different
                if metadata_a[key] != metadata_b[key]:
                    differences.append({
                        'field': key,
                        'dataset_a_value': metadata_a[key],
                        'dataset_b_value': metadata_b[key],
                        'impact': 'Value changed',
                        'recommendation': None
                    })
            # Key exists only in dataset A
            elif key in metadata_a:
                differences.append({
                    'field': key,
                    'dataset_a_value': metadata_a[key],
                    'dataset_b_value': None,
                    'impact': 'Field removed in dataset B',
                    'recommendation': 'Consider if this field is still needed'
                })
            # Key exists only in dataset B
            else:
                differences.append({
                    'field': key,
                    'dataset_a_value': None,
                    'dataset_b_value': metadata_b[key],
                    'impact': 'Field added in dataset B',
                    'recommendation': 'Consider if this field should be added to dataset A'
                })
        
        return differences
    
    def _generate_basic_summary(self, differences: List[Dict[str, Any]]) -> str:
        """
        Generate a basic summary of differences.
        
        Args:
            differences: List of differences
            
        Returns:
            str: Basic summary
        """
        if not differences:
            return "No differences found in metadata."
        
        summary = f"Found {len(differences)} differences in metadata:\n\n"
        
        for diff in differences:
            field = diff['field']
            value_a = diff['dataset_a_value']
            value_b = diff['dataset_b_value']
            
            if value_a is None and value_b is not None:
                summary += f"- Field '{field}' was added in dataset B with value: {value_b}\n"
            elif value_a is not None and value_b is None:
                summary += f"- Field '{field}' was removed in dataset B (was: {value_a})\n"
            else:
                summary += f"- Field '{field}' changed from '{value_a}' to '{value_b}'\n"
        
        return summary
    
    def _analyze_with_llm(self, differences: List[Dict[str, Any]], 
                         metadata_a: Dict[str, Any], 
                         metadata_b: Dict[str, Any], 
                         context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze differences using LLM.
        
        Args:
            differences: List of differences
            metadata_a: Metadata from dataset A
            metadata_b: Metadata from dataset B
            context: Additional context
            
        Returns:
            Dict[str, Any]: LLM analysis results
        """
        try:
            # Prepare the prompt
            prompt = self._prepare_metadata_analysis_prompt(metadata_a, metadata_b, context)
            
            # Call the LLM
            response = self.llm_enhancer._call_llm(prompt)
            
            # Parse the response
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                self.logger.error("Failed to parse LLM response as JSON")
                return {
                    'differences': differences,
                    'summary': self._generate_basic_summary(differences),
                    'llm_response': response
                }
        except Exception as e:
            self.logger.error(f"Error analyzing with LLM: {str(e)}")
            return {
                'differences': differences,
                'summary': self._generate_basic_summary(differences),
                'error': str(e)
            }
    
    def _prepare_metadata_analysis_prompt(self, metadata_a: Dict[str, Any], 
                                        metadata_b: Dict[str, Any], 
                                        context: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepare the prompt for metadata analysis.
        
        Args:
            metadata_a: Metadata from dataset A
            metadata_b: Metadata from dataset B
            context: Additional context
            
        Returns:
            str: Prepared prompt
        """
        from ..llm.prompts import METADATA_ANALYSIS_TEMPLATE
        
        # Format metadata as JSON strings
        metadata_a_str = json.dumps(metadata_a, indent=2)
        metadata_b_str = json.dumps(metadata_b, indent=2)
        
        # Format context
        context_str = ""
        if context:
            context_str = json.dumps(context, indent=2)
        
        # Fill the template
        prompt = METADATA_ANALYSIS_TEMPLATE.format(
            metadata_a=metadata_a_str,
            metadata_b=metadata_b_str,
            context=context_str
        )
        
        return prompt
    
    def generate_metadata_insights(self, metadata_a: Dict[str, Any], 
                                 metadata_b: Dict[str, Any], 
                                 context: Optional[Dict[str, Any]] = None) -> List[Insight]:
        """
        Generate insights about metadata differences.
        
        Args:
            metadata_a: Metadata from dataset A
            metadata_b: Metadata from dataset B
            context: Additional context
            
        Returns:
            List[Insight]: Generated insights
        """
        # Analyze metadata differences
        analysis = self.analyze_metadata_differences(metadata_a, metadata_b, context)
        
        # Generate insights from the analysis
        insights = []
        
        # Add a summary insight
        summary_insight = Insight(
            id=f"metadata_summary_{len(insights)}",
            description=f"Metadata Analysis: {analysis.get('summary', 'No summary available.')}",
            importance_score=0.7,
            source_data={
                'type': 'metadata_analysis',
                'analysis': analysis
            }
        )
        summary_insight.insight_type = 'metadata'
        summary_insight.scope_level = 'global'
        insights.append(summary_insight)
        
        # Add insights for each difference
        for i, diff in enumerate(analysis.get('differences', [])):
            field = diff.get('field', 'unknown')
            impact = diff.get('impact', 'unknown')
            recommendation = diff.get('recommendation', '')
            
            description = f"Metadata Difference: Field '{field}' {impact}"
            if recommendation:
                description += f". Recommendation: {recommendation}"
            
            insight = Insight(
                id=f"metadata_diff_{i}",
                description=description,
                importance_score=0.5,
                source_data={
                    'type': 'metadata_difference',
                    'field': field,
                    'dataset_a_value': diff.get('dataset_a_value'),
                    'dataset_b_value': diff.get('dataset_b_value'),
                    'impact': impact,
                    'recommendation': recommendation
                }
            )
            insight.insight_type = 'metadata'
            insight.scope_level = 'global'
            insights.append(insight)
        
        return insights 