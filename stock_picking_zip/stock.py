# coding: utf-8
# © 2016 David BEAL @ Akretion <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    short_zip = fields.Char(
        string='Zip', compute='_compute_short_zip', store=True,
        help="Troncated zip code to a limited chars number allowing group by")

    def _set_short_zip_size(self):
        """ if zip is 69100, then short zip is 69 """
        return 2

    @api.depends('partner_id')
    @api.multi
    def _compute_short_zip(self):
        for rec in self:
            if rec.partner_id and rec.partner_id.zip:
                rec.short_zip = rec.partner_id.zip[:self._set_short_zip_size()]
