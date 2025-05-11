"""
Prompt templates for LLM operations in LlamaSee.
"""

# Template for enhancing insights
ENHANCE_INSIGHTS_TEMPLATE = """
You are an AI assistant helping to enhance data insights. 
For each insight, provide tags and a detailed annotation.

{context}

{insights}

For each insight, provide:
1. A list of 3-5 relevant tags
2. A detailed annotation explaining the insight and its business implications

Format your response as JSON with the following structure:
{
  "insights": [
    {
      "id": "insight_id",
      "tags": ["tag1", "tag2", "tag3"],
      "annotation": "detailed annotation"
    },
    ...
  ]
}
"""

# Template for generating insight summaries
SUMMARY_TEMPLATE = """
You are an AI assistant helping to summarize data insights. 
Create a comprehensive summary of the following insights.

{context}

{insights}

Please provide a comprehensive summary of these insights, 
highlighting the most important findings and their business implications. 
Organize the summary into sections if appropriate.
"""

# Template for analyzing metadata differences
METADATA_ANALYSIS_TEMPLATE = """
You are an AI assistant helping to analyze differences in metadata between two datasets.
Please analyze the following metadata and identify key differences and their implications.

Dataset A Metadata:
{metadata_a}

Dataset B Metadata:
{metadata_b}

Context:
{context}

Please provide a detailed analysis of the differences between these datasets, 
focusing on:
1. Key differences in configuration or parameters
2. Potential impact on the data and results
3. Recommendations for addressing any issues

Format your response as JSON with the following structure:
{
  "differences": [
    {
      "field": "field_name",
      "dataset_a_value": "value in dataset A",
      "dataset_b_value": "value in dataset B",
      "impact": "description of impact",
      "recommendation": "recommendation if applicable"
    },
    ...
  ],
  "summary": "Overall summary of differences and implications"
}
"""

# Template for generating trace explanations
TRACE_EXPLANATION_TEMPLATE = """
You are an AI assistant helping to explain data traces in LlamaSee.
Please provide an explanation for the following trace data.

Insight Description: {insight_description}

Trace Data:
{trace_data}

Context:
{context}

Please provide a clear explanation of what this trace data represents and how it relates to the insight.
Focus on:
1. What specific data points are highlighted
2. Why these data points are significant
3. How they support the insight
""" 