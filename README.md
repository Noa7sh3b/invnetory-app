# 📦 Mini Inventory Management System

**A modern, full-featured inventory management system built with Python and Streamlit**

Perfect for small to medium businesses to efficiently manage products, suppliers, customers, invoices, and stock levels with a beautiful, intuitive interface.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)
![License](https://img.shields.io/badge/License-Commercial-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

---

## ✨ Key Features

### 📊 Real-Time Dashboard
- **Comprehensive Overview**: Track total sales (count of products sold), revenue, receivables, and more
- **Key Metrics**: Total products, invoices, customers, suppliers at a glance
- **Smart Notifications**: Bell icon with live alerts for low stock and expired products
- **Quick Access**: Navigate to critical areas with one click

### 📦 Complete Product Management
- **Full CRUD Operations**: Add, view, edit, and delete products with ease
- **Rich Product Data**: 
  - Product images with thumbnail display
  - SKU and model tracking
  - Production and expiry dates
  - Supplier, category, and warehouse assignments
  - Distributor and selling prices
  - Custom low stock alert thresholds
  - Detailed product descriptions
- **Advanced Features**:
  - Inline editing with save/cancel
  - Powerful search functionality
  - Paginated display (8 items per page)
  - Export to Excel, PDF, or print-friendly format
  - Bulk operations support

### 👥 Customer Management System
- **Customer Database**: Complete contact information (ID, name, phone, email, address)
- **Payment Tracking**: Monitor paid, unpaid, and partial payment status
- **Payment History**: Record and view all customer payment transactions
- **Status Filtering**: Quickly filter customers by payment status
- **Integrated Invoicing**: Seamlessly linked with invoice system

### 🧾 Professional Invoice System
- **Smart Invoice Creation**:
  - Auto-generated invoice numbers (INV-YYYYMMDD-XXX format)
  - Multiple products per invoice with quantity validation
  - Real-time stock checking and updates
  - Discount and payment tracking
  - Custom notes support
- **Payment Management**:
  - Track paid, partial, and unpaid invoices
  - Update payment status anytime
  - View payment history
- **Export & Print**:
  - Professional invoice layout
  - Export to Excel or PDF
  - Print-ready format

### 📈 Intelligent Stock Management
- **Low Stock Alerts**: 
  - Customizable thresholds per product
  - Visual indicators (red for critical, yellow for warning)
  - Real-time notifications in sidebar bell
  - Detailed stock status reports
- **Dead Stock Tracking**: 
  - Identify products with no recent sales
  - Configurable time period (default 30 days)
  - Help optimize inventory
- **Expiry Monitoring**:
  - Track products past expiration date
  - Prevent selling expired items
  - Proactive alerts

### 🏪 Suppliers & Warehouses
- **Supplier Database**:
  - Full contact information
  - Contact person details
  - Email and phone tracking
  - Address management
  - Linked to products for easy tracking
- **Warehouse Management**:
  - Multiple warehouse support
  - Rack number tracking for precise location
  - Product assignment and organization

### 👨‍💼 Staff Management
- **Employee Records**: Name, role, salary, age
- **Contact Information**: Phone and email
- **Employment Tracking**: Start date monitoring
- **Full CRUD Operations**: Add, view, edit, delete staff members

### ⚙️ Comprehensive Settings
- **Store Branding**:
  - Custom store name (displayed in sidebar)
  - Logo upload (60x60 recommended)
  - Personalize your instance
- **Currency Configuration**:
  - 30+ international currencies
  - Custom symbol support
  - Symbol position (before/after amount)
  - Decimal places (0-3)
  - Live preview
- **Low Stock Thresholds**:
  - Default alert level for new products
  - Critical and warning levels
  - Enable/disable alerts system-wide
- **About & Commercial Info**:
  - Application version and update info
  - Support extension plans
  - Updates access information
  - Custom feature development pricing
  - Contact information (Telegram & WhatsApp)

### 🔔 Smart Notification System
- **Facebook-Style Popover**: Click the bell icon in the header
- **Live Badge Count**: Shows total alerts at a glance
- **Categorized Alerts**: Low stock (yellow) and expired products (red)
- **Quick Navigation**: Jump directly to full alert pages
- **Preview Limit**: Shows first 5 items with "view all" option

### 🎨 Modern UI/UX
- **Dark Theme**: Professional, easy-on-the-eyes design
- **Responsive Layout**: Clean, organized interface
- **Hover Effects**: Interactive cards with visual feedback
- **Consistent Design**: Unified look across all pages
- **Intuitive Navigation**: Collapsible sidebar with expanders

---

## 🚀 Quick Start (Windows Users)

### One-Click Installation ⭐

**The easiest way to run this system!**

1. **Verify Python is installed:**
   ```bash
   python --version
   ```
   *(Should show Python 3.9 or higher)*

2. **Download and extract the project**

3. **Double-click `run.bat`**

That's it! The system will:
- ✅ Automatically check all requirements
- ✅ Create virtual environment if needed
- ✅ Install dependencies if needed
- ✅ Start the application
- ✅ Open your browser automatically

> 💡 **First run takes 1-2 minutes** (installation)  
> **Subsequent runs start instantly!**

### Alternative: Manual Setup

If you prefer manual control, use `setup.bat` first:

```bash
# 1. Install everything
setup.bat

# 2. Run application
run.bat
```

---

## 🚀 Installation Guide (All Platforms)

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package manager, included with Python)
- **Git** (optional, for cloning)

