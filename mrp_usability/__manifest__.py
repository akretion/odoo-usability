# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Usability',
    'version': '14.0.1.0.0',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on manufacturing',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mrp'],
    'data': [
        'views/mrp_production.xml',
        'views/product_template.xml',
    #    'report/mrp_report.xml'  # TODO
    ],
    'installable': True,
}
