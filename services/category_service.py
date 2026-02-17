"""
Category Service - Handles all category-related database operations.

This module provides CRUD operations for product categories with
proper error handling and validation.
"""

from typing import List, Tuple, Optional
from db import get_conn
from utils.logger import log_error, log_debug, log_db_operation


def add_category(name: str) -> Tuple[bool, str]:
    """
    Add a new category.
    
    Args:
        name: Category name
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Category name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)", (name.strip(),))
        conn.commit()
        log_db_operation("INSERT", "categories", True, f"name={name.strip()}")
        return True, "Category added successfully"
    except Exception as e:
        log_error("Failed to add category", e)
        return False, f"Failed to add category: {str(e)}"
    finally:
        if conn:
            conn.close()


def list_categories() -> List[Tuple]:
    """
    Get all categories.
    
    Returns:
        List of (id, name) tuples
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        log_debug(f"Listed {len(rows)} categories")
        return rows
    except Exception as e:
        log_error("Failed to list categories", e)
        return []
    finally:
        if conn:
            conn.close()


def get_category(category_id: int) -> Optional[Tuple]:
    """
    Get a category by ID.
    
    Args:
        category_id: Category ID
        
    Returns:
        Category tuple or None
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute(
            "SELECT id, name FROM categories WHERE id = ?", 
            (category_id,)
        ).fetchone()
        return row
    except Exception as e:
        log_error(f"Failed to get category {category_id}", e)
        return None
    finally:
        if conn:
            conn.close()


def update_category(category_id: int, name: str) -> Tuple[bool, str]:
    """
    Update a category.
    
    Args:
        category_id: Category ID
        name: New category name
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Category name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "UPDATE categories SET name = ? WHERE id = ?", 
            (name.strip(), category_id)
        )
        conn.commit()
        log_db_operation("UPDATE", "categories", True, f"id={category_id}")
        return True, "Category updated successfully"
    except Exception as e:
        log_error(f"Failed to update category {category_id}", e)
        return False, f"Failed to update category: {str(e)}"
    finally:
        if conn:
            conn.close()


def delete_category(category_id: int) -> Tuple[bool, str]:
    """
    Delete a category.
    
    Args:
        category_id: Category ID
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    conn = None
    try:
        conn = get_conn()
        # Check if category is in use
        product_count = conn.execute(
            "SELECT COUNT(*) FROM products WHERE category_id = ?",
            (category_id,)
        ).fetchone()[0]
        
        if product_count > 0:
            return False, f"Cannot delete: {product_count} products use this category"
        
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        log_db_operation("DELETE", "categories", True, f"id={category_id}")
        return True, "Category deleted successfully"
    except Exception as e:
        log_error(f"Failed to delete category {category_id}", e)
        return False, f"Failed to delete category: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_category_count() -> int:
    """Get total number of categories."""
    conn = None
    try:
        conn = get_conn()
        count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
        return count
    except Exception as e:
        log_error("Failed to count categories", e)
        return 0
    finally:
        if conn:
            conn.close()

