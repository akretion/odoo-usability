# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.tools import float_compare, float_is_zero
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class ServiceQtyUpdate(models.TransientModel):
    _name = 'service.qty.update'
    _description = 'Wizard to update delivery qty on service lines'

    line_ids = fields.One2many('service.qty.update.line', 'parent_id', string="Lines")

    def run(self):
        self.ensure_one()
        prec = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self.line_ids:
            if float_compare(line.post_delivered_qty, line.order_qty, precision_digits=prec) > 0:
                raise UserError(_(
                    "On line '%s', the total delivered qty (%s) is superior to the ordered qty (%s).") % (line.name, line.post_delivered_qty, line.order_qty))
            fc_added = float_compare(line.added_delivered_qty, 0, precision_digits=prec)
            if fc_added < 0:
                raise UserError(_(
                    "On line '%s', the added quantity is negative.") % line.name)
            if fc_added > 0:
                line.process_line()
        return True


class ServiceQtyUpdateLine(models.TransientModel):
    _name = 'service.qty.update.line'
    _description = 'Lines of the wizard that updates delivery qty on service lines'

    parent_id = fields.Many2one(
        'service.qty.update', string='Wizard', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    name = fields.Char()
    name_readonly = fields.Char(related='name', string='Description')
    order_qty = fields.Float(
        string='Order Qty',
        digits=dp.get_precision('Product Unit of Measure'))
    order_qty_readonly = fields.Float(related='order_qty', string='Product Unit of Measure')
    pre_delivered_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'))
    pre_delivered_qty_readonly = fields.Float(related='pre_delivered_qty', string='Current Delivered Qty')
    added_delivered_qty = fields.Float(
        string='Added Delivered Qty',
        digits=dp.get_precision('Product Unit of Measure'))
    post_delivered_qty = fields.Float(
        compute='_compute_post_delivered_qty',
        string='Total Delivered Qty',
        digits=dp.get_precision('Product Unit of Measure'))
    uom_id = fields.Many2one('uom.uom', string='UoM', readonly=True)
    comment = fields.Char(string='Comment')

    @api.depends('pre_delivered_qty', 'added_delivered_qty')
    def _compute_post_delivered_qty(self):
        for line in self:
            line.post_delivered_qty = line.pre_delivered_qty + line.added_delivered_qty

    def process_line(self):
        # Write and message_post
        return

    # sale : qty_delivered
    # purchase : qty_received
