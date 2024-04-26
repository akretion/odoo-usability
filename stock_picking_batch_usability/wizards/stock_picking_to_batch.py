# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class StockPickingToBatch(models.TransientModel):
    _inherit = 'stock.picking.to.batch'

    # add 'in_progress' in domain
    batch_id = fields.Many2one(domain="[('state', 'in', ('draft', 'in_progress'))]")
    mode = fields.Selection(default='new')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        pickings = self.env['stock.picking'].browse(self.env.context.get('active_ids'))
        for picking in pickings:
            if picking.batch_id:
                raise UserError(_(
                    "The picking %(picking)s is already part of batch %(batch)s.",
                    picking=picking.display_name,
                    batch=picking.batch_id.display_name))
        return res

    def attach_pickings(self):
        super().attach_pickings()
        if self.mode == 'new':
            pickings = self.env['stock.picking'].browse(self.env.context.get('active_ids'))
            batch_id = pickings[0].batch_id.id
        elif self.mode == 'existing':
            batch_id = self.batch_id.id
        else:
            raise UserError('It should never happen')
        action = self.env["ir.actions.actions"]._for_xml_id("stock_picking_batch.stock_picking_batch_action")
        action.update({
            'view_mode': 'form,tree',
            'res_id': batch_id,
            'views': False,
            })
        return action
