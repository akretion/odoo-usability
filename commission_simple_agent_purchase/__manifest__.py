# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Commission Simple Agent Purchase',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Glue module between commission_simple_agent and purchase',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        'commission_simple_agent',
        'purchase',
        ],
    'data': [
        'views/commission_result.xml',
        'views/commission_profile.xml',
        'wizards/res_config_settings.xml',
        ],
    'installable': True,
}
