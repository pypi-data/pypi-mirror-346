#!/usr/bin/env python
"""
Script to run LlamaSee with sample forecast data files.
This script lets LlamaSee automatically detect keys, values, and dimensions.
"""

import os
import json
import pandas as pd
from llamasee import LlamaSee

def main():
    """Run LlamaSee with sample forecast data files."""
    # Define paths to the sample files
    data_dir = "/Users/gpt2s/Desktop/Projects/LlamaSee/LlamaSee/data"
    file_a = os.path.join(data_dir, "ForecastResults_run_1_cleaned.csv")
    file_b = os.path.join(data_dir, "ForecastResults_run_2_cleaned.csv")
    
    # Load the data
    print(f"Loading data from {file_a} and {file_b}...")
    df_a = pd.read_csv(file_a)
    df_b = pd.read_csv(file_b)
    
    # Try to load metadata and context from the data directory
    metadata_a_path = os.path.join(data_dir, "ForecastResults_run_1.json")
    metadata_b_path = os.path.join(data_dir, "ForecastResults_run_2.json")
    context_path = os.path.join(data_dir, "context.json")
    
    # Default metadata if files don't exist
    metadata_a = {
        'source': 'ForecastResults_run_1',
        'description': 'Forecast results from run 1',
        'timestamp': '2024-03-20'
    }
    
    metadata_b = {
        'source': 'ForecastResults_run_2',
        'description': 'Forecast results from run 2',
        'timestamp': '2024-03-20'
    }
    
    # Default context if file doesn't exist
    context = {
        'objective': 'Compare forecast datasets',
        'background': 'Comparing two different forecast runs to identify differences',
        'domain': 'forecasting'
    }
    
    # Try to load metadata and context from files if they exist
    try:
        if os.path.exists(metadata_a_path):
            with open(metadata_a_path, 'r') as f:
                metadata_a = json.load(f)
                print(f"Loaded metadata for dataset A from {metadata_a_path}")
    except Exception as e:
        print(f"Error loading metadata for dataset A: {e}")
    
    try:
        if os.path.exists(metadata_b_path):
            with open(metadata_b_path, 'r') as f:
                metadata_b = json.load(f)
                print(f"Loaded metadata for dataset B from {metadata_b_path}")
    except Exception as e:
        print(f"Error loading metadata for dataset B: {e}")
    
    try:
        if os.path.exists(context_path):
            with open(context_path, 'r') as f:
                context = json.load(f)
                print(f"Loaded context from {context_path}")
    except Exception as e:
        print(f"Error loading context: {e}")
    
    # Initialize LlamaSee
    print("Initializing LlamaSee...")
    ls = LlamaSee(
        metadata_a=metadata_a,
        data_a=df_a,
        metadata_b=metadata_b,
        data_b=df_b,
        context=context,
        verbose=True,
        log_level="DEBUG"
    )
    
    # Let LlamaSee automatically detect the structure
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