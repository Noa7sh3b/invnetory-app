"""
Configuration Module – Central place for all application-wide constants.

Edit this file to customise behaviour without touching business logic.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "Mini Inventory"
APP_VERSION = "1.1.0"
APP_LAST_UPDATE = "February 2026"

# ---------------------------------------------------------------------------
# File-system paths (relative to the working directory)
# ---------------------------------------------------------------------------
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "inventory.db"
IMAGE_DIR = DATA_DIR / "images"

# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
PAGE_SIZE = 8                # items shown per page
MAX_LIST_LOAD = 100          # hard cap on in-memory rows for heavy lists

# ---------------------------------------------------------------------------
# Notification bell
# ---------------------------------------------------------------------------
NOTIFICATION_PREVIEW_LIMIT = 5   # max items shown inside the popover

# ---------------------------------------------------------------------------
# Contact information (displayed in the Read Me page)
# ---------------------------------------------------------------------------
CONTACT_TELEGRAM_USER = "@N7_miracle"
CONTACT_TELEGRAM_URL = "https://t.me/N7_miracle"
CONTACT_WHATSAPP_NUMBER = "+201012469699"
CONTACT_WHATSAPP_URL = "https://wa.me/+201012469699"

# ---------------------------------------------------------------------------
# Commercial offer prices (displayed in the Read Me page – static info only)
# ---------------------------------------------------------------------------

# Support extension plans
SUPPORT_6_MONTHS_PRICE = 15
SUPPORT_12_MONTHS_PRICE = 26
SUPPORT_EXTRA_3_MONTHS_PRICE = 12

# Updates & new features plans
UPDATES_6_MONTHS_PRICE = 19
UPDATES_12_MONTHS_PRICE = 33
UPDATES_18_MONTHS_PRICE = 49

# Custom feature development tiers
CUSTOM_SIMPLE_PRICE = 19
CUSTOM_MEDIUM_PRICE = 34
CUSTOM_COMPLEX_PRICE = "50+"

