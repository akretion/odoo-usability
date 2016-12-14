# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Layout Category per Order',
    'version': '10.0.1.0.0',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': 'Allow to create per-order sale report categories',
    'description': """
Sale Layout Category per Order
==============================

With this module, you can have:

* generic Sale report layout categories (native)
* per-order Sale Report categories (added by this module)

One limitation to be aware of: when you create a sale report layout category from the form view of a new quotation that hasn't been saved yet, the default affectation to the sale order won't work (for obvious technical reasons).

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': ['sale_view.xml'],
    'installable': True,
}
