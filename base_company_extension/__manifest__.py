# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Company Extension',
    'version': '10.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Adds capital and title on company',
    'description': """
Base Company Extension
======================

This module adds 2 fields on the Company :

* *Capital Amount*

* *Legal Form*
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    # I depend on base_usability only for _report_company_legal_name()
    'depends': ['base_usability'],
    'data': ['company_view.xml'],
    'installable': True,
}
