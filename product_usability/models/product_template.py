# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name = fields.Char(
        track_visibility='onchange')

    type = fields.Selection(
        track_visibility='onchange')

    categ_id = fields.Many2one(
        track_visibility='onchange')

    list_price = fields.Float(
        track_visibility='onchange')

    sale_ok = fields.Boolean(
        track_visibility='onchange')

    purchase_ok = fields.Boolean(
        track_visibility='onchange')
        
    active = fields.Boolean(
        track_visibility='onchange')

    def show_product_price_history(self):
        self.ensure_one()
        products = self.env['product.product'].search(
            [('product_tmpl_id', '=', self._context['active_id'])])
        action = self.env['ir.actions.act_window'].for_xml_id(
            'product_usability', 'product_price_history_action')
        action.update({
            'domain': "[('product_id', 'in', %s)]" % products.ids,
        })
        return action
