"""
Exporters for LlamaSee.

This module provides classes for exporting different types of data from LlamaSee
in various formats.
"""

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import logging
import traceback
import os

class Exporter:
    """Base class for exporters."""
    
    def __init__(self, llamasee):
        """
        Initialize the exporter.
        
        Args:
            llamasee: The LlamaSee instance to export data from.
        """
        self.llamasee = llamasee
        self.logger = llamasee.logger
        self.logger.debug(f"Initialized {self.__class__.__name__} exporter")
    
    def export(self, path: str, format: str = 'csv') -> Dict[str, Any]:
        """
        Export data to the specified path in the specified format.
        
        Args:
            path: Path to export the data to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        raise NotImplementedError("Subclasses must implement export method")


class ResultsExporter(Exporter):
    """Exporter for comparison results."""
    
    def export(self, path: str, format: str = 'csv') -> Dict[str, Any]:
        """
        Export comparison results to the specified path in the specified format.
        
        Args:
            path: Path to export the comparison results to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        self.logger.debug(f"Starting export of comparison results to {path} in {format} format")
        try:
            # Determine if path is a directory or a filename
            if os.path.isdir(path):
                self.logger.debug(f"Output path is a directory: {path}")
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = os.path.join(path, f"comparison_results_{timestamp}.{format}")
            else:
                self.logger.debug(f"Output path is a filename: {path}")
                file_name = path
            
            # Get comparison results in canonical format
            comparison_results_dict = None
            if hasattr(self.llamasee, '_comparison_result') and self.llamasee._comparison_result is not None:
                # Use the ComparisonResult object directly
                self.logger.debug("Using ComparisonResult object for export")
                comparison_results_dict = self.llamasee._comparison_result.to_dataframe().to_dict(orient='records')
                
                # Get summary statistics
                summary_stats = self.llamasee._comparison_result.get_summary_stats()
                
                # Get dimension statistics if available
                dimension_stats = None
                if hasattr(self.llamasee, 'dimensions') and self.llamasee.dimensions:
                    dimension_stats = self.llamasee._comparison_result.get_dimension_stats()
            elif self.llamasee._comparison_results is not None:
                # Fallback to the old format if ComparisonResult is not available
                self.logger.debug("Using legacy _comparison_results for export")
                comparison_results_dict = self.llamasee._comparison_results.to_dict(orient='records')
                summary_stats = None
                dimension_stats = None
            else:
                self.logger.debug("No comparison results found for export")
            
            # Prepare export data
            export_data = {
                'metadata': {
                    'source_a': self.llamasee.metadata_a,
                    'source_b': self.llamasee.metadata_b,
                    'context': self.llamasee.context,
                    'timestamp': datetime.now().isoformat()
                },
                'comparison_results': comparison_results_dict,
                'summary_statistics': summary_stats,
                'dimension_statistics': dimension_stats,
                'insights': [insight.to_dict() for insight in self.llamasee._insights]
            }
            
            # Export based on format
            if format.lower() == 'json':
                self.logger.debug(f"Exporting to JSON format: {file_name}")
                with open(file_name, 'w') as f:
                    json.dump(export_data, f, indent=2)
            elif format.lower() == 'csv':
                # For CSV, we'll export the comparison results as a DataFrame
                if comparison_results_dict:
                    self.logger.debug(f"Exporting to CSV format: {file_name}")
                    df = pd.DataFrame(comparison_results_dict)
                    df.to_csv(file_name, index=False)
                else:
                    self.logger.warning("No comparison results to export to CSV")
                    return {"error": "No comparison results to export to CSV"}
            elif format.lower() == 'text':
                self.logger.debug(f"Exporting to TEXT format: {file_name}")
                with open(file_name, 'w') as f:
                    f.write("=== COMPARISON RESULTS ===\n\n")
                    
                    # Write metadata
                    f.write("Metadata:\n")
                    f.write(f"Source A: {json.dumps(export_data['metadata']['source_a'], indent=2)}\n")
                    f.write(f"Source B: {json.dumps(export_data['metadata']['source_b'], indent=2)}\n")
                    f.write(f"Context: {json.dumps(export_data['metadata']['context'], indent=2)}\n")
                    f.write(f"Timestamp: {export_data['metadata']['timestamp']}\n\n")
                    
                    # Write summary statistics
                    if summary_stats:
                        f.write("Summary Statistics:\n")
                        for key, value in summary_stats.items():
                            if value is not None:
                                f.write(f"  - {key}: {value}\n")
                        f.write("\n")
                    
                    # Write dimension statistics
                    if dimension_stats:
                        f.write("Dimension Statistics:\n")
                        for dim, stats in dimension_stats.items():
                            f.write(f"  - Dimension '{dim}':\n")
                            for key, value in stats.items():
                                if value is not None:
                                    f.write(f"    - {key}: {value}\n")
                        f.write("\n")
                    
                    # Write insights
                    if self.llamasee._insights:
                        f.write("Insights:\n")
                        for i, insight in enumerate(self.llamasee._insights):
                            f.write(f"  {i+1}. {insight.to_dict()}\n")
            else:
                self.logger.error(f"Unsupported format: {format}")
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Exported comparison results to {file_name}")
            self.logger.debug(f"Export completed successfully: {file_name}")
            return {"path": file_name, "format": format}
            
        except Exception as e:
            self.logger.error(f"Error exporting comparison results: {str(e)}")
            self.logger.debug(f"Export failed with error: {traceback.format_exc()}")
            return {"error": str(e)}


