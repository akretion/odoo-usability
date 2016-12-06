# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Other Report Engines',
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Allows the use of report engines other than Qweb',
    'description': """
Base Other Report Engines
=========================

This module inherit the method *_get_report_from_name()* to allow the use of report engines other than Qweb.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['report'],
    'installable': True,
}
