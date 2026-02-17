"""
Main Application Entry Point – Bootstraps the Streamlit app.

Responsibilities:
  • Configure the Streamlit page and initialise the database.
  • Build the sidebar navigation (logo, store name, menu sections).
  • Render the notification bell with low-stock / expired-product alerts.
  • Route to the correct page renderer based on session state.
"""

import os
import streamlit as st

from config import APP_NAME, NOTIFICATION_PREVIEW_LIMIT
from db import init_db
from ui.theme import apply_theme
from pages.dashboard import render_dashboard
from pages.products import render_products_add, render_products_manage
from pages.categories import render_categories
from pages.warehouses import render_warehouses
from pages.suppliers import render_suppliers_add, render_suppliers_manage
from pages.staff import render_staff_add, render_staff_manage
from pages.stock import render_dead_stock, render_low_stock, render_expired_products
from pages.customers import render_customers_add, render_customers_manage, render_customers_status
from pages.invoices import render_invoices_create, render_invoices_manage, render_invoices_status
from pages.sales_analysis import render_sales_analysis
from pages.settings import (
    render_settings_store,
    render_settings_currency,
    render_settings_low_stock,
    render_settings_readme,
)
from services.settings_service import get_setting
from services.product_service import list_low_stock_products, list_expired_products


# ── helpers ────────────────────────────────────────────────────────────────


def get_alerts_count():
    """Return (low_stock_count, expired_count) for the notification badge."""
    low_stock = list_low_stock_products()
    expired = list_expired_products()
    return len(low_stock), len(expired)


# ── page-routing map ──────────────────────────────────────────────────────

# Maps a session-state key → the render function to call.
PAGE_ROUTES = {
    "dashboard": render_dashboard,
    "products_add": render_products_add,
    "products_manage": render_products_manage,
    "categories_crud": render_categories,
    "warehouses_crud": render_warehouses,
    "suppliers_add": render_suppliers_add,
    "suppliers_manage": render_suppliers_manage,
    "staff_add": render_staff_add,
    "staff_manage": render_staff_manage,
    "stock_dead": render_dead_stock,
    "stock_low": render_low_stock,
    "stock_expired": render_expired_products,
    "customers_add": render_customers_add,
    "customers_manage": render_customers_manage,
    "customers_status": render_customers_status,
    "invoices_create": render_invoices_create,
    "invoices_manage": render_invoices_manage,
    "invoices_status": render_invoices_status,
    "sales_analysis": render_sales_analysis,
    "settings_store": render_settings_store,
    "settings_currency": render_settings_currency,
    "settings_low_stock": render_settings_low_stock,
    "settings_readme": render_settings_readme,
}


# ── main ──────────────────────────────────────────────────────────────────


