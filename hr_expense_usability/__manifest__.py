# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Expense Usability',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'summary': 'Better usability for the management of expenses',
    'description': '',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'hr_expense',
        'hr_expense_sequence',
        ],
    'data': [
        'private_car_data.xml',
        'hr_employee_view.xml',
        'hr_expense_view.xml',
        'product_view.xml',
        'security/expense_security.xml',
        ],
    'demo': ['private_car_demo.xml'],
    'installable': True,
}
