"""
Settings Pages Module – Store configuration, currency, low-stock alerts & Read Me.

Each ``render_settings_*`` function is a self-contained Streamlit page.
Hard-coded values (prices, contact info) are pulled from ``config.py``
so they can be changed in a single place.
"""

import os
import streamlit as st

from config import (
    APP_NAME,
    APP_VERSION,
    APP_LAST_UPDATE,
    # Commercial offer prices
    SUPPORT_6_MONTHS_PRICE,
    SUPPORT_12_MONTHS_PRICE,
    SUPPORT_EXTRA_3_MONTHS_PRICE,
    UPDATES_6_MONTHS_PRICE,
    UPDATES_12_MONTHS_PRICE,
    UPDATES_18_MONTHS_PRICE,
    CUSTOM_SIMPLE_PRICE,
    CUSTOM_MEDIUM_PRICE,
    CUSTOM_COMPLEX_PRICE,
    # Contact info
    CONTACT_TELEGRAM_USER,
    CONTACT_TELEGRAM_URL,
    CONTACT_WHATSAPP_NUMBER,
    CONTACT_WHATSAPP_URL,
)
from services.settings_service import (
    get_setting,
    update_setting,
    get_all_settings,
    save_store_logo,
    CURRENCY_OPTIONS,
)


# ── Store Settings ─────────────────────────────────────────────────────────


def render_settings_store():
    """Render Store Settings page – logo upload & store-name form."""
    st.markdown("## Settings")
    st.markdown(
        "<p style='margin-top:-15px; font-size:14px; color:#888;'>Store Settings</p>",
        unsafe_allow_html=True,
    )

    # Flash success message if the previous action succeeded
    if st.session_state.get("store_name_updated"):
        st.success("Store settings updated successfully!")
        st.session_state["store_name_updated"] = False

    current_name = get_setting("store_name", "My Store")
    current_logo = get_setting("store_logo", "")

    # ── Logo section ──────────────────────────────────────────────────
    st.markdown("### Store Logo")

    if current_logo and os.path.exists(current_logo):
        col_logo, col_upload = st.columns([1, 2])
        with col_logo:
            st.image(current_logo, width=120)
            st.caption("Current Logo")
        with col_upload:
            logo_upload = st.file_uploader(
                "Upload New Logo",
                type=["png", "jpg", "jpeg"],
                key="store_logo_upload",
                help="Recommended: Square image, 200×200 px or larger",
            )
            if logo_upload and st.button("Save Logo", key="save_logo_btn"):
                save_store_logo(logo_upload)
                st.session_state["store_name_updated"] = True
                st.rerun()
    else:
        logo_upload = st.file_uploader(
            "Upload Store Logo",
            type=["png", "jpg", "jpeg"],
            key="store_logo_upload",
            help="Recommended: Square image, 200×200 px or larger",
        )
        if logo_upload and st.button("Save Logo", key="save_logo_btn"):
            save_store_logo(logo_upload)
            st.session_state["store_name_updated"] = True
            st.rerun()

    st.markdown("---")

    # ── Store name section ────────────────────────────────────────────
    st.markdown("### Store Name")
    with st.form("store_settings_form"):
        store_name = st.text_input(
            "Store Name *",
            value=current_name,
            help="This name will appear in the sidebar",
        )
        submitted = st.form_submit_button("Save Changes", use_container_width=False)
        if submitted:
            if not store_name.strip():
                st.error("Store name is required.")
            else:
                update_setting("store_name", store_name.strip())
                st.session_state["store_name_updated"] = True
                st.rerun()


# ── Currency Settings ──────────────────────────────────────────────────────


