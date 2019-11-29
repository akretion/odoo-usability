# Copyright 2014-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Usability',
    'version': '12.0.1.0.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in Warehouse management',
    'description': """
Stock Usability
===============

The usability enhancements include:
* display the source location on the tree view of the move lines of the pickings (by default, only the destination location is displayed).
* always display the field *Backorder* on the form view of picking (by default, this field is only displayed when it has a value, so the user doesn't know when the field has no value because he doesn't see the field !)
* add a group by Partner in the picking search view (particularly usefull for receptions)
* add graph view for pickings
* remove ability to translate stock.location, stock.location.route and stock.picking.type
* unactive view "stock.view_production_lot_form_simple" because it doesn't include smart buttons Locate and Traceability Report ; then we only use the main view "stock.view_production_lot_form" like in previous odoo versions

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'stock_view.xml',
        'procurement_view.xml',
        'wizard/stock_quantity_history_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
