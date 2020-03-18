# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Usability',
    'version': '12.0.0.1.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Better usability in base module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'security/group.xml',
        'views/partner_view.xml',
        'views/partner_bank_view.xml',
        'views/users_view.xml',
        'views/country_view.xml',
        'views/module_view.xml',
        'views/base_view.xml',
        ],
    'installable': True,
}