class DimensionResultsExporter(Exporter):
    """Exporter for dimension comparison results."""
    
    def export(self, path: str, format: str = 'json') -> Dict[str, Any]:
        """
        Export dimension comparison results to the specified path in the specified format.
        
        Args:
            path: Path to export the dimension results to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        self.logger.debug(f"Starting export of dimension results to {path} in {format} format")
        try:
            # Determine if path is a directory or a filename
            if os.path.isdir(path):
                self.logger.debug(f"Output path is a directory: {path}")
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = os.path.join(path, f"dimension_results_{timestamp}.{format}")
            else:
                self.logger.debug(f"Output path is a filename: {path}")
                file_name = path
            
            # Get dimension comparison results
            self.logger.debug("Retrieving dimension comparison results")
            dimension_results = self.llamasee.get_dimension_comparison_results()
            
            if not dimension_results:
                self.logger.warning("No dimension comparison results available to export")
                return {"error": "No dimension comparison results available"}
            
            self.logger.info(f"Exporting dimension results in {format} format to {file_name}")
            
            # Export based on format
            if format == 'json':
                self.logger.debug(f"Exporting to JSON format: {file_name}")
                with open(file_name, 'w') as f:
                    json.dump(dimension_results, f, indent=2)
                
                self.logger.debug(f"Export completed successfully: {file_name}")
                return {"path": file_name, "format": "json"}
                
            elif format == 'csv':
                self.logger.debug(f"Exporting to CSV format: {file_name}")
                # Create a CSV with dimension results
                with open(file_name, 'w', newline='') as f:
                    writer = csv.writer(f)
                    
                    # Write header
                    writer.writerow(['dimension', 'value', 'metric', 'value_type', 'value'])
                    
                    # Write data
                    for dimension, values in dimension_results.items():
                        for value, metrics in values.items():
                            for metric, data in metrics.items():
                                for value_type, value_data in data.items():
                                    writer.writerow([dimension, value, metric, value_type, value_data])
                
                self.logger.debug(f"Export completed successfully: {file_name}")
                return {"path": file_name, "format": "csv"}
                
            elif format == 'text':
                self.logger.debug(f"Exporting to TEXT format: {file_name}")
                with open(file_name, 'w') as f:
                    f.write("=== DIMENSION COMPARISON RESULTS ===\n\n")
                    
                    for dimension, values in dimension_results.items():
                        f.write(f"Dimension: {dimension}\n")
                        for value, metrics in values.items():
                            f.write(f"  Value: {value}\n")
                            for metric, data in metrics.items():
                                f.write(f"    Metric: {metric}\n")
                                for value_type, value_data in data.items():
                                    f.write(f"      {value_type}: {value_data}\n")
                        f.write("\n")
                
                self.logger.debug(f"Export completed successfully: {file_name}")
                return {"path": file_name, "format": "text"}
            
            else:
                self.logger.error(f"Unsupported format: {format}")
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            self.logger.error(f"Error exporting dimension results: {str(e)}")
            self.logger.debug(f"Export failed with error: {traceback.format_exc()}")
            return {"error": str(e)}


class FitResultsExporter(Exporter):
    """Exporter for fit results."""
    
    def export(self, path: Optional[str] = None, format: str = 'json') -> Dict[str, Any]:
        """
        Export fit results to the specified path in the specified format.
        
        Args:
            path: Path to export the fit results to.
            format: Format to export in ('csv', 'json', 'text').
            
        Returns:
            Dictionary containing export information.
        """
        self.logger.debug(f"Starting export of fit results to {path} in {format} format")
        try:
            # Get the comparison structure checkpoint
            self.logger.debug("Retrieving comparison structure checkpoint")
            comparison_structure = self.llamasee.stage_manager.get_stage("fit").get_checkpoint("comparison_structure")
            if not comparison_structure:
                self.logger.warning("Comparison structure checkpoint not found. Cannot export results.")
                return {"error": "Comparison structure checkpoint not found"}
            
            # Get the overlap meta checkpoint
            self.logger.debug("Retrieving overlap meta checkpoint")
            overlap_meta = self.llamasee.stage_manager.get_stage("fit").get_checkpoint("overlap_meta")
            if not overlap_meta:
                self.logger.warning("Overlap meta checkpoint not found. Cannot export results.")
                return {"error": "Overlap meta checkpoint not found"}
            
            # Prepare data for export
            export_data = {
                "comparison_structure": comparison_structure["data"],
                "overlap_meta": overlap_meta["data"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Generate default path if not provided
            if path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"fit_results_{timestamp}.{format}"
                self.logger.debug(f"Generated default path: {file_name}")
            else:
                # Determine if path is a directory or a filename
                if os.path.isdir(path):
                    self.logger.debug(f"Output path is a directory: {path}")
                    # Generate a filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = os.path.join(path, f"fit_results_{timestamp}.{format}")
                else:
                    self.logger.debug(f"Output path is a filename: {path}")
                    file_name = path
            
            # Export data based on format
            if format.lower() == 'json':
                self.logger.debug(f"Exporting to JSON format: {file_name}")
                with open(file_name, 'w') as f:
                    json.dump(export_data, f, indent=2)
            elif format.lower() == 'csv':
                self.logger.debug(f"Exporting to CSV format: {file_name}")
                # For CSV, we'll export the overlap meta as a DataFrame
                df = pd.DataFrame([overlap_meta["data"]])
                df.to_csv(file_name, index=False)
            elif format.lower() == 'text':
                self.logger.debug(f"Exporting to TEXT format: {file_name}")
                with open(file_name, 'w') as f:
                    f.write("=== FIT RESULTS ===\n\n")
                    f.write("Comparison Structure:\n")
                    f.write(f"Keys: {', '.join(export_data['comparison_structure']['keys'])}\n")
                    f.write(f"Values: {', '.join(export_data['comparison_structure']['values'])}\n")
                    f.write(f"Dimensions: {json.dumps(export_data['comparison_structure']['dimensions'], indent=2)}\n\n")
                    f.write("Overlap Meta:\n")
                    f.write(f"Original Counts: A={export_data['overlap_meta']['original_counts']['dataset_a']}, B={export_data['overlap_meta']['original_counts']['dataset_b']}\n")
                    f.write(f"Overlap Count: {export_data['overlap_meta']['overlap_count']}\n")
                    f.write(f"Removed Counts: A={export_data['overlap_meta']['removed_counts']['dataset_a']}, B={export_data['overlap_meta']['removed_counts']['dataset_b']}\n")
                    f.write(f"Overlap Percentage: A={export_data['overlap_meta']['overlap_percentage']['dataset_a']:.2f}%, B={export_data['overlap_meta']['overlap_percentage']['dataset_b']:.2f}%\n")
            else:
                self.logger.error(f"Unsupported format: {format}")
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Exported fit results to {file_name}")
            self.logger.debug(f"Export completed successfully: {file_name}")
            return {"path": file_name, "format": format}
            
        except Exception as e:
            self.logger.error(f"Error exporting fit results: {str(e)}")
            self.logger.debug(f"Export failed with error: {traceback.format_exc()}")
            return {"error": str(e)}


class DimensionComparisonResultsExporter(Exporter):
    """Exporter for dimension comparison results."""
    
    def export(self, output_path: str, format: str = "json") -> Dict[str, Any]:
        """
        Export dimension comparison results to a file.
        
        Args:
            output_path: Path to export the dimension comparison results to.
            format: Format to export in ('json', 'csv').
            
        Returns:
            Dictionary containing export information.
        """
        self.logger.debug(f"Starting export of dimension comparison results to {output_path} in {format} format")
        try:
            # Determine if output_path is a directory or a filename
            if os.path.isdir(output_path):
                self.logger.debug(f"Output path is a directory: {output_path}")
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = os.path.join(output_path, f"dimension_comparison_results_{timestamp}.{format}")
            else:
                self.logger.debug(f"Output path is a filename: {output_path}")
                file_name = output_path
            
            # Get dimension comparison results
            self.logger.debug("Generating dimension comparison results")
            dimension_comparison_results = self.llamasee._generate_dimension_comparison_results()
            
            if not dimension_comparison_results:
                self.logger.warning("No dimension comparison results available to export")
                return {"error": "No dimension comparison results available"}
            
            self.logger.info(f"Exporting dimension comparison results in {format} format to {file_name}")
            
            # Export based on format
            if format.lower() == 'json':
                self.logger.debug(f"Exporting to JSON format: {file_name}")
                with open(file_name, 'w') as f:
                    json.dump(dimension_comparison_results, f, indent=2)
            elif format.lower() == 'csv':
                # For CSV, we'll export each dimension as a separate file
                self.logger.debug(f"Exporting to CSV format: {file_name}")
                base_path = os.path.splitext(file_name)[0]
                
                for dimension, results in dimension_comparison_results.items():
                    dimension_path = f"{base_path}_{dimension}.csv"
                    self.logger.debug(f"Exporting dimension {dimension} to {dimension_path}")
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(results)
                    df.to_csv(dimension_path, index=False)
                    
                    self.logger.info(f"Exported dimension {dimension} to {dimension_path}")
            else:
                self.logger.error(f"Unsupported format: {format}")
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Exported dimension comparison results to {file_name}")
            self.logger.debug(f"Export completed successfully: {file_name}")
            return {"path": file_name, "format": format}
            
        except Exception as e:
            self.logger.error(f"Error exporting dimension comparison results: {str(e)}")
            self.logger.debug(f"Export failed with error: {traceback.format_exc()}")
            return {"error": str(e)}


class IndividualComparisonResultsExporter(Exporter):
    """Exporter for individual comparison results."""
    
    def export(self, output_path: str, format: str = "json") -> Dict[str, Any]:
        """
        Export individual comparison results to a file.
        
        Args:
            output_path: Path to export the individual comparison results to.
            format: Format to export in ('json', 'csv').
            
        Returns:
            Dictionary containing export information.
        """
        self.logger.debug(f"Starting export of individual comparison results to {output_path} in {format} format")
        try:
            # Get comparison results
            self.logger.debug("Retrieving comparison results")
            comparison_results = self.llamasee._comparison_results
            
            if comparison_results is None:
                self.logger.warning("No comparison results available to export")
                return {"error": "No comparison results available"}
            
            self.logger.info(f"Exporting individual comparison results in {format} format to {output_path}")
            
            # Determine if output_path is a directory or a filename
            if os.path.isdir(output_path):
                self.logger.debug(f"Output path is a directory: {output_path}")
                # Generate a filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = os.path.join(output_path, f"individual_comparison_results_{timestamp}.{format}")
            else:
                self.logger.debug(f"Output path is a filename: {output_path}")
                file_name = output_path
            
            # Export based on format
            if format.lower() == 'json':
                self.logger.debug(f"Exporting to JSON format: {file_name}")
                # Convert to dictionary
                if isinstance(comparison_results, pd.DataFrame):
                    self.logger.debug("Converting DataFrame to dictionary for JSON export")
                    comparison_dict = comparison_results.to_dict(orient='records')
                else:
                    self.logger.debug("Using comparison results directly for JSON export")
                    comparison_dict = comparison_results
                
                with open(file_name, 'w') as f:
                    json.dump(comparison_dict, f, indent=2)
            elif format.lower() == 'csv':
                self.logger.debug(f"Exporting to CSV format: {file_name}")
                # For CSV, we need a DataFrame
                if isinstance(comparison_results, pd.DataFrame):
                    self.logger.debug("Using comparison results DataFrame directly for CSV export")
                    df = comparison_results
                else:
                    # For any other type, try to convert to a DataFrame
                    self.logger.debug(f"Converting comparison results of type {type(comparison_results)} to DataFrame")
                    try:
                        df = pd.DataFrame({"data": [comparison_results]})
                    except:
                        self.logger.error(f"Failed to convert comparison results to DataFrame")
                        raise ValueError(f"Unexpected comparison results type: {type(comparison_results)}")
                
                # Write to CSV file
                df.to_csv(file_name, index=False)
            else:
                self.logger.error(f"Unsupported format: {format}")
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Individual comparison results exported to {file_name}")
            self.logger.debug(f"Export completed successfully: {file_name}")
            return {"path": file_name, "format": format}
            
        except Exception as e:
            self.logger.error(f"Error exporting individual comparison results: {str(e)}")
            self.logger.debug(f"Export failed with error: {traceback.format_exc()}")
            return {"error": str(e)} 