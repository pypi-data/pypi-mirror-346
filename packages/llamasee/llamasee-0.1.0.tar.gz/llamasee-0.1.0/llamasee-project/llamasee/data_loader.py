import pandas as pd
from typing import Tuple, Dict, Any, Optional
import logging

class DataLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def from_csv(file_path_a: str, file_path_b: str, **kwargs) -> Tuple[Dict[str, Any], pd.DataFrame, Dict[str, Any], pd.DataFrame]:
        """Load data from CSV files"""
        try:
            data_a = pd.read_csv(file_path_a, **kwargs)
            data_b = pd.read_csv(file_path_b, **kwargs)
            
            metadata_a = {
                'source': file_path_a,
                'format': 'csv',
                'rows': len(data_a),
                'columns': list(data_a.columns)
            }
            
            metadata_b = {
                'source': file_path_b,
                'format': 'csv',
                'rows': len(data_b),
                'columns': list(data_b.columns)
            }
            
            return metadata_a, data_a, metadata_b, data_b
        except Exception as e:
            logging.error(f"Error loading CSV files: {str(e)}")
            raise

    @staticmethod
    def from_parquet(file_path_a: str, file_path_b: str, **kwargs) -> Tuple[Dict[str, Any], pd.DataFrame, Dict[str, Any], pd.DataFrame]:
        """Load data from Parquet files"""
        try:
            data_a = pd.read_parquet(file_path_a, **kwargs)
            data_b = pd.read_parquet(file_path_b, **kwargs)
            
            metadata_a = {
                'source': file_path_a,
                'format': 'parquet',
                'rows': len(data_a),
                'columns': list(data_a.columns)
            }
            
            metadata_b = {
                'source': file_path_b,
                'format': 'parquet',
                'rows': len(data_b),
                'columns': list(data_b.columns)
            }
            
            return metadata_a, data_a, metadata_b, data_b
        except Exception as e:
            logging.error(f"Error loading Parquet files: {str(e)}")
            raise

    @staticmethod
    def from_dataframe(df_a: pd.DataFrame, df_b: pd.DataFrame, metadata_a: Optional[Dict[str, Any]] = None, 
                      metadata_b: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame, Dict[str, Any], pd.DataFrame]:
        """Load data from pandas DataFrames"""
        try:
            metadata_a = metadata_a or {
                'source': 'dataframe',
                'format': 'dataframe',
                'rows': len(df_a),
                'columns': list(df_a.columns)
            }
            
            metadata_b = metadata_b or {
                'source': 'dataframe',
                'format': 'dataframe',
                'rows': len(df_b),
                'columns': list(df_b.columns)
            }
            
            return metadata_a, df_a, metadata_b, df_b
        except Exception as e:
            logging.error(f"Error loading DataFrames: {str(e)}")
            raise 