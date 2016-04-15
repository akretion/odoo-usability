# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>


from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    intrastat_type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service'),
        ], string='Intrastat Type', default='product', required=True,
        help="Type of product used for the intrastat declarations. "
        "For example, you can configure a product with "
        "'Product Type' = 'Consumable' and 'Intrastat Type' = 'Service'.")


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
