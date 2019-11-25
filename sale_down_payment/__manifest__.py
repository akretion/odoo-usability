# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Down Payment',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Link payment to sale orders',
    'description': """
Sale Down Payment
=================

This module adds a link between payments and sale orders. It allows to see down payments directly on the sale order form view.

After processing a bank statement, you can start a wizard to link unreconciled incoming payments to a sale order. There is also a button *Register Payment* on the sale order.

This module targets B2B companies that don't want to generate a down payment invoice for an advanced payment.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': [
        'wizard/account_bank_statement_sale_view.xml',
        'views/account_bank_statement.xml',
        'views/sale.xml',
        'views/account_move_line.xml',
        'views/account_payment.xml',
        ],
    'installable': True,
}
