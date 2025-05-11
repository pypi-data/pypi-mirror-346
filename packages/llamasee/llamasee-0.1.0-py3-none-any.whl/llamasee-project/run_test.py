#!/usr/bin/env python
"""
Script to run LlamaSee with test data.
"""

import json
import pandas as pd
from llamasee import LlamaSee

def load_test_data():
    """Load test data from JSON files."""
    # Load individual comparison results
    with open('test-results/individual_comparison_results.json', 'r') as f:
        individual_results = json.load(f)
    
    # Load dimension results
    with open('test-results/dimension_results.json', 'r') as f:
        dimension_results = json.load(f)
    
    # Convert to DataFrames
    df_a = pd.DataFrame([{
        'sku': r['key']['sku'],
        'store_id': r['key']['store_id'],
        'forecast_date': r['key']['forecast_date'],
        'forecast_period': r['key']['forecast_period'],
        'forecast_value_p50': r['value_a']
    } for r in individual_results])
    
    df_b = pd.DataFrame([{
        'sku': r['key']['sku'],
        'store_id': r['key']['store_id'],
        'forecast_date': r['key']['forecast_date'],
        'forecast_period': r['key']['forecast_period'],
        'forecast_value_p50': r['value_b']
    } for r in individual_results])
    
    return df_a, df_b

def main():
    """Run LlamaSee with test data."""
    # Load test data
    print("Loading test data...")
    df_a, df_b = load_test_data()
    
    # Create metadata
    metadata_a = {
        'source': 'test_data_a',
        'description': 'Test dataset A',
        'timestamp': '2024-03-20'
    }
    
    metadata_b = {
        'source': 'test_data_b',
        'description': 'Test dataset B',
        'timestamp': '2024-03-20'
    }
    
    # Create context
    context = {
        'objective': 'Compare forecast datasets',
        'background': 'Testing LlamaSee functionality with forecast data',
        'domain': 'forecasting'
    }
    
    # Initialize LlamaSee
    print("Initializing LlamaSee...")
    ls = LlamaSee(
        metadata_a=metadata_a,
        data_a=df_a,
        metadata_b=metadata_b,
        data_b=df_b,
        context=context,
        verbose=True
    )
    
    # Define keys and values
    keys = ['sku', 'store_id', 'forecast_date', 'forecast_period']
    values = ['forecast_value_p50']
    
    # Set comparison structure
    print("Setting comparison structure...")
    ls.set_comparison_structure(keys=keys, values=values)
    
    # Set dimensions
    print("Setting dimensions...")
    ls.set_dimensions({
        'time': ['forecast_date', 'forecast_period'],
        'location': ['store_id'],
        'product': ['sku']
    })
    
    # Run full lifecycle
    print("Running LlamaSee lifecycle...")
    ls.prepare()
    ls.fit()
    ls.compare()
    
    # Generate insights
    print("Generating insights...")
    insights = ls.generate_insights()
    
    # Print insights
    print("\nGenerated Insights:")
    for i, insight in enumerate(insights, 1):
        print(f"\nInsight {i}:")
        print(f"Description: {insight.description}")
        print(f"Type: {insight.type}")
        print(f"Scope: {insight.scope}")
        print(f"Importance Score: {insight.importance_score}")
        print(f"Source Data: {insight.source_data}")

if __name__ == '__main__':
    main() 