def render_settings_currency():
    """Render Currency settings page – code, symbol, position, decimals."""
    st.markdown("## Settings")
    st.markdown(
        "<p style='margin-top:-15px; font-size:14px; color:#888;'>Currency</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.get("currency_updated"):
        st.success("Currency settings updated successfully!")
        st.session_state["currency_updated"] = False

    current_currency = get_setting("currency_code", "USD")
    current_symbol = get_setting("currency_symbol", "$")
    current_position = get_setting("currency_position", "before")

    with st.form("currency_settings_form"):
        st.markdown("### Currency Configuration")

        col1, col2 = st.columns(2)
        with col1:
            currency_codes = [c["code"] for c in CURRENCY_OPTIONS]
            try:
                current_index = currency_codes.index(current_currency)
            except ValueError:
                current_index = 0

            selected_currency = st.selectbox(
                "Currency",
                CURRENCY_OPTIONS,
                index=current_index,
                format_func=lambda x: f"{x['name']} ({x['code']}) - {x['symbol']}",
            )
            custom_symbol = st.text_input(
                "Custom Symbol (Optional)",
                value="" if current_symbol == selected_currency["symbol"] else current_symbol,
                help="Leave empty to use the default symbol",
            )

        with col2:
            position_options = ["before", "after"]
            position_index = (
                position_options.index(current_position)
                if current_position in position_options
                else 0
            )
            currency_position = st.selectbox(
                "Symbol Position",
                position_options,
                index=position_index,
                format_func=lambda x: (
                    "Before amount ($100)" if x == "before" else "After amount (100$)"
                ),
            )
            decimal_places = st.selectbox(
                "Decimal Places",
                [0, 1, 2, 3],
                index=2,
                help="Number of decimal places for prices",
            )

        submitted = st.form_submit_button("Save Changes", use_container_width=False)
        if submitted:
            final_symbol = (
                custom_symbol.strip()
                if custom_symbol.strip()
                else selected_currency["symbol"]
            )
            update_setting("currency_code", selected_currency["code"])
            update_setting("currency_symbol", final_symbol)
            update_setting("currency_position", currency_position)
            update_setting("decimal_places", str(decimal_places))
            st.session_state["currency_updated"] = True
            st.rerun()

    # Live preview
    st.markdown("---")
    st.markdown("### Preview")
    symbol = (
        custom_symbol.strip()
        if custom_symbol.strip()
        else selected_currency["symbol"]
    )
    example_amount = "1,234.56"
    formatted = (
        f"{symbol}{example_amount}"
        if current_position == "before"
        else f"{example_amount}{symbol}"
    )
    st.markdown(
        f"""
        <div style='background:#1a1a2e; padding:20px; border-radius:8px; text-align:center;'>
            <p style='margin:0; color:#888; font-size:14px;'>Amount Display</p>
            <p style='margin:10px 0 0 0; font-size:32px; font-weight:bold; color:#4ade80;'>{formatted}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Low-Stock Alert Threshold ──────────────────────────────────────────────


def render_settings_low_stock():
    """Render Low Stock Alert Threshold settings page."""
    st.markdown("## Settings")
    st.markdown(
        "<p style='margin-top:-15px; font-size:14px; color:#888;'>Low Stock Alert Threshold</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.get("low_stock_updated"):
        st.success("Low stock settings updated successfully!")
        st.session_state["low_stock_updated"] = False

    current_threshold = int(get_setting("default_low_stock_threshold", "10"))
    current_enabled = get_setting("low_stock_alerts_enabled", "true") == "true"

    with st.form("low_stock_settings_form"):
        st.markdown("### Low Stock Alert Configuration")
        st.info(
            "💡 Each product can have its own low stock alert level. "
            "The settings below are defaults for new products."
        )

        col1, col2 = st.columns(2)
        with col1:
            alerts_enabled = st.checkbox(
                "Enable Low Stock Alerts",
                value=current_enabled,
                help="Show warnings when products are running low",
            )
            default_threshold = st.number_input(
                "Default Low Stock Threshold",
                min_value=0,
                max_value=1000,
                value=current_threshold,
                step=1,
                help="Default minimum quantity before showing low stock warning",
            )
        with col2:
            st.markdown("##### Alert Levels")
            critical_level = st.number_input(
                "Critical Level (Red)",
                min_value=0,
                max_value=100,
                value=int(get_setting("critical_stock_level", "5")),
                step=1,
                help="Show red warning when stock falls below this",
            )
            warning_level = st.number_input(
                "Warning Level (Yellow)",
                min_value=0,
                max_value=100,
                value=int(get_setting("warning_stock_level", "10")),
                step=1,
                help="Show yellow warning when stock falls below this",
            )

        submitted = st.form_submit_button("Save Changes", use_container_width=False)
        if submitted:
            if warning_level <= critical_level:
                st.error("Warning level must be greater than critical level.")
            else:
                update_setting("low_stock_alerts_enabled", "true" if alerts_enabled else "false")
                update_setting("default_low_stock_threshold", str(default_threshold))
                update_setting("critical_stock_level", str(critical_level))
                update_setting("warning_stock_level", str(warning_level))
                st.session_state["low_stock_updated"] = True
                st.rerun()

    # ── Current status summary ────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Current Stock Status")

    from services.product_service import list_low_stock_products  # local import to avoid circular

    low_stock_items = list_low_stock_products()

    col1, col2, col3 = st.columns(3)
    with col1:
        critical_count = len([p for p in low_stock_items if p[2] <= critical_level])
        st.markdown(
            f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #ff6b6b;'>
                <p style='margin:0; color:#888; font-size:12px;'>Critical Stock</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#ff6b6b;'>{critical_count}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        warning_count = len([p for p in low_stock_items if critical_level < p[2] <= warning_level])
        st.markdown(
            f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #fbbf24;'>
                <p style='margin:0; color:#888; font-size:12px;'>Low Stock</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#fbbf24;'>{warning_count}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div style='background:#1a1a2e; padding:15px; border-radius:8px; text-align:center; border-left:4px solid #4ade80;'>
                <p style='margin:0; color:#888; font-size:12px;'>Total Low Stock Items</p>
                <p style='margin:0; font-size:24px; font-weight:bold; color:#4ade80;'>{len(low_stock_items)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Items needing attention
    if low_stock_items:
        st.markdown("#### Items Needing Attention")
        for item in low_stock_items[:10]:
            product_id, name, quantity, low_alert = item[0], item[1], item[2], item[3]
            if quantity <= critical_level:
                color = "#ff6b6b"
                status = "CRITICAL"
            else:
                color = "#fbbf24"
                status = "LOW"

            st.markdown(
                f"""
                <div style='display:flex; justify-content:space-between; padding:8px 12px;
                            background:#121620; border-radius:6px; margin:4px 0; border-left:3px solid {color};'>
                    <span>{name}</span>
                    <span style='color:{color}; font-weight:bold;'>{quantity} units ({status})</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if len(low_stock_items) > 10:
            st.caption(f"... and {len(low_stock_items) - 10} more items")


# ── Read Me / About ────────────────────────────────────────────────────────


def render_settings_readme():
    """Render Read Me / About section with app info and commercial offers.

    All prices and contact details are sourced from ``config.py`` so they
    can be updated without touching this file.
    """
    st.markdown("## Settings")
    st.markdown(
        "<p style='margin-top:-15px; font-size:14px; color:#888;'>Read Me</p>",
        unsafe_allow_html=True,
    )

    # ── Application information ───────────────────────────────────────
    st.markdown("###  Application Information")
    st.markdown(
        f"""
        <div style='background:#1a1a2e; padding:20px; border-radius:8px; margin-bottom:20px;'>
            <h3 style='margin:0 0 10px 0; color:#1e88ff;'>{APP_NAME} Management System</h3>
            <table style='width:100%; color:#e6edf3;'>
                <tr><td style='padding:5px 10px; color:#888;'>  Version:</td>
                    <td style='padding:5px 10px;'>   {APP_VERSION}</td></tr>
                <tr><td style='padding:5px 10px; color:#888;'>  Last Update:</td>
                    <td style='padding:5px 10px;'>   {APP_LAST_UPDATE}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── What's included ───────────────────────────────────────────────
    st.markdown("###  What's Included in Your Purchase")
    st.markdown(
        """
        <div style='background:#1a1a2e; padding:20px; border-radius:8px; margin-bottom:20px;'>
            <ul style='color:#e6edf3; margin:0; padding-left:20px;'>
                <li style='padding:5px 0;'>Full source code of the Mini Inventory Management System</li>
                <li style='padding:5px 0;'>Product, Category, Warehouse, and Supplier management</li>
                <li style='padding:5px 0;'>Customer management with payment tracking</li>
                <li style='padding:5px 0;'>Invoice creation and management</li>
                <li style='padding:5px 0;'>Stock alerts (Low Stock, Dead Stock, Expired Products)</li>
                <li style='padding:5px 0;'>Staff management</li>
                <li style='padding:5px 0;'>Customizable settings (Store info, Currency, Alerts)</li>
                <li style='padding:5px 0; color:#4ade80;'><strong>3 months of support and updates</strong> provided by the marketplace</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Inject card hover CSS (scoped to this page only)
    _inject_offer_card_css()

    # ── Support extension plans ───────────────────────────────────────
    st.markdown("###  Support Extension Plans")
    st.markdown(
        "<p style='color:#888; margin-bottom:15px;'>Extend your support period beyond the initial 3 months:</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        _offer_card("Basic", "6 Months", "Total Support", f"${SUPPORT_6_MONTHS_PRICE}",
                     "Including initial 3 months", color="#4ade80")
    with col2:
        _offer_card("Popular", "12 Months", "Total Support", f"${SUPPORT_12_MONTHS_PRICE}",
                     "Best value for long-term", color="#4ade80")
    with col3:
        _offer_card("Flexible", "+3 Months", "Additional Period", f"${SUPPORT_EXTRA_3_MONTHS_PRICE}",
                     "Extend anytime", color="#4ade80")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background:#121620; padding:15px; border-radius:8px; border-left:3px solid #4ade80;'>
            <p style='color:#e6edf3; margin:0; font-size:13px;'>
                <strong>Support includes:</strong>  Response within 24 hours •  WhatsApp, Telegram, or Email •  Active period only
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Updates & new features plans ──────────────────────────────────
    st.markdown("###  Updates & New Features Access")
    st.markdown(
        "<p style='color:#888; margin-bottom:15px;'>Access all new features and improvements released during your active period:</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        _offer_card("Starter", "6 Months", "Updates Access", f"${UPDATES_6_MONTHS_PRICE}",
                     "All features for 6 months", color="#1e88ff", modifier="offer-card-blue")
    with col2:
        _offer_card("Best Value", "12 Months", "Updates Access", f"${UPDATES_12_MONTHS_PRICE}",
                     "Save $5 vs monthly", color="#1e88ff", modifier="offer-card-blue")
    with col3:
        _offer_card("Pro", "18 Months", "Updates Access", f"${UPDATES_18_MONTHS_PRICE}",
                     "Maximum coverage", color="#1e88ff", modifier="offer-card-blue")

    st.markdown("<br>", unsafe_allow_html=True)
    st.warning(
        " **Important:** Updates access does **NOT** include technical support. "
        "Only features released during the active period are included."
    )

    st.markdown("---")

    # ── Custom feature development ────────────────────────────────────
    st.markdown("###  Custom Feature Development")
    st.markdown(
        "<p style='color:#888; margin-bottom:15px;'>Need custom modifications or new features? Choose based on complexity:</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        _offer_card("Simple", "Basic Feature", "Minor changes & tweaks", f"${CUSTOM_SIMPLE_PRICE}",
                     "Small modifications", color="#ef4444", modifier="offer-card-red", title_size="24px")
    with col2:
        _offer_card("Medium", "Standard Feature", "New functionality", f"${CUSTOM_MEDIUM_PRICE}",
                     "Moderate complexity", color="#ef4444", modifier="offer-card-red", title_size="24px")
    with col3:
        _offer_card("Complex", "Advanced Feature", "Major development", f"${CUSTOM_COMPLEX_PRICE}",
                     "Price varies by scope", color="#ef4444", modifier="offer-card-red", title_size="24px")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='background:#121620; padding:15px; border-radius:8px; border-left:3px solid #ef4444;'>
            <p style='color:#e6edf3; margin:0; font-size:13px;'>
                <strong>Note:</strong> Scope and delivery timeline must be agreed upon before payment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Contact section ───────────────────────────────────────────────
    st.markdown("<div id='contact'></div>", unsafe_allow_html=True)
    st.markdown("###  Contact Us")
    st.markdown(
        "<p style='color:#888; margin-bottom:15px;'>Choose your preferred communication channel:</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <a href="{CONTACT_TELEGRAM_URL}" target="_blank" style="text-decoration:none;">
            <div class="contact-card contact-card-telegram">
                <div style='font-size:50px; margin-bottom:15px;'>📱</div>
                <h3 style='color:#0088cc; margin:0 0 10px 0;'>Telegram</h3>
                <p style='color:#888; font-size:13px; margin:0;'>Fast response • Available 24/7</p>
                <p style='color:#0088cc; font-size:14px; margin-top:10px;'>{CONTACT_TELEGRAM_USER}</p>
            </div>
            </a>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <a href="{CONTACT_WHATSAPP_URL}" target="_blank" style="text-decoration:none;">
            <div class="contact-card contact-card-whatsapp">
                <div style='font-size:50px; margin-bottom:15px;'>💬</div>
                <h3 style='color:#25d366; margin:0 0 10px 0;'>WhatsApp</h3>
                <p style='color:#888; font-size:13px; margin:0;'>Direct messaging • Quick support</p>
                <p style='color:#25d366; font-size:14px; margin-top:10px;'>{CONTACT_WHATSAPP_NUMBER}</p>
            </div>
            </a>
            """,
            unsafe_allow_html=True,
        )


# ── Private helpers ────────────────────────────────────────────────────────


def _inject_offer_card_css():
    """Inject scoped CSS for offer and contact cards (hover effects)."""
    st.markdown("""
        <style>
        .offer-card {
            background: linear-gradient(145deg, #1a1a2e 0%, #12121f 100%);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #242b3a;
            height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .offer-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(255,255,255,0.1);
            border-color: #4ade80;
        }
        .offer-card-blue:hover {
            border-color: #1e88ff;
            box-shadow: 0 10px 40px rgba(30,136,255,0.2);
        }
        .offer-card-red:hover {
            border-color: #ef4444;
            box-shadow: 0 10px 40px rgba(239,68,68,0.2);
        }
        .contact-card {
            background: linear-gradient(145deg, #1a1a2e 0%, #12121f 100%);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            border: 1px solid #242b3a;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .contact-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(255,255,255,0.1);
        }
        .contact-card-telegram:hover {
            border-color: #0088cc;
            box-shadow: 0 10px 40px rgba(0,136,204,0.3);
        }
        .contact-card-whatsapp:hover {
            border-color: #25d366;
            box-shadow: 0 10px 40px rgba(37,211,102,0.3);
        }
        </style>
    """, unsafe_allow_html=True)


def _offer_card(
    tier: str,
    heading: str,
    subtitle: str,
    price: str,
    footer: str,
    *,
    color: str = "#4ade80",
    modifier: str = "",
    title_size: str = "28px",
):
    """Render a single offer card with consistent styling.

    Args:
        tier:       Tier label shown above the heading (e.g. "Basic").
        heading:    Main heading text (e.g. "6 Months").
        subtitle:   Small line below the heading.
        price:      Price string to display large.
        footer:     One-line note at the bottom.
        color:      Accent colour for text.
        modifier:   Extra CSS class (e.g. ``offer-card-blue``).
        title_size: Font-size for the heading.
    """
    css_class = f"offer-card {modifier}".strip()
    st.markdown(
        f"""
        <a href="#contact" style="text-decoration:none;">
        <div class="{css_class}">
            <div>
                <p style='color:{color}; font-size:12px; margin:0; text-transform:uppercase; letter-spacing:1px;'>{tier}</p>
                <h2 style='color:#fff; margin:10px 0; font-size:{title_size};'>{heading}</h2>
                <p style='color:#888; font-size:12px; margin:0;'>{subtitle}</p>
            </div>
            <div>
                <p style='color:{color}; font-size:36px; font-weight:bold; margin:20px 0;'>{price}</p>
            </div>
            <div>
                <p style='color:#888; font-size:11px; margin:0;'>{footer}</p>
            </div>
        </div>
        </a>
        """,
        unsafe_allow_html=True,
    )
