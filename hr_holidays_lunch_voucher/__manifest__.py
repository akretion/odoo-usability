# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Holidays Lunch Voucher',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'summary': 'Manage lunch vouchers in holidays requests',
    'description': '',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'hr_holidays_usability',
        'purchase',
        'onchange_helper',
        ],
    'data': [
        'security/ir.model.access.csv',
        'security/lunch_voucher_security.xml',
        'product_data.xml',
        'purchase_config_settings_view.xml',
        'wizard/lunch_voucher_purchase_view.xml',
        'lunch_voucher_attribution_view.xml',
        'hr_employee_view.xml',
        'hr_holidays_view.xml',
        'wizard/hr_holidays_to_payslip_view.xml',
        ],
    'installable': True,
}
