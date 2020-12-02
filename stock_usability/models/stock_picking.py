# Copyright 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
import logging

logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
#    _order = 'id desc'
    # In the stock module: _order = "priority desc, scheduled_date asc, id desc"
    # The problem is date asc

    partner_id = fields.Many2one(tracking=True)
    picking_type_id = fields.Many2one(tracking=True)
    move_type = fields.Selection(tracking=True)
    is_locked = fields.Boolean(tracking=True)

    def do_unreserve(self):
        res = super().do_unreserve()
        for pick in self:
            pick.message_post(body=_("Picking <b>unreserved</b>."))
        return res


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    name = fields.Char(translate=False)
