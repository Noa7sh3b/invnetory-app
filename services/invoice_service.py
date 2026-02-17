"""
Invoice Service – Comprehensive invoice and billing operations.

Handles invoice creation, payment tracking, stock updates, and dashboard statistics.
Includes invoice number generation, validation, and export functionality.
"""

from db import get_conn
from datetime import datetime


def generate_invoice_number():
    """Generate unique invoice number like INV-20260123-001"""
    conn = get_conn()
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"INV-{today}-"
    
    # Get the latest invoice number for today
    row = conn.execute(
        "SELECT invoice_number FROM invoices WHERE invoice_number LIKE ? ORDER BY id DESC LIMIT 1",
        (f"{prefix}%",)
    ).fetchone()
    
    if row:
        # Extract the sequence number and increment
        try:
            seq = int(row[0].split("-")[-1]) + 1
        except (ValueError, IndexError, AttributeError):
            seq = 1
    else:
        seq = 1
    
    conn.close()
    return f"{prefix}{seq:03d}"


def get_product_for_invoice(product_id: int):
    """Get product details for invoice item"""
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, sku, selling_price, quantity FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()
    conn.close()
    return row


def list_products_for_invoice():
    """Get all products with stock > 0 for dropdown"""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, sku, selling_price, quantity FROM products WHERE quantity > 0 ORDER BY name"
    ).fetchall()
    conn.close()
    return rows


