"""
Staff Page – Employee management system.

Provides interfaces for:
- Adding new staff members
- Managing staff information (view/edit/delete)
- Tracking staff details (name, role, salary, start date, age, contact info)
"""

import streamlit as st
from datetime import date

from config import PAGE_SIZE
from services.staff_service import (
    add_staff,
    delete_staff,
    get_staff,
    get_staff_count,
    list_staff_paginated,
    update_staff,
)
from utils.pagination import clamp_page, get_offset, get_total_pages


def render_staff_add():
    st.markdown("## Staff")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Add Staff</p>", unsafe_allow_html=True)

    # Show success message if exists
    if st.session_state.get("staff_added"):
        st.success("Staff added successfully!")
        st.session_state["staff_added"] = False

    with st.form("add_staff_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *", key="staff_name")
            phone = st.text_input("Phone", key="staff_phone")
            email = st.text_input("Email", key="staff_email")
            role = st.text_input("Role", key="staff_role")
        with col2:
            salary = st.text_input("Salary", key="staff_salary", placeholder="0")
            start_date = st.date_input("Start Date", value=None, key="staff_start_date")
            age = st.number_input("Age", min_value=0, max_value=100, value=0, key="staff_age")

        submitted = st.form_submit_button("Add Staff")
        if submitted:
            if not name.strip():
                st.error("Staff name is required.")
            else:
                try:
                    salary_val = float(salary) if salary.strip() else 0
                except ValueError:
                    salary_val = 0
                age_val = age if age > 0 else None
                start_date_str = str(start_date) if start_date else None
                add_staff(name, phone, email, role, salary_val, start_date_str, age_val)
                st.session_state["staff_added"] = True
                st.rerun()


def render_staff_manage():
    st.markdown("## Staff")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Manage Staff</p>", unsafe_allow_html=True)

    # Initialize session state
    if "staff_page" not in st.session_state:
        st.session_state["staff_page"] = 1
    if "staff_edit_id" not in st.session_state:
        st.session_state["staff_edit_id"] = None
    if "staff_view_id" not in st.session_state:
        st.session_state["staff_view_id"] = None

    # Search
    search_col1, search_col2 = st.columns([3, 1])
    with search_col2:
        search_query = st.text_input("Search", label_visibility="collapsed", placeholder="Search...", key="staff_search")

    # Handle View Mode
    if st.session_state.get("staff_view_id"):
        staff_id = st.session_state["staff_view_id"]
        staff = get_staff(staff_id)
        if staff:
            st.markdown("### View Staff")
            st.markdown(f"**Name:** {staff[1] or 'N/A'}")
            st.markdown(f"**Phone:** {staff[2] or 'N/A'}")
            st.markdown(f"**Email:** {staff[3] or 'N/A'}")
            st.markdown(f"**Role:** {staff[4] or 'N/A'}")
            st.markdown(f"**Salary:** {staff[5]:.2f}" if staff[5] else "**Salary:** 0.00")
            st.markdown(f"**Start Date:** {staff[6] or 'N/A'}")
            st.markdown(f"**Age:** {staff[7] or 'N/A'}")
            if st.button("Close View", key="close_view_staff"):
                st.session_state["staff_view_id"] = None
                st.rerun()
        return

    # Handle Edit Mode
    if st.session_state.get("staff_edit_id"):
        staff_id = st.session_state["staff_edit_id"]
        staff = get_staff(staff_id)
        if staff:
            st.markdown("### Edit Staff")
            with st.form("edit_staff_form"):
                col1, col2 = st.columns(2)
                with col1:
                    edit_name = st.text_input("Name *", value=staff[1] or "", key="edit_staff_name")
                    edit_phone = st.text_input("Phone", value=staff[2] or "", key="edit_staff_phone")
                    edit_email = st.text_input("Email", value=staff[3] or "", key="edit_staff_email")
                    edit_role = st.text_input("Role", value=staff[4] or "", key="edit_staff_role")
                with col2:
                    edit_salary = st.text_input("Salary", value=str(staff[5] or 0), key="edit_staff_salary")
                    start_val = None
                    if staff[6]:
                        try:
                            start_val = date.fromisoformat(staff[6])
                        except (ValueError, TypeError):
                            pass
                    edit_start_date = st.date_input("Start Date", value=start_val, key="edit_staff_start_date")
                    edit_age = st.number_input("Age", min_value=0, max_value=100, value=staff[7] or 0, key="edit_staff_age")

                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    save = st.form_submit_button("Save Changes")
                with btn_col2:
                    cancel = st.form_submit_button("Cancel")

                if save:
                    if not edit_name.strip():
                        st.error("Staff name is required.")
                    else:
                        try:
                            salary_val = float(edit_salary) if edit_salary.strip() else 0
                        except ValueError:
                            salary_val = 0
                        age_val = edit_age if edit_age > 0 else None
                        start_date_str = str(edit_start_date) if edit_start_date else None
                        update_staff(staff_id, edit_name, edit_phone, edit_email, edit_role, salary_val, start_date_str, age_val)
                        st.session_state["staff_edit_id"] = None
                        st.success("Staff updated successfully!")
                        st.rerun()
                if cancel:
                    st.session_state["staff_edit_id"] = None
                    st.rerun()
        return

    # Get data
    total = get_staff_count(search_query)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("staff_page", 1), total_pages)
    st.session_state["staff_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_staff_paginated(offset, PAGE_SIZE, search_query)

    # Table header
    st.markdown('<div class="staff-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([0.5, 2, 1.5, 2, 1.5, 1, 2], gap="small")
    headers = ["No", "Name", "Phone", "Email", "Role", "Salary", "Options"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    if total == 0:
        st.info("No staff found.")
    else:
        for idx, row in enumerate(rows, start=offset + 1):
            staff_id, name, phone, email, role, salary, start_date, age = row
            st.markdown('<div class="staff-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([0.5, 2, 1.5, 2, 1.5, 1, 2], gap="small")
            with row_cols[0]:
                st.markdown(str(idx))
            with row_cols[1]:
                st.markdown(name or "N/A")
            with row_cols[2]:
                st.markdown(phone or "N/A")
            with row_cols[3]:
                st.markdown(email or "N/A")
            with row_cols[4]:
                st.markdown(role or "N/A")
            with row_cols[5]:
                st.markdown(f"{salary:.2f}" if salary else "0.00")
            with row_cols[6]:
                st.markdown('<div class="staff-options-marker"></div>', unsafe_allow_html=True)
                opt_cols = st.columns([1, 1, 1], gap="small")
                with opt_cols[0]:
                    if st.button("View", key=f"view_staff_{staff_id}"):
                        st.session_state["staff_view_id"] = staff_id
                        st.rerun()
                with opt_cols[1]:
                    if st.button("Edit", key=f"edit_staff_{staff_id}"):
                        st.session_state["staff_edit_id"] = staff_id
                        st.rerun()
                with opt_cols[2]:
                    if st.button("Del", key=f"del_staff_{staff_id}"):
                        delete_staff(staff_id)
                        st.success("Staff deleted.")
                        st.rerun()

    # Pagination Box
    st.markdown(
        f'''
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-staff" {"disabled" if current_page == 1 else ""}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-staff" {"disabled" if current_page == total_pages else ""}>Next</button>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="staff_prev_hidden"):
            st.session_state["staff_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="staff_next_hidden"):
            st.session_state["staff_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



# Keep old function for backward compatibility
def render_staff():
    render_staff_manage()