def main():
    """Application entry point – called once per Streamlit rerun."""

    # -- Page configuration & bootstrap ------------------------------------
    st.set_page_config(
        page_title=APP_NAME,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_db()
    apply_theme()

    if "page" not in st.session_state:
        st.session_state["page"] = "dashboard"

    # -- Helper: sidebar navigation button ---------------------------------
    def nav_button(label, key):
        """Render a sidebar button that switches the active page."""
        if st.button(label, key=key, use_container_width=True):
            st.session_state["page"] = key
            st.rerun()

    # -- Fetch store branding & alert counts -------------------------------
    store_name = get_setting("store_name", "Inventory Management")
    store_logo = get_setting("store_logo", "")

    low_stock_count, expired_count = get_alerts_count()
    total_alerts = low_stock_count + expired_count

    # -- Sidebar -----------------------------------------------------------
    with st.sidebar:
        # Store logo + name header
        if store_logo and os.path.exists(store_logo):
            col_logo, col_name = st.columns([1, 2])
            with col_logo:
                st.image(store_logo, width=60)
            with col_name:
                st.markdown(
                    f"<h2 style='margin:0; padding-top:10px; font-size:1.4rem;'>"
                    f"{store_name}</h2>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f"<h2 style='margin:0; font-size:1.5rem;'>{store_name}</h2>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        nav_button("Dashboard", "dashboard")
        nav_button("📊 Sales Analysis", "sales_analysis")

        with st.expander("Products"):
            nav_button("Add Product", "products_add")
            nav_button(" Manage Products", "products_manage")

        with st.expander("Suppliers"):
            nav_button("Add Supplier", "suppliers_add")
            nav_button("Manage Suppliers", "suppliers_manage")

        with st.expander("Categories"):
            nav_button("CRUD", "categories_crud")

        with st.expander("Warehouses"):
            nav_button("CRUD", "warehouses_crud")

        with st.expander("Customers"):
            nav_button("Add Customer", "customers_add")
            nav_button("Manage Customers", "customers_manage")
            nav_button("Paid / Unpaid Customers", "customers_status")

        with st.expander("Invoices"):
            nav_button("Create Invoice", "invoices_create")
            nav_button("Manage Invoices", "invoices_manage")
            nav_button("Paid / Unpaid Invoices", "invoices_status")

        with st.expander("Stock"):
            nav_button("Dead Stock", "stock_dead")
            nav_button("Low Stock", "stock_low")
            nav_button("Expired Products", "stock_expired")

        with st.expander("Staff"):
            nav_button("Add Staff", "staff_add")
            nav_button("Manage Staff", "staff_manage")

        with st.expander("Settings"):
            nav_button("Store Settings", "settings_store")
            nav_button("Currency", "settings_currency")
            nav_button("Low Stock Alert Threshold", "settings_low_stock")
            nav_button("Read Me", "settings_readme")

    # -- Notification bell (top-right, Facebook-style popover) -------------
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    header_cols = st.columns([8, 1])
    with header_cols[1]:
        bell_text = f"🔔 {total_alerts}" if total_alerts > 0 else "🔔"

        with st.popover(bell_text, use_container_width=True):
            st.markdown("#### 🔔 Notifications")
            st.markdown("---")

            if total_alerts == 0:
                st.info("No alerts at the moment!")
            else:
                # Low-stock alerts
                if low_stock_count > 0:
                    st.markdown(f"**⚠️ Low Stock ({low_stock_count})**")
                    low_stock_items = list_low_stock_products()
                    for item in low_stock_items[:NOTIFICATION_PREVIEW_LIMIT]:
                        name, quantity, low_alert = item[1], item[2], item[3]
                        st.markdown(
                            f"<div style='padding:8px; margin:4px 0; background:#2d2d0d; "
                            f"border-left:3px solid #fbbf24; border-radius:4px;'>"
                            f"<b>{name}</b><br/>"
                            f"<small style='color:#fbbf24;'>Stock: {quantity} / Alert: {low_alert}</small>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    if low_stock_count > NOTIFICATION_PREVIEW_LIMIT:
                        st.caption(f"+{low_stock_count - NOTIFICATION_PREVIEW_LIMIT} more...")
                    if st.button("View All →", key="goto_low_stock_pop"):
                        st.session_state["page"] = "stock_low"
                        st.rerun()

                # Expired-product alerts
                if expired_count > 0:
                    st.markdown(f"**🚨 Expired ({expired_count})**")
                    expired_items = list_expired_products()
                    for item in expired_items[:NOTIFICATION_PREVIEW_LIMIT]:
                        name, expiry_date = item[1], item[3]
                        st.markdown(
                            f"<div style='padding:8px; margin:4px 0; background:#2d1515; "
                            f"border-left:3px solid #ff6b6b; border-radius:4px;'>"
                            f"<b>{name}</b><br/>"
                            f"<small style='color:#ff6b6b;'>Expired: {expiry_date}</small>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    if expired_count > NOTIFICATION_PREVIEW_LIMIT:
                        st.caption(f"+{expired_count - NOTIFICATION_PREVIEW_LIMIT} more...")
                    if st.button("View All →", key="goto_expired_pop"):
                        st.session_state["page"] = "stock_expired"
                        st.rerun()

    # -- Render the active page --------------------------------------------
    page_key = st.session_state["page"]
    renderer = PAGE_ROUTES.get(page_key)
    if renderer:
        renderer()
    else:
        st.markdown("## Coming Soon")
        st.info("This section is not implemented yet.")


# ── script entry ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
 