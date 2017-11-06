# coding: utf-8
# © 2017 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Web Export Usability',
    'version': '8.0.0.1.0',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'category': 'web',
    'description': """
Override of the module web for export features:

- set default export format to Excel


Roadmap:

- set default export type to 'Export all data'

""",
    'depends': ['web'],
    'data': [
    ],
    "external_dependencies": {
        "python": ['xlwt'],
    },
    'demo': [],
    'installable': True,
}
