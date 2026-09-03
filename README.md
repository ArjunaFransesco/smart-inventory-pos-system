# 📦 Smart Inventory & Point-of-Sale (POS) Information System

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-Solid_Dark_UI-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An enterprise-grade **Warehouse Management & Point-of-Sale (POS) Information System** engineered for multi-category stock tracking, automated reorder level alerts, cashier billing, and gross margin analytics with a crisp, solid enterprise user interface.

---

## 📌 Business Value & Problem Statement

Retail warehouses and distribution centers face major operational risks from stockouts (loss of sales) and overstocking (capital tied in carrying costs). This Information System delivers:

1. **Automated Safety Stock & Reorder Triggering**: Continuously evaluates current stock against dynamic safety thresholds:
   $$\text{Reorder Trigger} = \mathbb{I}\left(Q_{\text{stock}} \le Q_{\text{min}}\right)$$
2. **Economic Order Quantity (EOQ) Optimization**:
   $$\text{EOQ} = \sqrt{\frac{2DS}{H}}$$
3. **High-Throughput POS Terminal**: Instant cart calculations, multi-payment support (Cash, QRIS, EDC, Transfer), and invoice generation.

---

## 🏗️ System Architecture & Database Relational Schema

```
┌─────────────────────────────────────────────────────────────┐
│                    Web UI Layer (Tailwind CSS)              │
│    [Dashboard]      [Inventory Master]       [POS Terminal] │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Flask Application Controller Layer             │
│        Routing, Business Logic, Validation, Transactions    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   SQLite Relational Database                │
│    [Categories] ──< [Products] >── [Suppliers]              │
│                           │                                 │
│                           ▼                                 │
│    [Transactions] ──< [Transaction_Items]                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Functional Modules

* **📊 Executive Warehouse Dashboard**: Real-time KPI summary (Total SKUs, Wholesale Stock Valuation, Daily POS Revenue, Critical Reorder Alerts).
* **📦 Master Inventory Management**: Full CRUD operations, category segmentation, cost vs selling price margins, and low-stock badge indicators.
* **💳 Interactive POS Cashier Terminal**: Fast product selection grid, real-time quantity modifiers, multiple payment methods, and automated receipt invoice generator.
* **📈 Inventory Analytics Notebook**: Jupyter notebook analyzing inventory turnover ratios, gross margins, and Economic Order Quantity (EOQ) formulations.

---

## 📁 Repository Structure

```
smart-inventory-pos-system/
├── app/
│   └── templates/
│       ├── base.html          # Solid enterprise layout & navigation
│       ├── dashboard.html     # Real-time warehouse KPI dashboard
│       ├── inventory.html     # Inventory master catalog table
│       └── pos.html           # Cashier checkout terminal interface
├── data/
│   └── inventory_pos.db       # Relational SQLite database with seed data
├── notebooks/
│   └── inventory_analytics_and_reorder_optimization.ipynb # Analytics notebook
├── app.py                     # Flask web server & REST API controller
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
└── README.md                  # Enterprise documentation
```

---

## ⚡ Quickstart & Setup

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/ArjunaFransesco/smart-inventory-pos-system.git
cd smart-inventory-pos-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 👤 Author & Portfolio
- **Author**: **[Arjuna Fransesco](https://github.com/ArjunaFransesco)**
- **GitHub Repositories**: [https://github.com/ArjunaFransesco?tab=repositories](https://github.com/ArjunaFransesco?tab=repositories)
- **Live Portfolio Website**: [https://arjunafransesco.github.io/arjuna-portfolio/](https://arjunafransesco.github.io/arjuna-portfolio/)
- **LinkedIn**: [https://www.linkedin.com/in/arjunafransesco](https://www.linkedin.com/in/arjunafransesco)


<!-- Last Maintenance Audit: 2026-09-03 -->
