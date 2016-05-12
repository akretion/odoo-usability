# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>


from openerp.osv import orm, fields


class ProductTemplate(orm.Model):
    _inherit = 'product.template'

    _columns = {
        'intrastat_type': fields.selection([
            ('product', 'Product'),
            ('service', 'Service'),
            ], string='Intrastat Type', required=True,
            help="Type of product used for the intrastat declarations. "
            "For example, you can configure a product with "
            "'Product Type' = 'Consumable' and 'Intrastat Type' = 'Service'.")
        }

    _defaults = {
        'intrastat_type': 'product',
    }


class ReportIntrastatService(orm.Model):
    _inherit = "report.intrastat.service"

    def _is_service(self, cr, uid, invoice_line, context=None):
        if invoice_line.product_id.intrastat_type == 'service':
            return True
        else:
            return False


class ReportIntrastatProduct(orm.Model):
    _inherit = 'report.intrastat.product'

    def _is_product(self, cr, uid, invoice_line, context=None):
        if (
                invoice_line.product_id and
                invoice_line.product_id.intrastat_type == 'product'):
            return True
        else:
            return False
