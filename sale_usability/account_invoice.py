# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Usability Extension module for Odoo
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

from openerp import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # reverse of the native M2M invoice_lines field on sale.order.line
    sale_line_ids = fields.Many2many(
        'sale.order.line', 'sale_order_line_invoice_rel', 'invoice_id',
        'order_line_id', 'Sale Order Lines', readonly=True)
