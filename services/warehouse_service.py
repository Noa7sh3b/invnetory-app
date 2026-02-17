"""
Warehouse Service - Handles all warehouse-related database operations.

This module provides CRUD operations for warehouses with
proper error handling and validation.
"""

from typing import List, Tuple, Optional
from db import get_conn
from utils.logger import log_error, log_debug, log_db_operation


def add_warehouse(name: str, rack_number: str = "") -> Tuple[bool, str]:
    """
    Add a new warehouse.
    
    Args:
        name: Warehouse name
        rack_number: Optional rack number
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Warehouse name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "INSERT OR IGNORE INTO warehouses(name, rack_number) VALUES(?, ?)",
            (name.strip(), rack_number.strip() if rack_number else ""),
        )
        conn.commit()
        log_db_operation("INSERT", "warehouses", True, f"name={name.strip()}")
        return True, "Warehouse added successfully"
    except Exception as e:
        log_error("Failed to add warehouse", e)
        return False, f"Failed to add warehouse: {str(e)}"
    finally:
        if conn:
            conn.close()


def list_warehouses() -> List[Tuple]:
    """
    Get all warehouses.
    
    Returns:
        List of (id, name, rack_number) tuples
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute(
            "SELECT id, name, rack_number FROM warehouses ORDER BY name"
        ).fetchall()
        log_debug(f"Listed {len(rows)} warehouses")
        return rows
    except Exception as e:
        log_error("Failed to list warehouses", e)
        return []
    finally:
        if conn:
            conn.close()


def get_warehouse(warehouse_id: int) -> Optional[Tuple]:
    """
    Get a warehouse by ID.
    
    Args:
        warehouse_id: Warehouse ID
        
    Returns:
        Warehouse tuple or None
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute(
            "SELECT id, name, rack_number FROM warehouses WHERE id = ?",
            (warehouse_id,)
        ).fetchone()
        return row
    except Exception as e:
        log_error(f"Failed to get warehouse {warehouse_id}", e)
        return None
    finally:
        if conn:
            conn.close()


def update_warehouse(warehouse_id: int, name: str, rack_number: str = "") -> Tuple[bool, str]:
    """
    Update a warehouse.
    
    Args:
        warehouse_id: Warehouse ID
        name: New warehouse name
        rack_number: New rack number
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Warehouse name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "UPDATE warehouses SET name = ?, rack_number = ? WHERE id = ?",
            (name.strip(), rack_number.strip() if rack_number else "", warehouse_id),
        )
        conn.commit()
        log_db_operation("UPDATE", "warehouses", True, f"id={warehouse_id}")
        return True, "Warehouse updated successfully"
    except Exception as e:
        log_error(f"Failed to update warehouse {warehouse_id}", e)
        return False, f"Failed to update warehouse: {str(e)}"
    finally:
        if conn:
            conn.close()


def delete_warehouse(warehouse_id: int) -> Tuple[bool, str]:
    """
    Delete a warehouse.
    
    Args:
        warehouse_id: Warehouse ID
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    conn = None
    try:
        conn = get_conn()
        # Check if warehouse is in use
        product_count = conn.execute(
            "SELECT COUNT(*) FROM products WHERE warehouse_id = ?",
            (warehouse_id,)
        ).fetchone()[0]
        
        if product_count > 0:
            return False, f"Cannot delete: {product_count} products are in this warehouse"
        
        conn.execute("DELETE FROM warehouses WHERE id = ?", (warehouse_id,))
        conn.commit()
        log_db_operation("DELETE", "warehouses", True, f"id={warehouse_id}")
        return True, "Warehouse deleted successfully"
    except Exception as e:
        log_error(f"Failed to delete warehouse {warehouse_id}", e)
        return False, f"Failed to delete warehouse: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_warehouse_count() -> int:
    """Get total number of warehouses."""
    conn = None
    try:
        conn = get_conn()
        count = conn.execute("SELECT COUNT(*) FROM warehouses").fetchone()[0]
        return count
    except Exception as e:
        log_error("Failed to count warehouses", e)
        return 0
    finally:
        if conn:
            conn.close()
