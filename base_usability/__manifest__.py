# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Usability',
    'version': '12.0.0.1.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Better usability in base module',
    'description': """
Base Usability
==============

This module adds *track_visibility='onchange'* on all the important fields of the Partner object.

By default, Odoo doesn't display the title field on all the partner form views. This module fixes it (it replaces the module base_title_on_partner).

It also adds a log message at INFO level when sending an email via SMTP.

It displays the local modules with installable filter.
A group by 'State' is added to module search view.

It provides a _display_report_header method on the res.company object and
_display_full_address on res.partner which are useful for reporting.
    """,
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
        ],
    'installable': True,
}
