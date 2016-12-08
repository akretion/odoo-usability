# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'POS Sale Report',
    'version': '10.0.1.0.0',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': 'Add a graph via on that aggregate sale orders and pos orders',
    'description': """
In the *Point of sales > Reporting* menu, add a new entry *POS + Sale Orders Analysis* that show sale statistics per products that aggregate sale orders and pos orders.

Also add direct access to Sales statistics on the Product form view and Product Variants form view (Menu entry *Sales Statistics* in the *Action* drop down list).

This module has been written by  Alexis de Lattre
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale', 'sale'],
    'data': [
        'report/pos_sale_report_view.xml',
        'product_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