### Step-by-Step Installation

#### 1. **Download/Clone the Project**

```bash
# If using Git
git clone <repository-url>

# Or extract the ZIP file to your desired location
cd inventory_app
```

#### 2. **Create Virtual Environment (Highly Recommended)**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 **Why Virtual Environment?**  
> Keeps dependencies isolated, prevents conflicts with other projects, and makes deployment easier.

#### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

**Dependencies Installed:**
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `openpyxl` - Excel export
- `reportlab` - PDF generation
- `Pillow` - Image processing
- `python-dateutil` - Date utilities

#### 4. **Run the Application**

```bash
streamlit run app.py
```

#### 5. **Access the Application**

The application will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to this URL.

---

## 📁 Project Structure

```
inventory_app/
│
├── 📄 app.py                      # Main application entry point
├── 📄 config.py                   # Configuration constants and settings
├── 📄 db.py                       # Database initialization and connection
├── 📄 models.py                   # Data models (dataclasses)
├── 📄 requirements.txt            # Python dependencies
├── 📄 README.md                   # This documentation
│
├── 📁 data/                       # Data directory (auto-created on first run)
│   ├── 📊 inventory.db            # SQLite database file
│   └── 📁 images/                 # Product images storage
│       └── <uuid>.jpg/png         # Auto-generated image filenames
│
├── 📁 logs/                       # Application logs (auto-created)
│   └── 📝 app_YYYYMMDD.log        # Daily log files
│
├── 📁 pages/                      # Streamlit page modules
│   ├── dashboard.py               # Dashboard with metrics and stats
│   ├── products.py                # Product management (add/manage)
│   ├── categories.py              # Categories CRUD
│   ├── warehouses.py              # Warehouses CRUD
│   ├── suppliers.py               # Supplier management (add/manage)
│   ├── customers.py               # Customer management (add/manage/payments)
│   ├── invoices.py                # Invoice system (create/manage/status)
│   ├── stock.py                   # Stock monitoring (dead/low/expired)
│   ├── staff.py                   # Staff management (add/manage)
│   └── settings.py                # Application settings (store/currency/alerts/readme)
│
├── 📁 services/                   # Business logic layer
│   ├── product_service.py         # Product operations and queries
│   ├── category_service.py        # Category CRUD
│   ├── warehouse_service.py       # Warehouse CRUD
│   ├── supplier_service.py        # Supplier operations
│   ├── customer_service.py        # Customer and payment operations
│   ├── invoice_service.py         # Invoice creation and management
│   ├── staff_service.py           # Staff operations
│   └── settings_service.py        # Settings management and currency options
│
├── 📁 ui/                         # User interface components
│   ├── theme.py                   # Custom CSS styling and theme
│   └── components.py              # Reusable UI components (cards, sections)
│
└── 📁 utils/                      # Utility modules
    ├── logger.py                  # Centralized logging setup
    ├── export.py                  # Export functions (Excel, PDF, HTML)
    ├── pagination.py              # Pagination helpers
    └── db_utils.py                # Database utilities and safe operations
```

