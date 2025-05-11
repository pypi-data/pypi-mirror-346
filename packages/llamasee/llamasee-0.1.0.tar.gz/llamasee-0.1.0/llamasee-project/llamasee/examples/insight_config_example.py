"""
Example script demonstrating how to use the insight configuration.

This script shows how to:
1. Use the default configuration
2. Create a custom configuration
3. Compare insights with different configurations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from llamasee.llamasee import LlamaSee
from llamasee.insight_config import InsightConfig

def generate_sample_data(num_records=100):
    """Generate sample data for demonstration."""
    # Create date range
    dates = pd.date_range(start='2023-01-01', periods=num_records)
    
    # Create categories
    categories = np.random.choice(['A', 'B', 'C', 'D'], num_records)
    
    # Create values with some trends and anomalies
    base_values = np.linspace(100, 200, num_records)  # Linear trend
    noise = np.random.normal(0, 10, num_records)  # Random noise
    
    # Add some anomalies
    anomaly_indices = np.random.choice(num_records, 5, replace=False)
    for idx in anomaly_indices:
        noise[idx] += np.random.choice([-50, 50])  # Large positive or negative anomaly
    
    values = base_values + noise
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'category': categories,
        'value': values
    })
    
    return df

def create_modified_dataset(df, modification_factor=1.1):
    """Create a modified version of the dataset."""
    # Create a copy of the DataFrame
    modified_df = df.copy()
    
    # Modify values
    modified_df['value'] = df['value'] * modification_factor
    
    # Add some random changes
    random_indices = np.random.choice(len(df), 10, replace=False)
    for idx in random_indices:
        modified_df.loc[idx, 'value'] *= np.random.uniform(0.8, 1.2)
    
    return modified_df

def compare_insights(llamasee, title):
    """Generate and display insights."""
    # Generate insights
    insights = llamasee.generate_insights(top_n=5)
    
    # Print insights
    print(f"\n{title}")
    print("-" * 50)
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight.description}")
        print(f"   Type: {insight.insight_type}, Scope: {insight.scope_level}")
        print(f"   Magnitude: {insight.magnitude:.2f}, Frequency: {insight.frequency:.2f}")
        print(f"   Business Impact: {insight.business_impact:.2f}, Uniqueness: {insight.uniqueness:.2f}")
        print(f"   Weighted Score: {insight.weighted_score:.2f}")
        print()
    
    return insights

def main():
    """Main function to demonstrate insight configuration."""
    # Generate sample data
    print("Generating sample data...")
    data_a = generate_sample_data(100)
    data_b = create_modified_dataset(data_a, 1.1)
    
    # Create metadata
    metadata_a = {'source': 'original', 'description': 'Original dataset'}
    metadata_b = {'source': 'modified', 'description': 'Modified dataset'}
    
    # Create context
    context = {
        'objective': 'Compare original and modified datasets',
        'key_metrics': ['value']
    }
    
    # 1. Use default configuration
    print("\nUsing default configuration...")
    llamasee_default = LlamaSee(
        metadata_a, data_a,
        metadata_b, data_b,
        context=context
    )
    
    # Set comparison structure
    llamasee_default.set_comparison_structure(keys=['date', 'category'], values=['value'])
    
    # Generate insights with default configuration
    default_insights = compare_insights(llamasee_default, "Insights with Default Configuration")
    
    # 2. Create custom configuration that emphasizes anomalies
    print("\nCreating custom configuration that emphasizes anomalies...")
    custom_weights = {
        'magnitude': 0.4,  # Increase weight for magnitude
        'frequency': 0.1,  # Decrease weight for frequency
        'business_impact': 0.3,
        'uniqueness': 0.2
    }
    
    custom_type_adjustments = {
        'anomaly': {
            'magnitude': 0.2,  # Further increase magnitude for anomalies
            'frequency': -0.1,
            'business_impact': 0.1,  # Increase business impact for anomalies
            'uniqueness': 0.0
        }
    }
    
    custom_config = InsightConfig(
        weights=custom_weights,
        type_adjustments=custom_type_adjustments
    )
    
    # Create LlamaSee instance with custom configuration
    llamasee_custom = LlamaSee(
        metadata_a, data_a,
        metadata_b, data_b,
        context=context,
        insight_config=custom_config
    )
    
    # Set comparison structure
    llamasee_custom.set_comparison_structure(keys=['date', 'category'], values=['value'])
    
    # Generate insights with custom configuration
    custom_insights = compare_insights(llamasee_custom, "Insights with Custom Configuration (Emphasizing Anomalies)")
    
    # 3. Create custom configuration that emphasizes business impact
    print("\nCreating custom configuration that emphasizes business impact...")
    business_weights = {
        'magnitude': 0.2,
        'frequency': 0.2,
        'business_impact': 0.5,  # Increase weight for business impact
        'uniqueness': 0.1
    }
    
    business_type_adjustments = {
        'trend': {
            'magnitude': 0.0,
            'frequency': 0.0,
            'business_impact': 0.2,  # Further increase business impact for trends
            'uniqueness': -0.1
        }
    }
    
    business_config = InsightConfig(
        weights=business_weights,
        type_adjustments=business_type_adjustments
    )
    
    # Create LlamaSee instance with business-focused configuration
    llamasee_business = LlamaSee(
        metadata_a, data_a,
        metadata_b, data_b,
        context=context,
        insight_config=business_config
    )
    
    # Set comparison structure
    llamasee_business.set_comparison_structure(keys=['date', 'category'], values=['value'])
    
    # Generate insights with business-focused configuration
    business_insights = compare_insights(llamasee_business, "Insights with Business-Focused Configuration")
    
    # Compare the top insights from each configuration
    print("\nComparison of Top Insights from Different Configurations")
    print("-" * 50)
    print("Default Configuration:")
    for i, insight in enumerate(default_insights[:3], 1):
        print(f"{i}. {insight.description} (Type: {insight.insight_type}, Score: {insight.weighted_score:.2f})")
    
    print("\nAnomaly-Emphasizing Configuration:")
    for i, insight in enumerate(custom_insights[:3], 1):
        print(f"{i}. {insight.description} (Type: {insight.insight_type}, Score: {insight.weighted_score:.2f})")
    
    print("\nBusiness-Focused Configuration:")
    for i, insight in enumerate(business_insights[:3], 1):
        print(f"{i}. {insight.description} (Type: {insight.insight_type}, Score: {insight.weighted_score:.2f})")

if __name__ == "__main__":
    main() 