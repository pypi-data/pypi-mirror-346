"""
Stage-based logging utilities for LlamaSee.

This module provides utilities for logging the lifecycle stages of LlamaSee,
including input checkpoints, progress logging, output checkpoints, and error logging.
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from .logger import get_logger

class StageLogger:
    """
    Logger for LlamaSee lifecycle stages.
    
    This class provides methods for logging the inputs, outputs, and progress
    of each stage in the LlamaSee lifecycle.
    """
    
    def __init__(self, stage_name: str, logger_name: str = "llamasee.stages", stage_manager=None):
        """
        Initialize the stage logger.
        
        Args:
            stage_name: Name of the stage (e.g., "prepare", "fit", "compare")
            logger_name: Name of the logger to use
            stage_manager: Reference to the StageManager instance
        """
        self.stage_name = stage_name
        self.logger = get_logger(logger_name)
        self.start_time = None
        self.checkpoints = {}
        self.stage_manager = stage_manager
    
    def start_stage(self, inputs: Dict[str, Any]) -> None:
        """
        Log the start of a stage with input parameters.
        
        Args:
            inputs: Dictionary of input parameters
        """
        self.start_time = time.time()
        self.logger.info(f"Starting {self.stage_name} stage")
        self.logger.debug(f"{self.stage_name} stage inputs: {inputs}")
        
        # Create input checkpoint
        self.checkpoints["input"] = {
            "timestamp": datetime.now().isoformat(),
            "inputs": inputs
        }
    
    def log_progress(self, message: str, level: str = "info") -> None:
        """
        Log progress within a stage.
        
        Args:
            message: Progress message
            level: Log level (debug, info, warning, error)
        """
        log_method = getattr(self.logger, level.lower())
        log_method(f"{self.stage_name} stage progress: {message}")
    
    def create_checkpoint(self, name: str, data: Dict[str, Any]) -> None:
        """
        Create a checkpoint with the given name and data.
        
        Args:
            name: Checkpoint name
            data: Checkpoint data
        """
        self.checkpoints[name] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.logger.debug(f"{self.stage_name} stage checkpoint '{name}' created")
    
    def get_checkpoint(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a checkpoint by name.
        
        Args:
            name: Checkpoint name
            
        Returns:
            Checkpoint data or None if not found
        """
        return self.checkpoints.get(name)
    
    def validate_checkpoint(self, name: str, required_fields: List[str]) -> bool:
        """
        Validate that a checkpoint has all required fields.
        
        Args:
            name: Checkpoint name
            required_fields: List of required field names
            
        Returns:
            True if checkpoint exists and has all required fields
        """
        checkpoint = self.get_checkpoint(name)
        if not checkpoint or "data" not in checkpoint:
            return False
        
        return all(field in checkpoint["data"] for field in required_fields)
    
    def _end_stage(self, outputs: Dict[str, Any], success: bool = True) -> Dict[str, Any]:
        """
        Log the end of a stage with output parameters.
        
        Args:
            outputs: Dictionary of output parameters
            success: Whether the stage completed successfully
            
        Returns:
            Dictionary with stage summary
        """
        end_time = time.time()
        duration = end_time - self.start_time if self.start_time else 0
        
        # Create output checkpoint
        self.checkpoints["output"] = {
            "timestamp": datetime.now().isoformat(),
            "outputs": outputs,
            "success": success,
            "duration": duration
        }
        
        # Log stage completion
        if success:
            self.logger.info(f"Completed {self.stage_name} stage in {duration:.2f} seconds")
            self.logger.debug(f"{self.stage_name} stage outputs: {outputs}")
        else:
            self.logger.warning(f"{self.stage_name} stage completed with issues in {duration:.2f} seconds")
            self.logger.debug(f"{self.stage_name} stage outputs: {outputs}")
        
        # Update stage status in the stage manager
        if hasattr(self, 'stage_manager'):
            status = "completed" if success else "failed"
            self.stage_manager.set_stage_status(self.stage_name, status)
        
        # Return stage summary
        return {
            "stage": self.stage_name,
            "success": success,
            "duration": duration,
            "checkpoints": list(self.checkpoints.keys())
        }
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an error that occurred during a stage.
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat()
        }
        
        if context:
            error_data.update(context)
        
        self.logger.error(f"Error in {self.stage_name} stage: {str(error)}")
        self.logger.debug(f"{self.stage_name} stage error details: {error_data}")
        
        # Create error checkpoint
        self.checkpoints["error"] = error_data


