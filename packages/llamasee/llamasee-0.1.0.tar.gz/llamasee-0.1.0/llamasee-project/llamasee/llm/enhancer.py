"""
LLM integration for enhancing insights in LlamaSee.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
import openai
from ..core.insight import Insight

class LLMInsightEnhancer:
    """
    Enhances insights using LLM capabilities.
    
    This class provides methods to enhance insights with LLM-generated content,
    such as tags, annotations, and summaries.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM insight enhancer.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
            model: Model to use for LLM operations.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logging.warning("No OpenAI API key provided. LLM features will be disabled.")
        
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def enhance_insights(self, insights: List[Insight], context: Optional[Dict[str, Any]] = None) -> List[Insight]:
        """
        Enhance a list of insights with LLM-generated content.
        
        Args:
            insights: List of insights to enhance
            context: Additional context for the LLM
            
        Returns:
            List[Insight]: Enhanced insights
        """
        if not self.api_key:
            self.logger.warning("Cannot enhance insights: No API key available")
            return insights
        
        try:
            # Process insights in batches to avoid token limits
            batch_size = 5
            for i in range(0, len(insights), batch_size):
                batch = insights[i:i+batch_size]
                self._enhance_batch(batch, context)
            
            return insights
        except Exception as e:
            self.logger.error(f"Error enhancing insights: {str(e)}")
            return insights
    
    def _enhance_batch(self, insights: List[Insight], context: Optional[Dict[str, Any]] = None):
        """
        Enhance a batch of insights.
        
        Args:
            insights: Batch of insights to enhance
            context: Additional context for the LLM
        """
        # Prepare the prompt
        prompt = self._prepare_enhancement_prompt(insights, context)
        
        # Call the LLM
        response = self._call_llm(prompt)
        
        # Parse the response and update insights
        self._parse_enhancement_response(response, insights)
    
    def _prepare_enhancement_prompt(self, insights: List[Insight], context: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepare the prompt for enhancing insights.
        
        Args:
            insights: Insights to enhance
            context: Additional context
            
        Returns:
            str: Prepared prompt
        """
        prompt = "You are an AI assistant helping to enhance data insights. "
        prompt += "For each insight, provide tags and a detailed annotation.\n\n"
        
        if context:
            prompt += f"Context: {json.dumps(context)}\n\n"
        
        for i, insight in enumerate(insights):
            prompt += f"Insight {i+1}:\n"
            prompt += f"Description: {insight.description}\n"
            prompt += f"Type: {insight.insight_type or 'unknown'}\n"
            prompt += f"Scope: {insight.scope_level or 'unknown'}\n"
            prompt += f"Importance: {insight.importance_score}\n"
            
            if insight.source_data:
                prompt += f"Source Data: {json.dumps(insight.source_data)}\n"
            
            prompt += "\n"
        
        prompt += "For each insight, provide:\n"
        prompt += "1. A list of 3-5 relevant tags\n"
        prompt += "2. A detailed annotation explaining the insight and its business implications\n\n"
        prompt += "Format your response as JSON with the following structure:\n"
        prompt += "{\n"
        prompt += "  \"insights\": [\n"
        prompt += "    {\n"
        prompt += "      \"id\": \"insight_id\",\n"
        prompt += "      \"tags\": [\"tag1\", \"tag2\", \"tag3\"],\n"
        prompt += "      \"annotation\": \"detailed annotation\"\n"
        prompt += "    },\n"
        prompt += "    ...\n"
        prompt += "  ]\n"
        prompt += "}\n"
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the given prompt.
        
        Args:
            prompt: Prompt to send to the LLM
            
        Returns:
            str: LLM response
        """
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error calling LLM: {str(e)}")
            return "{}"
    
    def _parse_enhancement_response(self, response: str, insights: List[Insight]):
        """
        Parse the LLM response and update insights.
        
        Args:
            response: LLM response
            insights: Insights to update
        """
        try:
            # Try to parse the response as JSON
            data = json.loads(response)
            
            # Update insights with the parsed data
            for insight_data in data.get("insights", []):
                insight_id = insight_data.get("id")
                
                # Find the matching insight
                for insight in insights:
                    if insight.id == insight_id:
                        # Update tags
                        if "tags" in insight_data:
                            insight.llm_tags = insight_data["tags"]
                        
                        # Update annotation
                        if "annotation" in insight_data:
                            insight.llm_annotation = insight_data["annotation"]
                        
                        break
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
    
    def generate_insight_summary(self, insights: List[Insight], context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a summary of insights using LLM.
        
        Args:
            insights: Insights to summarize
            context: Additional context
            
        Returns:
            str: Generated summary
        """
        if not self.api_key:
            self.logger.warning("Cannot generate summary: No API key available")
            return "LLM features are disabled. No API key available."
        
        try:
            # Prepare the prompt
            prompt = self._prepare_summary_prompt(insights, context)
            
            # Call the LLM
            response = self._call_llm(prompt)
            
            return response
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def _prepare_summary_prompt(self, insights: List[Insight], context: Optional[Dict[str, Any]] = None) -> str:
        """
        Prepare the prompt for generating a summary.
        
        Args:
            insights: Insights to summarize
            context: Additional context
            
        Returns:
            str: Prepared prompt
        """
        prompt = "You are an AI assistant helping to summarize data insights. "
        prompt += "Create a comprehensive summary of the following insights.\n\n"
        
        if context:
            prompt += f"Context: {json.dumps(context)}\n\n"
        
        for i, insight in enumerate(insights):
            prompt += f"Insight {i+1}:\n"
            prompt += f"Description: {insight.description}\n"
            prompt += f"Type: {insight.insight_type or 'unknown'}\n"
            prompt += f"Scope: {insight.scope_level or 'unknown'}\n"
            prompt += f"Importance: {insight.importance_score}\n"
            
            if insight.llm_annotation:
                prompt += f"Annotation: {insight.llm_annotation}\n"
            
            prompt += "\n"
        
        prompt += "Please provide a comprehensive summary of these insights, "
        prompt += "highlighting the most important findings and their business implications. "
        prompt += "Organize the summary into sections if appropriate."
        
        return prompt 