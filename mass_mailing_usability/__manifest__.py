# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mass Mailing Campaigns Usability',
    'version': '10.0.1.0.0',
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
    'website': 'http://www.akretion.com',
    'depends': ['mass_mailing'],
    'data': [
        'link_tracker_view.xml',
        ],
    'installable': True,
}
