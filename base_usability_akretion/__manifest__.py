# Copyright 2014-2026 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Usability Akretion',
    'version': '20.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Better usability in base module',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['base'],
    'data': [
        'security/group.xml',
        'views/res_partner.xml',
        'views/res_country.xml',
        'views/res_country_state.xml',
        'views/res_company.xml',
        'views/ir_config_parameter.xml',
        'views/ir_module.xml',
        'views/ir_sequence.xml',
        ],
    'installable': True,
}
