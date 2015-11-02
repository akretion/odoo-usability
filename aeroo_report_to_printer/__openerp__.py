# -*- coding: utf-8 -*-
##############################################################################
#
#    Aeroo Report to Printer module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Aeroo Report to Printer',
    'version': '0.1',
    'category': 'Aeroo',
    'license': 'AGPL-3',
    'summary': 'Connect aeroo_report to base_report_to_printer',
    'description': """
Aeroo Report to Printer
=======================

There is a module *report_aeroo_direct_print* in https://github.com/aeroo/aeroo_reports that adds support for CUPS printing, but it's not as mature and clean as the OCA module *base_report_to_printer* from https://github.com/OCA/report-print-send.

And I want to use the best of both world : the best reporting engine (Aeroo) with the best CUPS printing module (base_report_to_printer). So I developped this small glue module.

You will find some sample code to use this module in the comments of the main Python file.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'base_report_to_printer',
        'report_aeroo',
        'base_other_report_engines',
        ],
    'installable': True,
}
