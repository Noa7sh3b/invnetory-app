"""
Customer Service - Handles all customer-related database operations.

This module provides CRUD operations for customers with
proper error handling and validation.
"""

from typing import List, Tuple, Optional
from db import get_conn
from datetime import datetime
from utils.logger import log_error, log_debug, log_db_operation


def add_customer(
    customer_id: str,
    name: str,
    phone: str = None,
    email: str = None,
    address: str = None
) -> Tuple[bool, str]:
    """
    Add a new customer.
    
    Args:
        customer_id: Custom customer ID
        name: Customer name (required)
        phone: Phone number
        email: Email address
        address: Customer address
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Customer name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "INSERT INTO customers(customer_id, name, phone, email, address) VALUES(?, ?, ?, ?, ?)",
            (
                customer_id.strip() if customer_id else None,
                name.strip(),
                phone.strip() if phone else None,
                email.strip() if email else None,
                address.strip() if address else None
            )
        )
        conn.commit()
        log_db_operation("INSERT", "customers", True, f"name={name.strip()}")
        return True, "Customer added successfully"
    except Exception as e:
        log_error("Failed to add customer", e)
        return False, f"Failed to add customer: {str(e)}"
    finally:
        if conn:
            conn.close()


def list_customers() -> List[Tuple]:
    """
    Get all customers.
    
    Returns:
        List of customer tuples
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute(
            "SELECT id, customer_id, name, phone, email, address FROM customers ORDER BY name"
        ).fetchall()
        log_debug(f"Listed {len(rows)} customers")
        return rows
    except Exception as e:
        log_error("Failed to list customers", e)
        return []
    finally:
        if conn:
            conn.close()


def get_customer(id: int) -> Optional[Tuple]:
    """
    Get a customer by ID.
    
    Args:
        id: Customer primary key ID
        
    Returns:
        Customer tuple or None
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute(
            "SELECT id, customer_id, name, phone, email, address FROM customers WHERE id=?",
            (id,)
        ).fetchone()
        return row
    except Exception as e:
        log_error(f"Failed to get customer {id}", e)
        return None
    finally:
        if conn:
            conn.close()


def update_customer(
    id: int,
    customer_id: str,
    name: str,
    phone: str = None,
    email: str = None,
    address: str = None
) -> Tuple[bool, str]:
    """
    Update a customer.
    
    Args:
        id: Customer primary key ID
        customer_id: Custom customer ID
        name: Customer name (required)
        phone: Phone number
        email: Email address
        address: Customer address
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Customer name is required"
    
    conn = None
    try:
        conn = get_conn()
        conn.execute(
            "UPDATE customers SET customer_id=?, name=?, phone=?, email=?, address=? WHERE id=?",
            (
                customer_id.strip() if customer_id else None,
                name.strip(),
                phone.strip() if phone else None,
                email.strip() if email else None,
                address.strip() if address else None,
                id
            )
        )
        conn.commit()
        log_db_operation("UPDATE", "customers", True, f"id={id}")
        return True, "Customer updated successfully"
    except Exception as e:
        log_error(f"Failed to update customer {id}", e)
        return False, f"Failed to update customer: {str(e)}"
    finally:
        if conn:
            conn.close()


def delete_customer(id: int) -> Tuple[bool, str]:
    """
    Delete a customer.
    
    Args:
        id: Customer primary key ID
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    conn = None
    try:
        conn = get_conn()
        # Check if customer has invoices
        invoice_count = conn.execute(
            "SELECT COUNT(*) FROM invoices WHERE customer_id = ?",
            (id,)
        ).fetchone()[0]
        
        if invoice_count > 0:
            return False, f"Cannot delete: Customer has {invoice_count} invoices"
        
        # Delete customer payments first
        conn.execute("DELETE FROM customer_payments WHERE customer_id=?", (id,))
        conn.execute("DELETE FROM customers WHERE id=?", (id,))
        conn.commit()
        log_db_operation("DELETE", "customers", True, f"id={id}")
        return True, "Customer deleted successfully"
    except Exception as e:
        log_error(f"Failed to delete customer {id}", e)
        return False, f"Failed to delete customer: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_customer_count(search: str = "") -> int:
    """
    Get total count of customers.
    
    Args:
        search: Optional search query
        
    Returns:
        Count of customers
    """
    conn = None
    try:
        conn = get_conn()
        if search:
            search_pattern = f"%{search}%"
            count = conn.execute(
                """SELECT COUNT(*) FROM customers 
                   WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR customer_id LIKE ?""",
                (search_pattern, search_pattern, search_pattern, search_pattern)
            ).fetchone()[0]
        else:
            count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        return count
    except Exception as e:
        log_error("Failed to count customers", e)
        return 0
    finally:
        if conn:
            conn.close()


def list_customers_paginated(offset: int, limit: int, search: str = "") -> List[Tuple]:
    """
    Get paginated list of customers.
    
    Args:
        offset: Number of records to skip
        limit: Maximum number of records to return
        search: Optional search query
        
    Returns:
        List of customer tuples
    """
    conn = None
    try:
        conn = get_conn()
        if search:
            search_pattern = f"%{search}%"
            rows = conn.execute(
                """SELECT id, customer_id, name, phone, email, address FROM customers 
                   WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR customer_id LIKE ? 
                   ORDER BY name LIMIT ? OFFSET ?""",
                (search_pattern, search_pattern, search_pattern, search_pattern, limit, offset)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT id, customer_id, name, phone, email, address FROM customers 
                   ORDER BY name LIMIT ? OFFSET ?""",
                (limit, offset)
            ).fetchall()
        return rows
    except Exception as e:
        log_error("Failed to list customers paginated", e)
        return []
    finally:
        if conn:
            conn.close()


