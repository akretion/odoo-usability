# -*- coding: utf-8 -*-
# Copyright 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Aged Partner Balance from Partner',
    'version': '10.0.0.1.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Direct access to the aged partner balance report from the partner form',
    'description': """
Aged Partner Balance from Partner
=================================

This module adds a button on the partner form view (the icon on the button is a banknote) to easily open the detailed aged partner balance of the partner in PDF format.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_financial_report_qweb'],
    'data': ['partner_view.xml'],
    'installable': True,
}
