# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Developer Menu',
    'version': '12.0.0.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': "Menu Shortcut for developer usage",
    'description': """
Developer menu
==============

Add a menu which gather main technical used menus

How to use it
-------------

Ensure you're in ERP manager group and go to configuration page
near `Technical` menu

This module has been written by David Béal
from Akretion <david.beal@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mail'],
    'data': [
        'menu_view.xml'
    ],
    'installable': True,
}
