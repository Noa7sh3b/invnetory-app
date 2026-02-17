"""
Stock Monitoring Page – Track inventory alerts and issues.

Provides interfaces for monitoring:
- Dead Stock: Products with no recent sales activity
- Low Stock: Products below their alert threshold
- Expired Products: Products past their expiration date
"""

import streamlit as st
from services.product_service import (
    list_low_stock_products,
    list_expired_products,
    list_dead_stock_products,
    get_all_products_simple,
)


def render_dead_stock():
    """Display products with no recent sales (configurable days threshold)."""
    st.markdown("## Stock")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Dead Stock</p>", unsafe_allow_html=True)

    # Settings
    col1, col2 = st.columns([1, 3])
    with col1:
        days = st.number_input("Days without sales", min_value=1, value=30, step=1)

    # Add product manually button
    if "show_add_dead" not in st.session_state:
        st.session_state["show_add_dead"] = False

    if st.button("+ Add Product to Dead Stock"):
        st.session_state["show_add_dead"] = not st.session_state["show_add_dead"]

    if st.session_state.get("show_add_dead"):
        products = get_all_products_simple()
        if products:
            product_options = [{"id": p[0], "name": p[1]} for p in products]
            selected = st.selectbox("Select Product", product_options, format_func=lambda x: x["name"])
            st.info(f"Product '{selected['name']}' will be shown in dead stock list if it has no sales in {days} days.")
        else:
            st.warning("No products available.")

    st.markdown("---")

    # Get dead stock products
    rows = list_dead_stock_products(days)

    if not rows:
        st.success("No dead stock found! All products have recent sales.")
        return

    st.warning(f"Found {len(rows)} products with no sales in the last {days} days")

    # Table header
    st.markdown('<div class="stock-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([0.5, 1.5, 1, 1, 1, 1], gap="small")
    headers = ["No", "Product", "Category", "Supplier", "Warehouse", "Qty"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    for idx, row in enumerate(rows, start=1):
        product_id, name, quantity, low_stock, dist_price, sell_price, image, cat, wh, sup, rack = row
        st.markdown('<div class="stock-row-marker"></div>', unsafe_allow_html=True)
        row_cols = st.columns([0.5, 1.5, 1, 1, 1, 1], gap="small")
        with row_cols[0]:
            st.markdown(str(idx))
        with row_cols[1]:
            st.markdown(name)
        with row_cols[2]:
            st.markdown(cat or "N/A")
        with row_cols[3]:
            st.markdown(sup or "N/A")
        with row_cols[4]:
            st.markdown(wh or "N/A")
        with row_cols[5]:
            st.markdown(str(quantity))


def render_low_stock():
    """Display products with quantity below their low stock alert threshold."""
    st.markdown("## Stock")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Low Stock</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Get low stock products (based on each product's low_stock_alert)
    rows = list_low_stock_products()

    if not rows:
        st.success("No low stock products found!")
        return

    st.warning(f"Found {len(rows)} products with low stock")

    # Table header
    st.markdown('<div class="stock-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([0.5, 1.5, 1, 1, 1, 1], gap="small")
    headers = ["No", "Product", "Category", "Supplier", "Qty", "Alert"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    for idx, row in enumerate(rows, start=1):
        product_id, name, quantity, low_stock, dist_price, sell_price, image, cat, wh, sup, rack = row
        st.markdown('<div class="stock-row-marker"></div>', unsafe_allow_html=True)
        row_cols = st.columns([0.5, 1.5, 1, 1, 1, 1], gap="small")
        with row_cols[0]:
            st.markdown(str(idx))
        with row_cols[1]:
            st.markdown(name)
        with row_cols[2]:
            st.markdown(cat or "N/A")
        with row_cols[3]:
            st.markdown(sup or "N/A")
        with row_cols[4]:
            st.markdown(f":red[{quantity}]")
        with row_cols[5]:
            st.markdown(str(low_stock))


def render_expired_products():
    """Display products that have passed their expiration date."""
    st.markdown("## Stock")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Expired Products</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Get expired products
    rows = list_expired_products()

    if not rows:
        st.success("No expired products found!")
        return

    st.error(f"Found {len(rows)} expired products!")

    # Table header
    st.markdown('<div class="stock-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([0.5, 1.5, 1, 1, 1, 1.5], gap="small")
    headers = ["No", "Product", "Category", "Supplier", "Qty", "Expiry Date"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    for idx, row in enumerate(rows, start=1):
        product_id, name, quantity, expiry_date, dist_price, sell_price, image, cat, wh, sup, rack = row
        st.markdown('<div class="stock-row-marker"></div>', unsafe_allow_html=True)
        row_cols = st.columns([0.5, 1.5, 1, 1, 1, 1.5], gap="small")
        with row_cols[0]:
            st.markdown(str(idx))
        with row_cols[1]:
            st.markdown(name)
        with row_cols[2]:
            st.markdown(cat or "N/A")
        with row_cols[3]:
            st.markdown(sup or "N/A")
        with row_cols[4]:
            st.markdown(str(quantity))
        with row_cols[5]:
            st.markdown(f":red[{expiry_date}]")
