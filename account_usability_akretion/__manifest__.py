# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Usability',
    'version': '16.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account module',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        'account',
        'base_usability',  # needed only to access base_usability.group_nobody
        ],
    'data': [
        'views/account_account.xml',
        'views/account_group.xml',
#        'views/account_bank_statement.xml',
        'views/account_invoice_report.xml',
        'views/account_journal.xml',
        'views/account_move.xml',
        'views/account_analytic_line.xml',
        'views/account_menu.xml',
        'views/account_tax.xml',
#        'views/product.xml',  # TODO
        'views/res_company.xml',
        'views/account_report.xml',
        'wizard/account_invoice_mark_sent_view.xml',
        'wizard/account_group_generate_view.xml',
        'wizard/account_payment_register_views.xml',
        'security/ir.model.access.csv',
#        'report/invoice_report.xml',  # TODO
        ],
#    'qweb': ['static/src/xml/account_payment.xml'],
    'installable': True,
#    "post_init_hook": "post_init_hook",
}
