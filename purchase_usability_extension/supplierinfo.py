# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    supplier_is_company = fields.Boolean(
        comodel_name='res.partner', related='name.is_company')
