"""
Supplier Service – CRUD and query operations for the suppliers table.

Each function manages its own database connection lifecycle.
"""

from db import get_conn


def add_supplier(name: str, contact_person: str = "", email: str = "", phone: str = "", address: str = ""):
    """Insert a new supplier record."""
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO suppliers(name, contact_person, email, phone, address) VALUES(?, ?, ?, ?, ?)",
        (name.strip(), contact_person.strip(), email.strip(), phone.strip(), address.strip())
    )
    conn.commit()
    conn.close()


def list_suppliers():
    """Return all suppliers ordered by name."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, contact_person, email, phone, address FROM suppliers ORDER BY name"
    ).fetchall()
    conn.close()
    return rows


def get_supplier(supplier_id: int):
    """Fetch a single supplier by primary key."""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, contact_person, email, phone, address FROM suppliers WHERE id=?",
        (supplier_id,)
    ).fetchone()
    conn.close()
    return row


def update_supplier(supplier_id: int, name: str, contact_person: str = "", email: str = "", phone: str = "", address: str = ""):
    """Update an existing supplier's fields."""
    conn = get_conn()
    conn.execute(
        "UPDATE suppliers SET name=?, contact_person=?, email=?, phone=?, address=? WHERE id=?",
        (name.strip(), contact_person.strip(), email.strip(), phone.strip(), address.strip(), supplier_id)
    )
    conn.commit()
    conn.close()


def delete_supplier(supplier_id: int):
    """Permanently delete a supplier by primary key."""
    conn = get_conn()
    conn.execute("DELETE FROM suppliers WHERE id=?", (supplier_id,))
    conn.commit()
    conn.close()


def get_supplier_count(search: str = ""):
    """Return supplier count, optionally filtered by a search term."""
    conn = get_conn()
    if search:
        count = conn.execute(
            "SELECT COUNT(*) FROM suppliers WHERE name LIKE ?",
            (f"%{search}%",)
        ).fetchone()[0]
    else:
        count = conn.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
    conn.close()
    return count


def list_suppliers_paginated(offset: int, limit: int, search: str = ""):
    """Return a paginated slice of suppliers, with optional search."""
    conn = get_conn()
    if search:
        rows = conn.execute(
            "SELECT id, name, contact_person, email, phone, address FROM suppliers WHERE name LIKE ? ORDER BY name LIMIT ? OFFSET ?",
            (f"%{search}%", limit, offset)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, contact_person, email, phone, address FROM suppliers ORDER BY name LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
    conn.close()
    return rows
