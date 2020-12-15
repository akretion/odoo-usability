# Copyright 2014-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Usability',
    'version': '14.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Better usability in base module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_bank.xml',
        'views/res_country.xml',
        'views/ir_module.xml',
        'views/ir_sequence.xml',
        ],
    'installable': True,
}
