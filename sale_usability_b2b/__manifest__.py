# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Usability B2B',
    'version': '10.0.1.0.0',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': 'Show amount untaxed by default in sale graphs/pivot',
    'description': """
Sale Usability B2B
==================

By default, Odoo shows the amount with taxes in the pivot, graph and calendar views, which is confusing for B2B companies. This module changes this to show by default with amount without taxes.

Note that you should also install the module *sale_usability*, which adds amount untaxed in tree views with a sum.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': ['sale_view.xml'],
    'installable': True,
}
