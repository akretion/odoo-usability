# Copyright 2023 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Subcontracting Usability',
    'version': '14.0.1.0.0',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on mrp_subcontracting',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['mrp_subcontracting'],
    'data': [
        'views/mrp_bom.xml',
    ],
    'installable': True,
}
