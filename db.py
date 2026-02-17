"""
Database Module - Handles database connection and initialization.

This module provides database connection management and schema initialization
for the inventory management system.
"""

import sqlite3
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR, IMAGE_DIR


def get_conn():
    """
    Get a database connection.
    
    Creates necessary directories if they don't exist.
    
    Returns:
        sqlite3.Connection: Database connection object
        
    Note:
        Remember to close the connection after use, or use get_db_connection()
        context manager for automatic cleanup.
    """
    DATA_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    
    Automatically handles connection cleanup and commits/rollbacks.
    
    Usage:
        with get_db_connection() as conn:
            conn.execute("SELECT * FROM products")
            
    Yields:
        sqlite3.Connection: Database connection object
    """
    DATA_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        rack_number TEXT
    )
    """)
    # Add rack_number column if not exists (for existing databases)
    try:
        cur.execute("ALTER TABLE warehouses ADD COLUMN rack_number TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    cur.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        address TEXT
    )
    """)
    # Add new columns if not exists (for existing databases)
    for col in ["contact_person", "email", "phone", "address"]:
        try:
            cur.execute(f"ALTER TABLE suppliers ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address TEXT
    )
    """)
    # Add new columns if not exists (for existing databases)
    for col in ["phone", "email", "address", "customer_id"]:
        try:
            cur.execute(f"ALTER TABLE customers ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Customer payments table for tracking paid/unpaid status
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        total_amount REAL NOT NULL DEFAULT 0,
        amount_paid REAL NOT NULL DEFAULT 0,
        amount_due REAL NOT NULL DEFAULT 0,
        payment_status TEXT DEFAULT 'unpaid',
        payment_date TEXT,
        notes TEXT,
        created_at TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER,
        warehouse_id INTEGER,
        rack_number TEXT,
        image_path TEXT,
        details TEXT,
        production_date TEXT,
        expiry_date TEXT,
        quantity INTEGER NOT NULL DEFAULT 0,
        low_stock_alert INTEGER NOT NULL DEFAULT 0,
        distributor_price REAL NOT NULL DEFAULT 0,
        selling_price REAL NOT NULL DEFAULT 0,
        model TEXT,
        sku TEXT,
        supplier_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id),
        FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
        FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE,
        customer_id INTEGER,
        invoice_date TEXT NOT NULL,
        subtotal REAL NOT NULL DEFAULT 0,
        discount REAL NOT NULL DEFAULT 0,
        total REAL NOT NULL DEFAULT 0,
        paid_amount REAL NOT NULL DEFAULT 0,
        due_amount REAL NOT NULL DEFAULT 0,
        payment_status TEXT DEFAULT 'unpaid',
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)
    # Add new columns if not exists (for existing databases)
    for col, col_type in [("invoice_number", "TEXT"), ("invoice_date", "TEXT"), ("subtotal", "REAL"), 
                          ("discount", "REAL"), ("paid_amount", "REAL"), ("due_amount", "REAL"), 
                          ("payment_status", "TEXT"), ("notes", "TEXT")]:
        try:
            cur.execute(f"ALTER TABLE invoices ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        product_id INTEGER,
        product_name TEXT,
        sku TEXT,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY(invoice_id) REFERENCES invoices(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)
    # Add new columns if not exists (for existing databases)
    for col, col_type in [("product_name", "TEXT"), ("sku", "TEXT"), ("unit_price", "REAL"), ("total_price", "REAL"), ("cost_price", "REAL DEFAULT 0")]:
        try:
            cur.execute(f"ALTER TABLE invoice_items ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        role TEXT,
        salary REAL DEFAULT 0,
        start_date TEXT,
        age INTEGER
    )
    """)
    # Add new columns if not exists (for existing databases)
    for col in [("start_date", "TEXT"), ("age", "INTEGER")]:
        try:
            cur.execute(f"ALTER TABLE staff ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    conn.commit()
    conn.close()
