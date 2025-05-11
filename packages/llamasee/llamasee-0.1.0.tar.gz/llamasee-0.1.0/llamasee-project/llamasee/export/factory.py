"""
Factory for creating exporters.
"""

from typing import Dict, Type, Optional
from .exporters import (
    Exporter, 
    ResultsExporter, 
    DimensionResultsExporter, 
    FitResultsExporter,
    DimensionComparisonResultsExporter,
    IndividualComparisonResultsExporter
)

class ExporterFactory:
    """Factory for creating exporters."""
    
    _exporters: Dict[str, Type[Exporter]] = {
        'results': ResultsExporter,
        'dimension_results': DimensionResultsExporter,
        'fit_results': FitResultsExporter,
        'dimension_comparison_results': DimensionComparisonResultsExporter,
        'individual_comparison_results': IndividualComparisonResultsExporter
    }
    
    @classmethod
    def register_exporter(cls, name: str, exporter_class: Type[Exporter]) -> None:
        """
        Register a new exporter class.
        
        Args:
            name: Name of the exporter.
            exporter_class: Exporter class to register.
        """
        cls._exporters[name] = exporter_class
    
    @classmethod
    def get_exporter(cls, name: str, llamasee) -> Optional[Exporter]:
        """
        Get an exporter instance by name.
        
        Args:
            name: Name of the exporter.
            llamasee: LlamaSee instance to pass to the exporter.
            
        Returns:
            Exporter instance or None if not found.
        """
        exporter_class = cls._exporters.get(name)
        if exporter_class:
            return exporter_class(llamasee)
        return None
    
    @classmethod
    def get_available_exporters(cls) -> list:
        """
        Get a list of available exporter names.
        
        Returns:
            List of available exporter names.
        """
        return list(cls._exporters.keys()) 