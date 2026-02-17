"""
Settings Service Module - Handles application settings storage and retrieval.

This module provides functions for managing application settings
stored in the database.
"""

from db import get_conn
from datetime import datetime


# Available currency options
CURRENCY_OPTIONS = [
    {"code": "USD", "name": "US Dollar", "symbol": "$"},
    {"code": "EUR", "name": "Euro", "symbol": "€"},
    {"code": "GBP", "name": "British Pound", "symbol": "£"},
    {"code": "EGP", "name": "Egyptian Pound", "symbol": "E£"},
    {"code": "SAR", "name": "Saudi Riyal", "symbol": "﷼"},
    {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ"},
    {"code": "KWD", "name": "Kuwaiti Dinar", "symbol": "د.ك"},
    {"code": "QAR", "name": "Qatari Riyal", "symbol": "﷼"},
    {"code": "BHD", "name": "Bahraini Dinar", "symbol": ".د.ب"},
    {"code": "OMR", "name": "Omani Rial", "symbol": "﷼"},
    {"code": "JOD", "name": "Jordanian Dinar", "symbol": "د.ا"},
    {"code": "LBP", "name": "Lebanese Pound", "symbol": "ل.ل"},
    {"code": "IQD", "name": "Iraqi Dinar", "symbol": "ع.د"},
    {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
    {"code": "PKR", "name": "Pakistani Rupee", "symbol": "₨"},
    {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥"},
    {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
    {"code": "KRW", "name": "South Korean Won", "symbol": "₩"},
    {"code": "TRY", "name": "Turkish Lira", "symbol": "₺"},
    {"code": "RUB", "name": "Russian Ruble", "symbol": "₽"},
    {"code": "BRL", "name": "Brazilian Real", "symbol": "R$"},
    {"code": "MXN", "name": "Mexican Peso", "symbol": "$"},
    {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$"},
    {"code": "AUD", "name": "Australian Dollar", "symbol": "A$"},
    {"code": "NZD", "name": "New Zealand Dollar", "symbol": "NZ$"},
    {"code": "ZAR", "name": "South African Rand", "symbol": "R"},
    {"code": "NGN", "name": "Nigerian Naira", "symbol": "₦"},
    {"code": "KES", "name": "Kenyan Shilling", "symbol": "KSh"},
    {"code": "GHS", "name": "Ghanaian Cedi", "symbol": "₵"},
    {"code": "MAD", "name": "Moroccan Dirham", "symbol": "د.م."},
    {"code": "TND", "name": "Tunisian Dinar", "symbol": "د.ت"},
    {"code": "DZD", "name": "Algerian Dinar", "symbol": "د.ج"},
]


def init_settings_table():
    """Initialize the settings table if it doesn't exist."""
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT
        )
    """)
    # Add updated_at column if missing (for databases created by older scripts)
    try:
        conn.execute("ALTER TABLE settings ADD COLUMN updated_at TEXT")
    except Exception:
        pass  # Column already exists
    conn.commit()
    conn.close()


def get_setting(key: str, default: str = "") -> str:
    """
    Get a setting value by key.
    
    Args:
        key: The setting key to retrieve
        default: Default value if setting doesn't exist
        
    Returns:
        The setting value or default if not found
    """
    init_settings_table()
    conn = get_conn()
    row = conn.execute(
        "SELECT value FROM settings WHERE key = ?", (key,)
    ).fetchone()
    conn.close()
    return row[0] if row else default


def update_setting(key: str, value: str) -> bool:
    """
    Update or insert a setting.
    
    Args:
        key: The setting key
        value: The value to store
        
    Returns:
        True if successful
    """
    init_settings_table()
    conn = get_conn()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO settings (key, value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = ?
    """, (key, value, now, value, now))
    conn.commit()
    conn.close()
    return True


def delete_setting(key: str) -> bool:
    """
    Delete a setting by key.
    
    Args:
        key: The setting key to delete
        
    Returns:
        True if successful
    """
    init_settings_table()
    conn = get_conn()
    conn.execute("DELETE FROM settings WHERE key = ?", (key,))
    conn.commit()
    conn.close()
    return True


def get_all_settings() -> dict:
    """
    Get all settings as a dictionary.
    
    Returns:
        Dictionary of all settings
    """
    init_settings_table()
    conn = get_conn()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


def get_currency_symbol() -> str:
    """Get the configured currency symbol."""
    return get_setting("currency_symbol", "$")


def get_currency_code() -> str:
    """Get the configured currency code."""
    return get_setting("currency_code", "USD")


def format_currency(amount: float) -> str:
    """
    Format an amount with the configured currency settings.
    
    Args:
        amount: The amount to format
        
    Returns:
        Formatted currency string
    """
    symbol = get_currency_symbol()
    position = get_setting("currency_position", "before")
    decimal_places = int(get_setting("decimal_places", "2"))
    
    formatted_amount = f"{amount:,.{decimal_places}f}"
    
    if position == "before":
        return f"{symbol}{formatted_amount}"
    else:
        return f"{formatted_amount}{symbol}"


def get_store_info() -> dict:
    """
    Get store information for invoices and reports.
    
    Returns:
        Dictionary with store information
    """
    return {
        "name": get_setting("store_name", "My Store"),
        "tagline": get_setting("store_tagline", ""),
        "phone": get_setting("store_phone", ""),
        "email": get_setting("store_email", ""),
        "address": get_setting("store_address", ""),
        "logo": get_setting("store_logo", ""),
    }


def save_store_logo(uploaded_file) -> str:
    """
    Save store logo image to data/images folder.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Path to saved image or empty string if failed
    """
    import os
    import uuid
    
    if uploaded_file is None:
        return ""
    
    # Create images directory if not exists
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate unique filename
    file_ext = uploaded_file.name.split(".")[-1].lower()
    filename = f"store_logo_{uuid.uuid4().hex[:8]}.{file_ext}"
    filepath = os.path.join(images_dir, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Store relative path in settings
    relative_path = f"data/images/{filename}"
    update_setting("store_logo", relative_path)
    
    return relative_path
