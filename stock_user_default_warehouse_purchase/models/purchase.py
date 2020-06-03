# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_pref_picking_type(self):
        in_type = self.env.user.context_default_warehouse_id.in_type_id
        return in_type.id if in_type else self._default_picking_type()

    picking_type_id = fields.Many2one(default=_default_pref_picking_type)
