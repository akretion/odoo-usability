# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Sale Stock Usability',
    'version': '10.0.1.0.3',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Small usability improvements to the sale_stock module',
    'description': """
Sale Stock Usability
====================

The usability enhancements include:

* *To invoice* filter on pickings filters on invoice_state = 2binvoiced AND state = done
* Add a tab with the list of related pickings in sale order form

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock'],
    'data': ['sale_stock_view.xml'],
    'installable': True,
}
