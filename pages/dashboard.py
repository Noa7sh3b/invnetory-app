import streamlit as st
from services.invoice_service import get_dashboard_stats
from ui.components import render_metric_cards


def render_dashboard():
    st.markdown("## Dashboard")
    stats = get_dashboard_stats()

    metrics = [
        {"label": "Total Sales", "value": f"{int(stats['total_sales'])}"},
        {"label": "Total Receivable", "value": f"{stats['total_receivable']:.2f}"},
        {"label": "Total Received Amount", "value": f"{stats['total_received']:.2f}"},
        {"label": "Sales Total Price Saling", "value": f"{stats['sales_total_price_saling']:.2f}"},
        {"label": "Total Cost (Supplier)", "value": f"{stats['total_cost']:.2f}"},
        {"label": "Total Profit", "value": f"{stats['total_profit']:.2f}"},
        {"label": "Total Products", "value": f"{stats['total_products']}"},
        {"label": "Total Invoice", "value": f"{stats['total_invoice']}"},
        {"label": "Total Customer", "value": f"{stats['total_customers']}"},
        {"label": "Total Suppliers", "value": f"{stats['total_suppliers']}"},
    ]
    render_metric_cards(metrics, columns=3)
