# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CommissionProfile(models.Model):
    _inherit = 'commission.profile'

    commission_product_id = fields.Many2one(
        'product.product', string='Specific Commission Product', ondelete='restrict',
        check_company=True,
        domain=[('type', '=', 'service')],
        help="If not set, Odoo will use the commission product configured on the accounting "
        "configuration page."
        )

