# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_warehouse_id(self):
        warehouse = self.env.user.context_default_warehouse_id
        if not warehouse:
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.user.company_id.id)], limit=1)
        return warehouse

    warehouse_id = fields.Many2one(default=_default_warehouse_id)
