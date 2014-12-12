# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Invoice Service from Delivery module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
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
    'name': 'Stock Invoice Service from Delivery',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Add the service lines of the sale order when invoicing from delivery',
    'description': """
Stock Invoice Service from Delivery
===================================

In OpenERP 6.1, when invoicing from the delivery order, OpenERP would get the service lines of the sale order and add them on the invoice. This feature has been dropped in OpenERP 7.0 and some users are missing this issue, which lead to the following bug : https://bugs.launchpad.net/openobject-addons/+bug/1167330

This module restores this feature. At the end of December 2013, this bug was fixed by OpenERP SA in the 7.0 branch. But, after this fix, a bug remained: https://github.com/odoo/odoo/issues/4201 I solved the remaining bug here: https://github.com/odoo/odoo/pull/4204 So you should just get this patch with up-to-date stable 7.0 branch and not use this module.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [],
    'images': [],
    'installable': True,
    'active': False,
}