def validate_quantity(product_id: int, requested_qty: int):
    """Check if requested quantity is available in stock"""
    conn = get_conn()
    row = conn.execute("SELECT quantity FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if not row:
        return False, "Product not found"
    if requested_qty <= 0:
        return False, "Quantity must be greater than 0"
    if requested_qty > row[0]:
        return False, f"Not enough stock. Available: {row[0]}"
    return True, "OK"


def create_invoice(customer_id: int, invoice_date: str, items: list, discount: float, paid_amount: float, notes: str = None):
    """
    Create a new invoice with items
    items: list of dicts with {product_id, quantity}
    Returns: (success: bool, message: str, invoice_id: int or None)
    """
    conn = get_conn()
    
    # Validate all items first
    for item in items:
        product = conn.execute(
            "SELECT id, name, sku, selling_price, quantity FROM products WHERE id = ?",
            (item["product_id"],)
        ).fetchone()
        
        if not product:
            conn.close()
            return False, f"Product not found", None
        
        if item["quantity"] <= 0:
            conn.close()
            return False, f"Quantity must be greater than 0 for {product[1]}", None
        
        if item["quantity"] > product[4]:
            conn.close()
            return False, f"Not enough stock for {product[1]}. Available: {product[4]}", None
    
    # Calculate subtotal
    subtotal = 0.0
    item_details = []
    for item in items:
        product = conn.execute(
            "SELECT id, name, sku, selling_price, distributor_price FROM products WHERE id = ?",
            (item["product_id"],)
        ).fetchone()
        unit_price = product[3]
        cost_price = product[4] if product[4] else 0.0  # distributor_price (supplier/cost price)
        total_price = unit_price * item["quantity"]
        subtotal += total_price
        item_details.append({
            "product_id": product[0],
            "product_name": product[1],
            "sku": product[2],
            "quantity": item["quantity"],
            "unit_price": unit_price,
            "cost_price": cost_price,
            "total_price": total_price
        })
    
    # Calculate totals
    total = subtotal - discount
    if total < 0:
        total = 0
    
    # Validate paid amount
    if paid_amount < 0:
        paid_amount = 0
    if paid_amount > total:
        conn.close()
        return False, f"Paid amount ({paid_amount}) cannot exceed total ({total})", None
    
    due_amount = total - paid_amount
    
    # Determine payment status
    if due_amount <= 0:
        payment_status = "paid"
    elif paid_amount > 0:
        payment_status = "partial"
    else:
        payment_status = "unpaid"
    
    # Generate invoice number
    invoice_number = generate_invoice_number()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert invoice
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO invoices(invoice_number, customer_id, invoice_date, subtotal, discount, total, paid_amount, due_amount, payment_status, notes, created_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (invoice_number, customer_id, invoice_date, subtotal, discount, total, paid_amount, due_amount, payment_status, notes, created_at))
    
    invoice_id = cur.lastrowid
    
    # Insert invoice items and update stock
    for item in item_details:
        cur.execute("""
            INSERT INTO invoice_items(invoice_id, product_id, product_name, sku, quantity, unit_price, total_price, cost_price)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (invoice_id, item["product_id"], item["product_name"], item["sku"], item["quantity"], item["unit_price"], item["total_price"], item["cost_price"]))
        
        # Reduce stock
        cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (item["quantity"], item["product_id"]))
    
    conn.commit()
    conn.close()
    
    return True, f"Invoice {invoice_number} created successfully", invoice_id


def get_invoice(invoice_id: int):
    """Get invoice with customer details"""
    conn = get_conn()
    row = conn.execute("""
        SELECT i.id, i.invoice_number, i.customer_id, c.name, i.invoice_date, 
               i.subtotal, i.discount, i.total, i.paid_amount, i.due_amount,
               i.payment_status, i.notes, i.created_at
        FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        WHERE i.id = ?
    """, (invoice_id,)).fetchone()
    conn.close()
    return row


def get_invoice_items(invoice_id: int):
    """Get all items for an invoice"""
    conn = get_conn()
    rows = conn.execute("""
        SELECT id, product_id, product_name, sku, quantity, 
               COALESCE(unit_price, price) as unit_price, 
               COALESCE(total_price, price * quantity) as total_price
        FROM invoice_items
        WHERE invoice_id = ?
    """, (invoice_id,)).fetchall()
    conn.close()
    return rows


def update_invoice_payment(invoice_id: int, paid_amount: float, notes: str = None):
    """Update payment for an existing invoice"""
    conn = get_conn()
    
    # Get current invoice
    invoice = conn.execute("SELECT total, paid_amount FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    if not invoice:
        conn.close()
        return False, "Invoice not found"
    
    total = invoice[0]
    
    if paid_amount < 0:
        paid_amount = 0
    if paid_amount > total:
        conn.close()
        return False, f"Paid amount ({paid_amount}) cannot exceed total ({total})"
    
    due_amount = total - paid_amount
    
    # Determine payment status
    if due_amount <= 0:
        payment_status = "paid"
    elif paid_amount > 0:
        payment_status = "partial"
    else:
        payment_status = "unpaid"
    
    conn.execute("""
        UPDATE invoices SET paid_amount = ?, due_amount = ?, payment_status = ?, notes = ?
        WHERE id = ?
    """, (paid_amount, due_amount, payment_status, notes, invoice_id))
    
    conn.commit()
    conn.close()
    return True, "Invoice updated successfully"


def delete_invoice(invoice_id: int):
    """Delete invoice and restore stock"""
    conn = get_conn()
    
    # Get invoice items to restore stock
    items = conn.execute(
        "SELECT product_id, quantity FROM invoice_items WHERE invoice_id = ?",
        (invoice_id,)
    ).fetchall()
    
    # Restore stock
    for item in items:
        conn.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (item[1], item[0]))
    
    # Delete invoice items
    conn.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    
    # Delete invoice
    conn.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
    
    conn.commit()
    conn.close()
    return True, "Invoice deleted and stock restored"


def get_invoice_count(search: str = "", status_filter: str = ""):
    """Get total count of invoices with filters"""
    conn = get_conn()
    query = """
        SELECT COUNT(*) FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (c.name LIKE ? OR i.invoice_number LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    if status_filter:
        query += " AND i.payment_status = ?"
        params.append(status_filter)
    
    count = conn.execute(query, params).fetchone()[0]
    conn.close()
    return count


def list_invoices_paginated(offset: int, limit: int, search: str = "", status_filter: str = ""):
    """List invoices with pagination and filters"""
    conn = get_conn()
    query = """
        SELECT i.id, i.invoice_number, c.name, i.invoice_date, 
               (SELECT COUNT(*) FROM invoice_items WHERE invoice_id = i.id) as item_count,
               (SELECT GROUP_CONCAT(product_name, ', ') FROM invoice_items WHERE invoice_id = i.id LIMIT 1) as first_product,
               i.total, i.paid_amount, i.due_amount, i.payment_status
        FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (c.name LIKE ? OR i.invoice_number LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    if status_filter:
        query += " AND i.payment_status = ?"
        params.append(status_filter)
    
    query += " ORDER BY i.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


def list_invoices_for_export(search: str = "", status_filter: str = ""):
    """Get all invoices for export"""
    conn = get_conn()
    query = """
        SELECT i.invoice_number, c.name as customer_name, i.invoice_date,
               i.subtotal, i.discount, i.total, i.paid_amount, i.due_amount, i.payment_status
        FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += " AND (c.name LIKE ? OR i.invoice_number LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    if status_filter:
        query += " AND i.payment_status = ?"
        params.append(status_filter)
    
    query += " ORDER BY i.id DESC"
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    columns = ["invoice_number", "customer_name", "invoice_date", "subtotal", "discount", "total", "paid_amount", "due_amount", "payment_status"]
    return [dict(zip(columns, row)) for row in rows]


def get_invoice_for_print(invoice_id: int):
    """Get complete invoice data for printing"""
    invoice = get_invoice(invoice_id)
    items = get_invoice_items(invoice_id)
    return invoice, items


def get_dashboard_stats():
    """Get dashboard statistics for invoices, including profit calculation.
    
    Profit = Total Selling Revenue - Total Cost (supplier/distributor price).
    For invoice items that have cost_price stored, we use it directly.
    For older items without cost_price, we fall back to the product's current distributor_price.
    """
    conn = get_conn()
    # Total sales = total quantity of products sold (not money)
    total_sales = conn.execute("SELECT COALESCE(SUM(quantity),0) FROM invoice_items").fetchone()[0]
    # Total sales amount (money) = sum of invoice totals (selling price)
    total_sales_amount = conn.execute("SELECT COALESCE(SUM(total),0) FROM invoices").fetchone()[0]
    total_receivable = conn.execute("SELECT COALESCE(SUM(due_amount),0) FROM invoices WHERE payment_status != 'paid'").fetchone()[0]
    total_received = conn.execute("SELECT COALESCE(SUM(paid_amount),0) FROM invoices").fetchone()[0]
    # --- Profit Calculation ---
    # Total selling revenue from all invoice items
    total_selling = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) FROM invoice_items"
    ).fetchone()[0]

    # Total cost: use cost_price if available, otherwise fall back to product's distributor_price
    total_cost = conn.execute("""
        SELECT COALESCE(SUM(
            CASE 
                WHEN ii.cost_price IS NOT NULL AND ii.cost_price > 0 
                    THEN ii.cost_price * ii.quantity
                ELSE COALESCE(p.distributor_price, 0) * ii.quantity
            END
        ), 0)
        FROM invoice_items ii
        LEFT JOIN products p ON ii.product_id = p.id
    """).fetchone()[0]

    total_profit = total_selling - total_cost

    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_invoice = conn.execute("SELECT COUNT(*) FROM invoices").fetchone()[0]
    total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    total_suppliers = conn.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
    total_items_in_stock = conn.execute("SELECT COALESCE(SUM(quantity),0) FROM products").fetchone()[0]
    total_items_in_category = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    conn.close()
    return {
        "total_sales": total_sales,
        "total_receivable": total_receivable,
        "total_received": total_received,
        "total_products": total_products,
        "total_invoice": total_invoice,
        "sales_total_price_saling": total_sales_amount,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_items_in_stock": total_items_in_stock,
        "total_items_in_category": total_items_in_category,
        "total_selling": total_selling,
        "total_cost": total_cost,
        "total_profit": total_profit,
    }


def get_last_invoices(limit=10):
    """Get last invoices for dashboard"""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT i.id, c.name, i.total, i.paid_amount, i.due_amount, i.invoice_date
        FROM invoices i
        LEFT JOIN customers c ON i.customer_id = c.id
        ORDER BY i.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return rows
