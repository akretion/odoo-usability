# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Picking Type Default Partner module for Odoo
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

# For an unknown reasons, it doesn't work when using the new API
# with this module it breaks in an SQL query trying to select the
# "picking_type_code" on stock.picking although it is a related field
# store=False So I keep it with the old API for the moment
from openerp.osv import orm, fields


class StockPickingType(orm.Model):
    _inherit = 'stock.picking.type'

    _columns = {
        'default_partner_id': fields.many2one(
            'res.partner', 'Default Partner', ondelete='restrict',
            help="If set, it will be the default partner on this type "
            "of pickings."),
    }


class StockPicking(orm.Model):
    _inherit = 'stock.picking'

    def _default_partner_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        if context.get('default_picking_type_id'):
            picktype = self.pool['stock.picking.type'].browse(
                cr, uid, context.get('default_picking_type_id'),
                context=context)
            if picktype.default_partner_id:
                return picktype.default_partner_id.id
        return False

    _defaults = {
        'partner_id': _default_partner_id,
    }
