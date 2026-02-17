"""
Sample Data Generator for Video Recording Demo

This script helps you quickly populate the database with sample data
for demonstration purposes during video recording.

Usage:
    python generate_sample_data.py
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

# Import from project
from db import get_conn, init_db
from config import DB_PATH


def generate_sample_data():
    """Generate sample data for demo purposes."""
    
    print("[*] Generating sample data for video demo...\n")
    
    # Initialize database
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    
    # 1. Categories
    print("[1/7] Adding categories...")
    categories = [
        "Electronics",
        "Furniture",
        "Clothing",
        "Food & Beverages",
        "Office Supplies"
    ]
    
    for cat in categories:
        try:
            cur.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
        except sqlite3.IntegrityError:
            pass  # Already exists
    
    conn.commit()
    print(f"   [OK] Added {len(categories)} categories")
    
    # 2. Warehouses
    print("[2/7] Adding warehouses...")
    warehouses = [
        ("Main Store", "A"),
        ("Secondary Store", "B"),
        ("Downtown Branch", "C")
    ]
    
    for warehouse, rack in warehouses:
        try:
            cur.execute("INSERT INTO warehouses (name, rack_number) VALUES (?, ?)", (warehouse, rack))
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    print(f"   [OK] Added {len(warehouses)} warehouses")
    
    # 3. Suppliers
    print("[3/7] Adding suppliers...")
    suppliers = [
        ("TechSupply Inc.", "John Smith", "john.smith@techsupply.com", "+1-555-123-4567", "123 Tech Street, New York, NY 10001"),
        ("Furniture World Co.", "Sarah Johnson", "sarah.j@furnitureworld.com", "+1-555-987-6543", "456 Furniture Ave, Los Angeles, CA 90001"),
        ("Office Solutions Ltd.", "Michael Brown", "m.brown@officesolutions.com", "+1-555-555-1234", "789 Office Road, Chicago, IL 60601")
    ]
    
    for supplier in suppliers:
        try:
            cur.execute("""
                INSERT INTO suppliers (name, contact_person, email, phone, address) 
                VALUES (?, ?, ?, ?, ?)
            """, supplier)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    print(f"   [OK] Added {len(suppliers)} suppliers")
    
    # 4. Customers
    print("[4/7] Adding customers...")
    customers = [
        ("CUST001", "Robert Anderson", "+1-555-100-1234", "robert.a@email.com", "10 Main Street, New York, NY 10001"),
        ("CUST002", "Emily Davis", "+1-555-101-7654", "emily.d@email.com", "20 Second Avenue, Boston, MA 02101"),
        ("CUST003", "James Wilson", "+1-555-102-9876", "james.w@email.com", "30 Third Boulevard, Seattle, WA 98101"),
        ("CUST004", "Lisa Martinez", "+1-555-103-5555", "lisa.m@email.com", "40 Fourth Street, Miami, FL 33101"),
        ("CUST005", "David Thompson", "+1-555-104-4444", "david.t@email.com", "50 Fifth Road, Austin, TX 73301")
    ]
    
    for customer in customers:
        try:
            cur.execute("""
                INSERT INTO customers (customer_id, name, phone, email, address) 
                VALUES (?, ?, ?, ?, ?)
            """, customer)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    print(f"   [OK] Added {len(customers)} customers")
    
    # 5. Products
    print("[5/7] Adding products...")
    products = [
        # Electronics
        ("Laptop HP ProBook", 1, 1, "A1", None, "15.6 inch, i5, 8GB RAM", None, None, 25, 5, 12000, 15000, "ProBook 450", "LPTHP001", 1),
        ("Dell Monitor 24\"", 1, 1, "A2", None, "Full HD, IPS Panel", None, None, 40, 10, 3000, 4000, "P2419H", "MONDL001", 1),
        ("Wireless Mouse Logitech", 1, 1, "A3", None, "Optical, USB Receiver", None, None, 100, 20, 150, 250, "M185", "MOULOG01", 1),
        ("USB Flash Drive 32GB", 1, 1, "A4", None, "USB 3.0, High Speed", None, None, 200, 30, 80, 150, "USB32GB", "USBFLSH32", 1),
        
        # Furniture
        ("Office Desk Large", 2, 2, "B1", None, "Wood, 160x80cm", None, None, 15, 3, 2500, 4000, "DESK160", "DESKOF01", 2),
        ("Office Chair Ergonomic", 2, 2, "B2", None, "Adjustable, Lumbar Support", None, None, 30, 5, 800, 1500, "CHAIR-ERG", "CHAIROF01", 2),
        ("Meeting Table", 2, 2, "B3", None, "6 persons, Modern design", None, None, 8, 2, 3000, 5000, "TABLE-MT6", "TABLEMT01", 2),
        
        # Clothing
        ("T-Shirt Cotton - Blue", 3, 3, "C1", None, "Size: L, 100% Cotton", None, None, 150, 20, 50, 120, "TSHIRT-BL", "TSHIRT01", 3),
        ("Jeans Denim - Black", 3, 3, "C2", None, "Size: 32, Slim Fit", None, None, 100, 15, 200, 400, "JEANS-BK", "JEANS01", 3),
        
        # Food & Beverages
        ("Coffee Beans 1kg", 4, 1, "A5", None, "Premium Arabica", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"), 
         (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"), 50, 10, 150, 250, "COFFEE-1KG", "COFFEE01", 3),
        ("Mineral Water 1.5L (Pack of 12)", 4, 1, "A6", None, "Natural Spring Water", 
         (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"), 
         (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"), 80, 20, 30, 60, "WATER-12PK", "WATER01", 3),
        
        # Office Supplies
        ("A4 Paper Ream (500 sheets)", 5, 2, "B4", None, "80gsm, White", None, None, 100, 15, 40, 80, "A4-500", "PAPER01", 3),
        ("Pen Set (10 pcs)", 5, 2, "B5", None, "Blue ink, Ballpoint", None, None, 200, 30, 10, 25, "PEN-10SET", "PENSET01", 3),
        ("Notebook A5", 5, 2, "B6", None, "100 pages, Ruled", None, None, 150, 25, 15, 35, "NOTE-A5", "NOTEA501", 3)
    ]
    
    for product in products:
        try:
            cur.execute("""
                INSERT INTO products (
                    name, category_id, warehouse_id, rack_number, image_path, details,
                    production_date, expiry_date, quantity, low_stock_alert,
                    distributor_price, selling_price, model, sku, supplier_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, product)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    print(f"   [OK] Added {len(products)} products")
    
    # 6. Staff
    print("[6/7] Adding staff members...")
    staff = [
        ("John Anderson", "+1-555-100-1111", "john.a@store.com", "Manager", 5000, (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"), 35),
        ("Sarah Williams", "+1-555-101-2222", "sarah.w@store.com", "Sales Representative", 3000, (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d"), 28),
        ("Michael Davis", "+1-555-102-3333", "michael.d@store.com", "Warehouse Manager", 4000, (datetime.now() - timedelta(days=270)).strftime("%Y-%m-%d"), 32),
        ("Emily Johnson", "+1-555-103-4444", "emily.j@store.com", "Accountant", 3500, (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"), 30)
    ]
    
    for member in staff:
        try:
            cur.execute("""
                INSERT INTO staff (name, phone, email, role, salary, start_date, age) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, member)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    print(f"   [OK] Added {len(staff)} staff members")
    
    # 7. Sample Invoices (to demonstrate profit calculation)
    print("[7/8] Adding sample invoices...")
    
    invoice_data = [
        # (customer_id, days_ago, items: [(product_id, qty)], discount, paid_amount)
        (1, 10, [(1, 2), (3, 5)], 0, 31250),      # 2 laptops + 5 mice = 2*15000 + 5*250 = 31250 (full paid)
        (2, 7, [(2, 3), (4, 10)], 50, 10000),       # 3 monitors + 10 USB = 3*4000 + 10*150 = 13500 - 50 = 13450 (partial)
        (3, 5, [(5, 1), (6, 2)], 0, 7000),          # 1 desk + 2 chairs = 4000 + 2*1500 = 7000 (full paid)
        (4, 3, [(8, 10), (9, 5)], 100, 0),          # 10 tshirts + 5 jeans = 10*120 + 5*400 = 3200 - 100 = 3100 (unpaid)
        (5, 1, [(12, 20), (13, 30), (14, 10)], 0, 2000),  # 20 paper + 30 pens + 10 notebooks = 20*80 + 30*25 + 10*35 = 2700 (partial)
    ]
    
    invoices_created = 0
    for idx, (cust_id, days_ago, items, discount, paid) in enumerate(invoice_data):
        try:
            inv_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            created_at = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
            # Generate unique invoice number based on the invoice date
            inv_number = f"INV-{inv_date.replace('-', '')}-{idx+1:03d}"
            
            # Calculate totals
            subtotal = 0.0
            item_details = []
            for prod_id, qty in items:
                product = cur.execute(
                    "SELECT id, name, sku, selling_price, distributor_price FROM products WHERE id = ?",
                    (prod_id,)
                ).fetchone()
                if product:
                    unit_price = product[3]
                    cost_price = product[4] if product[4] else 0.0
                    total_price = unit_price * qty
                    subtotal += total_price
                    item_details.append((prod_id, product[1], product[2], qty, unit_price, total_price, cost_price))
            
            total = subtotal - discount
            if total < 0:
                total = 0
            if paid > total:
                paid = total
            due = total - paid
            
            if due <= 0:
                status = "paid"
            elif paid > 0:
                status = "partial"
            else:
                status = "unpaid"
            
            cur.execute("""
                INSERT INTO invoices(invoice_number, customer_id, invoice_date, subtotal, discount, 
                                     total, paid_amount, due_amount, payment_status, notes, created_at)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (inv_number, cust_id, inv_date, subtotal, discount, total, paid, due, status, "Sample invoice", created_at))
            
            invoice_id = cur.lastrowid
            
            for prod_id, pname, psku, qty, uprice, tprice, cprice in item_details:
                cur.execute("""
                    INSERT INTO invoice_items(invoice_id, product_id, product_name, sku, quantity, 
                                              unit_price, total_price, cost_price)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """, (invoice_id, prod_id, pname, psku, qty, uprice, tprice, cprice))
                
                # Reduce stock
                cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (qty, prod_id))
            
            invoices_created += 1
        except Exception as e:
            print(f"   [WARNING] Invoice error: {e}")
    
    conn.commit()
    print(f"   [OK] Added {invoices_created} invoices with items")
    
    # 8. Settings
    print("[8/8] Adding default settings...")
    settings = [
        ("store_name", "Premier Inventory Store"),
        ("currency_symbol", "$"),
        ("currency_code", "USD"),
        ("low_stock_threshold", "10")
    ]
    
    for key, value in settings:
        try:
            # Check if settings table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT
                )
            """)
            cur.execute("INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)", (key, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except Exception as e:
            print(f"   [WARNING] Settings error: {e}")
    
    conn.commit()
    print(f"   [OK] Added default settings")
    
    # Close connection
    conn.close()
    
    print("\n" + "="*50)
    print("[OK] Sample data generated successfully!")
    print("="*50)
    print("\nSummary:")
    print(f"   - {len(categories)} Categories")
    print(f"   - {len(warehouses)} Warehouses")
    print(f"   - {len(suppliers)} Suppliers")
    print(f"   - {len(customers)} Customers")
    print(f"   - {len(products)} Products")
    print(f"   - {len(staff)} Staff Members")
    print(f"   - {invoices_created} Invoices")
    print(f"   - Settings configured")
    print("\nYou're ready to record your video!")
    print("   Run: run.bat\n")


if __name__ == "__main__":
    try:
        generate_sample_data()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("Make sure you're in the project directory and all modules are available.")
