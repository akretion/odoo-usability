# Copyright 2026 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Valuation XLSX History",
    "summary": "Schedule stock valuation and variation exports and keep their history",
    "version": "18.0.1.0.0",
    "category": "Inventory/Inventory",
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "license": "AGPL-3",
    "depends": ["stock_valuation_xlsx"],
    "data": [
        "security/ir.model.access.csv",
        "security/stock_valuation_xlsx_history_security.xml",
        "data/ir_cron.xml",
        "views/stock_valuation_xlsx_history_views.xml",
        "views/stock_valuation_xlsx_export_views.xml",
    ],
    "installable": True,
}
