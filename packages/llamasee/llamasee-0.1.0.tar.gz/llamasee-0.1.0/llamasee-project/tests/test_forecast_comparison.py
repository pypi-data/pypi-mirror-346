"""
Test script for the forecasting comparison scenario.

This script demonstrates how to use LlamaSee to compare two forecasting runs
and generate meaningful insights.
"""

import os
import sys
import json
import pandas as pd
import time
from pathlib import Path

# Add the parent directory to the path so we can import LlamaSee
sys.path.append(str(Path(__file__).parent.parent))

from llamasee.utils import get_logger
from llamasee.config.insight_config import InsightConfig
from llamasee.config.storage_config import CSVStorageConfig
from llamasee.config.llm_config import LLMConfig
from llamasee.config.analysis_config import AnalysisConfig
from llamasee.llm.adapters import LLMAdapterFactory

# Set up logger
logger = get_logger("test_forecast_comparison")

def load_forecast_data(run_id):
    """
    Load forecast data for a specific run.
    
    Args:
        run_id: The run ID (1 or 2)
        
    Returns:
        Tuple of (forecast_results, forecast_control)
    """
    data_dir = Path(__file__).parent.parent.parent / "data"
    
    # Load forecast results
    results_file = data_dir / f"ForecastResults_run_{run_id}.csv"
    forecast_results = pd.read_csv(results_file)
    
    # Load forecast control
    control_file = data_dir / f"ForecastControl_run_{run_id}.json"
    with open(control_file, 'r') as f:
        forecast_control = json.load(f)
    
    return forecast_results, forecast_control

def compare_forecasts(forecast1, control1, forecast2, control2):
    """
    Compare two forecasting runs.
    
    Args:
        forecast1: DataFrame of forecast results for run 1
        control1: Dictionary of control parameters for run 1
        forecast2: DataFrame of forecast results for run 2
        control2: Dictionary of control parameters for run 2
        
    Returns:
        Dictionary of comparison results
    """
    # Calculate differences between forecasts
    merged = pd.merge(
        forecast1, 
        forecast2, 
        on=['sku', 'store_id', 'forecast_date', 'forecast_period'],
        suffixes=('_run1', '_run2')
    )
    
    # Calculate absolute and percentage differences
    merged['p50_diff'] = merged['forecast_value_p50_run2'] - merged['forecast_value_p50_run1']
    merged['p50_pct_diff'] = (merged['p50_diff'] / merged['forecast_value_p50_run1']) * 100
    
    # Identify significant differences (e.g., > 10% change)
    significant_diff = merged[abs(merged['p50_pct_diff']) > 10]
    
    # Group by SKU and store to identify patterns
    sku_store_summary = merged.groupby(['sku', 'store_id']).agg({
        'p50_diff': ['mean', 'std', 'min', 'max'],
        'p50_pct_diff': ['mean', 'std', 'min', 'max']
    }).reset_index()
    
    # Identify SKUs with the largest changes
    top_changes = sku_store_summary.sort_values(('p50_pct_diff', 'mean'), ascending=False).head(10)
    
    # Compare control parameters
    control_diff = {}
    for key in control1:
        if key in control2 and control1[key] != control2[key]:
            control_diff[key] = {
                'run1': control1[key],
                'run2': control2[key]
            }
    
    return {
        'merged_data': merged,
        'significant_diff': significant_diff,
        'sku_store_summary': sku_store_summary,
        'top_changes': top_changes,
        'control_diff': control_diff
    }

def generate_insights(comparison_results, llm_adapter):
    """
    Generate insights from comparison results using LLM.
    
    Args:
        comparison_results: Dictionary of comparison results
        llm_adapter: LLM adapter instance
        
    Returns:
        Dictionary of generated insights
    """
    # Prepare data for LLM
    top_changes = comparison_results['top_changes']
    control_diff = comparison_results['control_diff']
    
    # Create a summary of the top changes
    top_changes_summary = []
    for _, row in top_changes.iterrows():
        sku = row['sku']
        store = row['store_id']
        mean_pct_diff = row[('p50_pct_diff', 'mean')]
        top_changes_summary.append(f"SKU {sku} at {store}: {mean_pct_diff:.2f}% change")
    
    # Create a summary of control differences
    control_diff_summary = []
    for key, value in control_diff.items():
        control_diff_summary.append(f"{key}: {value['run1']} → {value['run2']}")
    
    # Create prompt for LLM
    prompt = f"""
    You are a data analyst for a retail company. I need you to analyze the differences between two forecasting runs and provide insights.
    
    Top changes in forecast values:
    {chr(10).join(top_changes_summary)}
    
    Differences in control parameters:
    {chr(10).join(control_diff_summary)}
    
    Please provide:
    1. A summary of the key differences between the two forecasting runs
    2. Potential reasons for these differences
    3. Implications for inventory planning and business operations
    4. Recommendations for addressing any issues identified
    """
    
    # Generate insights using LLM
    start_time = time.time()
    response = llm_adapter.generate_completion(prompt)
    duration = time.time() - start_time
    
    # Log the LLM request
    from llamasee.utils import logger
    logger.log_llm_request(
        provider=llm_adapter.__class__.__name__,
        model=llm_adapter.model_name,
        prompt=prompt,
        response=response,
        duration=duration
    )
    
    return {
        'raw_insight': response,
        'duration': duration
    }

def main():
    """Main function to run the test."""
    logger.info("Starting forecast comparison test")
    
    # Load forecast data
    logger.info("Loading forecast data")
    forecast1, control1 = load_forecast_data(1)
    forecast2, control2 = load_forecast_data(2)
    
    # Compare forecasts
    logger.info("Comparing forecasts")
    comparison_results = compare_forecasts(forecast1, control1, forecast2, control2)
    
    # Initialize LLM adapter
    logger.info("Initializing LLM adapter")
    llm_config = LLMConfig()
    llm_adapter = LLMAdapterFactory.create_adapter("openai", llm_config.get_config())
    
    # Generate insights
    logger.info("Generating insights")
    insights = generate_insights(comparison_results, llm_adapter)
    
    # Print insights
    print("\n" + "="*80)
    print("FORECAST COMPARISON INSIGHTS")
    print("="*80)
    print(insights['raw_insight'])
    print("="*80)
    print(f"Insight generation took {insights['duration']:.2f} seconds")
    
    logger.info("Forecast comparison test completed")

if __name__ == "__main__":
    main() 