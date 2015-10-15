# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Invoice Try Again module for Odoo
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

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def revert_to_tobeinvoiced(self):
        self.ensure_one()
        if self.invoice_state == 'invoiced':
            if self.invoice_id:
                raise UserError(_(
                    "This picking is linked to the invoice with "
                    "description '%s'. You should first delete this "
                    "invoice and try again.")
                    % self.invoice_id.name)
            self.invoice_state = '2binvoiced'
        else:
            raise UserError(_(
                "You can only do this when the Delivery Order "
                "has 'Invoice State' = 'Invoiced'."))
        return True
