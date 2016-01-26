# -*- coding: utf-8 -*-
##############################################################################
#
#    L10n FR Intrastat Product ODS module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
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
    'name': 'L10n FR Intrastat Product ODS',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds an Aeroo ODS report on DEB',
    'description': """
L10n FR Intrastat Product ODS
=============================

This module will add an Aeroo ODS report on French Intrastat Product Declaration (DEB). It depends on the new intrastat modules that are currently under review in the following OCA PR: https://github.com/OCA/account-financial-reporting/pull/80 and https://github.com/OCA/l10n-france/pull/50

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['l10n_fr_intrastat_product', 'report_aeroo'],
    'data': ['report.xml'],
    'installable': True,
}
