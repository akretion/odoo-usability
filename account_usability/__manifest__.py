# Copyright 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Usability',
    'version': '12.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'account',
        'base_view_inheritance_extension',
        'base_usability',  # needed only to access base_usability.group_nobody
                           # in v12, I may create a module only for group_nobody
        ],
    'data': [
        'account_view.xml',
        'account_report.xml',
        'account_invoice_report_view.xml',
        'partner_view.xml',
        'wizard/account_invoice_mark_sent_view.xml',
        'report/invoice_report.xml',
        ],
    'installable': True,
}
