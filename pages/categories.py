"""
Categories Page – CRUD operations for product categories.

Provides a simple interface for adding, editing, deleting, and searching categories
with pagination support.
"""

import streamlit as st

from config import PAGE_SIZE
from services.category_service import add_category, delete_category, list_categories, update_category
from utils.pagination import clamp_page, get_offset, get_total_pages


def render_categories():
    """Render the categories CRUD page with inline editing and search."""
    st.markdown("## CRUD")

    st.markdown('<div class="cat-add-marker"></div>', unsafe_allow_html=True)
    add_cols = st.columns([5, 1], gap="small")
    with add_cols[0]:
        new_name = st.text_input("Category Name", label_visibility="collapsed", placeholder="Category Name")
    with add_cols[1]:
        if st.button("Add", use_container_width=True):
            if not new_name.strip():
                st.error("Category name is required.")
            else:
                add_category(new_name)
                st.success("Category added.")
                st.rerun()

    # Search box on the right
    search_cols = st.columns([8, 1])
    with search_cols[1]:
        search_query = st.text_input("🔍", label_visibility="collapsed", placeholder="Search...", key="cat_search")

    rows = list_categories()
    # Filter by search
    if search_query:
        rows = [r for r in rows if search_query.lower() in r[1].lower()]
    
    total = len(rows)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("category_page", 1), total_pages)
    st.session_state["category_page"] = current_page

    if "category_edit_id" not in st.session_state:
        st.session_state["category_edit_id"] = None

    st.markdown('<div class="cat-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1, 6, 3], gap="small")
    with header_cols[0]:
        st.markdown("**No**")
    with header_cols[1]:
        st.markdown("**Category Name**")
    with header_cols[2]:
        st.markdown("**Options**")
    if total == 0:
        st.info("No categories found.")
    else:
        offset = get_offset(current_page, PAGE_SIZE)
        page_rows = rows[offset: offset + PAGE_SIZE]
        for idx, (cat_id, name) in enumerate(page_rows, start=offset + 1):
            st.markdown('<div class="cat-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1, 6, 3], gap="small")
            with row_cols[0]:
                st.markdown(str(idx))
            with row_cols[1]:
                if st.session_state.get("category_edit_id") == cat_id:
                    edit_value = st.text_input(
                        "Category Name",
                        value=name,
                        label_visibility="collapsed",
                        key=f"cat_edit_{cat_id}",
                    )
                else:
                    st.markdown(name)
            with row_cols[2]:
                if st.session_state.get("category_edit_id") == cat_id:
                    st.markdown('<div class="cat-options-marker"></div>', unsafe_allow_html=True)
                    opt_cols = st.columns([1, 1, 3], gap="small")
                    with opt_cols[0]:
                        save_clicked = st.button("Save", key=f"save_cat_{cat_id}")
                    with opt_cols[1]:
                        cancel_clicked = st.button("Cancel", key=f"cancel_cat_{cat_id}")
                    # opt_cols[2] empty spacer
                    if save_clicked:
                        if not edit_value.strip():
                            st.error("Category name is required.")
                        else:
                            update_category(cat_id, edit_value)
                            st.session_state["category_edit_id"] = None
                            st.success("Category updated.")
                            st.rerun()
                    if cancel_clicked:
                        st.session_state["category_edit_id"] = None
                        st.rerun()
                else:
                    st.markdown('<div class="cat-options-marker"></div>', unsafe_allow_html=True)
                    opt_cols = st.columns([1, 1, 3], gap="small")
                    with opt_cols[0]:
                        edit_clicked = st.button("Edit", key=f"edit_cat_{cat_id}")
                    with opt_cols[1]:
                        delete_clicked = st.button("Delete", key=f"del_cat_{cat_id}")
                    # opt_cols[2] empty spacer
                    if edit_clicked:
                        st.session_state["category_edit_id"] = cat_id
                        st.rerun()
                    if delete_clicked:
                        delete_category(cat_id)
                        st.success("Category deleted.")
                        st.rerun()
    st.markdown(
        f"""
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-cat" {'disabled' if current_page == 1 else ''}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-cat" {'disabled' if current_page == total_pages else ''}>Next</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='display:none'>", unsafe_allow_html=True)
    nav_cols = st.columns([1, 1, 1])
    with nav_cols[0]:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="cat_prev"):
            st.session_state["category_page"] = current_page - 1
            st.rerun()
    with nav_cols[2]:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="cat_next"):
            st.session_state["category_page"] = current_page + 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)