from datetime import date
from uuid import uuid4
import streamlit as st
from PIL import Image

from config import IMAGE_DIR, PAGE_SIZE, MAX_LIST_LOAD
from services.category_service import add_category, list_categories
from services.warehouse_service import add_warehouse, list_warehouses
from services.supplier_service import add_supplier, list_suppliers
from services.product_service import (
    add_product,
    delete_product,
    get_product_by_id,
    get_product_count,
    list_products,
    list_products_for_export,
    update_product,
)
from ui.components import section_title
from utils.pagination import clamp_page, get_offset, get_total_pages
from utils.export import products_to_excel, products_to_pdf, products_to_print_html


def _save_image(uploaded_file):
    if not uploaded_file:
        return None
    IMAGE_DIR.mkdir(exist_ok=True)
    ext = uploaded_file.name.split(".")[-1].lower()
    filename = f"{uuid4().hex}.{ext}"
    path = IMAGE_DIR / filename
    image = Image.open(uploaded_file)
    image.save(path)
    return str(path)


def _select_options(rows):
    return [{"id": None, "name": "None"}] + [{"id": r[0], "name": r[1]} for r in rows]


def _option_index(options, selected_id):
    for i, item in enumerate(options):
        if item["id"] == selected_id:
            return i
    return 0


def _parse_int(value, label, required=False, default=0):
    text = (value or "").strip()
    if not text:
        return (None, f"{label} is required.") if required else (default, None)
    try:
        return int(float(text)), None
    except ValueError:
        return None, f"{label} must be a whole number."


def _parse_float(value, label, required=False, default=0.0):
    text = (value or "").strip()
    if not text:
        return (None, f"{label} is required.") if required else (default, None)
    try:
        return float(text), None
    except ValueError:
        return None, f"{label} must be a number."


