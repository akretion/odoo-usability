# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Holidays Usability',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'summary': 'Better usability for the management of holidays',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['hr_holidays', 'hr_public_holidays'],
    'data': [
        'report/hr_holidays_employee_counter_view.xml',
        'hr_holidays_view.xml',
        'hr_holidays_mail.xml',
        'base_config_settings_view.xml',
        'hr_employee_view.xml',
        'security/holiday_security.xml',
        'security/ir.model.access.csv',
        'wizard/hr_holidays_mass_allocation_view.xml',
        'wizard/hr_holidays_to_payslip_view.xml',
        ],
    'installable': True,
}
