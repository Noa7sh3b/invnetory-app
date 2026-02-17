"""
Invoices Page – Invoice creation and management.

Provides interfaces for:
- Creating new invoices with multiple product items
- Managing invoices (view/edit/delete)
- Tracking invoice payment status (paid/unpaid/partial)
- Updating invoice payments
- Exporting invoices and printing
"""

import streamlit as st
from datetime import date, datetime

from config import PAGE_SIZE
from services.invoice_service import (
    generate_invoice_number,
    list_products_for_invoice,
    get_product_for_invoice,
    validate_quantity,
    create_invoice,
    get_invoice,
    get_invoice_items,
    update_invoice_payment,
    delete_invoice,
    get_invoice_count,
    list_invoices_paginated,
    list_invoices_for_export,
    get_invoice_for_print,
)
from services.customer_service import list_customers
from utils.pagination import clamp_page, get_offset, get_total_pages
from utils.export import products_to_excel, products_to_pdf


def render_invoices_create():
    st.markdown("## Invoices")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Create Invoice</p>", unsafe_allow_html=True)

    # Initialize session state
    if "invoice_items" not in st.session_state:
        st.session_state["invoice_items"] = []
    if "invoice_created" not in st.session_state:
        st.session_state["invoice_created"] = False

    # Show success message
    if st.session_state.get("invoice_created"):
        st.success("Invoice created successfully!")
        st.session_state["invoice_created"] = False
        st.session_state["invoice_items"] = []

    # Get customers and products
    customers = list_customers()
    products = list_products_for_invoice()

    if not customers:
        st.warning("No customers found. Please add customers first.")
        return

    if not products:
        st.warning("No products in stock. Please add products first.")
        return

    # Customer options
    customer_options = [{"id": c[0], "cust_id": c[1], "name": c[2]} for c in customers]

    # Product options
    product_options = [{"id": p[0], "name": p[1], "sku": p[2], "price": p[3], "stock": p[4]} for p in products]

    # Invoice Header
    st.markdown("### Invoice Details")
    col1, col2 = st.columns(2)
    with col1:
        selected_customer = st.selectbox(
            "Customer Name *",
            customer_options,
            format_func=lambda x: f"{x['name']} ({x['cust_id'] or 'N/A'})",
            key="inv_customer"
        )
        invoice_date = st.date_input("Invoice Date *", value=date.today(), key="inv_date")
    with col2:
        # Show auto-generated invoice number preview
        preview_inv_num = generate_invoice_number()
        st.text_input("Invoice Number (Auto)", value=preview_inv_num, disabled=True)

    st.markdown("---")

    # Add Product Section
    st.markdown("### Add Products")

    with st.form("add_product_form", clear_on_submit=True):
        add_col1, add_col2, add_col3 = st.columns([3, 1, 1])
        with add_col1:
            product_index = st.selectbox(
                "Select Product",
                range(len(product_options)),
                format_func=lambda i: f"{product_options[i]['name']} | SKU: {product_options[i]['sku'] or 'N/A'} | Price: {product_options[i]['price']:.2f} | Stock: {product_options[i]['stock']}",
                key="inv_product_select"
            )
        with add_col2:
            quantity_str = st.text_input("Quantity *", placeholder="0", key="inv_qty")
        with add_col3:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            add_btn = st.form_submit_button("+ Add Product", use_container_width=True)
        
        if add_btn:
            selected_product = product_options[product_index]
            try:
                qty = int(quantity_str) if quantity_str.strip() else 0
            except ValueError:
                qty = 0

            if qty <= 0:
                st.error("Quantity must be greater than 0")
            elif qty > selected_product["stock"]:
                st.error(f"Not enough stock! Available: {selected_product['stock']}")
            else:
                # Check if product already in list
                existing = next((i for i, item in enumerate(st.session_state["invoice_items"]) 
                                if item["product_id"] == selected_product["id"]), None)
                if existing is not None:
                    # Update quantity
                    new_qty = st.session_state["invoice_items"][existing]["quantity"] + qty
                    if new_qty > selected_product["stock"]:
                        st.error(f"Total quantity exceeds stock! Available: {selected_product['stock']}")
                    else:
                        st.session_state["invoice_items"][existing]["quantity"] = new_qty
                        st.session_state["invoice_items"][existing]["total"] = new_qty * selected_product["price"]
                        st.rerun()
                else:
                    # Add new item
                    st.session_state["invoice_items"].append({
                        "product_id": selected_product["id"],
                        "name": selected_product["name"],
                        "sku": selected_product["sku"],
                        "price": selected_product["price"],
                        "quantity": qty,
                        "total": qty * selected_product["price"],
                        "stock": selected_product["stock"]
                    })
                    st.rerun()

    # Show added products
    if st.session_state["invoice_items"]:
        st.markdown("### Invoice Items")
        
        # Table header
        st.markdown('<div class="cust-table-marker"></div>', unsafe_allow_html=True)
        header_cols = st.columns([2, 1.5, 1, 1, 1.5, 0.8], gap="small")
        headers = ["Product Name", "SKU", "Price", "Qty", "Total", ""]
        for idx, h in enumerate(headers):
            with header_cols[idx]:
                st.markdown(f"**{h}**")

        # Items
        for idx, item in enumerate(st.session_state["invoice_items"]):
            st.markdown('<div class="cust-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([2, 1.5, 1, 1, 1.5, 0.8], gap="small")
            with row_cols[0]:
                st.markdown(item["name"])
            with row_cols[1]:
                st.markdown(item["sku"] or "N/A")
            with row_cols[2]:
                st.markdown(f"{item['price']:.2f}")
            with row_cols[3]:
                st.markdown(str(item["quantity"]))
            with row_cols[4]:
                st.markdown(f"{item['total']:.2f}")
            with row_cols[5]:
                if st.button("✕", key=f"remove_item_{idx}"):
                    st.session_state["invoice_items"].pop(idx)
                    st.rerun()

        st.markdown("---")

        # Calculate subtotal
        subtotal = sum(item["total"] for item in st.session_state["invoice_items"])

        # Discount and Payment Section
        st.markdown("### Payment Details")
        pay_col1, pay_col2 = st.columns(2)
        with pay_col1:
            discount_str = st.text_input("Discount", placeholder="0.00", key="inv_discount")
            try:
                discount = float(discount_str) if discount_str.strip() else 0.0
            except ValueError:
                discount = 0.0

        total = subtotal - discount
        if total < 0:
            total = 0.0

        with pay_col2:
            paid_amount_str = st.text_input("Paid Amount", placeholder="0.00", key="inv_paid")
            try:
                paid_amount = float(paid_amount_str) if paid_amount_str.strip() else 0.0
            except ValueError:
                paid_amount = 0.0

        due_amount = total - paid_amount
        if due_amount < 0:
            due_amount = 0.0

        # Summary (Read-only display)
        st.markdown("### Invoice Summary")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        with summary_col1:
            st.markdown(f"""
                <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center;'>
                    <p style='margin:0; color:#888; font-size:12px;'>Subtotal</p>
                    <p style='margin:0; font-size:20px; font-weight:bold;'>{subtotal:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with summary_col2:
            st.markdown(f"""
                <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center;'>
                    <p style='margin:0; color:#888; font-size:12px;'>Discount</p>
                    <p style='margin:0; font-size:20px; font-weight:bold; color:#ff6b6b;'>-{discount:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with summary_col3:
            st.markdown(f"""
                <div style='background:#1e88ff; padding:15px; border-radius:8px; text-align:center;'>
                    <p style='margin:0; color:#fff; font-size:12px;'>Total</p>
                    <p style='margin:0; font-size:20px; font-weight:bold; color:#fff;'>{total:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        with summary_col4:
            due_color = "#ff6b6b" if due_amount > 0 else "#4ade80"
            st.markdown(f"""
                <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center;'>
                    <p style='margin:0; color:#888; font-size:12px;'>Due Amount</p>
                    <p style='margin:0; font-size:20px; font-weight:bold; color:{due_color};'>{due_amount:.2f}</p>
                </div>
            """, unsafe_allow_html=True)

        # Notes
        notes = st.text_area("Notes (Optional)", key="inv_notes", height=80)

        # Submit button
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, _ = st.columns([1, 1, 4])
        with col_btn1:
            if st.button("Submit Invoice", type="primary", use_container_width=True):
                if paid_amount > total:
                    st.error(f"Paid amount ({paid_amount:.2f}) cannot exceed total ({total:.2f})")
                else:
                    items_to_create = [{"product_id": item["product_id"], "quantity": item["quantity"]} 
                                       for item in st.session_state["invoice_items"]]
                    success, message, invoice_id = create_invoice(
                        customer_id=selected_customer["id"],
                        invoice_date=str(invoice_date),
                        items=items_to_create,
                        discount=discount,
                        paid_amount=paid_amount,
                        notes=notes
                    )
                    if success:
                        st.session_state["invoice_created"] = True
                        st.rerun()
                    else:
                        st.error(message)
        with col_btn2:
            if st.button("Clear All", use_container_width=True):
                st.session_state["invoice_items"] = []
                st.rerun()
    else:
        st.info("No products added yet. Select a product and quantity to add.")


def render_invoices_manage():
    st.markdown("## Invoices")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Manage Invoices</p>", unsafe_allow_html=True)

    # Initialize session state
    if "invoice_page" not in st.session_state:
        st.session_state["invoice_page"] = 1
    if "invoice_view_id" not in st.session_state:
        st.session_state["invoice_view_id"] = None
    if "invoice_edit_id" not in st.session_state:
        st.session_state["invoice_edit_id"] = None

    # Handle View Mode
    if st.session_state.get("invoice_view_id"):
        inv_id = st.session_state["invoice_view_id"]
        invoice = get_invoice(inv_id)
        items = get_invoice_items(inv_id)
        
        if invoice:
            st.markdown("### View Invoice")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Invoice Number:** {invoice[1]}")
                st.markdown(f"**Customer:** {invoice[3] or 'N/A'}")
                st.markdown(f"**Date:** {invoice[4]}")
            with col2:
                status = invoice[10]
                if status == "paid":
                    status_display = ":green[Paid]"
                elif status == "partial":
                    status_display = ":orange[Partial]"
                else:
                    status_display = ":red[Unpaid]"
                st.markdown(f"**Status:** {status_display}")
                st.markdown(f"**Total:** {invoice[7]:.2f}")
                st.markdown(f"**Paid:** {invoice[8]:.2f}")
                st.markdown(f"**Due:** {invoice[9]:.2f}")

            st.markdown("#### Items")
            if items:
                for item in items:
                    st.markdown(f"- **{item[2]}** (SKU: {item[3] or 'N/A'}) | Qty: {item[4]} × {item[5]:.2f} = **{item[6]:.2f}**")
            
            if invoice[11]:
                st.markdown(f"**Notes:** {invoice[11]}")

            if st.button("Close View", key="close_view_inv"):
                st.session_state["invoice_view_id"] = None
                st.rerun()
        return

    # Handle Edit Mode (Payment only)
    if st.session_state.get("invoice_edit_id"):
        inv_id = st.session_state["invoice_edit_id"]
        invoice = get_invoice(inv_id)
        
        if invoice:
            st.markdown("### Edit Invoice Payment")
            st.markdown(f"**Invoice:** {invoice[1]} | **Customer:** {invoice[3]} | **Total:** {invoice[7]:.2f}")
            
            with st.form("edit_invoice_form"):
                edit_paid_str = st.text_input("Paid Amount *", value=f"{invoice[8]:.2f}", key="edit_inv_paid")
                edit_notes = st.text_area("Notes", value=invoice[11] or "", key="edit_inv_notes", height=80)
                
                btn_col1, btn_col2, _ = st.columns([1, 1, 4])
                with btn_col1:
                    save = st.form_submit_button("Save Changes")
                with btn_col2:
                    cancel = st.form_submit_button("Cancel")
                
                if save:
                    try:
                        edit_paid = float(edit_paid_str) if edit_paid_str.strip() else 0.0
                    except ValueError:
                        edit_paid = 0.0
                    
                    success, message = update_invoice_payment(inv_id, edit_paid, edit_notes)
                    if success:
                        st.session_state["invoice_edit_id"] = None
                        st.success("Invoice payment updated!")
                        st.rerun()
                    else:
                        st.error(message)
                
                if cancel:
                    st.session_state["invoice_edit_id"] = None
                    st.rerun()
        return

    # Export & Search Section
    export_col1, export_col2, export_col3, export_col4 = st.columns([1, 1, 1, 3])
    
    # Get current filters for export
    search_query = st.session_state.get("inv_search", "")
    status_filter_val = st.session_state.get("inv_status_filter", "All")
    status_val = "" if status_filter_val == "All" else status_filter_val
    
    with export_col1:
        invoices_for_print = list_invoices_for_export(search_query, status_val)
        if invoices_for_print:
            print_html = generate_print_html(invoices_for_print)
            st.download_button(
                "🖨️ Print",
                data=print_html,
                file_name=f"invoices_print_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True,
                help="Download and open the file to print"
            )
        else:
            st.button("🖨️ Print", disabled=True, use_container_width=True, help="No invoices to print")
    with export_col2:
        invoices_export = list_invoices_for_export(search_query, status_val)
        if invoices_export:
            excel_data = invoices_to_excel(invoices_export)
            st.download_button(
                "📥 Excel",
                data=excel_data,
                file_name=f"invoices_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📥 Excel", disabled=True, use_container_width=True)
    with export_col3:
        if invoices_export:
            pdf_data = invoices_to_pdf(invoices_export)
            st.download_button(
                "📄 PDF",
                data=pdf_data,
                file_name=f"invoices_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.button("📄 PDF", disabled=True, use_container_width=True)

    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns([2, 3, 1.5], gap="small")
    with filter_col1:
        status_filter = st.selectbox("Filter by Status", ["All", "paid", "partial", "unpaid"], key="inv_status_filter")
    with filter_col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_query = st.text_input("Search", label_visibility="collapsed", placeholder="Search...", key="inv_search")

    status_val = "" if status_filter == "All" else status_filter

    # Get data
    total = get_invoice_count(search_query, status_val)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("invoice_page", 1), total_pages)
    st.session_state["invoice_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_invoices_paginated(offset, PAGE_SIZE, search_query, status_val)

    # Table header
    st.markdown('<div class="cust-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1.5, 2, 1.2, 1.5, 1, 1, 1, 1, 2], gap="small")
    headers = ["Invoice #", "Customer", "Date", "Products", "Total", "Paid", "Due", "Status", "Options"]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    if total == 0:
        st.info("No invoices found.")
    else:
        for row in rows:
            inv_id, inv_num, customer_name, inv_date, item_count, first_product, total_amt, paid_amt, due_amt, status = row
            
            # Format products display
            if item_count == 1:
                product_display = first_product or "N/A"
            else:
                product_display = f"{item_count} items"

            st.markdown('<div class="cust-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1.5, 2, 1.2, 1.5, 1, 1, 1, 1, 2], gap="small")
            with row_cols[0]:
                st.markdown(inv_num or "N/A")
            with row_cols[1]:
                st.markdown(customer_name or "N/A")
            with row_cols[2]:
                st.markdown(inv_date or "N/A")
            with row_cols[3]:
                st.markdown(product_display[:20] + "..." if len(product_display) > 20 else product_display)
            with row_cols[4]:
                st.markdown(f"{total_amt:.2f}")
            with row_cols[5]:
                st.markdown(f"{paid_amt:.2f}")
            with row_cols[6]:
                st.markdown(f"{due_amt:.2f}")
            with row_cols[7]:
                if status == "paid":
                    st.markdown(":green[Paid]")
                elif status == "partial":
                    st.markdown(":orange[Partial]")
                else:
                    st.markdown(":red[Unpaid]")
            with row_cols[8]:
                opt_cols = st.columns(3, gap="small")
                with opt_cols[0]:
                    st.button("View", key=f"view_inv_{inv_id}", on_click=lambda id=inv_id: st.session_state.update({"invoice_view_id": id}))
                with opt_cols[1]:
                    st.button("Edit", key=f"edit_inv_{inv_id}", on_click=lambda id=inv_id: st.session_state.update({"invoice_edit_id": id}))
                with opt_cols[2]:
                    if st.button("Del", key=f"del_inv_{inv_id}"):
                        success, message = delete_invoice(inv_id)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                        st.rerun()

    # Pagination Box
    st.markdown(
        f'''
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-inv" {"disabled" if current_page == 1 else ""}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-inv" {"disabled" if current_page == total_pages else ""}>Next</button>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="inv_prev_hidden"):
            st.session_state["invoice_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="inv_next_hidden"):
            st.session_state["invoice_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_invoices_status():
    st.markdown("## Invoices")
    st.markdown("<p style='margin-top:-15px; font-size:14px; color:#888;'>Paid / Unpaid Invoices</p>", unsafe_allow_html=True)

    # Initialize session state
    if "inv_status_page" not in st.session_state:
        st.session_state["inv_status_page"] = 1

    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns([2, 3, 1.5], gap="small")
    with filter_col1:
        status_filter = st.selectbox("Filter by Status", ["All", "paid", "partial", "unpaid"], key="inv_st_filter")
    with filter_col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_query = st.text_input("Search", label_visibility="collapsed", placeholder="Search...", key="inv_st_search")

    status_val = "" if status_filter == "All" else status_filter

    # Get data
    total = get_invoice_count(search_query, status_val)
    total_pages = get_total_pages(total, PAGE_SIZE)
    current_page = clamp_page(st.session_state.get("inv_status_page", 1), total_pages)
    st.session_state["inv_status_page"] = current_page

    offset = get_offset(current_page, PAGE_SIZE)
    rows = list_invoices_paginated(offset, PAGE_SIZE, search_query, status_val)

    # Summary cards
    paid_count = get_invoice_count("", "paid")
    partial_count = get_invoice_count("", "partial")
    unpaid_count = get_invoice_count("", "unpaid")

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    with summary_col1:
        st.markdown(f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #4ade80;'>
                <p style='margin:0; color:#888; font-size:12px;'>Paid Invoices</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#4ade80;'>{paid_count}</p>
            </div>
        """, unsafe_allow_html=True)
    with summary_col2:
        st.markdown(f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #fbbf24;'>
                <p style='margin:0; color:#888; font-size:12px;'>Partial Invoices</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#fbbf24;'>{partial_count}</p>
            </div>
        """, unsafe_allow_html=True)
    with summary_col3:
        st.markdown(f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #ff6b6b;'>
                <p style='margin:0; color:#888; font-size:12px;'>Unpaid Invoices</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#ff6b6b;'>{unpaid_count}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Table header
    st.markdown('<div class="cust-table-marker"></div>', unsafe_allow_html=True)
    header_cols = st.columns([1.5, 2, 1.2, 1.2, 1.2, 1.2, 1], gap="small")
    headers = ["Invoice #", "Customer", "Total", "Paid", "Due", "Status", ""]
    for idx, h in enumerate(headers):
        with header_cols[idx]:
            st.markdown(f"**{h}**")

    if total == 0:
        st.info("No invoices found.")
    else:
        for row in rows:
            inv_id, inv_num, customer_name, inv_date, item_count, first_product, total_amt, paid_amt, due_amt, status = row

            st.markdown('<div class="cust-row-marker"></div>', unsafe_allow_html=True)
            row_cols = st.columns([1.5, 2, 1.2, 1.2, 1.2, 1.2, 1], gap="small")
            with row_cols[0]:
                st.markdown(inv_num or "N/A")
            with row_cols[1]:
                st.markdown(customer_name or "N/A")
            with row_cols[2]:
                st.markdown(f"{total_amt:.2f}")
            with row_cols[3]:
                st.markdown(f"{paid_amt:.2f}")
            with row_cols[4]:
                st.markdown(f"{due_amt:.2f}")
            with row_cols[5]:
                if status == "paid":
                    st.markdown(":green[Paid]")
                elif status == "partial":
                    st.markdown(":orange[Partial]")
                else:
                    st.markdown(":red[Unpaid]")
            with row_cols[6]:
                if st.button("View", key=f"view_inv_st_{inv_id}"):
                    st.session_state["page"] = "invoices_manage"
                    st.session_state["invoice_view_id"] = inv_id
                    st.rerun()

    # Pagination Box
    st.markdown(
        f'''
        <div class="pagination-box">
            <button class="pagination-btn" id="prev-inv-st" {"disabled" if current_page == 1 else ""}>Previous</button>
            <div class="page-number">Page {current_page} / {max(total_pages, 1)}</div>
            <button class="pagination-btn" id="next-inv-st" {"disabled" if current_page == total_pages else ""}>Next</button>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    # Hidden functional Streamlit buttons for pagination
    st.markdown('<div class="hidden-pagination-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("p", disabled=current_page == 1 or total_pages == 0, key="inv_st_prev_hidden"):
            st.session_state["inv_status_page"] = current_page - 1
            st.rerun()
    with col3:
        if st.button("n", disabled=current_page == total_pages or total_pages == 0, key="inv_st_next_hidden"):
            st.session_state["inv_status_page"] = current_page + 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



# Export helper functions
def invoices_to_excel(invoices):
    """Convert invoices to Excel format"""
    from io import BytesIO
    import pandas as pd
    
    df = pd.DataFrame(invoices)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Invoices")
    output.seek(0)
    return output.read()


def invoices_to_pdf(invoices):
    """Convert invoices to PDF format"""
    from io import BytesIO
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(A4))
    data = [list(invoices[0].keys())] if invoices else [["No data"]]
    for item in invoices:
        data.append([str(value) for value in item.values()])
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e88ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    doc.build([table])
    output.seek(0)
    return output.read()


def generate_print_html(invoices):
    """Generate HTML for printing invoices"""
    if not invoices:
        return "<html><body><h1>No invoices to print</h1></body></html>"
    
    # Build table rows
    headers = list(invoices[0].keys())
    header_html = "".join(f"<th>{h.replace('_', ' ').title()}</th>" for h in headers)
    
    rows_html = ""
    for inv in invoices:
        cols = "".join(f"<td>{v}</td>" for v in inv.values())
        rows_html += f"<tr>{cols}</tr>"
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Invoices Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #fff;
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #1e88ff;
            color: white;
            padding: 12px 8px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        td {{
            padding: 10px 8px;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .print-info {{
            display: flex;
            justify-content: space-between;
            color: #666;
            font-size: 12px;
            margin-bottom: 10px;
        }}
        .print-btn {{
            background: #1e88ff;
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin: 20px auto;
            display: block;
        }}
        .print-btn:hover {{
            background: #1565c0;
        }}
        @media print {{
            .print-btn {{
                display: none;
            }}
            body {{
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <h1>📄 Invoices Report</h1>
    <div class="print-info">
        <span>Total: {len(invoices)} invoices</span>
        <span>Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
    </div>
    <button class="print-btn" onclick="window.print()">🖨️ Print Now</button>
    <table>
        <thead>
            <tr>{header_html}</tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    <button class="print-btn" onclick="window.print()">🖨️ Print Now</button>
</body>
</html>"""
