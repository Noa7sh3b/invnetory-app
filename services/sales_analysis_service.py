"""
Sales Analysis Service - Comprehensive sales data analysis and reporting.

Provides functions for analyzing product sales performance, profit calculation,
and generating data for visualizations and reports.
"""

from db import get_conn
from datetime import datetime


def get_top_selling_products(limit=1):
    """
    Get top selling products by quantity sold.
    Returns: list of tuples (product_id, product_name, total_quantity_sold, total_revenue, total_profit)
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            ii.product_id,
            ii.product_name,
            SUM(ii.quantity) as total_quantity_sold,
            SUM(ii.total_price) as total_revenue,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit
        FROM invoice_items ii
        GROUP BY ii.product_id, ii.product_name
        ORDER BY total_quantity_sold DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_lowest_selling_products(limit=1):
    """
    Get lowest selling products by quantity sold.
    Returns: list of tuples (product_id, product_name, total_quantity_sold, total_revenue, total_profit)
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            ii.product_id,
            ii.product_name,
            SUM(ii.quantity) as total_quantity_sold,
            SUM(ii.total_price) as total_revenue,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit
        FROM invoice_items ii
        GROUP BY ii.product_id, ii.product_name
        ORDER BY total_quantity_sold ASC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_product_sales_summary(limit=10):
    """
    Get detailed sales summary for all products.
    Returns: list of tuples with complete product sales information
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            ii.product_id,
            ii.product_name,
            ii.sku,
            SUM(ii.quantity) as total_quantity_sold,
            SUM(ii.total_price) as total_revenue,
            AVG(ii.unit_price) as avg_selling_price,
            SUM(COALESCE(ii.cost_price, 0) * ii.quantity) as total_cost,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit,
            COUNT(DISTINCT ii.invoice_id) as number_of_sales
        FROM invoice_items ii
        GROUP BY ii.product_id, ii.product_name, ii.sku
        ORDER BY total_quantity_sold DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_sales_by_period(start_date=None, end_date=None):
    """
    Get sales statistics for a specific period.
    If dates are None, returns all-time statistics.
    """
    conn = get_conn()
    
    query = """
        SELECT 
            COUNT(DISTINCT i.id) as total_invoices,
            SUM(ii.quantity) as total_items_sold,
            SUM(ii.total_price) as total_revenue,
            SUM(COALESCE(ii.cost_price, 0) * ii.quantity) as total_cost,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit
        FROM invoices i
        JOIN invoice_items ii ON i.id = ii.invoice_id
        WHERE 1=1
    """
    
    params = []
    if start_date:
        query += " AND i.invoice_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND i.invoice_date <= ?"
        params.append(end_date)
    
    row = conn.execute(query, params).fetchone()
    conn.close()
    
    return {
        "total_invoices": row[0] or 0,
        "total_items_sold": row[1] or 0,
        "total_revenue": row[2] or 0.0,
        "total_cost": row[3] or 0.0,
        "total_profit": row[4] or 0.0,
        "profit_margin": (row[4] / row[2] * 100) if row[2] and row[2] > 0 else 0.0
    }


def get_sales_trend_by_month(months=6):
    """
    Get sales trend for the last N months.
    Returns monthly data for charts.
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            strftime('%Y-%m', i.invoice_date) as month,
            SUM(ii.quantity) as total_quantity,
            SUM(ii.total_price) as total_revenue,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit
        FROM invoices i
        JOIN invoice_items ii ON i.id = ii.invoice_id
        WHERE i.invoice_date >= date('now', '-' || ? || ' months')
        GROUP BY month
        ORDER BY month ASC
    """, (months,)).fetchall()
    conn.close()
    return rows


def get_customer_sales_ranking(limit=10):
    """
    Get top customers by total purchase amount.
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            c.id,
            c.name,
            COUNT(DISTINCT i.id) as total_invoices,
            SUM(i.total) as total_purchase_amount,
            SUM(i.paid_amount) as total_paid,
            SUM(i.due_amount) as total_due
        FROM customers c
        JOIN invoices i ON c.id = i.customer_id
        GROUP BY c.id, c.name
        ORDER BY total_purchase_amount DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_category_sales_performance():
    """
    Get sales performance by product category.
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            cat.name as category_name,
            COUNT(DISTINCT p.id) as products_count,
            COALESCE(SUM(ii.quantity), 0) as total_quantity_sold,
            COALESCE(SUM(ii.total_price), 0) as total_revenue,
            COALESCE(SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)), 0) as total_profit
        FROM categories cat
        LEFT JOIN products p ON cat.id = p.category_id
        LEFT JOIN invoice_items ii ON p.id = ii.product_id
        GROUP BY cat.id, cat.name
        HAVING total_quantity_sold > 0
        ORDER BY total_revenue DESC
    """).fetchall()
    conn.close()
    return rows


def get_profit_margin_by_product(limit=10):
    """
    Get products with their profit margins.
    Useful for identifying most and least profitable products.
    """
    conn = get_conn()
    rows = conn.execute("""
        SELECT 
            ii.product_id,
            ii.product_name,
            SUM(ii.total_price) as total_revenue,
            SUM(COALESCE(ii.cost_price, 0) * ii.quantity) as total_cost,
            SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) as total_profit,
            CASE 
                WHEN SUM(ii.total_price) > 0 
                THEN (SUM(ii.total_price - (COALESCE(ii.cost_price, 0) * ii.quantity)) / SUM(ii.total_price) * 100)
                ELSE 0 
            END as profit_margin_percentage
        FROM invoice_items ii
        GROUP BY ii.product_id, ii.product_name
        HAVING total_revenue > 0
        ORDER BY profit_margin_percentage DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_sales_analysis_summary():
    """
    Get comprehensive sales analysis summary for the dashboard.
    Includes top/bottom products, overall statistics, and key metrics.
    """
    # Get overall stats
    stats = get_sales_by_period()
    
    # Get top and bottom products
    top_product = get_top_selling_products(limit=1)
    bottom_product = get_lowest_selling_products(limit=1)
    
    # Get top 6 products for chart
    top_products_chart = get_product_sales_summary(limit=6)
    
    return {
        "overall_stats": stats,
        "top_product": top_product[0] if top_product else None,
        "bottom_product": bottom_product[0] if bottom_product else None,
        "top_products_for_chart": top_products_chart
    }
