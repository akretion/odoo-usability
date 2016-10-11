# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Payment Security module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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
    'name': 'Account Payment Security',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Only members of Account Payment can create/write on bank accounts',
    'description': """
Account Payment Security
========================

By default in OpenERP, members of the group *Contact Creation* can create and modify bank accounts ; this can be a risk, as explained in this mail : https://lists.launchpad.net/openerp-community/msg01035.html

With this module, only the members of the group *Accounting / Payments* can create and modify bank accounts. Also, some rights on the configuration of bank accounts (res.partner.bank.type and res.partner.bank.type.field) are moved from the group *Contact Creation* to *Financial Manager*.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
""",
    'author': 'Akretion',
    'depends': ['account_payment'],
    'data': [
        'security/ir.model.access.csv',
        ],
    'active': False,
}
