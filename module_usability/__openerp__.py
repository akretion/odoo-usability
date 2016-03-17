# coding: utf-8
# © 2016 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Module Usability',
    'version': '8.0.0.0.0',
    'category': 'Base',
    'summary': "Module views improved",
    'description': """
Remove 'Application' filter, add group by 'State'

Why this module ?

- We don't install Applications modules directly but install lower level modules first
- We must take care of modules state: it's a really precious information

Contributors: David BEAL
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'base',
        ],
    'data': [
        'view.xml',
    ],
    'installable': True,
}