---

## ⚙️ Configuration

### Application Settings (config.py)

Key configuration constants you can modify:

| Setting | Default | Description |
|---------|---------|-------------|
| `APP_NAME` | "Mini Inventory" | Application title |
| `APP_VERSION` | "1.0.0" | Current version |
| `PAGE_SIZE` | 8 | Items displayed per page |
| `MAX_LIST_LOAD` | 100 | Max items loaded for performance |
| `DEFAULT_LOW_STOCK_THRESHOLD` | 10 | Default low stock alert level |
| `NOTIFICATION_PREVIEW_LIMIT` | 5 | Items shown in notification popover |

### Database

The application uses **SQLite** for data storage:
- **Location**: `data/inventory.db`
- **Type**: Single-file database
- **Tables**: products, categories, warehouses, suppliers, customers, customer_payments, invoices, invoice_items, staff
- **Auto-initialization**: Database and tables created on first run

### Images

Product images are stored in `data/images/`:
- **Format**: JPEG, PNG
- **Naming**: UUID-based (e.g., `a1b2c3d4.jpg`)
- **Size**: Automatically handled by Pillow
- **Display**: Thumbnails in product list, full size in view mode

---

## 🎨 Customization

### Changing Theme Colors

Edit `ui/theme.py` and modify CSS variables in the `:root` section:

```css
:root {
    --bg: #0f1115;        /* Background color */
    --card: #161a22;      /* Card background */
    --accent: #1e88ff;    /* Primary accent color (blue) */
    --text: #e6edf3;      /* Main text color */
    --muted: #a1a7b3;     /* Secondary text color */
    --border: #242b3a;    /* Border color */
}
```

### Adding New Currency

Edit `services/settings_service.py` and add to `CURRENCY_OPTIONS` list:

```python
{
    "code": "XXX",              # ISO 4217 currency code
    "name": "Your Currency",    # Full currency name
    "symbol": "¤"               # Currency symbol
},
```

### Modifying Page Size

Change the `PAGE_SIZE` constant in `config.py`:

```python
PAGE_SIZE = 10  # Display 10 items per page instead of 8
```

### Adjusting Low Stock Alerts

Modify default thresholds in `config.py`:

```python
DEFAULT_LOW_STOCK_THRESHOLD = 15      # Default alert level
DEFAULT_CRITICAL_STOCK_LEVEL = 5      # Red alert level
DEFAULT_WARNING_STOCK_LEVEL = 15      # Yellow alert level
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **Database Locked Error**

**Problem**: `sqlite3.OperationalError: database is locked`

**Solutions**:
- Close all other instances of the application
- Restart the Streamlit server (Ctrl+C, then `streamlit run app.py`)
- Check if another program is accessing `inventory.db`
- Delete any `.db-journal` files in the `data` folder

#### 2. **Images Not Displaying**

**Problem**: Product images show as "No img" or broken

**Solutions**:
- Verify the `data/images` folder exists
- Check file permissions (read/write access)
- Ensure image files aren't corrupted
- Try re-uploading the images
- Check image path in database (`image_path` column)

#### 3. **Export Not Working**

**Problem**: Excel or PDF export fails

**Solutions**:
- Verify `openpyxl` and `reportlab` are installed:
  ```bash
  pip install --upgrade openpyxl reportlab
  ```
- Check write permissions in your browser's download folder
- Try a different browser
- Ensure you have disk space available

#### 4. **Port Already in Use**

**Problem**: `OSError: [Errno 98] Address already in use`

**Solutions**:
- Change the port:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- Find and kill the process using port 8501:
  ```bash
  # Windows
  netstat -ano | findstr :8501
  taskkill /PID <PID> /F
  
  # macOS/Linux
  lsof -i :8501
  kill -9 <PID>
  ```

#### 5. **Module Not Found Error**

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solutions**:
- Ensure virtual environment is activated
- Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Check Python version: `python --version` (must be 3.9+)

#### 6. **Slow Performance**

**Problem**: Application is slow or freezing

**Solutions**:
- Reduce `MAX_LIST_LOAD` in `config.py` (default: 100)
- Clear old/unused data from database
- Optimize product images (resize to reasonable dimensions)
- Check system resources (RAM, CPU)
- Consider database optimization (VACUUM command)

### Reset Database

To start with a fresh database:

**Windows:**
```bash
del data\inventory.db
```

**macOS/Linux:**
```bash
rm data/inventory.db
```

Then restart the application. The database will be recreated automatically.

### Clear All Data

To completely reset the application:

```bash
# Windows
rmdir /s data
rmdir /s logs