def render_products(show_add=True, show_manage=True, **_kwargs):
    st.markdown("## Products")
    if show_manage and not show_add:
        st.markdown(
            '<div style="margin-top:3px; color:#a1a7b3;">Manage Products</div>',
            unsafe_allow_html=True,
        )

    categories = _select_options(list_categories())
    warehouses = _select_options(list_warehouses())
    suppliers = _select_options(list_suppliers())

    if show_add:
        section_title("Add Product")

        # Show success message if exists
        if st.session_state.get("product_added"):
            st.success("Product added successfully!")
            st.session_state["product_added"] = False

        with st.form("add_product", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Product Name *")
                quantity = st.text_input("Quantity *")
                distributor_price = st.text_input("Supplier Price*")
            with col2:
                category = st.selectbox("Category", categories, format_func=lambda x: x["name"])
                low_stock_alert = st.text_input("Low Stock Alert")
                selling_price = st.text_input("Selling Price #")
            with col3:
                warehouse = st.selectbox("Warehouse", warehouses, format_func=lambda x: x["name"])
                rack_number = st.text_input("Warehouse Rack Number")
                supplier = st.selectbox("Supplier", suppliers, format_func=lambda x: x["name"])

            image_file = st.file_uploader("Product Image", type=["png", "jpg", "jpeg"])
            details = st.text_area("Product Details)")

            col4, col5, col6, col7 = st.columns(4)
            with col4:
                production_date = st.date_input("Production Date", value=None, key="add_prod_date")
            with col5:
                expiry_date = st.date_input("Expiry Date", value=None, key="add_exp_date")
            with col6:
                model = st.text_input("Model")
            with col7:
                sku = st.text_input("SKU")

            submitted = st.form_submit_button("Add Product")
            if submitted:
                qty_val, qty_err = _parse_int(quantity, "Quantity", required=True)
                low_val, low_err = _parse_int(low_stock_alert, "Low Stock Alert", required=False, default=0)
                dist_val, dist_err = _parse_float(distributor_price, "Supplier Price", required=True)
                sell_val, sell_err = _parse_float(selling_price, "Selling Price", required=True)
                errors = [e for e in [qty_err, low_err, dist_err, sell_err] if e]
                if errors:
                    for err in errors:
                        st.error(err)
                    return
                if not name.strip():
                    st.error("Product name is required.")
                elif qty_val <= 0 or sell_val <= 0 or dist_val <= 0:
                    st.error("Quantity and prices must be greater than zero.")
                else:
                    image_path = _save_image(image_file)
                    add_product(
                        {
                            "name": name.strip(),
                            "category_id": category["id"],
                            "warehouse_id": warehouse["id"],
                            "rack_number": rack_number.strip(),
                            "image_path": image_path,
                            "details": details.strip(),
                            "production_date": str(production_date) if production_date else None,
                            "expiry_date": str(expiry_date) if expiry_date else None,
                            "quantity": int(qty_val),
                            "low_stock_alert": int(low_val),
                            "distributor_price": float(dist_val),
                            "selling_price": float(sell_val),
                            "model": model.strip(),
                            "sku": sku.strip(),
                            "supplier_id": supplier["id"],
                        }
                    )
                    st.session_state["product_added"] = True
                    st.rerun()

    if not show_manage:
        return

    st.markdown("---")

    if "export_action" not in st.session_state:
        st.session_state["export_action"] = None
    if "export_ready" not in st.session_state:
        st.session_state["export_ready"] = False

    # Export buttons + Search on same line
    st.markdown('<div class="export-row-marker"></div>', unsafe_allow_html=True)
    export_cols = st.columns([1, 1, 1, 4, 2], gap="small")
    with export_cols[0]:
        if st.button("Export Excel"):
            st.session_state["export_action"] = "excel"
            st.session_state["export_ready"] = False
    with export_cols[1]:
        if st.button("Export PDF"):
            st.session_state["export_action"] = "pdf"
            st.session_state["export_ready"] = False
    with export_cols[2]:
        if st.button("Print Products"):
            st.session_state["export_action"] = "print"
            st.session_state["export_ready"] = False
    with export_cols[4]:
        search_query = st.text_input("🔍", label_visibility="collapsed", placeholder="Search...", key="prod_search")

    total_count = get_product_count(search_query)
    effective_total = min(total_count, MAX_LIST_LOAD)
    if total_count > MAX_LIST_LOAD:
        st.warning(
            f"Only the first {MAX_LIST_LOAD} products are available for listing "
            "to reduce memory usage. Consider cleaning older items."
        )

    total_pages = get_total_pages(effective_total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("product_page", 1), total_pages)

    if st.session_state.get("export_action"):
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="box">', unsafe_allow_html=True)
            export_scope = st.radio("Export Scope", ["All products", "Page range"], horizontal=True)
            start_page, end_page = 1, total_pages
            if export_scope == "Page range":
                start_page = st.number_input("From page", min_value=1, max_value=total_pages, value=1, step=1)
                end_page = st.number_input("To page", min_value=1, max_value=total_pages, value=total_pages, step=1)
                if end_page < start_page:
                    st.error("End page must be greater than or equal to start page.")

            st.markdown('<div class="export-action-marker"></div>', unsafe_allow_html=True)
            action_row = st.columns([1, 1, 8], gap="small")
            with action_row[0]:
                if st.button("Execute"):
                    st.session_state["export_ready"] = True
            with action_row[1]:
                if st.button("Cancel"):
                    st.session_state["export_action"] = None
                    st.session_state["export_ready"] = False
                    st.rerun()

            export_limit = PAGE_SIZE
            export_offset = 0
            if export_scope == "All products":
                export_limit = effective_total
                export_offset = 0
            else:
                export_offset = get_offset(start_page, PAGE_SIZE)
                export_limit = (end_page - start_page + 1) * PAGE_SIZE
                export_limit = min(export_limit, effective_total - export_offset)

            export_data = list_products_for_export(export_limit, export_offset) if export_limit > 0 else []

            if st.session_state.get("export_ready"):
                action = st.session_state.get("export_action")
                if action == "excel":
                    st.download_button(
                        "Download Excel",
                        data=products_to_excel(export_data) if export_data else b"",
                        file_name="products.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        disabled=not export_data,
                    )
                elif action == "pdf":
                    st.download_button(
                        "Download PDF",
                        data=products_to_pdf(export_data) if export_data else b"",
                        file_name="products.pdf",
                        mime="application/pdf",
                        disabled=not export_data,
                    )
                elif action == "print":
                    if export_data:
                        st.markdown("### Print Preview")
                        st.markdown(products_to_print_html(export_data), unsafe_allow_html=True)
                        st.info("Use your browser print command to print this table.")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="header-row-marker"></div>', unsafe_allow_html=True)
    # IMAGE, PRODUCT, CATEGORY, WAREHOUSE, SUPPLIER, SUPP.PRICE, SELL PRICE, QTY, OPTIONS
    header_cols = st.columns([1, 1.5, 1, 1, 1, 1, 1, 0.6, 2], gap="small")
    header_titles = [
        "IMAGE",
        "PRODUCT",
        "CATEGORY",
        "WAREHOUSE",
        "SUPPLIER",
        "SUPP. PRICE",
        "SELL PRICE",
        "QTY",
        "OPTIONS",
    ]
    for idx, title in enumerate(header_titles):
        with header_cols[idx]:
            st.markdown(f"<div class='header-cell'>{title}</div>", unsafe_allow_html=True)

    offset = get_offset(current_page, PAGE_SIZE)
    if offset >= effective_total:
        offset = max(0, effective_total - PAGE_SIZE)
    rows = list_products(PAGE_SIZE, offset, search_query) if effective_total > 0 else []

    if not rows:
        st.info("No products found.")
        return

    if "view_id" not in st.session_state:
        st.session_state["view_id"] = None
    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None

    for row in rows:
        (
            product_id,
            name,
            quantity,
            low_stock_alert,
            distributor_price,
            selling_price,
            image_path,
            category_name,
            warehouse_name,
            supplier_name,
            rack_number,
            details,
            production_date,
            expiry_date,
            model,
            sku,
        ) = row

        st.markdown('<div class="row-marker"></div>', unsafe_allow_html=True)
        with st.container():
            # IMAGE, PRODUCT, CATEGORY, WAREHOUSE, SUPPLIER, SUPP.PRICE, SELL PRICE, QTY, OPTIONS
            cols = st.columns([1, 1.5, 1, 1, 1, 1, 1, 0.6, 2], gap="small")
            with cols[0]:
                if image_path:
                    st.image(image_path, width=60)
                else:
                    st.caption("No img")
            with cols[1]:
                st.markdown(f"**{name}**")
            with cols[2]:
                st.markdown(category_name or "N/A")
            with cols[3]:
                st.markdown(warehouse_name or "N/A")
            with cols[4]:
                st.markdown(supplier_name or "N/A")
            with cols[5]:
                st.markdown(f"{distributor_price:.2f}")
            with cols[6]:
                st.markdown(f"{selling_price:.2f}")
            with cols[7]:
                st.markdown(f"{quantity}")
            with cols[8]:
                opt_cols = st.columns(3, gap="small")
                with opt_cols[0]:
                    view_btn = st.button("View", key=f"view_{product_id}")
                with opt_cols[1]:
                    edit_btn = st.button("Edit", key=f"edit_{product_id}")
                with opt_cols[2]:
                    delete_btn = st.button("Del", key=f"delete_{product_id}")

            if view_btn:
                st.session_state["view_id"] = product_id
                st.session_state["edit_id"] = None
            if edit_btn:
                st.session_state["edit_id"] = product_id
                st.session_state["view_id"] = None
            if delete_btn:
                delete_product(product_id)
                st.success("Product deleted.")
                st.rerun()

            if st.session_state.get("view_id") == product_id:
                product = get_product_by_id(product_id)
                if product:
                    (
                        _id,
                        name_v,
                        category_id_v,
                        warehouse_id_v,
                        rack_number_v,
                        image_path_v,
                        details_v,
                        production_date_v,
                        expiry_date_v,
                        quantity_v,
                        low_stock_alert_v,
                        distributor_price_v,
                        selling_price_v,
                        model_v,
                        sku_v,
                        supplier_id_v,
                    ) = product

                    st.markdown("### Product Details")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.text_input("Product Name #", value=name_v, disabled=True, key=f"view_name_{product_id}")
                        st.text_input("Quantity #", value=str(quantity_v), disabled=True, key=f"view_qty_{product_id}")
                        st.text_input("Distributor Price #", value=f"{distributor_price_v:.2f}", disabled=True, key=f"view_dist_{product_id}")
                    with col2:
                        st.text_input("Category", value=category_name or "N/A", disabled=True, key=f"view_cat_{product_id}")
                        st.text_input("Low Stock Alert", value=str(low_stock_alert_v), disabled=True, key=f"view_low_{product_id}")
                        st.text_input("Selling Price #", value=f"{selling_price_v:.2f}", disabled=True, key=f"view_sell_{product_id}")
                    with col3:
                        st.text_input("Warehouse", value=warehouse_name or "N/A", disabled=True, key=f"view_wh_{product_id}")
                        st.text_input("Warehouse Rack Number", value=rack_number_v or "", disabled=True, key=f"view_rack_{product_id}")
                        st.text_input("Supplier", value=supplier_name or "N/A", disabled=True, key=f"view_sup_{product_id}")

                    if image_path_v:
                        st.image(image_path_v, caption="Product Image", width=200)
                    
                    st.text_area("Product Details (Optional)", value=details_v or "", disabled=True, key=f"view_details_{product_id}", height=100)

                    col4, col5, col6, col7 = st.columns(4)
                    with col4:
                        st.text_input("Production Date (Optional)", value=production_date_v or "", disabled=True, key=f"view_prod_{product_id}")
                    with col5:
                        st.text_input("Expiry Date (Optional)", value=expiry_date_v or "", disabled=True, key=f"view_exp_{product_id}")
                    with col6:
                        st.text_input("Model", value=model_v or "", disabled=True, key=f"view_model_{product_id}")
                    with col7:
                        st.text_input("SKU", value=sku_v or "", disabled=True, key=f"view_sku_{product_id}")
                    
                    if st.button("Close View", key=f"close_view_{product_id}"):
                        st.session_state["view_id"] = None
                        st.rerun()

            if st.session_state.get("edit_id") == product_id:
                product = get_product_by_id(product_id)
                if product:
                    (
                        _id,
                        name_v,
                        category_id_v,
                        warehouse_id_v,
                        rack_number_v,
                        image_path_v,
                        details_v,
                        production_date_v,
                        expiry_date_v,
                        quantity_v,
                        low_stock_alert_v,
                        distributor_price_v,
                        selling_price_v,
                        model_v,
                        sku_v,
                        supplier_id_v,
                    ) = product

                    with st.form(f"edit_form_{product_id}"):
                        name_edit = st.text_input("Product Name", value=name_v)
                        category_edit = st.selectbox(
                            "Category",
                            categories,
                            index=_option_index(categories, category_id_v),
                            format_func=lambda x: x["name"],
                        )
                        warehouse_edit = st.selectbox(
                            "Warehouse",
                            warehouses,
                            index=_option_index(warehouses, warehouse_id_v),
                            format_func=lambda x: x["name"],
                        )
                        supplier_edit = st.selectbox(
                            "Supplier",
                            suppliers,
                            index=_option_index(suppliers, supplier_id_v),
                            format_func=lambda x: x["name"],
                        )
                        rack_edit = st.text_input("Warehouse Rack Number", value=rack_number_v or "")
                        quantity_edit = st.text_input("Quantity", value=str(quantity_v))
                        low_stock_edit = st.text_input("Low Stock Alert", value=str(low_stock_alert_v))
                        distributor_edit = st.text_input("Supplier Price", value=f"{distributor_price_v:.2f}")
                        selling_edit = st.text_input("Selling Price", value=f"{selling_price_v:.2f}")
                        image_edit = st.file_uploader(
                            "Product Image (Optional)", type=["png", "jpg", "jpeg"], key=f"edit_image_{product_id}"
                        )
                        details_edit = st.text_area("Product Details", value=details_v or "")
                        prod_date_val = None
                        if production_date_v:
                            try:
                                prod_date_val = date.fromisoformat(production_date_v)
                            except (ValueError, TypeError):
                                pass
                        production_edit = st.date_input(
                            "Production Date (Optional)",
                            value=prod_date_val,
                            key=f"edit_prod_date_{product_id}",
                        )
                        exp_date_val = None
                        if expiry_date_v:
                            try:
                                exp_date_val = date.fromisoformat(expiry_date_v)
                            except (ValueError, TypeError):
                                pass
                        expiry_edit = st.date_input(
                            "Expiry Date (Optional)",
                            value=exp_date_val,
                            key=f"edit_exp_date_{product_id}",
                        )
                        model_edit = st.text_input("Model", value=model_v or "")
                        sku_edit = st.text_input("SKU", value=sku_v or "")

                        save_btn = st.form_submit_button("Save Changes")
                        if save_btn:
                            qty_val, qty_err = _parse_int(quantity_edit, "Quantity", required=True)
                            low_val, low_err = _parse_int(
                                low_stock_edit, "Low Stock Alert", required=False, default=0
                            )
                            dist_val, dist_err = _parse_float(
                                distributor_edit, "Supplier Price", required=True
                            )
                            sell_val, sell_err = _parse_float(
                                selling_edit, "Selling Price", required=True
                            )
                            errors = [e for e in [qty_err, low_err, dist_err, sell_err] if e]
                            if errors:
                                for err in errors:
                                    st.error(err)
                                return
                            new_image_path = image_path_v
                            if image_edit:
                                new_image_path = _save_image(image_edit)
                            update_product(
                                product_id,
                                {
                                    "name": name_edit.strip(),
                                    "category_id": category_edit["id"],
                                    "warehouse_id": warehouse_edit["id"],
                                    "rack_number": rack_edit.strip(),
                                    "image_path": new_image_path,
                                    "details": details_edit.strip(),
                                    "production_date": str(production_edit) if production_edit else None,
                                    "expiry_date": str(expiry_edit) if expiry_edit else None,
                                    "quantity": int(qty_val),
                                    "low_stock_alert": int(low_val),
                                    "distributor_price": float(dist_val),
                                    "selling_price": float(sell_val),
                                    "model": model_edit.strip(),
                                    "sku": sku_edit.strip(),
                                    "supplier_id": supplier_edit["id"],
                                },
                            )
                            st.success("Product updated.")
                            st.rerun()


    # Pagination Box
    st.markdown(
        f"""
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-btn" {'disabled' if current_page == 1 else ''}>Previous</button>
            <div class="page-number">Page {current_page} / {total_pages}</div>
            <button class="pagination-btn" id="next-btn" {'disabled' if current_page == total_pages else ''}>Next</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1, key="prev_hidden"):
            st.session_state["product_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages, key="next_hidden"):
            st.session_state["product_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



def render_products_add():
    render_products(show_add=True, show_manage=False)


def render_products_manage():
    render_products(show_add=False, show_manage=True)
