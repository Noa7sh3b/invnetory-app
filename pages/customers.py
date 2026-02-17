"""
Customers Page – Customer management and payment tracking.

Provides interfaces for:
- Adding new customers
- Managing customer information (view/edit/delete)
- Tracking customer payment status (paid/unpaid/partial)
- Recording customer payments with history
"""

import streamlit as st
from datetime import date

from config import PAGE_SIZE
from services.customer_service import (
    add_customer,
    delete_customer,
    get_customer,
    get_customer_count,
    list_customers_paginated,
    list_customers,
    update_customer,
    add_customer_payment,
    list_payments_paginated,
    get_payment_count,
    get_customer_payment,
    update_customer_payment,
    delete_customer_payment,
)
from utils.pagination import clamp_page, get_offset, get_total_pages


def render_customers_add():
    st.markdown("## Customers")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Add Customer</p>", unsafe_allow_html=True)

    # Show success message if exists
    if st.session_state.get("customer_added"):
        st.success("Customer added successfully!")
        st.session_state["customer_added"] = False

    with st.form("add_customer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            customer_id = st.text_input("Customer ID", key="cust_id")
            name = st.text_input("Customer Name *", key="cust_name")
            phone = st.text_input("Phone", key="cust_phone")
        with col2:
            email = st.text_input("Email", key="cust_email")
            address = st.text_area("Address", key="cust_address", height=100)

        submitted = st.form_submit_button("Add Customer")
        if submitted:
            if not name.strip():
                st.error("Customer name is required.")
            else:
                add_customer(customer_id, name, phone, email, address)
                st.session_state["customer_added"] = True
                st.rerun()


def render_customers_manage():
    st.markdown("## Customers")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Manage Customers</p>", unsafe_allow_html=True)

    # Initialize session state
    if "customer_page" not in st.session_state:
        st.session_state["customer_page"] = 1
    if "customer_edit_id" not in st.session_state:
        st.session_state["customer_edit_id"] = None
    if "customer_view_id" not in st.session_state:
        st.session_state["customer_view_id"] = None

    # Search
    search_col1, search_col2 = st.columns([3, 1])
    with search_col2:
        search_query = st.text_input("Search", label_visibility="collapsed", placeholder="Search...", key="cust_search")

    # Handle View Mode
    if st.session_state.get("customer_view_id"):
        cust_pk = st.session_state["customer_view_id"]
        customer = get_customer(cust_pk)
        if customer:
            st.markdown("### View Customer")
            st.markdown(f"**Customer ID:** {customer[1] or 'N/A'}")
            st.markdown(f"**Name:** {customer[2] or 'N/A'}")
            st.markdown(f"**Phone:** {customer[3] or 'N/A'}")
            st.markdown(f"**Email:** {customer[4] or 'N/A'}")
            st.markdown(f"**Address:** {customer[5] or 'N/A'}")
            if st.button("Close View", key="close_view_cust"):
                st.session_state["customer_view_id"] = None
                st.rerun()
        return

    # Handle Edit Mode
    if st.session_state.get("customer_edit_id"):
        cust_pk = st.session_state["customer_edit_id"]
        customer = get_customer(cust_pk)
        if customer:
            st.markdown("### Edit Customer")
            with st.form("edit_customer_form"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_cust_id = st.text_input("Customer ID", value=customer[1] or "", key="edit_cust_id")
                    edit_name = st.text_input("Customer Name *", value=customer[2] or "", key="edit_cust_name")
                    edit_phone = st.text_input("Phone", value=customer[3] or "", key="edit_cust_phone")
                with col2:
                    edit_email = st.text_input("Email", value=customer[4] or "", key="edit_cust_email")
                    edit_address = st.text_area("Address", value=customer[5] or "", key="edit_cust_address", height=100)

                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    save = st.form_submit_button("Save Changes")
                with btn_col2:
                    cancel = st.form_submit_button("Cancel")

                if save:
                    if not edit_name.strip():
                        st.error("Customer name is required.")
                    else:
                        update_customer(cust_pk, edit_cust_id, edit_name, edit_phone, edit_email, edit_address)
                        st.session_state["customer_edit_id"] = None
                        st.success("Customer updated successfully!")
                        st.rerun()
                if cancel:
                    st.session_state["customer_edit_id"] = None
                    st.rerun()
        return

    # Get data
    total = get_customer_count(search_query)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("customer_page", 1), total_pages)
    st.session_state["customer_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_customers_paginated(offset, PAGE_SIZE, search_query)

    # Table header
    st.markdown('<div class="cust-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1, 2, 1.5, 2, 2], gap="small")
    headers = ["Cust ID", "Name", "Phone", "Email", "Options"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    if total == 0:
        st.info("No customers found.")
    else:
        for idx, row in enumerate(rows, start=offset + 1):
            pk, cust_id, name, phone, email, address = row
            st.markdown('<div class="cust-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1, 2, 1.5, 2, 2], gap="small")
            with row_cols[0]:
                st.markdown(cust_id or "N/A")
            with row_cols[1]:
                st.markdown(name or "N/A")
            with row_cols[2]:
                st.markdown(phone or "N/A")
            with row_cols[3]:
                st.markdown(email or "N/A")
            with row_cols[4]:
                st.markdown('<div class="cust-options-marker"></div>', unsafe_allow_html=True)
                opt_cols = st.columns([1, 1, 1], gap="small")
                with opt_cols[0]:
                    if st.button("View", key=f"view_cust_{pk}"):
                        st.session_state["customer_view_id"] = pk
                        st.rerun()
                with opt_cols[1]:
                    if st.button("Edit", key=f"edit_cust_{pk}"):
                        st.session_state["customer_edit_id"] = pk
                        st.rerun()
                with opt_cols[2]:
                    if st.button("Del", key=f"del_cust_{pk}"):
                        delete_customer(pk)
                        st.success("Customer deleted.")
                        st.rerun()

    # Pagination Box
    st.markdown(
        f'''
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-cust" {"disabled" if current_page == 1 else ""}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-cust" {"disabled" if current_page == total_pages else ""}>Next</button>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="cust_prev_hidden"):
            st.session_state["customer_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="cust_next_hidden"):
            st.session_state["customer_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_customers_status():
    st.markdown("## Customers")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Paid / Unpaid Customers</p>", unsafe_allow_html=True)

    # Initialize session state
    if "payment_page" not in st.session_state:
        st.session_state["payment_page"] = 1
    if "payment_edit_id" not in st.session_state:
        st.session_state["payment_edit_id"] = None
    if "payment_view_id" not in st.session_state:
        st.session_state["payment_view_id"] = None
    if "show_add_payment" not in st.session_state:
        st.session_state["show_add_payment"] = False

    # Show success message
    if st.session_state.get("payment_added"):
        st.success("Payment record added successfully!")
        st.session_state["payment_added"] = False

    # Add button
    if st.button("+ Add Payment Record"):
        st.session_state["show_add_payment"] = not st.session_state["show_add_payment"]

    # Add Payment Form
    if st.session_state.get("show_add_payment"):
        st.markdown("### Add Payment Record")
        customers = list_customers()
        if not customers:
            st.warning("No customers found. Please add customers first.")
        else:
            customer_options = [{"id": c[0], "cust_id": c[1], "name": c[2]} for c in customers]
            with st.form("add_payment_form", clear_on_submit=True):
                selected_customer = st.selectbox(
                    "Select Customer *",
                    customer_options,
                    format_func=lambda x: f"{x['cust_id'] or 'N/A'} - {x['name']}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    total_amount_str = st.text_input("Total Amount *", placeholder="0.00", key="pay_total")
                    amount_paid_str = st.text_input("Amount Paid", placeholder="0.00", key="pay_paid")
                with col2:
                    payment_date = st.date_input("Payment Date", value=None, key="pay_date")
                    notes = st.text_area("Notes", key="pay_notes", height=80)

                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    add_btn = st.form_submit_button("Add")
                with btn_col2:
                    cancel_btn = st.form_submit_button("Cancel")

                if add_btn:
                    try:
                        total_amount = float(total_amount_str) if total_amount_str.strip() else 0.0
                    except ValueError:
                        total_amount = 0.0
                    try:
                        amount_paid = float(amount_paid_str) if amount_paid_str.strip() else 0.0
                    except ValueError:
                        amount_paid = 0.0
                    if total_amount <= 0:
                        st.error("Total amount must be greater than 0.")
                    else:
                        payment_date_str = str(payment_date) if payment_date else None
                        add_customer_payment(selected_customer["id"], total_amount, amount_paid, payment_date_str, notes)
                        st.session_state["payment_added"] = True
                        st.session_state["show_add_payment"] = False
                        st.rerun()
                if cancel_btn:
                    st.session_state["show_add_payment"] = False
                    st.rerun()
        st.markdown("---")

    # Handle View Mode
    if st.session_state.get("payment_view_id"):
        pay_id = st.session_state["payment_view_id"]
        payment = get_customer_payment(pay_id)
        if payment:
            st.markdown("### View Payment Record")
            st.markdown(f"**Customer ID:** {payment[2] or 'N/A'}")
            st.markdown(f"**Name:** {payment[3] or 'N/A'}")
            st.markdown(f"**Email:** {payment[4] or 'N/A'}")
            st.markdown(f"**Payment Status:** {payment[5] or 'N/A'}")
            st.markdown(f"**Total Amount:** {payment[6]:.2f}")
            st.markdown(f"**Amount Paid:** {payment[7]:.2f}")
            st.markdown(f"**Amount Due:** {payment[8]:.2f}")
            st.markdown(f"**Payment Date:** {payment[9] or 'N/A'}")
            st.markdown(f"**Notes:** {payment[10] or 'N/A'}")
            if st.button("Close View", key="close_view_pay"):
                st.session_state["payment_view_id"] = None
                st.rerun()
        return

    # Handle Edit Mode
    if st.session_state.get("payment_edit_id"):
        pay_id = st.session_state["payment_edit_id"]
        payment = get_customer_payment(pay_id)
        if payment:
            st.markdown("### Edit Payment Record")
            st.markdown(f"**Customer:** {payment[2] or 'N/A'} - {payment[3]}")
            with st.form("edit_payment_form"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_total_str = st.text_input("Total Amount *", value=f"{payment[6]:.2f}", key="edit_pay_total")
                    edit_paid_str = st.text_input("Amount Paid", value=f"{payment[7]:.2f}", key="edit_pay_paid")
                with col2:
                    pay_date_val = None
                    if payment[9]:
                        try:
                            pay_date_val = date.fromisoformat(payment[9])
                        except (ValueError, TypeError):
                            pass
                    edit_date = st.date_input("Payment Date", value=pay_date_val, key="edit_pay_date")
                    edit_notes = st.text_area("Notes", value=payment[10] or "", key="edit_pay_notes", height=80)

                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    save = st.form_submit_button("Save Changes")
                with btn_col2:
                    cancel = st.form_submit_button("Cancel")

                if save:
                    try:
                        edit_total = float(edit_total_str) if edit_total_str.strip() else 0.0
                    except ValueError:
                        edit_total = 0.0
                    try:
                        edit_paid = float(edit_paid_str) if edit_paid_str.strip() else 0.0
                    except ValueError:
                        edit_paid = 0.0
                    edit_date_str = str(edit_date) if edit_date else None
                    update_customer_payment(pay_id, edit_total, edit_paid, edit_date_str, edit_notes)
                    st.session_state["payment_edit_id"] = None
                    st.success("Payment record updated!")
                    st.rerun()
                if cancel:
                    st.session_state["payment_edit_id"] = None
                    st.rerun()
        return

    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns([2, 3, 1.5], gap="small")
    with filter_col1:
        status_filter = st.selectbox("Filter by Status", ["All", "paid", "unpaid"], key="pay_status_filter")
    with filter_col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_query = st.text_input("Search", label_visibility="collapsed", placeholder="Search...", key="pay_search")

    status_val = "" if status_filter == "All" else status_filter

    # Get data
    total = get_payment_count(search_query, status_val)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("payment_page", 1), total_pages)
    st.session_state["payment_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_payments_paginated(offset, PAGE_SIZE, search_query, status_val)

    # Table header
    st.markdown('<div class="cust-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1, 2, 1, 1, 1, 1, 2], gap="small")
    headers = ["Cust ID", "Name", "Status", "Total", "Paid", "Due", "Options"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    if total == 0:
        st.info("No payment records found.")
    else:
        for row in rows:
            pay_id, cust_id, name, status, total_amt, paid_amt, due_amt = row
            st.markdown('<div class="cust-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1, 2, 1, 1, 1, 1, 2], gap="small")
            with row_cols[0]:
                st.markdown(cust_id or "N/A")
            with row_cols[1]:
                st.markdown(name or "N/A")
            with row_cols[2]:
                if status == "paid":
                    st.markdown(":green[Paid]")
                else:
                    st.markdown(":red[Unpaid]")
            with row_cols[3]:
                st.markdown(f"{total_amt:.2f}")
            with row_cols[4]:
                st.markdown(f"{paid_amt:.2f}")
            with row_cols[5]:
                st.markdown(f"{due_amt:.2f}")
            with row_cols[6]:
                st.markdown('<div class="cust-options-marker"></div>', unsafe_allow_html=True)
                opt_cols = st.columns([1, 1, 1], gap="small")
                with opt_cols[0]:
                    if st.button("View", key=f"view_pay_{pay_id}"):
                        st.session_state["payment_view_id"] = pay_id
                        st.rerun()
                with opt_cols[1]:
                    if st.button("Edit", key=f"edit_pay_{pay_id}"):
                        st.session_state["payment_edit_id"] = pay_id
                        st.rerun()
                with opt_cols[2]:
                    if st.button("Del", key=f"del_pay_{pay_id}"):
                        delete_customer_payment(pay_id)
                        st.success("Payment record deleted.")
                        st.rerun()

    # Pagination Box
    st.markdown(
        f'''
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-pay" {"disabled" if current_page == 1 else ""}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-pay" {"disabled" if current_page == total_pages else ""}>Next</button>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="pay_prev_hidden"):
            st.session_state["payment_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="pay_next_hidden"):
            st.session_state["payment_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