# macOS/Linux
rm -rf data logs
```

---

## 📊 Database Schema

### Products Table
```sql
id, name, category_id, warehouse_id, rack_number, image_path, 
details, production_date, expiry_date, quantity, low_stock_alert, 
distributor_price, selling_price, model, sku, supplier_id
```

### Invoices Table
```sql
id, invoice_number, customer_id, invoice_date, subtotal, discount, 
total, paid_amount, due_amount, payment_status, notes, created_at
```

### Invoice Items Table
```sql
id, invoice_id, product_id, product_name, sku, quantity, 
unit_price, total_price
```

*See `db.py` for complete schema details.*

---

## 🔒 Security Considerations

- **Local Use**: This application is designed for local/internal network use
- **No Authentication**: Current version doesn't include user authentication
- **Database Access**: SQLite database is accessible to anyone with file system access
- **Backups**: Regularly backup the `data` folder
- **Production Use**: If deploying publicly, add authentication and SSL

---

## 🆘 Support & Contact

Need help or want to extend your application?

### 📱 Contact Channels

- **Telegram**: [@N7_miracle](https://t.me/N7_miracle)
- **WhatsApp**: [+201012469699](https://wa.me/+201012469699)

### 💡 Support Options

**Included (First 3 Months)**:
- Bug fixes
- Technical support
- Minor updates

**Extended Support Plans**:
- 6 months total: $15
- 12 months total: $26
- Each additional 3 months: $12

**Updates & New Features**:
- 6 months access: $19
- 12 months access: $33
- 18 months access: $49

**Custom Feature Development**:
- Simple features: $19
- Medium complexity: $34
- Complex features: $50+

*Visit Settings → Read Me in the application for full details.*

---

## 📝 Changelog

### Version 1.0.0 (February 2026)
- Initial release
- Complete inventory management system
- Dashboard with key metrics
- Product, customer, supplier, and invoice management
- Stock monitoring (low, dead, expired)
- Smart notification system
- Professional settings page
- Export functionality (Excel, PDF)
- Modern dark theme UI

---

## 📄 License

This software is sold under a **Commercial License**.

**Permitted Use**:
- Install on unlimited local machines
- Use for your business operations
- Modify for personal use

**Restrictions**:
- No redistribution or resale
- No public sharing of source code
- No use in SaaS products without additional licensing

For full license terms, refer to your purchase agreement.

---

## 🙏 Acknowledgments

Built with:
- [Python](https://www.python.org/) - Programming language
- [Streamlit](https://streamlit.io/) - Web framework
- [SQLite](https://www.sqlite.org/) - Database
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [ReportLab](https://www.reportlab.com/) - PDF generation

---

## 🎯 Roadmap (Future Versions)

Potential features for future releases:

- [ ] User authentication and roles
- [ ] Multi-user support with permissions
- [ ] Advanced reporting and analytics
- [ ] Barcode scanning integration
- [ ] Email notifications for alerts
- [ ] Backup and restore functionality
- [ ] API for external integrations
- [ ] Mobile-responsive improvements
- [ ] Multi-language support
- [ ] Cloud deployment option

*Contact us for custom feature requests!*

---

<div align="center">

**Made with ❤️ using Python and Streamlit**

⭐ **Enjoy using Mini Inventory?** Consider leaving a review!

</div>
