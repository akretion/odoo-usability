# Copyright 2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Picking Batch Usability',
    'version': '14.0.1.0.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in Batch Pickings',
    'description': """
Stock Picking Batch Usability
=============================

The usability enhancements include:

* add batch_id on picking form view
* when creating a batch from a list of pickings, raise an error if a picking is already linked to a batch.
* when creating a batch from a list of pickings, display the form view of the batch after validation of the wizard

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['stock_picking_batch'],
    'data': [
        'views/stock_picking.xml',
        ],
    'installable': True,
}