# ============ Customer Payments Functions ============

def add_customer_payment(
    customer_id: int,
    total_amount: float,
    amount_paid: float,
    payment_date: str = None,
    notes: str = None
) -> Tuple[bool, str]:
    """
    Add a customer payment record.
    
    Args:
        customer_id: Customer ID
        total_amount: Total amount owed
        amount_paid: Amount paid
        payment_date: Payment date
        notes: Optional notes
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if total_amount <= 0:
        return False, "Total amount must be greater than zero"
    
    if amount_paid < 0:
        return False, "Amount paid cannot be negative"
    
    conn = None
    try:
        conn = get_conn()
        amount_due = total_amount - amount_paid
        payment_status = "paid" if amount_due <= 0 else "unpaid"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn.execute(
            """INSERT INTO customer_payments
               (customer_id, total_amount, amount_paid, amount_due, payment_status, payment_date, notes, created_at) 
               VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
            (customer_id, total_amount, amount_paid, max(0, amount_due), payment_status, 
             payment_date, notes.strip() if notes else None, created_at)
        )
        conn.commit()
        log_db_operation("INSERT", "customer_payments", True, f"customer_id={customer_id}")
        return True, "Payment record added successfully"
    except Exception as e:
        log_error("Failed to add customer payment", e)
        return False, f"Failed to add payment: {str(e)}"
    finally:
        if conn:
            conn.close()


def list_customer_payments() -> List[Tuple]:
    """Get all customer payment records."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT cp.id, c.customer_id, c.name, cp.payment_status, cp.total_amount, 
                   cp.amount_paid, cp.amount_due, cp.payment_date, cp.notes, cp.customer_id as cust_fk
            FROM customer_payments cp
            JOIN customers c ON cp.customer_id = c.id
            ORDER BY cp.created_at DESC
        """).fetchall()
        return rows
    except Exception as e:
        log_error("Failed to list customer payments", e)
        return []
    finally:
        if conn:
            conn.close()


def get_customer_payment(payment_id: int) -> Optional[Tuple]:
    """Get a specific customer payment record."""
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT cp.id, c.id, c.customer_id, c.name, c.email, cp.payment_status, 
                   cp.total_amount, cp.amount_paid, cp.amount_due, cp.payment_date, cp.notes
            FROM customer_payments cp
            JOIN customers c ON cp.customer_id = c.id
            WHERE cp.id = ?
        """, (payment_id,)).fetchone()
        return row
    except Exception as e:
        log_error(f"Failed to get customer payment {payment_id}", e)
        return None
    finally:
        if conn:
            conn.close()


def update_customer_payment(
    payment_id: int,
    total_amount: float,
    amount_paid: float,
    payment_date: str = None,
    notes: str = None
) -> Tuple[bool, str]:
    """Update a customer payment record."""
    if total_amount <= 0:
        return False, "Total amount must be greater than zero"
    
    conn = None
    try:
        conn = get_conn()
        amount_due = total_amount - amount_paid
        payment_status = "paid" if amount_due <= 0 else "unpaid"
        
        conn.execute(
            """UPDATE customer_payments 
               SET total_amount=?, amount_paid=?, amount_due=?, payment_status=?, payment_date=?, notes=? 
               WHERE id=?""",
            (total_amount, amount_paid, max(0, amount_due), payment_status, 
             payment_date, notes.strip() if notes else None, payment_id)
        )
        conn.commit()
        log_db_operation("UPDATE", "customer_payments", True, f"id={payment_id}")
        return True, "Payment record updated successfully"
    except Exception as e:
        log_error(f"Failed to update customer payment {payment_id}", e)
        return False, f"Failed to update payment: {str(e)}"
    finally:
        if conn:
            conn.close()


def delete_customer_payment(payment_id: int) -> Tuple[bool, str]:
    """Delete a customer payment record."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM customer_payments WHERE id=?", (payment_id,))
        conn.commit()
        log_db_operation("DELETE", "customer_payments", True, f"id={payment_id}")
        return True, "Payment record deleted successfully"
    except Exception as e:
        log_error(f"Failed to delete customer payment {payment_id}", e)
        return False, f"Failed to delete payment: {str(e)}"
    finally:
        if conn:
            conn.close()


def get_payment_count(search: str = "", status_filter: str = "") -> int:
    """Get total count of payment records with filters."""
    conn = None
    try:
        conn = get_conn()
        query = """
            SELECT COUNT(*) FROM customer_payments cp
            JOIN customers c ON cp.customer_id = c.id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (c.name LIKE ? OR c.customer_id LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        if status_filter:
            query += " AND cp.payment_status = ?"
            params.append(status_filter)
        
        count = conn.execute(query, params).fetchone()[0]
        return count
    except Exception as e:
        log_error("Failed to count payments", e)
        return 0
    finally:
        if conn:
            conn.close()


def list_payments_paginated(
    offset: int,
    limit: int,
    search: str = "",
    status_filter: str = ""
) -> List[Tuple]:
    """Get paginated list of payment records."""
    conn = None
    try:
        conn = get_conn()
        query = """
            SELECT cp.id, c.customer_id, c.name, cp.payment_status, cp.total_amount, cp.amount_paid, cp.amount_due
            FROM customer_payments cp
            JOIN customers c ON cp.customer_id = c.id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (c.name LIKE ? OR c.customer_id LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        if status_filter:
            query += " AND cp.payment_status = ?"
            params.append(status_filter)
        
        query += " ORDER BY cp.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        rows = conn.execute(query, params).fetchall()
        return rows
    except Exception as e:
        log_error("Failed to list payments paginated", e)
        return []
    finally:
        if conn:
            conn.close()
