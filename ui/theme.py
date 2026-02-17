import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bg: #0f1115;
            --card: #161a22;
            --accent: #1e88ff;
            --text: #e6edf3;
            --muted: #a1a7b3;
            --border: #242b3a;
        }
        .stApp {
            background-color: var(--bg);
            color: var(--text);
        }
        .block-container {
            padding-top: 1.5rem;
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            margin-bottom: 15px;
        }
        .card:hover {
            border-color: var(--accent);
            box-shadow: 0 10px 28px rgba(30,136,255,0.25);
            transform: translateY(-2px);
            transition: all 0.15s ease-in-out;
        }
        .card-title {
            color: var(--muted);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: .08em;
            margin-bottom: 6px;
        }
        .card-value {
            color: var(--text);
            font-size: 24px;
            font-weight: 700;
        }
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text);
        }
        .box {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
        }
        .list-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            margin: 8px 0;
            background: #121620;
            width: 100%;
            box-sizing: border-box;
        }
        .header-row-marker + div [data-testid="stHorizontalBlock"] {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto 6px auto;
        }
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div {
            flex: 1 !important;
            min-width: 60px !important;
        }
        /* Specific column widths for products header */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(1) { flex: 0 0 70px !important; max-width: 70px !important; } /* IMAGE */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(2) { flex: 0 0 140px !important; max-width: 140px !important; } /* PRODUCT */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(3) { flex: 0 0 100px !important; max-width: 100px !important; } /* CATEGORY */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(4) { flex: 0 0 100px !important; max-width: 100px !important; } /* WAREHOUSE */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(5) { flex: 0 0 80px !important; max-width: 80px !important; } /* SUPPLIER */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(6) { flex: 0 0 70px !important; max-width: 70px !important; } /* SUPP. PRICE */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(7) { flex: 0 0 80px !important; max-width: 80px !important; } /* SELL PRICE */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(8) { flex: 0 0 50px !important; max-width: 50px !important; } /* QTY */
        .header-row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(9) { flex: 0 0 150px !important; max-width: 150px !important; } /* OPTIONS */
        .header-cell {
            color: var(--muted);
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.06em;
        }
        .row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 12px;
            margin: 5px 0;
            background: #121620;
            min-height: 100px;
            align-items: center;
            gap: 0 !important;
            width: 100%;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        .row-marker + div [data-testid="stHorizontalBlock"] > div {
            flex: 1 !important;
            min-width: 60px !important;
        }
        /* Specific column widths for products rows */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(1) { flex: 0 0 70px !important; max-width: 70px !important; } /* IMAGE */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(2) { flex: 0 0 140px !important; max-width: 140px !important; } /* PRODUCT */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(3) { flex: 0 0 100px !important; max-width: 100px !important; } /* CATEGORY */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(4) { flex: 0 0 100px !important; max-width: 100px !important; } /* WAREHOUSE */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(5) { flex: 0 0 80px !important; max-width: 80px !important; } /* SUPPLIER */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(6) { flex: 0 0 70px !important; max-width: 70px !important; } /* SUPP. PRICE */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(7) { flex: 0 0 80px !important; max-width: 80px !important; } /* SELL PRICE */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(8) { flex: 0 0 50px !important; max-width: 50px !important; } /* QTY */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:nth-child(9) { flex: 0 0 150px !important; max-width: 150px !important; } /* OPTIONS */
        .row-marker + div [data-testid="stHorizontalBlock"] > div:last-child {
            padding-left: 0;
        }
        .row-marker + div [data-testid="stHorizontalBlock"] img {
            max-height: 150px;
            object-fit: cover;
        }
        /* Categories CRUD layout (strict) */
        .cat-add-marker + div [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            margin: 0 !important;
        }
        .cat-add-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"] {
            padding: 0 !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"],
        .cat-row-marker + div [data-testid="stHorizontalBlock"] {
            width: 330px !important; /* 20 + 150 + 160 */
            margin: 0 auto 0 auto !important;
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 0 !important;
            align-items: center !important;
            gap: 0 !important;
            justify-content: flex-start !important;
            box-sizing: border-box !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"],
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"] {
            border-right: 1px solid #1e90ff !important;
            padding: 2px 4px !important;
            box-sizing: border-box !important;
            text-align: center !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child,
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child {
            border-right: 0 !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1),
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(1) {
            flex: 0 0 20px !important;
            max-width: 20px !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2),
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(2) {
            flex: 0 0 150px !important;
            max-width: 150px !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3),
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3) {
            flex: 0 0 160px !important;
            max-width: 160px !important;
        }
        .cat-table-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"] {
            background: #121620 !important;
            color: #e6edf3 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
        }
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"] {
            background: #0f1115 !important;
            color: #e6edf3 !important;
        }
        .cat-row-marker + div [data-testid="stHorizontalBlock"] button {
            padding: 1px 4px !important;
            min-width: 36px !important;
            height: 24px !important;
            font-size: 11px !important;
            margin: 0 !important;
        }
        .cat-row-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-child(3) [data-testid="stHorizontalBlock"] {
            gap: 2px !important;
            justify-content: flex-start !important;
        }
        .cat-row-marker + div [data-testid="stHorizontalBlock"] button + button {
            margin-left: 0 !important;
        }
        .cat-options-marker + div [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            gap: 2px !important;
            justify-content: flex-start !important;
            align-items: center !important;
            flex-wrap: nowrap !important;
            width: 100% !important;
        }
        .cat-options-marker + div [data-testid="stHorizontalBlock"] [data-testid="column"] {
            padding: 0 !important;
            flex: 0 0 auto !important;
            width: auto !important;
            min-width: 0 !important;
        }
        .cat-options-marker + div .stButton {
            display: inline-flex !important;
        }
        .cat-options-marker + div .stButton > button {
            white-space: nowrap !important;
            margin: 0 !important;
        }
        .pagination-box + div [data-testid="stHorizontalBlock"] {
            background: var(--bg) !important;
        }
        .pagination-box + div [data-testid="stHorizontalBlock"] > div {
            background: var(--bg) !important;
        }
        .export-row-marker + div [data-testid="stHorizontalBlock"] {
            gap: 0px !important;
            justify-content: flex-start !important;
        }
        .export-action-marker + div [data-testid="stHorizontalBlock"] {
            gap: 2px !important;
            justify-content: flex-start !important;
        }
        /* Pagination box */
        .pagination-box {
            width: 299px;
            margin: 20px 0 20px auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #1a1d24;
            border: 0px solid #1e90ff;
            border-radius: 12px;
            padding: 12px 16px;
            gap: 12px;
        }
        .pagination-btn {
            width: 70px;
            height: 36px;
            background: transparent;
            color: #1e90ff;
            border: 0;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
        }
        .pagination-btn:hover:not([disabled]) {
            background: rgba(30, 144, 255, 0.1);
            transform: translateY(-1px);
        }
        .pagination-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
        .page-number {
            flex: 1;
            text-align: center;
            color: white;
            font-size: 14px;
            font-weight: 500;
        }
        /* Hide streamlit functional buttons for pagination (JS handles actual hiding) */
        button[aria-label="View"] {
            background: var(--accent) !important;
            color: white !important;
            border: 0 !important;
        }
        button[aria-label="Edit"] {
            background: #f1c40f !important;
            color: #0f1115 !important;
            border: 0 !important;
        }
        button[aria-label="Del"] {
            background: #e74c3c !important;
            color: white !important;
            border: 0 !important;
        }
        button[aria-label="View"], button[aria-label="Edit"], button[aria-label="Del"] {
            min-width: 50px !important;
            height: 32px !important;
            padding: 0 6px !important;
            font-size: 11px !important;
        }
        .accent {
            color: var(--accent);
        }
        .stButton>button {
            background: var(--accent);
            color: white;
            border: 0;
            border-radius: 8px;
            padding: 6px 12px;
        }
        .stButton>button:disabled {
            opacity: 0.6;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stSidebar"] {
            background: #0f1115;
            border-right: 1px solid var(--border);
            min-width: 280px !important;
            max-width: 280px !important;
            width: 280px !important;
            display: block !important;
            visibility: visible !important;
            transform: none !important;
            margin-left: 0 !important;
            left: 0 !important;
        }
        /* Sidebar expander arrow visibility */
        [data-testid="stSidebar"] details summary {
            display: flex !important;
            align-items: center !important;
            color: var(--text) !important;
        }
        [data-testid="stSidebar"] details summary svg {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            fill: var(--accent) !important;
            color: var(--accent) !important;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Always show the collapsed control if sidebar gets hidden */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        /* Force blue focus for all inputs (text, number, select, textarea) */
        input:focus,
        textarea:focus,
        select:focus,
        [data-baseweb="input"] input:focus,
        [data-baseweb="textarea"] textarea:focus,
        [data-baseweb="select"] div:focus-within,
        [data-baseweb="input"]:focus-within,
        [data-baseweb="base-input"]:focus-within,
        [data-baseweb="textarea"]:focus-within,
        [data-baseweb="select"]:focus-within,
        [data-baseweb="select"] > div:focus-within,
        [data-baseweb="select"] [role="combobox"]:focus-within,
        [data-baseweb="input"] [role="textbox"]:focus,
        [data-baseweb="input"] [role="spinbutton"]:focus {
            border-color: #1e90ff !important;
            box-shadow: 0 0 0 1px #1e90ff !important;
            outline: none !important;
        }
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="base-input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #1e90ff !important;
            box-shadow: 0 0 0 1px #1e90ff !important;
        }
        /* Number input blue border */
        [data-testid="stNumberInput"] > div > div {
            border-color: #1e90ff !important;
        }
        [data-testid="stNumberInput"] > div > div:focus-within {
            border-color: #1e90ff !important;
            box-shadow: 0 0 0 1px #1e90ff !important;
        }
        [data-testid="stNumberInput"] input:focus {
            border-color: #1e90ff !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stSidebar"] button[aria-label="Dashboard"] {
            background: transparent !important;
            color: var(--accent) !important;
            border: 1px solid var(--accent) !important;
        }
        /* Warehouses page styles */
        .wh-add-marker + div [data-testid="stTextInput"] {
            
            max-width: 280px !important;
        }
        .wh-add-marker + div + div [data-testid="stTextInput"] {
            
            max-width: 280px !important;
        }
        .wh-table-marker + div [data-testid="stHorizontalBlock"],
        .wh-row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 4px 8px !important;
            gap: 0 !important;
            margin-bottom: 2px !important;
        }
        .wh-options-marker + div [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
        }
        /* Suppliers page styles */
        .sup-table-marker + div [data-testid="stHorizontalBlock"],
        .sup-row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            gap: 0 !important;
            margin-bottom: 2px !important;
        }
        .sup-options-marker + div [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
        }
        .sup-options-marker + div [data-testid="stHorizontalBlock"] button {
            padding: 2px 8px !important;
            font-size: 12px !important;
            min-height: 28px !important;
        }
        /* Stock page styles */
        .stock-table-marker + div [data-testid="stHorizontalBlock"],
        .stock-row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            gap: 0 !important;
            margin-bottom: 2px !important;
        }
        /* Staff page styles */
        .staff-table-marker + div [data-testid="stHorizontalBlock"],
        .staff-row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            gap: 0 !important;
            margin-bottom: 2px !important;
        }
        .staff-options-marker + div [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
        }
        .staff-options-marker + div [data-testid="stHorizontalBlock"] button {
            padding: 2px 8px !important;
            font-size: 12px !important;
            min-height: 28px !important;
        }
        /* Customers page styles */
        .cust-table-marker + div [data-testid="stHorizontalBlock"],
        .cust-row-marker + div [data-testid="stHorizontalBlock"] {
            border: 1px solid #1e90ff !important;
            border-radius: 4px !important;
            padding: 8px 12px !important;
            gap: 0 !important;
            margin-bottom: 2px !important;
        }
        .cust-options-marker + div [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
        }
        .cust-options-marker + div [data-testid="stHorizontalBlock"] button {
            padding: 2px 8px !important;
            font-size: 12px !important;
            min-height: 28px !important;
        }
        /* Notification Bell Popover Styling */
        [data-testid="stPopover"] {
            margin-top: 10px !important;
        }
        [data-testid="stPopover"] > div {
            max-height: 400px !important;
            overflow-y: auto !important;
            min-width: 280px !important;
        }
        [data-testid="stPopoverBody"] {
            padding: 12px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # JavaScript to connect HTML pagination buttons to hidden Streamlit buttons
    # and hide the p/n buttons visually
    import streamlit.components.v1 as components
    components.html("""
    <script>
    const doc = window.parent.document;
    
    // Hide all Streamlit buttons with text "p" or "n" (pagination helpers)
    function hidePaginationButtons() {
        const allButtons = doc.querySelectorAll('button');
        allButtons.forEach(function(btn) {
            const text = btn.innerText.trim();
            if (text === 'p' || text === 'n') {
                // Hide the button's parent containers up to the column level
                let el = btn;
                for (let i = 0; i < 5; i++) {
                    if (el.parentElement) el = el.parentElement;
                }
                el.style.position = 'absolute';
                el.style.width = '1px';
                el.style.height = '1px';
                el.style.overflow = 'hidden';
                el.style.clip = 'rect(0,0,0,0)';
            }
        });
    }
    
    // Run immediately and observe for changes
    hidePaginationButtons();
    const observer = new MutationObserver(hidePaginationButtons);
    observer.observe(doc.body, { childList: true, subtree: true });
    
    // Connect HTML pagination buttons to hidden Streamlit buttons
    doc.addEventListener('click', function(e) {
        if (e.target.classList.contains('pagination-btn') && !e.target.disabled) {
            const isPrev = e.target.textContent.trim() === 'Previous';
            const label = isPrev ? 'p' : 'n';
            const allButtons = doc.querySelectorAll('button');
            for (let i = 0; i < allButtons.length; i++) {
                if (allButtons[i].innerText.trim() === label && !allButtons[i].disabled) {
                    allButtons[i].click();
                    break;
                }
            }
        }
    });
    </script>
    """, height=0)
