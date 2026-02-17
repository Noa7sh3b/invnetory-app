"""
Suppliers Page – Add and manage supplier information.

Provides separate views for adding new suppliers and managing existing ones
with view/edit/delete capabilities and pagination.
"""

import streamlit as st

from config import PAGE_SIZE
from services.supplier_service import (
    add_supplier,
    delete_supplier,
    list_suppliers_paginated,
    get_supplier_count,
    get_supplier,
    update_supplier,
)
from utils.pagination import clamp_page, get_offset, get_total_pages


def render_suppliers_add():
    """Render Add Supplier page"""
    st.markdown("## Suppliers")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Add Supplier</p>", unsafe_allow_html=True)

    # Show success message if exists
    if st.session_state.get("supplier_added"):
        st.success("Supplier added successfully!")
        st.session_state["supplier_added"] = False

    # Add form
    with st.form("add_supplier_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Supplier Name *", key="sup_name")
            email = st.text_input("Email", key="sup_email")
            phone = st.text_input("Phone", key="sup_phone")
        with col2:
            contact_person = st.text_input("Contact Person", key="sup_contact")
            address = st.text_area("Address", key="sup_address", height=120)

        submitted = st.form_submit_button("Add Supplier")
        if submitted:
            if not name.strip():
                st.error("Supplier name is required.")
            else:
                add_supplier(name, contact_person, email, phone, address)
                st.session_state["supplier_added"] = True
                st.rerun()


def render_suppliers_manage():
    """Render Manage Suppliers page with list view"""
    st.markdown("## Suppliers")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Manage Suppliers</p>", unsafe_allow_html=True)

    # Initialize session state
    if "supplier_page" not in st.session_state:
        st.session_state["supplier_page"] = 1
    if "supplier_edit_id" not in st.session_state:
        st.session_state["supplier_edit_id"] = None
    if "supplier_view_id" not in st.session_state:
        st.session_state["supplier_view_id"] = None

    # Search
    search_col1, search_col2 = st.columns([3, 1])
    with search_col2:
        search_query = st.text_input("🔍", label_visibility="collapsed", placeholder="Search...", key="sup_search")

    # Handle View Mode
    if st.session_state.get("supplier_view_id"):
        sup_id = st.session_state["supplier_view_id"]
        supplier = get_supplier(sup_id)
        if supplier:
            st.markdown("### View Supplier")
            st.markdown(f"**Supplier Name:** {supplier[1] or 'N/A'}")
            st.markdown(f"**Contact Person:** {supplier[2] or 'N/A'}")
            st.markdown(f"**Email:** {supplier[3] or 'N/A'}")
            st.markdown(f"**Phone:** {supplier[4] or 'N/A'}")
            st.markdown(f"**Address:** {supplier[5] or 'N/A'}")
            if st.button("Close View", key="close_view_sup"):
                st.session_state["supplier_view_id"] = None
                st.rerun()
        return

    # Handle Edit Mode
    if st.session_state.get("supplier_edit_id"):
        sup_id = st.session_state["supplier_edit_id"]
        supplier = get_supplier(sup_id)
        if supplier:
            st.markdown("### Edit Supplier")
            with st.form("edit_supplier_form"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_name = st.text_input("Supplier Name *", value=supplier[1] or "", key="edit_sup_name")
                    edit_email = st.text_input("Email", value=supplier[3] or "", key="edit_sup_email")
                    edit_phone = st.text_input("Phone", value=supplier[4] or "", key="edit_sup_phone")
                with col2:
                    edit_contact = st.text_input("Contact Person", value=supplier[2] or "", key="edit_sup_contact")
                    edit_address = st.text_area("Address", value=supplier[5] or "", key="edit_sup_address", height=120)

                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    save = st.form_submit_button("Save Changes")
                with btn_col2:
                    cancel = st.form_submit_button("Cancel")

                if save:
                    if not edit_name.strip():
                        st.error("Supplier name is required.")
                    else:
                        update_supplier(sup_id, edit_name, edit_contact, edit_email, edit_phone, edit_address)
                        st.session_state["supplier_edit_id"] = None
                        st.success("Supplier updated successfully!")
                        st.rerun()
                if cancel:
                    st.session_state["supplier_edit_id"] = None
                    st.rerun()
        return

    # Get data
    total = get_supplier_count(search_query)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("supplier_page", 1), total_pages)
    st.session_state["supplier_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_suppliers_paginated(offset, PAGE_SIZE, search_query)

    # Table header
    st.markdown('<div class="sup-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([0.5, 2, 1.5, 1.5, 1.5, 2], gap="small")
    with header_cols[0]:
        st.markdown("**No**")
    with header_cols[1]:
        st.markdown("**Supplier Name**")
    with header_cols[2]:
        st.markdown("**Contact**")
    with header_cols[3]:
        st.markdown("**Phone**")
    with header_cols[4]:
        st.markdown("**Email**")
    with header_cols[5]:
        st.markdown("**Options**")

    if total == 0:
        st.info("No suppliers found.")
    else:
        for idx, row in enumerate(rows, start=offset + 1):
            sup_id, name, contact_person, email, phone, address = row
            st.markdown('<div class="sup-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([0.5, 2, 1.5, 1.5, 1.5, 2], gap="small")
            with row_cols[0]:
                st.markdown(str(idx))
            with row_cols[1]:
                st.markdown(name or "N/A")
            with row_cols[2]:
                st.markdown(contact_person or "N/A")
            with row_cols[3]:
                st.markdown(phone or "N/A")
            with row_cols[4]:
                st.markdown(email or "N/A")
            with row_cols[5]:
                st.markdown('<div class="sup-options-marker"></div>', unsafe_allow_html=True)
                opt_cols = st.columns([1, 1, 1], gap="small")
                with opt_cols[0]:
                    if st.button("View", key=f"view_sup_{sup_id}"):
                        st.session_state["supplier_view_id"] = sup_id
                        st.rerun()
                with opt_cols[1]:
                    if st.button("Edit", key=f"edit_sup_{sup_id}"):
                        st.session_state["supplier_edit_id"] = sup_id
                        st.rerun()
                with opt_cols[2]:
                    if st.button("Del", key=f"del_sup_{sup_id}"):
                        delete_supplier(sup_id)
                        st.success("Supplier deleted.")
                        st.rerun()

    # Pagination Box
    st.markdown(
        f"""
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-sup" {'disabled' if current_page == 1 else ''}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-sup" {'disabled' if current_page == total_pages else ''}>Next</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="sup_prev_hidden"):
            st.session_state["supplier_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="sup_next_hidden"):
            st.session_state["supplier_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



# Keep old function for backward compatibility
def render_suppliers():
    render_suppliers_manage()