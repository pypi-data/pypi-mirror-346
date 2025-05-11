"""
Insight storage components for LlamaSee.

This module provides interfaces and implementations for storing and retrieving insights
from various storage backends (files, databases, etc.).
"""
import os
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Type
import pandas as pd
from pathlib import Path

from ..core.insight import Insight

class InsightStorage:
    """
    Base class for insight storage implementations.
    
    This abstract class defines the interface for storing and retrieving insights.
    Concrete implementations should handle the specifics of different storage backends.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the insight storage.
        
        Args:
            **kwargs: Storage-specific configuration parameters
        """
        self.logger = logging.getLogger(__name__)
    
    def save_insights(self, insights: List[Insight], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save a list of insights to the storage backend.
        
        Args:
            insights: List of insights to save
            metadata: Optional metadata about the insights (e.g., comparison ID, timestamp)
            
        Returns:
            str: Identifier for the saved insights (e.g., file path, database ID)
        """
        raise NotImplementedError("Subclasses must implement save_insights")
    
    def load_insights(self, identifier: str) -> List[Insight]:
        """
        Load insights from the storage backend.
        
        Args:
            identifier: Identifier for the insights to load
            
        Returns:
            List[Insight]: Loaded insights
        """
        raise NotImplementedError("Subclasses must implement load_insights")
    
    def list_saved_insights(self) -> List[Dict[str, Any]]:
        """
        List all saved insight sets.
        
        Returns:
            List[Dict[str, Any]]: List of metadata for saved insight sets
        """
        raise NotImplementedError("Subclasses must implement list_saved_insights")
    
    def delete_insights(self, identifier: str) -> bool:
        """
        Delete insights from the storage backend.
        
        Args:
            identifier: Identifier for the insights to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement delete_insights")


class FileInsightStorage(InsightStorage):
    """
    File-based storage for insights.
    
    This implementation stores insights as JSON files in a specified directory.
    """
    
    def __init__(self, storage_dir: str = "insights", **kwargs):
        """
        Initialize the file-based insight storage.
        
        Args:
            storage_dir: Directory to store insight files
            **kwargs: Additional configuration parameters
        """
        super().__init__(**kwargs)
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Initialized file-based insight storage in {self.storage_dir}")
    
    def save_insights(self, insights: List[Insight], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save insights to a JSON file.
        
        Args:
            insights: List of insights to save
            metadata: Optional metadata about the insights
            
        Returns:
            str: Path to the saved file
        """
        if not insights:
            self.logger.warning("No insights to save")
            return ""
        
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        insight_id = str(uuid.uuid4())[:8]
        filename = f"insights_{timestamp}_{insight_id}.json"
        filepath = self.storage_dir / filename
        
        # Prepare data for serialization
        insight_data = []
        for insight in insights:
            insight_dict = {
                "id": insight.id,
                "description": insight.description,
                "importance_score": insight.importance_score,
                "weighted_score": insight.weighted_score,
                "insight_type": insight.insight_type,
                "insight_subtype": insight.insight_subtype,
                "scope_level": insight.scope_level,
                "scope_details": insight.scope_details,
                "dimensions": insight.dimensions,
                "magnitude": insight.magnitude,
                "frequency": insight.frequency,
                "business_impact": insight.business_impact,
                "uniqueness": insight.uniqueness,
                "source_data": insight.source_data,
                "trace": insight.trace
            }
            insight_data.append(insight_dict)
        
        # Create the complete data structure
        data = {
            "insights": insight_data,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Saved {len(insights)} insights to {filepath}")
        return str(filepath)
    
    def load_insights(self, identifier: str) -> List[Insight]:
        """
        Load insights from a JSON file.
        
        Args:
            identifier: Path to the insight file
            
        Returns:
            List[Insight]: Loaded insights
        """
        filepath = Path(identifier)
        if not filepath.exists():
            self.logger.error(f"Insight file not found: {filepath}")
            return []
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            insights = []
            for insight_dict in data.get("insights", []):
                insight = Insight(
                    id=insight_dict["id"],
                    description=insight_dict["description"],
                    importance_score=insight_dict["importance_score"],
                    source_data=insight_dict["source_data"]
                )
                
                # Set additional attributes
                insight.weighted_score = insight_dict.get("weighted_score", 0.0)
                insight.insight_type = insight_dict.get("insight_type", "other")
                insight.insight_subtype = insight_dict.get("insight_subtype")
                insight.scope_level = insight_dict.get("scope_level", "global")
                insight.scope_details = insight_dict.get("scope_details", {})
                insight.dimensions = insight_dict.get("dimensions", [])
                insight.magnitude = insight_dict.get("magnitude", 0.5)
                insight.frequency = insight_dict.get("frequency", 0.5)
                insight.business_impact = insight_dict.get("business_impact", 0.5)
                insight.uniqueness = insight_dict.get("uniqueness", 0.5)
                insight.trace = insight_dict.get("trace", {})
                
                insights.append(insight)
            
            self.logger.info(f"Loaded {len(insights)} insights from {filepath}")
            return insights
        
        except Exception as e:
            self.logger.error(f"Error loading insights from {filepath}: {str(e)}")
            return []
    
    def get_insight_by_id(self, insight_id: str, batch_id: Optional[str] = None) -> Optional[Insight]:
        """
        Get a specific insight by its ID.
        
        Args:
            insight_id: The ID of the insight to retrieve
            batch_id: Optional batch ID to search within
            
        Returns:
            Optional[Insight]: The requested insight, or None if not found
        """
        # If batch_id is provided, load insights from that batch
        if batch_id:
            insights = self.load_insights(batch_id)
            for insight in insights:
                if insight.id == insight_id:
                    return insight
            return None
        
        # Otherwise, search all insight files
        insight_files = list(self.storage_dir.glob("insights_*.json"))
        
        for filepath in insight_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                for insight_dict in data.get("insights", []):
                    if insight_dict["id"] == insight_id:
                        insight = Insight(
                            id=insight_dict["id"],
                            description=insight_dict["description"],
                            importance_score=insight_dict["importance_score"],
                            source_data=insight_dict["source_data"]
                        )
                        
                        # Set additional attributes
                        insight.weighted_score = insight_dict.get("weighted_score", 0.0)
                        insight.insight_type = insight_dict.get("insight_type", "other")
                        insight.insight_subtype = insight_dict.get("insight_subtype")
                        insight.scope_level = insight_dict.get("scope_level", "global")
                        insight.scope_details = insight_dict.get("scope_details", {})
                        insight.dimensions = insight_dict.get("dimensions", [])
                        insight.magnitude = insight_dict.get("magnitude", 0.5)
                        insight.frequency = insight_dict.get("frequency", 0.5)
                        insight.business_impact = insight_dict.get("business_impact", 0.5)
                        insight.uniqueness = insight_dict.get("uniqueness", 0.5)
                        insight.trace = insight_dict.get("trace", {})
                        
                        return insight
            
            except Exception as e:
                self.logger.error(f"Error reading insight file {filepath}: {str(e)}")
        
        self.logger.warning(f"Insight with ID {insight_id} not found")
        return None
    
    def list_saved_insights(self) -> List[Dict[str, Any]]:
        """
        List all saved insight files.
        
        Returns:
            List[Dict[str, Any]]: List of metadata for saved insight files
        """
        insight_files = list(self.storage_dir.glob("insights_*.json"))
        result = []
        
        for filepath in insight_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                metadata = data.get("metadata", {})
                metadata["filepath"] = str(filepath)
                metadata["timestamp"] = data.get("timestamp", "")
                metadata["insight_count"] = len(data.get("insights", []))
                
                result.append(metadata)
            
            except Exception as e:
                self.logger.error(f"Error reading metadata from {filepath}: {str(e)}")
        
        # Sort by timestamp (newest first)
        result.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return result
    
    def delete_insights(self, identifier: str) -> bool:
        """
        Delete an insight file.
        
        Args:
            identifier: Path to the insight file
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        filepath = Path(identifier)
        if not filepath.exists():
            self.logger.error(f"Insight file not found: {filepath}")
            return False
        
        try:
            filepath.unlink()
            self.logger.info(f"Deleted insight file: {filepath}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error deleting insight file {filepath}: {str(e)}")
            return False


class CSVInsightStorage(InsightStorage):
    """
    CSV-based storage for insights.
    
    This implementation stores insights as CSV files, which can be easily
    imported into spreadsheet applications or data analysis tools.
    """
    
    def __init__(self, storage_dir: str = "insights", **kwargs):
        """
        Initialize the CSV-based insight storage.
        
        Args:
            storage_dir: Directory to store insight files
            **kwargs: Additional configuration parameters
        """
        super().__init__(**kwargs)
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Initialized CSV-based insight storage in {self.storage_dir}")
    
    def save_insights(self, insights: List[Insight], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save insights to a CSV file.
        
        Args:
            insights: List of insights to save
            metadata: Optional metadata about the insights
            
        Returns:
            str: Path to the saved file
        """
        if not insights:
            self.logger.warning("No insights to save")
            return ""
        
        # Generate a unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        insight_id = str(uuid.uuid4())[:8]
        filename = f"insights_{timestamp}_{insight_id}.csv"
        filepath = self.storage_dir / filename
        
        # Prepare data for CSV
        insight_data = []
        for insight in insights:
            insight_dict = {
                "id": insight.id,
                "description": insight.description,
                "importance_score": insight.importance_score,
                "weighted_score": insight.weighted_score,
                "insight_type": insight.insight_type,
                "insight_subtype": insight.insight_subtype,
                "scope_level": insight.scope_level,
                "scope_details": json.dumps(insight.scope_details),
                "dimensions": ",".join(insight.dimensions),
                "magnitude": insight.magnitude,
                "frequency": insight.frequency,
                "business_impact": insight.business_impact,
                "uniqueness": insight.uniqueness,
                "trace_data": json.dumps(insight.trace)
            }
            
            # Add source data fields (flattened)
            if insight.source_data:
                for key, value in insight.source_data.items():
                    if isinstance(value, (str, int, float, bool)):
                        insight_dict[f"source_{key}"] = value
                    else:
                        insight_dict[f"source_{key}"] = json.dumps(value)
            
            insight_data.append(insight_dict)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(insight_data)
        df.to_csv(filepath, index=False)
        
        # Save metadata separately
        if metadata:
            metadata_filepath = self.storage_dir / f"metadata_{timestamp}_{insight_id}.json"
            with open(metadata_filepath, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        self.logger.info(f"Saved {len(insights)} insights to {filepath}")
        return str(filepath)
    
    def load_insights(self, filepath: str) -> List[Insight]:
        """
        Load insights from a CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            List[Insight]: List of loaded insights
        """
        if not os.path.exists(filepath):
            self.logger.warning(f"Insight file not found: {filepath}")
            return []
        
        try:
            df = pd.read_csv(filepath)
            insights = []
            
            for _, row in df.iterrows():
                try:
                    # Create source data dictionary
                    source_data = {}
                    for col in df.columns:
                        if col.startswith('source_'):
                            key = col[7:]  # Remove 'source_' prefix
                            value = row[col]
                            if pd.notna(value):
                                try:
                                    # Try to parse as JSON if it's a string
                                    if isinstance(value, str):
                                        source_data[key] = json.loads(value)
                                    else:
                                        source_data[key] = value
                                except json.JSONDecodeError:
                                    source_data[key] = value
                    
                    # Create insight
                    insight = Insight(
                        id=row['id'],
                        description=row['description'],
                        importance_score=float(row['importance_score']),
                        source_data=source_data
                    )
                    
                    # Set additional attributes
                    insight.weighted_score = float(row['weighted_score'])
                    insight.insight_type = row['insight_type']
                    insight.insight_subtype = row.get('insight_subtype', '')
                    insight.scope_level = row['scope_level']
                    insight.scope_details = json.loads(row['scope_details']) if pd.notna(row['scope_details']) else {}
                    insight.dimensions = row['dimensions'].split(',') if pd.notna(row['dimensions']) else []
                    insight.magnitude = float(row['magnitude'])
                    insight.frequency = float(row['frequency'])
                    insight.business_impact = float(row['business_impact'])
                    insight.uniqueness = float(row['uniqueness'])
                    
                    # Load traceability data
                    if 'trace_data' in row and pd.notna(row['trace_data']):
                        insight.trace = json.loads(row['trace_data'])
                    
                    insights.append(insight)
                    
                except Exception as e:
                    self.logger.warning(f"Error loading insight with ID {row.get('id', 'unknown')}: {str(e)}")
                    continue
            
            self.logger.info(f"Loaded {len(insights)} insights from {filepath}")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error loading insights from {filepath}: {str(e)}")
            return []
    
    def get_insight_by_id(self, insight_id: str, batch_id: Optional[str] = None) -> Optional[Insight]:
        """
        Get a specific insight by its ID.
        
        Args:
            insight_id: The ID of the insight to retrieve
            batch_id: Optional batch ID to search within
            
        Returns:
            Optional[Insight]: The requested insight, or None if not found
        """
        # If batch_id is provided, load insights from that batch
        if batch_id:
            insights = self.load_insights(batch_id)
            for insight in insights:
                if insight.id == insight_id:
                    return insight
            return None
        
        # Otherwise, search all insight files
        insight_files = list(self.storage_dir.glob("insights_*.csv"))
        
        for filepath in insight_files:
            try:
                # Load CSV data
                df = pd.read_csv(filepath)
                
                # Check if the insight ID exists in this file
                if insight_id in df["id"].values:
                    row = df[df["id"] == insight_id].iloc[0]
                    
                    # Extract source data
                    source_data = {}
                    for col in df.columns:
                        if col.startswith("source_"):
                            key = col[7:]  # Remove "source_" prefix
                            try:
                                value = json.loads(row[col])
                            except (json.JSONDecodeError, TypeError):
                                value = row[col]
                            source_data[key] = value
                    
                    # Create insight
                    insight = Insight(
                        id=row["id"],
                        description=row["description"],
                        importance_score=float(row["importance_score"]),
                        source_data=source_data
                    )
                    
                    # Set additional attributes
                    insight.weighted_score = float(row["weighted_score"])
                    insight.insight_type = row["insight_type"]
                    insight.insight_subtype = row["insight_subtype"]
                    insight.scope_level = row["scope_level"]
                    insight.scope_details = json.loads(row["scope_details"])
                    insight.dimensions = row["dimensions"].split(",") if row["dimensions"] else []
                    insight.magnitude = float(row["magnitude"])
                    insight.frequency = float(row["frequency"])
                    insight.business_impact = float(row["business_impact"])
                    insight.uniqueness = float(row["uniqueness"])
                    
                    return insight
            
            except Exception as e:
                self.logger.error(f"Error reading insight file {filepath}: {str(e)}")
        
        self.logger.warning(f"Insight with ID {insight_id} not found")
        return None
    
    def list_saved_insights(self) -> List[Dict[str, Any]]:
        """
        List all saved insight files.
        
        Returns:
            List[Dict[str, Any]]: List of metadata for saved insight files
        """
        insight_files = list(self.storage_dir.glob("insights_*.csv"))
        result = []
        
        for filepath in insight_files:
            try:
                # Load metadata if available
                metadata_filepath = self.storage_dir / f"metadata_{filepath.stem.split('_', 1)[1]}.json"
                metadata = {}
                if metadata_filepath.exists():
                    with open(metadata_filepath, 'r') as f:
                        metadata = json.load(f)
                
                # Count insights in the CSV file
                df = pd.read_csv(filepath)
                insight_count = len(df)
                
                metadata["filepath"] = str(filepath)
                metadata["timestamp"] = filepath.stem.split("_")[1]  # Extract timestamp from filename
                metadata["insight_count"] = insight_count
                
                result.append(metadata)
            
            except Exception as e:
                self.logger.error(f"Error reading metadata from {filepath}: {str(e)}")
        
        # Sort by timestamp (newest first)
        result.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return result
    
    def delete_insights(self, identifier: str) -> bool:
        """
        Delete an insight file.
        
        Args:
            identifier: Path to the insight file
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        filepath = Path(identifier)
        if not filepath.exists():
            self.logger.error(f"Insight file not found: {filepath}")
            return False
        
        try:
            # Delete the CSV file
            filepath.unlink()
            
            # Delete the metadata file if it exists
            metadata_filepath = self.storage_dir / f"metadata_{filepath.stem.split('_', 1)[1]}.json"
            if metadata_filepath.exists():
                metadata_filepath.unlink()
            
            self.logger.info(f"Deleted insight file: {filepath}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error deleting insight file {filepath}: {str(e)}")
            return False


class SQLiteInsightStorage(InsightStorage):
    """
    SQLite-based storage for insights.
    
    This implementation stores insights in a SQLite database, which provides
    a lightweight but powerful database solution without requiring a separate server.
    """
    
    def __init__(self, db_path: str = "insights.db", **kwargs):
        """
        Initialize the SQLite-based insight storage.
        
        Args:
            db_path: Path to the SQLite database file
            **kwargs: Additional configuration parameters
        """
        super().__init__(**kwargs)
        self.db_path = db_path
        self._init_db()
        self.logger.info(f"Initialized SQLite-based insight storage at {db_path}")
    
    def _init_db(self):
        """Initialize the database schema."""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create insights table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS insights (
            id TEXT PRIMARY KEY,
            description TEXT,
            importance_score REAL,
            weighted_score REAL,
            insight_type TEXT,
            scope_level TEXT,
            dimensions TEXT,
            magnitude REAL,
            frequency REAL,
            business_impact REAL,
            uniqueness REAL,
            source_data TEXT,
            trace TEXT,
            created_at TEXT,
            batch_id TEXT
        )
        ''')
        
        # Create metadata table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            batch_id TEXT PRIMARY KEY,
            metadata TEXT,
            created_at TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_insights(self, insights: List[Insight], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Save insights to the SQLite database.
        
        Args:
            insights: List of insights to save
            metadata: Optional metadata about the insights
            
        Returns:
            str: Batch ID for the saved insights
        """
        if not insights:
            self.logger.warning("No insights to save")
            return ""
        
        import sqlite3
        
        # Generate a batch ID
        batch_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Save metadata
            if metadata:
                cursor.execute(
                    "INSERT INTO metadata (batch_id, metadata, created_at) VALUES (?, ?, ?)",
                    (batch_id, json.dumps(metadata), timestamp)
                )
            
            # Save insights
            for insight in insights:
                cursor.execute(
                    """
                    INSERT INTO insights (
                        id, description, importance_score, weighted_score, insight_type,
                        scope_level, dimensions, magnitude, frequency, business_impact,
                        uniqueness, source_data, trace, created_at, batch_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        insight.id,
                        insight.description,
                        insight.importance_score,
                        insight.weighted_score,
                        insight.insight_type,
                        insight.scope_level,
                        json.dumps(insight.dimensions),
                        insight.magnitude,
                        insight.frequency,
                        insight.business_impact,
                        insight.uniqueness,
                        json.dumps(insight.source_data),
                        json.dumps(insight.trace),
                        timestamp,
                        batch_id
                    )
                )
            
            conn.commit()
            self.logger.info(f"Saved {len(insights)} insights to database with batch ID {batch_id}")
            return batch_id
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error saving insights to database: {str(e)}")
            return ""
        
        finally:
            conn.close()
    
    def load_insights(self, identifier: str) -> List[Insight]:
        """
        Load insights from the SQLite database.
        
        Args:
            identifier: Batch ID for the insights to load
            
        Returns:
            List[Insight]: Loaded insights
        """
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT * FROM insights WHERE batch_id = ?",
                (identifier,)
            )
            rows = cursor.fetchall()
            
            if not rows:
                self.logger.warning(f"No insights found with batch ID {identifier}")
                return []
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            insights = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                
                # Create insight
                insight = Insight(
                    id=row_dict["id"],
                    description=row_dict["description"],
                    importance_score=row_dict["importance_score"],
                    source_data=json.loads(row_dict["source_data"])
                )
                
                # Set additional attributes
                insight.weighted_score = row_dict["weighted_score"]
                insight.insight_type = row_dict["insight_type"]
                insight.insight_subtype = row_dict["insight_subtype"]
                insight.scope_level = row_dict["scope_level"]
                insight.scope_details = row_dict["scope_details"]
                insight.dimensions = json.loads(row_dict["dimensions"])
                insight.magnitude = row_dict["magnitude"]
                insight.frequency = row_dict["frequency"]
                insight.business_impact = row_dict["business_impact"]
                insight.uniqueness = row_dict["uniqueness"]
                insight.trace = json.loads(row_dict["trace"])
                
                insights.append(insight)
            
            self.logger.info(f"Loaded {len(insights)} insights from database with batch ID {identifier}")
            return insights
        
        except Exception as e:
            self.logger.error(f"Error loading insights from database: {str(e)}")
            return []
        
        finally:
            conn.close()
    
    def list_saved_insights(self) -> List[Dict[str, Any]]:
        """
        List all saved insight batches.
        
        Returns:
            List[Dict[str, Any]]: List of metadata for saved insight batches
        """
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT m.batch_id, m.metadata, m.created_at, COUNT(i.id) as insight_count
                FROM metadata m
                LEFT JOIN insights i ON m.batch_id = i.batch_id
                GROUP BY m.batch_id
                ORDER BY m.created_at DESC
                """
            )
            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                batch_id, metadata_json, created_at, insight_count = row
                
                metadata = json.loads(metadata_json) if metadata_json else {}
                metadata["batch_id"] = batch_id
                metadata["created_at"] = created_at
                metadata["insight_count"] = insight_count
                
                result.append(metadata)
            
            return result
        
        except Exception as e:
            self.logger.error(f"Error listing saved insights: {str(e)}")
            return []
        
        finally:
            conn.close()
    
    def delete_insights(self, identifier: str) -> bool:
        """
        Delete insights from the SQLite database.
        
        Args:
            identifier: Batch ID for the insights to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete insights
            cursor.execute(
                "DELETE FROM insights WHERE batch_id = ?",
                (identifier,)
            )
            
            # Delete metadata
            cursor.execute(
                "DELETE FROM metadata WHERE batch_id = ?",
                (identifier,)
            )
            
            conn.commit()
            self.logger.info(f"Deleted insights with batch ID {identifier}")
            return True
        
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Error deleting insights from database: {str(e)}")
            return False
        
        finally:
            conn.close()


# Factory function to create the appropriate storage backend
def create_insight_storage(storage_type: str = "file", **kwargs) -> InsightStorage:
    """
    Create an insight storage instance based on the specified type.
    
    Args:
        storage_type: Type of storage to create ("file", "csv", "sqlite")
        **kwargs: Additional configuration parameters
        
    Returns:
        InsightStorage: An instance of the specified storage type
    """
    storage_types = {
        "file": FileInsightStorage,
        "csv": CSVInsightStorage,
        "sqlite": SQLiteInsightStorage
    }
    
    if storage_type not in storage_types:
        raise ValueError(f"Unknown storage type: {storage_type}. Valid types are: {', '.join(storage_types.keys())}")
    
    storage_class = storage_types[storage_type]
    return storage_class(**kwargs) 