# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    commission_product_id = fields.Many2one(
        'product.product', string='Commission Product', ondelete='restrict', check_company=True,
        domain=[('type', '=', 'service')])
    commission_po_config = fields.Selection([
        ('single_line', 'Single Line'),
        ('details', 'One line per commission line'),
        ], default='details', string="Purchase Order Configuration")
