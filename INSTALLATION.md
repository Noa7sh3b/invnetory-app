# Installation Guide

Complete installation guide for the Mini Inventory Management System.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Deployment Options](#deployment-options)
5. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 100MB for application + space for data

### Required Software
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- pip (comes with Python)
- Web browser (Chrome, Firefox, Edge, Safari)

---

## Quick Installation

### Windows

```batch
# 1. Open Command Prompt or PowerShell
# 2. Navigate to the project folder
cd path\to\inventory_app

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
streamlit run app.py
```

### macOS / Linux

```bash
# 1. Open Terminal
# 2. Navigate to the project folder
cd path/to/inventory_app

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
streamlit run app.py
```

---

## Detailed Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.9.x or higher
```

If Python is not installed:
- **Windows**: Download from python.org, check "Add to PATH" during installation
- **macOS**: `brew install python3` (requires Homebrew)
- **Linux**: `sudo apt install python3 python3-pip`

### Step 2: Extract the Project

Extract the downloaded zip file to your desired location:
- Windows: `C:\Users\YourName\inventory_app`
- macOS/Linux: `~/inventory_app`

### Step 3: Create Virtual Environment

A virtual environment keeps dependencies isolated:

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### Step 4: Activate Virtual Environment

```bash
# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- streamlit (Web framework)
- pandas (Data handling)
- openpyxl (Excel export)
- reportlab (PDF export)
- Pillow (Image handling)

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will:
1. Start a local server
2. Open your default browser
3. Display the dashboard

Default URL: `http://localhost:8501`

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Demo)

Free hosting with Streamlit Cloud:

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your repository

### Option 2: Local Network Access

To access from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Access via: `http://YOUR_IP:8501`

### Option 3: Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t inventory-app .
docker run -p 8501:8501 inventory-app
```

### Option 4: Windows Service

Use NSSM (Non-Sucking Service Manager) to run as Windows service:

```batch
nssm install InventoryApp "C:\path\to\venv\Scripts\streamlit.exe" "run app.py"
nssm set InventoryApp AppDirectory "C:\path\to\inventory_app"
nssm start InventoryApp
```

---

## Troubleshooting

### Issue: "python is not recognized"

**Solution**: Add Python to PATH
- Windows: Reinstall Python, check "Add to PATH"
- Or manually add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311` to PATH

### Issue: "pip is not recognized"

**Solution**: Use `python -m pip` instead:
```bash
python -m pip install -r requirements.txt
```

### Issue: "Permission denied" on macOS/Linux

**Solution**: Don't use sudo with pip in virtual environment:
```bash
# Wrong
sudo pip install -r requirements.txt

# Correct (inside activated venv)
pip install -r requirements.txt
```

### Issue: "Address already in use"

**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Database locked

**Solution**:
1. Close all instances of the application
2. Delete `data/inventory.db` to reset (warning: loses data)
3. Restart the application

### Issue: Images not showing

**Solution**:
1. Check that `data/images` folder exists
2. Verify file permissions
3. Ensure images are in supported formats (PNG, JPG, JPEG)

### Issue: Export not working

**Solution**: Ensure all dependencies are installed:
```bash
pip install openpyxl reportlab
```

---

## First Run Checklist

After installation, complete these steps:

1. ✅ Go to Settings → Store Name
   - Set your store name and contact info

2. ✅ Go to Settings → Currency
   - Select your currency

3. ✅ Go to Settings → Low Stock Alert
   - Configure alert thresholds

4. ✅ Add your first Category
   - Products → Categories → Add

5. ✅ Add your first Warehouse
   - Products → Warehouses → Add

6. ✅ Add your first Supplier
   - Suppliers → Add Supplier

7. ✅ Add your first Product
   - Products → Add Product

8. ✅ Add your first Customer
   - Customers → Add Customer

9. ✅ Create your first Invoice
   - Invoices → Create Invoice

---

## Need Help?

If you encounter issues not covered here:

1. Check the [README.md](README.md) for additional documentation
2. Contact support through CodeCanyon
3. Include the error message and steps to reproduce

---

**Installation Complete!** 🎉

Your inventory management system is ready to use.
