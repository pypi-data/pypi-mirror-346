"""
Demo script for key enrichment functionality in LlamaSee.
"""

import pandas as pd
import json
import sys
import os

# Add the parent directory to the path so we can import the llamasee package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llamasee.llamasee import LlamaSee
from llamasee.schema.key_enricher import KeyEnricher


def create_sample_data():
    """Create sample datasets for demonstration."""
    # Create sample dataset A
    data_a = pd.DataFrame({
        'store_id': [123, 456, 789, 101, 202],
        'product_id': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'sales': [100, 200, 300, 400, 500]
    })
    
    # Create sample dataset B
    data_b = pd.DataFrame({
        'store_id': [123, 456, 789, 101, 202, 303],
        'product_id': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
        'sales': [110, 210, 310, 410, 510, 600]
    })
    
    return data_a, data_b


def load_enrichment_config(file_path):
    """Load key enrichment configuration from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    """Run the key enrichment demo."""
    print("LlamaSee Key Enrichment Demo")
    print("============================")
    
    # Create sample data
    data_a, data_b = create_sample_data()
    print("\nSample Dataset A:")
    print(data_a)
    print("\nSample Dataset B:")
    print(data_b)
    
    # Load key enrichment configuration
    config_path = os.path.join(os.path.dirname(__file__), 'key_enrichment_example.json')
    enrichment_config = load_enrichment_config(config_path)
    print("\nKey Enrichment Configuration:")
    print(json.dumps(enrichment_config, indent=2))
    
    # Create LlamaSee instance
    llamasee = LlamaSee(
        metadata_a={"name": "Dataset A"},
        data_a=data_a,
        metadata_b={"name": "Dataset B"},
        data_b=data_b,
        verbose=True
    )
    
    # Run prepare stage
    print("\nRunning prepare stage...")
    llamasee.prepare()
    
    # Run fit stage with key enrichment
    print("\nRunning fit stage with key enrichment...")
    key_enrichment = {
        "store_region": enrichment_config
    }
    llamasee.fit(key_enrichment=key_enrichment)
    
    # Show the enriched datasets
    print("\nEnriched Dataset A:")
    print(llamasee.data_a)
    print("\nEnriched Dataset B:")
    print(llamasee.data_b)
    
    # Show the enrichment metadata
    print("\nEnrichment Metadata:")
    print(json.dumps(llamasee.key_enrichment_metadata, indent=2))
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main() 