# Copyright 2017-2023 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Partner Reference',
    'version': '16.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': "Improve usage of partner's Internal Reference",
    'description': """
Base Partner Reference
======================

* Adds Internal Reference in partner tree view

* Adds Internal Reference in name_get()

* Adds unicity constraint on Internal Reference
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['base'],
    'data': ['views/res_partner.xml'],
    'post_init_hook': 'update_partner_display_name',
    'installable': True,
}
