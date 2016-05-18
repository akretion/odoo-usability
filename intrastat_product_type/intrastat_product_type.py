# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>


from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    intrastat_type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service'),
        ], string='Intrastat Type', default='product', required=True,
        help="Type of product used for the intrastat declarations. "
        "For example, you can configure a product with "
        "'Product Type' = 'Consumable' and 'Intrastat Type' = 'Service'.")

    @api.multi
    @api.constrains('type', 'intrastat_type')
    def check_intrastat_type(self):
        for pt in self:
            if pt.intrastat_type == 'product' and pt.type == 'service':
                raise ValidationError(_(
                    "On the product %s, you cannot set Product Type to "
                    "'Service' and Intrastat Type to 'Product'.") % pt.name)
            if pt.intrastat_type == 'service' and pt.type == 'product':
                raise ValidationError(_(
                    "On the product %s, you cannot set Intrastat Type to "
                    "'Service' and Product Type to 'Stockable product' "
                    "(but you can set Product Type to 'Consumable' or "
                    "'Service').") % pt.name)

    @api.multi
    def onchange_type(self, type):
        res = super(ProductTemplate, self).onchange_type(type)
        if 'value' not in res:
            res['value'] = {}
        if type == 'product':
            res['value']['intrastat_type'] = 'product'
        elif type == 'service':
            res['value']['intrastat_type'] = 'service'
        return res


class L10nFrIntrastatServiceDeclaration(models.Model):
    _inherit = "l10n.fr.intrastat.service.declaration"

    def _is_service(self, invoice_line):
        if invoice_line.product_id.intrastat_type == 'service':
            return True
        else:
            return False


class IntrastatProductDeclaration(models.Model):
    _inherit = 'intrastat.product.declaration'

    def _is_product(self, invoice_line):
        if (
                invoice_line.product_id and
                invoice_line.product_id.intrastat_type == 'product'):
            return True
        else:
            return False
