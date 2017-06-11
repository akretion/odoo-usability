# -*- encoding: utf-8 -*-
##############################################################################
#
#    L10n FR Infogreffe connector module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com/)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Infogreffe connector',
    'version': '10.0.0.1.0',
    'category': 'French Localization',
    'license': 'AGPL-3',
    'summary': 'Download info from infogreffe.fr',
    'description': """
Infogreffe connector
====================

This module adds a button on Partner form view in the *Accounting* tab to download data from Infogreffe. If the Partner has a SIREN in OpenERP, it will check if the company has *Key Figures* in Infogreffe, get the latest *Key Figures* and copy to OpenERP :

* Turnover

* Profit

* Headcount

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['l10n_fr_siret'],
    'external_dependencies': {'python': ['requests', 'bs4']},
    'data': ['partner_view.xml'],
    'active': False,
}