class StageManager:
    """
    Manager for LlamaSee lifecycle stages.
    
    This class provides methods for managing the lifecycle stages,
    including tracking stage status and dependencies.
    """
    
    def __init__(self):
        """Initialize the stage manager."""
        self.logger = get_logger("llamasee.stages")
        self.stages = {}
        self.stage_status = {}
        self.stage_dependencies = {
            "prepare": [],
            "fit": ["prepare"],
            "compare": ["fit"],
            "generate_insights": ["compare"],
            "export_results": ["generate_insights"]
        }
    
    def register_stage(self, stage_name: str, stage_logger: StageLogger) -> None:
        """
        Register a stage with the manager.
        
        Args:
            stage_name: Name of the stage
            stage_logger: Stage logger instance
        """
        self.stages[stage_name] = stage_logger
        self.stage_status[stage_name] = "not_started"
        self.logger.debug(f"Registered stage: {stage_name}")
        
        # Set the stage manager reference in the stage logger
        stage_logger.stage_manager = self
    
    def start_stage(self, stage_name: str, inputs: Dict[str, Any] = None) -> None:
        """
        Start a stage and set its status to in_progress.
        
        Args:
            stage_name: Name of the stage to start
            inputs: Optional dictionary of input parameters
        """
        if stage_name in self.stages:
            self.set_stage_status(stage_name, "in_progress")
            stage_logger = self.stages[stage_name]
            stage_logger.start_stage(inputs or {})
            self.logger.debug(f"Started stage: {stage_name}")
        else:
            self.logger.warning(f"Cannot start unregistered stage: {stage_name}")
    
    def complete_stage(self, stage_name: str, outputs: Dict[str, Any] = None) -> None:
        """
        Complete a stage and set its status to completed.
        
        Args:
            stage_name: Name of the stage to complete
            outputs: Optional dictionary of output parameters
        """
        if stage_name in self.stages:
            self.set_stage_status(stage_name, "completed")
            stage_logger = self.stages[stage_name]
            stage_logger._end_stage(outputs or {}, success=True)
            self.logger.debug(f"Completed stage: {stage_name}")
        else:
            self.logger.warning(f"Cannot complete unregistered stage: {stage_name}")
    
    def fail_stage(self, stage_name: str, outputs: Dict[str, Any] = None) -> None:
        """
        Mark a stage as failed and set its status to failed.
        
        Args:
            stage_name: Name of the stage that failed
            outputs: Optional dictionary of output parameters
        """
        if stage_name in self.stages:
            self.set_stage_status(stage_name, "failed")
            stage_logger = self.stages[stage_name]
            stage_logger._end_stage(outputs or {}, success=False)
            self.logger.debug(f"Failed stage: {stage_name}")
        else:
            self.logger.warning(f"Cannot fail unregistered stage: {stage_name}")
    
    def get_stage(self, stage_name: str) -> Optional[StageLogger]:
        """
        Get a stage by name.
        
        Args:
            stage_name: Name of the stage
            
        Returns:
            Stage logger or None if not found
        """
        return self.stages.get(stage_name)
    
    def get_stage_status(self, stage_name: str) -> str:
        """
        Get the status of a stage.
        
        Args:
            stage_name: Name of the stage
            
        Returns:
            Stage status (not_started, in_progress, completed, failed)
        """
        return self.stage_status.get(stage_name, "unknown")
    
    def set_stage_status(self, stage_name: str, status: str) -> None:
        """
        Set the status of a stage.
        
        Args:
            stage_name: Name of the stage
            status: New status (not_started, in_progress, completed, failed)
        """
        if stage_name in self.stage_status:
            self.stage_status[stage_name] = status
            self.logger.debug(f"Stage {stage_name} status set to {status}")
    
    def is_stage_completed(self, stage_name: str) -> bool:
        """
        Check if a stage has completed successfully.
        
        Args:
            stage_name: Name of the stage
            
        Returns:
            True if the stage has completed successfully, False otherwise
        """
        return self.get_stage_status(stage_name) == "completed"
    
    def can_run_stage(self, stage_name: str) -> bool:
        """
        Check if a stage can be run based on its dependencies.
        
        Args:
            stage_name: Name of the stage
            
        Returns:
            True if all dependencies are completed
        """
        if stage_name not in self.stage_dependencies:
            return True
        
        for dependency in self.stage_dependencies[stage_name]:
            if self.get_stage_status(dependency) != "completed":
                return False
        
        return True
    
    def get_stage_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all stages.
        
        Returns:
            Dictionary with stage summaries
        """
        summary = {}
        for stage_name, status in self.stage_status.items():
            stage_logger = self.get_stage(stage_name)
            if stage_logger:
                output_checkpoint = stage_logger.get_checkpoint("output")
                summary[stage_name] = {
                    "status": status,
                    "duration": output_checkpoint.get("duration", 0) if output_checkpoint else 0,
                    "success": output_checkpoint.get("success", False) if output_checkpoint else False
                }
            else:
                summary[stage_name] = {
                    "status": status,
                    "duration": 0,
                    "success": False
                }
        
        return summary 