# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Auto Invoice Method module for Odoo
#    Copyright (C) 2013-2015 Akretion (http://www.akretion.com)
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

from openerp import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def wkf_confirm_order(self):
        for po in self:
            if (
                    po.invoice_method == 'picking' and all([
                        line.product_id and
                        line.product_id.type == 'service'
                        for line in po.order_line])):
                po.invoice_method = 'order'
        return super(PurchaseOrder, self).wkf_confirm_order()
