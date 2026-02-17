"""
Warehouses Page – CRUD operations for warehouse locations.

Manages warehouse entries with name and rack number, supporting inline editing,
search, and pagination.
"""

import streamlit as st

from config import PAGE_SIZE
from services.warehouse_service import add_warehouse, delete_warehouse, list_warehouses, update_warehouse
from utils.pagination import clamp_page, get_offset, get_total_pages


def render_warehouses():
    """Render the warehouses CRUD page with inline editing and search."""
    st.markdown("## Warehouses")

    # Add section - two text inputs stacked, button below
    st.markdown('<div class="wh-add-marker"></div>', unsafe_allow_html=True)
    
    new_name = st.text_input(
        "Warehouse Name",
        label_visibility="collapsed",
        placeholder="Warehouse Name",
        key="wh_new_name",
    )
    new_rack = st.text_input(
        "Rack Number",
        label_visibility="collapsed",
        placeholder="Warehouse Rack Number",
        key="wh_new_rack",
    )
    
    # Add button + Search on same line
    add_search_cols = st.columns([1, 6, 2], gap="small")
    with add_search_cols[0]:
        add_clicked = st.button("Add", key="wh_add_btn")
    with add_search_cols[2]:
        search_query = st.text_input("🔍", label_visibility="collapsed", placeholder="Search...", key="wh_search")
    
    if add_clicked:
        if not new_name.strip():
            st.error("Warehouse name is required.")
        else:
            add_warehouse(new_name, new_rack)
            st.success("Warehouse added.")
            st.rerun()

    rows = list_warehouses()
    # Filter by search
    if search_query:
        rows = [r for r in rows if search_query.lower() in r[1].lower() or (r[2] and search_query.lower() in r[2].lower())]
    
    total = len(rows)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("warehouse_page", 1), total_pages)
    st.session_state["warehouse_page"] = current_page

    if "warehouse_edit_id" not in st.session_state:
        st.session_state["warehouse_edit_id"] = None

    # Table header
    st.markdown('<div class="wh-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1, 5, 3, 4], gap="small")
    with header_cols[0]:
        st.markdown("**No**")
    with header_cols[1]:
        st.markdown("**Warehouse Name**")
    with header_cols[2]:
        st.markdown("**Rack Number**")
    with header_cols[3]:
        st.markdown("**Options**")

    if total == 0:
        st.info("No warehouses found.")
    else:
        offset = get_offset(current_page, PAGE_SIZE)
        page_rows = rows[offset: offset + PAGE_SIZE]
        for idx, (wh_id, name, rack_number) in enumerate(page_rows, start=offset + 1):
            rack_number = rack_number or ""
            st.markdown('<div class="wh-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1, 5, 3, 4], gap="small")
            with row_cols[0]:
                st.markdown(str(idx))
            with row_cols[1]:
                if st.session_state.get("warehouse_edit_id") == wh_id:
                    edit_name = st.text_input(
                        "Warehouse Name",
                        value=name,
                        label_visibility="collapsed",
                        key=f"wh_edit_name_{wh_id}",
                    )
                else:
                    st.markdown(name)
            with row_cols[2]:
                if st.session_state.get("warehouse_edit_id") == wh_id:
                    edit_rack = st.text_input(
                        "Rack Number",
                        value=rack_number,
                        label_visibility="collapsed",
                        key=f"wh_edit_rack_{wh_id}",
                    )
                else:
                    st.markdown(rack_number if rack_number else "-")
            with row_cols[3]:
                if st.session_state.get("warehouse_edit_id") == wh_id:
                    st.markdown('<div class="wh-options-marker"></div>', unsafe_allow_html=True)
                    opt_cols = st.columns([1, 1, 3], gap="small")
                    with opt_cols[0]:
                        save_clicked = st.button("Save", key=f"save_wh_{wh_id}")
                    with opt_cols[1]:
                        cancel_clicked = st.button("Cancel", key=f"cancel_wh_{wh_id}")
                    if save_clicked:
                        if not edit_name.strip():
                            st.error("Warehouse name is required.")
                        else:
                            update_warehouse(wh_id, edit_name, edit_rack)
                            st.session_state["warehouse_edit_id"] = None
                            st.success("Warehouse updated.")
                            st.rerun()
                    if cancel_clicked:
                        st.session_state["warehouse_edit_id"] = None
                        st.rerun()
                else:
                    st.markdown('<div class="wh-options-marker"></div>', unsafe_allow_html=True)
                    opt_cols = st.columns([1, 1, 3], gap="small")
                    with opt_cols[0]:
                        edit_clicked = st.button("Edit", key=f"edit_wh_{wh_id}")
                    with opt_cols[1]:
                        delete_clicked = st.button("Delete", key=f"del_wh_{wh_id}")
                    if edit_clicked:
                        st.session_state["warehouse_edit_id"] = wh_id
                        st.rerun()
                    if delete_clicked:
                        delete_warehouse(wh_id)
                        st.success("Warehouse deleted.")
                        st.rerun()

    # Pagination
    st.markdown(
        f"""
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-wh" {'disabled' if current_page == 1 else ''}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-wh" {'disabled' if current_page == total_pages else ''}>Next</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='display:none'>", unsafe_allow_html=True)
    nav_cols = st.columns([1, 1, 1])
    with nav_cols[0]:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="wh_prev"):
            st.session_state["warehouse_page"] = current_page - 1
            st.rerun()
    with nav_cols[2]:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="wh_next"):
            st.session_state["warehouse_page"] = current_page + 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)