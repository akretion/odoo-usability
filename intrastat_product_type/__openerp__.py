# -*- coding: utf-8 -*-
##############################################################################
#
#    Intrastat Product Type module for Odoo
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
    'name': 'Intrastat Product Type',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Adds a special field Intrastat Type on Products',
    'description': """
Intrastat Product Type
======================

This module is designed for a very special usage scenario. Some companies want to handle the delivery of services the same way as they handle the delivery of goods ; they want to show the services in the delivery note, etc. So, those companies configure the services with Type = *Consumable*. This works well to have the services on the outgoing pickings, but it is a problem for the intrastat declarations.

This module adds a field *Intrastat Type* on the Product Form with 2 possible options: *Product* or *Service*. The intrastat declaration will use this field instead of the native *Type* field.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['intrastat_product', 'l10n_fr_intrastat_service'],
    'data': ['product_view.xml'],
    'post_init_hook': 'set_intrastat_type_on_products',
    'installable': True,
}
