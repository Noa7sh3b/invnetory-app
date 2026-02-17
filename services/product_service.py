"""
Product Service – CRUD and query operations for the products table.

Every public function opens (and closes) its own database connection.
"""

from db import get_conn


def add_product(data: dict):
    """Insert a new product row from a dictionary of column values."""
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO products(
            name, category_id, warehouse_id, rack_number, image_path, details,
            production_date, expiry_date, quantity, low_stock_alert,
            distributor_price, selling_price, model, sku, supplier_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["category_id"],
            data["warehouse_id"],
            data["rack_number"],
            data["image_path"],
            data["details"],
            data["production_date"],
            data["expiry_date"],
            data["quantity"],
            data["low_stock_alert"],
            data["distributor_price"],
            data["selling_price"],
            data["model"],
            data["sku"],
            data["supplier_id"],
        ),
    )
    conn.commit()
    conn.close()


def update_product(product_id: int, data: dict):
    """Update all columns of an existing product."""
    conn = get_conn()
    conn.execute(
        """
        UPDATE products
        SET name=?, category_id=?, warehouse_id=?, rack_number=?, image_path=?,
            details=?, production_date=?, expiry_date=?, quantity=?,
            low_stock_alert=?, distributor_price=?, selling_price=?,
            model=?, sku=?, supplier_id=?
        WHERE id=?
        """,
        (
            data["name"],
            data["category_id"],
            data["warehouse_id"],
            data["rack_number"],
            data["image_path"],
            data["details"],
            data["production_date"],
            data["expiry_date"],
            data["quantity"],
            data["low_stock_alert"],
            data["distributor_price"],
            data["selling_price"],
            data["model"],
            data["sku"],
            data["supplier_id"],
            product_id,
        ),
    )
    conn.commit()
    conn.close()


def delete_product(product_id: int):
    """Permanently delete a product by its primary key."""
    conn = get_conn()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def get_product_count(search: str = ""):
    """Return total product count, optionally filtered by a search term."""
    conn = get_conn()
    if search:
        search_pattern = f"%{search}%"
        total = conn.execute(
            "SELECT COUNT(*) FROM products WHERE name LIKE ? OR sku LIKE ? OR model LIKE ?",
            (search_pattern, search_pattern, search_pattern),
        ).fetchone()[0]
    else:
        total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    conn.close()
    return total


def list_products(limit: int, offset: int, search: str = ""):
    """Return a paginated list of products with joined category/warehouse/supplier names."""
    conn = get_conn()
    if search:
        search_pattern = f"%{search}%"
        rows = conn.execute(
            """
            SELECT p.id, p.name, p.quantity, p.low_stock_alert,
                   p.distributor_price, p.selling_price, p.image_path,
                   c.name, w.name, s.name, p.rack_number, p.details,
                   p.production_date, p.expiry_date, p.model, p.sku
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN warehouses w ON p.warehouse_id = w.id
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            WHERE p.name LIKE ? OR p.sku LIKE ? OR p.model LIKE ?
            ORDER BY p.id DESC
            LIMIT ? OFFSET ?
            """,
            (search_pattern, search_pattern, search_pattern, limit, offset),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT p.id, p.name, p.quantity, p.low_stock_alert,
                   p.distributor_price, p.selling_price, p.image_path,
                   c.name, w.name, s.name, p.rack_number, p.details,
                   p.production_date, p.expiry_date, p.model, p.sku
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN warehouses w ON p.warehouse_id = w.id
            LEFT JOIN suppliers s ON p.supplier_id = s.id
            ORDER BY p.id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
    conn.close()
    return rows


def get_product_by_id(product_id: int):
    """Fetch a single product's full row by primary key."""
    conn = get_conn()
    row = conn.execute(
        """
        SELECT id, name, category_id, warehouse_id, rack_number, image_path,
               details, production_date, expiry_date, quantity, low_stock_alert,
               distributor_price, selling_price, model, sku, supplier_id
        FROM products WHERE id=?
        """,
        (product_id,),
    ).fetchone()
    conn.close()
    return row


def list_products_for_export(limit: int, offset: int):
    """Return products as a list of dicts suitable for Excel/PDF export."""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT p.name AS name,
               c.name AS category,
               w.name AS warehouse,
               p.rack_number AS rack_number,
               p.quantity AS quantity,
               p.low_stock_alert AS low_stock_alert,
               p.distributor_price AS distributor_price,
               p.selling_price AS selling_price,
               s.name AS supplier,
               p.model AS model,
               p.sku AS sku
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN warehouses w ON p.warehouse_id = w.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        ORDER BY p.id DESC
        LIMIT ? OFFSET ?
        """,
        (limit, offset),
    ).fetchall()
    conn.close()
    columns = [
        "name",
        "category",
        "warehouse",
        "rack_number",
        "quantity",
        "low_stock_alert",
        "distributor_price",
        "selling_price",
        "supplier",
        "model",
        "sku",
    ]
    return [dict(zip(columns, row)) for row in rows]


def list_low_stock_products():
    """Get products where quantity <= low_stock_alert (based on each product's own alert level)"""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT p.id, p.name, p.quantity, p.low_stock_alert,
               p.distributor_price, p.selling_price, p.image_path,
               c.name, w.name, s.name, p.rack_number
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN warehouses w ON p.warehouse_id = w.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.low_stock_alert > 0 AND p.quantity <= p.low_stock_alert
        ORDER BY p.quantity ASC
        """
    ).fetchall()
    conn.close()
    return rows


def list_expired_products():
    """Get products where expiry_date < today"""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT p.id, p.name, p.quantity, p.expiry_date,
               p.distributor_price, p.selling_price, p.image_path,
               c.name, w.name, s.name, p.rack_number
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN warehouses w ON p.warehouse_id = w.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.expiry_date IS NOT NULL AND p.expiry_date < date('now')
        ORDER BY p.expiry_date ASC
        """
    ).fetchall()
    conn.close()
    return rows


def list_dead_stock_products(days: int = 30):
    """Get products that haven't been sold in the last X days (no invoice items)"""
    conn = get_conn()
    # Products with no sales in the last X days or never sold
    rows = conn.execute(
        """
        SELECT p.id, p.name, p.quantity, p.low_stock_alert,
               p.distributor_price, p.selling_price, p.image_path,
               c.name, w.name, s.name, p.rack_number
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN warehouses w ON p.warehouse_id = w.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.id NOT IN (
            SELECT DISTINCT ii.product_id 
            FROM invoice_items ii
            JOIN invoices i ON ii.invoice_id = i.id
            WHERE date(i.created_at) >= date('now', '-' || ? || ' days')
        )
        ORDER BY p.name ASC
        """,
        (days,),
    ).fetchall()
    conn.close()
    return rows


def mark_as_dead_stock(product_id: int):
    """Mark a product as dead stock (optional - can add a flag column later)"""
    pass  # For now, dead stock is calculated dynamically


def get_all_products_simple():
    """Get all products for dropdown selection"""
    conn = get_conn()
    rows = conn.execute("SELECT id, name FROM products ORDER BY name").fetchall()
    conn.close()
    return rows
