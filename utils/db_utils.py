"""
Database Utilities - Safe database operations with error handling.

This module provides wrapper functions for database operations
that include proper error handling, logging, and connection management.
"""

import sqlite3
from typing import Any, List, Optional, Tuple, Union
from functools import wraps

from db import get_conn
from utils.logger import log_error, log_debug, log_db_operation


class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def safe_db_operation(operation_name: str = "DB Operation"):
    """
    Decorator for safe database operations with error handling.
    
    Args:
        operation_name: Name of the operation for logging
        
    Returns:
        Decorated function with error handling
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = None
            try:
                result = func(*args, **kwargs)
                log_debug(f"{operation_name} completed successfully")
                return result
            except sqlite3.IntegrityError as e:
                log_error(f"{operation_name} integrity error", e)
                raise DatabaseError(f"Data integrity error: {str(e)}")
            except sqlite3.OperationalError as e:
                log_error(f"{operation_name} operational error", e)
                raise DatabaseError(f"Database operation failed: {str(e)}")
            except sqlite3.Error as e:
                log_error(f"{operation_name} error", e)
                raise DatabaseError(f"Database error: {str(e)}")
            except Exception as e:
                log_error(f"{operation_name} unexpected error", e)
                raise
        return wrapper
    return decorator


def execute_query(
    query: str,
    params: tuple = (),
    fetch: str = "none",
    commit: bool = False
) -> Union[List[Tuple], Tuple, int, None]:
    """
    Execute a database query safely.
    
    Args:
        query: SQL query string
        params: Query parameters (tuple)
        fetch: "none", "one", "all", or "lastrowid"
        commit: Whether to commit the transaction
        
    Returns:
        Query results based on fetch parameter
        
    Raises:
        DatabaseError: If the query fails
    """
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        result = None
        if fetch == "one":
            result = cursor.fetchone()
        elif fetch == "all":
            result = cursor.fetchall()
        elif fetch == "lastrowid":
            result = cursor.lastrowid
        
        if commit:
            conn.commit()
            
        return result
        
    except sqlite3.IntegrityError as e:
        if conn:
            conn.rollback()
        log_error("Query integrity error", e)
        raise DatabaseError(f"Data integrity error: {str(e)}")
    except sqlite3.OperationalError as e:
        if conn:
            conn.rollback()
        log_error("Query operational error", e)
        raise DatabaseError(f"Database operation failed: {str(e)}")
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        log_error("Query error", e)
        raise DatabaseError(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()


def validate_required(value: Any, field_name: str) -> None:
    """
    Validate that a required field is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error message
        
    Raises:
        ValidationError: If value is empty
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{field_name} is required")


def validate_positive_number(value: Union[int, float], field_name: str, allow_zero: bool = False) -> None:
    """
    Validate that a number is positive.
    
    Args:
        value: Number to validate
        field_name: Name of the field for error message
        allow_zero: Whether zero is allowed
        
    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        raise ValidationError(f"{field_name} is required")
    
    if not allow_zero and value <= 0:
        raise ValidationError(f"{field_name} must be greater than zero")
    elif allow_zero and value < 0:
        raise ValidationError(f"{field_name} cannot be negative")


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return True  # Empty is OK (optional field)
    
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def sanitize_string(value: Optional[str], max_length: int = 500) -> Optional[str]:
    """
    Sanitize a string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string or None
    """
    if value is None:
        return None
    
    # Strip whitespace
    cleaned = value.strip()
    
    # Truncate if too long
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned if cleaned else None


class TransactionManager:
    """
    Context manager for database transactions.
    
    Usage:
        with TransactionManager() as conn:
            conn.execute("INSERT ...")
            conn.execute("UPDATE ...")
        # Automatically commits on success, rolls back on error
    """
    
    def __init__(self):
        self.conn = None
        
    def __enter__(self):
        self.conn = get_conn()
        return self.conn
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An error occurred, rollback
            if self.conn:
                self.conn.rollback()
                log_error(f"Transaction rolled back due to: {exc_val}")
        else:
            # Success, commit
            if self.conn:
                self.conn.commit()
                log_debug("Transaction committed successfully")
        
        if self.conn:
            self.conn.close()
            
        # Don't suppress the exception
        return False
