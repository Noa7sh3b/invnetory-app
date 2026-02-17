"""
Staff Service - Handles all staff-related database operations.

This module provides CRUD operations for staff members with
proper error handling and validation.
"""

from typing import List, Tuple, Optional
from db import get_conn
from utils.logger import log_error, log_debug, log_db_operation


def add_staff(
    name: str,
    phone: str = None,
    email: str = None,
    role: str = None,
    salary: float = 0,
    start_date: str = None,
    age: int = None
) -> Tuple[bool, str]:
    """
    Add a new staff member.
    
    Args:
        name: Staff member name (required)
        phone: Phone number
        email: Email address
        role: Job role/position
        salary: Monthly salary
        start_date: Employment start date
        age: Staff member age
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Staff name is required"
    
    if salary < 0:
        return False, "Salary cannot be negative"
    
    if age is not None and (age < 0 or age > 120):
        return False, "Invalid age value"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO staff(name, phone, email, role, salary, start_date, age) VALUES(?,?,?,?,?,?,?)",
            (
                name.strip(),
                phone.strip() if phone else None,
                email.strip() if email else None,
                role.strip() if role else None,
                salary,
                start_date,
                age
            )
        )
        conn.commit()
        log_db_operation("INSERT", "staff", True, f"name={name.strip()}")
        return True, "Staff member added successfully"
    except Exception as e:
        log_error("Failed to add staff member", e)
        return False, f"Failed to add staff member: {str(e)}"
    finally:
        if conn:
            conn.close()


def list_staff() -> List[Tuple]:
    """
    Get all staff members.
    
    Returns:
        List of staff tuples
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute(
            "SELECT id, name, phone, email, role, salary, start_date, age FROM staff ORDER BY name"
        ).fetchall()
        log_debug(f"Listed {len(rows)} staff members")
        return rows
    except Exception as e:
        log_error("Failed to list staff", e)
        return []
    finally:
        if conn:
            conn.close()


def get_staff(staff_id: int) -> Optional[Tuple]:
    """
    Get a staff member by ID.
    
    Args:
        staff_id: Staff ID
        
    Returns:
        Staff tuple or None
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute(
            "SELECT id, name, phone, email, role, salary, start_date, age FROM staff WHERE id=?",
            (staff_id,)
        ).fetchone()
        return row
    except Exception as e:
        log_error(f"Failed to get staff {staff_id}", e)
        return None
    finally:
        if conn:
            conn.close()


def update_staff(
    staff_id: int,
    name: str,
    phone: str = None,
    email: str = None,
    role: str = None,
    salary: float = 0,
    start_date: str = None,
    age: int = None
) -> Tuple[bool, str]:
    """
    Update a staff member.
    
    Args:
        staff_id: Staff ID to update
        name: Staff member name (required)
        phone: Phone number
        email: Email address
        role: Job role/position
        salary: Monthly salary
        start_date: Employment start date
        age: Staff member age
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Staff name is required"
    
    if salary < 0:
        return False, "Salary cannot be negative"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "UPDATE staff SET name=?, phone=?, email=?, role=?, salary=?, start_date=?, age=? WHERE id=?",
            (
                name.strip(),
                phone.strip() if phone else None,
                email.strip() if email else None,
                role.strip() if role else None,
                salary,
                start_date,
                age,
                staff_id
            )
        )
        conn.commit()
        log_db_operation("UPDATE", "staff", True, f"id={staff_id}")
        return True, "Staff member updated successfully"
    except Exception as e:
        log_error(f"Failed to update staff {staff_id}", e)
        return False, f"Failed to update staff member: {str(e)}"
    finally:
        if conn:
            conn.close()


def delete_staff(staff_id: int) -> Tuple[bool, str]:
    """
    Delete a staff member.
    
    Args:
        staff_id: Staff ID to delete
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM staff WHERE id=?", (staff_id,))
        conn.commit()
        log_db_operation("DELETE", "staff", True, f"id={staff_id}")
        return True, "Staff member deleted successfully"
    except Exception as e:
        log_error(f"Failed to delete staff {staff_id}", e)
        return False, f"Failed to delete staff member: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_staff_count(search: str = "") -> int:
    """
    Get total count of staff members.
    
    Args:
        search: Optional search query
        
    Returns:
        Count of staff members
    """
    conn = None
    try:
        conn = get_conn()
        if search:
            search_pattern = f"%{search}%"
            count = conn.execute(
                "SELECT COUNT(*) FROM staff WHERE name LIKE ? OR role LIKE ?",
                (search_pattern, search_pattern)
            ).fetchone()[0]
        else:
            count = conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
        return count
    except Exception as e:
        log_error("Failed to count staff", e)
        return 0
    finally:
        if conn:
            conn.close()


def list_staff_paginated(offset: int, limit: int, search: str = "") -> List[Tuple]:
    """
    Get paginated list of staff members.
    
    Args:
        offset: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search query
        
    Returns:
        List of staff tuples
    """
    conn = None
    try:
        conn = get_conn()
        if search:
            search_pattern = f"%{search}%"
            rows = conn.execute(
                """SELECT id, name, phone, email, role, salary, start_date, age 
                   FROM staff 
                   WHERE name LIKE ? OR role LIKE ? 
                   ORDER BY name LIMIT ? OFFSET ?""",
                (search_pattern, search_pattern, limit, offset)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT id, name, phone, email, role, salary, start_date, age 
                   FROM staff 
                   ORDER BY name LIMIT ? OFFSET ?""",
                (limit, offset)
            ).fetchall()
        return rows
    except Exception as e:
        log_error("Failed to list staff paginated", e)
        return []
    finally:
        if conn:
            conn.close()
