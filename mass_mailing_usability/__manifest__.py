# Copyright 2019-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mass Mailing Campaigns Usability',
    'version': '14.0.1.0.0',
    'category': 'Marketing',
    'license': 'AGPL-3',
    'summary': 'Improve usability of mass mailing campaigns',
    'description': """
Mass Mailing Campaigns Usability
================================

Several small usability improvements on the module mass_mailing:

* show fields on link.tracker.click that are not displayed by default

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['mass_mailing', 'link_tracker_usability'],
    'data': [
        'views/link_tracker.xml',
        ],
    'installable': True,
}
