#!/usr/bin/env python3
"""
Script to export stage data from LlamaSee stages.

This script provides functionality to export stage data from LlamaSee stages
to various formats (JSON, CSV, text) for offline analysis.
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

def export_stage_checkpoint(checkpoint: Dict[str, Any], output_dir: str, stage_name: str, checkpoint_name: str) -> Dict[str, str]:
    """
    Export a stage checkpoint to various formats.
    
    Args:
        checkpoint: The checkpoint data to export
        output_dir: Directory to save the exports
        stage_name: Name of the stage
        checkpoint_name: Name of the checkpoint
        
    Returns:
        Dictionary with paths to exported files
    """
    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{stage_name}_{checkpoint_name}_{timestamp}"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Export paths
    export_paths = {}
    
    # Export as JSON
    json_path = os.path.join(output_dir, f"{base_filename}.json")
    with open(json_path, 'w') as f:
        json.dump(checkpoint, f, indent=2)
    export_paths['json'] = json_path
    
    # Export as text
    text_path = os.path.join(output_dir, f"{base_filename}.txt")
    with open(text_path, 'w') as f:
        f.write(f"=== {stage_name.upper()} STAGE CHECKPOINT: {checkpoint_name} ===\n")
        f.write(f"Timestamp: {checkpoint.get('timestamp', 'N/A')}\n\n")
        
        if 'data' in checkpoint:
            f.write("=== DATA ===\n")
            for key, value in checkpoint['data'].items():
                if isinstance(value, (list, dict)):
                    f.write(f"\n{key}:\n{json.dumps(value, indent=2)}\n")
                else:
                    f.write(f"{key}: {value}\n")
    
    export_paths['text'] = text_path
    
    # If data is tabular, export as CSV
    if 'data' in checkpoint and isinstance(checkpoint['data'], dict):
        try:
            df = pd.DataFrame(checkpoint['data'])
            csv_path = os.path.join(output_dir, f"{base_filename}.csv")
            df.to_csv(csv_path, index=False)
            export_paths['csv'] = csv_path
        except:
            pass
    
    return export_paths

def export_stage_data(stage_logger, output_dir: str, stage_name: str) -> Dict[str, Dict[str, str]]:
    """
    Export all checkpoints from a stage logger.
    
    Args:
        stage_logger: The stage logger containing checkpoints
        output_dir: Directory to save the exports
        stage_name: Name of the stage
        
    Returns:
        Dictionary mapping checkpoint names to their export paths
    """
    export_paths = {}
    
    for checkpoint_name, checkpoint in stage_logger.checkpoints.items():
        export_paths[checkpoint_name] = export_stage_checkpoint(
            checkpoint=checkpoint,
            output_dir=output_dir,
            stage_name=stage_name,
            checkpoint_name=checkpoint_name
        )
    
    return export_paths

def export_all_stages(llamasee_instance, output_dir: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Export data from all stages in a LlamaSee instance.
    
    Args:
        llamasee_instance: The LlamaSee instance
        output_dir: Directory to save the exports
        
    Returns:
        Dictionary mapping stage names to their checkpoint export paths
    """
    all_exports = {}
    
    for stage_name, stage_logger in llamasee_instance.stages.items():
        stage_dir = os.path.join(output_dir, stage_name)
        all_exports[stage_name] = export_stage_data(
            stage_logger=stage_logger,
            output_dir=stage_dir,
            stage_name=stage_name
        )
    
    return all_exports

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Export LlamaSee stage data")
    parser.add_argument("--output-dir", default="stage_exports",
                      help="Directory to save exports (default: stage_exports)")
    parser.add_argument("--stage", help="Specific stage to export (optional)")
    parser.add_argument("--checkpoint", help="Specific checkpoint to export (optional)")
    
    args = parser.parse_args()
    
    # Example usage:
    # python export_stage_data.py --output-dir ./exports --stage prepare --checkpoint key_value_detection 