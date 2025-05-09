"""Singleton logger for WorkBack application."""

import os
import logging
from typing import Optional

class WorkBackLogger:
    """Singleton logger for WorkBack application."""
    
    _instance: Optional['WorkBackLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'WorkBackLogger':
        if cls._instance is None:
            cls._instance = super(WorkBackLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self) -> None:
        """Initialize the logger with fixed path and configuration."""
        if self._logger is not None:
            return
            
        # Set up log directory
        log_dir = os.path.expanduser("~/.workback")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "workback.log")
        
        # Configure logger
        self._logger = logging.getLogger("workback")
        self._logger.setLevel(logging.DEBUG)
        
        # Create file handler if not already added
        if not self._logger.handlers:
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatter - simplified format focusing on key info
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            self._logger.addHandler(file_handler)
        
        # Prevent propagation to avoid duplicate logs
        self._logger.propagate = False
    
    @property
    def logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self._logger
    
    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a debug message."""
        self._logger.debug(msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an info message."""
        self._logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log a warning message."""
        self._logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs) -> None:
        """Log an error message."""
        self._logger.error(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs) -> None:
        """Log a critical message."""
        self._logger.critical(msg, *args, **kwargs)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a named child logger."""
        return self._logger.getChild(name) 