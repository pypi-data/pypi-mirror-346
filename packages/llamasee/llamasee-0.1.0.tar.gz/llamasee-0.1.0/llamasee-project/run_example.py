#!/usr/bin/env python
"""
Script to run the LlamaSee insight configuration example.
"""

import sys
import os

def run_example():
    """Run the insight configuration example."""
    # Add the parent directory to the path so we can import the package
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Import and run the example
    from examples.insight_config_example import main
    main()

if __name__ == '__main__':
    run_example() 