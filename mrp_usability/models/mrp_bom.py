# Copyright 2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    code = fields.Char(tracking=50)
    type = fields.Selection(tracking=20)
    product_tmpl_id = fields.Many2one(tracking=10)
    product_id = fields.Many2one(tracking=15)
    product_qty = fields.Float(tracking=30)
    product_uom_id = fields.Many2one(tracking=35)
    ready_to_produce = fields.Selection(tracking=90)
    picking_type_id = fields.Many2one(tracking=60)
    consumption = fields.Selection(tracking=40)
