import argparse
import logging
from typing import Dict, Any
import pandas as pd
from .llamasee import LlamaSee
from .data_loader import DataLoader

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_example_data() -> tuple[Dict[str, Any], pd.DataFrame, Dict[str, Any], pd.DataFrame]:
    """Load example data for testing"""
    # Create sample data
    data_a = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'value': range(10),
        'category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    })
    data_b = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'value': range(5, 15),
        'category': ['A', 'B', 'C', 'D', 'E', 'K', 'L', 'M', 'N', 'O']
    })
    
    metadata_a = {
        'source': 'example_a',
        'format': 'dataframe',
        'rows': len(data_a),
        'columns': list(data_a.columns)
    }
    
    metadata_b = {
        'source': 'example_b',
        'format': 'dataframe',
        'rows': len(data_b),
        'columns': list(data_b.columns)
    }
    
    return metadata_a, data_a, metadata_b, data_b

def print_scope_analysis(scope: Dict[str, Any]):
    """Print scope analysis results in a readable format"""
    print("\n=== SCOPE ANALYSIS ===")
    
    # Print column overlap
    print("\nColumn Overlap:")
    print(f"  Common columns: {len(scope['common_columns'])} / {len(scope['common_columns']) + len(scope['unique_to_a']) + len(scope['unique_to_b'])} ({scope['overlap_percentage']:.1f}%)")
    if scope['unique_to_a']:
        print(f"  Unique to dataset A: {', '.join(scope['unique_to_a'])}")
    if scope['unique_to_b']:
        print(f"  Unique to dataset B: {', '.join(scope['unique_to_b'])}")
    
    # Print dimension overlap
    if scope['overlap']:
        print("\nDimension Overlap:")
        for dimension, info in scope['overlap'].items():
            print(f"  {dimension}:")
            print(f"    Common values: {info['total_common']} / {max(info['total_a'], info['total_b'])} ({info['overlap_percentage']:.1f}%)")
            if info['unique_to_a']:
                print(f"    Unique to dataset A: {', '.join(map(str, info['unique_to_a'][:5]))}{'...' if len(info['unique_to_a']) > 5 else ''}")
            if info['unique_to_b']:
                print(f"    Unique to dataset B: {', '.join(map(str, info['unique_to_b'][:5]))}{'...' if len(info['unique_to_b']) > 5 else ''}")

def main():
    parser = argparse.ArgumentParser(description="LlamaSee: Data Comparison CLI")
    parser.add_argument("--compare", action="store_true", help="Run a sample comparison")
    parser.add_argument("--analyze", action="store_true", help="Analyze data scope and overlap")
    parser.add_argument("--file-a", type=str, help="Path to first data file")
    parser.add_argument("--file-b", type=str, help="Path to second data file")
    parser.add_argument("--format", choices=['csv', 'parquet'], default='csv', help="Input file format")
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    if args.compare or args.analyze:
        if args.file_a and args.file_b:
            # Load data from files
            loader = DataLoader()
            if args.format == 'csv':
                meta_a, data_a, meta_b, data_b = loader.from_csv(args.file_a, args.file_b)
            else:
                meta_a, data_a, meta_b, data_b = loader.from_parquet(args.file_a, args.file_b)
        else:
            # Use example data
            logger.info("Using example data...")
            meta_a, data_a, meta_b, data_b = load_example_data()

        # Initialize LlamaSee
        context = {
            'objective': 'Compare sample datasets',
            'background': 'Testing LlamaSee functionality',
            'domain': 'example'
        }
        
        ls = LlamaSee(meta_a, data_a, meta_b, data_b, context=context)
        
        # Analyze scope
        if args.analyze:
            scope = ls.analyze_scope()
            print_scope_analysis(scope)
            return
        
        # Set dimensions
        ls.set_dimensions(
            dimensions=['time', 'category'],
            aggregation_levels={'time': 'day'}
        )
        
        # Run comparison
        ls.prepare()
        result = ls.compare()
        
        # Generate insights
        insights = ls.generate_insights(top_n=5)
        
        # Print results
        print("\nComparison Result:")
        print(result)
        
        print("\nInsights:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight.description}")
            
        # Generate summary
        summary = ls.generate_insight_summary()
        print("\nSummary:")
        print(summary)

if __name__ == "__main__":
    main() 