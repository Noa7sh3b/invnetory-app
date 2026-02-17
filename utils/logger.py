"""
Logging Module - Provides centralized logging for the application.

This module sets up a consistent logging configuration that can be used
throughout the application for debugging and error tracking.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file path with date
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = "inventory_app") -> logging.Logger:
    """
    Set up and return a configured logger.
    
    Args:
        name: Logger name (default: 'inventory_app')
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # File handler - logs everything to file
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Console handler - only warnings and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger instance
logger = setup_logger()


def log_error(message: str, exc: Exception = None):
    """Log an error message with optional exception details."""
    if exc:
        logger.error(f"{message}: {type(exc).__name__}: {str(exc)}", exc_info=True)
    else:
        logger.error(message)


def log_warning(message: str):
    """Log a warning message."""
    logger.warning(message)


def log_info(message: str):
    """Log an info message."""
    logger.info(message)


def log_debug(message: str):
    """Log a debug message."""
    logger.debug(message)


def log_db_operation(operation: str, table: str, success: bool, details: str = ""):
    """
    Log a database operation.
    
    Args:
        operation: Type of operation (INSERT, UPDATE, DELETE, SELECT)
        table: Table name
        success: Whether the operation succeeded
        details: Additional details
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"DB {operation} on {table}: {status}"
    if details:
        message += f" | {details}"
    
    if success:
        logger.debug(message)
    else:
        logger.error(message)
